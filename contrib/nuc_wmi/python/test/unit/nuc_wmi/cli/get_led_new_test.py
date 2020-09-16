"""
The `test.unit.nuc_wmi.cli.get_led_new_test` module provides unit tests for the functions in
`nuc_wmi.cli.get_led_new`.

Classes:
    TestCliGetLedNew: A unit test class for the functions in `nuc_wmi.cli.get_led_new`.
"""

from __future__ import print_function

import json
import unittest

from mock import MagicMock, patch

from nuc_wmi import CONTROL_ITEM, CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR, LED_BRIGHTNESS_MULTI_COLOR
from nuc_wmi import LED_COLOR, LED_COLOR_TYPE, LED_INDICATOR_OPTION, LED_TYPE, NucWmiError
from nuc_wmi.cli.get_led_new import get_led_control_item_cli, get_led_indicator_option_cli

import nuc_wmi


class TestCliGetLedNew(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.cli.get_led_new`

    Methods:
        setUp: Unit test initialization.
        test_get_led_control_item_cli: Tests that it returns the proper JSON response and exit code for
                                       valid cli args, tests that it captures raised errors and returns
                                       the proper JSON error response and exit code, tests that invalid
                                       indicator option or control items raises the proper error.
        test_get_led_indicator_option_cli: Tests that it returns the proper JSON response and exit code for
                                           valid cli args, tests that it captures raised errors and returns
                                           the proper JSON error response and exit code.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None


    @patch('nuc_wmi.cli.get_led_new.print')
    @patch('nuc_wmi.cli.get_led_new.exit')
    @patch('nuc_wmi.cli.get_led_new.query_led_color_type')
    @patch('nuc_wmi.cli.get_led_new.query_led_indicator_options')
    @patch('nuc_wmi.cli.get_led_new.get_led_control_item')
    def test_get_led_control_item_cli(
            self,
            nuc_wmi_get_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `get_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.get_led_new.get_led_control_item is nuc_wmi_get_led_control_item)
        self.assertTrue(nuc_wmi.cli.get_led_new.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.get_led_new.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.get_led_new.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.get_led_new.print is nuc_wmi_print)

        # Branch 1: Test that get_led_control_item_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Get HDD LED control item value of 37 for Brightness of HDD Activity Indicator
        expected_brightness = 0x37
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [0x01, 0x04]
        nuc_wmi_get_led_control_item.return_value = expected_brightness
        returned_get_led_control_item_cli = get_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[0]['Control Item']
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None
        )

        nuc_wmi_get_led_control_item.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Brightness',
                    'Options': LED_BRIGHTNESS_MULTI_COLOR
                }
            ),
            control_file=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[1],
                    'control_item': CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[0]['Control Item'],
                    'control_item_value': str(expected_brightness)
                }
            }
        )

        self.assertEqual(returned_get_led_control_item_cli, None)

        # Reset
        nuc_wmi_query_led_color_type.reset_mock()
        nuc_wmi_query_led_indicator_options.reset_mock()
        nuc_wmi_get_led_control_item.reset_mock()
        nuc_wmi_sys_exit.reset_mock()
        nuc_wmi_print.reset_mock()

        # Branch 2: Test that get_led_control_item_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [0x01, 0x04]
        nuc_wmi_get_led_control_item.side_effect = NucWmiError('Error (Function not supported)')
        returned_get_led_control_item_cli = get_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[0]['Control Item']
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None
        )

        nuc_wmi_get_led_control_item.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Brightness',
                    'Options': LED_BRIGHTNESS_MULTI_COLOR
                }
            ),
            control_file=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_get_led_control_item_cli, None)

        # Reset
        nuc_wmi_query_led_color_type.reset_mock()
        nuc_wmi_query_led_indicator_options.reset_mock()
        nuc_wmi_sys_exit.reset_mock()
        nuc_wmi_print.reset_mock()

        nuc_wmi_get_led_control_item = MagicMock()

        # Branch 3: Test that get_led_control_item_cli raises proper error when an invalid indicator
        #           option for the current LED is chosen and returns he proper JSON error response and exit code.
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [0x01, 0x04]
        returned_get_led_control_item_cli = get_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[2],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[0]['Control Item']
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None
        )

        nuc_wmi_get_led_control_item.assert_not_called()
        nuc_wmi_print.assert_called_with('{"error": "Invalid indicator option for the selected LED"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_get_led_control_item_cli, None)

        # Reset
        nuc_wmi_query_led_color_type.reset_mock()
        nuc_wmi_query_led_indicator_options.reset_mock()
        nuc_wmi_get_led_control_item.reset_mock()
        nuc_wmi_sys_exit.reset_mock()
        nuc_wmi_print.reset_mock()

        # Branch 4: Test that get_led_control_item_cli raises proper error when there are no control items for
        #           for the current LED and indicator option chosen and returns he proper JSON error response and exit
        #           code.
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Single-color LED')
        nuc_wmi_query_led_indicator_options.return_value = [0x01, 0x04, 0x05]
        returned_get_led_control_item_cli = get_led_control_item_cli(
            [
                LED_TYPE['new'][0],
                LED_INDICATOR_OPTION[5],
                'Brightness'
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('Power Button LED'),
            control_file=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('Power Button LED'),
            control_file=None
        )

        nuc_wmi_get_led_control_item.assert_not_called()
        nuc_wmi_print.assert_called_with(
            '{"error": "No control items are available for the selected LED and indicator option"}'
        )
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_get_led_control_item_cli, None)

        # Reset
        nuc_wmi_query_led_color_type.reset_mock()
        nuc_wmi_query_led_indicator_options.reset_mock()
        nuc_wmi_get_led_control_item.reset_mock()
        nuc_wmi_sys_exit.reset_mock()
        nuc_wmi_print.reset_mock()

        # Branch 5: Test that get_led_control_item_cli raises proper error when an invalid control item for
        #           for the current LED and indicator option is chosen and returns he proper JSON error response and
        #           exit code.
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [0x01, 0x04]
        returned_get_led_control_item_cli = get_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1],
                'Indication Scheme'
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None
        )

        nuc_wmi_get_led_control_item.assert_not_called()
        nuc_wmi_print.assert_called_with(
            '{"error": "Invalid control item specified for the selected LED and indicator option"}'
        )
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_get_led_control_item_cli, None)


    @patch('nuc_wmi.cli.get_led_new.print')
    @patch('nuc_wmi.cli.get_led_new.exit')
    @patch('nuc_wmi.cli.get_led_new.query_led_color_type')
    @patch('nuc_wmi.cli.get_led_new.query_led_indicator_options')
    @patch('nuc_wmi.cli.get_led_new.get_led_control_item')
    def test_get_led_control_item_cli2(
            self,
            nuc_wmi_get_led_control_item,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `get_led_control_item_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.get_led_new.get_led_control_item is nuc_wmi_get_led_control_item)
        self.assertTrue(nuc_wmi.cli.get_led_new.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.get_led_new.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.get_led_new.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.get_led_new.print is nuc_wmi_print)

        # Branch 6: Test getting control item that uses color

        # Get HDD LED control item color of White for Color of HDD Activity Indicator
        expected_color = LED_COLOR['new']['Dual-color Blue / White'].index('White')
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [0x01, 0x04]
        nuc_wmi_get_led_control_item.return_value = expected_color
        returned_get_led_control_item_cli = get_led_control_item_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1],
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[1]['Control Item']
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None
        )

        nuc_wmi_get_led_control_item.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Color',
                    'Options': LED_COLOR['new']
                }
            ),
            control_file=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[1],
                    'control_item': CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[1]['Control Item'],
                    'control_item_value': LED_COLOR['new']['Dual-color Blue / White'][expected_color]
                }
            }
        )

        self.assertEqual(returned_get_led_control_item_cli, None)


    @patch('nuc_wmi.cli.get_led_new.print')
    @patch('nuc_wmi.cli.get_led_new.exit')
    @patch('nuc_wmi.cli.get_led_new.get_led_indicator_option')
    def test_get_led_indicator_option_cli(
            self,
            nuc_wmi_get_led_indicator_option,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `get_led_indicator_option_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.get_led_new.get_led_indicator_option is nuc_wmi_get_led_indicator_option)
        self.assertTrue(nuc_wmi.cli.get_led_new.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.get_led_new.print is nuc_wmi_print)

        # Branch 1: Test that get_led_indicator_option_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Get HDD LED indicator option of HDD Activity Indicator
        expected_led_indicator = 0x01
        nuc_wmi_get_led_indicator_option.return_value = expected_led_indicator
        returned_get_led_indicator_option_cli = get_led_indicator_option_cli(
            [
                LED_TYPE['new'][1]
            ]
        )

        nuc_wmi_get_led_indicator_option.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[expected_led_indicator]
                }
            }
        )

        self.assertEqual(returned_get_led_indicator_option_cli, None)

        # Reset
        nuc_wmi_get_led_indicator_option.reset_mock()
        nuc_wmi_sys_exit.reset_mock()
        nuc_wmi_print.reset_mock()

        # Branch 2: Test that get_led_indicator_option_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_get_led_indicator_option.side_effect = NucWmiError('Error (Function not supported)')

        returned_get_led_indicator_option_cli = get_led_indicator_option_cli(
            [
                LED_TYPE['new'][1]
            ]
        )

        nuc_wmi_get_led_indicator_option.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_get_led_indicator_option_cli, None)
