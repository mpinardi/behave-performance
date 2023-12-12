import unittest
import sys
import os
import asyncio

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/src')
from behave_performance.tasks import Task, RUNNER_TASKS

class TasksTest(unittest.TestCase):
    """Test tasks

    Args:
        unittest (_type_): _description_
    """    
    def test_task(self):
        try:
            t = Task('example','message')
            self.assertEqual(t.task,'example')
            self.assertEqual(t.message,'message')
        except Exception:
            self.assertTrue(False)

    def test_runner_task_create(self):
        try:
            t = RUNNER_TASKS.create(RUNNER_TASKS.RUN,'my message')
            self.assertEqual(t.task,'RUN')
            self.assertEqual(t.message,'my message')
        except Exception:
            self.assertTrue(False)
        
if __name__ == '__main__':
    unittest.main()