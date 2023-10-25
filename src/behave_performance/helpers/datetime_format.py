JS_TO_PY = {
    'YYYY': '%Y',
    'MM': '%m',
    'DD': '%d',
    'T': 'T',
    ':': ':',
    '.': '.',
    'HH': '%H',
    'mm': '%M',
    'ss': '%S',
    'sss': '%f'
}

def is_java_format(time:str)->bool:
    for key, value in enumerate(JS_TO_PY):
        if key in time and key != value:
            return True
    return False

def js_to_python(time:str)->str:
    for key, value in JS_TO_PY.items():
        if key in time:
            time = time.replace(key,value)
    return time


# YYYY is the year, with four digits (0000 to 9999), or as an expanded year of + or - followed by six digits. The sign is required for expanded years. -000000 is explicitly disallowed as a valid year.
# MM is the month, with two digits (01 to 12). Defaults to 01.
# DD is the day of the month, with two digits (01 to 31). Defaults to 01.
# T is a literal character, which indicates the beginning of the time part of the string. The T is required when specifying the time part.
# HH is the hour, with two digits (00 to 23). As a special case, 24:00:00 is allowed, and is interpreted as midnight at the beginning of the next day. Defaults to 00.
# mm is the minute, with two digits (00 to 59). Defaults to 00.
# ss is the second, with two digits (00 to 59). Defaults to 00.
# sss is the millisecond, with three digits (000 to 999). Defaults to 000.
# Z is the timezone offset, which can either be the literal character Z (indicating UTC), or + or - followed by HH:mm, the offset in hours and minutes from UTC.



# (9)

# %I

# Hour (12-hour clock) as a zero-padded decimal number.

# 01, 02, …, 12


# %f

# Microsecond as a decimal number, zero-padded to 6 digits.

# 000000, 000001, …, 999999

# (5)

# %z

# UTC offset in the form ±HHMM[SS[.ffffff]] (empty string if the object is naive).

# (empty), +0000, -0400, +1030, +063415, -030712.345216

# (6)

# % %b

# % Month as locale’s abbreviated name.

# % Jan, Feb, …, Dec (en_US);
# % Jan, Feb, …, Dez (de_DE)
# % (1)

# % %B

# % Month as locale’s full name.

# % January, February, …, December (en_US);
# % Januar, Februar, …, Dezember (de_DE)
# % (1)
# % %y

# % Year without century as a zero-padded decimal number.

# % 00, 01, …, 99

# % (9)

# % %p

# % Locale’s equivalent of either AM or PM.

# % AM, PM (en_US);
# % am, pm (de_DE)
# % (1), (3)


# % %Z

# % Time zone name (empty string if the object is naive).

# % (empty), UTC, GMT

# % (6)

# % %j

# % Day of the year as a zero-padded decimal number.

# % 001, 002, …, 366

# % (9)

# % %U

# % Week number of the year (Sunday as the first day of the week) as a zero-padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0.

# % 00, 01, …, 53

# % (7), (9)

# % %W

# % Week number of the year (Monday as the first day of the week) as a zero-padded decimal number. All days in a new year preceding the first Monday are considered to be in week 0.

# % 00, 01, …, 53

# % (7), (9)

# % %c

# % Locale’s appropriate date and time representation.

# % Tue Aug 16 21:30:00 1988 (en_US);
# % Di 16 Aug 21:30:00 1988 (de_DE)
# % (1)

# % %x

# % Locale’s appropriate date representation.

# % 08/16/88 (None);
# % 08/16/1988 (en_US);
# % 16.08.1988 (de_DE)
# % (1)

# % %X

# % Locale’s appropriate time representation.

# % 21:30:00 (en_US);
# % 21:30:00 (de_DE)
# % (1)


# % %a

# % Weekday as locale’s abbreviated name.

# % Sun, Mon, …, Sat (en_US);
# % So, Mo, …, Sa (de_DE)
# % (1)

# % %A

# % Weekday as locale’s full name.

# % Sunday, Monday, …, Saturday (en_US);
# % Sonntag, Montag, …, Samstag (de_DE)
# % (1)

# % %w

# % Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.

# % 0, 1, …, 6