from __future__ import absolute_import, print_function, with_statement

import os.path

import six

from testcase_filter import TestCaseFilter
from _behave.perf_runner import PerfRunner
from _behave.slice import Slice
from behave.runner import Context, path_getrootdir
from behave.exception import ConfigError
from behave.configuration import Configuration, LogLevel
from behave.runner_util import \
    collect_feature_locations, parse_features, \
    exec_file, load_step_modules, PathManager
from behave.step_registry import registry as the_step_registry
from enum import Enum

if six.PY2:
    # -- USE PYTHON3 BACKPORT: With unicode traceback support.
    import traceback2 as traceback
else:
    import traceback


class PerfRunnerBuilder():
    """Creates runners
      * setup paths
      * loads environment hooks
      * loads step definitions
      * select feature files, parses them and creates model (elements)
    """

    def __init__(self, config):
        self.config:Configuration = config
        self.path_manager = PathManager()
        self.base_dir = None
        self.hooks = {}
        self.features = []
        self.formatters = []
        self.setup()

    def setup_paths(self):
        # pylint: disable=too-many-branches, too-many-statements
        if self.config.paths:
            if self.config.verbose:
                print("Supplied path:", \
                      ", ".join('"%s"' % path for path in self.config.paths))
            first_path = self.config.paths[0]
            if hasattr(first_path, "filename"):
                # -- BETTER: isinstance(first_path, FileLocation):
                first_path = first_path.filename
            base_dir = first_path
            if base_dir.startswith("@"):
                # -- USE: behave @features.txt
                base_dir = base_dir[1:]
                file_locations = self.feature_locations()
                if file_locations:
                    base_dir = os.path.dirname(file_locations[0].filename)
            base_dir = os.path.abspath(base_dir)

            # supplied path might be to a feature file
            if os.path.isfile(base_dir):
                if self.config.verbose:
                    print("Primary path is to a file so using its directory")
                base_dir = os.path.dirname(base_dir)
        else:
            if self.config.verbose:
                print('Using default path "./features"')
            base_dir = os.path.abspath("features")

        # Get the root. This is not guaranteed to be "/" because Windows.
        root_dir = path_getrootdir(base_dir)
        new_base_dir = base_dir
        steps_dir = self.config.steps_dir
        environment_file = self.config.environment_file

        while True:
            if self.config.verbose:
                print("Trying base directory:", new_base_dir)

            if os.path.isdir(os.path.join(new_base_dir, steps_dir)):
                break
            if os.path.isfile(os.path.join(new_base_dir, environment_file)):
                break
            if new_base_dir == root_dir:
                break

            new_base_dir = os.path.dirname(new_base_dir)

        if new_base_dir == root_dir:
            if self.config.verbose:
                if not self.config.paths:
                    print('ERROR: Could not find "%s" directory. '\
                          'Please specify where to find your features.' % \
                                steps_dir)
                else:
                    print('ERROR: Could not find "%s" directory in your '\
                        'specified path "%s"' % (steps_dir, base_dir))

            message = 'No %s directory in %r' % (steps_dir, base_dir)
            raise ConfigError(message)

        base_dir = new_base_dir
        self.config.base_dir = base_dir

        for dirpath, dirnames, filenames in os.walk(base_dir, followlinks=True):
            if [fn for fn in filenames if fn.endswith(".feature")]:
                break
        else:
            if self.config.verbose:
                if not self.config.paths:
                    print('ERROR: Could not find any "<name>.feature" files. '\
                        'Please specify where to find your features.')
                else:
                    print('ERROR: Could not find any "<name>.feature" files '\
                        'in your specified path "%s"' % base_dir)
            raise ConfigError('No feature files in %r' % base_dir)

        self.base_dir = base_dir
        self.path_manager.add(base_dir)
        if not self.config.paths:
            self.config.paths = [base_dir]

        if base_dir != os.getcwd():
            self.path_manager.add(os.getcwd())

    def before_all_default_hook(self, context):
        """
        Default implementation for :func:`before_all()` hook.
        Setup the logging subsystem based on the configuration data.
        """
        # pylint: disable=no-self-use
        context.config.setup_logging()

    def load_hooks(self, filename=None):
        filename = filename or self.config.environment_file
        hooks_path = os.path.join(self.base_dir, filename)
        if os.path.exists(hooks_path):
            exec_file(hooks_path, self.hooks)

        if "before_all" not in self.hooks:
            self.hooks["before_all"] = self.before_all_default_hook

    def load_step_definitions(self, extra_step_paths=None):
        if extra_step_paths is None:
            extra_step_paths = []
        # -- Allow steps to import other stuff from the steps dir
        # NOTE: Default matcher can be overridden in "environment.py" hook.
        steps_dir = os.path.join(self.base_dir, self.config.steps_dir)
        step_paths = [steps_dir] + list(extra_step_paths)
        load_step_modules(step_paths)

    #TODO move out
    def feature_locations(self):
        return collect_feature_locations(self.config.paths)


    def setup(self):
        self.context = Context(self)
        self.setup_paths()
        self.load_hooks()
        self.load_step_definitions()

        # -- ENSURE: context.execute_steps() works in weird cases (hooks, ...)
        # self.setup_capture()
        # self.run_hook("before_all", self.context)
        
        feature_locations = [filename for filename in self.feature_locations()
                             if not self.config.exclude(filename)]
        self.features = parse_features(feature_locations, language=self.config.lang)

        # removeing streams...trying to nail this down.
        # self.config.reporters[0] = None
        # self.config.outputs[0] = None

    def build_runner(self,group):
        fs = TestCaseFilter(self.features).filter(group['text'])
        slice:Slice = self.get_slice(group)
        features = slice.parse_features(fs) if slice is not None else fs
        bargs = dict(self.config.defaults)
        tags = None
        if '@' in group['text']:
            tags = group['text']
        config = Configuration(
            [],
            tags = tags,
            **bargs,
        )
        if not config.format:
            config.format = [config.default_format]
        config.log_capture
            
        return  PerfRunner(group['id'],group['text'],config,features,the_step_registry,self.hooks)
    
    def get_slice(self,group):
        rows = []
        if 'argument' in group and 'data_table' in group['argument'] and len(group['argument']['data_table']) > 0:
            rows.append(group['argument']['data_table']['rows'][0])
            sel = (group['running'] if group['ran'] == 0 else group['ran']) % len(group['argument']['data_table']['rows'])
            if sel == 0:
                sel += 1
            rows.append(group['argument']['data_table']['rows'][sel])
            return Slice(rows)
        return None