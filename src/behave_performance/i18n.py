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

def get_table(headers:list[str], rows:list[list[str]]):
  result = ''
  row_format ="{:>30}" * (len(headers) + 1)
  result += row_format.format("", *headers)+'\n'
  for row in rows:
      for i in range(len(row)):
        if not isinstance(row[i], str):
          row[i] = str(row[i])
      result += row_format.format('', *row)+'\n'
  return result

def get_languages():
  rows = list(map(lambda lang: [lang[0],lang[1]['name'],lang[1]['native']],DIALECTS.items()))
  return get_table(['ISO 639-1', 'ENGLISH NAME', 'NATIVE NAME'], rows)

def get_keywords(iso_code):
  language = DIALECTS[iso_code]
  rows  = []
  for keyword in keywords:
    words = list(map(lambda s: f'"{s}"',language[keyword]))
    rows.append([keyword, words])
  return get_table(['ENGLISH KEYWORD', 'NATIVE KEYWORDS'], rows)