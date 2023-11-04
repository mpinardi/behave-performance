from datetime import datetime
from . import get_default_stats, get_default_stat_types
from behave_performance.results import Result,StepResult
from behave.model import Status

class GroupStatistics():
    def __init__(self, name:str, start:datetime, stop:datetime,is_strict:bool=True)->None:
        self.start:datetime = start
        self.stop:datetime = stop
        self.name:str = name
        self.stats:{} = get_default_stats(is_strict)
        self.test_cases:[TestCaseStatistics] = []
        self.durations:[float] = []
        self.has_issues:bool = False


class TestCaseStatistics():
    def __init__(self, name:str, location:str,is_strict:bool=True)->None:
        self.steps: list[StepStatistics] = []
        self.name:str = name
        self.location = location
        self.has_issues:bool = False
        self.stats:{} = get_default_stats(is_strict)
        self.durations:[float] = []


class StepStatistics():
    def __init__(self, step_result:StepResult,is_strict:bool=True)->None:
        self.name = step_result.name
        self.location = step_result.location
        self.keyword = step_result.keyword
        self.step_type = step_result.step_type
        self.table= step_result.table
        self.issues:[Issues] = []
        self.stats:{} = get_default_stats(is_strict)
        self.durations:[float]=[]

class Issues():
    def __init__(self,count:int,status:Status,first:datetime,last:datetime,exception:Exception=None,traceback=None) -> None:
        self.exception:IssueException = IssueException(exception,traceback=traceback) if exception else None
        self.count:int = count
        self.status:Status = status
        self.first:datetime = first
        self.last:datetime = last
   
class IssueException():
    def __init__(self, exception:Exception,error_message:str=None,traceback=None) -> None:
        self.message:str = error_message if error_message else str(exception)
        self.type:str = type(exception).__name__
        self.traceback:[str] = traceback
            
class StatisticsResult():
    def __init__(self, result:Result, is_strict:bool=True)->None:
        self.start: datetime = result.start
        self.stop: datetime = result.stop
        self.duration: float = result.duration
        self.groups:[GroupStatistics] = []
        self.stat_types:{} = get_default_stat_types(is_strict)
        self.name:str =  result.name
        self.has_issues:bool = result.success