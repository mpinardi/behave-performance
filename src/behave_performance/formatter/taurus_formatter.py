from behave_performance.formatter.helpers import format_csv
from behave_performance.formatter.base_formatter import Formatter
from behave_performance.formatter.statistics import StatDataType,StatTypes
from behave_performance.events import PERF_EVENTS

HEADER = 'label,avg_ct,avg_lt,avg_rt,bytes,concurrency,fail,stdev_rt,succ,throughput,perc_0.0,perc_50.0,perc_90.0,perc_95.0,perc_99.0,perc_99.9,perc_100.0,rc_200'

ORDER = [
    {'key': 'avg_ct', 'default': '0.000'},
    {'key': 'avg_lt', 'default': '0.000'},
    {'key': StatTypes.AVERAGE.key, 'default': '0.000'},
    {'key': 'bytes', 'default': '0'},
    {'key': StatTypes.CONCURRENCY.key, 'default': '0.000'},
    {'key': StatTypes.FAILED.key, 'default': '0'},
    {'key': StatTypes.STD_DEVIATION.key, 'default': '0.000'},
    {'key': StatTypes.PASSED.key, 'default': '0'},
    {'key': StatTypes.COUNT.key, 'default': '0'},
    {'key': StatTypes.MINIMUM.key, 'default': '0'},
    {'key': 'perc_50', 'default': '0.000'},
    {'key': 'perc_90', 'default': '0.000'},
    {'key': 'perc_95', 'default': '0.000'},
    {'key': 'perc_99', 'default': '0.000'},
    {'key': 'perc_99.5', 'default': '0.000'},
    {'key': StatTypes.MAXIMUM.key, 'default': '0'},
    {'key': 'rc_200', 'default': '0'},
]

class TaurusFormatter(Formatter):
    DEFAULT=False
    FAMILY='result'
    SINGLETON=False

    def __init__(self, options):
        super().__init__(options)
        if not self.is_stdio():
            self.color_fns.disable()
        self.event_broadcaster.add_listener(PERF_EVENTS.SIMULATION_STATISTICS_FINISHED, self.__log_final_stats)
        self.event_broadcaster.add_listener(PERF_EVENTS.PERF_RUN_STARTED, self.__config_statistics)

    async def __config_statistics(self):
        self.event_broadcaster.emit(PERF_EVENTS.CONFIG_STATISTICS, 'prcntl','50')
        self.event_broadcaster.emit(PERF_EVENTS.CONFIG_STATISTICS, 'prcntl','90')
        self.event_broadcaster.emit(PERF_EVENTS.CONFIG_STATISTICS, 'prcntl','95')
        self.event_broadcaster.emit(PERF_EVENTS.CONFIG_STATISTICS, 'prcntl','99')
        self.event_broadcaster.emit(PERF_EVENTS.CONFIG_STATISTICS, 'prcntl','99.5')

    async def __log_final_stats(self, result):
        self.event_broadcaster.emit(PERF_EVENTS.FORMATTER_STARTED, 'taurus')
        await self.log(format_csv(self.color_fns, HEADER,ORDER,StatDataType.SECONDS,result))
        await self.log('\n')
        self.event_broadcaster.emit(PERF_EVENTS.FORMATTER_FINISHED, 'taurus')
