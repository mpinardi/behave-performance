import re
import os
import cucumber_tag_expressions as cte

PLAN_LINENUM_REGEXP = r'^(.*?)((?::[\d]+)+)?$'

class VeggieFilter:
    def __init__(self, plan_paths=None, names=None, tag_expressions:[]=None):
        self.plan_uri_to_lines_mapping = self.get_plan_uri_to_lines_mapping(
            plan_paths or [])
        self.names = names or []
        self.tag_expression_nodes = list(map(cte.parse,tag_expressions)) if tag_expressions else None

    def get_plan_uri_to_lines_mapping(self, plan_paths):
        mapping = {}
        for plan_path in plan_paths:
            match = re.match(PLAN_LINENUM_REGEXP, plan_path)
            if match:
                uri = os.path.abspath(match.group(1))
                lines_expression = match.group(2)
                if lines_expression:
                    if uri not in mapping:
                        mapping[uri] = []
                    mapping[uri].extend([int(l) for l in lines_expression.split(':') if l])
        return mapping

    def matches(self, veggie, uri):
        return (
            self.matches_any_line(veggie, uri) and
            self.matches_any_name(veggie) and
            self.matches_all_tag_expressions(veggie)
        )

    def matches_any_line(self, veggie, uri):
        lines = self.plan_uri_to_lines_mapping.get(os.path.abspath(uri))
        if lines:
            return bool(set(lines) & set(l['line'] for l in veggie['locations']))
        return True

    def matches_any_name(self, veggie):
        if not self.names:
            return True
        return any(name in veggie['name'] for name in self.names)

    def matches_all_tag_expressions(self, veggie):
        if not self.tag_expression_nodes:
            return True
        return all(node.evaluate([tag['name'] for tag in veggie['tags']]) for node in self.tag_expression_nodes)