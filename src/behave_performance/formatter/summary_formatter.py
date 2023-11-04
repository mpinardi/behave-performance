
from .helpers import format_issue, format_summary
from behave_performance.formatter.statistics import StatDataType, StatisticsResult,GroupStatistics, TestCaseStatistics
from behave_performance.formatter.base_formatter import Formatter
import asyncio

class SummaryFormatter(Formatter):
    DEFAULT=True
    FAMILY='result'
    SINGLETON=False

    def __init__(self, options):
        super().__init__(options)
        from behave_performance.runtime import PERF_EVENTS
        self.event_broadcaster.add_listener(PERF_EVENTS.SIMULATION_STATISTICS_FINISHED, self.log_summary)

    async def log_summary(self, result:StatisticsResult):
        self.event_broadcaster.emit('formatter-started', 'summary')
        if self.is_stdio():
            await self.log('\n')
        else:
            self.color_fns.disable()
        await self.log(
            format_summary({
                'display_type': StatDataType.SECONDS,
                'color_fns': self.color_fns,
                'test_run': result,
            })
        )
        await self.log('\n')
        if any(group.has_issues for group in result.groups):
           await self.log_issues({'result': result, 'title': 'Issues'})
        self.event_broadcaster.emit('formatter-finished', 'summary')

    async def log_issues(self, data):
        result = data['result']
        title = data['title']
        await self.log(f"{title}:\n")
        group:GroupStatistics
        for group in result.groups:
            if group.has_issues:
                test_case:TestCaseStatistics
                c = 0
                for test_case in group.test_cases:
                    if test_case.has_issues:
                        await self.log(
                            format_issue(self.color_fns,c,test_case)
                        )
                        c +=1
