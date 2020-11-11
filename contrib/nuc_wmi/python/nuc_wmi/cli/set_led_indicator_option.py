"""
`nuc_wmi.cli.set_led_indicator_option` provides a CLI interface to the WMI set led indicator function.
"""

from __future__ import print_function

import sys

from argparse import ArgumentParser
from json import dumps

from nuc_wmi import CONTROL_FILE, LED_INDICATOR_OPTION, LED_TYPE
from nuc_wmi.set_led_indicator_option import set_led_indicator_option

import nuc_wmi

def set_led_indicator_option_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.set_led_indicator_option` `set_led_indicator_option` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       led_indicator_option: The indicator option for the specified LED type for which to set the indicator option.
       led: Selects the LED to set the indicator option for.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with the set indicator option of the selected LED or error message with
               failure error.
    Exit code:
       0 on successfully setting the selected LED's indicator option or 1 on error.
    """

    parser = ArgumentParser(
        description='Set the LED indicator option for the specified LED type,'
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
        '-q',
        '--quirks',
        action='append',
        choices=nuc_wmi.QUIRKS_AVAILABLE,
        default=None,
        help='Enable NUC WMI quirks to work around various implementation issues or bugs.'
    )
    parser.add_argument(
        'led',
        choices=LED_TYPE['new'],
        help='The LED for which to set the indicator option.'
    )
    parser.add_argument(
        'led_indicator_option',
        choices=LED_INDICATOR_OPTION,
        help='The LED indicator option to set for the LED.'
    )

    try:
        args = parser.parse_args(args=cli_args)

        led_type_index = LED_TYPE['new'].index(args.led)

        led_indicator_option_index = LED_INDICATOR_OPTION.index(args.led_indicator_option)

        set_led_indicator_option(
            led_type_index,
            led_indicator_option_index,
            control_file=args.control_file,
            debug=args.debug,
            quirks=args.quirks
        )

        print(
            dumps(
                {
                    'led': {
                        'type': args.led,
                        'indicator_option': args.led_indicator_option
                    }
                }
            )
        )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)
