from salad.stream.source_events import SourceEvents
from salad.stream.salad_events import SaladEvents
import math
import random

def get_simulations_from_filesystem(event_broadcaster, language, plan_paths, order, veggie_filter):
    result = []
    for plan_path in plan_paths:
        source_events = SourceEvents([plan_path])        
        for source_event in source_events.enum():
            result.extend(get_simulations(event_broadcaster,language,veggie_filter,source_event))
    order_simulations(result, order)
    return result


def get_simulations(event_broadcaster, language, veggie_filter, source_event):
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
                event_broadcaster.emit(
                    'veggie-accepted', {'veggie': veggie, 'uri': uri})
                result.append({'veggie': veggie, 'uri': uri})
            else:
                event_broadcaster.emit(
                    'veggie-rejected', {'veggie': veggie, 'uri': uri})
        elif event['type'] == 'attachment':
            raise Exception(f'Parse error in \'{uri}\': {event.data}')
    return result

def validate_simulation(simulation:dict):
    """There is one case where a simulation might be gramaticaly correct but not have needed fields

    Args:
        simulation (dict): _description_

    Returns:
        _type_: _description_
    """
    message = ''
    valid = False
    has_total_count ='totalCount' in simulation['veggie']
    has_total_runners ='totalRunners' in simulation['veggie']
    has_prc = False
    for group in simulation['veggie']['groups']:
        if 'precentage' in group:
            has_prc = True
            if not has_total_runners:
                message = 'No total runners set for group with precentage of runners.'
                break
    if valid and has_total_runners and not has_prc:
        message = 'Total runners set for simulation without any precentage groups. The total will be ignored.'
    if (valid and has_total_count and not has_prc):
        message = 'Total count set for simulation without any precentage groups. The total will be ignored.'
    return (valid,message)


def order_simulations(simulations, order):
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
        random.shuffle(simulations, seed)
    else:
        raise Exception('Unrecognized order type. Should be `defined` or `random`')
