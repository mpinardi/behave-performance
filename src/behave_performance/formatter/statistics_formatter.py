from behave_performance.formatter.base_formatter import Formatter
from behave_performance.formatter.statistics import generate_default_statistics
from behave_performance.formatter.helpers import MinionOptionSplitter

CONFIG_ADDPLUGIN = 'addPlugin'

class StatisticsFormatter(Formatter):
    DEFAULT=True
    FAMILY='statistics'
    SINGLETON=True

    def __init__(self, options):
        from behave_performance.runtime import PERF_EVENTS
        from behave_performance.formatter.builder import PluginBuilder as pb
        super().__init__(options)
        self.plugin_minions = []
        for option in self.options:
            m = MinionOptionSplitter.split(option, options)
            if pb.is_minion(m['type'],options):
                self.plugin_minions.append(m)
        self.calculated_result = None
        self.event_broadcaster.add_listener(PERF_EVENTS.SIMULATION_RUN_FINISHED, self.generate_statistics)
        self.event_broadcaster.add_listener(PERF_EVENTS.CONFIG_STATISTICS, self.config)
    
    async def generate_statistics(self, data):
        from behave_performance.runtime import PERF_EVENTS
        self.event_broadcaster.emit(PERF_EVENTS.SIMULATION_STATISTICS_STARTED)
        self.calculated_result = await generate_default_statistics(data, self.strict, None, None)
        await self.run_minions()
        self.event_broadcaster.emit(PERF_EVENTS.SIMULATION_STATISTICS_FINISHED, self.calculated_result)

    async def config(self, setting, value):
        from .builder import PluginBuilder as pb
        if setting == CONFIG_ADDPLUGIN:
            m = MinionOptionSplitter.split(value, {
                'strict': self.strict,
                'color_fns': self.colorFns,
                'cwd': self.cwd,
            })
            if pb.is_minion(m['type'],self.options):
                self.plugin_minions.append(m)

    async def run_minions(self):
        from .builder import PluginBuilder as pb
        for plugin in self.plugin_minions:
            sc = pb.build(plugin['type'], plugin['options'])
            result = await sc.run(self.calculated_result)
            self.calculated_result = result if result is not None else self.calculated_result