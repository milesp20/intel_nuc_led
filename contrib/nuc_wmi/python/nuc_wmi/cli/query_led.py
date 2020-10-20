"""
`nuc_wmi.cli.query_led` provides a CLI interface to the WMI query led set of functions.
"""

from __future__ import print_function

import sys

from argparse import ArgumentParser
from json import dumps

from nuc_wmi import CONTROL_ITEM, CONTROL_FILE, LED_COLOR_TYPE, LED_INDICATOR_OPTION, LED_TYPE
from nuc_wmi.query_led import query_led_color_type, query_led_control_items, query_led_indicator_options, query_leds

def query_led_color_type_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.query_led` `query_led_color_type` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       led: Selects the LED to get the color type for.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with color type of the selected LED or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the selected LED's color type or 1 on error.
    """

    parser = ArgumentParser(
        description='Query the LED color type for the LED type.'
    )

    parser.add_argument(
        '-c',
        '--control-file',
        default=None,
        help='The path to the NUC WMI control file. Defaults to ' + CONTROL_FILE + ' if not specified.'
    )
    parser.add_argument(
        'led',
        choices=LED_TYPE['new'],
        help='The LED for which to get the color type.'
    )

    try:
        args = parser.parse_args(args=cli_args)

        led_color_type = query_led_color_type(LED_TYPE['new'].index(args.led), control_file=args.control_file)

        print(
            dumps(
                {
                    'led': {
                        'type': args.led,
                        'color_type': LED_COLOR_TYPE['new'][led_color_type]
                    }
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
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with control items for the selected LED indicator option or
               error message with failure error.
    Exit code:
       0 on successfully retrieving the control items or 1 on error.
    """

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
        'led',
        choices=LED_TYPE['new'],
        help='The LED for which to get the control items.'
    )
    parser.add_argument(
        'led_indicator_option',
        choices=LED_INDICATOR_OPTION,
        help='The LED indicator option for the LED for which to get control items.'
    )

    try:
        args = parser.parse_args(args=cli_args)

        led_color_type = query_led_color_type(
            LED_TYPE['new'].index(args.led),
            control_file=args.control_file
        )

        available_indicator_options = query_led_indicator_options(
            LED_TYPE['new'].index(args.led),
            control_file=args.control_file
        )

        indicator = LED_INDICATOR_OPTION.index(args.led_indicator_option)

        if indicator not in available_indicator_options:
            raise ValueError('Invalid indicator option for the selected LED')

        control_items = query_led_control_items(
            LED_TYPE['new'].index(args.led),
            indicator,
            control_file=args.control_file
        )

        print(
            dumps(
                {
                    'led': {
                        'type': args.led,
                        'indicator_option': args.led_indicator_option,
                        'control_items': [CONTROL_ITEM[indicator][led_color_type][control_item]['Control Item'] \
                                          for control_item in control_items]
                    }
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
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with indicator options of the selected LED or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the selected LED's indicator options or 1 on error.
    """

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
        'led',
        choices=LED_TYPE['new'],
        help='The LED for which to get the indicator options.'
    )

    try:
        args = parser.parse_args(args=cli_args)

        led_indicator_options = query_led_indicator_options(
            LED_TYPE['new'].index(args.led),
            control_file=args.control_file
        )

        print(
            dumps(
                {
                    'led': {
                        'type': args.led,
                        'indicator_options': [LED_INDICATOR_OPTION[indicator] for indicator in led_indicator_options]
                    }
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
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with list of available LEDs or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the list of available LEDs or 1 on error.
    """

    parser = ArgumentParser(
        description='List all LED types supported.'
    )

    parser.add_argument(
        '-c',
        '--control-file',
        default=None,
        help='The path to the NUC WMI control file. Defaults to ' + CONTROL_FILE + ' if not specified.'
    )

    try:
        args = parser.parse_args(args=cli_args)

        leds = query_leds(control_file=args.control_file)

        print(
            dumps(
                {
                    'leds': [LED_TYPE['new'][led] for led in leds]
                }
            )
        )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)
