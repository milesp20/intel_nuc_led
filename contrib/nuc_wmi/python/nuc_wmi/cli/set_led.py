"""
`nuc_wmi.cli.set_led` provides a CLI interface to the WMI set led state function.
"""

from __future__ import print_function

import sys

from argparse import ArgumentParser
from json import dumps

from nuc_wmi import CONTROL_FILE, LED_BRIGHTNESS, LED_COLOR, LED_COLOR_TYPE, LED_BLINK_FREQUENCY, LED_TYPE, LOCK_FILE
from nuc_wmi.set_led import set_led
from nuc_wmi.utils import acquire_file_lock, load_nuc_wmi_spec


def set_led_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.set_led` `set_led` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       brightness: Controls the brightness level of the LED.
       color: Sets legacy RGB-color for LED.
       frequency: Sets the legacy LED frequency.
       led: Selects the legacy LED to set the state for.
       nuc_wmi_spec_alias: Selects the NUC WMI specification to use from the NUC WMI specification configuration file.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with brightness, frequency, and color of the selected LED or error message with
               failure error.
    Exit code:
       0 on successfully setting the selected LED state properties or 1 on error.
    """

    try:
        nuc_wmi_spec = load_nuc_wmi_spec()

        parser = ArgumentParser(
            description='Set legacy LED state with regard to brightness, frequency, and color.'
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
            choices=[led for led in LED_TYPE['legacy'] if led],
            help='The legacy LED for which to set the state.'
        )
        parser.add_argument(
            'brightness',
            choices=LED_BRIGHTNESS['legacy'],
            help='The brightness to set for the LED.'
        )
        parser.add_argument(
            'frequency',
            choices=[freq for freq in LED_BLINK_FREQUENCY['legacy'] if freq],
            help='The legacy frequency to set for the LED.'
        )
        parser.add_argument(
            'color',
            choices=set(LED_COLOR['legacy']['Dual-color Blue / Amber'] + LED_COLOR['legacy']['RGB-color']),
            help='The legacy color to set for the LED.'
        )

        args = parser.parse_args(args=cli_args)

        with open(args.lock_file or LOCK_FILE, 'w', encoding='utf8') as lock_file:
            acquire_file_lock(lock_file, blocking_file_lock=args.blocking_file_lock)

            led_color_type = LED_COLOR_TYPE['legacy'][args.led]
            led_type_index = LED_TYPE['legacy'].index(args.led)
            frequency_index = LED_BLINK_FREQUENCY['legacy'].index(args.frequency)

            try:
                color_index = LED_COLOR['legacy'][led_color_type].index(args.color)
            except ValueError as err:
                raise ValueError('Invalid color for the specified legacy LED') from err

            set_led(
                nuc_wmi_spec['nuc_wmi_spec'].get(args.nuc_wmi_spec_alias),
                led_type_index,
                args.brightness,
                frequency_index,
                color_index,
                control_file=args.control_file,
                debug=args.debug,
                metadata=None
            )

            print(
                dumps(
                    {
                        'led': {
                            'type': args.led,
                            'brightness': str(args.brightness),
                            'frequency': args.frequency,
                            'color': args.color
                        },
                        'nuc_wmi_spec_alias': args.nuc_wmi_spec_alias
                    }
                )
            )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)
