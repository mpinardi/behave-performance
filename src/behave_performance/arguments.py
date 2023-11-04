# -*- coding: utf-8 -*-
"""

@Author: Inital version taken from behave x project
"""
# __future__ has been added to maintain compatibility
from __future__ import absolute_import

import argparse

BEHAVE_ARGS = [
    'dry_run',
    'filename',
    'no_color',
    'color',
    'define',
    'exclude',
    'include',
    'no_junit',
    'junit',
    'junit_directory',
    'steps_catalog',
    'no_skipped',
    'show_skipped',
    'lang',
    'no_snippets',
    'snippets',
    'no_multiline',
    'multiline',
    'no_capture',
    'name',
    'capture',
    'no_capture_stderr',
    'capture_stderr',
    'no_logcapture',
    'logcapture',
    'logging_level',
    'logging_format',
    'logging_datefmt',
    'logging_filter',
    'logging_clear_handlers',
    'no_summary',
    'summary',
    'outfile',
    'quiet',
    'no_source',
    'show_source',
    'stage',
    'stop',
    'tags',
    'no_timings',
    'show_timings',
    'verbose',
    'wip',
    'expand',
    'lang_list',
    'lang_help',
    'tags_help',
]

BEHAVE_PERFORMANCE_ARGS = [
    'perf-dry_run',
    'format',
    'format-options',
    'i18n-keywords',
    'i18n-languages',
    'language',
    'no-strict-stats',
    'no-format-color',
    'silent',
    'silent-progress',
    'silent-anouncement',
    'plans',
    'plan-tags',
    'perf-name',
    'profile'

]


