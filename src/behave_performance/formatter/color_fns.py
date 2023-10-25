from behave.model_core import Status
from behave.formatter.ansi_escapes import colors,escapes


class ColorTypes():
    DEFAULT = "default"
    FAILED = Status.failed.name
    EXECUTING = Status.executing.name
    UNTESTED = Status.untested.name
    SKIPPED = Status.skipped.name
    UNDEFINDED = Status.undefined.name
    PASSED = Status.passed.name
    LOCATION = "location"
    TAG ="tag"
    DIFF_ADDED="diffAdded"
    DIFF_REMOVED="diffRemoved"
    ERROR_MESSAGE="errorMessage"
    ERROR_STACK ="errorStack"
    SIMULATION_TITLE="simulationTitle"
    GROUP_TITLE="groupTitle"
    CUKE_TITLE="cukeTitle"
    STAT_TITLE="statTitle"

class ColorFns:
    def __init__(self, enabled):
        self.enabled = enabled
        self.perf_colors={
            "default": colors['black'],
            Status.failed.name: colors['red'],
            Status.executing.name: colors['green'],
            Status.untested.name: colors['yellow'],
            Status.skipped.name: colors['cyan'],
            Status.undefined.name: colors['yellow'],
            Status.passed.name: colors['green'],
            "location": colors['grey'],
            "tag": colors['cyan'],
            "diffAdded": colors['green'],
            "diffRemoved": colors['red'],
            "errorMessage": colors['red'],
            "errorStack": colors['grey'],
            "simulationTitle": colors['blue'],
            "groupTitle": colors['green'],
            "cukeTitle": colors['cyan'],
            "statTitle": colors['grey'],
        }
  
    def text(self, type, text):
        if self.enabled:
            return self.perf_colors[type] + text + escapes["reset"]
        return text
    
    def disable(self):
        self.enabled = False
    
    def enable(self):
        self.enabled = True
