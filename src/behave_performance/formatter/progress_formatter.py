from behave_performance.formatter.base_formatter import Formatter
from behave.model_core import Status
from behave_performance.events import PERF_EVENTS

class ProgressFormatter(Formatter):
    DEFAULT=False
    FAMILY='progress'
    SINGLETON=True

    def __init__(self, options):
        super().__init__(options)
        self.event_broadcaster.add_listener(PERF_EVENTS.CUKE_RUN_FINISHED, self.log_progress)
        self.event_broadcaster.add_listener(PERF_EVENTS.CUKE_RUN_STARTED, self.log_progress)
        self.groups = {}
        self.last_length = 0
        self.last_success = None

    async def log_progress(self, data):
        name = data['text']
        if name not in self.groups:
            self.groups[name] = data
        line = '\r'
        success = data['result'].success if 'result' in data else None
        self.groups[name] = data
        for i,key in enumerate(self.groups):
            group = self.groups[key]
            line += ' | ' if i > 0 else ''
            ran = str(group['ran'])
            if name == key and success is not None:
                ran = self.color_fns.text(Status.passed.name,ran) if success else self.color_fns.text(Status.passed.name,ran)
                line += f"{trim_feature(group['text'])}:{group['running']}-{group['max_runners']}>{ran}"
            else:
                line += f"{trim_feature(group['text'])}:{group['running']}-{group['max_runners']}>{ran}"
        
        await self.log(await self.buffer_length(line, success))

    async def buffer_length(self, line, success):
        line = line.ljust(
            self.last_length if self.last_length > 0 else (self.last_length - 10 if success is None and self.last_success is not None else (self.last_length + 10 if success is not None and self.last_success is None else self.last_length)),
            ' '
        )
        self.last_length = len(line)
        self.last_success = success
        return line


def trim_feature(name):
  if name.endswith('.feature'):
    return  name[0:  len(name)- 8]
  return name