def parse_arguments(args):
    """Process all command line arguments"""
    parser = argparse.ArgumentParser(
        description='Behave Performance'
    )
    # -------------------- Behave Performance args---------------------------------------
    perf = parser.add_argument_group('Performance Specific Arguments','Configurations specific to behave performance.')
    perf.add_argument(
        '-p',
        '--plans',
        action='append',
        help='The folder location of the plans you wish to run or a plan file name.',
        required=True,
        metavar="FILE"
    )
    perf.add_argument(
        '--perf-dry-run',
        action='store_true',
        help='Invokes formatters without executing the a plan.',
        required=False,
    )
    perf.add_argument(
        '--no-strict-stats',
        help='enable including failed results in statistics',
        required=False,
        dest='strict',
        action='store_false'
    )
    perf.add_argument(
        '--plan-tags',
        help='only include simulations with tags matching the expression (repeatable)',
        action='append',
        default=None,
        required=False
    )
    perf.add_argument(
        '--perf-name',
        help='Only execute the simulations with name matching the expression (repeatable)',
        default=None,
        action='append',
        required=False
    )
    perf.add_argument(
        '--profile',
        help='specify the profile to use (repeatable)',
        action='append',
        required=False
    )
    perf.add_argument(
        '-f',
        '--format',
        help='Specify the output format, optionally supply PATH to redirect formatter output (repeatable)',
        action='append',
        required=False
    )
    perf.add_argument(
        '--format-options',
        help='Provide options for formatters (repeatable)',
        action='append',
        required=False
    )
    perf.add_argument(
        '--i18n-keywords',
        help='list language keywords',
        required=False,
    )
    perf.add_argument(
        '--i18n-languages',
        help='list languages',
        required=False,
        action='store_true',
        default=False
    )
    perf.add_argument(
        '--language',
        help='Provide the default language for feature files  <ISO 639-1>',
        default='en',
        required=False,
    )

    perf.add_argument(
        '--no-format-color',
        help='Disable color for all performance formatters.',
        required=False,
        action='store_true'
    )

    perf.add_argument(
        '--silent',
        help='Silence all stdout including all formatters and anouncments',
        required=False,
        action='store_true'
    )

    perf.add_argument(
        '--silent-progress',
        help='Silence progress formatter',
        required=False,
        action='store_true'
    )

    perf.add_argument(
        '--silent-announcements',
        help='Silence all announcements',
        required=False,
        action='store_true'
    )

    # --------------------------------------------------------------------------------------

    # ------------------- Behave arguments -------------------#
    behave = parser.add_argument_group('Behave Specific Arguments','Configurations specific to behave.')
    behave.add_argument(
        '-d',
        '--dry-run',
        action='store_true',
        help='Invokes formatters without executing the steps.',
        required=False,
    )
    behave.add_argument('filename')
    behave.add_argument(
        '-t',
        '--tags',
        action='append',
        help='Tags used to properly filter the tests to run. \
                                When multiple --tags (-t) arguments are \
                                provided it means a logical AND \
                                (e.g. -t @TAG_1 -t @TAG_2 means \
                                @TAG_1 AND @TAG_2). \
                                When multiple comma separated tags are \
                                provided as part of the same --tags (-t) \
                                argument it means a logical OR \
                                (e.g. -t @TAG_1,@TAG_2 means \
                                @TAG_1 OR @TAG_2)',
        required=False,
    )
    behave.add_argument(
        '-D',
        '--define',
        help='Define user-specific data in config.userdata '
        'dictionary. Example: -D foo=bar to store it in '
        "config.userdata['foo'].",
        action='append',
        required=False,
    )
    behave.add_argument(
        '--exclude',
        help="Don't run feature files matching regular expression PATTERN.",
        required=False,
    )
    behave.add_argument(
        '-i',
        '--include',
        help='Only run feature files matching regular expression PATTERN.',
        required=False,
    )
    behave.add_argument(
        '--name',
        help='Only execute the feature elements which match'
        ' part of the given name. If this option is given'
        ' more than once, it will match against all the '
        'given names.',
        required=False,
    )
    behave.add_argument(
        '--no_capture',
        help="Don't capture stdout (any stdout output will be printed immediately.)",
        action='store_false',
        required=False,
    )
    behave.add_argument(
        '--capture',
        help='Capture stdout (any stdout output will be '
        'printed if there is a failure.) This is the '
        'default behaviour. This switch is used to '
        'override a configuration file setting.',
        action='store_true',
        required=False,
    )
    behave.add_argument(
        '--no-capture-stderr',
        '--no_capture_stderr',
        help="Don't capture stderr (any stderr output will be printed immediately.)",
        default=False,
        action='store_true',
        required=False,
    )
    behave.add_argument(
        '--capture-stderr',
        '--capture_stderr',
        help='Capture stderr (any stderr output will be pri'
        'nted if there is a failure) This is the default'
        ' behaviour. This switch is used to override a '
        'configuration file setting.',
        default=False,
        action='store_true',
        required=False,
    )
    behave.add_argument(
        '--no-logcapture',
        '--no_logcapture',
        help="Don't capture logging. Logging configuration will be left intact.",
        action='store_true',
        default=False,
        required=False,
    )
    behave.add_argument(
        '--log-capture',
        '--log_capture',
        help='Capture logging. All logging during a step will'
        ' be captured and displayed in the event of a '
        'failure. This is the default behaviour. This '
        'switch is used to override a configuration file'
        ' setting.',
        action='store_true',
        required=False,
    )

    behave.add_argument(
        '--tags-help',
        '--tags_help',
        help='Show help for tag expressions.',
        action='store_true',
        required=False,
    )
    behave.add_argument(
        '--logging-level',
        '--logging_level',
        default='INFO',
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'],
        help='Specify a level to capture logging at. The '
        'default is INFO - capturing everything.',
        required=False,
    )
    behave.add_argument(
        '-ip',
        '--include-paths',
        default=[],
        nargs='*',
        help='Filter test set to the specified list of features '
        'or feature file locations (FEATURE_FILE:LINE).',
    )

    result = parser.parse_args(args)
    
    return result

