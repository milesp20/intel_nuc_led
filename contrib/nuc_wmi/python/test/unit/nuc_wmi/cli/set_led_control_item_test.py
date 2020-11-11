"""
The `test.unit.nuc_wmi.cli.set_led_control_item_test` module provides unit tests for the functions in
`nuc_wmi.cli.set_led_control_item`.

Classes:
    TestCliSetLedControlItem: A unit test class for the functions in `nuc_wmi.cli.set_led_control_item`.
"""

from __future__ import print_function

import json
import unittest

from mock import patch

from nuc_wmi import CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR, CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR
from nuc_wmi import LED_BLINK_FREQUENCY, LED_BRIGHTNESS_MULTI_COLOR, LED_COLOR, LED_COLOR_TYPE, LED_INDICATOR_OPTION
from nuc_wmi import LED_TYPE, NucWmiError
from nuc_wmi.cli.set_led_control_item import set_led_control_item_cli

import nuc_wmi


class TestCliSetLedControlItem(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.cli.set_led_control_item`

    Methods:
        setUp: Unit test initialization.
        test_set_led_control_item_cli: Tests that it returns the proper JSON response and exit code for
                                       valid cli args, tests that it captures raised errors and returns
                                       the proper JSON error response and exit code, tests that invalid
                                       indicator option or control items raises the proper error.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('nuc_wmi.cli.set_led_control_item.print')
    @patch('nuc_wmi.cli.set_led_control_item.sys.exit')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_color_type')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_control_items')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_indicator_options')
    @patch('nuc_wmi.cli.set_led_control_item.set_led_control_item')
    def test_set_led_control_item_cli( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_set_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `set_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_control_item.set_led_control_item is nuc_wmi_set_led_control_item)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_indicator_options is \
                        nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 1: Test that set_led_control_item_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Set HDD LED control item value of 37 for Brightness of HDD Activity Indicator
        led_brightness = 37
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        returned_set_led_control_item_cli = set_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[0]['Control Item'],
                str(led_brightness)
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_control_items.assert_not_called()

        nuc_wmi_set_led_control_item.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Brightness',
                    'Options': LED_BRIGHTNESS_MULTI_COLOR
                }
            ),
            led_brightness,
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[1],
                    'control_item': CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[0]['Control Item'],
                    'control_item_value': str(led_brightness)
                }
            }
        )

        self.assertEqual(returned_set_led_control_item_cli, None)


    @patch('nuc_wmi.cli.set_led_control_item.print')
    @patch('nuc_wmi.cli.set_led_control_item.sys.exit')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_color_type')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_control_items')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_indicator_options')
    @patch('nuc_wmi.cli.set_led_control_item.set_led_control_item')
    def test_set_led_control_item_cli2( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_set_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `set_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_control_item.set_led_control_item is nuc_wmi_set_led_control_item)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_indicator_options is \
                        nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 2: Test that set_led_control_item_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        led_brightness = 37
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        nuc_wmi_set_led_control_item.side_effect = NucWmiError('Error (Function not supported)')
        returned_set_led_control_item_cli = set_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[0]['Control Item'],
                str(led_brightness)
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_control_items.assert_not_called()

        nuc_wmi_set_led_control_item.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Brightness',
                    'Options': LED_BRIGHTNESS_MULTI_COLOR
                }
            ),
            led_brightness,
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_set_led_control_item_cli, None)


    @patch('nuc_wmi.cli.set_led_control_item.print')
    @patch('nuc_wmi.cli.set_led_control_item.sys.exit')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_color_type')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_control_items')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_indicator_options')
    @patch('nuc_wmi.cli.set_led_control_item.set_led_control_item')
    def test_set_led_control_item_cli3( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_set_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `set_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_control_item.set_led_control_item is nuc_wmi_set_led_control_item)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_indicator_options is \
                        nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 3: Test that set_led_control_item_cli raises proper error when an invalid indicator
        #           option for the current LED is chosen and returns he proper JSON error response and exit code.
        led_brightness = 37
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        returned_set_led_control_item_cli = set_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[2],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[0]['Control Item'],
                str(led_brightness)
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_control_items.assert_not_called()

        nuc_wmi_set_led_control_item.assert_not_called()
        nuc_wmi_print.assert_called_with('{"error": "Invalid indicator option for the selected LED"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_set_led_control_item_cli, None)


    @patch('nuc_wmi.cli.set_led_control_item.print')
    @patch('nuc_wmi.cli.set_led_control_item.sys.exit')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_color_type')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_control_items')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_indicator_options')
    @patch('nuc_wmi.cli.set_led_control_item.set_led_control_item')
    def test_set_led_control_item_cli4( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_set_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `set_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_control_item.set_led_control_item is nuc_wmi_set_led_control_item)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_indicator_options is \
                        nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 4: Test that set_led_control_item_cli raises proper error when there are no control items for
        #           for the current LED and indicator option chosen and returns he proper JSON error response and exit
        #           code.
        led_brightness = 37
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Single-color LED')
        nuc_wmi_query_led_indicator_options.return_value = [1, 4, 5]
        returned_set_led_control_item_cli = set_led_control_item_cli(
            [
                LED_TYPE['new'][0],
                LED_INDICATOR_OPTION[5],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[0]['Control Item'],
                str(led_brightness)
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('Power Button LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('Power Button LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_control_items.assert_not_called()

        nuc_wmi_set_led_control_item.assert_not_called()
        nuc_wmi_print.assert_called_with(
            '{"error": "No control items are available for the selected LED and indicator option"}'
        )
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_set_led_control_item_cli, None)


    @patch('nuc_wmi.cli.set_led_control_item.print')
    @patch('nuc_wmi.cli.set_led_control_item.sys.exit')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_color_type')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_control_items')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_indicator_options')
    @patch('nuc_wmi.cli.set_led_control_item.set_led_control_item')
    def test_set_led_control_item_cli5( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_set_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `set_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_control_item.set_led_control_item is nuc_wmi_set_led_control_item)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_indicator_options is \
                        nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 5: Test that set_led_control_item_cli raises proper error when an invalid control item for
        #           for the current LED and indicator option is chosen and returns the proper JSON error response and
        #           exit code.
        led_brightness = 37
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        returned_set_led_control_item_cli = set_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1],
                'Indication Scheme',
                str(led_brightness)
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_control_items.assert_not_called()

        nuc_wmi_set_led_control_item.assert_not_called()
        nuc_wmi_print.assert_called_with(
            '{"error": "Invalid control item specified for the selected LED and indicator option"}'
        )
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_set_led_control_item_cli, None)


    @patch('nuc_wmi.cli.set_led_control_item.print')
    @patch('nuc_wmi.cli.set_led_control_item.sys.exit')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_color_type')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_control_items')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_indicator_options')
    @patch('nuc_wmi.cli.set_led_control_item.set_led_control_item')
    def test_set_led_control_item_cli6( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_set_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `set_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_control_item.set_led_control_item is nuc_wmi_set_led_control_item)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_indicator_options is \
                        nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 6: Test setting control item that uses color

        # Set HDD LED control item to White for Color of HDD Activity Indicator
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        returned_set_led_control_item_cli = set_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[1]['Control Item'],
                LED_COLOR['new']['Dual-color Blue / White'][1]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_control_items.assert_not_called()

        nuc_wmi_set_led_control_item.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Color',
                    'Options': LED_COLOR['new']
                }
            ),
            LED_COLOR['new']['Dual-color Blue / White'].index('White'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[1],
                    'control_item': CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[1]['Control Item'],
                    'control_item_value': LED_COLOR['new']['Dual-color Blue / White'][1]
                }
            }
        )

        self.assertEqual(returned_set_led_control_item_cli, None)


    @patch('nuc_wmi.cli.set_led_control_item.print')
    @patch('nuc_wmi.cli.set_led_control_item.sys.exit')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_color_type')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_control_items')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_indicator_options')
    @patch('nuc_wmi.cli.set_led_control_item.set_led_control_item')
    def test_set_led_control_item_cli7( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_set_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `set_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_control_item.set_led_control_item is nuc_wmi_set_led_control_item)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_indicator_options is \
                        nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 7: Test setting control item that uses wrong color raises proper error

        # Set HDD LED control item to wrong color Amber for Color of HDD Activity Indicator
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        returned_set_led_control_item_cli = set_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[1]['Control Item'],
                'Amber'
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_control_items.assert_not_called()

        nuc_wmi_set_led_control_item.assert_not_called()
        nuc_wmi_print.assert_called_with(
            '{"error": "Invalid control item value for the specified control item"}'
        )
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_set_led_control_item_cli, None)


    @patch('nuc_wmi.cli.set_led_control_item.print')
    @patch('nuc_wmi.cli.set_led_control_item.sys.exit')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_color_type')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_control_items')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_indicator_options')
    @patch('nuc_wmi.cli.set_led_control_item.set_led_control_item')
    def test_set_led_control_item_cli8( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_set_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `set_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_control_item.set_led_control_item is nuc_wmi_set_led_control_item)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_indicator_options is \
                        nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 8: Test setting control item that uses color

        # Set HDD LED control item to Indigo for Color of HDD Activity Indicator with 1d RGB-color LED type
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('RGB-color')
        nuc_wmi_query_led_control_items.return_value = [0, 1, 4]
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        returned_set_led_control_item_cli = set_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[1]['Control Item'],
                LED_COLOR['new']['RGB-color']['1d']['HDD LED'][6]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_control_items.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            control_file=None,
            debug=False,
            quirks=None
        )

        nuc_wmi_set_led_control_item.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Color',
                    'Options': LED_COLOR['new']
                }
            ),
            LED_COLOR['new']['RGB-color']['1d']['HDD LED'].index('Indigo'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[1],
                    'control_item': CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[1]['Control Item'],
                    'control_item_value': LED_COLOR['new']['RGB-color']['1d']['HDD LED'][6]
                }
            }
        )

        self.assertEqual(returned_set_led_control_item_cli, None)


    @patch('nuc_wmi.cli.set_led_control_item.print')
    @patch('nuc_wmi.cli.set_led_control_item.sys.exit')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_color_type')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_control_items')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_indicator_options')
    @patch('nuc_wmi.cli.set_led_control_item.set_led_control_item')
    def test_set_led_control_item_cli9( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_set_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `set_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_control_item.set_led_control_item is nuc_wmi_set_led_control_item)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_indicator_options is \
                        nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 9: Test setting control item that uses color

        # Set HDD LED control item to 100 for Color of HDD Activity Indicator with 3d RGB-color LED type
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('RGB-color')
        nuc_wmi_query_led_control_items.return_value = [0, 1, 2, 3, 4]
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        returned_set_led_control_item_cli = set_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[1]['Control Item'],
                LED_COLOR['new']['RGB-color']['3d'][100]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_control_items.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            control_file=None,
            debug=False,
            quirks=None
        )

        nuc_wmi_set_led_control_item.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Color',
                    'Options': LED_COLOR['new']
                }
            ),
            LED_COLOR['new']['RGB-color']['3d'].index('100'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[1],
                    'control_item': CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[1]['Control Item'],
                    'control_item_value': LED_COLOR['new']['RGB-color']['3d'][100]
                }
            }
        )

        self.assertEqual(returned_set_led_control_item_cli, None)


    @patch('nuc_wmi.cli.set_led_control_item.print')
    @patch('nuc_wmi.cli.set_led_control_item.sys.exit')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_color_type')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_control_items')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_indicator_options')
    @patch('nuc_wmi.cli.set_led_control_item.set_led_control_item')
    def test_set_led_control_item_cli10( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_set_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `set_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_control_item.set_led_control_item is nuc_wmi_set_led_control_item)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_indicator_options is \
                        nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 10: Test setting control item that uses color

        # Set HDD LED control item to Indigo for Color of Software Indicator with 1d RGB-color LED type
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('RGB-color')
        nuc_wmi_query_led_control_items.return_value = [0, 1, 2, 3]
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        returned_set_led_control_item_cli = set_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[4],
                CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR[3]['Control Item'],
                LED_COLOR['new']['RGB-color']['1d']['HDD LED'][6]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_control_items.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('Software Indicator'),
            control_file=None,
            debug=False,
            quirks=None
        )

        nuc_wmi_set_led_control_item.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('Software Indicator'),
            CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Color',
                    'Options': LED_COLOR['new']
                }
            ),
            LED_COLOR['new']['RGB-color']['1d']['HDD LED'].index('Indigo'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[4],
                    'control_item': CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR[3]['Control Item'],
                    'control_item_value': LED_COLOR['new']['RGB-color']['1d']['HDD LED'][6]
                }
            }
        )

        self.assertEqual(returned_set_led_control_item_cli, None)


    @patch('nuc_wmi.cli.set_led_control_item.print')
    @patch('nuc_wmi.cli.set_led_control_item.sys.exit')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_color_type')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_control_items')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_indicator_options')
    @patch('nuc_wmi.cli.set_led_control_item.set_led_control_item')
    def test_set_led_control_item_cli11( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_set_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `set_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_control_item.set_led_control_item is nuc_wmi_set_led_control_item)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_indicator_options is \
                        nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 11: Test setting control item that uses color

        # Set HDD LED control item to 100 for Color of Software Indicator with 3d RGB-color LED type
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('RGB-color')
        nuc_wmi_query_led_control_items.return_value = [0, 1, 2, 3, 4, 5]
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        returned_set_led_control_item_cli = set_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[4],
                CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR[3]['Control Item'],
                LED_COLOR['new']['RGB-color']['3d'][100]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_control_items.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('Software Indicator'),
            control_file=None,
            debug=False,
            quirks=None
        )

        nuc_wmi_set_led_control_item.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('Software Indicator'),
            CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Color',
                    'Options': LED_COLOR['new']
                }
            ),
            LED_COLOR['new']['RGB-color']['3d'].index('100'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[4],
                    'control_item': CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR[3]['Control Item'],
                    'control_item_value': LED_COLOR['new']['RGB-color']['3d'][100]
                }
            }
        )

        self.assertEqual(returned_set_led_control_item_cli, None)


    @patch('nuc_wmi.cli.set_led_control_item.print')
    @patch('nuc_wmi.cli.set_led_control_item.sys.exit')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_color_type')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_control_items')
    @patch('nuc_wmi.cli.set_led_control_item.query_led_indicator_options')
    @patch('nuc_wmi.cli.set_led_control_item.set_led_control_item')
    def test_set_led_control_item_cli12( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_set_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `set_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.set_led_control_item.set_led_control_item is nuc_wmi_set_led_control_item)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_indicator_options is \
                        nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.set_led_control_item.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 12: Test setting control item that uses blinking frequency

        # Set HDD LED control item to 1.0Hz for Blinking Frequency of Software Indicator with 3d RGB-color LED type
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('RGB-color')
        nuc_wmi_query_led_control_items.return_value = [0, 1, 2, 3, 4, 5]
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        returned_set_led_control_item_cli = set_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[4],
                CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR[2]['Control Item'],
                LED_BLINK_FREQUENCY['new'][10]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_query_led_control_items.assert_not_called()

        nuc_wmi_set_led_control_item.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('Software Indicator'),
            CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Blinking Frequency',
                    'Options': LED_BLINK_FREQUENCY['new']
                }
            ),
            LED_BLINK_FREQUENCY['new'].index('1.0Hz'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[4],
                    'control_item': CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR[2]['Control Item'],
                    'control_item_value': LED_BLINK_FREQUENCY['new'][10]
                }
            }
        )

        self.assertEqual(returned_set_led_control_item_cli, None)
