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

    @patch('nuc_wmi.cli.get_led.print')
    @patch('nuc_wmi.cli.get_led.sys.exit')
    @patch('nuc_wmi.cli.get_led.get_led')
    def test_get_led_cli(
            self,
            nuc_wmi_get_led,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `get_led_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.get_led.get_led is nuc_wmi_get_led)
        self.assertTrue(nuc_wmi.cli.get_led.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.get_led.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 1: Test that get_led_cli returns the proper JSON response and exit
        #           code for valid cli args

        # Get S0 Ring LED with a brightness of 47%, frequency of Always on, and color of Cyan
        expected_brightness = str(LED_BRIGHTNESS['legacy'].index('47'))
        expected_frequency = LED_BLINK_FREQUENCY['legacy'].index('Always on')
        expected_color = LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Cyan')
        nuc_wmi_get_led.return_value = (expected_brightness, expected_frequency, expected_color)
        returned_get_led_cli = get_led_cli(
            [
                LED_TYPE['legacy'][2]
            ]
        )

        nuc_wmi_get_led.assert_called_with(
            LED_TYPE['legacy'].index('S0 Ring LED'),
            control_file=None,
            debug=False,
            quirks=None
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
                }
            }
        )

        self.assertEqual(returned_get_led_cli, None)


    @patch('nuc_wmi.cli.get_led.print')
    @patch('nuc_wmi.cli.get_led.sys.exit')
    @patch('nuc_wmi.cli.get_led.get_led')
    def test_get_led_cli2(
            self,
            nuc_wmi_get_led,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `get_led_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.get_led.get_led is nuc_wmi_get_led)
        self.assertTrue(nuc_wmi.cli.get_led.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.get_led.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 2: Test that get_led_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_get_led.side_effect = NucWmiError('Error (Function not supported)')

        returned_get_led_cli = get_led_cli(
            [
                LED_TYPE['legacy'][2]
            ]
        )

        nuc_wmi_get_led.assert_called_with(
            LED_TYPE['legacy'].index('S0 Ring LED'),
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_get_led_cli, None)
