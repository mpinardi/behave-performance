from behave_performance.formatter.minion import Minion
from behave_performance.formatter.statistics import StatTypes
import math

class StdDeviationCreator(Minion):

    async def run(self, calculatedResults):
        type = StatTypes.STD_DEVIATION
        calculatedResults.statTypes[type.key] = type

        for group in calculatedResults.groups:
            group.stats[type.key] = self.calculate_std_dev(group.durations)
            
            for test_case in group.test_cases:
                test_case.stats[type.key] = self.calculate_std_dev(test_case.durations)
                
                for step in test_case.steps:
                    step.stats[type.key] = self.calculate_std_dev(step.durations)

        return calculatedResults

    def calculate_std_dev(self, values):
        if len(values) > 0:
            m = self.mean(values)
            smsl = self.subtract_mean_square(m, values)
            dm = self.mean(smsl)
            return math.sqrt(dm)
        return None

    def sum(self, values):
        _sum = 0
        for l in values:
            _sum += l
        return _sum

    def mean(self, values):
        return self.sum(values) / len(values)

    def subtract_mean_square(self, mean, values):
        result = []
        for l in values:
            sub = l - mean
            result.append(sub * sub)
        return result
