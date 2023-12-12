import unittest
import sys
import os

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/src')
from behave_performance.option_spliter import split

class OptionSplitterTest(unittest.TestCase):
    """Test Option spliter

    Args:
        unittest (_type_): _description_
    """    
    def test_split_empty(self):
        try:
            r = split('')
            self.assertEqual(r['type'],'')
            self.assertEqual(r['output_to'],'')
            self.assertEqual(r['options'],[])
        except Exception:
            self.assertTrue(False)
    
    def test_split_no_output_options(self):
        try:
            r = split('pretty')
            self.assertEqual(r['type'],'pretty')
            self.assertEqual(r['output_to'],'')
            self.assertEqual(r['options'],[])
        except Exception:
            self.assertTrue(False)
    
    def test_split_output_no_options(self):
        try:
            r = split('pretty:where/to')
            self.assertEqual(r['type'],'pretty')
            self.assertEqual(r['output_to'],'where/to')
            self.assertEqual(r['options'],[])
        except Exception:
            self.assertTrue(False)
        
    def test_split_output_option(self):
        try:
            r = split('pretty:where/to:opt')
            self.assertEqual(r['type'],'pretty')
            self.assertEqual(r['output_to'],'where/to')
            self.assertEqual(r['options'],['opt'])
        except Exception:
            self.assertTrue(False)

    def test_split_output_options(self):
        try:
            r = split('pretty:where/to:opt,opt2,opt3')
            self.assertEqual(r['type'],'pretty')
            self.assertEqual(r['output_to'],'where/to')
            self.assertEqual(r['options'],['opt','opt2','opt3'])
        except Exception:
            self.assertTrue(False)
    
    def test_split_no_output_options(self):
        try:
            r = split('pretty::opt,opt2,opt3')
            self.assertEqual(r['type'],'pretty')
            self.assertEqual(r['output_to'],'')
            self.assertEqual(r['options'],['opt','opt2','opt3'])
        except Exception:
            self.assertTrue(False)

    def test_split_no_type_output_options(self):
        try:
            r = split('::opt,opt2,opt3')
            self.assertEqual(r['type'],'')
            self.assertEqual(r['output_to'],'')
            self.assertEqual(r['options'],['opt','opt2','opt3'])
        except Exception:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()