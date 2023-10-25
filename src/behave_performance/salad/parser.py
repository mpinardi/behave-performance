# This file is generated. Do not edit! Edit Python.razor instead.
import sys
from collections import deque

from .token_matcher import TokenMatcher
from .errors import *
from .ast_builder import AstBuilder
from collections import deque
from .token_scanner import TokenScanner

RULE_TYPE = [
    'None',
    '_EOF',  # #EOF
    '_Empty',  # #Empty
    '_Comment',  # #Comment
    '_TagLine',  # #TagLine
    '_PlanLine',  # #PlanLine
    '_SimulationLine',  # #SimulationLine
    '_SimulationPeriodLine',  # #SimulationPeriodLine
    '_SynchronizedLine',  # #SynchronizedLine
    '_TimeLine',  # #TimeLine
    '_GroupLine',  # #GroupLine
    '_DocStringSeparator',  # #DocStringSeparator
    '_TableRow',  # #TableRow
    '_Language',  # #Language
    '_RunnersLine',  # #RunnersLine
    '_TotalRunnersLine',  # #TotalRunnersLine
    '_CountLine',  # #CountLine
    '_TotalCountLine',  # #TotalCountLine
    '_RandomWaitLine',  # #RandomWaitLine
    '_StartLine',  # #StartLine
    '_StopLine',  # #StopLine
    '_PercentageLine',  # #PercentageLine
    '_RampUpLine',  # #RampUpLine
    '_RampDownLine',  # #RampDownLine
    '_GroupsLine',  # #GroupsLine
    '_GroupTypeLine',  # #GroupTypeLine
    '_FeaturesLine',  # #FeaturesLine
    '_Other',  # #Other
    'SaladDocument',  # SaladDocument! := Plan?
    'Plan',  # Plan! := Plan_Header Groups* Simulation_Definition*
    'Plan_Header',  # Plan_Header! := #Language? Tags? #PlanLine Description_Helper
    'Simulation_Definition',  # Simulation_Definition! := Tags? (Simulation | SimulationPeriod)
    'Simulation',  # Simulation! := #SimulationLine Description_Helper Group* TotalRunners? TotalCount? RampUp? RampDown? RandomWait?
    'SimulationPeriod',  # SimulationPeriod! := #SimulationPeriodLine Description_Helper Group* Time TotalRunners? RampUp? RampDown? RandomWait?
    'Groups',  # Groups! := #GroupsLine Description_Helper Type*
    'Type',  # Type! := #GroupTypeLine Group_Type_Arg?
    'Group_Type_Arg',  # Group_Type_Arg := DataTable? DocString? Features
    'Features',  # Features! := #FeaturesLine
    'Group',  # Group! := #GroupLine Group_Arg?
    'Group_Arg',  # Group_Arg := DataTable? DocString? (Runners | Percentage) Count? Start? Stop? Synchronized?
    'DataTable',  # DataTable! := #TableRow+
    'DocString',  # DocString! := #DocStringSeparator #Other* #DocStringSeparator
    'Runners',  # Runners! := #RunnersLine
    'Percentage',  # Percentage! := #PercentageLine
    'Count',  # Count! := #CountLine
    'Start',  # Start! := #StartLine
    'Stop',  # Stop! := #StopLine
    'Synchronized',  # Synchronized! := #SynchronizedLine
    'RampUp',  # RampUp! := #RampUpLine
    'RampDown',  # RampDown! := #RampDownLine
    'Tags',  # Tags! := #TagLine+
    'RandomWait',  # RandomWait! := #RandomWaitLine
    'TotalRunners',  # TotalRunners! := #TotalRunnersLine
    'TotalCount',  # TotalCount! := #TotalCountLine
    'Time',  # Time! := #TimeLine Description_Helper
    'Description_Helper',  # Description_Helper := #Empty* Description? #Comment*
    'Description',  # Description! := #Other+
]


class ParserContext(object):
    def __init__(self, token_scanner, token_matcher, token_queue, errors):
        self.token_scanner = token_scanner
        self.token_matcher = token_matcher
        self.token_queue = token_queue
        self.errors = errors


