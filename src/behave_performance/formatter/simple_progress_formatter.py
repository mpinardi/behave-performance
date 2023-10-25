from behave_performance.formatter.base_formatter import Formatter
from behave.model_core import Status
from behave_performance.formatter.helpers.issue_helpers import CHARACTERS
from events import PERF_EVENTS

class SimpleProgressFormatter(Formatter):
    DEFAULT=True
    FAMILY='progress'
    SINGLETON=True

    def __init__(self, options):
        super().__init__(options)
        self.event_broadcaster.add_listener(PERF_EVENTS.CUKE_RUN_FINISHED, self.log_progress)

    async def log_progress(self, data):
        status =  data['result'].get_meta_status() if 'result' in data else 'default'
        text= self.color_fns.text(status,CHARACTERS[status])
        await self.log(text)



