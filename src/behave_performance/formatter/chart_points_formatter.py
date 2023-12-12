from datetime import datetime, timedelta
from behave_performance.formatter.statistics import generate_default_statistics
from behave_performance.formatter.base_formatter import Formatter
from behave_performance.formatter.helpers import MinionOptionSplitter
from behave_performance.results import Result
from behave_performance.formatter.statistics import StatisticsResult


class ChartPointsFormatter(Formatter):
    DEFAULT=False
    FAMILY='result'
    SINGLETON=False

    def __init__(self, options):
        super().__init__(options)
        self.max_points = 20
        self.chart_points = []
        self.plugin_minions = []
        if not self.is_stdio():
            self.color_fns.disable()
        from .builder import PluginBuilder as pb
        for option in self.options:
            if option.isnumeric():
                mp = int(option)
                self.max_points = mp
            else:
                m = MinionOptionSplitter.split(option, options)
                if pb.is_minion(m['type'],options):
                    self.plugin_minions.append(m)
        from ..runtime import PerfEvents
        self.event_broadcaster.add_listener(PerfEvents.SIMULATION_RUN_FINISHED, self.process_data)

    async def process_data(self, data):
        self.event_broadcaster.emit('formatter-started', 'chartpoints')
        self.event_broadcaster.emit('chartpoints-started')
        await self.create_chart_points(data)
        await self.log_chart_points()
        self.event_broadcaster.emit('chartpoints-finished', self.chart_points)
        self.event_broadcaster.emit('formatter-finished', 'chartpoints')

    async def create_chart_points(self, data:Result):
        start_period = data.start
        period = self.__get_period(
            data.stop-data.start,
            self.max_points
        )
        end_period = self.__get_end(start_period, period)

        while end_period <= data.stop:
            presult = await generate_default_statistics(
                data,
                self.strict,
                start_period,
                end_period
            )
            presult = await self.__run_minions(presult)

            self.chart_points.append({
                'instant': self.__get_mid(start_period, end_period),
                'value': presult
            })

            start_period = end_period
            end_period = self.__get_end(end_period, period)

    async def log_chart_points(self):
        for cp in self.chart_points:
            self.statTypes = cp['value'].stat_types
            instant = cp['instant'].isoformat()
            for cpg in cp['value'].groups:
                group = cpg.name
                scenario = ''
                step = ''
                await self.log(
                    f'{group},{scenario},{step},{instant}{self.__get_row_stats(cpg.stats)}\n'
                )

                for cptc in cpg.test_cases:
                    scenario = cptc.name
                    await self.log(
                        f'{group},{scenario},{step},{instant}{self.__get_row_stats(cptc.stats)}\n'
                    )

                    for cpts in cptc.steps:
                        step = cpts.name
                        await self.log(
                            f'{group},{scenario},{step},{instant}{self.__get_row_stats(cpts.stats)}\n'
                        )

    def __get_row_stats(self, row:{})->str:
        text = ''
        for stat, stat_type in self.statTypes.items():
            if stat_type.is_floating_point and row[stat] is not None:
                text += f',{stat},{row[stat]:.3f}'
            else:
                text += f',{stat},{row[stat]}'
        return text

    def __get_end(self, start: datetime, seconds:float)->timedelta:
        m = start + timedelta(0,seconds)
        return m

    def __get_mid(self, start:datetime, end:datetime)->datetime:
        td = (end-start) / 2
        return start + td

    def __get_period(self, time: timedelta, times: int)->float:
        # total time in seconds/times
        return (time.total_seconds() / times)

    async def __run_minions(self, chart_point:StatisticsResult)->StatisticsResult:
        from .builder import PluginBuilder
        for plugin in self.plugin_minions:
            sc = PluginBuilder.build(plugin['type'], plugin['options'])
            result = await sc.run(chart_point)
            chart_point = result if result is not None else chart_point
        return chart_point
