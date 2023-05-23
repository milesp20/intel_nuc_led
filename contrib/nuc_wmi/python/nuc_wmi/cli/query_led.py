"""
`nuc_wmi.cli.query_led` provides a CLI interface to the WMI query led set of functions.
"""

from __future__ import print_function

import sys

from argparse import ArgumentParser
from json import dumps

from nuc_wmi import CONTROL_ITEM, CONTROL_FILE, LED_COLOR_TYPE, LED_INDICATOR_OPTION, LED_TYPE, LOCK_FILE
from nuc_wmi.query_led import query_led_color_type, query_led_control_items, query_led_indicator_options, query_leds
from nuc_wmi.utils import acquire_file_lock, load_nuc_wmi_spec


def query_led_color_type_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.query_led` `query_led_color_type` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       led: Selects the LED to get the color type for.
       nuc_wmi_spec_alias: Selects the NUC WMI specification to use from the NUC WMI specification configuration file.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with color type of the selected LED or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the selected LED's color type or 1 on error.
    """

    try:
        nuc_wmi_spec = load_nuc_wmi_spec()

        parser = ArgumentParser(
            description='Query the LED color type for the LED type.'
        )

        parser.add_argument(
            '-b',
            '--blocking-file-lock',
            action='store_true',
            help='Acquire a blocking lock on the NUC WMI lock file instead of the default non blocking lock.'
        )
        parser.add_argument(
            '-c',
            '--control-file',
            default=None,
            help='The path to the NUC WMI control file. Defaults to ' + CONTROL_FILE + ' if not specified.'
        )
        parser.add_argument(
            '-d',
            '--debug',
            action='store_true',
            help='Enable debug logging of read and write to the NUC LED control file to stderr.'
        )
        parser.add_argument(
            '-l',
            '--lock-file',
            default=None,
            help='The path to the NUC WMI lock file. Defaults to ' + LOCK_FILE + ' if not specified.'
        )
        parser.add_argument(
            'nuc_wmi_spec_alias',
            choices=nuc_wmi_spec['nuc_wmi_spec'].keys(),
            help='The name of the NUC WMI specification to use from the specification configuration file.'
        )
        parser.add_argument(
            'led',
            choices=LED_TYPE['new'],
            help='The LED for which to get the color type.'
        )

        args = parser.parse_args(args=cli_args)

        with open(args.lock_file or LOCK_FILE, 'w', encoding='utf8') as lock_file:
            acquire_file_lock(lock_file, blocking_file_lock=args.blocking_file_lock)

            led_type_index = LED_TYPE['new'].index(args.led)

            led_color_type_index = query_led_color_type(
                nuc_wmi_spec['nuc_wmi_spec'].get(args.nuc_wmi_spec_alias),
                led_type_index,
                control_file=args.control_file,
                debug=args.debug,
                metadata=None
            )

            led_color_type = LED_COLOR_TYPE['new'][led_color_type_index]

            print(
                dumps(
                    {
                        'led': {
                            'type': args.led,
                            'color_type': led_color_type
                        },
                        'nuc_wmi_spec_alias': args.nuc_wmi_spec_alias
                    }
                )
            )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)


def query_led_control_items_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.query_led` `query_led_control_items` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       led_indicator_option: The indicator option for the specified LED type for which to retrieve the available control
                             items.
       led: Selects the LED to get the available control items for.
       nuc_wmi_spec_alias: Selects the NUC WMI specification to use from the NUC WMI specification configuration file.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with control items for the selected LED indicator option or
               error message with failure error.
    Exit code:
       0 on successfully retrieving the control items or 1 on error.
    """

    try:
        nuc_wmi_spec = load_nuc_wmi_spec()

        parser = ArgumentParser(
            description='Query the LED control items for the LED indicator option of the LED type.'
        )

        parser.add_argument(
            '-c',
            '--control-file',
            default=None,
            help='The path to the NUC WMI control file. Defaults to ' + CONTROL_FILE + ' if not specified.'
        )
        parser.add_argument(
            '-d',
            '--debug',
            action='store_true',
            help='Enable debug logging of read and write to the NUC LED control file to stderr.'
        )
        parser.add_argument(
            '-l',
            '--lock-file',
            default=None,
            help='The path to the NUC WMI lock file. Defaults to ' + LOCK_FILE + ' if not specified.'
        )
        parser.add_argument(
            'nuc_wmi_spec_alias',
            choices=nuc_wmi_spec['nuc_wmi_spec'].keys(),
            help='The name of the NUC WMI specification to use from the specification configuration file.'
        )
        parser.add_argument(
            'led',
            choices=LED_TYPE['new'],
            help='The LED for which to get the control items.'
        )
        parser.add_argument(
            'led_indicator_option',
            choices=LED_INDICATOR_OPTION,
            help='The LED indicator option for the LED for which to get control items.'
        )

        args = parser.parse_args(args=cli_args)

        with open(args.lock_file or LOCK_FILE, 'w', encoding='utf8') as lock_file:
            acquire_file_lock(lock_file)

            led_type_index = LED_TYPE['new'].index(args.led)

            led_color_type_index = query_led_color_type(
                nuc_wmi_spec['nuc_wmi_spec'].get(args.nuc_wmi_spec_alias),
                led_type_index,
                control_file=args.control_file,
                debug=args.debug,
                metadata=None
            )

            available_indicator_option_indexes = query_led_indicator_options(
                nuc_wmi_spec['nuc_wmi_spec'].get(args.nuc_wmi_spec_alias),
                led_type_index,
                control_file=args.control_file,
                debug=args.debug,
                metadata=None
            )

            led_indicator_option_index = LED_INDICATOR_OPTION.index(args.led_indicator_option)

            if led_indicator_option_index not in available_indicator_option_indexes:
                raise ValueError('Invalid indicator option for the selected LED')

            available_control_item_indexes = query_led_control_items(
                nuc_wmi_spec['nuc_wmi_spec'].get(args.nuc_wmi_spec_alias),
                led_type_index,
                led_indicator_option_index,
                control_file=args.control_file,
                debug=args.debug,
                metadata=None
            )

            led_control_items = [
                CONTROL_ITEM[led_indicator_option_index][led_color_type_index][control_item_index]['Control Item'] \
                for control_item_index in available_control_item_indexes
            ]

            print(
                dumps(
                    {
                        'led': {
                            'type': args.led,
                            'indicator_option': args.led_indicator_option,
                            'control_items': led_control_items
                        },
                        'nuc_wmi_spec_alias': args.nuc_wmi_spec_alias
                    }
                )
            )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)


def query_led_indicator_options_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.query_led` `query_led_indicator_options` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       led: Selects the LED to get the indicator options for.
       nuc_wmi_spec_alias: Selects the NUC WMI specification to use from the NUC WMI specification configuration file.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with indicator options of the selected LED or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the selected LED's indicator options or 1 on error.
    """

    try:
        nuc_wmi_spec = load_nuc_wmi_spec()

        parser = ArgumentParser(
            description='Query the LED indicator options available for the LED type.'
        )

        parser.add_argument(
            '-c',
            '--control-file',
            default=None,
            help='The path to the NUC WMI control file. Defaults to ' + CONTROL_FILE + ' if not specified.'
        )
        parser.add_argument(
            '-d',
            '--debug',
            action='store_true',
            help='Enable debug logging of read and write to the NUC LED control file to stderr.'
        )
        parser.add_argument(
            '-l',
            '--lock-file',
            default=None,
            help='The path to the NUC WMI lock file. Defaults to ' + LOCK_FILE + ' if not specified.'
        )
        parser.add_argument(
            'nuc_wmi_spec_alias',
            choices=nuc_wmi_spec['nuc_wmi_spec'].keys(),
            help='The name of the NUC WMI specification to use from the specification configuration file.'
        )
        parser.add_argument(
            'led',
            choices=LED_TYPE['new'],
            help='The LED for which to get the indicator options.'
        )

        args = parser.parse_args(args=cli_args)

        with open(args.lock_file or LOCK_FILE, 'w', encoding='utf8') as lock_file:
            acquire_file_lock(lock_file)

            led_type_index = LED_TYPE['new'].index(args.led)

            available_indicator_option_indexes = query_led_indicator_options(
                nuc_wmi_spec['nuc_wmi_spec'].get(args.nuc_wmi_spec_alias),
                led_type_index,
                control_file=args.control_file,
                debug=args.debug,
                metadata=None
            )

            led_indicator_options = [
                LED_INDICATOR_OPTION[led_indicator_option_index] \
                for led_indicator_option_index in available_indicator_option_indexes
            ]

            print(
                dumps(
                    {
                        'led': {
                            'type': args.led,
                            'indicator_options': led_indicator_options
                        },
                        'nuc_wmi_spec_alias': args.nuc_wmi_spec_alias
                    }
                )
            )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)


