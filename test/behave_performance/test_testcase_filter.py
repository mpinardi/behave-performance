import unittest
import sys
import os
import asyncio
from behave.runner_util import \
    collect_feature_locations, parse_features, \
    exec_file, load_step_modules, PathManager
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/src')
from behave_performance.testcase_filter import TestCaseFilter,make_tag_expression

class TestCaseFilterTest(unittest.TestCase):
    """Test TestCaseFilter

    Args:
        unittest (_type_): _description_
    """    

    def setUp(self):
        p = os.path.realpath('.\\test\\features')
        fl = collect_feature_locations([os.path.normpath(p)])
        self.features = parse_features(fl, 'en')

    def test_test_case_filter_feature_level_tag(self):
        try:
            fs = TestCaseFilter(self.features).filter('@t1')
            self.assertTrue(len(fs)==1)
            self.assertTrue('t1' in fs[0].tags)
        except Exception:
            self.assertTrue(False)
        
    def test_test_case_filter_scenario_level_tag(self):
        try:
            fs = TestCaseFilter(self.features).filter('@only1')
            self.assertTrue(len(fs)==1)
            self.assertEqual(fs[0].name,'test')
        except Exception:
            self.assertTrue(False)

    def test_test_case_filter_feature_file_name(self) -> None:
        try:
            fs = TestCaseFilter(self.features).filter('test2')
            self.assertEqual(len(fs),1)
            self.assertEqual(fs[0].name,'test 2')
        except Exception:
            self.assertTrue(False)
    
    def test_test_case_filter_feature_name(self) -> None:
        try:
            fs = TestCaseFilter(self.features).filter('My test 3')
            self.assertEqual(len(fs),1)
            self.assertEqual(fs[0].name,'My test 3')
        except Exception:
            self.assertTrue(False)
if __name__ == '__main__':
    unittest.main()