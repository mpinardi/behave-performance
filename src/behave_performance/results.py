from datetime import datetime, timedelta
from behave.model import Feature, Scenario, ScenarioOutline, Step, Status,Table, Row
from behave.model_core import FileLocation
import traceback as Traceback


class StepResult():

    def __init__(self,  name:str, duration:float, status:str, location:FileLocation, keyword:str,step_type:str,table:Table,error_message:str,exception:Exception,traceback, hook_failed):
        self.duration: float = duration
        self.name:str = name
        self.status:str = status
        self.location:FileLocation = location
        self.error_message:str =error_message
        self.exception: Exception = exception
        self.traceback = traceback
        self.hook_failed = hook_failed
        self.keyword = keyword
        self.step_type = step_type
        self.table:Table= table

    @classmethod
    def from_dict(cls, d: dict):
        duration = float(d['duration'])#timedelta(seconds=(d['duration']))
        name:str = d['name']
        status:str = d['status']
        location:FileLocation = FileLocation(d['location']['filename'],d['location']['line'])
        error_message = d['error_message']
        exception: Exception = None
        traceback = d['traceback']
        hook_failed = d['hook_failed']
        keyword = d['keyword']
        step_type = d['step_type']
        rows = []
        if d['table']:
            for r in d['table']['rows']:
             rows.append(Row(r['headings'],r['cells'],r['line'],r['comments']))
        table:Table= Table(d['table']['headings'],d['table']['line'],rows) if d['table'] else None
        if (not exception and status=='failed'):
            pass
        return cls(name,duration, status, location, keyword,step_type,table,error_message,exception,traceback, hook_failed)
    
    @classmethod
    def from_step(cls, step:Step):
        duration: float = step.duration
        name:str = step.name
        status:str = step.status.name
        location:FileLocation = step.location 
        error_message = step.error_message 
        exception: Exception = step.exception
        traceback = (Traceback.format_exception(step.exception) if step.exc_traceback else None)
        hook_failed = step.hook_failed 
        keyword = step.keyword 
        step_type = step.step_type 
        table:Table= step.table
        return cls(name,duration, status, location, keyword,step_type,table,error_message,exception,traceback, hook_failed)
 
class ScenarioResult():

    def __init__(self,  name:str, duration:float, steps:[StepResult],status:str, location:FileLocation):
        self.duration: float = duration
        self.steps: list[StepResult] = steps
        self.name:str = name
        self.status: str = status
        self.location:FileLocation = location
    
    @classmethod
    def from_dict(cls, d: dict):
        duration: float = float(d['duration'])#timedelta(seconds=(d['duration']))
        steps: list[StepResult] = []
        name:str = d['name']
        status: str = d['status']
        location:FileLocation = FileLocation(d['location']['filename'],d['location']['line'])
        for s in d['steps']:
            steps.append(StepResult.from_dict(s))
        return cls(name, duration, steps, status, location)
    
    @classmethod
    def from_scenario(cls, scenario:Scenario):
        steps = []
        duration: float = scenario.duration
        steps: list[StepResult] = []
        name:str = scenario.name
        status: str = scenario.status.name
        location:FileLocation = scenario.location
        for s in scenario.steps:
            steps.append(StepResult.from_step(s))
        return cls(name, duration, steps, status, location)

# class FeatureResult():

#     def __init__(self, feature: Feature):
#         self.start: datetime = datetime.fromtimestamp(feature.run_starttime)
#         self.stop: datetime = datetime.fromtimestamp(feature.run_endtime)
#         self.duration: float = feature.duration
#         self.test_cases: list[ScenarioResult] = []
#         self.name = feature.name
#         self.status = feature.status.name
#         self.success = is_success(feature.status.name)

#         for s in feature.scenarios:
#             if type(s) is ScenarioOutline:
#                 for so in s.scenarios:
#                     self.test_cases.append(ScenarioResult(so))
#             else:
#                 self.test_cases.append(ScenarioResult(s))
    
#     @classmethod
#     def get_instance(cls, d: dict):
#         test_cases = []
#         for res in d['test_cases']:
#             test_cases.append(ScenarioResult.get_instance(res))
#         return cls()
 

