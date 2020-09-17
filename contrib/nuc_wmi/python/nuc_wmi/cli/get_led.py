"""
`nuc_wmi.cli.get_led` provides a CLI interface to the WMI get led state function.
"""

from __future__ import print_function

from argparse import ArgumentParser
from json import dumps
from sys import exit

from nuc_wmi import CONTROL_FILE, LED_COLOR, LED_COLOR_TYPE, LED_BLINK_FREQUENCY, LED_TYPE
from nuc_wmi.get_led import get_led

def get_led_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.get_led` `get_led` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       led: Selects the legacy LED to get the state for.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with brightness, frequency, and color of the selected LED or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the selected LED state properties or 1 on error.
    """

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
        'led',
        choices=[led for led in LED_TYPE['legacy'] if led],
        help='The legacy LED for which to get the state.'
    )

    try:
        args = parser.parse_args(args=cli_args)

        (brightness, frequency, color) = get_led(LED_TYPE['legacy'].index(args.led), control_file=args.control_file)

        print(
            dumps(
                {
                    'led': {
                        'type': args.led,
                        'brightness': str(brightness),
                        'frequency': LED_BLINK_FREQUENCY['legacy'][frequency],
                        'color': LED_COLOR['legacy'][LED_COLOR_TYPE['legacy'][args.led]][color]
                    }
                }
            )
        )
    except Exception as err:
        print(dumps({'error': str(err)}))

        exit(1)
