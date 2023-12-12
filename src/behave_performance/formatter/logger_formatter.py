import json
import datetime
import aiofiles
from behave_performance.formatter.base_formatter import Formatter
from behave_performance.events import PerfEvents
from behave_performance.results import Result, GroupResult
from behave_performance.helpers.paths import get_absolute_path
import dataclasses, json
import decimal

class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            if isinstance(o, datetime.datetime):
                return o.isoformat()
            if isinstance(o, datetime.timedelta):
                return o.isoformat()
            if isinstance(o, type(decimal)):
                return str(o)
            if isinstance(o, Exception):
                return str(o)
            if hasattr(o, '__dict__'):
                return o.__dict__
            return super().default(o)
        
class LoggerFormatter(Formatter):
    DEFAULT=False
    FAMILY='result'
    SINGLETON=False

    def __init__(self, options):
        super().__init__(options)
        self.count = 0
        self.sim =0

        if self.is_stdio() and len(self.options) == 0:
            self.log('No output path was specified! Unable to log plan execution results.')
        elif not self.is_stdio():
            self.event_broadcaster.add_listener(PerfEvents.PERF_RUN_STARTED, self.__run_start)
            self.event_broadcaster.add_listener(PerfEvents.SIMULATION_RUN_STARTED, self.__sim_start)
            self.event_broadcaster.add_listener(PerfEvents.CUKE_RUN_FINISHED, self.log_to_file)
            self.event_broadcaster.add_listener(PerfEvents.SIMULATION_RUN_FINISHED, self.__sim_stop)
            self.event_broadcaster.add_listener(PerfEvents.PERF_RUN_FINISHED, self.__run_stop)
        if len(self.options) > 0:
            self.event_broadcaster.add_listener(PerfEvents.PERF_RUN_STARTED, self.__process_file)
    
    async def __run_start(self):
        self.event_broadcaster.emit(PerfEvents.FORMATTER_STARTED, 'logger')
        await self.log("{")

    async def __sim_start(self,name,date):
        message =  f'"{name}":['
        await self.log( ',\n' + message if self.sim > 0 else message)
        self.sim += 1
    
    async def __sim_stop(self,result):
        await self.log("]")
    
    async def __run_stop(self,result):
        self.event_broadcaster.emit(PerfEvents.FORMATTER_FINISHED, 'logger')
        await self.log("}")

    async def log_to_file(self, data):
        await self.log(((',\n' if self.count > 0 else '') + json.dumps(data, cls=JSONEncoder)))
        self.count += 1

    async def __process_file(self):
        log_path = self.options[0]
        async with aiofiles.open(get_absolute_path(log_path), mode='r') as f:
            contents = await f.read()
        logobj = json.loads(contents)
        for key, value in logobj.items():
            result = Result(key,datetime.datetime.fromisoformat(value[0]['result']['start']),datetime.datetime.fromisoformat(value[-1]['result']['stop']))
            result.duration = result.stop - result.stop
            for group in value:
                result.add_group_result(GroupResult.from_dict(group['result']))
            self.event_broadcaster.emit(PerfEvents.SIMULATION_RUN_FINISHED, result)
        return True