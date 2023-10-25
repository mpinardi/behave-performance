from salad.ast_builder import AstBuilder
from salad.parser import Parser
from salad.veggies.compiler import Compiler
from salad.errors import ParserError, CompositeParserException
from salad.stream.id_generator import IdGenerator
from salad.token_matcher import TokenMatcher

def create_errors(errors, uri):
    for error in errors:
        yield {
            'type': 'salad-parser-error',
            'parse_error': {
            'source': {
                'uri': uri,
                'location': error.location
            },
            'message': str(error)
        }}


class SaladEvents:
    def __init__(self, language:str='en',source:bool=True,ast:bool=True,veggies:bool=True):
        self.id_generator = IdGenerator()
        self.parser = Parser(ast_builder=AstBuilder(self.id_generator))
        self.compiler = Compiler(self.id_generator)
        self.token_matcher = TokenMatcher(language)
        self.source = source
        self.ast = ast
        self.veggies = veggies

    def enum(self, source_event):
        uri = source_event['source']['uri']
        source = source_event['source']['data']

        try:
            salad_document = self.parser.parse(source,self.token_matcher)
            salad_document['uri'] = uri

            if (self.source):
                source_event['type'] = 'source'
                yield source_event
            if (self.ast):
                yield {
                    'type': 'salad-document',
                    'salad_document': salad_document
                }
            if (self.veggies):
                veggies = self.compiler.compile(salad_document)
                for veggie in veggies:
                    yield {
                        'veggie': veggie,
                        'type': 'veggie'
                    }
        except CompositeParserException as e:
            for event in create_errors(e.errors, uri):
                yield event
        except ParserError as e:
            for event in create_errors([e], uri):
                yield event
