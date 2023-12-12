from behave_performance.salad.stream.source_events import SourceEvents
from behave_performance.salad.stream.salad_events import SaladEvents
from behave_performance.veggie_filter import VeggieFilter
import math
import random

def get_simulations_from_filesystem(event_broadcaster, language:str, plan_paths:[str], order:str, veggie_filter:VeggieFilter)-> list:
    """Get simulations from the file system.

    Args:
        event_broadcaster (AsyncIOEventEmitter): The event broadcaster to use.
        language (str): The language code of the langauge to read the simulations in.
        plan_paths ([str]): All plan paths.
        order (str): The order to use for simulations.
        veggie_filter (VeggieFilter): The veggie filter to use to filter out simulations.

    Returns:
        _type_: _description_
    """
    result = []
    for plan_path in plan_paths:
        source_events = SourceEvents([plan_path])        
        for source_event in source_events.enum():
            result.extend(get_simulations(event_broadcaster,language,veggie_filter,source_event))
    order_simulations(result, order)
    return result


def get_simulations(event_broadcaster, language:str, veggie_filter:VeggieFilter, source_event:dict) -> list:
    """Get simulations from the source events. Broadcasts messages related to source events.

    Args:
        event_broadcaster (AsyncIOEventEmitter): The event broadcaster to use.
        language (str): The language code of the langauge to read the simulations in.
        veggie_filter (VeggieFilter): The veggie filter to use to filter out simulations.
        source_event (dict): A source event to process.

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    result = []
    uri = source_event['source']['uri']
    salad_events = SaladEvents(language)
    for event in salad_events.enum(source_event):
        if 'error' in event['type']:
            print(event)
        event_broadcaster.emit(
            event['type'], {k: v for k, v in event.items() if k != 'type'})
        if event['type'] == 'veggie':
            veggie = event['veggie']
            if veggie_filter.matches(veggie, uri):
                event_broadcaster.emit('veggie-accepted', {'veggie': veggie, 'uri': uri})
                result.append({'veggie': veggie, 'uri': uri})
            else:
                event_broadcaster.emit(
                    'veggie-rejected', {'veggie': veggie, 'uri': uri})
        elif event['type'] == 'attachment':
            raise Exception(f'Parse error in \'{uri}\': {event.data}')
    return result

def validate_simulation(veggie:dict)-> tuple[bool, dict]:
    """There is one case where a simulation might be gramaticaly correct but not have needed fields

    Args:
        simulation (dict): The salad dict

    Returns:
        (bool,dict): If there is an issue with the simulation and what it is.
    """
    messages = []
    is_valid= True
    has_total_count = veggie['total_count'] != None
    has_total_runners = veggie['total_runners'] != None
    has_prc = False
    for group in veggie['groups']:
        if group['runners']:
            pass
        elif group['percentage']:
            has_prc = True
            if not has_total_runners:
                messages.append('No total runners set for group with precentage of runners. The total will be set to 10.')
                break
        else:
            messages.append(f'Runners or precentage is not set for group. This simulation {veggie["name"]} will not be run!')
            is_valid=False
    if has_total_runners and not has_prc:
        messages.append('Total runners set for veggie without any precentage groups. The total will be ignored.')
    if has_total_count and not has_prc:
        messages.append('Total count set for simulation without any precentage groups. The total will be ignored.')
    if messages:
        messages = { veggie['name']+' issues': messages}
    return (is_valid,messages)


def order_simulations(simulations:[dict], order:str):
    """Orders simulations in random order with seeds or leaves it alone.

    Args:
        simulations ([dict]): A list of simulations
        order (str): A type of order. Options are "defined" or "random". For random you can provide a seed using the format "random:200".

    Raises:
        Exception: Bad type was provided
    """
    if ':' in order:
        type, seed = order.split(':')
    else:
        type = order
        seed = None
    if type == 'defined':
        pass
    elif type == 'random':
        if seed is None:
            seed = str(math.floor(math.random() * 1000 * 1000))
            print(f'Random order using seed: {seed}')
        random.shuffle(simulations, float(seed))
    else:
        raise Exception('Unrecognized order type. Should be `defined` or `random`')
