"""
`nuc_wmi.cli.get_led` provides a CLI interface to the WMI get led state function.
"""

from __future__ import print_function

import sys

from argparse import ArgumentParser
from json import dumps

from nuc_wmi import CONTROL_FILE, LED_BLINK_FREQUENCY, LED_BRIGHTNESS, LED_COLOR, LED_COLOR_TYPE, LED_TYPE, LOCK_FILE
from nuc_wmi import NucWmiError
from nuc_wmi.get_led import get_led
from nuc_wmi.utils import acquire_file_lock, defined_indexes, load_nuc_wmi_spec


def get_led_cli(cli_args=None): # pylint: disable=too-many-locals
    """
    Creates a CLI interface on top of the `nuc_wmi.get_led` `get_led` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       led: Selects the legacy LED to get the state for.
       nuc_wmi_spec_alias: Selects the NUC WMI specification to use from the NUC WMI specification configuration file.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with brightness, frequency, and color of the selected LED or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the selected LED state properties or 1 on error.
    """

    try:
        nuc_wmi_spec = load_nuc_wmi_spec()

        parser = ArgumentParser(
            description='Get legacy LED state with regard to brightness, frequency, and color.'
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
            choices=[led for led in LED_TYPE['legacy'] if led],
            help='The legacy LED for which to get the state.'
        )

        args = parser.parse_args(args=cli_args)

        with open(args.lock_file or LOCK_FILE, 'w', encoding='utf8') as lock_file:
            acquire_file_lock(lock_file)

            led_color_type = LED_COLOR_TYPE['legacy'][args.led]
            led_type_index = LED_TYPE['legacy'].index(args.led)

            brightness_range = defined_indexes(LED_BRIGHTNESS['legacy'])
            color_range = defined_indexes(LED_COLOR['legacy'][led_color_type])
            frequency_range = defined_indexes(LED_BLINK_FREQUENCY['legacy'])

            (brightness, frequency_index, color_index) = get_led( # pylint: disable=unbalanced-tuple-unpacking
                nuc_wmi_spec['nuc_wmi_spec'].get(args.nuc_wmi_spec_alias),
                led_type_index,
                control_file=args.control_file,
                debug=args.debug,
                metadata={
                    'brightness_range': brightness_range,
                    'color_range': color_range,
                    'frequency_range': frequency_range
                }
            )

            if brightness not in brightness_range:
                raise NucWmiError(
                    "Error (Intel NUC WMI get_led function returned invalid brightness of %i, expected one of %s)" % \
                    (brightness, str(brightness_range))
                )

            if color_index not in color_range:
                raise NucWmiError(
                    "Error (Intel NUC WMI get_led function returned invalid color of %i, expected one of %s)" % \
                    (color_index, str(color_range))
                )

            if frequency_index not in frequency_range:
                raise NucWmiError(
                    "Error (Intel NUC WMI get_led function returned invalid frequency of %i, expected one of %s)" % \
                    (frequency_index, str(frequency_range))
                )

            led_color = LED_COLOR['legacy'][led_color_type][color_index]
            led_frequency = LED_BLINK_FREQUENCY['legacy'][frequency_index]

            print(
                dumps(
                    {
                        'led': {
                            'type': args.led,
                            'brightness': str(brightness),
                            'frequency': led_frequency,
                            'color': led_color
                        },
                        'nuc_wmi_spec_alias': args.nuc_wmi_spec_alias
                    }
                )
            )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)
