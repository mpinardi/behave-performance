import unittest
import sys
import os
from pyee import EventEmitter
import asyncio
    
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/src')
from behave_performance.formatter_init import FormattersInitializer
from behave_performance.configuration import Configuration
from behave_performance.formatter import AnnouncementFormatter,ProgressFormatter,StdDeviationCreator,StatisticsFormatter,SilentProgressFormatter,SimpleProgressFormatter,TaurusFormatter,SummaryFormatter,ChartPointsFormatter

class FormattersInitializerTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):
        ee = EventEmitter()
        args =['./features','-p','./plans']
        fi = FormattersInitializer(sys.stdout,os.getcwd(),Configuration(args))
    
    
    def test_initalize_formatters(self):
        ee = EventEmitter()
        args =['./features','--plans','./plans','--format','progress','--format','taurus']
        fi = FormattersInitializer(sys.stdout,os.getcwd(),Configuration(args))
        asyncio.run(fi.initialize_formatters(ee))
        self.assertEqual(len(fi.formatters),5)
        self.assertTrue(isinstance(fi.formatters[0]['formatter'],ProgressFormatter))
        self.assertTrue(isinstance(fi.formatters[1]['formatter'],TaurusFormatter))
        self.assertTrue(isinstance(fi.formatters[2]['formatter'],AnnouncementFormatter))
        self.assertTrue(isinstance(fi.formatters[3]['formatter'],SummaryFormatter))
        self.assertTrue(isinstance(fi.formatters[4]['formatter'],StatisticsFormatter))
    

    def test_initalize_formatter(self):
        ee = EventEmitter()
        args =['./features','--plans','./plans','--format','progress','--format','taurus']
        fi = FormattersInitializer(sys.stdout,os.getcwd(),Configuration(args))
        result = asyncio.run(fi.initialize_formatter(ee ,{"type":'progress',"output_to":"","options":""},True,{'cwd':os.getcwd(),"colors_enabled":False}))
        self.assertTrue(isinstance(result['formatter'],ProgressFormatter))
    
    def test_initalize_formatter_bad(self):
        ee = EventEmitter()
        args =['./features','--plans','./plans','--format','pretty','--format','taurus']
        fi = FormattersInitializer(sys.stdout,os.getcwd(),Configuration(args))
        result = asyncio.run(fi.initialize_formatter(ee ,{"type":'prog',"output_to":"","options":""},True,{'cwd':os.getcwd(),"colors_enabled":False}))
        self.assertEqual(result,None)
    
    def test_update_formatters(self):
        ee = EventEmitter()
        args =['./features','--plans','./plans','--format','chartpoints:C:/test/chartpoints|_#1.csv']
        fi = FormattersInitializer(sys.stdout,os.getcwd(),Configuration(args))
        asyncio.run(fi.initialize_formatters(ee))
        self.assertEqual(len(fi.formatters),5)
        self.assertTrue(isinstance(fi.formatters[0]['formatter'],ChartPointsFormatter))
        self.assertTrue(isinstance(fi.formatters[1]['formatter'],AnnouncementFormatter))
        self.assertTrue(isinstance(fi.formatters[3]['formatter'],SummaryFormatter))
        self.assertTrue(isinstance(fi.formatters[4]['formatter'],StatisticsFormatter))
        priorstream = fi.formatters[0]['formatter'].stream.name
        asyncio.run(fi.update_formatters(1))
        self.assertNotEqual(fi.formatters[0]['formatter'].stream.name,priorstream)

 
if __name__ == '__main__':
    unittest.main()