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

        self.nuc_wmi_spec = {
            'nuc_wmi_spec': {
                'TEST_DEVICE': {
                    'function_return_type': {
                        'query_led_color_type': 'bitmap',
                        'query_led_control_items': 'bitmap',
                        'query_led_indicator_options': 'bitmap',
                        'query_leds': 'bitmap'
                    },
                    'function_oob_return_value_recover': {
                        'query_led_color_type': False,
                        'query_led_control_items': False,
                        'query_led_indicator_options': False,
                        'query_leds': False
                    }
                }
            }
        }


    @patch('nuc_wmi.cli.query_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    def test_query_led_color_type_cli(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_query_led_color_type,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `query_led_color_type_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 1: Test that query_led_color_type_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Return HDD LED color type of Dual-color Blue / White
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')

        returned_query_led_color_type_cli = query_led_color_type_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['new'][1]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called()

        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'color_type': LED_COLOR_TYPE['new'][1]
                },
                'nuc_wmi_spec_alias': nuc_wmi_spec_alias
            }
        )

        self.assertEqual(returned_query_led_color_type_cli, None)


    @patch('nuc_wmi.cli.query_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    def test_query_led_color_type_cli2(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_query_led_color_type,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `query_led_color_type_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 2: Test that query_led_color_type_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_query_led_color_type.side_effect = NucWmiError('Error (Function not supported)')

        returned_query_led_color_type_cli = query_led_color_type_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['new'][1]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_color_type_cli, None)


    @patch('nuc_wmi.cli.query_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    def test_query_led_color_type_cli3(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_query_led_color_type,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `query_led_color_type_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 3: Test that query_led_color_type_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Return HDD LED color type of Single-color LED
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Single-color LED')

        returned_query_led_color_type_cli = query_led_color_type_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['new'][1]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called()

        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'color_type': LED_COLOR_TYPE['new'][3]
                },
                'nuc_wmi_spec_alias': nuc_wmi_spec_alias
            }
        )

        self.assertEqual(returned_query_led_color_type_cli, None)


    @patch('nuc_wmi.cli.query_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    @patch('nuc_wmi.cli.query_led.query_led_control_items')
    @patch('nuc_wmi.cli.query_led.query_led_indicator_options')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    def test_query_led_control_items_cli( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `query_led_control_items_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 1: Test that query_led_control_items_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Get control items for HDD LED set to HDD Activity Indicator
        expected_control_items = [0, 1, 2, 3]
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_control_items.return_value = expected_control_items
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]

        returned_query_led_control_items_cli = query_led_control_items_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_query_led_control_items.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            control_file=None,
            debug=False,
            metadata=None
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
                },
                'nuc_wmi_spec_alias': nuc_wmi_spec_alias
            }
        )

        self.assertEqual(returned_query_led_control_items_cli, None)


    @patch('nuc_wmi.cli.query_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    @patch('nuc_wmi.cli.query_led.query_led_control_items')
    @patch('nuc_wmi.cli.query_led.query_led_indicator_options')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    def test_query_led_control_items_cli2( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `query_led_control_items_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 2: Test that query_led_control_items_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_control_items.side_effect = NucWmiError('Error (Function not supported)')
        nuc_wmi_query_led_indicator_options.return_value = [1, 4]

        returned_query_led_control_items_cli = query_led_control_items_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_query_led_control_items.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_control_items_cli, None)


    @patch('nuc_wmi.cli.query_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    @patch('nuc_wmi.cli.query_led.query_led_control_items')
    @patch('nuc_wmi.cli.query_led.query_led_indicator_options')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    def test_query_led_control_items_cli3( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `query_led_control_items_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 3: Tests that invalid LED indicator raises appropriate error.
        expected_control_items = [0, 1, 2, 3]
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_control_items.return_value = expected_control_items
        nuc_wmi_query_led_indicator_options.return_value = []

        returned_query_led_control_items_cli = query_led_control_items_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[1]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_query_led_control_items.assert_not_called()
        nuc_wmi_print.assert_called_with('{"error": "Invalid indicator option for the selected LED"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_control_items_cli, None)


    @patch('nuc_wmi.cli.query_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.query_led_color_type')
    @patch('nuc_wmi.cli.query_led.query_led_control_items')
    @patch('nuc_wmi.cli.query_led.query_led_indicator_options')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    def test_query_led_control_items_cli4( # pylint: disable=too-many-arguments,too-many-statements
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_query_led_control_items,
            nuc_wmi_query_led_color_type,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `query_led_control_items_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_control_items is nuc_wmi_query_led_control_items)
        self.assertTrue(nuc_wmi.cli.query_led.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 4: Test that query_led_control_items_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Get control items for HDD LED set to Disable
        expected_control_items = []
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_query_led_control_items.return_value = expected_control_items
        nuc_wmi_query_led_indicator_options.return_value = [1, 4, 6]

        returned_query_led_control_items_cli = query_led_control_items_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['new'][1],
                LED_INDICATOR_OPTION[6]
            ]
        )

        nuc_wmi_query_led_color_type.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_query_led_indicator_options.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_query_led_control_items.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('Disable'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called()

        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_option': LED_INDICATOR_OPTION[6],
                    'control_items': [CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR[control_item]['Control Item'] \
                                      for control_item in expected_control_items]
                },
                'nuc_wmi_spec_alias': nuc_wmi_spec_alias
            }
        )

        self.assertEqual(returned_query_led_control_items_cli, None)


    @patch('nuc_wmi.cli.query_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.query_led_indicator_options')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    def test_query_led_indicator_options_cli(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `query_led_indicator_options_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.query_led.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 1: Test that query_led_indicator_options_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Return HDD LED indicator options of HDD Activity Indicator and Software Indicator
        expected_indicator_options = [1, 4]
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_query_led_indicator_options.return_value = expected_indicator_options

        returned_query_led_indicator_options_cli = query_led_indicator_options_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['new'][1]
            ]
        )

        nuc_wmi_query_led_indicator_options.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called()

        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['new'][1],
                    'indicator_options': [LED_INDICATOR_OPTION[indicator] for indicator in expected_indicator_options]
                },
                'nuc_wmi_spec_alias': nuc_wmi_spec_alias
            }
        )

        self.assertEqual(returned_query_led_indicator_options_cli, None)


    @patch('nuc_wmi.cli.query_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.query_led_indicator_options')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    def test_query_led_indicator_options_cli2(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_query_led_indicator_options,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `query_led_indicator_options_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.query_led.query_led_indicator_options is nuc_wmi_query_led_indicator_options)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 2: Test that query_led_indicator_options_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_query_led_indicator_options.side_effect = NucWmiError('Error (Function not supported)')

        returned_query_led_indicator_options_cli = query_led_indicator_options_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['new'][1]
            ]
        )

        nuc_wmi_query_led_indicator_options.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_led_indicator_options_cli, None)


    @patch('nuc_wmi.cli.query_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.query_leds')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    def test_query_leds_cli(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_query_leds,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `query_leds_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.query_led.query_leds is nuc_wmi_query_leds)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 1: Test that query_leds_cli returns the proper JSON response and exit
        #           code for valid cli args
        expected_leds = [0, 1]
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_query_leds.return_value = expected_leds

        returned_query_leds_cli = query_leds_cli([nuc_wmi_spec_alias])

        nuc_wmi_query_leds.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called()

        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'leds': [LED_TYPE['new'][led] for led in expected_leds],
                'nuc_wmi_spec_alias': nuc_wmi_spec_alias
            }
        )

        self.assertEqual(returned_query_leds_cli, None)


    @patch('nuc_wmi.cli.query_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.query_led.print')
    @patch('nuc_wmi.cli.query_led.query_leds')
    @patch('nuc_wmi.cli.query_led.sys.exit')
    def test_query_leds_cli2(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_query_leds,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec
    ):
        """
        Tests that `query_leds_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.query_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.query_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.query_led.query_leds is nuc_wmi_query_leds)
        self.assertTrue(nuc_wmi.cli.query_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 2: Test that query_leds_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_query_leds.side_effect = NucWmiError('Error (Function not supported)')

        returned_query_leds_cli = query_leds_cli([nuc_wmi_spec_alias])

        nuc_wmi_query_leds.assert_called_with(
            self.nuc_wmi_spec.get('nuc_wmi_spec', {}).get(nuc_wmi_spec_alias),
            control_file=None,
            debug=False,
            metadata=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_query_leds_cli, None)
