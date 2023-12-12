import re
import os
import cucumber_tag_expressions as cte

PLAN_LINENUM_REGEXP = r'^(.*?)((?::[\d]+)+)?$'

class VeggieFilter:
    """filters out veggies (simulation dict) for the passed in tags, names and paths with line numbers.
    """
    def __init__(self, plan_paths:[str]=None, names:[str]=None, tag_expressions:[str]=None):
        """New Veggie Filter

        Args:
            plan_paths ([str], optional): The plan paths with line numbers for simulations (./example.feature:20) to search for. Defaults to None.
            names ([str], optional): The names to search for. Defaults to None.
            tag_expressions ([str], optional): The tag expressions to search for. Defaults to None.
        """
        self.plan_uri_to_lines_mapping = self.get_plan_uri_to_lines_mapping(
            plan_paths or [])
        self.names = names or []
        self.tag_expression_nodes = list(map(cte.parse,tag_expressions)) if tag_expressions else None

    def get_plan_uri_to_lines_mapping(self, plan_paths):
        """Generates a dict of uris to line numbers

        Args:
            plan_paths (_type_): Plan paths that include line numbers to simualtions

        Returns:
            dict: A mapping of files with line numbers of simulations
        """
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

    def matches(self, veggie:dict, uri:str) -> bool:
        """Matches the veggie to the existing configuration. This checks all possible options.

        Args:
            veggie (dict): The dictionary version of a simulation.
            uri (str): A URI for the veggie.

        Returns:
            _type_: _description_
        """
        return (
            self.matches_any_line(veggie, uri) and
            self.matches_any_name(veggie) and
            self.matches_all_tag_expressions(veggie)
        )

    def matches_any_line(self, veggie:dict, uri:str) -> bool:
        """Match if the veggie matches any line for the URI

        Args:
            veggie (dict): The dictionary version of a simulation.
            uri (str): A URI for the veggie.

        Returns:
            bool: Returns true if the veggie matches or if no configuration exists. Returns false if it doesn't match.
        """
        lines = self.plan_uri_to_lines_mapping.get(os.path.abspath(uri))
        if lines:
            return bool(set(lines) & set( [veggie['location']['line']]))
        return True

    def matches_any_name(self, veggie:dict) -> bool:
        """Matches the names against the veggie.

        Args:
            veggie (dict): The dictionary version of a simulation.

        Returns:
            bool: Returns true if veggie matches any name or if no names are configured. Otherwise it returns false.
        """
        if not self.names:
            return True
        return any(name in veggie['name'] for name in self.names)

    def matches_all_tag_expressions(self, veggie:dict) -> bool:
        """Matches all tag expressions against the veggie.

        Args:
            veggie (dict): The dictionary version of a simulation.

        Returns:
            bool: Returns trye if tag expression in veggie matches or if no tag expressions are configured. Otheriwse it returns False.
        """
        if not self.tag_expression_nodes:
            return True
        return all(node.evaluate([tag['name'] for tag in veggie['tags']]) for node in self.tag_expression_nodes)