def query_leds_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.query_led` `query_leds` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       nuc_wmi_spec_alias: Selects the NUC WMI specification to use from the NUC WMI specification configuration file.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with list of available LEDs or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the list of available LEDs or 1 on error.
    """

    try:
        nuc_wmi_spec = load_nuc_wmi_spec()

        parser = ArgumentParser(
            description='List all LED types supported.'
        )

        parser.add_argument(
            '-c',
            '--control-file',
            default=None,
            help='The path to the NUC WMI control file. Defaults to ' + CONTROL_FILE + ' if not specified.'
        )
        parser.add_argument(
            '-d',
            '--debug',
            action='store_true',
            help='Enable debug logging of read and write to the NUC LED control file to stderr.'
        )
        parser.add_argument(
            '-l',
            '--lock-file',
            default=None,
            help='The path to the NUC WMI lock file. Defaults to ' + LOCK_FILE + ' if not specified.'
        )
        parser.add_argument(
            'nuc_wmi_spec_alias',
            choices=nuc_wmi_spec['nuc_wmi_spec'].keys(),
            help='The name of the NUC WMI specification to use from the specification configuration file.'
        )

        args = parser.parse_args(args=cli_args)

        with open(args.lock_file or LOCK_FILE, 'w', encoding='utf8') as lock_file:
            acquire_file_lock(lock_file)

            available_led_type_indexes = query_leds(
                nuc_wmi_spec['nuc_wmi_spec'].get(args.nuc_wmi_spec_alias),
                control_file=args.control_file,
                debug=args.debug,
                metadata=None
            )

            led_types = [LED_TYPE['new'][led_type_index] for led_type_index in available_led_type_indexes]

            print(
                dumps(
                    {
                        'leds': led_types,
                        'nuc_wmi_spec_alias': args.nuc_wmi_spec_alias
                    }
                )
            )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)
