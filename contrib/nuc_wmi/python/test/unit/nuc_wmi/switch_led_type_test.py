"""
The `test.unit.nuc_wmi.switch_led_type_test` module provides unit tests for the functions in
`nuc_wmi.switch_led_type`.

Classes:
    TestSwitchLedType: A unit test class for the functions in `nuc_wmi.switch_led_type`.
"""

import unittest

from mock import patch

from nuc_wmi import NucWmiError
from nuc_wmi.switch_led_type import LED_COLOR_GROUP, METHOD_ID, switch_led_type

import nuc_wmi


class TestSwitchLedType(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.switch_led_type`

    Methods:
        setUp: Unit test initialization.
        test_switch_led_type: Tests that it sends the expected byte list to the control file, tests that the returned
                              control file response is properly processed, tests that it raises an exception when the
                              control file returns an error code.
    """

    def setUp(self):
        """
        Initializes the unit tests;
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('nuc_wmi.switch_led_type.read_control_file')
    @patch('nuc_wmi.switch_led_type.write_control_file')
    def test_switch_led_type(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `switch_led_type` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.switch_led_type.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.switch_led_type.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that switch_led_type sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.
        expected_write_byte_list = [METHOD_ID, LED_COLOR_GROUP.index('Single color LED')]
        read_byte_list = [0x00, 0x00, 0x00, 0x00]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_switch_led_type = switch_led_type(
            LED_COLOR_GROUP.index('Single color LED'),
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

        self.assertEqual(returned_switch_led_type, None)


    @patch('nuc_wmi.switch_led_type.read_control_file')
    @patch('nuc_wmi.switch_led_type.write_control_file')
    def test_switch_led_type2(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `switch_led_type` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.switch_led_type.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.switch_led_type.write_control_file is nuc_wmi_write_control_file)

        # Branch 2: Test that switch_led_type raises an exception when the control file returns an
        #           error code.
        expected_write_byte_list = [METHOD_ID, len(LED_COLOR_GROUP)] # Send incorrect LED_COLOR_GROUP index
        read_byte_list = [0xE4, 0x00, 0x00, 0x00] # Return invalid parameter

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            switch_led_type(
                len(LED_COLOR_GROUP),
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

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')
