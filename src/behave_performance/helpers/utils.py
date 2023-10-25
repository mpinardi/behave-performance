
"""testharness.utils

Utils for general python testing.
"""
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Imports
# region
import csv
import datetime
import json
import os
import random
import string
import threading
import xml.etree.ElementTree as ET
import asyncio
from copy import copy

# endregion


# ---------------------------------------------------------------------------
# Threading
# ------------------------------------------------------------------------------
# region


async def set_interval_async(interval:float, func, *args):
    async def _run():
        while True:
            await asyncio.sleep(interval)
            await func(*args)
    task = asyncio.ensure_future(_run())
    return task



async def set_interval_deamon_async(interval:float, func, *args):
    """ A threaded python implimentation of node js's setInterval
        Will perform an action every "interval" seconds.
        Example:
        cancel_future_calls = set_interval(60, print, "Hello, World")
        cancel_future_calls() # will stop the execution

    Args:
        interval (float): The interval in seconds
        func (*): The function to execute

    Returns:
        Event: The threading event to allow for canceling.
    """
    stopped = threading.Event()
    async def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            await func(*args)
    
    def between():
        l = asyncio.new_event_loop()
        asyncio.set_event_loop(l)
        l.run_until_complete(loop())
        l.close()

    threading.Thread(target=between,daemon=True).start()    
    return stopped.set

def set_interval_deamon(interval:float, func, *args):
    """ A threaded python implimentation of node js's setInterval
        Will perform an action every "interval" seconds.
        Example:
        cancel_future_calls = set_interval(60, print, "Hello, World")
        cancel_future_calls() # will stop the execution

    Args:
        interval (float): The interval in seconds
        func (*): The function to execute

    Returns:
        Event: The threading event to allow for canceling.
    """
    stopped = threading.Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    threading.Thread(target=loop,daemon=True).start()    
    return stopped.set

thread_local = threading.local()
lock = threading.Lock()


def is_local_first(name: str) -> bool:
    """Has the name been set as a attribute to the thread_local object.
        If it hasn't it will add it and return True. Otherwise returns False.

    Args:
        name (str): The name of the attribute.

    Returns:
        bool : True if attribute was not already assigned to thread local. Otherwise false.
    """
    initialized = getattr(thread_local, name, None)
    if initialized is None:
        setattr(thread_local, name, True)
        return True
    return False
    
def get_local(name: str, default_to = None):
    """Get a attribute set to the thread_local object.
        Each thread only has access to its own local object.

    Args:
        name (str): The name of the attribute.
        default_to (optional): The default response if the attribute doesn't exist.

    Returns:
        Obj : The attribute of the thread local obj.
    """
    return getattr(thread_local, name, default_to)

def set_local(name: str, value:object):
    """Set a attribute to the thread_local object.
    Each thread only has access to its own local object.

    Args:
        name (str): The name of the attribute.
        value (object): The value to set to attribute to.
    """
    setattr(thread_local, name, value)

def del_local(name: str):
    """Delete a attribute from the thread_local object.
    Each thread only has access to its own local object.

    Args:
        name (str): The name of the attribute.
    """
    delattr(thread_local, name)  
    
