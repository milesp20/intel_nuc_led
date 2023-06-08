"""
The `test.unit.nuc_wmi.cli.get_led_test` module provides unit tests for the functions in
`nuc_wmi.cli.get_led`.

Classes:
    TestCliGetLed: A unit test class for the functions in `nuc_wmi.cli.get_led`.
"""

from __future__ import print_function

import json
import unittest

from mock import patch

from nuc_wmi import LED_BLINK_FREQUENCY, LED_BRIGHTNESS, LED_COLOR, LED_COLOR_TYPE, LED_TYPE, NucWmiError
from nuc_wmi.cli.get_led import get_led_cli
from nuc_wmi.utils import defined_indexes

import nuc_wmi


class TestCliGetLed(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.cli.get_led`

    Methods:
        setUp: Unit test initialization.
        test_get_led_cli: Tests that it returns the proper JSON response and exit code for
                          valid cli args, tests that it captures raised errors and returns
                          the proper JSON error response and exit code.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name

        self.nuc_wmi_spec = {
            'TEST_DEVICE': {
                'nuc_wmi_spec': {
                    'function_return_type': {
                        'get_led': 'index'
                    },
                    'recover': {
                        'function_oob_return_value': {
                            'get_led': False
                        }
                    }
                }
            }
        }


    @patch('nuc_wmi.cli.get_led.get_led')
    @patch('nuc_wmi.cli.get_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.get_led.print')
    @patch('nuc_wmi.cli.get_led.sys.exit')
    def test_get_led_cli(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec,
            nuc_wmi_get_led
    ):
        """
        Tests that `get_led_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.get_led.get_led is nuc_wmi_get_led)
        self.assertTrue(nuc_wmi.cli.get_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.get_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.get_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 1: Test that get_led_cli returns the proper JSON response and exit
        #           code for valid cli args
        led_color_type = LED_COLOR_TYPE['legacy']['S0 Ring LED']

        brightness_range = defined_indexes(LED_BRIGHTNESS['legacy'])
        frequency_range = defined_indexes(LED_BLINK_FREQUENCY['legacy'])
        color_range = defined_indexes(LED_COLOR['legacy'][led_color_type])

        metadata = {
            'brightness_range': brightness_range,
            'frequency_range': frequency_range,
            'color_range': color_range
        }
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        # Get S0 Ring LED with a brightness of 47%, frequency of Always on, and color of Cyan
        expected_brightness = LED_BRIGHTNESS['legacy'].index('47')
        expected_frequency = LED_BLINK_FREQUENCY['legacy'].index('Always on')
        expected_color = LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Cyan')

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_get_led.return_value = (expected_brightness, expected_frequency, expected_color)

        returned_get_led_cli = get_led_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['legacy'][2]
            ]
        )

        nuc_wmi_get_led.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            LED_TYPE['legacy'].index('S0 Ring LED'),
            control_file=None,
            debug=False,
            metadata=metadata
        )
        nuc_wmi_print.assert_called()

        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led': {
                    'type': LED_TYPE['legacy'][2],
                    'brightness': LED_BRIGHTNESS['legacy'][47],
                    'frequency': LED_BLINK_FREQUENCY['legacy'][4],
                    'color': LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']][1]
                },
                'nuc_wmi_spec_alias': nuc_wmi_spec_alias
            }
        )

        self.assertEqual(returned_get_led_cli, None)


    @patch('nuc_wmi.cli.get_led.get_led')
    @patch('nuc_wmi.cli.get_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.get_led.print')
    @patch('nuc_wmi.cli.get_led.sys.exit')
    def test_get_led_cli2(
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec,
            nuc_wmi_get_led
    ):
        """
        Tests that `get_led_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.get_led.get_led is nuc_wmi_get_led)
        self.assertTrue(nuc_wmi.cli.get_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.get_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.get_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 2: Test that get_led_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        led_color_type = LED_COLOR_TYPE['legacy']['S0 Ring LED']

        brightness_range = defined_indexes(LED_BRIGHTNESS['legacy'])
        frequency_range = defined_indexes(LED_BLINK_FREQUENCY['legacy'])
        color_range = defined_indexes(LED_COLOR['legacy'][led_color_type])

        metadata = {
            'brightness_range': brightness_range,
            'frequency_range': frequency_range,
            'color_range': color_range
        }
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_get_led.side_effect = NucWmiError('Error (Function not supported)')

        returned_get_led_cli = get_led_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['legacy'][2]
            ]
        )

        nuc_wmi_get_led.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            LED_TYPE['legacy'].index('S0 Ring LED'),
            control_file=None,
            debug=False,
            metadata=metadata
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_get_led_cli, None)


    @patch('nuc_wmi.cli.get_led.get_led')
    @patch('nuc_wmi.cli.get_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.get_led.print')
    @patch('nuc_wmi.cli.get_led.sys.exit')
    def test_get_led_cli3( # pylint: disable=too-many-locals
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec,
            nuc_wmi_get_led
    ):
        """
        Tests that `get_led_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.get_led.get_led is nuc_wmi_get_led)
        self.assertTrue(nuc_wmi.cli.get_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.get_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.get_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 3: Test that get_led_cli raises exception with error message for invalid brightness returned by WMI,
        #           captures raised errors and returns the proper JSON error response and exit code.
        led_color_type = LED_COLOR_TYPE['legacy']['S0 Ring LED']

        brightness_range = defined_indexes(LED_BRIGHTNESS['legacy'])
        frequency_range = defined_indexes(LED_BLINK_FREQUENCY['legacy'])
        color_range = defined_indexes(LED_COLOR['legacy'][led_color_type])

        metadata = {
            'brightness_range': brightness_range,
            'frequency_range': frequency_range,
            'color_range': color_range
        }
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        # Get S0 Ring LED with a invalid brightness, frequency of Always on, and color of Cyan
        expected_brightness = 0xFF
        expected_color = LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Cyan')
        expected_error = "Error (Intel NUC WMI get_led function returned invalid brightness of %i, expected one of %s)"
        expected_frequency = LED_BLINK_FREQUENCY['legacy'].index('Always on')

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_get_led.return_value = (expected_brightness, expected_frequency, expected_color)

        returned_get_led_cli = get_led_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['legacy'][2]
            ]
        )

        nuc_wmi_get_led.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            LED_TYPE['legacy'].index('S0 Ring LED'),
            control_file=None,
            debug=False,
            metadata=metadata
        )
        nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error % (expected_brightness, brightness_range)
                }
            )
        )
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_get_led_cli, None)


    @patch('nuc_wmi.cli.get_led.get_led')
    @patch('nuc_wmi.cli.get_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.get_led.print')
    @patch('nuc_wmi.cli.get_led.sys.exit')
    def test_get_led_cli4( # pylint: disable=too-many-locals
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec,
            nuc_wmi_get_led
    ):
        """
        Tests that `get_led_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.get_led.get_led is nuc_wmi_get_led)
        self.assertTrue(nuc_wmi.cli.get_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.get_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.get_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 4: Test that get_led_cli raises exception with error message for invalid frequency returned by WMI,
        #           captures raised errors and returns the proper JSON error response and exit code.
        led_color_type = LED_COLOR_TYPE['legacy']['S0 Ring LED']

        brightness_range = defined_indexes(LED_BRIGHTNESS['legacy'])
        frequency_range = defined_indexes(LED_BLINK_FREQUENCY['legacy'])
        color_range = defined_indexes(LED_COLOR['legacy'][led_color_type])

        metadata = {
            'brightness_range': brightness_range,
            'frequency_range': frequency_range,
            'color_range': color_range
        }
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        # Get S0 Ring LED with a brightness of 47%, invalid frequency, and color of Cyan
        expected_brightness = LED_BRIGHTNESS['legacy'].index('47')
        expected_color = LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Cyan')
        expected_error = "Error (Intel NUC WMI get_led function returned invalid frequency of %i, expected one of %s)"
        expected_frequency = 0xFF

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_get_led.return_value = (expected_brightness, expected_frequency, expected_color)

        returned_get_led_cli = get_led_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['legacy'][2]
            ]
        )

        nuc_wmi_get_led.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            LED_TYPE['legacy'].index('S0 Ring LED'),
            control_file=None,
            debug=False,
            metadata=metadata
        )
        nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error % (expected_frequency, frequency_range)
                }
            )
        )
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_get_led_cli, None)


    @patch('nuc_wmi.cli.get_led.get_led')
    @patch('nuc_wmi.cli.get_led.load_nuc_wmi_spec')
    @patch('nuc_wmi.cli.get_led.print')
    @patch('nuc_wmi.cli.get_led.sys.exit')
    def test_get_led_cli5( # pylint: disable=too-many-locals
            self,
            nuc_wmi_sys_exit,
            nuc_wmi_print,
            nuc_wmi_cli_load_nuc_wmi_spec,
            nuc_wmi_get_led
    ):
        """
        Tests that `get_led_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.get_led.get_led is nuc_wmi_get_led)
        self.assertTrue(nuc_wmi.cli.get_led.load_nuc_wmi_spec is nuc_wmi_cli_load_nuc_wmi_spec)
        self.assertTrue(nuc_wmi.cli.get_led.print is nuc_wmi_print) # pylint: disable=no-member
        self.assertTrue(nuc_wmi.cli.get_led.sys.exit is nuc_wmi_sys_exit)

        # Branch 5: Test that get_led_cli raises exception with error message for invalid color returned by WMI,
        #           captures raised errors and returns the proper JSON error response and exit code.
        led_color_type = LED_COLOR_TYPE['legacy']['S0 Ring LED']

        brightness_range = defined_indexes(LED_BRIGHTNESS['legacy'])
        frequency_range = defined_indexes(LED_BLINK_FREQUENCY['legacy'])
        color_range = defined_indexes(LED_COLOR['legacy'][led_color_type])

        metadata = {
            'brightness_range': brightness_range,
            'frequency_range': frequency_range,
            'color_range': color_range
        }
        nuc_wmi_spec_alias = 'TEST_DEVICE'

        # Get S0 Ring LED with a brightness of 47%, frequency of Always on, and invalid color
        expected_brightness = LED_BRIGHTNESS['legacy'].index('47')
        expected_color = 0xFF
        expected_error = "Error (Intel NUC WMI get_led function returned invalid color of %i, expected one of %s)"
        expected_frequency = LED_BLINK_FREQUENCY['legacy'].index('Always on')

        nuc_wmi_cli_load_nuc_wmi_spec.return_value = self.nuc_wmi_spec
        nuc_wmi_get_led.return_value = (expected_brightness, expected_frequency, expected_color)

        returned_get_led_cli = get_led_cli(
            [
                nuc_wmi_spec_alias,
                LED_TYPE['legacy'][2]
            ]
        )

        nuc_wmi_get_led.assert_called_with(
            self.nuc_wmi_spec.get(nuc_wmi_spec_alias),
            LED_TYPE['legacy'].index('S0 Ring LED'),
            control_file=None,
            debug=False,
            metadata=metadata
        )
        nuc_wmi_print.assert_called_with(
            json.dumps(
                {
                    "error": expected_error % (expected_color, color_range)
                }
            )
        )
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_get_led_cli, None)
