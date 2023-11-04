import re

from behave_performance.salad.stream.id_generator import IdGenerator


class Compiler(object):
    def __init__(self, id_generator=None):
        self.id_generator = id_generator
        if self.id_generator is None:
            self.id_generator = IdGenerator()

    def compile(self, salad_document):
        veggies = []
        veggie_groups = []
        if 'plan' not in salad_document:
            return veggies

        plan = salad_document['plan']
        if not plan['children']:
            return veggies

        uri = salad_document['uri']
        plan_tags = plan['tags']
        language = plan['language']
        for child in plan['children']:
            if 'simulation' in child:
                sim = child['simulation']
                args = (uri, plan_tags, sim, language, veggies)
                self._compile_simulation(*args)
            else:
                groups = child['groups']
                args = (uri, groups, language, veggie_groups)
                self._compile_groups(*args)
        self._apply_groups(veggies,veggie_groups)
        return veggies

    def _compile_simulation(self, uri, inherited_tags, simulation, language, veggies):
        tags = list(inherited_tags) + list(simulation['tags'])
        groups = list()
        if simulation['groups']:
            for group in simulation['groups']:
                groups.append(self._veggie_group(group))
        
        veggie = {
            'ast_node_ids': [simulation['id']],
            'location': simulation['location'],
            'id': self.id_generator.get_next_id(),
            'tags': self._veggie_tags(tags),
            'name': simulation['name'],
            'language': language,
            'time': self.get_value_or_none('time',simulation),
            'total_count': self.get_value_or_none('totalCount',simulation),
            'total_runners': self.get_value_or_none('totalRunners',simulation),
            'ramp_up': self.get_value_or_none('rampUp',simulation),
            'ramp_down': self.get_value_or_none('rampDown',simulation),
            'random_wait': self.get_value_or_none('randomWait',simulation),
            'synchronization': self.get_value_or_none('synchronization',simulation),
            'groups': groups,
            'uri': uri
        }
        veggies.append(veggie)

    def _compile_groups(self, uri, groups, language, veggies):
        types = list()
        if groups['types']:
            for type in groups['types']:
                types.append(self._veggie_type(type))

        veggie = {
            'ast_node_ids': [groups['id']],
            'location': groups['location'],
            'id': self.id_generator.get_next_id(),
            'name': groups['name'],
            'language': language,
            'types': types,
            'uri': uri
        }
        veggies.append(veggie)
    
    def _apply_groups(self, veggies:list[dict], veggie_groups:list[dict]):
        """Applys veggie_groups to veggies replacing any group text that is a reference.

        Args:
            veggies (list[dict]): The veggies in the plan
            veggie_groups (list[dict]): The veggie_groups in the plan.
        """
        types = {}
        if veggie_groups:
            for groups in veggie_groups:
                for type in groups['types']:
                    types[type['text']]=type['features']
            for veggie in veggies:
                for group in veggie['groups']:
                    if group['text'] in types:
                        group['text'] = types[group['text']]
                        #group['text'] = group['text']+'('+types[group['text']]+')'
         

    def _create_veggie_arguments(self, group, variables, values):
        if 'dataTable' in group:
            table = {'rows': []}
            for row in group['dataTable']['rows']:
                cells = [
                    {
                        'value': self._interpolate(cell['value'], variables, values)
                    } for cell in row['cells']
                ]
                table['rows'].append({'cells': cells})
            return {'data_table': table}

        elif 'docString' in group:
            argument = group['docString']
            docstring = {
                'content': self._interpolate(argument['content'], variables, values)
            }
            if 'mediaType' in argument:
                docstring['mediaType'] = self._interpolate(argument['mediaType'], variables, values)
            return {'doc_string': docstring}
        else:
            return None

    def _interpolate(self, name, variable_cells, value_cells):
        if name is None:
            return name

        for n, variable_cell in enumerate(variable_cells):
            value_cell = value_cells[n]
            # For the case of trailing backslash, re-escaping backslashes are needed
            reescaped_value = re.sub(r'\\', r'\\\\', value_cell['value'])
            name = re.sub(
                u'<{0[value]}>'.format(variable_cell),
                reescaped_value,
                name
            )
        return name

    def _veggie_group(self, group):
        veggie_group = {
            'ast_node_ids': [group['id']],
            'location': group['location'],
            'id': self.id_generator.get_next_id(),
            'text': group['text'],
            'runners': self.get_value_or_none('runners',group),
            'percentage': self.get_value_or_none('percentage',group),
            'count': self.get_value_or_none('count',group),
            'start': self.get_value_or_none('start',group),
            'stop': self.get_value_or_none('stop',group),
            'synchronized': self.get_value_or_none('synchronized',group)
        }
        argument = self._create_veggie_arguments(
            group,
            [],
            [])
        if argument is not None:
            veggie_group['argument'] = argument
        return veggie_group

    def _veggie_type(self, type):
        veggie_type = {
            'ast_node_ids': [type['id']],
            'location': type['location'],
            'id': self.id_generator.get_next_id(),
            'text': type['text'],
            'features': self.get_value_or_none('features',type)
        }
        argument = self._create_veggie_arguments(
            type,
            [],
            [])
        if argument is not None:
            veggie_type['argument'] = argument
        return veggie_type

    def _veggie_tags(self, tags):
        return [self._veggie_tag(tag) for tag in tags]

    def _veggie_tag(self, tag):
        return {
            'ast_node_id': tag['id'],
            'name': tag['name']
        }
    
    def get_value_or_none(self, value, node):
        return node[value] if value in node else None

    def reject_nones(self, values):
        return {k: v for k, v in values.items() if v is not None}
