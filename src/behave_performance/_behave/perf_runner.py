from __future__ import absolute_import, print_function, with_statement

import six

from behave_performance.events import BehaveEvents,PerfEvents
from behave.formatter._registry import make_formatters
from behave.api.runner import ITestRunner
from behave.runner import Context
from behave._types import ExceptionUtil
from behave.capture import CaptureController
from behave.step_registry import registry as the_step_registry

if six.PY2:
    # -- USE PYTHON3 BACKPORT: With unicode traceback support.
    import traceback2 as traceback
else:
    import traceback


#SO we need to make our own runner plugin
#It needs to have the features passed to it
#


class PerfRunner(object):
    """Test runner for a behave model (features).
    Provides the core functionality of a test runner and
    the functional API needed by model elements.

    .. attribute:: aborted

          This is set to true when the user aborts a test run
          (:exc:`KeyboardInterrupt` exception). Initially: False.
          Stored as derived attribute in :attr:`Context.aborted`.

    .. attribute:: captured

        If any output capture is enabled, provides access to a
        :class:`~behave.capture.Captured` object that contains a snapshot
        of all captured data (stdout/stderr/log).

        .. versionadded:: 1.3.0
    """
    # pylint: disable=too-many-instance-attributes

    def __init__(self,id:str, name:str, config,features=None, step_registry=None,hooks={}):
        self.id = id
        self.name = name
        self.config = config
        self.features = features or []
        self.hooks = hooks
        self._undefined_steps = []
        self.step_registry = step_registry
        self.capture_controller = CaptureController(config)
        self.context = None
        self.feature = None
        self.hook_failures = 0
        stream_openers = self.config.outputs
        self.formatters = make_formatters(self.config, stream_openers)

    @property
    def undefined_steps(self):
        return self._undefined_steps

    @property
    def aborted(self):
        """Indicates that test run is aborted by the user or system."""
        if self.context:
            return self.context.aborted
        # -- OTHERWISE
        return False

    @aborted.setter
    def aborted(self, value):
        """Mark the test run as aborted."""
        # pylint: disable=protected-access
        assert self.context, "REQUIRE: context, but context=%r" % self.context
        if self.context:
            self.context._set_root_attribute("aborted", bool(value))

    # DISABLED: aborted = property(_get_aborted, _set_aborted, doc="...")

    def abort(self, reason=None):
        """Abort the test run.

        .. versionadded:: 1.2.7
        """
        if self.context is None:
            return  # -- GRACEFULLY IGNORED.

        # -- NORMAL CASE:
        # SIMILAR TO: self.aborted = True
        self.context.abort(reason=reason)

    def run_hook(self, name, context, *args):
        #TODO Event hook 
        if not self.config.dry_run and (name in self.hooks):
            try:
                with context.use_with_user_mode():
                    self.hooks[name](context, *args)
            # except KeyboardInterrupt:
            #     self.abort(reason="KeyboardInterrupt")
            #     if name not in ("before_all", "after_all"):
            #         raise
            except Exception as e:  # pylint: disable=broad-except
                # -- HANDLE HOOK ERRORS:
                use_traceback = False
                if self.config.verbose:
                    use_traceback = True
                    ExceptionUtil.set_traceback(e)
                extra = u""
                if "tag" in name:
                    extra = "(tag=%s)" % args[0]

                error_text = ExceptionUtil.describe(e, use_traceback).rstrip()
                error_message = u"HOOK-ERROR in %s%s: %s" % (name, extra, error_text)
                print(error_message)
                self.hook_failures += 1
                if "tag" in name:
                    # -- SCENARIO or FEATURE
                    statement = getattr(context, "scenario", context.feature)
                elif "all" in name:
                    # -- ABORT EXECUTION: For before_all/after_all
                    self.abort(reason="HOOK-ERROR in hook=%s" % name)
                    statement = None
                else:
                    # -- CASE: feature, scenario, step
                    statement = args[0]

                if statement:
                    # -- CASE: feature, scenario, step
                    statement.hook_failed = True
                    if statement.error_message:
                        # -- NOTE: One exception/failure is already stored.
                        #    Append only error message.
                        statement.error_message += u"\n"+ error_message
                    else:
                        # -- FIRST EXCEPTION/FAILURE:
                        statement.store_exception_context(e)
                        statement.error_message = error_message

    def setup_capture(self):
        if not self.context:
            self.context = Context(self)
        self.capture_controller.setup_capture(self.context)

    def start_capture(self):
        self.capture_controller.start_capture()

    def stop_capture(self):
        self.capture_controller.stop_capture()

    def teardown_capture(self):
        self.capture_controller.teardown_capture()

    @property
    def captured(self):
        """Return the current state of the captured output/logging
        (as captured object).
        """
        return self.capture_controller.captured

    def run_model(self, features=None):
        # pylint: disable=too-many-branches
        if not self.context:
            self.context = Context(self)
        if self.step_registry is None:
            self.step_registry = the_step_registry
        if features is None:
            features = self.features

        # -- ENSURE: context.execute_steps() works in weird cases (hooks, ...)
        context = self.context
        self.hook_failures = 0
        self.setup_capture()
        self.run_hook("before_all", context)

        run_feature = not self.aborted
        failed_count = 0
        undefined_steps_initial_size = len(self.undefined_steps)
        for feature in features:
            if run_feature:
                try:
                    self.feature = feature
                    for formatter in self.formatters:
                        formatter.uri(feature.filename)

                    failed = feature.run(self)
                    if failed:
                        failed_count += 1
                        if self.config.stop or self.aborted:
                            # -- FAIL-EARLY: After first failure.
                            run_feature = False
                except KeyboardInterrupt:
                    self.abort(reason="KeyboardInterrupt")
                    failed_count += 1
                    run_feature = False

            # -- ALWAYS: Report run/not-run feature to reporters.
            # REQUIRED-FOR: Summary to keep track of untested features.
            for reporter in self.config.reporters:
                reporter.feature(feature)

        # -- AFTER-ALL:
        # pylint: disable=protected-access, broad-except
        cleanups_failed = False
        self.run_hook("after_all", self.context)
        try:
            self.context._do_cleanups()   # Without dropping the last context layer.
        except Exception:
            cleanups_failed = True

        if self.aborted:
            print("\nABORTED: By user.")
        for formatter in self.formatters:
            formatter.close()
        for reporter in self.config.reporters:
            reporter.end()

        failed = ((failed_count > 0) or self.aborted or (self.hook_failures > 0)
                  or (len(self.undefined_steps) > undefined_steps_initial_size)
                  or cleanups_failed)
                  # XXX-MAYBE: or context.failed)
        return (self.id,self.name,features,failed)

    def run(self):
        """
        Implements the run method by running the model.
        """
        self.context = Context(self)
        return self.run_model()

# -----------------------------------------------------------------------------
# REGISTER RUNNER-CLASSES:
# -----------------------------------------------------------------------------
ITestRunner.register(PerfRunner)


