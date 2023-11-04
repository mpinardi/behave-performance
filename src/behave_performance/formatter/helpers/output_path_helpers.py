import re
import datetime
from behave_performance.helpers.datetime_format import js_to_python


ARGUMENT_POSTFIX_PATTERN = r'([^|]+)\|(.*)'
ARGUMENT_POSTFIX_SEPARATOR_PATTERN = r'-|\[|\]|\(|\)|\{|}|_'
ARGUMENT_POSTFIX_PART_PATTERN = r'(?:(?!#).)+?(?=@)|(?:(?!@).)+?(?=#)|#.*$|@.*$'

def get_path_with_prefix(output_to, count):
    argument_with_postfix = re.match(ARGUMENT_POSTFIX_PATTERN , output_to)
    path = argument = ''
    if argument_with_postfix:
        path = argument_with_postfix.group(1)
        argument = argument_with_postfix.group(2)
    else:
        path = output_to

    return path + parse_postfix(argument, count)

def parse_postfix(argument, count):
    a = argument.split('.')
    args = []

    if len(a) > 1:
        match = re.search(ARGUMENT_POSTFIX_SEPARATOR_PATTERN, a[0])
        
        while match:
            if match.start() > 0:
                args.append(a[0][:match.start()])
            a[0] = a[0][match.end():]
            match = re.search(ARGUMENT_POSTFIX_SEPARATOR_PATTERN, a[0])
        
        if len(a[0]) > 0:
            args.append(a[0])
        
        if not args:
            args.append(a[0])

    for larg in args:
        m = re.search(ARGUMENT_POSTFIX_PART_PATTERN, larg)

        while m:
            value = larg[1:len(str(m.group()))]
            
            if value.isnumeric():
                argument = argument.replace('#' + value, str(count).zfill(len(value)))
            elif value:
                argument = argument.replace('@' + value, get_date_time(value))
            
            larg = larg[len(str(m.group())):]
            m = re.search(ARGUMENT_POSTFIX_PART_PATTERN, larg)
    
    return argument

def get_date_time(value):
    return datetime.datetime.now().strftime(js_to_python(value))
