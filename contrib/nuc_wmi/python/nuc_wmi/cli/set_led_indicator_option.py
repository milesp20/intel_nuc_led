"""
`nuc_wmi.cli.set_led_indicator_option` provides a CLI interface to the WMI set led indicator function.
"""

from __future__ import print_function

from argparse import ArgumentParser
from json import dumps
from sys import exit

from nuc_wmi import CONTROL_FILE, LED_INDICATOR_OPTION, LED_TYPE
from nuc_wmi.set_led_indicator_option import set_led_indicator_option

def set_led_indicator_option_cli():
    """
    Creates a CLI interface ontop of the `nuc_wmi.set_led_indicator_option` `set_led_indicator_option` function.

    Args:
       led_indicator_option: The indicator option for the specified LED type for which to set the indicator option.
       led: Selects the LED to set the indicator option for.
    Options:
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
        args = parser.parse_args()

        set_led_indicator_option(
            LED_TYPE['new'].index(args.led),
            LED_INDICATOR_OPTION.index(args.led_indicator_option),
            control_file=args.control_file
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
    except Exception as err:
        print(dumps({'error': str(err)}))

        exit(1)

    exit(0)
