import re
from collections import defaultdict
from .dialect import Dialect
from .errors import NoSuchLanguageException

# Source: https://stackoverflow.com/a/8348914
try:
    import textwrap
    textwrap.indent
except AttributeError:  # undefined function (wasn't added until Python 3.3)
    def indent(text, amount, ch=' '):
        padding = amount * ch
        return ''.join(padding+line for line in text.splitlines(True))
else:
    def indent(text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)

class TokenMatcher(object):
    LANGUAGE_RE = re.compile(r"^\s*#\s*language\s*:\s*([a-zA-Z\-_]+)\s*$")

    def __init__(self, dialect_name='en'):
        self._default_dialect_name = dialect_name
        self._change_dialect(dialect_name)
        self.reset()

    def reset(self):
        if self.dialect_name != self._default_dialect_name:
            self._change_dialect(self._default_dialect_name)
        self._indent_to_remove = 0
        self._active_doc_string_separator = None

    def match_PlanLine(self, token):
        return self._match_title_line(token, 'PlanLine', self.dialect.plan_keywords)

    def match_SimulationLine(self, token):
        return self._match_title_line(token, 'SimulationLine', self.dialect.simulation_keywords,'Simulation')
    
    def match_SimulationPeriodLine(self, token):
        return self._match_title_line(token, 'SimulationPeriodLine', self.dialect.simulation_period_keywords,'SimulationPeriod')

    def match_TableRow(self, token):
        if not token.line.startswith('|'):
            return False
        # TODO: indent
        self._set_token_matched(token, 'TableRow', items=token.line.table_cells)
        return True

    def match_GroupLine(self, token):
        for keyword in (k for k in self.dialect.group_keywords if token.line.startswith(k)):
            title = token.line.get_rest_trimmed(len(keyword))
            self._set_token_matched(token, 'GroupLine', title, keyword,'Group')
            return True

        return False
    
    def match_RunnersLine(self, token):
        return self._match_title_line(token, 'RunnersLine', self.dialect.runners_keywords)

    def match_CountLine(self, token):
        return self._match_title_line(token, 'CountLine', self.dialect.count_keywords)

    def match_RandomWaitLine(self, token):
        return self._match_title_line(token, 'RandomWaitLine', self.dialect.random_wait_keywords)
    
    def match_RampUpLine(self, token):
        return self._match_title_line(token, 'RampUpLine', self.dialect.ramp_up_keywords)
    
    def match_RampDownLine(self, token):
        return self._match_title_line(token, 'RampDownLine', self.dialect.ramp_down_keywords)
    
    def match_StartLine(self, token):
        return self._match_title_line(token, 'StartLine', self.dialect.start_keywords)

    def match_StopLine(self, token):
        return self._match_title_line(token, 'StopLine', self.dialect.stop_keywords)
    
    def match_TimeLine(self, token):
        return self._match_title_line(token, 'TimeLine', self.dialect.time_keywords)
        
    def match_PopulationLine(self, token):
        for keyword in (k for k in self.dialect.population_keywords if token.line.startswith(k)):
            title = token.line.get_rest_trimmed(len(keyword))
            self._set_token_matched(token, 'PopulationLine', title, keyword,'Population')
            return True

        return False

    def match_PercentageLine(self, token):
        return self._match_title_line(token, 'PercentageLine', self.dialect.percentage_keywords)
    
    def match_TotalCountLine(self, token):
        return self._match_title_line(token, 'TotalCountLine', self.dialect.total_count_keywords)
    
    def match_TotalRunnersLine(self, token):
        return self._match_title_line(token, 'TotalRunnersLine', self.dialect.total_runners_keywords)
    
    def match_GroupsLine(self, token):
        return self._match_title_line(token, 'GroupsLine', self.dialect.groups_keywords)
    
    def match_GroupTypeLine(self, token):
        for keyword in (k for k in self.dialect.type_keywords if token.line.startswith(k)):
            title = token.line.get_rest_trimmed(len(keyword))
            self._set_token_matched(token, 'GroupTypeLine', title, keyword,"Type")
            return True

        return False
    
    def match_FeaturesLine(self, token):
        return self._match_title_line(token, 'FeaturesLine', self.dialect.features_keywords)

    def match_SynchronizedLine(self, token):
        return self._match_title_line(token, 'SynchronizedLine', self.dialect.synchronized_keywords)

    def match_Comment(self, token):
        if not token.line.startswith('#'):
            return False
        text = token.line._line_text  # take the entire line, including leading space
        self._set_token_matched(token, 'Comment', text, indent=0)
        return True

    def match_Empty(self, token):
        if not token.line.is_empty():
            return False

        self._set_token_matched(token, 'Empty', indent=0)
        return True

    def match_Language(self, token):
        match = self.LANGUAGE_RE.match(token.line.get_line_text())
        if not match:
            return False

        dialect_name = match.group(1)
        self._set_token_matched(token, 'Language', dialect_name)
        self._change_dialect(dialect_name, token.location)
        return True

    def match_TagLine(self, token):
        if not token.line.startswith('@'):
            return False

        self._set_token_matched(token, 'TagLine', items=token.line.tags)
        return True

    def match_DocStringSeparator(self, token):
        if not self._active_doc_string_separator:
            # open
            return (self._match_DocStringSeparator(token, '"""', True) or
                    self._match_DocStringSeparator(token, '```', True))
        else:
            # close
            return self._match_DocStringSeparator(token, self._active_doc_string_separator, False)

    def _match_DocStringSeparator(self, token, separator, is_open):
        if not token.line.startswith(separator):
            return False

        content_type = None
        if is_open:
            content_type = token.line.get_rest_trimmed(len(separator))
            self._active_doc_string_separator = separator
            self._indent_to_remove = token.line.indent
        else:
            self._active_doc_string_separator = None
            self._indent_to_remove = 0

        # TODO: Use the separator as keyword. That's needed for pretty printing.
        self._set_token_matched(token, 'DocStringSeparator', content_type, separator)
        return True

    def match_Other(self, token):
        # take the entire line, except removing DocString indents
        text = token.line.get_line_text(self._indent_to_remove)
        self._set_token_matched(token, 'Other', self._unescaped_docstring(text), indent=0)
        return True

    def match_EOF(self, token):
        if not token.eof():
            return False

        self._set_token_matched(token, 'EOF')
        return True

    def _match_title_line(self, token, token_type, keywords,keyword_type=None):        
        for keyword in (k for k in keywords if token.line.startswith_title_keyword(k)):
            title = token.line.get_rest_trimmed(len(keyword) + len(':'))
            self._set_token_matched(token, token_type, title, keyword,keyword_type)
            return True
        return False

    def _set_token_matched(self, token, matched_type, text=None,
                           keyword=None, keyword_type=None, indent=None, items=None):
        if items is None:
            items = []
        token.matched_type = matched_type
        # text == '' should not result in None
        token.matched_text = text.rstrip('\r\n') if text is not None else None
        token.matched_keyword = keyword
        token.matched_keyword_type = keyword_type
        if indent is not None:
            token.matched_indent = indent
        else:
            token.matched_indent = token.line.indent if token.line else 0
        token.matched_items = items
        token.location['column'] = token.matched_indent + 1
        token.matched_salad_dialect = self.dialect_name

    def _change_dialect(self, dialect_name, location=None):
        dialect = Dialect.for_name(dialect_name)
        if not dialect:
            raise NoSuchLanguageException(dialect_name, location)

        self.dialect_name = dialect_name
        self.dialect = dialect

    def _unescaped_docstring(self, text):
        if self._active_doc_string_separator == '"""':
            return text.replace('\\"\\"\\"', '"""')
        elif self._active_doc_string_separator == '```':
            return text.replace('\\`\\`\\`', '```')
        else:
            return text
