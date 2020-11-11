"""
The `test.unit.nuc_wmi.cli.query_led_test` module provides unit tests for the functions in
`nuc_wmi.cli.query_led`.

Classes:
    TestCliQueryLed: A unit test class for the functions in `nuc_wmi.cli.query_led`.
"""

from __future__ import print_function

import json
import unittest

from mock import patch

from nuc_wmi import CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR, LED_COLOR_TYPE, LED_INDICATOR_OPTION
from nuc_wmi import LED_TYPE, NucWmiError
from nuc_wmi.cli.query_led import query_led_color_type_cli, query_led_control_items_cli
from nuc_wmi.cli.query_led import query_led_indicator_options_cli, query_leds_cli

import nuc_wmi


class TestCliQueryLed(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.cli.query_led`

    Methods:
        setUp: Unit test initialization.
        test_query_led_color_type_cli: Tests that it returns the proper JSON response and exit code for
                                       valid cli args, tests that it captures raised errors and returns
                                       the proper JSON error response and exit code, tests that invalid
                                       LED color raises appropriate error.
        test_query_led_control_items_cli: Tests that it returns the proper JSON response and exit code for
                                          valid cli args, tests that it captures raised errors and returns
                                          the proper JSON error response and exit code, tests that invalid
                                          LED color raises appropriate error.
        test_query_led_indicator_options_cli: Tests that it returns the proper JSON response and exit code for
                                              valid cli args, tests that it captures raised errors and returns
                                              the proper JSON error response and exit code, tests that invalid
                                              LED color raises appropriate error.
        test_query_leds_cli: Tests that it returns the proper JSON response and exit code for
                             valid cli args, tests that it captures raised errors and returns
                             the proper JSON error response and exit code, tests that invalid
                             LED color raises appropriate error.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name

    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    def test_query_led_color_type_cli(
            self,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `query_led_color_type_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 1: Test that query_led_color_type_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Return HDD LED color type of Dual-color Blue / White
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        returned_query_led_color_type_cli = query_led_color_type_cli(
            [
                LED_TYPE['new'][1]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
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
                    'color_type': LED_COLOR_TYPE['new'][1]
                }
            }
        )

        self.assertEqual(returned_query_led_color_type_cli, None)


    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    def test_query_led_color_type_cli2(
            self,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `query_led_color_type_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 2: Test that query_led_color_type_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_query_led_color_type.side_effect = NucWmiError('Error (Function not supported)')

        returned_query_led_color_type_cli = query_led_color_type_cli(
            [
                LED_TYPE['new'][1]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_color_type_cli, None)


    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    def test_query_led_color_type_cli3(
            self,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `query_led_color_type_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 3: Test that query_led_color_type_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Return HDD LED color type of Single-color LED
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Single-color LED')
        returned_query_led_color_type_cli = query_led_color_type_cli(
            [
                LED_TYPE['new'][1]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
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
                    'color_type': LED_COLOR_TYPE['new'][3]
                }
            }
        )

        self.assertEqual(returned_query_led_color_type_cli, None)


    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    @patch('nuc_wmi.cli.query_led.query_led_indicator_options')
    @patch('nuc_wmi.cli.query_led.query_led_control_items')
    def test_query_led_control_items_cli( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `query_led_control_items_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 1: Test that query_led_control_items_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Get control items for HDD LED set to HDD Activity Indicator
        expected_control_items = [0, 1, 2, 3]
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        nuc_wmi_query_led_control_items.return_value = expected_control_items
        returned_query_led_control_items_cli = query_led_control_items_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1]
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
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[1],
                    'control_items': [CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[control_item]['Control Item'] \
                                      for control_item in expected_control_items]
                }
            }
        )

        self.assertEqual(returned_query_led_control_items_cli, None)


    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    @patch('nuc_wmi.cli.query_led.query_led_indicator_options')
    @patch('nuc_wmi.cli.query_led.query_led_control_items')
    def test_query_led_control_items_cli2( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `query_led_control_items_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 2: Test that query_led_control_items_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]
        nuc_wmi_query_led_control_items.side_effect = NucWmiError('Error (Function not supported)')
        returned_query_led_control_items_cli = query_led_control_items_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1]
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
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_control_items_cli, None)


    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    @patch('nuc_wmi.cli.query_led.query_led_indicator_options')
    @patch('nuc_wmi.cli.query_led.query_led_control_items')
    def test_query_led_control_items_cli3( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_color_type,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `query_led_control_items_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 3: Tests that invalid LED indicator raises appropriate error.
        expected_control_items = [0, 1, 2, 3]
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_indicator_options.return_value = []
        nuc_wmi_query_led_control_items.return_value = expected_control_items
        returned_query_led_control_items_cli = query_led_control_items_cli(
            [
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1]
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
        nuc_wmi_print.assert_called_with('{"error": "Invalid indicator option for the selected LED"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_control_items_cli, None)


    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    @patch('nuc_wmi.cli.query_led.query_led_indicator_options')
    def test_query_led_indicator_options_cli(
            self,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `query_led_indicator_options_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 1: Test that query_led_indicator_options_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Return HDD LED indicator options of HDD Activity Indicator and Software Indicator
        expected_indicator_options = [1, 4]
        nuc_wmi_query_led_indicator_options.return_value = expected_indicator_options
        returned_query_led_indicator_options_cli = query_led_indicator_options_cli(
            [
                LED_TYPE['new'][1]
            ]
        )

        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
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
                    'indicator_options': [LED_INDICATOR_OPTION[indicator] for indicator in expected_indicator_options]
                }
            }
        )

        self.assertEqual(returned_query_led_indicator_options_cli, None)


    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    @patch('nuc_wmi.cli.query_led.query_led_indicator_options')
    def test_query_led_indicator_options_cli2(
            self,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `query_led_indicator_options_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 2: Test that query_led_indicator_options_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_query_led_indicator_options.side_effect = NucWmiError('Error (Function not supported)')

        returned_query_led_indicator_options_cli = query_led_indicator_options_cli(
            [
                LED_TYPE['new'][1]
            ]
        )

        nuc_wmi_query_led_indicator_options.assert_called_with(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_indicator_options_cli, None)


    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    @patch('nuc_wmi.cli.query_led.query_leds')
    def test_query_leds_cli(
            self,
            nuc_wmi_query_leds,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `query_leds_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.query_leds is nuc_wmi_query_leds)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 1: Test that query_leds_cli returns the proper JSON response and exit
        #           code for valid cli args
        expected_leds = [0, 1]
        nuc_wmi_query_leds.return_value = expected_leds
        returned_query_leds_cli = query_leds_cli([])

        nuc_wmi_query_leds.assert_called_with(
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'leds': [LED_TYPE['new'][led] for led in expected_leds]
            }
        )

        self.assertEqual(returned_query_leds_cli, None)


    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    @patch('nuc_wmi.cli.query_led.query_leds')
    def test_query_leds_cli2(
            self,
            nuc_wmi_query_leds,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `query_leds_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.query_leds is nuc_wmi_query_leds)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 2: Test that query_leds_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_query_leds.side_effect = NucWmiError('Error (Function not supported)')

        returned_query_leds_cli = query_leds_cli([])

        nuc_wmi_query_leds.assert_called_with(
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_leds_cli, None)
