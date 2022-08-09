"""
`nuc_wmi.cli.switch_led_type` provides a CLI interface to the WMI switch led type function.
"""

from __future__ import print_function

import sys

from argparse import ArgumentParser
from json import dumps

from nuc_wmi import CONTROL_FILE
from nuc_wmi.switch_led_type import LED_COLOR_GROUP, switch_led_type

import nuc_wmi

def switch_led_type_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.switch_led_type` `switch_led_type` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       led_color_group: Selects the LED color group type to set..
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with the selected LED color group type or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the selected LED state properties or 1 on error.
    """

    parser = ArgumentParser(
        description='Switches the LED color group type.'
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
        'led_color_group',
        choices=LED_COLOR_GROUP,
        help='The LED color group type to set the LEDs to.'
    )

    try:
        args = parser.parse_args(args=cli_args)

        led_color_group_index = LED_COLOR_GROUP.index(args.led_color_group)

        switch_led_type(
            led_color_group_index,
            control_file=args.control_file,
            debug=args.debug,
            quirks=args.quirks
        )

        print(
            dumps(
                {
                    'led_color_group': {
                        'type': args.led_color_group
                    }
                }
            )
        )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)
