from multiprocessing import Queue
from queue import Empty
from behave.configuration import Configuration
from ._behave.perf_runner_builder import PerfRunnerBuilder
from behave_performance.tasks import RUNNER_TASKS,task
from concurrent.futures import ThreadPoolExecutor
from behave_performance.results import GroupResult
from functools import partial
from io import StringIO
import sys

#This is for threading or proccessing only. No combo.
def runner(input_queue: Queue, result_queue: Queue, bargs):
    config = Configuration(bargs,
                           load_config=False,
                           stdout_capture=False,
                           stderr_capture=False,
                           log_capture=False,
                           )
    if not config.format:
        config.format = [config.default_format]
    rb = PerfRunnerBuilder(config)
    
    for group in iter(input_queue.get, 'STOP'):
        behave_result = rb.build_runner(group).run()
        result = GroupResult.from_features(behave_result[0], behave_result[1], behave_result[2],not behave_result[3])
        result_queue.put(result)

def manager(id,thread_count,input_queue: Queue, result_queue: Queue, bargs):
    #Capture all stdout as string
    #TODO do something with the captured out
    stdout = sys.stdout
    sys.stdout = capture = StringIO()
    cur_max = thread_count
    running = 0
    cargs = []
    if 'filename' in bargs:
        cargs.append(bargs['filename'])
    config = Configuration(cargs,
        load_config=False,
        stdout_capture=False,
        stderr_capture=False,
        log_capture=False,
        **bargs
    )
    if not config.format:
        config.format = [config.default_format]
    rb = PerfRunnerBuilder(config)
    
    def on_completed(future):
        res = future.result()
        result_queue.put((id,res))#(index, res)
        nonlocal running
        running = running - 1

    def run_thread(group:dict):
        future = executor.submit(trunner,rb.build_runner(group))
        future.add_done_callback(on_completed)
        nonlocal running
        running = running + 1

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        executing = True
        # This will hold onto the last run task if it can't run it
        #   Which could cause it to hang if no prevous tasks clear
        last_t:task = None
        while executing:
            try:
                if last_t:
                    t:task = last_t
                    last_t = None
                else:
                    t:task = input_queue.get(False) 
                match t.task:
                    case RUNNER_TASKS.STOP_ALL.name:
                        executing = False
                    case RUNNER_TASKS.RAMP.name:
                        cur_max = cur_max + t.message
                    case RUNNER_TASKS.RUN.name:
                        if running < cur_max:
                            run_thread(t.message)
                        else:
                            last_t = t
                            
            except Empty:
                pass
        # Wait for remaining threads
        while running > 0:
            pass
        # Reset Std out
        sys.stdout = stdout
    
def trunner(runner):
    behave_result = runner.run()
    result = GroupResult.from_features(behave_result[0], behave_result[1], behave_result[2], not behave_result[3])
    return result
