import os
from optparse import OptionParser
import sys
if sys.version_info < (3, 0):
    string_type = basestring
    if os.name != 'nt':
        import codecs
        UTF8Writer = codecs.getwriter('utf8')
        sys.stdout = UTF8Writer(sys.stdout)
else:
    string_type = str

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import json
from salad.stream.salad_events import SaladEvents
from salad.stream.source_events import SourceEvents

parser = OptionParser()
parser.add_option("--no-source",  action="store_false", dest="print_source",  default=True, help="don't print source events")
parser.add_option("--no-ast",     action="store_false", dest="print_ast",     default=True, help="don't print ast events")
parser.add_option("--no-veggies", action="store_false", dest="print_veggies", default=True, help="don't print veggie events")

(options, args) = parser.parse_args()

source_events = SourceEvents(args)
salad_events = SaladEvents(options)

for source_event in source_events.enum():
    for event in salad_events.enum(source_event):
        print(json.dumps(event))