# class ScenarioResult():

#     def __init__(self, scenario: Scenario):

#         self.duration: float = scenario.duration
#         self.steps: list[StepResult] = []
#         self.name:str = scenario.name
#         self.status: str = scenario.status.name
#         self.location:FileLocation = scenario.location
#         self.line:int = scenario.line
#         for s in scenario.steps:
#             self.steps.append(StepResult(s))
    

# class StepResult():

#     def __init__(self, step: Step):
#         self.duration: float = step.duration
#         self.name:str = step.name
#         self.status:str = step.status.name
#         self.location:FileLocation = step.location
#         self.line = step.line
#         self.error_message = step.error_message
#         self.exception: Exception = step.exception
#         self.traceback = traceback.format_exception(step.exception) if step.exc_traceback else None
#         self.hook_failed = step.hook_failed
#         self.keyword = step.keyword
#         self.step_type = step.step_type
#         self.table:Table= step.

class FeatureResult():

    def __init__(self, name:str, start:datetime, stop:datetime, duration:float, test_cases:[ScenarioResult],success:bool,status:str):
        self.start: datetime = start
        self.stop: datetime = stop
        self.duration: float = duration
        self.test_cases: list[ScenarioResult] = test_cases
        self.name:str = name
        self.status:str = status
        self.success:bool = success

    @classmethod
    def from_dict(cls, d: dict):
        test_cases = []
        start: datetime = datetime.fromisoformat(d['start'])
        stop: datetime = datetime.fromisoformat(d['stop'])
        duration: float = float(d['duration'])
        name = d['name']
        status = d['status']
        success = d['success']
        for s in d['test_cases']:
            test_cases.append(ScenarioResult.from_dict(s))
        return cls(name,start,stop,duration,test_cases,success,status)
    
    @classmethod
    def from_feature(cls, feature:Feature):
        start: datetime = datetime.fromtimestamp(feature.run_starttime)
        stop: datetime = datetime.fromtimestamp(feature.run_endtime)
        duration: float = feature.duration
        test_cases: list[ScenarioResult] = []
        name = feature.name
        status = feature.status.name
        success = is_success(feature.status.name)

        for s in feature.scenarios:
            if type(s) is ScenarioOutline:
                for so in s.scenarios:
                    test_cases.append(ScenarioResult.from_scenario(so))
            else:
                test_cases.append(ScenarioResult.from_scenario(s))
        return cls(name,start,stop,duration,test_cases,success,status)
 


class GroupResult():

    def __init__(self, id:str, name:str, features: list[FeatureResult], success: bool):
        self.name:name = name
        self.id:str = id
        self.success:bool = success
        self.start:datetime = features[0].start
        self.stop:datetime = features[-1].stop
        self.duration:float = (features[-1].stop - features[0].start).total_seconds()
        self.results:list[FeatureResult] = features
    
    def get_meta_status(self)->str:
        feature:FeatureResult
        status = Status.untested
        for feature in self.results:
            cs = Status.from_name(feature.status)
            if cs.value > status.value:
                status = cs
        return status.name

    @classmethod
    def from_dict(cls, d: dict):
        features = []
        for res in d['results']:
            features.append(FeatureResult.from_dict(res))
        return cls(d['id'],d['name'],features,d['success'])
    
    @classmethod
    def from_features(cls, id:str, name:str, features: list[Feature], success: bool):
        feature_results = []
        for f in features:
            feature_results.append(FeatureResult.from_feature(f))
        return cls(id,name,feature_results,success)
    
    
class Result():

    def __init__(self, name: str, start: datetime, stop:datetime=None, duration:float=None, groups:dict=None,success:bool=True):
        self.start = start
        self.stop: datetime = stop
        self.duration: float = duration
        if groups is not None:
            self.groups: dict = groups
        else:
            self.groups = {}
        self.name = name
        self.success = success

    def add_group_result(self, result:GroupResult):
        if result.name in self.groups:
            self.groups.get(
                result.name).append(result)
        else:
            self.groups[result.name] = [result]
    

def is_success(status:str):
    if status in (Status.executing.name ,Status.failed.name, Status.undefined.name):
        return False
    return True


