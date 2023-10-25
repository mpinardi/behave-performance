from .ast_node import AstNode
from .errors import AstBuilderException
from .stream.id_generator import IdGenerator

class AstBuilder(object):
    def __init__(self, id_generator=None):
        self.id_generator = id_generator
        if self.id_generator is None:
            self.id_generator = IdGenerator()
        self.reset()

    def reset(self):
        self.stack = [AstNode('None')]
        self.comments = []
        self.id_counter = 0

    def start_rule(self, rule_type):
        self.stack.append(AstNode(rule_type))

    def end_rule(self, rule_type):
        node = self.stack.pop()
        self.current_node.add(node.rule_type, self.transform_node(node))

    def build(self, token):
        if token.matched_type == 'Comment':
            self.comments.append({
                'location': self.get_location(token),
                'text': token.matched_text
            })
        else:
            self.current_node.add(token.matched_type, token)

    def get_result(self):
        return self.current_node.get_single('SaladDocument')

    @property
    def current_node(self):
        return self.stack[-1]

    def get_location(self, token, column=None):
        return (token.location if not column else
                {'line': token.location['line'], 'column': column})

    def get_tags(self, node):
        tags = []
        tags_node = node.get_single('Tags')
        if not tags_node:
            return tags

        for token in tags_node.get_tokens('TagLine'):
            tags += [{'id': self.id_generator.get_next_id(),
                      'location': self.get_location(token, tag_item['column']),
                      'name': tag_item['text']} for tag_item in token.matched_items]

        return tags

    def get_table_rows(self, node):
        rows = [{'id': self.id_generator.get_next_id(),
                 'location': self.get_location(token),
                 'cells': self.get_cells(token)} for token in node.get_tokens('TableRow')]
        self.ensure_cell_count(rows)
        return rows

    def ensure_cell_count(self, rows):
        if not rows:
            return

        cell_count = len(rows[0]['cells'])
        for row in rows:
            if len(row['cells']) != cell_count:
                raise AstBuilderException("inconsistent cell count within the table",
                                          row['location'])

    def get_cells(self, table_row_token):
        return [self.reject_nones(
            {'location': self.get_location(table_row_token, cell_item['column']),
             'value': cell_item['text']}) for cell_item in table_row_token.matched_items]

    def get_value_or_none(self, token, node):
        n = node.get_single(token)
        return n if n is None else n.get_single(token+'Line').matched_text

    def get_start(self, node):
        n =  node.get_token('StartLine')
        return n if n is None else n.matched_text

    def get_stop(self, node):
        n =  node.get_token('StopLine')
        return n if n is None else n.matched_text

    def get_description(self, node):
        return node.get_single('Description', '')

    def get_sim_groups(self, node):
        return node.get_items('Group')
    
    def get_sim_populations(self, node):
        return node.get_items('Population')
    
    def get_sim_types(self, node):
        return node.get_items('Type')

    def transform_node(self, node):
        if node.rule_type == 'Group':
            group_line = node.get_token('GroupLine')
            group_argument_type = 'dummy_type'
            group_argument = None
            if node.get_single('DataTable'):
                group_argument_type = 'dataTable'
                group_argument = node.get_single('DataTable')
            elif node.get_single('DocString'):
                group_argument_type = 'docString'
                group_argument = node.get_single('DocString')


            return self.reject_nones({
                'id': self.id_generator.get_next_id(),
                'location': self.get_location(group_line),
                'keyword': group_line.matched_keyword,
                'keywordType': group_line.matched_keyword_type,
                'text': group_line.matched_text,
                'runners': self. get_value_or_none("Runners",node),
                'count': self. get_value_or_none("Count",node),
                'percentage': self. get_value_or_none("Percentage",node),
                'start': self.get_value_or_none('Start',node),
                'stop':self.get_value_or_none('Stop',node),
                'synchronized': self.get_value_or_none('Synchronized',node),
                group_argument_type: group_argument
            })
        elif node.rule_type == 'Type':
            type_line = node.get_token('GroupTypeLine')
            type_argument_type = 'dummy_type'
            type_argument = None
            if node.get_single('DataTable'):
                type_argument_type = 'dataTable'
                type_argument = node.get_single('DataTable')
            elif node.get_single('DocString'):
                type_argument_type = 'docString'
                type_argument = node.get_single('DocString')

            return self.reject_nones({
                'id': self.id_generator.get_next_id(),
                'location': self.get_location(type_line),
                'keyword': type_line.matched_keyword,
                'keywordType': type_line.matched_keyword_type,
                'text': type_line.matched_text,
                'features': self. get_value_or_none("Features",node),
                type_argument_type: type_argument
            })
        elif node.rule_type == 'DocString':
            separator_token = node.get_tokens('DocStringSeparator')[0]
            media_type = (separator_token.matched_text if len(separator_token.matched_text) > 0
                            else None)
            line_tokens = node.get_tokens('Other')
            content = '\n'.join([t.matched_text for t in line_tokens])

            return self.reject_nones({
                'location': self.get_location(separator_token),
                'content': content,
                'delimiter': separator_token.matched_keyword,
                'mediaType': media_type
            })
        elif node.rule_type == 'DataTable':
            rows = self.get_table_rows(node)
            return self.reject_nones({
                'location': rows[0]['location'],
                'rows': rows,
            })
        elif node.rule_type == 'Simulation_Definition':
            tags = self.get_tags(node)
            simulation_node = node.get_single('Simulation')
            if simulation_node is not None:
                simulation_line = simulation_node.get_token('SimulationLine')
            elif node.get_single('SimulationPeriod') is not None:
                simulation_node = node.get_single('SimulationPeriod')
                simulation_line = simulation_node.get_token('SimulationPeriodLine')

            description = self.get_description(simulation_node)
            groups = self.get_sim_groups(simulation_node)
            if not groups:
                groups = self.get_sim_populations(simulation_node)

            return self.reject_nones({
                'id': self.id_generator.get_next_id(),
                'tags': tags,
                'location': self.get_location(simulation_line),
                'keyword': simulation_line.matched_keyword,
                'keywordType': simulation_line.matched_keyword_type,
                'name': simulation_line.matched_text,
                'rampUp': self. get_value_or_none("RampUp",simulation_node),
                'rampDown': self. get_value_or_none("RampDown",simulation_node),
                'randomWait': self. get_value_or_none("RandomWait",simulation_node),
                'time': self. get_value_or_none("Time",simulation_node),
                'totalCount': self. get_value_or_none("TotalCount",simulation_node),
                'totalRunners': self. get_value_or_none("TotalRunners",simulation_node),
                'synchronization': self. get_value_or_none("synchronization",simulation_node),
                'description': description,
                'groups': groups,
            })
        elif node.rule_type == 'Groups':
            groups_line = node.get_token('GroupsLine')
            description = self.get_description(node)
            types = self.get_sim_types(node)
            return self.reject_nones({
                'id': self.id_generator.get_next_id(),
                'location': self.get_location(groups_line),
                'keyword': groups_line.matched_keyword,
                'keywordType': groups_line.matched_keyword_type,
                'name': groups_line.matched_text,
                'description': description,
                'types': types,
            })
        elif node.rule_type == 'Description':
            line_tokens = node.get_tokens('Other')
            # Trim trailing empty lines
            last_non_empty = next(i for i, j in reversed(list(enumerate(line_tokens)))
                                  if j.matched_text)
            description = '\n'.join([token.matched_text for token in
                                     line_tokens[:last_non_empty + 1]])

            return description
      
        elif node.rule_type == 'Plan':
            header = node.get_single('Plan_Header')
            if not header:
                return

            tags = self.get_tags(header)
            plan_line = header.get_token('PlanLine')
            if not plan_line:
                return

            children = []
            children = children + [{'simulation': i} for i in node.get_items('Simulation_Definition')]
            children = children + [{'groups': i} for i in node.get_items('Groups')]
            description = self.get_description(header)
            language = plan_line.matched_salad_dialect

            return self.reject_nones({
                'tags': tags,
                'location': self.get_location(plan_line),
                'language': language,
                'keyword': plan_line.matched_keyword,
                'name': plan_line.matched_text,
                'description': description,
                'children': children
            })
        elif node.rule_type == 'SaladDocument':
            plan = node.get_single('Plan')

            return self.reject_nones({
                'plan': plan,
                'comments': self.comments
            })
        else:
            return node

    def reject_nones(self, values):
        return {k: v for k, v in values.items() if v is not None}
