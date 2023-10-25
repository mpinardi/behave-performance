from __future__ import print_function
import json
from .parser import Parser
from .token_scanner import TokenScanner
from .veggies.compiler import compile
from .errors import ParserException, CompositeParserException

class Inout(object):
    def __init__(self, print_source, print_ast, print_veggies):
        self.print_source = print_source
        self.print_ast = print_ast
        self.print_veggies = print_veggies
        self.parser = Parser()
        self.parser.stop_at_first_error = False

    def process(self, input, output):
        line = input.readline().rstrip()
        event = json.loads(line)
        if (event['type'] == 'source'):
            uri = event['uri']
            source = event['data']
            token_scanner = TokenScanner(source)

            try:
                salad_document = self.parser.parse(token_scanner)
                if (self.print_source):
                    print(line, file=output)
                if (self.print_ast):
                    print(json.dumps(salad_document), file=output)
                if (self.print_veggies):
                    veggies = compile(salad_document, uri)
                    for veggie in veggies:
                        print(json.dumps(veggie), file=output)
            except CompositeParserException as e:
                self.print_errors(output, e.errors, uri)
            except ParserException as e:
                self.print_errors(output, [e], uri)

    def print_errors(self, output, errors, uri):
        for error in errors:
            attachment = {
                'type': "attachment",
                'source': {
                    'uri': uri,
                    'start': {
                        'line': error.location['line'],
                        'column': error.location['column']
                    }
                },
                'data': error.message,
                'media': {
                    'encoding': "utf-8",
                    'type': "text/x.cucumber.stacktrace+plain"
                }
            }
            print(json.dumps(attachment), file=output)
