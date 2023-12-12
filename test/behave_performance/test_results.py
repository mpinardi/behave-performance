import unittest
import sys
import os
from datetime import datetime
from behave.model import Step,Scenario,Feature
from behave.model_core import FileLocation
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/src')
from behave_performance.results import StepResult, ScenarioResult,GroupResult, FeatureResult, Result, is_success

class ResultsTest(unittest.TestCase):
    """Test Results

    Args:
        unittest (_type_): _description_
    """    
    def test_step_result_init(self):
        try:
            r = StepResult('name',1.1,'passed','../features/','when','when',None,None,None,None,None)
            self.assertEqual(r.name,'name')
            self.assertEqual(r.status,'passed')
        except Exception:
            self.assertTrue(False)
    
    def test_step_result_from_dict(self):
        try:
            r = StepResult.from_dict({'name':'name','duration':1.1,'status':'passed','location':{'filename':'../features/','line':20},'keyword':'when','step_type':
                                      'when','table':None,'error_message':None,'exception':None,'traceback':None,'hook_failed':False})
            self.assertEqual(r.name,'name')
            self.assertEqual(r.status,'passed')
            self.assertEqual(r.location.line,20)
        except Exception:
            self.assertTrue(False)
    
    def test_step_result_from_step(self):
        try:
            r = StepResult.from_step(Step('../features/myfeature.feature',120,'when','when','myname','Hello this is my text',None))
            self.assertEqual(r.name,'myname')
            self.assertEqual(r.location.line,120)
        except Exception:
            self.assertTrue(False)

    def test_scenario_result_init(self):
        try:
            r = ScenarioResult('name',1.1,[],'passed',FileLocation('../features/',12))
            self.assertEqual(r.name,'name')
            self.assertEqual(r.status,'passed')
            self.assertEqual(r.location.line,12)
        except Exception:
            self.assertTrue(False)
    
    def test_scenario_result_from_dict(self):
        try:
            r = ScenarioResult.from_dict({'name':'name','duration':1.1,'steps':[],'status':'passed','location':{'filename':'../features/','line':20}})
            self.assertEqual(r.name,'name')
            self.assertEqual(r.status,'passed')
            self.assertEqual(r.location.line,20)
        except Exception:
            self.assertTrue(False)
    
    def test_scenario_result_from_scenario(self):
        try:
            r = ScenarioResult.from_scenario(Scenario('../features/myfeature.feature',120,'scenario','myname',['@myname'],[],''))
            self.assertEqual(r.name,'myname')
            self.assertEqual(r.location.line,120)
        except Exception:
            self.assertTrue(False)


    def test_feature_result_init(self):
        try:
            r = FeatureResult('name',datetime.now(),datetime.now(),2.1,[],True,'passed')
            self.assertEqual(r.name,'name')
            self.assertEqual(r.status,'passed')
        except Exception:
            self.assertTrue(False)
    
    def test_feature_result_from_dict(self):
        try:
            r = FeatureResult.from_dict({'name':'name','start':str(datetime.now()),'stop':str(datetime.now()),'duration':1.1,'test_cases':[],'success':True,'status':'passed'})
            self.assertEqual(r.name,'name')
            self.assertEqual(r.status,'passed')
        except Exception:
            self.assertTrue(False)
    
    def test_feature_result_from_feature(self):
        try:
            r = FeatureResult.from_feature(Feature('../features/myfeature.feature',120,'feature','myname',['@myname'],[],[]))
            self.assertEqual(r.name,'myname')
        except Exception:
            self.assertTrue(False)

    def test_group_result_init(self):
        try:
            f=FeatureResult('name',datetime.now(),datetime.now(),2.1,[],True,'passed')
            r = GroupResult('12','name',[f],True)
            self.assertEqual(r.name,'name')
            self.assertEqual(r.success,second=True)
        except Exception:
            self.assertTrue(False)
    
    def test_group_result_from_dict(self):
        try:
            f ={'name':'name','start':str(datetime.now()),'stop':str(datetime.now()),'duration':1.1,'test_cases':[],'success':True,'status':'passed'}
            r = GroupResult.from_dict({'id':'12','name':'name','results':[f],'success':True})
            self.assertEqual(r.name,'name')
            self.assertEqual(r.success,True)
        except Exception:
            self.assertTrue(False)
    
    def test_group_result_from_features(self):
        try:
            f = GroupResult.from_features('12','myname',[Feature('../features/myfeature.feature',120,'feature','myname',['@myname'],[],[])],True)
            self.assertEqual(f.name,'myname')
        except Exception:
            self.assertTrue(False)

    def test_result_init(self):
        try:
            f= FeatureResult('name',datetime.now(),datetime.now(),2.1,[],True,'passed')
            g = GroupResult('12','name',[f],True)
            r = Result('name',datetime.now(),datetime.now(),2.1,{'name':g},True)
            self.assertEqual(r.name,'name')
            self.assertEqual(r.success,second=True)
        except Exception:
            self.assertTrue(False)
    
    def test_result_add_group(self):
        try:
            f= FeatureResult('name',datetime.now(),datetime.now(),2.1,[],True,'passed')
            g = GroupResult('12','name',[f],True)
            r = Result('name',datetime.now())
            r.add_group_result(g)
            self.assertEqual(r.name,'name')
            self.assertEqual(r.success,second=True)
        except Exception:
            self.assertTrue(False)

    def test_is_success(self):
        try:
            self.assertEqual(is_success('passed'),True)
            self.assertEqual(is_success('pending'),True)
            self.assertEqual(is_success('executing'),False)
            self.assertEqual(is_success('failed'),False)
            self.assertEqual(is_success('undefined'),False)
        except Exception:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
    