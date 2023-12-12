from .salad.dialect import DIALECTS
keywords =[
  'plan',
  'simulation',
  'simulationPeriod',
  'group',
  'runners',
  'count',
  'time',
  'rampUp',
  'rampDown',
]

def get_table(headers:list[str], rows:list[list[str]],space=10):
    """Get a string table.

    Args:
        headers (list[str]): Headers to use in the table.
        rows (list[list[str]]): Rows to use in the table.
        space (int, optional): The space for columns. Defaults to 10.

    Returns:
        _type_: _description_
    """
    result = ''
    row_format ='{:<5}' +(f"{{:<{space}}} " * (len(headers)))
    result += row_format.format("", *headers)+'\n'
    for row in rows:
        for i in range(len(row)):
            if not isinstance(row[i], str):
                row[i] = str(row[i])
            result += row_format.format('', *row)+'\n'
    return result

def get_languages():
    """Get a string table of avaliable languages.

    Returns:
        str: A string table of the avaliable languages.
    """
    rows = list(map(lambda lang: [lang[0],lang[1]['name'],lang[1]['native']],DIALECTS.items()))
    return get_table(['ISO 639-1', 'ENGLISH NAME', 'NATIVE NAME'], rows,15)

def get_keywords(iso_code:str):
    """Get Keywords for a given iso code.

    Args:
        iso_code (str): The isocode to look up.

    Returns:
        dtr: The resulting keywords as string table.
    """
    language = DIALECTS[iso_code]
    rows  = []
    for keyword in keywords:
        words = list(map(lambda s: f'"{s}"',language[keyword]))
        rows.append([keyword, words])
    return get_table(['ENGLISH KEYWORD', 'NATIVE KEYWORDS'], rows,30)
