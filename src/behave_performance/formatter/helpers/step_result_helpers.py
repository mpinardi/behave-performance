from behave.model_core import Status
from behave.textutil import make_indentation, indent
from behave_performance.formatter.color_fns import ColorTypes,ColorFns
from .format_helpers import format_error



def get_failed_step_result_message(color_fns:ColorFns, issue):
    return format_error(issue.exception, color_fns)

def get_pending_step_result_message(color_fns:ColorFns):
    message = 'Pending step. This implies that some issue occured.'
    return color_fns.text(ColorTypes.UNTESTED,message)

def get_step_messages(color_fns:ColorFns, test_step):
    messages = ''
    number = 1
    for issue in test_step.issues:
        message = ''
        if issue.status == Status.failed:
            message = get_failed_step_result_message(color_fns, issue)
        elif issue.status == Status.undefined:
            message = get_undefined_step_result_message(color_fns)
        elif issue.status == Status.untested:
            message = get_pending_step_result_message(color_fns)

        if len(message) > 0:
            message = get_message(number, issue.count, message)
            messages += '\n' + message if len(messages) > 0 else message
        number += 1

    if len(messages) > 0:
        return messages

def get_undefined_step_result_message(color_fns:ColorFns):
    message = 'Undefined. Implement this step.'
    return color_fns.text(ColorTypes.UNDEFINDED,message)

def get_message(number, cnt, message):
    prefix = f"{number}) "
    return f"{prefix}Count: {cnt}\n{indent(message,  make_indentation(len(prefix+'Count')))}"