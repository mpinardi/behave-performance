from enum import Enum

class task():
    def __init__ (self,task:str,message:object):
        self.task = task
        self.message = message

class RUNNER_TASKS(Enum):
    STOP_ALL = 'STOP_ALL'
    RAMP = 'RAMP'
    RUN = 'RUN'
    READY= 'READY'
    EVENT = 'EVENT'

    def __init__ (self, type:str):
        self.type = type

    def create(self,message:object='')-> task:
        return task(self.type,message)