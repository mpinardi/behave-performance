import re
from behave.model import Status, Table, Row
from behave.textutil import indent,make_indentation
from .step_result_helpers import get_step_messages
from behave_performance.formatter.color_fns import ColorTypes
from behave_performance.formatter.statistics import StepStatistics,TestCaseStatistics

CHARACTERS = {
    Status.failed.name: '+',#figures.cross,
    Status.passed.name: '.',#figures.tick,
    Status.executing.name: '?',
    Status.skipped.name: '-',
    Status.undefined.name: '?',
    Status.untested.name: '_',
}

IS_ISSUE = {
    Status.untested.name: False,
    Status.failed.name: True,
    Status.passed.name: False,
    Status.executing.name: True,
    Status.skipped.name: False,
    Status.undefined.name: True,
}

def format_table(table:Table):
    text = '| '
    for heading in table.headings:
        text += heading + ' | '
    row:Row
    for row in table.rows:
        rt = '| '
        for c in row.cells:
            rt = rt + c + ' | '
        text += '\n'+rt
    return text
#     rows = [[re.sub(r'\\', r'\\\\', re.sub(r'\n', r'\\n', cell.value)) for cell in row.cells] for row in arg.rows]
#     table = Table(chars=OrderedDict([
#         ('bottom', ''), ('bottom-left', ''), ('bottom-mid', ''), ('bottom-right', ''),
#         ('left', '|'), ('left-mid', ''), ('mid', ''), ('mid-mid', ''), ('middle', '|'),
#         ('right', '|'), ('right-mid', ''), ('top', ''), ('top-left', ''), ('top-mid', ''), ('top-right', ''),
#     ]), style=OrderedDict([
#         ('border', []), ('padding-left', 1), ('padding-right', 1),
#     ]))
#     table.add_rows(rows)
#     return table.table

def format_doc_string(arg):
    return '"""\n' + arg.content + '\n"""'

def format_step(color_fns, test_step:StepStatistics):
    status = test_step.issues[0].status if test_step.issues else Status.passed.name
    text = color_fns.text(status,CHARACTERS[status] + ' ' + test_step.step_type + ' ' + test_step.name)

    if test_step.table:
        text += '\n'+indent(format_table(test_step.table), make_indentation(4,' '))

    message = get_step_messages(color_fns, test_step)
    if message:
        text += '\n'+indent(message, make_indentation(4,' '))
    return text + '\n'

def is_issue(status):
    return IS_ISSUE[status]

def format_issue(color_fns, number, test_case:TestCaseStatistics):
    prefix = f'{number}) '
    text = prefix
    scenario_location =str(test_case.location)
    text += f'Scenario: {test_case.name} # {color_fns.text(ColorTypes.LOCATION,scenario_location)}\n'

    for test_step in test_case.steps:
        formatted_step = format_step(color_fns,test_step)
        text += indent(formatted_step, make_indentation(len(prefix),' '))

    return text
