import asyncio
import aiofiles
from behave_performance.formatter.builder import PluginBuilder as FormatterBuilder
from behave_performance.formatter.base_formatter import Formatter
from behave_performance.formatter.helpers.output_path_helpers import get_path_with_prefix
from behave_performance.option_spliter import split
from behave_performance.helpers.paths import get_absolute_path
from behave_performance.configuration import Configuration

class FormattersInitializer:
    def __init__(self, stdout, cwd, config:Configuration):
        self.stdout = stdout
        self.cwd = cwd
        self.streams_to_close = []
        self.formatters = []
        self.silent = config.silent
        self.silent_progress = config.silent_progress
        self.silent_anouncements = config.silent_announcements
        self.strict = config.strict
        self.formats = config.format
        self.format_options = config.format_options

    async def initialize_formatters(self, event_broadcaster, format_options=None, formats=None, strict=None):
        if not strict:
             strict = self.strict
        if not formats:
             formats = self.formats
        if not format_options:
             format_options = self.format_options
        if formats:
            for format in formats:
                fmtr = await self.initialize_formatter(event_broadcaster, split(format), strict, format_options)
                if fmtr:
                    self.formatters.append(fmtr)
                else:
                    print(f'\nWarning: Passed in formatter \"{format}\" does not exists and has been ignored')
        for fc in Formatter.__subclasses__():
            if fc.DEFAULT:
                found = False
                for f in self.formatters:
                    if fc.__name__ == f['formatter'].__class__.__name__:
                        found = True
                    elif fc.SINGLETON:
                            if f["formatter"].FAMILY == fc.FAMILY:
                                found = True
                if not found:
                    name = fc.__module__ + '.' + fc.__qualname__
                    self.formatters.append(await self.initialize_formatter(event_broadcaster, split(name), strict, format_options))
        for f in self.formatters:
            if self.silent_progress and f['formatter'].FAMILY == 'progress':
                    f['formatter'].update_log(None)
            elif self.silent_anouncements and f['formatter'].FAMILY == 'announcement':
                    f['formatter'].update_log(None)
            elif self.silent and f['formatter'].is_stdio():
                    f['formatter'].update_log(None)

    
    async def close_streams(self):
        for stream in self.streams_to_close:
            await stream.close()

    async def initialize_formatter(self, event_broadcaster, format, strict, format_options):
        type, output_to, options = format["type"], format["output_to"], format["options"]
        stream = self.stdout
        if output_to:
            output_path = get_absolute_path(get_path_with_prefix(output_to, 0))
            stream = await aiofiles.open(output_path, 'w+', encoding='utf8')
            self.streams_to_close.append(stream)
            
        type_options = {
            "event_broadcaster": event_broadcaster,
            "stream": stream,
            "strict": strict,
            **format_options,
            "options": options,
        }

        if "colors_enabled" not in format_options:
            type_options["colors_enabled"] = stream.isatty()

        formatter = FormatterBuilder.build(type, type_options)
        if not formatter:
             return
        return {"formatter": formatter, "output_to": output_to}

    async def update_formatters(self, count):
        async def update_formatter(formatter, output_to):
                nonlocal self
                if hasattr(formatter, 'is_stdio') and callable(getattr(formatter, 'is_stdio')) and not formatter.is_stdio():
                    # fd = await asyncio.to_thread(
                    #     lambda: os.open(get_absolute_path(get_path_with_prefix(output_to, count)), os.O_WRONLY | os.O_CREAT)
                    # )
                    # stream = io.open(fd, 'w+')
                    stream = await aiofiles.open(get_absolute_path(get_path_with_prefix(output_to, count)), 'w+', encoding='utf8')
                    formatter.update_log(stream)
                    self.streams_to_close.append(stream)

        await asyncio.gather(*[update_formatter(formatter['formatter'], formatter['output_to']) for formatter in self.formatters])

