import unittest
import sys
import os
import asyncio

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/src')
from behave_performance import BehavePerformance
from behave_performance.configuration import Configuration

class RuntimeTest(unittest.TestCase):
    """Test RunTime

    Args:
        unittest (_type_): _description_
    """    
    def test_behave_performance_init(self):
        try:
            args =['./path/to/place','--perf-dry-run','--format','pretty','--format-options','{"what":"where"}',
               '--language','en','--no-strict-stats','--no-format-color',
               '--silent','--silent-progress','--silent-announcements','--plans','./test/plans',
               '--plan-tags', '@simple', '--profile', 'example']
            cfg = Configuration(args)
            bp = BehavePerformance(cfg)
            self.assertEqual(bp.cur_percent,100)
            self.assertTrue(bp.simulations)
        except Exception:
            self.assertTrue(False)
        
    def test_behave_performance_setup(self):
        try:
            args =['./path/to/place','--perf-dry-run','--format','progress','--format-options','{"what":"where"}',
               '--language','en','--no-strict-stats','--no-format-color','--plans','./test/plans',
               '--plan-tags', '@simple', '--profile', 'example']
            cfg = Configuration(args)
            bp = BehavePerformance(cfg)
            asyncio.run(bp.setup())

            self.assertEqual(bp.cur_percent,100)
            self.assertTrue(bp.simulations)
            self.assertTrue(bp.formatters.formatters)
        except Exception:
            self.assertTrue(False)
    
   
if __name__ == '__main__':
    unittest.main()