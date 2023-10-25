from behave_performance.formatter.base_formatter import Formatter

class SilentProgressFormatter(Formatter):
    DEFAULT=False
    FAMILY='progress'
    SINGLETON=True

    def __init__(self, options):
        super().__init__(options)