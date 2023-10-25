import os
from formatter.color_fns import ColorFns
from formatter.announcement_formatter import AnnouncementFormatter
from behave_performance.formatter.silent_progress_formatter import SilentProgressFormatter
from behave_performance.formatter.simple_progress_formatter import SimpleProgressFormatter
from behave_performance.formatter.progress_formatter import ProgressFormatter
from behave_performance.formatter.summary_formatter import SummaryFormatter
from behave_performance.formatter.taurus_formatter import TaurusFormatter
from behave_performance.formatter.chart_points_formatter import ChartPointsFormatter
from behave_performance.formatter.logger_formatter import LoggerFormatter
from behave_performance.formatter.percentile_minion import PercentileCreator
from behave_performance.formatter.stddeviation_minion import StdDeviationCreator
from behave_performance.formatter.statistics_formatter import StatisticsFormatter
from behave_performance.formatter.minion import Minion
from behave_performance.formatter.base_formatter import Formatter


class PluginBuilder:
    @staticmethod
    def build(type, options):
        FormatterClass = PluginBuilder.get_constructor_by_type(type, options)
        extended_options = {
            'color_fns': ColorFns(options['colors_enabled']),
            **options,
        }
        return FormatterClass(extended_options)

    @staticmethod
    def get_constructor_by_type(type, options):
        constructor_map = {
            'announcement': AnnouncementFormatter,
            'summary': SummaryFormatter,
            'statistics': StatisticsFormatter,
            'progress': ProgressFormatter,
            'simple_progress': SimpleProgressFormatter,
            'silent_progress': SilentProgressFormatter,
            'prcntl': PercentileCreator,
            'prctl': PercentileCreator,
            'stddev': StdDeviationCreator,
            'stdev': StdDeviationCreator,
            'chartpoints': ChartPointsFormatter,
            'logger': LoggerFormatter,
            'taurus': TaurusFormatter
        }
        t = constructor_map.get(type,None)
        if not t:
            return PluginBuilder.load_custom_formatter(type, options)
        return t

    @staticmethod
    def is_minion(type,options):
        if type is not None:
            plugin = PluginBuilder.get_constructor_by_type(type, options)
            if issubclass(plugin, Minion):
                return True
        return False

    @staticmethod
    def is_formatter(type,options):
        if type is not None:
            plugin = PluginBuilder.get_constructor_by_type(type, options)
            if issubclass(plugin, Formatter):
                return True
        return False

    @staticmethod
    def load_custom_formatter(custom_formatter_path:str, options):
        custom_formatter= None
        if is_identifier(custom_formatter_path):
            module_path = custom_formatter_path[0:custom_formatter_path.rfind('.')]
            cls = custom_formatter_path[custom_formatter_path.rfind('.')+1:]
            mod  = __import__(module_path, fromlist=[cls])
            custom_formatter = getattr(mod, cls)
        else:
            full_custom_formatter_path = os.path.join(
                options['cwd'], custom_formatter_path)
            custom_formatter = __import__(full_custom_formatter_path, fromlist=[''])
        if callable(custom_formatter):
            return custom_formatter
        elif hasattr(custom_formatter, 'default') and callable(custom_formatter.default):
            return custom_formatter.default
        raise Exception(
            f"Custom formatter ({custom_formatter_path}) does not export a function")

def is_identifier(x):
    return all(s and s.isidentifier() for s in x.split('.'))
