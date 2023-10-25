from behave_performance.formatter.minion import Minion
from behave_performance.formatter.statistics import StatTypes, create_stat_type_with_postfix
import math

class PercentileCreator(Minion):
    def __init__(self, options):
        super().__init__(options)
        self.percentile = 90.0
        self.postfix = '90'

        for opt in self.options:
            n = float(opt)
            if not math.isnan(n):
                self.postfix = opt
                self.percentile = n

    async def run(self, calculatedResults):
        type = create_stat_type_with_postfix(StatTypes.PERCENTILE, self.postfix)
        calculatedResults.stat_types[type.key] = type

        for group in calculatedResults.groups:
            if group.durations:
                if len(group.durations) > 0:
                    group.stats[type.key] = group.durations[self.percentilePosition(len(group.durations)) - 1]
                else:
                    group.stats[type.key] = None
            else:
                group.stats[type.key] = None

            for test_case in group.test_cases:
                if test_case.durations:
                    if len(test_case.durations) > 0:
                        test_case.stats[type.key] = test_case.durations[self.percentilePosition(len(test_case.durations)) - 1]
                    else:
                        test_case.stats[type.key] = None
                else:
                    test_case.stats[type.key] = None

                for step in test_case.steps:
                    if step.durations:
                        if len(step.durations) > 0:
                            step.stats[type.key] = step.durations[self.percentilePosition(len(step.durations)) - 1]
                        else:
                            step.stats[type.key] = None
                    else:
                        step.stats[type.key] = None
        return calculatedResults

    def percentilePosition(self, length):
        percent = self.percentile / 100
        return round(length * percent)