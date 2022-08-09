"""
The `test.unit.nuc_wmi.cli.led_app_notification_test` module provides unit tests for the functions in
`nuc_wmi.cli.led_app_notification`.

Classes:
    TestCliLedAppNotification: A unit test class for the functions in `nuc_wmi.cli.led_app_notification`.
"""

from __future__ import print_function

import json
import unittest

from mock import patch

from nuc_wmi import NucWmiError
from nuc_wmi.cli.led_app_notification import save_led_config_cli

import nuc_wmi


class TestCliLedAppNotification(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.cli.led_app_notification`

    Methods:
        setUp: Unit test initialization.
        test_save_led_config_cli: Tests that it returns the proper JSON response and exit code for
                                  valid cli args, tests that it captures raised errors and returns
                                  the proper JSON error response and exit code.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name

    @patch('nuc_wmi.cli.led_app_notification.print')
    @patch('nuc_wmi.cli.led_app_notification.sys.exit')
    @patch('nuc_wmi.cli.led_app_notification.save_led_config')
    def test_save_led_config_cli(
            self,
            nuc_wmi_cli_save_led_config,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `save_led_config_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.led_app_notification.save_led_config is nuc_wmi_cli_save_led_config)
        self.assertTrue(nuc_wmi.cli.led_app_notification.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.led_app_notification.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 1: Test that save_led_config_cli returns the proper JSON response and exit
        #           code for valid cli args
        returned_save_led_config_cli = save_led_config_cli([])

        nuc_wmi_cli_save_led_config.assert_called_with(
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called()
        self.assertEqual(
            json.loads(nuc_wmi_print.call_args.args[0]),
            {
                'led_app_notification': {
                    'type': 'save_led_config'
                }
            }
        )

        self.assertEqual(returned_save_led_config_cli, None)


    @patch('nuc_wmi.cli.led_app_notification.print')
    @patch('nuc_wmi.cli.led_app_notification.sys.exit')
    @patch('nuc_wmi.cli.led_app_notification.save_led_config')
    def test_save_led_config_cli2(
            self,
            nuc_wmi_cli_save_led_config,
            nuc_wmi_sys_exit,
            nuc_wmi_print
    ):
        """
        Tests that `save_led_config_cli` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.cli.led_app_notification.save_led_config is nuc_wmi_cli_save_led_config)
        self.assertTrue(nuc_wmi.cli.led_app_notification.sys.exit is nuc_wmi_sys_exit)
        self.assertTrue(nuc_wmi.cli.led_app_notification.print is nuc_wmi_print) # pylint: disable=no-member

        # Branch 2: Test that save_led_config_cli captures raised errors and returns
        #           the proper JSON error response and exit code.
        nuc_wmi_cli_save_led_config.side_effect = NucWmiError('Error (Function not supported)')

        returned_save_led_config_cli = save_led_config_cli([])

        nuc_wmi_cli_save_led_config.assert_called_with(
            control_file=None,
            debug=False,
            quirks=None
        )
        nuc_wmi_print.assert_called_with('{"error": "Error (Function not supported)"}')
        nuc_wmi_sys_exit.assert_called_with(1)

        self.assertEqual(returned_save_led_config_cli, None)
