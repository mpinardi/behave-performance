import unittest
import sys
import os

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/src')
from behave_performance.configuration import Configuration

class ConfigurationTest(unittest.TestCase):
    
    def test_configuration(self):
        args =['./path/to/place','--perf-dry-run','--format','pretty','--format-options','{"what":"where"}',
               '--language','es','--no-strict-stats','--no-format-color',
               '--silent','--silent-progress','--silent-announcements','--plans','../plans',
               '--plan-tags', '@simple', '--perf-name', 'test', '--profile', 'example']
        cfg = Configuration(args)
        self.assertIn('pretty',cfg.format,'Format missing')
        self.assertEqual("where",cfg.format_options['what'],'Format option missing')
        self.assertIn('es',cfg.language,'Language missing')
        self.assertIn('../plans',cfg.plans,'Plans missing')
        self.assertIn('test',cfg.perf_name,'Perf Name missing')
        self.assertIn('example',cfg.profile,'Profile missing')
        self.assertIn('@simple',cfg.plan_tags,'Plan Tags missing')
        self.assertEqual(cfg.silent,second=True)
        self.assertEqual(cfg.silent_progress,second=True)
        self.assertEqual(cfg.silent_announcements,second=True)
        self.assertEqual(cfg.no_format_color,second=True)
        self.assertEqual(cfg.strict,second=False)
        
 
    
 
if __name__ == '__main__':
    unittest.main()