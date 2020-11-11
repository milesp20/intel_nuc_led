"""
`nuc_wmi.cli.get_led_new` provides a CLI interface to the WMI get led set of functions.
"""

from __future__ import print_function

import sys

from argparse import ArgumentParser
from json import dumps

from nuc_wmi import CONTROL_ITEM, CONTROL_FILE, LED_COLOR, LED_COLOR_TYPE, LED_INDICATOR_OPTION, LED_TYPE
from nuc_wmi.get_led_new import get_led_control_item, get_led_indicator_option
from nuc_wmi.query_led import query_led_color_type, query_led_control_items, query_led_indicator_options

import nuc_wmi

RGB_COLOR_1D = LED_COLOR['new']['RGB-color']['1d']
RGB_COLOR_3D = LED_COLOR['new']['RGB-color']['3d']

def get_led_control_item_cli(cli_args=None): # pylint: disable=too-many-branches,too-many-locals,too-many-statements
    """
    Creates a CLI interface on top of the `nuc_wmi.get_led_new` `get_led_control_item` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       control_item: The control item of the specified LED type indicator option for which to retrieve the value.
       led_indicator_option: The indicator option for the specified LED type for which to retrieve the current control
                            item value.
       led: Selects the LED to get the control item for.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with control item value for the control item of the indicator option for the selected LED or
               error message with failure error.
    Exit code:
       0 on successfully retrieving the control item value or 1 on error.
    """

    control_item_labels = list()

    for indicator_option in CONTROL_ITEM:
        if indicator_option is None:
            continue

        for control_items in indicator_option:
            if control_items is None:
                continue

            for control_item in control_items:
                control_item_labels.append(control_item['Control Item'])

    parser = ArgumentParser(
        description='Get the current control item value for the control item of the indicator option ' + \
        'for the specified LED type.'
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
        help='The LED for which to get the control item value.'
    )
    parser.add_argument(
        'led_indicator_option',
        choices=LED_INDICATOR_OPTION,
        help='The LED indicator option for the current LED.'
    )
    parser.add_argument(
        'control_item',
        choices=set(control_item_labels),
        help='The control item for the current LED indicator option that is being retrieved.'
    )

    try:
        args = parser.parse_args(args=cli_args)

        led_type_index = LED_TYPE['new'].index(args.led)

        available_indicator_options = query_led_indicator_options(
            led_type_index,
            control_file=args.control_file,
            debug=args.debug,
            quirks=args.quirks
        )

        led_color_type_index = query_led_color_type(
            led_type_index,
            control_file=args.control_file,
            debug=args.debug,
            quirks=args.quirks
        )

        led_color_type = LED_COLOR_TYPE['new'][led_color_type_index]

        led_indicator_option_index = LED_INDICATOR_OPTION.index(args.led_indicator_option)

        if led_indicator_option_index not in available_indicator_options:
            raise ValueError('Invalid indicator option for the selected LED')

        control_items = CONTROL_ITEM[led_indicator_option_index][led_color_type_index]

        if control_items is None:
            raise ValueError('No control items are available for the selected LED and indicator option')

        control_item_index = None

        for index, control_item in enumerate(control_items):
            if control_item['Control Item'] == args.control_item:
                control_item_index = index

        if control_item_index is None:
            raise ValueError('Invalid control item specified for the selected LED and indicator option')

        control_item_value = get_led_control_item(
            led_type_index,
            led_indicator_option_index,
            control_item_index,
            control_file=args.control_file,
            debug=args.debug,
            quirks=args.quirks
        )

        # Convert the control item value index into its value
        if control_items[control_item_index]['Options'] == LED_COLOR['new']:
            if led_color_type == 'RGB-color':
                color_dimensions = '1d'

                available_control_item_indexes = query_led_control_items(
                    led_type_index,
                    led_indicator_option_index,
                    control_file=args.control_file,
                    debug=args.debug,
                    quirks=args.quirks
                )

                for control_item_index2 in available_control_item_indexes:
                    if control_items[control_item_index2]['Options'] == RGB_COLOR_3D:
                        color_dimensions = '3d'

                        break

                if color_dimensions == '1d':
                    led_colors = RGB_COLOR_1D[args.led]
                else:
                    led_colors = RGB_COLOR_3D

                control_item_value = led_colors[control_item_value]
            else:
                control_item_value = LED_COLOR['new'][led_color_type][control_item_value]
        else:
            control_item_value = control_items[control_item_index]['Options'][control_item_value]

        print(
            dumps(
                {
                    'led': {
                        'type': args.led,
                        'indicator_option': args.led_indicator_option,
                        'control_item': args.control_item,
                        'control_item_value': control_item_value
                    }
                }
            )
        )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)


def get_led_indicator_option_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.get_led_new` `get_led_indicator_option` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       led: Selects the LED to get the indicator option for.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with indicator option of the selected LED or error message with
               failure error.
    Exit code:
       0 on successfully retrieving the selected LED's indicator option or 1 on error.
    """

    parser = ArgumentParser(
        description='Get the current indicator option for the LED type.'
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
        help='The LED for which to get the indicator option.'
    )

    try:
        args = parser.parse_args(args=cli_args)

        led_type_index = LED_TYPE['new'].index(args.led)

        led_indicator_option_index = get_led_indicator_option(
            led_type_index,
            control_file=args.control_file,
            debug=args.debug,
            quirks=args.quirks
        )

        led_indicator_option = LED_INDICATOR_OPTION[led_indicator_option_index]

        print(
            dumps(
                {
                    'led': {
                        'type': args.led,
                        'indicator_option': led_indicator_option
                    }
                }
            )
        )
    except Exception as err: # pylint: disable=broad-except
        print(dumps({'error': str(err)}))

        sys.exit(1)
