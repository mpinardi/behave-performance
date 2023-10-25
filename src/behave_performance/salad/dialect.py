import io
import os
import json


DIALECT_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    'salad-languages.json')

with io.open(DIALECT_FILE_PATH, 'r', encoding='utf-8') as file:
    DIALECTS = json.load(file)


class Dialect(object):

    @classmethod
    def for_name(cls, name):
        return cls(DIALECTS[name]) if name in DIALECTS else None

    def __init__(self, spec):
        self.spec = spec

    @property
    def plan_keywords(self):
        return self.spec['plan']

    @property
    def simulation_keywords(self):
        return self.spec['simulation']

    @property
    def simulation_period_keywords(self):
        return self.spec['simulationPeriod']

    @property
    def group_keywords(self):
        return self.spec['group']
    
    @property
    def population_keywords(self):
        return self.spec['population']

    @property
    def groups_keywords(self):
        return self.spec['groups']
    
    @property
    def type_keywords(self):
        return self.spec['type']

    @property
    def features_keywords(self):
        return self.spec['features']

    @property
    def type_keywords(self):
        return self.spec['type']

    @property
    def runners_keywords(self):
        return self.spec['runners']

    @property
    def percentage_keywords(self):
        return self.spec['percentage']
    
    @property
    def count_keywords(self):
        return self.spec['count']

    @property
    def start_keywords(self):
        return self.spec['start']

    @property
    def stop_keywords(self):
        return self.spec['stop']

    @property
    def synchronized_keywords(self):
        return self.spec['synchronized']

    @property
    def ramp_up_keywords(self):
        return self.spec['rampUp']

    @property
    def ramp_down_keywords(self):
        return self.spec['rampDown']

    @property
    def random_wait_keywords(self):
        return self.spec['randomWait']

    @property
    def total_count_keywords(self):
        return self.spec['totalCount']

    @property
    def total_runners_keywords(self):
        return self.spec['totalRunners']

    @property
    def time_keywords(self):
        return self.spec['time']
