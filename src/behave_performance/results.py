from datetime import datetime
import traceback as Traceback
from behave.model import Feature, Scenario, ScenarioOutline, Step, Status,Table, Row
from behave.model_core import FileLocation


class StepResult():
    """The result of step's execution
    """
    def __init__(self,  name:str, duration:float, status:str, location:FileLocation,
    keyword:str,step_type:str,table:Table,error_message:str,
    exception:Exception,traceback, hook_failed):
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
        """Convert a dictionary representation of a step 
            into a step result.

        Args:
            d (dict): A dict representation of a step.

        Returns:
            StepResult: The resulting step result object.
        """
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
        return cls(name,duration, status, location, keyword,step_type,table,
        error_message,exception,traceback, hook_failed)

    @classmethod
    def from_step(cls, step:Step):
        """Covert a step object into a step result.

        Args:
            step (Step): The step object to process.

        Returns:
            StepResult: The resulting step result.
        """
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
        return cls(name,duration, status, location, keyword,
                   step_type,table,error_message,exception,traceback, hook_failed)

class ScenarioResult():
    """Result of scenarios execution
    """
    def __init__(self,  name:str, duration:float, steps:[StepResult],
        status:str, location:FileLocation):
        self.duration: float = duration
        self.steps: list[StepResult] = steps
        self.name:str = name
        self.status: str = status
        self.location:FileLocation = location

    @classmethod
    def from_dict(cls, d: dict):
        """Convert a dictionary representation of a scenario result into a ScenarioResult.

        Args:
            d (dict): The dictionary representation of a ScenarioResult.

        Returns:
            ScenarioResult: A scenario result object.
        """
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
        """Convert a scenario into a ScenarioResult

        Args:
            scenario (Scenario): A scenario to process.

        Returns:
            ScenarioResult: A scenario result object.
        """
        steps = []
        duration: float = scenario.duration
        steps: list[StepResult] = []
        name:str = scenario.name
        status: str = scenario.status.name
        location:FileLocation = scenario.location
        for s in scenario.steps:
            steps.append(StepResult.from_step(s))
        return cls(name, duration, steps, status, location)

class FeatureResult():
    """Result of a features execution.
    """
    def __init__(self, name:str, start:datetime, stop:datetime, duration:float,
        test_cases:[ScenarioResult],success:bool,status:str):
        self.start: datetime = start
        self.stop: datetime = stop
        self.duration: float = duration
        self.test_cases: list[ScenarioResult] = test_cases
        self.name:str = name
        self.status:str = status
        self.success:bool = success

    @classmethod
    def from_dict(cls, d: dict):
        """Create a feature result from a dictionary.

        Args:
            d (dict): THe dictionary representation of the FeatureResult.

        Returns:
            FeatureResult: The resulting feature result.
        """
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
        """Create a feature result from a feature.

        Args:
            feature (Feature): A feature which has been executed.

        Returns:
            FeatureResult: A feature result version of the feature.
        """
        start: datetime = datetime.fromtimestamp(feature.run_starttime)
        stop: datetime = datetime.fromtimestamp(feature.run_endtime)
        duration: float = feature.duration
        test_cases: list[ScenarioResult] = []
        name = feature.name
        status = feature.status.name
        success = is_success(feature.status.name)

        for s in feature.scenarios:
            if isinstance(s,ScenarioOutline.__class__):
                for so in s.scenarios:
                    test_cases.append(ScenarioResult.from_scenario(so))
            else:
                test_cases.append(ScenarioResult.from_scenario(s))
        return cls(name,start,stop,duration,test_cases,success,status)

class GroupResult():
    """The result of a group's execution.
    """
    def __init__(self, uid:str, name:str, features: list[FeatureResult], success: bool):
        self.name:name = name
        self.id:str = uid
        self.success:bool = success
        self.start:datetime = features[0].start
        self.stop:datetime = features[-1].stop
        self.duration:float = (features[-1].stop - features[0].start).total_seconds()
        self.results:list[FeatureResult] = features

    def get_meta_status(self)->str:
        """Get the worst status for this group.

        Returns:
            str: The status with the highest number.
        """
        feature:FeatureResult
        status = Status.untested
        for feature in self.results:
            cs = Status.from_name(feature.status)
            if cs.value > status.value:
                status = cs
        return status.name

    @classmethod
    def from_dict(cls, d: dict):
        """From dictionary to Group Result.

        Args:
            d (dict): A dictoionary of the group result.

        Returns:
            GroupResult: The resulting GroupResult object.
        """
        features = []
        for res in d['results']:
            features.append(FeatureResult.from_dict(res))
        return cls(d['id'],d['name'],features,d['success'])

    @classmethod
    def from_features(cls, uid:str, name:str, features: list[Feature], success: bool):
        """Createa a group result from list of features.

        Args:
            uid (str): The uid of the group
            name (str): The name of the group
            features (list[Feature]): The result of the group as a list of features.
            success (bool): If the result was a success.

        Returns:
           GroupResult: Returns a group result.
        """
        feature_results = []
        for f in features:
            feature_results.append(FeatureResult.from_feature(f))
        return cls(uid,name,feature_results,success)

class Result():
    """Result of a complete simulation run.
    """
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
        """Add group result to result.

        Args:
            result (GroupResult): The group result to add.
        """
        if result.name in self.groups:
            self.groups.get(
                result.name).append(result)
        else:
            self.groups[result.name] = [result]

def is_success(status:str):
    """Check if status is success.

    Args:
        status (str): The status string.

    Returns:
        bool: True if success else false.
    """
    if status in (Status.executing.name ,Status.failed.name, Status.undefined.name):
        return False
    return True
