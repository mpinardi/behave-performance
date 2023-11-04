from .summary_helpers import convert_output
from behave_performance.formatter.color_fns import ColorFns
from behave_performance.formatter.statistics import GroupStatistics,StatisticsResult, StatType

def format_csv(color_fns:ColorFns, heading:str, stat_order:[dict[str,float]], display_type:str, test_run:StatisticsResult)->str:
    rows = ''
    for group in test_run.groups:
        v = __get_group_lines(color_fns=color_fns, group=group, stat_order=stat_order, display_type=display_type, stat_types=test_run.stat_types)
        rows += v
    return color_fns.text('simulationTitle',heading) + '\n' + rows

def __get_group_lines(color_fns:ColorFns, group:GroupStatistics, stat_order:[dict[str,float]], display_type:str, stat_types:[StatType])->str:
    gt = color_fns.text('groupTitle',group.name.replace('"', '""'))
    text = f'"{gt}"{__get_statistics(group, stat_order, stat_types, display_type)}\n'
    
    for testCase in group.test_cases:
        tct = color_fns.text('cukeTitle','.' + testCase.name.replace('"', '""'))
        text += f'"{gt}{tct}"{__get_statistics(testCase, stat_order, stat_types, display_type)}\n'
        
        for step in testCase.steps:
            st = color_fns.text('cukeTitle','.' + step.name.replace('"', '""'))
            text += f'"{gt}{tct}{st}"{__get_statistics(step, stat_order, stat_types, display_type)}\n'
    
    return text

def __get_statistics(obj, stat_order:[dict[str,float]], stat_types:{StatType}, display_type:str):
    text = ''
    
    for stat in stat_order:
        if stat['key'] in stat_types:
            if stat_types[stat['key']] and obj.stats.get(stat['key']) is not None:
                text += f',{convert_output(display_type, stat_types[stat["key"]].data_type, obj.stats[stat["key"]]):.3f}'
            else:
                text += f',{convert_output(display_type, stat_types[stat["key"]].data_type, obj.stats[stat["key"]])}'
        else:
            text += f',{stat["default"]}' if 'default' in stat else ','
    
    return text