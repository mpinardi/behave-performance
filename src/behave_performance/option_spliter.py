import re

def split(option):
    parts = re.split(r':(?!\/|//)', option)

    def split_options(option):
        parts = option.split(',')
        return parts
    result = []
    for i, part in enumerate(parts):
        if i > 2:
            result[2]=result[2]+':'+part
        else:
            result.append(part)
    if not len(result) > 1:
        result.append('')
    if not len(result) > 2:
        result.append([])
    else:
        result[2] = split_options(result[2])

    return {"type": result[0], "output_to": result[1], "options": result[2]}
