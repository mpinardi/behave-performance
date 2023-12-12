from behave.model_core import Status
from datetime import timedelta
from behave_performance.results import Result,GroupResult,ScenarioResult,StepResult,FeatureResult
from .statistics import StatTypes
from .statistics_results import Issues,IssueException,StatisticsResult,StepStatistics,GroupStatistics,TestCaseStatistics


async def generate_default_statistics(data:Result, is_strict, period_start, period_stop):
    calculated_result = StatisticsResult(data,is_strict)
    for key in data.groups:
        calculated_result.groups.append(await calculate_group(data.groups[key], is_strict, period_start, period_stop))
    return calculated_result

async def calculate_group(group_results:GroupResult, is_strict, period_start, period_stop):
    result = GroupStatistics(group_results[0].name,period_start if period_start is not None else group_results[0].start,period_stop if period_stop is not None else group_results[len(group_results)-1].stop,is_strict)
    next_concurrent_period = None
    concurrency = []
    gr:GroupResult
    for gr in group_results:
        if period_stop is not None and gr.stop > period_stop:
            break
        if period_start is None or gr.stop > period_start:
            if next_concurrent_period is None:
                next_concurrent_period = gr.start + timedelta(seconds=1)
            elif gr.start >= next_concurrent_period:
                while fr.start >= next_concurrent_period:
                    next_concurrent_period += timedelta(seconds=1)
                    result.stats[StatTypes.CONCURRENCY.key] += get_concurrent(next_concurrent_period, concurrency)
            if (is_strict and gr.success) or not is_strict:
                concurrency.append(gr.stop)
                result.durations.append(gr.duration)
                result.stats[StatTypes.AVERAGE.key] += gr.duration
                result.stats[StatTypes.COUNT.key] += 1
                if result.stats[StatTypes.MAXIMUM.key] is None or gr.duration > result.stats[StatTypes.MAXIMUM.key]:
                    result.stats[StatTypes.MAXIMUM.key] = gr.duration
                if result.stats[StatTypes.MINIMUM.key] is None or gr.duration < result.stats[StatTypes.MINIMUM.key]:
                    result.stats[StatTypes.MINIMUM.key] = gr.duration
                if not is_strict:
                    if gr.success:
                        result.stats[StatTypes.PASSED.key] += 1
                    else:
                        result.stats[StatTypes.FAILED.key] += 1
            fr: FeatureResult
            for fr in gr.results:
                tc: ScenarioResult
                for tc in fr.test_cases:
                    ctc = next((item for item in result.test_cases if item.name == tc.name and item.location == tc.location), None)
                    if ctc is None:
                        ctc = TestCaseStatistics(tc.name,tc.location,is_strict)
                        result.test_cases.append(ctc)
                    if (is_strict and gr.success) or not is_strict:
                        ctc.durations.append(tc.duration)
                        ctc.stats[StatTypes.AVERAGE.key] += tc.duration
                        ctc.stats[StatTypes.COUNT.key] += 1
                        if ctc.stats[StatTypes.MAXIMUM.key] is None or tc.duration > ctc.stats[StatTypes.MAXIMUM.key]:
                            ctc.stats[StatTypes.MAXIMUM.key] = tc.duration
                        if ctc.stats[StatTypes.MINIMUM.key] is None or tc.duration < ctc.stats[StatTypes.MINIMUM.key]:
                            ctc.stats[StatTypes.MINIMUM.key] = tc.duration
                        if not is_strict:
                            if tc.status == Status.passed:
                                ctc.stats[StatTypes.PASSED.key] += 1
                            else:
                                ctc.stats[StatTypes.FAILED.key] += 1
                    ts: StepResult
                    for ts in tc.steps:
                        cts = next((item for item in ctc.steps if item.name == ts.name), None)
                        if cts is None:
                            cts = StepStatistics(ts,is_strict)
                            ctc.steps.append(cts)
                        if is_status_failure(ts.status) or is_status_warning(ts.status):
                            result.has_issues = True
                            ctc.has_issues = True
                            if not cts.issues:
                                issue = Issues(1,ts.status,fr.stop,fr.stop)
                                if ts.exception:
                                    issue.exception = IssueException(ts.exception,traceback=ts.traceback)
                                cts.issues.append(issue)
                            elif ts.exception:
                                ex = next((item for item in cts.issues if str(item.exception.message) == str(ts.exception)), None)
                                if ex:
                                    ex.count += 1
                                    if fr.stop < ex.first:
                                        ex.first = fr.stop
                                    if fr.stop > ex.last:
                                        ex.last = fr.stop
                                else:
                                    issue = Issues(1,ts.status,fr.stop,fr.stop,ts.exception,ts.traceback)
                                    cts.issues.append(issue)
                            else:
                                wrn = next((item for item in cts.issues if item.status == ts.status), None)
                                if wrn:
                                    wrn.count += 1
                                    if fr.stop < wrn.first:
                                        wrn.first = fr.stop
                                    if fr.stop > wrn.last:
                                        wrn.last = fr.stop
                                else:
                                    cts.issues.append(Issues(1,ts.status,fr.stop,fr.stop,ts.exception,ts.traceback))

                        if (is_strict and gr.success) or not is_strict:
                            cts.durations.append(ts.duration)
                            cts.stats[StatTypes.AVERAGE.key] += ts.duration
                            cts.stats[StatTypes.COUNT.key] += 1
                            if cts.stats[StatTypes.MAXIMUM.key] is None or ts.duration > cts.stats[StatTypes.MAXIMUM.key]:
                                cts.stats[StatTypes.MAXIMUM.key] = ts.duration
                            if cts.stats[StatTypes.MINIMUM.key] is None or ts.duration < cts.stats[StatTypes.MINIMUM.key]:
                                cts.stats[StatTypes.MINIMUM.key] = ts.duration
                            if not is_strict:
                                if ts.status == Status.passed:
                                    cts.stats[StatTypes.PASSED.key] += 1
                                else:
                                    cts.stats[StatTypes.FAILED.key] += 1
    if period_start is None:
        period_start = group_results[0].start
        period_stop = group_results[len(group_results)-1].stop
    if next_concurrent_period:
        while period_stop >= next_concurrent_period:
            next_concurrent_period += timedelta(seconds=1)
            result.stats[StatTypes.CONCURRENCY.key] += get_concurrent(next_concurrent_period, concurrency)
    total_seconds = (period_stop - period_start).total_seconds()
    if total_seconds > 0:
        result.stats[StatTypes.CONCURRENCY.key] /= total_seconds
    if result.stats[StatTypes.AVERAGE.key] > 0:
        result.stats[StatTypes.AVERAGE.key] /= result.stats[StatTypes.COUNT.key]
        result.durations.sort()
        for tc in result.test_cases:
            tc.stats[StatTypes.AVERAGE.key] /= tc.stats[StatTypes.COUNT.key]
            tc.durations.sort()
            for ts in tc.steps:
                ts.stats[StatTypes.AVERAGE.key] /= ts.stats[StatTypes.COUNT.key]
                ts.durations.sort()
    return result

def get_concurrent(period: timedelta, concurrency:[]):
    for i, o in enumerate(concurrency):
        if concurrency[i] < period:
            concurrency.pop(i)
    return len(concurrency)

def is_status_failure(status):
  return status in [Status.failed.name]

def is_status_warning(status):
  return status in [Status.untested.name, Status.undefined.name]

