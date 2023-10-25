from behave_performance.formatter.base_formatter import Formatter
from behave.model_core import Status
from behave_performance.formatter.helpers.issue_helpers import CHARACTERS
from events import PERF_EVENTS
import runtime

class AnnouncementFormatter(Formatter):
    DEFAULT=True
    FAMILY='announcement'
    SINGLETON=True

    def __init__(self, options):
        super().__init__(options)
        self.name = ''
        self.event_broadcaster.add_listener(PERF_EVENTS.PERF_RUN_STARTED, self.perf_run_start)
        self.event_broadcaster.add_listener(PERF_EVENTS.SIMULATION_RUN_STARTED, self.sim_run_start)
        self.event_broadcaster.add_listener(PERF_EVENTS.SIMULATION_RUN_FINISHED, self.sim_run_stop)
        #self.event_broadcaster.add_listener(PERF_EVENTS.SIMULATION_STATISTICS_STARTED, self.gen_stats)

    async def perf_run_start(self):
        await self.log(f"\n{self.color_fns.text('groupTitle','Behave_Performance')} version: {str(runtime.version())}\n")

    async def sim_run_start(self,name,start):
        self.name = name
        await self.log(f"\nStarting Simulation: {name} at {start.isoformat()}\n")
    
    async def sim_run_stop(self,data):
        await self.log(f"\nFinished Simulation: {self.name}\n")



