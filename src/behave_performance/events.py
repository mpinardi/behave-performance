from enum import Enum

class PerfEvents(Enum):
    """Behave Performance Events
    """
    SOURCE='source'
    SALAD_DOCUMENT='salad-document'
    SALAD_PARSER_ERROR='salad-parser-error'
    VEGGIE='veggie'
    VEGGIE_ACCEPTED='veggie-accepted'
    VEGGIE_REJECTED='veggie-rejected'
    PERF_RUN_STARTED='perf-run-started'
    PERF_RUN_FINISHED='perf-run-finished'
    SIMULATION_RUN_FINISHED='simulation-run-finished'
    SIMULATION_RUN_STARTED='simulation-run-started'
    CUKE_RUN_FINISHED='cuke-run-finished'
    CUKE_RUN_STARTED='cuke-run-started'
    RAMP_FINISHED='ramp-finished'
    RAMP_STARTED='ramp-started'
    RAMP_PRECENT='ramp-precent'
    SIMULATION_STATISTICS_STARTED='simulation-statistics-started'
    SIMULATION_STATISTICS_FINISHED='simulation-statistics-finished'
    ADD_PLUGIN='add-plugin'
    CONFIG_STATISTICS = 'config-statistics'
    FORMATTER_STARTED = 'formatter-started'
    FORMATTER_FINISHED = 'formatter-finished'
    ANNOUNCEMENT = 'announce'

class BehaveEvents(Enum):
    """Behave events
    """
    TEST_RUN_STARTED='test-run-started'
    TEST_CASE_PREPARED='test-case-prepared'
    TEST_CASE_STARTED='test-case-started'
    TEST_STEP_STARTED='test-step-started'
    TEST_STEP_ATTACHMENT='test-step-attachment'
    TEST_STEP_FINISHED='test-step-finished'
    TEST_CASE_FINISHED='test-case-finished'
    TEST_RUN_FINISHED='test-run-finished'
