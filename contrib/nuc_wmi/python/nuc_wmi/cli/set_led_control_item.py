"""
`nuc_wmi.cli.set_led_control_item` provides a CLI interface to the WMI set control item function.
"""

from __future__ import print_function

from argparse import ArgumentParser
from json import dumps
from sys import exit

from nuc_wmi import CONTROL_ITEM, CONTROL_FILE, LED_COLOR, LED_COLOR_TYPE, LED_INDICATOR_OPTION, LED_TYPE
from nuc_wmi.query_led import query_led_color_type, query_led_indicator_options
from nuc_wmi.set_led_control_item import set_led_control_item

def set_led_control_item_cli(cli_args=None):
    """
    Creates a CLI interface on top of the `nuc_wmi.set_led_control` `set_led_control_item` function.

    Args:
       cli_args: If provided, overrides the CLI args to use for `argparse`.
    CLI Args:
       control_item: The control item of the specified LED type indicator option for which to set the value.
       control_item_value: The value for the control item to set.
       led_indicator_option: The indicator option for the specified LED type for which to set the control
                            item value.
       led: Selects the LED to set the control item for.
    CLI Options:
       --control_file <control_file>: Sets the control file to use if provided,
                                      otherwise `nuc_wmi.CONTROL_FILE` is used.
    Outputs:
       stdout: JSON object with control item value for the control item of the indicator option for the selected LED or
               error message with failure error.
    Exit code:
       0 on successfully setting the control item value or 1 on error.
    """

    control_item_labels = list()
    control_item_values = list()

    for indicator_option in CONTROL_ITEM:
        if indicator_option is None:
            continue

        for control_items in indicator_option:
            if control_items is None:
                continue

            for control_item in control_items:
                control_item_labels.append(control_item['Control Item'])

                if control_item['Options'] is not None and control_item['Options'] != LED_COLOR['new']:
                    control_item_values.extend(control_item['Options'])

    control_item_values.extend(LED_COLOR['new']['Dual-color Blue / Amber'])
    control_item_values.extend(LED_COLOR['new']['Dual-color Blue / White'])

    parser = ArgumentParser(
        description='Set the control item value for the control item of the indicator option ' + \
        'for the specified LED type.'
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
        help='The LED for which to set the control item value.'
    )
    parser.add_argument(
        'led_indicator_option',
        choices=LED_INDICATOR_OPTION,
        help='The LED indicator option for the LED.'
    )
    parser.add_argument(
        'control_item',
        choices=set(control_item_labels),
        help='The control item for the LED indicator option that is being set.'
    )
    parser.add_argument(
        'control_item_value',
        choices=set(control_item_values),
        help='The control item value for the control item for the LED indicator option that is being set.'
    )

    try:
        args = parser.parse_args(args=cli_args)

        available_indicator_options = query_led_indicator_options(
            LED_TYPE['new'].index(args.led),
            control_file=args.control_file
        )

        led_color_type = query_led_color_type(
            LED_TYPE['new'].index(args.led),
            control_file=args.control_file
        )

        indicator = LED_INDICATOR_OPTION.index(args.led_indicator_option)

        if indicator not in available_indicator_options:
            raise ValueError('Invalid indicator option for the selected LED')

        control_items = CONTROL_ITEM[indicator][led_color_type]

        if control_items is None:
            raise ValueError('No control items are available for the selected LED and indicator option')

        control_item_index = None

        for index, control_item in enumerate(control_items):
            if control_item['Control Item'] == args.control_item:
                control_item_index = index

        if control_item_index is None:
            raise ValueError('Invalid control item specified for the selected LED and indicator option')

        try:
            # Convert the control item value into its index
            if control_items[control_item_index]['Options'] == LED_COLOR['new']:
                control_item_value_index = control_items[control_item_index]['Options'][LED_COLOR_TYPE['new'][led_color_type]].index(args.control_item_value)
            else:
                control_item_value_index = control_items[control_item_index]['Options'].index(args.control_item_value)
        except ValueError as err:
            raise ValueError('Invalid control item value for the specified control item')

        set_led_control_item(
            LED_TYPE['new'].index(args.led),
            indicator,
            control_item_index,
            control_item_value_index,
            control_file=args.control_file
        )

        print(
            dumps(
                {
                    'led': {
                        'type': args.led,
                        'indicator_option': args.led_indicator_option,
                        'control_item': args.control_item,
                        'control_item_value': args.control_item_value
                    }
                }
            )
        )
    except Exception as err:
        print(dumps({'error': str(err)}))

        exit(1)
