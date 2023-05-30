"""
`nuc_wmi.cli.set_led_indicator_option` provides a CLI interface to the WMI set led indicator function.
"""

from __future__ import print_function

import sys

from argparse import ArgumentParser
from json import dumps

from nuc_wmi import CONTROL_FILE, LED_INDICATOR_OPTION, LED_TYPE, LOCK_FILE
from nuc_wmi.set_led_indicator_option import set_led_indicator_option
from nuc_wmi.utils import acquire_file_lock, load_nuc_wmi_spec


def set_led_indicator_option_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.set_led_indicator_option` `set_led_indicator_option` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       led_indicator_option: The indicator option for the specified LED type for which to set the indicator option.
       led: Selects the LED to set the indicator option for.
       nuc_wmi_spec_alias: Selects the NUC WMI specification to use from the NUC WMI specification configuration file.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with the set indicator option of the selected LED or error message with
               failure error.
    Exit code:
       0 on successfully setting the selected LED's indicator option or 1 on error.
    """

    try:
        nuc_wmi_spec = load_nuc_wmi_spec()

        parser = ArgumentParser(
            description='Set the LED indicator option for the specified LED type,'
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
            help='The LED for which to set the indicator option.'
        )
        parser.add_argument(
            'led_indicator_option',
            choices=LED_INDICATOR_OPTION,
            help='The LED indicator option to set for the LED.'
        )

        args = parser.parse_args(args=cli_args)

        with open(args.lock_file or LOCK_FILE, 'w', encoding='utf8') as lock_file:
            acquire_file_lock(lock_file, blocking_file_lock=args.blocking_file_lock)

            led_type_index = LED_TYPE['new'].index(args.led)

            led_indicator_option_index = LED_INDICATOR_OPTION.index(args.led_indicator_option)

            set_led_indicator_option(
                nuc_wmi_spec['nuc_wmi_spec'].get(args.nuc_wmi_spec_alias),
                led_type_index,
                led_indicator_option_index,
                control_file=args.control_file,
                debug=args.debug,
                metadata=None
            )

            print(
                dumps(
                    {
                        'led': {
                            'type': args.led,
                            'indicator_option': args.led_indicator_option
                        },
                        'nuc_wmi_spec_alias': args.nuc_wmi_spec_alias
                    }
                )
            )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)
