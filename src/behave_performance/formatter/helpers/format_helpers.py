import json
from formatter.color_fns import ColorFns, ColorTypes
from behave.textutil import indent, make_indentation

def format_error(err, color_fns:ColorFns = ColorFns(True), should_inline_diff:bool=False ):
    message = ''
    trace =''
    if err:
        if err.message:
            message = str(err.message)
        
        # if hasattr(err, 'message') and callable(getattr(err.message, 'toString', None)):
        #     message = str(err.message)
        # elif callable(getattr(err, 'inspect', None)):
        #     message = str(err.inspect())
        # elif isinstance(err, str):
        #     message = err
        # else:
        #     message = json.dumps(err)

        # stack = getattr(err, 'stack', message)
        # start_of_message_index = stack.find(message)

        # if start_of_message_index == -1:
        #     stack = '\n' + stack
        # else:
        #     end_of_message_index = start_of_message_index + len(message)
        #     message = stack[:end_of_message_index]
        #     stack = stack[end_of_message_index:]

        # if hasattr(err, 'uncaught') and err.uncaught:
        #     message = 'Uncaught ' + message

        # actual = getattr(err, 'actual', None)
        # expected = getattr(err, 'expected', None)

        # if (
        #     err.get('showDiff', True)
        #     and type(actual) == type(expected)
        #     and expected is not None
        # ):
        #     if not (isinstance(actual, str) and isinstance(expected, str)):
        #         actual = json.dumps(actual)
        #         expected = json.dumps(expected)

        #     match = message.split(':')[0]
        #     message = color_fns.text(ColorTypes.ERROR_MESSAGE,match if match else message)

        #     if should_inline_diff:
        #         message += inline_diff(actual, expected, color_fns)
        #     else:
        #         message += unified_diff(actual, expected, color_fns)
        # else:
        #     message = color_fns.text(ColorTypes.ERROR_MESSAGE,message)

        if err.traceback:
            trace = color_fns.text(ColorTypes.ERROR_STACK, json.dumps(err.traceback))
        return err.type+': '+message + '\n'+ indent(trace, make_indentation(4,' '))
    return ''

def inline_diff(actual, expected, colorFns):
    # Implementation for inline_diff
    pass

def unified_diff(actual, expected, colorFns):
    # Implementation for unified_diff
    pass

def format_location(obj):
    return f'{object.location}+{object.line}'