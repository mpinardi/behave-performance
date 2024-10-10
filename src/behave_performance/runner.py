from multiprocessing import Queue
from queue import Empty
from io import StringIO
import sys
from concurrent.futures import ThreadPoolExecutor
from behave.configuration import Configuration
from behave_performance._behave.perf_runner_builder import PerfRunnerBuilder,PerfRunner
from behave_performance.tasks import RUNNER_TASKS,Task
from behave_performance.results import GroupResult

def manager(uid,thread_count:int,input_queue: Queue, result_queue: Queue, bargs):
    """Manger process which handles queues and threads.

    Args:
        uid (_type_): The id for the manager process.
        thread_count (int): The thread count to start with.
        input_queue (Queue): Input queue for jobs.
        result_queue (Queue): Result queue for results.
        bargs (args): The behave args to pass to the runners.
    """
    #Capture all stdout as string
    #TODO do something with the captured out
    stdout = sys.stdout
    sys.stdout = capture = StringIO()
    cur_max = thread_count
    running = 0
    cargs = []
    if 'filename' in bargs:
        for path in bargs['filename']:
            cargs.append( path) 
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
        result_queue.put((uid,res))#(index, res)
        nonlocal running
        running = running - 1

    def run_thread(group:dict):
        future = executor.submit(trunner,rb.build_runner(group))
        future.add_done_callback(on_completed)
        nonlocal running
        running = running + 1

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        executing = True
        # This will hold onto the last run Task if it can't run it
        #   Which could cause it to hang if no prevous Tasks clear
        last_t:Task = None
        while executing:
            try:
                if last_t:
                    t:Task = last_t
                    last_t = None
                else:
                    t:Task = input_queue.get(False) 
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

def trunner(runner:PerfRunner):
    """Thread Runner

    Args:
        runner (PerfRunner): The runner to run.

    Returns:
       GroupResult: The resulting group result.
    """
    behave_result = runner.run()
    result = GroupResult.from_features(behave_result[0], behave_result[1],
        behave_result[2], not behave_result[3])
    return result
