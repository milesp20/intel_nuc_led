"""
The `test.unit.nuc_wmi.led_app_notification_test` module provides unit tests for the functions in
`nuc_wmi.led_app_notification`.

Classes:
    TestLedAppNotification: A unit test class for the functions in `nuc_wmi.led_app_notification`.
"""

import unittest

from mock import patch

from nuc_wmi import NucWmiError
from nuc_wmi.led_app_notification import NOTIFICATION_TYPE, METHOD_ID, save_led_config

import nuc_wmi


class TestLedAppNotification(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.led_app_notification`

    Methods:
        setUp: Unit test initialization.
        test_save_led_config: Tests that it sends the expected byte list to the control file, tests that the returned
                              control file response is properly processed, tests that it raises an exception when the
                              control file returns an error code.
    """

    def setUp(self):
        """
        Initializes the unit tests;
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('nuc_wmi.led_app_notification.read_control_file')
    @patch('nuc_wmi.led_app_notification.write_control_file')
    def test_save_led_config(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `save_led_config` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.led_app_notification.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.led_app_notification.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that save_led_config sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.
        expected_write_byte_list = [METHOD_ID, NOTIFICATION_TYPE.index('save_led_config')]
        read_byte_list = [0x00, 0x00, 0x00, 0x00]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_save_led_config = save_led_config(
            control_file=None,
            debug=False,
            quirks=None
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False,
            quirks=None
        )

        self.assertEqual(returned_save_led_config, None)


    @patch('nuc_wmi.led_app_notification.read_control_file')
    @patch('nuc_wmi.led_app_notification.write_control_file')
    def test_save_led_config2(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `save_led_config` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.led_app_notification.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.led_app_notification.write_control_file is nuc_wmi_write_control_file)

        # Branch 2: Test that save_led_config raises an exception when the control file returns an
        #           error code.
        expected_write_byte_list = [METHOD_ID, NOTIFICATION_TYPE.index('save_led_config')]
        read_byte_list = [0xE1, 0x00, 0x00, 0x00] # Return function not supported

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            save_led_config(
                control_file=None,
                debug=False,
                quirks=None
            )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False,
            quirks=None
        )

        self.assertEqual(str(err.exception), 'Error (Function not supported)')
