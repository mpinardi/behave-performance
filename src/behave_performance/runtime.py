import os
import datetime
import math
import random
import sys
import asyncio
from datetime import timedelta, datetime
from multiprocessing import Process, Queue, cpu_count
import pkg_resources
from pyee.asyncio import AsyncIOEventEmitter
from behave_performance.configuration import Configuration
from behave_performance.helpers.paths import expand_plan_paths
from behave_performance.helpers.simulation import get_simulations_from_filesystem, validate_simulation
from behave_performance.formatter_init import FormattersInitializer
from behave_performance.events import PerfEvents
from behave_performance.runner import manager
from behave_performance.tasks import RUNNER_TASKS
from behave_performance.results import Result
from behave_performance.helpers.utils import set_interval_async
from behave_performance.veggie_filter import VeggieFilter



def version():
    """Get version"""
    vs = 'dev'
    try:
        vs = pkg_resources.get_distribution(__package__).version
    except Exception:
        pass

    return vs

class BehavePerformance(object):
    """
    Behave Performance
    ~~~~~~~~~~~~~~~~~~~~~

    """

    def __init__(self, config:Configuration):
        self.config = config
        self.ee = AsyncIOEventEmitter()
        self.ee.add_listener(PerfEvents.CUKE_RUN_FINISHED,
                             self.__listener_cuke_finished)
        self.ee.add_listener(PerfEvents.FORMATTER_STARTED,
                             self.__listener_formatter_started)
        self.ee.add_listener(PerfEvents.FORMATTER_FINISHED,
                             self.__listener_formatter_finished)
        self.formatters_running = []
        if not config.plans:
            raise Exception('Behave_Performance can not run. No plans where passed into the configuration')
        plan_paths = expand_plan_paths(self.config.plans)
        self.simulations = get_simulations_from_filesystem(self.ee, self.config.language,
            plan_paths, 'defined:none', VeggieFilter(plan_paths, self.config.perf_name,
            self.config.plan_tags))
        self.results = []
        self.formatters = FormattersInitializer(sys.stdout,os.getcwd(),config)
        self.__set_defaults()

    def __set_defaults(self):
        self.task_queues = []
        self.groups = {}
        self.processes = []  # [avaliable_threads,max_threads,process]
        self.cur_max_runners = 0
        self.max_ramp_periods = 20
        self.max_runners = 0
        self.max_ran = 0
        self.running = 0
        self.ran = 0
        self.end_ramp = None
        self.ramp_down = None
        self.ramp_up = None
        self.cur_percent = 100
        self.executing = False
        self.begin_end = None
        self.simulation = None
        self.scheduled_runtime = None
        self.ramper = None
        self.random_wait = 0

    async def setup(self):
        """Initalizes the formatters and validates simulations.
        """
        # format_options = {
        #     "colors_enabled": not self.config.no_format_color,
        #     "cwd": os.getcwd(),
        # }
        await self.formatters.initialize_formatters(self.ee,self.config.format_options)
        # Validation simulations remove if issues
        for sim in self.simulations:
            validation = validate_simulation(sim['veggie'])
            if validation[1]:
                self.ee.emit(PerfEvents.ANNOUNCEMENT,validation)
            if not validation[0]:
                self.simulations.remove(sim)

    async def run(self):
        """Runs the configured simulations.

        Returns:
            bool: True if sucess otherwise false.
        """
        await self.setup()
        self.ee.emit(PerfEvents.PERF_RUN_STARTED)
        result_queue = Queue()

        for i, sim in enumerate(self.simulations):
            if i>0:
                await self.formatters.update_formatters(i)
            #print("start: " + datetime.now().strftime("%c"))
            self.scheduled_runtime = sim["veggie"].get("time", None)
            self.ramp_up = sim["veggie"].get("ramp_up", None)
            self.ramp_down = sim["veggie"].get("ramp_down", None)
            rw = sim["veggie"].get("random_wait", 0)
            self.random_wait = self.__get_time(rw if rw is not None else "00:00:00").total_seconds()/1000
            sim_result = Result(sim['veggie']['name'],datetime.now())
            self.ee.emit(PerfEvents.SIMULATION_RUN_STARTED,sim["veggie"]["name"],sim_result.start)

            if not self.config.perf_dry_run:
                for group in sim['veggie']['groups']:
                    g = dict(group)
                    if g['percentage']:
                        precent = float(g['percentage'])
                        precent = precent if precent < 1 else precent/100
                        g['runners']=int((int(sim['veggie']['total_runners']) if sim['veggie']['total_runners'] else 10)* precent)
                        if sim['veggie']['total_count']:
                            g['count']=int((int(sim['veggie']['total_count']) if sim['veggie']['total_count'] else 10)* precent)
                    g['running'] = 0
                    g['ran'] = 0
                    g['max_runners'] = g['runners']
                    self.groups[g['id']] = g
                    self.max_runners = self.cur_max_runners+int(g['runners'])
                    self.cur_max_runners = self.max_runners
                    # TODO should this be set at all if in period
                    self.max_ran = self.max_ran + \
                        int(g['count'] if g['count']
                            is not None else g['runners'])

                self.executing = True
                listening = True
                cur_time = datetime.now()
                if self.scheduled_runtime is not None:
                    self.begin_end = self.__get_end(
                        cur_time, self.scheduled_runtime)
                if self.ramp_up is not None:
                    self.ee.emit(PerfEvents.RAMP_STARTED,"up")
                    self.cur_percent = 0
                    self.end_ramp = self.__get_end(cur_time, self.ramp_up)
                    ramp_period = self.__get_ramp_period(
                        (self.end_ramp - cur_time), self.max_ramp_periods)
                    await self.__set_cur_group_threads(0)
                    self.ramper = await set_interval_async(ramp_period, self.__ramp)

                cnt_per_proc = self.__calculate_processes_threads(self.max_runners)
                # Queue max size is 0 or infinate not sure if blocking on put matters or not in this case
                # multiple queues for the sake of even distribution
                self.task_queues = [Queue() for _ in range(len(cnt_per_proc))]
                for i in range(len(cnt_per_proc)):
                    p = Process(target=manager, args=[
                                i, cnt_per_proc[i], self.task_queues[i], result_queue, self.config.behave_args])
                    # (Avaliable Threads, Max Threads, Process)
                    self.processes.append([cnt_per_proc[i], cnt_per_proc[i], p])
                    p.start()
                    
                await self.__manage_run()

                # Loop to monitor results
                while listening:
                    if not result_queue.empty():
                        try:
                            p_id, result = result_queue.get_nowait()
                            self.ran += 1
                            self.running -= 1
                            self.processes[p_id][0] += 1
                            self.groups[result.id]["running"] -= 1
                            self.groups[result.id]["ran"] += 1
                            event = dict(self.groups[result.id])
                            event['result']=result
                            self.ee.emit(
                                PerfEvents.CUKE_RUN_FINISHED, event)
                            sim_result.add_group_result(result)
                        except Exception as e:
                            print(e)
                            pass
                    await asyncio.sleep(0.01)
                    if not self.executing:
                        if self.running == 0:
                            listening = False

                # Will need to wait for closing
                for p in self.processes:
                    if not self.task_queues[i].empty():
                        await asyncio.sleep(0.1)

            sim_result.stop = datetime.now()
            sim_result.duration = sim_result.stop-sim_result.start
            self.results.append(sim_result)

            self.ee.emit(PerfEvents.SIMULATION_RUN_FINISHED,sim_result)
            #Sleep for formatters
            await asyncio.sleep(1)
            await self.__cleanup()

        self.ee.emit(PerfEvents.PERF_RUN_FINISHED,self.results)
        #Wait for formatters to complete before closing stream
        while self.formatters_running:
            await asyncio.sleep(0.1)
        await asyncio.sleep(1)
        #Close streams
        await self.formatters.close_streams()
        return True

    async def __cleanup(self):
        for queue in self.task_queues:
            queue.close()
        for process in self.processes:
            process[2].terminate()
            process[2].join()
        self.__set_defaults()

    async def __manage_run(self):
        cur_time = datetime.now()
        if self.executing:
            if self.end_ramp is None:
                # check if time is up
                if (self.begin_end is not None and cur_time > self.begin_end) or (self.ran >= self.max_ran and self.begin_end is None):
                    if self.ramp_down is None:
                        self.executing = False
                        return
                    else:
                        self.ee.emit(PerfEvents.RAMP_STARTED, "down")
                        self.end_ramp = self.__get_end(
                            cur_time, self.ramp_down)
                        ramp_period = self.__get_ramp_period(
                            (self.end_ramp - cur_time), self.max_ramp_periods)
                        self.ramper = await set_interval_async(ramp_period, self.__ramp)

            # are all runners runningramp_up
            if self.running < self.cur_max_runners and (self.scheduled_runtime is not None or await self.__has_groups_to_run()):
                pi = 0
                for i in range(self.cur_max_runners-self.running):
                    # Want to randomize which process we start with.
                    # This should stop one process from getting all the jobs
                    loc = random.randint(1, 99999999)
                    for l in range(len(self.processes)):
                        p = (loc + l) % len(self.processes)
                        if self.processes[p][0] > 0:
                            pi += 1
                            await self.__manage_process(p)
                            break
                #print('after manage runners: mp_ran: ' + str(pi) + ' running: ' + str(self.running))
        else:
            for i in range(len(self.processes)):
                self.task_queues[i].put(RUNNER_TASKS.STOP_ALL.create())

    async def __manage_process(self, p_id: int):
        # Running more threads then needed.
        if self.running > self.cur_max_runners:
            if await self.__should_ramp(p_id):
                self.task_queues[p_id].put(RUNNER_TASKS.RAMP.create(-1))
                self.processes[p_id][0] -= 1
                self.processes[p_id][1] -= 1
            return

        loc = random.randint(1, 99999999)
        gs = list(self.groups.values())
        for l in range(len(gs)):
            g_id = (loc + l) % len(gs)
            pg = gs[g_id]
            if pg["running"] < int(pg["runners"]) and (self.scheduled_runtime is not None or pg["ran"] + pg["running"] < int(pg["count"])):
                pg["running"] += 1
                self.running += 1
                self.processes[p_id][0] -= 1
                self.ee.emit(PerfEvents.CUKE_RUN_STARTED, dict(pg))
                self.task_queues[p_id].put(RUNNER_TASKS.RUN.create(dict(pg)))
                return

    async def __listener_cuke_finished(self, data):
        if self.executing:
            await self.__manage_run()

    async def __listener_formatter_started(self, data):
        self.formatters_running.append(data)

    async def __listener_formatter_finished(self, data):
        self.formatters_running.remove(data)

    def __calculate_processes_threads(self, runners_max: int) -> [int]:
        procs_count = cpu_count()
        if runners_max < procs_count:
            procs_count = runners_max

        threads_pp = math.ceil(runners_max / procs_count)
        procs = []
        diff = (threads_pp*procs_count)-runners_max
        for _ in range(procs_count):
            procs.append(threads_pp)
        for i in range(diff):
            procs[i % procs_count] -= 1
        return procs

    async def __should_ramp(self, p_id: int):
        """Find out if the process should reduce or increase its thread count.
            Check if its has the lowest or highest number avaiable based on ramp direction.

        Args:
            p_id (int): _description_

        Returns:
            _type_: _description_
        """
        maxs = [y for x, y in self.processes]
        if self.ramp_up:
            if self.processes[p_id][1] == min(maxs):
                return True
        elif self.ramp_down:
            if self.processes[p_id][1] == max(maxs):
                return True
        return False

    async def __ramp(self):
        cur_time = datetime.now()
        if self.end_ramp is not None:
            if cur_time > self.end_ramp:
                self.end_ramp = None
                if self.ramp_up is None:
                    self.ee.emit(PerfEvents.RAMP_FINISHED,"down")
                    self.ramp_down = None
                    self.executing = False
                    self.cur_percent = 0
                else:
                    self.ee.emit(PerfEvents.RAMP_FINISHED,"up")
                    self.ramp_up = None
                    self.cur_percent = 100
                self.ramper.cancel()
                await self.__set_cur_group_threads(self.cur_percent)
            else:
                if self.ramp_up is None:
                    self.cur_percent -= 100 / self.max_ramp_periods
                    self.ee.emit(PerfEvents.RAMP_PRECENT,str(self.cur_percent))
                else:
                    self.cur_percent += 100 / self.max_ramp_periods
                    self.ee.emit(PerfEvents.RAMP_PRECENT,str(self.cur_percent))
                await self.__set_cur_group_threads(self.cur_percent)
            await self.__manage_run()

    async def __set_cur_group_threads(self, percent):
        per = 1
        if percent < 100:
            if percent > 0:
                per = percent / 100
            else:
                per = 0
        mrs = 0
        for group in self.groups.values():
            group["runners"] = round(int(group["max_runners"]) * per)
            mrs = mrs + int(group["runners"])
        self.cur_max_runners = mrs

    async def __has_groups_to_run(self):
        for group in self.groups.values():
            if int(group["ran"]) < int(group["count"]):
                return True
        return False

    # TODO: Handle more formats
    def __get_time(self,time: str)->timedelta:
        t = datetime.strptime(time, "%H:%M:%S")
        delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        return delta

    def __get_end(self, start: datetime, time: str)->timedelta:
        delta = self.__get_time(time)
        m = start + delta
        return m

    def __get_ramp_period(self, time: timedelta, times: int):
        # total time in seconds/times
        return time.total_seconds() / times
