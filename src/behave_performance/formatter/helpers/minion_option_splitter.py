from os import getcwd
class MinionOptionSplitter:
    @staticmethod
    def split(minion, formatter_options):
        result = minion.split(':')
        return {
            "type": result[0] if result else minion,
            "options": MinionOptionSplitter.get_options(result[1] if len(result) > 1 else '', formatter_options),
        }

    @staticmethod
    def get_options(options, formatter_options):
        mo = options.split(',') if ',' in options else [] if not options else [options]
        return {
            "options": mo,
            "colors_enabled": formatter_options.get('colors_enabled',True),
            "cwd": formatter_options.get('cwd', getcwd()),
            "strict": formatter_options.get('strict',False),
        }