class Parser(object):
    def __init__(self, ast_builder=None):
        self.ast_builder = ast_builder if ast_builder is not None else AstBuilder()
        self.stop_at_first_error = False

    def parse(self, token_scanner_or_str, token_matcher=None):
        if sys.version_info < (3, 0):
            token_scanner = TokenScanner(token_scanner_or_str) if isinstance(token_scanner_or_str, basestring) else token_scanner_or_str
        else:
            token_scanner = TokenScanner(token_scanner_or_str) if isinstance(token_scanner_or_str, str) else token_scanner_or_str
        self.ast_builder.reset()
        if token_matcher is None:
            token_matcher = TokenMatcher()
        token_matcher.reset()
        context = ParserContext(
            token_scanner,
            token_matcher,
            deque(),
            [])

        self.start_rule(context, 'SaladDocument')
        state = 0
        token = None
        while True:
            token = self.read_token(context)
            state = self.match_token(state, token, context)
            if token.eof():
                break

        self.end_rule(context, 'SaladDocument')

        if context.errors:
            raise CompositeParserException(context.errors)

        return self.get_result()

    def build(self, context, token):
        self.handle_ast_error(context, token, self.ast_builder.build)

    def add_error(self, context, error):
        context.errors.append(error)
        if len(context.errors) > 10:
            raise CompositeParserException(context.errors)

    def start_rule(self, context, rule_type):
        self.handle_ast_error(context, rule_type, self.ast_builder.start_rule)

    def end_rule(self, context, rule_type):
        self.handle_ast_error(context, rule_type, self.ast_builder.end_rule)

    def get_result(self):
        return self.ast_builder.get_result()

    def read_token(self, context):
        if context.token_queue:
            return context.token_queue.popleft()
        else:
            return context.token_scanner.read()

    def match_EOF(self, context, token):
        return self.handle_external_error(context, False, token, context.token_matcher.match_EOF)
    def match_Empty(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_Empty)
    def match_Comment(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_Comment)
    def match_TagLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_TagLine)
    def match_PlanLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_PlanLine)
    def match_SimulationLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_SimulationLine)
    def match_SimulationPeriodLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_SimulationPeriodLine)
    def match_SynchronizedLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_SynchronizedLine)
    def match_TimeLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_TimeLine)
    def match_GroupLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_GroupLine)
    def match_DocStringSeparator(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_DocStringSeparator)
    def match_TableRow(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_TableRow)
    def match_Language(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_Language)
    def match_RunnersLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_RunnersLine)
    def match_TotalRunnersLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_TotalRunnersLine)
    def match_CountLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_CountLine)
    def match_TotalCountLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_TotalCountLine)
    def match_RandomWaitLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_RandomWaitLine)
    def match_StartLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_StartLine)
    def match_StopLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_StopLine)
    def match_PercentageLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_PercentageLine)
    def match_RampUpLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_RampUpLine)
    def match_RampDownLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_RampDownLine)
    def match_GroupsLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_GroupsLine)
    def match_GroupTypeLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_GroupTypeLine)
    def match_FeaturesLine(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_FeaturesLine)
    def match_Other(self, context, token):
        if token.eof():
            return False
        return self.handle_external_error(context, False, token, context.token_matcher.match_Other)
    def match_token(self, state, token, context):
        state_map = {
            0: self.match_token_at_0,
            1: self.match_token_at_1,
            2: self.match_token_at_2,
            3: self.match_token_at_3,
            4: self.match_token_at_4,
            5: self.match_token_at_5,
            6: self.match_token_at_6,
            7: self.match_token_at_7,
            8: self.match_token_at_8,
            9: self.match_token_at_9,
            10: self.match_token_at_10,
            11: self.match_token_at_11,
            12: self.match_token_at_12,
            13: self.match_token_at_13,
            14: self.match_token_at_14,
            15: self.match_token_at_15,
            16: self.match_token_at_16,
            17: self.match_token_at_17,
            18: self.match_token_at_18,
            19: self.match_token_at_19,
            20: self.match_token_at_20,
            21: self.match_token_at_21,
            22: self.match_token_at_22,
            23: self.match_token_at_23,
            24: self.match_token_at_24,
            25: self.match_token_at_25,
            26: self.match_token_at_26,
            27: self.match_token_at_27,
            28: self.match_token_at_28,
            29: self.match_token_at_29,
            30: self.match_token_at_30,
            31: self.match_token_at_31,
            32: self.match_token_at_32,
            33: self.match_token_at_33,
            34: self.match_token_at_34,
            35: self.match_token_at_35,
            36: self.match_token_at_36,
            37: self.match_token_at_37,
            38: self.match_token_at_38,
            39: self.match_token_at_39,
            40: self.match_token_at_40,
            41: self.match_token_at_41,
            42: self.match_token_at_42,
            43: self.match_token_at_43,
            44: self.match_token_at_44,
            45: self.match_token_at_45,
            46: self.match_token_at_46,
            47: self.match_token_at_47,
            48: self.match_token_at_48,
            49: self.match_token_at_49,
            50: self.match_token_at_50,
            52: self.match_token_at_52,
            53: self.match_token_at_53,
        }
        if state in state_map:
            return state_map[state](token, context)
        else:
            raise RuntimeError("Unknown state: " + str(state))

    # Start
    def match_token_at_0(self, token, context):
        if self.match_EOF(context, token):
                self.build(context, token)
                return 51
        if self.match_Language(context, token):
                self.start_rule(context, 'Plan')
                self.start_rule(context, 'Plan_Header')
                self.build(context, token)
                return 1
        if self.match_TagLine(context, token):
                self.start_rule(context, 'Plan')
                self.start_rule(context, 'Plan_Header')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 2
        if self.match_PlanLine(context, token):
                self.start_rule(context, 'Plan')
                self.start_rule(context, 'Plan_Header')
                self.build(context, token)
                return 3
        if self.match_Comment(context, token):
                self.build(context, token)
                return 0
        if self.match_Empty(context, token):
                self.build(context, token)
                return 0

        state_comment = "State: 0 - Start"
        token.detach
        expected_tokens = ["#EOF", "#Language", "#TagLine", "#PlanLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 0
    # SaladDocument:0>Plan:0>Plan_Header:0>#Language:0
    def match_token_at_1(self, token, context):
        if self.match_TagLine(context, token):
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 2
        if self.match_PlanLine(context, token):
                self.build(context, token)
                return 3
        if self.match_Comment(context, token):
                self.build(context, token)
                return 1
        if self.match_Empty(context, token):
                self.build(context, token)
                return 1

        state_comment = "State: 1 - SaladDocument:0>Plan:0>Plan_Header:0>#Language:0"
        token.detach
        expected_tokens = ["#TagLine", "#PlanLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 1
    # SaladDocument:0>Plan:0>Plan_Header:1>Tags:0>#TagLine:0
    def match_token_at_2(self, token, context):
        if self.match_TagLine(context, token):
                self.build(context, token)
                return 2
        if self.match_PlanLine(context, token):
                self.end_rule(context, 'Tags')
                self.build(context, token)
                return 3
        if self.match_Comment(context, token):
                self.build(context, token)
                return 2
        if self.match_Empty(context, token):
                self.build(context, token)
                return 2

        state_comment = "State: 2 - SaladDocument:0>Plan:0>Plan_Header:1>Tags:0>#TagLine:0"
        token.detach
        expected_tokens = ["#TagLine", "#PlanLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 2
    # SaladDocument:0>Plan:0>Plan_Header:2>#PlanLine:0
    def match_token_at_3(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Plan_Header')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_Empty(context, token):
                self.build(context, token)
                return 3
        if self.match_Comment(context, token):
                self.build(context, token)
                return 5
        if self.match_GroupsLine(context, token):
                self.end_rule(context, 'Plan_Header')
                self.start_rule(context, 'Groups')
                self.build(context, token)
                return 6
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Plan_Header')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Plan_Header')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Plan_Header')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Other(context, token):
                self.start_rule(context, 'Description')
                self.build(context, token)
                return 4

        state_comment = "State: 3 - SaladDocument:0>Plan:0>Plan_Header:2>#PlanLine:0"
        token.detach
        expected_tokens = ["#EOF", "#Empty", "#Comment", "#GroupsLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 3
    # SaladDocument:0>Plan:0>Plan_Header:3>Description_Helper:1>Description:0>#Other:0
    def match_token_at_4(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Plan_Header')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_Comment(context, token):
                self.end_rule(context, 'Description')
                self.build(context, token)
                return 5
        if self.match_GroupsLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Plan_Header')
                self.start_rule(context, 'Groups')
                self.build(context, token)
                return 6
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Plan_Header')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Plan_Header')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Plan_Header')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Other(context, token):
                self.build(context, token)
                return 4

        state_comment = "State: 4 - SaladDocument:0>Plan:0>Plan_Header:3>Description_Helper:1>Description:0>#Other:0"
        token.detach
        expected_tokens = ["#EOF", "#Comment", "#GroupsLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 4
    # SaladDocument:0>Plan:0>Plan_Header:3>Description_Helper:2>#Comment:0
    def match_token_at_5(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Plan_Header')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_Comment(context, token):
                self.build(context, token)
                return 5
        if self.match_GroupsLine(context, token):
                self.end_rule(context, 'Plan_Header')
                self.start_rule(context, 'Groups')
                self.build(context, token)
                return 6
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Plan_Header')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Plan_Header')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Plan_Header')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Empty(context, token):
                self.build(context, token)
                return 5

        state_comment = "State: 5 - SaladDocument:0>Plan:0>Plan_Header:3>Description_Helper:2>#Comment:0"
        token.detach
        expected_tokens = ["#EOF", "#Comment", "#GroupsLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 5
    # SaladDocument:0>Plan:1>Groups:0>#GroupsLine:0
    def match_token_at_6(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Groups')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_Empty(context, token):
                self.build(context, token)
                return 6
        if self.match_Comment(context, token):
                self.build(context, token)
                return 8
        if self.match_GroupTypeLine(context, token):
                self.start_rule(context, 'Type')
                self.build(context, token)
                return 9
        if self.match_GroupsLine(context, token):
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Groups')
                self.build(context, token)
                return 6
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Other(context, token):
                self.start_rule(context, 'Description')
                self.build(context, token)
                return 7

        state_comment = "State: 6 - SaladDocument:0>Plan:1>Groups:0>#GroupsLine:0"
        token.detach
        expected_tokens = ["#EOF", "#Empty", "#Comment", "#GroupTypeLine", "#GroupsLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 6
    # SaladDocument:0>Plan:1>Groups:1>Description_Helper:1>Description:0>#Other:0
    def match_token_at_7(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Groups')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_Comment(context, token):
                self.end_rule(context, 'Description')
                self.build(context, token)
                return 8
        if self.match_GroupTypeLine(context, token):
                self.end_rule(context, 'Description')
                self.start_rule(context, 'Type')
                self.build(context, token)
                return 9
        if self.match_GroupsLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Groups')
                self.build(context, token)
                return 6
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Other(context, token):
                self.build(context, token)
                return 7

        state_comment = "State: 7 - SaladDocument:0>Plan:1>Groups:1>Description_Helper:1>Description:0>#Other:0"
        token.detach
        expected_tokens = ["#EOF", "#Comment", "#GroupTypeLine", "#GroupsLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 7
    # SaladDocument:0>Plan:1>Groups:1>Description_Helper:2>#Comment:0
    def match_token_at_8(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Groups')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_Comment(context, token):
                self.build(context, token)
                return 8
        if self.match_GroupTypeLine(context, token):
                self.start_rule(context, 'Type')
                self.build(context, token)
                return 9
        if self.match_GroupsLine(context, token):
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Groups')
                self.build(context, token)
                return 6
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Empty(context, token):
                self.build(context, token)
                return 8

        state_comment = "State: 8 - SaladDocument:0>Plan:1>Groups:1>Description_Helper:2>#Comment:0"
        token.detach
        expected_tokens = ["#EOF", "#Comment", "#GroupTypeLine", "#GroupsLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 8
    # SaladDocument:0>Plan:1>Groups:2>Type:0>#GroupTypeLine:0
    def match_token_at_9(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Type')
                self.end_rule(context, 'Groups')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_TableRow(context, token):
                self.start_rule(context, 'DataTable')
                self.build(context, token)
                return 10
        if self.match_DocStringSeparator(context, token):
                self.start_rule(context, 'DocString')
                self.build(context, token)
                return 11
        if self.match_FeaturesLine(context, token):
                self.start_rule(context, 'Features')
                self.build(context, token)
                return 13
        if self.match_GroupTypeLine(context, token):
                self.end_rule(context, 'Type')
                self.start_rule(context, 'Type')
                self.build(context, token)
                return 9
        if self.match_GroupsLine(context, token):
                self.end_rule(context, 'Type')
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Groups')
                self.build(context, token)
                return 6
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Type')
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Type')
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Type')
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 9
        if self.match_Empty(context, token):
                self.build(context, token)
                return 9

        state_comment = "State: 9 - SaladDocument:0>Plan:1>Groups:2>Type:0>#GroupTypeLine:0"
        token.detach
        expected_tokens = ["#EOF", "#TableRow", "#DocStringSeparator", "#FeaturesLine", "#GroupTypeLine", "#GroupsLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 9
    # SaladDocument:0>Plan:1>Groups:2>Type:1>Group_Type_Arg:0>DataTable:0>#TableRow:0
    def match_token_at_10(self, token, context):
        if self.match_TableRow(context, token):
                self.build(context, token)
                return 10
        if self.match_DocStringSeparator(context, token):
                self.end_rule(context, 'DataTable')
                self.start_rule(context, 'DocString')
                self.build(context, token)
                return 11
        if self.match_FeaturesLine(context, token):
                self.end_rule(context, 'DataTable')
                self.start_rule(context, 'Features')
                self.build(context, token)
                return 13
        if self.match_Comment(context, token):
                self.build(context, token)
                return 10
        if self.match_Empty(context, token):
                self.build(context, token)
                return 10

        state_comment = "State: 10 - SaladDocument:0>Plan:1>Groups:2>Type:1>Group_Type_Arg:0>DataTable:0>#TableRow:0"
        token.detach
        expected_tokens = ["#TableRow", "#DocStringSeparator", "#FeaturesLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 10
    # SaladDocument:0>Plan:1>Groups:2>Type:1>Group_Type_Arg:1>DocString:0>#DocStringSeparator:0
    def match_token_at_11(self, token, context):
        if self.match_DocStringSeparator(context, token):
                self.build(context, token)
                return 12
        if self.match_Other(context, token):
                self.build(context, token)
                return 11

        state_comment = "State: 11 - SaladDocument:0>Plan:1>Groups:2>Type:1>Group_Type_Arg:1>DocString:0>#DocStringSeparator:0"
        token.detach
        expected_tokens = ["#DocStringSeparator", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 11
    # SaladDocument:0>Plan:1>Groups:2>Type:1>Group_Type_Arg:1>DocString:2>#DocStringSeparator:0
    def match_token_at_12(self, token, context):
        if self.match_FeaturesLine(context, token):
                self.end_rule(context, 'DocString')
                self.start_rule(context, 'Features')
                self.build(context, token)
                return 13
        if self.match_Comment(context, token):
                self.build(context, token)
                return 12
        if self.match_Empty(context, token):
                self.build(context, token)
                return 12

        state_comment = "State: 12 - SaladDocument:0>Plan:1>Groups:2>Type:1>Group_Type_Arg:1>DocString:2>#DocStringSeparator:0"
        token.detach
        expected_tokens = ["#FeaturesLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 12
    # SaladDocument:0>Plan:1>Groups:2>Type:1>Group_Type_Arg:2>Features:0>#FeaturesLine:0
    def match_token_at_13(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Features')
                self.end_rule(context, 'Type')
                self.end_rule(context, 'Groups')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_GroupTypeLine(context, token):
                self.end_rule(context, 'Features')
                self.end_rule(context, 'Type')
                self.start_rule(context, 'Type')
                self.build(context, token)
                return 9
        if self.match_GroupsLine(context, token):
                self.end_rule(context, 'Features')
                self.end_rule(context, 'Type')
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Groups')
                self.build(context, token)
                return 6
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Features')
                self.end_rule(context, 'Type')
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Features')
                self.end_rule(context, 'Type')
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Features')
                self.end_rule(context, 'Type')
                self.end_rule(context, 'Groups')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 13
        if self.match_Empty(context, token):
                self.build(context, token)
                return 13

        state_comment = "State: 13 - SaladDocument:0>Plan:1>Groups:2>Type:1>Group_Type_Arg:2>Features:0>#FeaturesLine:0"
        token.detach
        expected_tokens = ["#EOF", "#GroupTypeLine", "#GroupsLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 13
    # SaladDocument:0>Plan:2>Simulation_Definition:0>Tags:0>#TagLine:0
    def match_token_at_14(self, token, context):
        if self.match_TagLine(context, token):
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Tags')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Tags')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 14
        if self.match_Empty(context, token):
                self.build(context, token)
                return 14

        state_comment = "State: 14 - SaladDocument:0>Plan:2>Simulation_Definition:0>Tags:0>#TagLine:0"
        token.detach
        expected_tokens = ["#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 14
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:0>#SimulationLine:0
    def match_token_at_15(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_Empty(context, token):
                self.build(context, token)
                return 15
        if self.match_Comment(context, token):
                self.build(context, token)
                return 17
        if self.match_GroupLine(context, token):
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 18
        if self.match_TotalRunnersLine(context, token):
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 27
        if self.match_TotalCountLine(context, token):
                self.start_rule(context, 'TotalCount')
                self.build(context, token)
                return 28
        if self.match_RampUpLine(context, token):
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 29
        if self.match_RampDownLine(context, token):
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Other(context, token):
                self.start_rule(context, 'Description')
                self.build(context, token)
                return 16

        state_comment = "State: 15 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:0>#SimulationLine:0"
        token.detach
        expected_tokens = ["#EOF", "#Empty", "#Comment", "#GroupLine", "#TotalRunnersLine", "#TotalCountLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 15
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:1>Description_Helper:1>Description:0>#Other:0
    def match_token_at_16(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_Comment(context, token):
                self.end_rule(context, 'Description')
                self.build(context, token)
                return 17
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Description')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 18
        if self.match_TotalRunnersLine(context, token):
                self.end_rule(context, 'Description')
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 27
        if self.match_TotalCountLine(context, token):
                self.end_rule(context, 'Description')
                self.start_rule(context, 'TotalCount')
                self.build(context, token)
                return 28
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'Description')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 29
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'Description')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'Description')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Other(context, token):
                self.build(context, token)
                return 16

        state_comment = "State: 16 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:1>Description_Helper:1>Description:0>#Other:0"
        token.detach
        expected_tokens = ["#EOF", "#Comment", "#GroupLine", "#TotalRunnersLine", "#TotalCountLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 16
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:1>Description_Helper:2>#Comment:0
    def match_token_at_17(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_Comment(context, token):
                self.build(context, token)
                return 17
        if self.match_GroupLine(context, token):
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 18
        if self.match_TotalRunnersLine(context, token):
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 27
        if self.match_TotalCountLine(context, token):
                self.start_rule(context, 'TotalCount')
                self.build(context, token)
                return 28
        if self.match_RampUpLine(context, token):
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 29
        if self.match_RampDownLine(context, token):
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Empty(context, token):
                self.build(context, token)
                return 17

        state_comment = "State: 17 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:1>Description_Helper:2>#Comment:0"
        token.detach
        expected_tokens = ["#EOF", "#Comment", "#GroupLine", "#TotalRunnersLine", "#TotalCountLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 17
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:0>#GroupLine:0
    def match_token_at_18(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_TableRow(context, token):
                self.start_rule(context, 'DataTable')
                self.build(context, token)
                return 19
        if self.match_DocStringSeparator(context, token):
                self.start_rule(context, 'DocString')
                self.build(context, token)
                return 20
        if self.match_RunnersLine(context, token):
                self.start_rule(context, 'Runners')
                self.build(context, token)
                return 22
        if self.match_PercentageLine(context, token):
                self.start_rule(context, 'Percentage')
                self.build(context, token)
                return 53
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 18
        if self.match_TotalRunnersLine(context, token):
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 27
        if self.match_TotalCountLine(context, token):
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalCount')
                self.build(context, token)
                return 28
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 29
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 18
        if self.match_Empty(context, token):
                self.build(context, token)
                return 18

        state_comment = "State: 18 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:0>#GroupLine:0"
        token.detach
        expected_tokens = ["#EOF", "#TableRow", "#DocStringSeparator", "#RunnersLine", "#PercentageLine", "#GroupLine", "#TotalRunnersLine", "#TotalCountLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 18
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:0>DataTable:0>#TableRow:0
    def match_token_at_19(self, token, context):
        if self.match_TableRow(context, token):
                self.build(context, token)
                return 19
        if self.match_DocStringSeparator(context, token):
                self.end_rule(context, 'DataTable')
                self.start_rule(context, 'DocString')
                self.build(context, token)
                return 20
        if self.match_RunnersLine(context, token):
                self.end_rule(context, 'DataTable')
                self.start_rule(context, 'Runners')
                self.build(context, token)
                return 22
        if self.match_PercentageLine(context, token):
                self.end_rule(context, 'DataTable')
                self.start_rule(context, 'Percentage')
                self.build(context, token)
                return 53
        if self.match_Comment(context, token):
                self.build(context, token)
                return 19
        if self.match_Empty(context, token):
                self.build(context, token)
                return 19

        state_comment = "State: 19 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:0>DataTable:0>#TableRow:0"
        token.detach
        expected_tokens = ["#TableRow", "#DocStringSeparator", "#RunnersLine", "#PercentageLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 19
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:1>DocString:0>#DocStringSeparator:0
    def match_token_at_20(self, token, context):
        if self.match_DocStringSeparator(context, token):
                self.build(context, token)
                return 21
        if self.match_Other(context, token):
                self.build(context, token)
                return 20

        state_comment = "State: 20 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:1>DocString:0>#DocStringSeparator:0"
        token.detach
        expected_tokens = ["#DocStringSeparator", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 20
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:1>DocString:2>#DocStringSeparator:0
    def match_token_at_21(self, token, context):
        if self.match_RunnersLine(context, token):
                self.end_rule(context, 'DocString')
                self.start_rule(context, 'Runners')
                self.build(context, token)
                return 22
        if self.match_PercentageLine(context, token):
                self.end_rule(context, 'DocString')
                self.start_rule(context, 'Percentage')
                self.build(context, token)
                return 53
        if self.match_Comment(context, token):
                self.build(context, token)
                return 21
        if self.match_Empty(context, token):
                self.build(context, token)
                return 21

        state_comment = "State: 21 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:1>DocString:2>#DocStringSeparator:0"
        token.detach
        expected_tokens = ["#RunnersLine", "#PercentageLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 21
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:2>__alt1:0>Runners:0>#RunnersLine:0
    def match_token_at_22(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Runners')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_CountLine(context, token):
                self.end_rule(context, 'Runners')
                self.start_rule(context, 'Count')
                self.build(context, token)
                return 23
        if self.match_StartLine(context, token):
                self.end_rule(context, 'Runners')
                self.start_rule(context, 'Start')
                self.build(context, token)
                return 24
        if self.match_StopLine(context, token):
                self.end_rule(context, 'Runners')
                self.start_rule(context, 'Stop')
                self.build(context, token)
                return 25
        if self.match_SynchronizedLine(context, token):
                self.end_rule(context, 'Runners')
                self.start_rule(context, 'Synchronized')
                self.build(context, token)
                return 26
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Runners')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 18
        if self.match_TotalRunnersLine(context, token):
                self.end_rule(context, 'Runners')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 27
        if self.match_TotalCountLine(context, token):
                self.end_rule(context, 'Runners')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalCount')
                self.build(context, token)
                return 28
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'Runners')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 29
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'Runners')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'Runners')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Runners')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Runners')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Runners')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 22
        if self.match_Empty(context, token):
                self.build(context, token)
                return 22

        state_comment = "State: 22 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:2>__alt1:0>Runners:0>#RunnersLine:0"
        token.detach
        expected_tokens = ["#EOF", "#CountLine", "#StartLine", "#StopLine", "#SynchronizedLine", "#GroupLine", "#TotalRunnersLine", "#TotalCountLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 22
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:3>Count:0>#CountLine:0
    def match_token_at_23(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Count')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_StartLine(context, token):
                self.end_rule(context, 'Count')
                self.start_rule(context, 'Start')
                self.build(context, token)
                return 24
        if self.match_StopLine(context, token):
                self.end_rule(context, 'Count')
                self.start_rule(context, 'Stop')
                self.build(context, token)
                return 25
        if self.match_SynchronizedLine(context, token):
                self.end_rule(context, 'Count')
                self.start_rule(context, 'Synchronized')
                self.build(context, token)
                return 26
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Count')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 18
        if self.match_TotalRunnersLine(context, token):
                self.end_rule(context, 'Count')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 27
        if self.match_TotalCountLine(context, token):
                self.end_rule(context, 'Count')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalCount')
                self.build(context, token)
                return 28
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'Count')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 29
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'Count')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'Count')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Count')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Count')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Count')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 23
        if self.match_Empty(context, token):
                self.build(context, token)
                return 23

        state_comment = "State: 23 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:3>Count:0>#CountLine:0"
        token.detach
        expected_tokens = ["#EOF", "#StartLine", "#StopLine", "#SynchronizedLine", "#GroupLine", "#TotalRunnersLine", "#TotalCountLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 23
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:4>Start:0>#StartLine:0
    def match_token_at_24(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Start')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_StopLine(context, token):
                self.end_rule(context, 'Start')
                self.start_rule(context, 'Stop')
                self.build(context, token)
                return 25
        if self.match_SynchronizedLine(context, token):
                self.end_rule(context, 'Start')
                self.start_rule(context, 'Synchronized')
                self.build(context, token)
                return 26
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Start')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 18
        if self.match_TotalRunnersLine(context, token):
                self.end_rule(context, 'Start')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 27
        if self.match_TotalCountLine(context, token):
                self.end_rule(context, 'Start')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalCount')
                self.build(context, token)
                return 28
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'Start')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 29
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'Start')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'Start')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Start')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Start')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Start')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 24
        if self.match_Empty(context, token):
                self.build(context, token)
                return 24

        state_comment = "State: 24 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:4>Start:0>#StartLine:0"
        token.detach
        expected_tokens = ["#EOF", "#StopLine", "#SynchronizedLine", "#GroupLine", "#TotalRunnersLine", "#TotalCountLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 24
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:5>Stop:0>#StopLine:0
    def match_token_at_25(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Stop')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_SynchronizedLine(context, token):
                self.end_rule(context, 'Stop')
                self.start_rule(context, 'Synchronized')
                self.build(context, token)
                return 26
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Stop')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 18
        if self.match_TotalRunnersLine(context, token):
                self.end_rule(context, 'Stop')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 27
        if self.match_TotalCountLine(context, token):
                self.end_rule(context, 'Stop')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalCount')
                self.build(context, token)
                return 28
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'Stop')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 29
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'Stop')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'Stop')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Stop')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Stop')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Stop')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 25
        if self.match_Empty(context, token):
                self.build(context, token)
                return 25

        state_comment = "State: 25 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:5>Stop:0>#StopLine:0"
        token.detach
        expected_tokens = ["#EOF", "#SynchronizedLine", "#GroupLine", "#TotalRunnersLine", "#TotalCountLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 25
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:6>Synchronized:0>#SynchronizedLine:0
    def match_token_at_26(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Synchronized')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Synchronized')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 18
        if self.match_TotalRunnersLine(context, token):
                self.end_rule(context, 'Synchronized')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 27
        if self.match_TotalCountLine(context, token):
                self.end_rule(context, 'Synchronized')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalCount')
                self.build(context, token)
                return 28
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'Synchronized')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 29
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'Synchronized')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'Synchronized')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Synchronized')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Synchronized')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Synchronized')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 26
        if self.match_Empty(context, token):
                self.build(context, token)
                return 26

        state_comment = "State: 26 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:6>Synchronized:0>#SynchronizedLine:0"
        token.detach
        expected_tokens = ["#EOF", "#GroupLine", "#TotalRunnersLine", "#TotalCountLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 26
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:3>TotalRunners:0>#TotalRunnersLine:0
    def match_token_at_27(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'TotalRunners')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_TotalCountLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.start_rule(context, 'TotalCount')
                self.build(context, token)
                return 28
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 29
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 27
        if self.match_Empty(context, token):
                self.build(context, token)
                return 27

        state_comment = "State: 27 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:3>TotalRunners:0>#TotalRunnersLine:0"
        token.detach
        expected_tokens = ["#EOF", "#TotalCountLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 27
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:4>TotalCount:0>#TotalCountLine:0
    def match_token_at_28(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'TotalCount')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'TotalCount')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 29
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'TotalCount')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'TotalCount')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'TotalCount')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'TotalCount')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'TotalCount')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 28
        if self.match_Empty(context, token):
                self.build(context, token)
                return 28

        state_comment = "State: 28 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:4>TotalCount:0>#TotalCountLine:0"
        token.detach
        expected_tokens = ["#EOF", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 28
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:5>RampUp:0>#RampUpLine:0
    def match_token_at_29(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'RampUp')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'RampUp')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'RampUp')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'RampUp')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'RampUp')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'RampUp')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 29
        if self.match_Empty(context, token):
                self.build(context, token)
                return 29

        state_comment = "State: 29 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:5>RampUp:0>#RampUpLine:0"
        token.detach
        expected_tokens = ["#EOF", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 29
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:6>RampDown:0>#RampDownLine:0
    def match_token_at_30(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'RampDown')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'RampDown')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'RampDown')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'RampDown')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'RampDown')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 30
        if self.match_Empty(context, token):
                self.build(context, token)
                return 30

        state_comment = "State: 30 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:6>RampDown:0>#RampDownLine:0"
        token.detach
        expected_tokens = ["#EOF", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 30
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:7>RandomWait:0>#RandomWaitLine:0
    def match_token_at_31(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'RandomWait')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_TagLine(context, token):
                self.end_rule(context, 'RandomWait')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'RandomWait')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'RandomWait')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 31
        if self.match_Empty(context, token):
                self.build(context, token)
                return 31

        state_comment = "State: 31 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:7>RandomWait:0>#RandomWaitLine:0"
        token.detach
        expected_tokens = ["#EOF", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 31
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:0>#SimulationPeriodLine:0
    def match_token_at_32(self, token, context):
        if self.match_Empty(context, token):
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 34
        if self.match_GroupLine(context, token):
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 35
        if self.match_TimeLine(context, token):
                self.start_rule(context, 'Time')
                self.build(context, token)
                return 44
        if self.match_Other(context, token):
                self.start_rule(context, 'Description')
                self.build(context, token)
                return 33

        state_comment = "State: 32 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:0>#SimulationPeriodLine:0"
        token.detach
        expected_tokens = ["#Empty", "#Comment", "#GroupLine", "#TimeLine", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 32
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:1>Description_Helper:1>Description:0>#Other:0
    def match_token_at_33(self, token, context):
        if self.match_Comment(context, token):
                self.end_rule(context, 'Description')
                self.build(context, token)
                return 34
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Description')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 35
        if self.match_TimeLine(context, token):
                self.end_rule(context, 'Description')
                self.start_rule(context, 'Time')
                self.build(context, token)
                return 44
        if self.match_Other(context, token):
                self.build(context, token)
                return 33

        state_comment = "State: 33 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:1>Description_Helper:1>Description:0>#Other:0"
        token.detach
        expected_tokens = ["#Comment", "#GroupLine", "#TimeLine", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 33
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:1>Description_Helper:2>#Comment:0
    def match_token_at_34(self, token, context):
        if self.match_Comment(context, token):
                self.build(context, token)
                return 34
        if self.match_GroupLine(context, token):
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 35
        if self.match_TimeLine(context, token):
                self.start_rule(context, 'Time')
                self.build(context, token)
                return 44
        if self.match_Empty(context, token):
                self.build(context, token)
                return 34

        state_comment = "State: 34 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:1>Description_Helper:2>#Comment:0"
        token.detach
        expected_tokens = ["#Comment", "#GroupLine", "#TimeLine", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 34
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:0>#GroupLine:0
    def match_token_at_35(self, token, context):
        if self.match_TableRow(context, token):
                self.start_rule(context, 'DataTable')
                self.build(context, token)
                return 36
        if self.match_DocStringSeparator(context, token):
                self.start_rule(context, 'DocString')
                self.build(context, token)
                return 37
        if self.match_RunnersLine(context, token):
                self.start_rule(context, 'Runners')
                self.build(context, token)
                return 39
        if self.match_PercentageLine(context, token):
                self.start_rule(context, 'Percentage')
                self.build(context, token)
                return 52
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 35
        if self.match_TimeLine(context, token):
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Time')
                self.build(context, token)
                return 44
        if self.match_Comment(context, token):
                self.build(context, token)
                return 35
        if self.match_Empty(context, token):
                self.build(context, token)
                return 35

        state_comment = "State: 35 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:0>#GroupLine:0"
        token.detach
        expected_tokens = ["#TableRow", "#DocStringSeparator", "#RunnersLine", "#PercentageLine", "#GroupLine", "#TimeLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 35
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:0>DataTable:0>#TableRow:0
    def match_token_at_36(self, token, context):
        if self.match_TableRow(context, token):
                self.build(context, token)
                return 36
        if self.match_DocStringSeparator(context, token):
                self.end_rule(context, 'DataTable')
                self.start_rule(context, 'DocString')
                self.build(context, token)
                return 37
        if self.match_RunnersLine(context, token):
                self.end_rule(context, 'DataTable')
                self.start_rule(context, 'Runners')
                self.build(context, token)
                return 39
        if self.match_PercentageLine(context, token):
                self.end_rule(context, 'DataTable')
                self.start_rule(context, 'Percentage')
                self.build(context, token)
                return 52
        if self.match_Comment(context, token):
                self.build(context, token)
                return 36
        if self.match_Empty(context, token):
                self.build(context, token)
                return 36

        state_comment = "State: 36 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:0>DataTable:0>#TableRow:0"
        token.detach
        expected_tokens = ["#TableRow", "#DocStringSeparator", "#RunnersLine", "#PercentageLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 36
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:1>DocString:0>#DocStringSeparator:0
    def match_token_at_37(self, token, context):
        if self.match_DocStringSeparator(context, token):
                self.build(context, token)
                return 38
        if self.match_Other(context, token):
                self.build(context, token)
                return 37

        state_comment = "State: 37 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:1>DocString:0>#DocStringSeparator:0"
        token.detach
        expected_tokens = ["#DocStringSeparator", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 37
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:1>DocString:2>#DocStringSeparator:0
    def match_token_at_38(self, token, context):
        if self.match_RunnersLine(context, token):
                self.end_rule(context, 'DocString')
                self.start_rule(context, 'Runners')
                self.build(context, token)
                return 39
        if self.match_PercentageLine(context, token):
                self.end_rule(context, 'DocString')
                self.start_rule(context, 'Percentage')
                self.build(context, token)
                return 52
        if self.match_Comment(context, token):
                self.build(context, token)
                return 38
        if self.match_Empty(context, token):
                self.build(context, token)
                return 38

        state_comment = "State: 38 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:1>DocString:2>#DocStringSeparator:0"
        token.detach
        expected_tokens = ["#RunnersLine", "#PercentageLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 38
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:2>__alt1:0>Runners:0>#RunnersLine:0
    def match_token_at_39(self, token, context):
        if self.match_CountLine(context, token):
                self.end_rule(context, 'Runners')
                self.start_rule(context, 'Count')
                self.build(context, token)
                return 40
        if self.match_StartLine(context, token):
                self.end_rule(context, 'Runners')
                self.start_rule(context, 'Start')
                self.build(context, token)
                return 41
        if self.match_StopLine(context, token):
                self.end_rule(context, 'Runners')
                self.start_rule(context, 'Stop')
                self.build(context, token)
                return 42
        if self.match_SynchronizedLine(context, token):
                self.end_rule(context, 'Runners')
                self.start_rule(context, 'Synchronized')
                self.build(context, token)
                return 43
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Runners')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 35
        if self.match_TimeLine(context, token):
                self.end_rule(context, 'Runners')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Time')
                self.build(context, token)
                return 44
        if self.match_Comment(context, token):
                self.build(context, token)
                return 39
        if self.match_Empty(context, token):
                self.build(context, token)
                return 39

        state_comment = "State: 39 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:2>__alt1:0>Runners:0>#RunnersLine:0"
        token.detach
        expected_tokens = ["#CountLine", "#StartLine", "#StopLine", "#SynchronizedLine", "#GroupLine", "#TimeLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 39
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:3>Count:0>#CountLine:0
    def match_token_at_40(self, token, context):
        if self.match_StartLine(context, token):
                self.end_rule(context, 'Count')
                self.start_rule(context, 'Start')
                self.build(context, token)
                return 41
        if self.match_StopLine(context, token):
                self.end_rule(context, 'Count')
                self.start_rule(context, 'Stop')
                self.build(context, token)
                return 42
        if self.match_SynchronizedLine(context, token):
                self.end_rule(context, 'Count')
                self.start_rule(context, 'Synchronized')
                self.build(context, token)
                return 43
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Count')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 35
        if self.match_TimeLine(context, token):
                self.end_rule(context, 'Count')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Time')
                self.build(context, token)
                return 44
        if self.match_Comment(context, token):
                self.build(context, token)
                return 40
        if self.match_Empty(context, token):
                self.build(context, token)
                return 40

        state_comment = "State: 40 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:3>Count:0>#CountLine:0"
        token.detach
        expected_tokens = ["#StartLine", "#StopLine", "#SynchronizedLine", "#GroupLine", "#TimeLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 40
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:4>Start:0>#StartLine:0
    def match_token_at_41(self, token, context):
        if self.match_StopLine(context, token):
                self.end_rule(context, 'Start')
                self.start_rule(context, 'Stop')
                self.build(context, token)
                return 42
        if self.match_SynchronizedLine(context, token):
                self.end_rule(context, 'Start')
                self.start_rule(context, 'Synchronized')
                self.build(context, token)
                return 43
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Start')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 35
        if self.match_TimeLine(context, token):
                self.end_rule(context, 'Start')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Time')
                self.build(context, token)
                return 44
        if self.match_Comment(context, token):
                self.build(context, token)
                return 41
        if self.match_Empty(context, token):
                self.build(context, token)
                return 41

        state_comment = "State: 41 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:4>Start:0>#StartLine:0"
        token.detach
        expected_tokens = ["#StopLine", "#SynchronizedLine", "#GroupLine", "#TimeLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 41
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:5>Stop:0>#StopLine:0
    def match_token_at_42(self, token, context):
        if self.match_SynchronizedLine(context, token):
                self.end_rule(context, 'Stop')
                self.start_rule(context, 'Synchronized')
                self.build(context, token)
                return 43
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Stop')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 35
        if self.match_TimeLine(context, token):
                self.end_rule(context, 'Stop')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Time')
                self.build(context, token)
                return 44
        if self.match_Comment(context, token):
                self.build(context, token)
                return 42
        if self.match_Empty(context, token):
                self.build(context, token)
                return 42

        state_comment = "State: 42 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:5>Stop:0>#StopLine:0"
        token.detach
        expected_tokens = ["#SynchronizedLine", "#GroupLine", "#TimeLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 42
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:6>Synchronized:0>#SynchronizedLine:0
    def match_token_at_43(self, token, context):
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Synchronized')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 35
        if self.match_TimeLine(context, token):
                self.end_rule(context, 'Synchronized')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Time')
                self.build(context, token)
                return 44
        if self.match_Comment(context, token):
                self.build(context, token)
                return 43
        if self.match_Empty(context, token):
                self.build(context, token)
                return 43

        state_comment = "State: 43 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:6>Synchronized:0>#SynchronizedLine:0"
        token.detach
        expected_tokens = ["#GroupLine", "#TimeLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 43
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:3>Time:0>#TimeLine:0
    def match_token_at_44(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Time')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_Empty(context, token):
                self.build(context, token)
                return 44
        if self.match_Comment(context, token):
                self.build(context, token)
                return 46
        if self.match_TotalRunnersLine(context, token):
                self.end_rule(context, 'Time')
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 47
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'Time')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 48
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'Time')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 49
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'Time')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 50
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Time')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Time')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Time')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Other(context, token):
                self.start_rule(context, 'Description')
                self.build(context, token)
                return 45

        state_comment = "State: 44 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:3>Time:0>#TimeLine:0"
        token.detach
        expected_tokens = ["#EOF", "#Empty", "#Comment", "#TotalRunnersLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 44
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:3>Time:1>Description_Helper:1>Description:0>#Other:0
    def match_token_at_45(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Time')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_Comment(context, token):
                self.end_rule(context, 'Description')
                self.build(context, token)
                return 46
        if self.match_TotalRunnersLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Time')
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 47
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Time')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 48
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Time')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 49
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Time')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 50
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Time')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Time')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Description')
                self.end_rule(context, 'Time')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Other(context, token):
                self.build(context, token)
                return 45

        state_comment = "State: 45 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:3>Time:1>Description_Helper:1>Description:0>#Other:0"
        token.detach
        expected_tokens = ["#EOF", "#Comment", "#TotalRunnersLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Other"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 45
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:3>Time:1>Description_Helper:2>#Comment:0
    def match_token_at_46(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Time')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_Comment(context, token):
                self.build(context, token)
                return 46
        if self.match_TotalRunnersLine(context, token):
                self.end_rule(context, 'Time')
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 47
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'Time')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 48
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'Time')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 49
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'Time')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 50
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Time')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Time')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Time')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Empty(context, token):
                self.build(context, token)
                return 46

        state_comment = "State: 46 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:3>Time:1>Description_Helper:2>#Comment:0"
        token.detach
        expected_tokens = ["#EOF", "#Comment", "#TotalRunnersLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 46
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:4>TotalRunners:0>#TotalRunnersLine:0
    def match_token_at_47(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'TotalRunners')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 48
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 49
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 50
        if self.match_TagLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'TotalRunners')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 47
        if self.match_Empty(context, token):
                self.build(context, token)
                return 47

        state_comment = "State: 47 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:4>TotalRunners:0>#TotalRunnersLine:0"
        token.detach
        expected_tokens = ["#EOF", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 47
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:5>RampUp:0>#RampUpLine:0
    def match_token_at_48(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'RampUp')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'RampUp')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 49
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'RampUp')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 50
        if self.match_TagLine(context, token):
                self.end_rule(context, 'RampUp')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'RampUp')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'RampUp')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 48
        if self.match_Empty(context, token):
                self.build(context, token)
                return 48

        state_comment = "State: 48 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:5>RampUp:0>#RampUpLine:0"
        token.detach
        expected_tokens = ["#EOF", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 48
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:6>RampDown:0>#RampDownLine:0
    def match_token_at_49(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'RampDown')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'RampDown')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 50
        if self.match_TagLine(context, token):
                self.end_rule(context, 'RampDown')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'RampDown')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'RampDown')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 49
        if self.match_Empty(context, token):
                self.build(context, token)
                return 49

        state_comment = "State: 49 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:6>RampDown:0>#RampDownLine:0"
        token.detach
        expected_tokens = ["#EOF", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 49
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:7>RandomWait:0>#RandomWaitLine:0
    def match_token_at_50(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'RandomWait')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_TagLine(context, token):
                self.end_rule(context, 'RandomWait')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'RandomWait')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'RandomWait')
                self.end_rule(context, 'SimulationPeriod')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 50
        if self.match_Empty(context, token):
                self.build(context, token)
                return 50

        state_comment = "State: 50 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:7>RandomWait:0>#RandomWaitLine:0"
        token.detach
        expected_tokens = ["#EOF", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 50
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:2>__alt1:1>Percentage:0>#PercentageLine:0
    def match_token_at_52(self, token, context):
        if self.match_CountLine(context, token):
                self.end_rule(context, 'Percentage')
                self.start_rule(context, 'Count')
                self.build(context, token)
                return 40
        if self.match_StartLine(context, token):
                self.end_rule(context, 'Percentage')
                self.start_rule(context, 'Start')
                self.build(context, token)
                return 41
        if self.match_StopLine(context, token):
                self.end_rule(context, 'Percentage')
                self.start_rule(context, 'Stop')
                self.build(context, token)
                return 42
        if self.match_SynchronizedLine(context, token):
                self.end_rule(context, 'Percentage')
                self.start_rule(context, 'Synchronized')
                self.build(context, token)
                return 43
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Percentage')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 35
        if self.match_TimeLine(context, token):
                self.end_rule(context, 'Percentage')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Time')
                self.build(context, token)
                return 44
        if self.match_Comment(context, token):
                self.build(context, token)
                return 52
        if self.match_Empty(context, token):
                self.build(context, token)
                return 52

        state_comment = "State: 52 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:1>SimulationPeriod:2>Group:1>Group_Arg:2>__alt1:1>Percentage:0>#PercentageLine:0"
        token.detach
        expected_tokens = ["#CountLine", "#StartLine", "#StopLine", "#SynchronizedLine", "#GroupLine", "#TimeLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 52
    # SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:2>__alt1:1>Percentage:0>#PercentageLine:0
    def match_token_at_53(self, token, context):
        if self.match_EOF(context, token):
                self.end_rule(context, 'Percentage')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.end_rule(context, 'Plan')
                self.build(context, token)
                return 51
        if self.match_CountLine(context, token):
                self.end_rule(context, 'Percentage')
                self.start_rule(context, 'Count')
                self.build(context, token)
                return 23
        if self.match_StartLine(context, token):
                self.end_rule(context, 'Percentage')
                self.start_rule(context, 'Start')
                self.build(context, token)
                return 24
        if self.match_StopLine(context, token):
                self.end_rule(context, 'Percentage')
                self.start_rule(context, 'Stop')
                self.build(context, token)
                return 25
        if self.match_SynchronizedLine(context, token):
                self.end_rule(context, 'Percentage')
                self.start_rule(context, 'Synchronized')
                self.build(context, token)
                return 26
        if self.match_GroupLine(context, token):
                self.end_rule(context, 'Percentage')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'Group')
                self.build(context, token)
                return 18
        if self.match_TotalRunnersLine(context, token):
                self.end_rule(context, 'Percentage')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalRunners')
                self.build(context, token)
                return 27
        if self.match_TotalCountLine(context, token):
                self.end_rule(context, 'Percentage')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'TotalCount')
                self.build(context, token)
                return 28
        if self.match_RampUpLine(context, token):
                self.end_rule(context, 'Percentage')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampUp')
                self.build(context, token)
                return 29
        if self.match_RampDownLine(context, token):
                self.end_rule(context, 'Percentage')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RampDown')
                self.build(context, token)
                return 30
        if self.match_RandomWaitLine(context, token):
                self.end_rule(context, 'Percentage')
                self.end_rule(context, 'Group')
                self.start_rule(context, 'RandomWait')
                self.build(context, token)
                return 31
        if self.match_TagLine(context, token):
                self.end_rule(context, 'Percentage')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Tags')
                self.build(context, token)
                return 14
        if self.match_SimulationLine(context, token):
                self.end_rule(context, 'Percentage')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation')
                self.build(context, token)
                return 15
        if self.match_SimulationPeriodLine(context, token):
                self.end_rule(context, 'Percentage')
                self.end_rule(context, 'Group')
                self.end_rule(context, 'Simulation')
                self.end_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'Simulation_Definition')
                self.start_rule(context, 'SimulationPeriod')
                self.build(context, token)
                return 32
        if self.match_Comment(context, token):
                self.build(context, token)
                return 53
        if self.match_Empty(context, token):
                self.build(context, token)
                return 53

        state_comment = "State: 53 - SaladDocument:0>Plan:2>Simulation_Definition:1>__alt0:0>Simulation:2>Group:1>Group_Arg:2>__alt1:1>Percentage:0>#PercentageLine:0"
        token.detach
        expected_tokens = ["#EOF", "#CountLine", "#StartLine", "#StopLine", "#SynchronizedLine", "#GroupLine", "#TotalRunnersLine", "#TotalCountLine", "#RampUpLine", "#RampDownLine", "#RandomWaitLine", "#TagLine", "#SimulationLine", "#SimulationPeriodLine", "#Comment", "#Empty"]
        error = UnexpectedEOFException(token, expected_tokens, state_comment) if token.eof() else UnexpectedTokenException(token, expected_tokens, state_comment)
        if (self.stop_at_first_error):
            raise error
        self.add_error(context, error)
        return 53
    # private

    def handle_ast_error(self, context, argument, action):
        self.handle_external_error(context, True, argument, action)

    def handle_external_error(self, context, default_value, argument, action):
        if self.stop_at_first_error:
            return action(argument)

        try:
            return action(argument)
        except CompositeParserException as e:
            for error in e.errors:
                self.add_error(context, error)
        except ParserException as e:
            self.add_error(context, e)
        return default_value

