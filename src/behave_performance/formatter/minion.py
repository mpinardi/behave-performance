class Minion:
    def __init__(self, options):
        self.colorFns = options.get('color_fns', None)
        self.strict = options.get('strict', None)
        self.options = options.get('options', None)

    async def run(self, obj):
        return obj