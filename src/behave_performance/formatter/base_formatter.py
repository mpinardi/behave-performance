import sys
import asyncio
from abc import ABC, abstractmethod
from behave_performance.formatter.color_fns import ColorFns
from behave_performance.helpers.paths import expand_paths
from pyee.asyncio import AsyncIOEventEmitter
from io import IOBase

class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

class Formatter(ABC):
    
    @classproperty
    def FAMILY(cls):
        return ''

    @classproperty
    def DEFAULT(cls):
        return False

    @classproperty
    def SINGLETON(cls):
        return False
    
    
    def __init__(self, options):
        self.color_fns:ColorFns = options.get('color_fns', None)
        self.cwd:str = options.get('cwd', None)
        self.event_broadcaster:AsyncIOEventEmitter = options.get('event_broadcaster', None)
        self.stream:IOBase = options.get('stream', None)
        self.strict:bool = options.get('strict', None)
        self.support_code_library = options.get('support_code_library', None)
        self.options = options.get('options', None)

    def update_log(self, stream):
        self.stream = stream

    def is_stdio(self):
        return self.stream.name == sys.stdout.name
    
    async def log(self,value):
        if self.stream:
            if self.is_stdio():
                self.stream.write(value)
            else:
                await self.log_file(value)
    
    async def log_file(self,value):
        try:
            await self.stream.write(value)
        except asyncio.CancelledError as err:
            pass
        await self.stream.flush()     
        