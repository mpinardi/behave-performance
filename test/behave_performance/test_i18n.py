import unittest
import sys
import os
    
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/src')
from behave_performance.i18n import get_languages,get_keywords,get_table

class i18nTest(unittest.TestCase):
    
    def test_get_languages(self):
        res = get_languages()
        self.assertIn('es',res)
        print(res)
    
    def test_get_language_keywords(self):
        res = get_keywords('es')
        self.assertIn('Tiempo',res)
        print(res)
    
    def test_get_table(self):
        res = get_table(['What','Where'],[['Hat','Head'],['Pillow','Bed']],10)
        self.assertIn('Head',res)
        print(res)
    
if __name__ == '__main__':
    unittest.main()