from typing import Dict
from behave_performance.formatter.statistics import StatType, StatisticsResult, GroupStatistics, TestCaseStatistics, StepStatistics, StatDataType
from datetime import timedelta


def convert_output(display_type: str, data_type: str, value: float) -> float:
    output = value
    if data_type != StatDataType.COUNT and data_type != StatDataType.OTHER and display_type != data_type:
        if data_type == StatDataType.NANOS and display_type == StatDataType.MILLIS:
            output = value / 1000000
        elif data_type == StatDataType.MILLIS and display_type == StatDataType.NANOS:
            output = value * 1000000
        elif data_type == StatDataType.MILLIS and display_type == StatDataType.SECONDS:
            output = value / 1000
        elif data_type == StatDataType.NANOS and display_type == StatDataType.SECONDS:
            output = value / 1000000000
        elif data_type == StatDataType.SECONDS and display_type == StatDataType.MILLIS:
            output = value * 1000
        elif data_type == StatDataType.SECONDS and display_type == StatDataType.NANOS:
            output = value * 1000000000
    return output

def format_summary(data: Dict[str, any]) -> str:
    display_type = data['display_type']
    color_fns = data['color_fns']
    test_run:StatisticsResult = data['test_run']
    group_summaries = []
    for group in test_run.groups:
        v = get_group_summary(color_fns, group, test_run.stat_types, display_type)
        group_summaries.append(v)
    duration_summary = get_duration(test_run.duration)
    return (
        color_fns.text('simulationTitle','Simulation: ') +
        test_run.name +
        color_fns.text('statTitle',' Start: ') +
        test_run.start.ctime() +
        color_fns.text('statTitle',' Stop: ') +
        test_run.stop.ctime() +
        color_fns.text('statTitle',' Duration: ') +
        duration_summary + '\n' +
        '\n'.join(group_summaries)
    )

def get_group_summary(color_fns: Dict[str, callable], group:GroupStatistics, stat_types: Dict[str, any], display_type: str) -> str:
    text = (
        color_fns.text('groupTitle','Group: ') +
        group.name +
        ' ' +
        get_statistics(color_fns, group.stats, stat_types, display_type) +
        '\n'
    )
    test_case:TestCaseStatistics
    for test_case in group.test_cases:
        text += (
            '\t' +
            color_fns.text('cukeTitle','Scenario: ') +
            test_case.name +
            ' ' +
            get_statistics(color_fns, test_case.stats, stat_types, display_type) +
            '\n'
        )
        step:StepStatistics
        for step in test_case.steps:
            text += (
                '\t\t' +
                color_fns.text('cukeTitle','Step: ') +
                step.name +
                ' ' +
                get_statistics(color_fns, step.stats, stat_types, display_type) +
                '\n'
            )
    return text

def get_statistics(color_fns , stats: Dict[str, any], stat_types: Dict[str, StatType], display_type: str) -> str:
    text = ''
    for stat in stat_types:
        if stat in stats and stats[stat] is not None:
            value = stats[stat]
        else:
            value = stat_types[stat].get_default_value()
        if stat_types[stat].is_floating_point:
            text += f"{color_fns.text('statTitle',stat)}:{convert_output(display_type, stat_types[stat].data_type, value):.3f} "
        else:
            text += f"{color_fns.text('statTitle',stat)}:{convert_output(display_type, stat_types[stat].data_type, value)} "
    return text

def get_duration(duration:timedelta) -> str:
    hours, minutes, millis = duration.seconds // 3600, duration.seconds // 60 % 60, duration.microseconds/1000
    return f"{hours}:{minutes}:{duration.seconds}.{millis}"

