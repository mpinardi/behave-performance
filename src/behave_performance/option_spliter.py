import re

def split(option:str):
    """Splits type, output and options from a formatter string
        example: "pretty:C:/outputto/text.txt:opt1,opt2"

    Args:
        option (str): The formatter string to split.

    Returns:
        dict: A dict with type, output_to and options
    """
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
    if result <= 1:
        result.append('')
    if result <= 2:
        result.append([])
    else:
        result[2] = split_options(result[2])

    return {"type": result[0], "output_to": result[1], "options": result[2]}
