import unittest
import sys
import os
    
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/src')
from behave_performance.arguments import parse_arguments,BEHAVE_ARGS,BEHAVE_PERFORMANCE_ARGS

class ArgumentsTest(unittest.TestCase):

    def test_parse_arguments_perf(self):
        args =['./path/to/place','--perf-dry-run','--format','pretty','--format-options','{}',
               '--language','en','--no-strict-stats','--no-format-color',
               '--silent','--silent-progress','--silent-announcements','--plans','../plans',
               '--plan-tags', '@simple', '--perf-name', 'test', '--profile', 'example']
        pargs= parse_arguments(args)
        for pa in BEHAVE_PERFORMANCE_ARGS:
            if not hasattr(pargs,self.replace_dash(pa)):
                self.fail(f"{pa} was not found.")
    
    def test_parse_arguments_perf_format_options(self):
        args =['./path/to/place','--plans','../plans','--format-options','{"what":"where"}','--format-options','{"then":"how"}']
        pargs= parse_arguments(args)
        if not hasattr(pargs,'format_options'):
            self.fail(f"format_options was not found.")
        self.assertEqual(pargs.format_options,{'what': 'where', 'then': 'how'})
    
    def test_parse_arguments_perf_no_plans_but_languages_both(self):
        try:
            args =['--i18n-keywords','en','--i18n-languages']
            pargs= parse_arguments(args)
        except SystemExit:
            return
        self.fail('')
    
    def test_parse_arguments_perf_no_plans_but_languages(self):
        try:
            args =['--i18n-languages']
            pargs= parse_arguments(args)
        except SystemExit:
            return
        self.fail('')

    def test_parse_arguments_perf_no_plans(self):
        try:
            args =['--format','pretty']
            pargs= parse_arguments(args)
        except SystemExit:
            return
        self.fail('Did not post message about required plans')
    
    def test_parse_arguments_perf_no_features(self):
        try:
            args =['--plans','../plans','--format','pretty']
            pargs= parse_arguments(args)
        except SystemExit:
            return
        self.fail('Did not post message about required plans')
    
    def replace_dash(self,name:str)->str:
        return name.replace('-','_')
if __name__ == '__main__':
    unittest.main()