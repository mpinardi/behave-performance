import os
from behave_performance.arguments import parse_arguments, BEHAVE_ARGS

class Configuration():
    """Behave performance configuration.
    """

    def __init__(self, args=None):
        pargs = parse_arguments(args)
        self.perf_dry_run = getattr(pargs,'perf_dry_run',False)
        self.format:[str] = getattr(pargs,'format',[])
        self.format_options:{} = getattr(pargs,'format_options',{})
        self.i18n_keywords = getattr(pargs,'i18n_keywords',None)
        self.i18n_languages = getattr(pargs,'i18n_languages',False)
        self.language = getattr(pargs,'language','en')
        self.strict = getattr(pargs,'strict',True)
        self.no_format_color = getattr(pargs,'no_format_color',False)
        self.silent = getattr(pargs,'silent',False)
        self.silent_progress = getattr(pargs,'silent_progress',False)
        self.silent_announcements = getattr(pargs,'silent_announcements',False)
        self.plans:[str] = getattr(pargs,'plans',[])
        self.plan_tags:[str] = getattr(pargs,'plan_tags',[])
        self.perf_name:[str] = getattr(pargs,'perf_name',[])
        self.profile:[str] = getattr(pargs,'profile',[])
        self.behave_args = {}
        for arg in BEHAVE_ARGS:
            value_arg = getattr(pargs, arg, None)
            if arg == 'filename':
                self.behave_args[arg] = [os.path.realpath(path) for path in value_arg]
            elif value_arg and value_arg is not None:
                self.behave_args[arg] = value_arg
        #Turn off all verbosity
        self.behave_args['summary'] = False
        self.behave_args['quiet'] = True
        self.behave_args['show_snippets'] = False
        self.behave_args['show_skipped'] = False
        #Add default format options
        self.format_options["colors_enabled"] = not self.no_format_color
        self.format_options["cwd"]= os.getcwd()
