"""
`nuc_wmi.cli.set_led` provides a CLI interface to the WMI set led state function.
"""

from __future__ import print_function

from argparse import ArgumentParser
from json import dumps
from sys import exit

from nuc_wmi import CONTROL_FILE, LED_BRIGHTNESS, LED_COLOR, LED_COLOR_TYPE, LED_BLINK_FREQUENCY, LED_TYPE
from nuc_wmi.set_led import set_led

def set_led_cli():
    """
    Creates a CLI interface ontop of the `nuc_wmi.set_led` `set_led` function.

    Args:
       brightness: Controls the brightness level of the LED.
       color: Sets legacy RGB-color for LED.
       frequency: Sets the legacy LED frequency.
       led: Selects the legacy LED to set the state for.
    Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with brightness, frequency, and color of the selected LED or error message with
               failure error.
    Exit code:
       0 on successfully setting the selected LED state properties or 1 on error.
    """

    parser = ArgumentParser(
        description='Set legacy LED state with regard to brightness, frequency, and color.'
    )

    parser.add_argument(
        '-c',
        '--control-file',
        default=None,
        help='The path to the NUC WMI control file. Defaults to ' + CONTROL_FILE + ' if not specified.'
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

    try:
        args = parser.parse_args()

        led_type = LED_TYPE['legacy'].index(args.led)
        frequency = LED_BLINK_FREQUENCY['legacy'].index(args.frequency)

        try:
            color = LED_COLOR['legacy'][LED_COLOR_TYPE['legacy'][args.led]].index(args.color)
        except ValueError as err:
            raise ValueError('Invalid color for the specified legacy LED')

        set_led(led_type, args.brightness, frequency, color, control_file=args.control_file)

        print(
            dumps(
                {
                    'led': {
                        'type': args.led,
                        'brightness': str(args.brightness),
                        'frequency': args.frequency,
                        'color': args.color
                    }
                }
            )
        )
    except Exception as err:
        print(dumps({'error': str(err)}))

        exit(1)

    exit(0)