class _singleton(type):
    """ A metaclass for singleton classes

    Args:
        type (_self): The class to use.

    Returns:
       _self : An existing version of the class.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(
                        _singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# endregion

# ---------------------------------------------------------------------------
# file utils
# ------------------------------------------------------------------------------
# region
def delete_file(path):
    """Delete a file

    :param path: file path
    :return: True if success otherwise false
    """
    if os.path.isfile(path):
        try:
           os.remove(path)
        except IOError as e:
            raise Exception("File", e)
        return True
    return False

def load_string(path):
    """Load string contents of file from path

    :param path: file path
    :return: String value of the file.
    """
    if os.path.isfile(path):
        try:
            with open(path) as f:
                return f.read()
        except IOError as e:
            raise Exception("File", e)
    return None

def load_csv(path):
    """Load CSV file. Detects delimiter automatically

    :param path: file path
    :return: list
    """
    if os.path.isfile(path):
        with open(path, "rb") as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=";,")
            csvfile.seek(0)
            reader = csv.DictReader(csvfile, dialect=dialect)
            return [row for row in reader]
    return None

def get_csv(value):
    """Convert a CSV string to list or load a CSV file.

    :param value: file path or a string csv.
    :return: list
    """
    if isinstance(value, str):
        obj = load_csv(value)
        if obj == None:
            try:
                return [row for row in csv.reader([value])]
            except Exception:
                return None
        return obj
    return value


def load_json(path):
    """Load JSON file from path

    :param path: file path
    :return: dict
    """
    if os.path.isfile(path):
        try:
            with open(path) as f:
                return json.load(f)
        except IOError as e:
            raise Exception("File", e)
    return None

def get_json(value):
    """Convert a string to JSON object or load a JSON file.

    :param value: file path or a string json.
    :return: dict
    """
    if isinstance(value, str):
        jsn = load_json(value)
        if jsn == None:
            try:
                #convert if dict
                value = value.replace("'", '"').replace("True", '"True"').replace("False", '"False"').replace("null", '"null"')
                jsn = json.loads(value)
            except Exception:
                return None
        return jsn
    return value

def search_type(path:str, fileType:str)->str:
    """Combine a filetype to a path for a search string.

    Args:
        path ([str]): The path to use.
        fileType ([str]): The file type to search for.

    Returns:
        str: A string of the resulting path.
    """
    if os.path.isdir(path):
        if path.endswith(os.sep):
            return path + "*" + fileType
        else:
            return path + os.sep + "*"+fileType
    return path


def fpath(path:str, filename:str):
    """Updates a path with a filename. Handles os seperators.

    Args:
        path (str): The base path to use.
        filename (str): The filename to add.

    Returns:
        str: The resulting file path.
    """
    if os.path.isdir(path):
        if path.endswith(os.sep):
            return path + filename
        else:
            return path + os.sep + filename
    return path


def path_here(file=__file__):
    """The path to where this is running.

    Args:
        file (str): The file path to use.

    Returns:
        str: The absolute path of this location.
    """
    return os.path.abspath(os.path.dirname(file))

def parent_here(file=__file__):
    """The path to parent of where this is running.

    Args:
        file (str): The file path to use.

    Returns:
        str: The absolute path of the parent of this location.
    """
    return os.path.abspath(os.path.join(os.path.dirname(file),os.pardir))

def get_linux_user_id()->str:
    """Gets the current users name from the OS.

    Returns:
        str: The user running this automation.
    """
    return os.environ.get('USER')
    
# endregion

# ---------------------------------------------------------------------------
# data utils
# ------------------------------------------------------------------------------
# region

def to_dict(value):
    """Converts a string into a dict.

    Args:
        value (str, obj): The value to convert

    Returns:
        dict: Returns the new dict or the passed in object if it was not a string.
    """
    if isinstance(value, str):
        json_str = value.replace("'", '"').replace("True", '"True"').replace("False", '"False"').replace("null", '"null"')
        try:
            return json.loads(json_str)
        except Exception:
            pass
    return value


def ordered(obj):
    """Order a dictionary or list in ascending order.

    Args:
        obj (dict, list): The dictionary or list to order.

    Returns:
        dict,list: The resulting ordered object.
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

def merge_dicts(*dict_args):
    """
    Given any number of dictionaries, shallow copy and merge into a new dict,
    precedence goes to key-value pairs in latter dictionaries.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result
    
def xml_to_dict(ele:ET.ElementTree,root=True):
    """Convert xml into a dict
       Example: input:<erik><a x='1'>v</a><a y='2'>w</a></erik>
                output:{'erik': {'a': [{'x': '1', '_text': 'v'}, {'y': '2', '_text': 'w'}]}}
       Taken from stackex and @Erik Aronesty

    Args:
        r (xml.etree.ElementTree): The xml element to convert
        root (bool, optional): Is this the root element. Defaults to True.

    Returns:
        dict: A dict representation of the xml.
    """
    if root:
        return {ele.tag : xml_to_dict(ele, False)}
    d=copy(ele.attrib)
    if ele.text:
        d["_text"]=ele.text
    for x in ele.findall("./*"):
        if x.tag not in d:
            d[x.tag]=[]
        d[x.tag].append(xml_to_dict(x,False))
    return d

def dict_to_xml(item:dict,tag=None):
    """Convert dict to xml
       Example: input:{'matt': '{'a': [{'x': '1', '_text': 'v'}, {'y': '2', '_text': 'w'}]}}
                output:<matt><a x='1'>v</a><a y='2'>w</a></matt>
    Args:
        item (dict): The xml element to convert
        tag (str, optional): The Name of the current tag. Defaults to None.

    Returns:
        ElementTree: A element tree xml representation
    """
    if not tag:
        k = list(item.keys())[0]
        return dict_to_xml(item[k],k)
    ele = ET.Element(tag)
    attr = {}
    text = None
    for k,v in item.items():
        if isinstance(v, dict):
            ele.append(dict_to_xml(v,k))
        elif isinstance(v,list):
            for r in v:
                ele.append(dict_to_xml(r,k))
        else:
            if k =="_text":
                text = v
            else:
                attr[k] = v
    ele.text =text
    ele.attrib = attr
    return ele
    

def next_alpha(s:chr)->chr:
    """Return the following alpha character.

    Args:
        s (chr): The next alpha character.

    Returns:
        chr: The next alpha character.
    """
    return chr((ord(s.upper())+1 - 65) % 26 + 65)
#endregion