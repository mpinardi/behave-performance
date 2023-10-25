import copy
from behave.model import Feature,Scenario,ScenarioOutline,Step,Text

class Slice:
    def __init__(self, rows):
        self.rows = rows

    def parse_features(self, features:[Feature])->[Feature]:
        fs = [self.parse_feature(fs) for fs in features]
        return fs
    
    def parse_feature(self, feature:Feature):
        test_cases = self.parse_test_cases(feature.scenarios)  
        fs = Feature(feature.filename,feature.line,feature.keyword,feature.name,feature.tags,feature.description,test_cases,feature.background,feature.language)
        return fs
            
    def parse_test_cases(self, test_cases)->[Scenario]:
        tcs = [self.parse_test_case(tc) for tc in test_cases]
        return tcs
    
    def parse_test_case(self, test_case:Scenario):
        tc = None
        steps = []
        for step in test_case.steps:
            name = self.replace_parameter(step.name)
            steps.append(Step(step.filename,step.line,step.keyword,step.step_type,name,step.text,step.table))
        if type(test_case) is ScenarioOutline:
            tc = ScenarioOutline(test_case.filename,test_case.line,test_case.keyword,test_case.name,test_case.tags,steps,test_case.examples,test_case.description)
        else:
            tc = Scenario(test_case.filename,test_case.line,test_case.keyword,test_case.name,test_case.tags,steps,test_case.description,test_case.parent)
        return tc
    
    def replace_parameter(self, value):
        loc = self.find_parameter(value)
        if loc >= 0:
            value = value.replace(
                '"' + self.rows[0]['cells'][loc]['value'] + '"',
                '"' + self.rows[1]['cells'][loc]['value'] + '"'
            )
        return value
    
    def has_parameter(self, value):
        return self.find_parameter(value) >= 0
    
    def find_parameter(self, value):
        i = 0
        if len(self.rows) > 0:
            for c in self.rows[0]['cells']:
                if '"' + c['value'] + '"' in value:
                    if len(self.rows[1]['cells']) >= i:
                        return i
                i += 1
        return -1
