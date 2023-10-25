
class Simulation():

    def __init__(self,ast_node_ids:list,id:str,tags:list,location:dict,keyword:str,keyword_type:str,name:str,time:str=None,total_count:str=None,total_runners:str=None,ramp_up:str=None,ramp_down:str=None,random_wait:str=None,synchronization:str=None,groups:list=[],description:str=None,uri=None):
        self._ast_node_ids = ast_node_ids
        self.id = id
        self.location = location
        self.tags = tags
        self.keyword = keyword
        self.keyword_type = keyword_type
        self.name = name
        self.time = time
        self.total_count = total_count
        self.total_runners = total_runners
        self.ramp_up = ramp_up
        self.ramp_down = ramp_down
        self.random_wait = random_wait
        self.synchronization = synchronization
        self.groups = []
        for group in groups:
            self.groups.append(Group(**group))
        self.description = description
        self.uri = uri


class Group():
   
    def __init__(self,ast_node_ids:list,id:str,text:str,runners:str=None,precentage:str=None,count:str=None,start:str=None,stop:str=None,synchronized:str=None,argument:str=None):
        self._ast_node_ids = ast_node_ids
        self.id = id
        self.text = text
        self.runners = runners
        self.precentage = precentage
        self.count = count
        self.start = start
        self.stop = stop
        self.synchronized = synchronized
        self.argument = argument
   