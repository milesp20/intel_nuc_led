"""
The `test.unit.nuc_wmi.set_led_indicator_option_test` module provides unit tests for the functions in
`nuc_wmi.set_led_indicator_option`.

Classes:
    TestSetLedIndicatorOption: A unit test class for the functions in `nuc_wmi.set_led_indicator_option`.
"""

import unittest

from mock import patch

from nuc_wmi import LED_INDICATOR_OPTION, LED_TYPE, NucWmiError
from nuc_wmi.set_led_indicator_option import METHOD_ID, set_led_indicator_option

import nuc_wmi


class TestSetLedIndicatorOption(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.set_led_indicator_option`

    Methods:
        setUp: Unit test initialization.
        test_set_led_indicator_option: Tests that it sends the expected byte list to the control file, tests that the
                                       returned control file response is properly processed, tests that it raises an
                                       exception when the control file returns an error code.
    """

    def setUp(self):
        """
        Initializes the unit tests;
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('nuc_wmi.set_led_indicator_option.read_control_file')
    @patch('nuc_wmi.set_led_indicator_option.write_control_file')
    def test_set_led_indicator_option(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `set_led_indicator_option` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.set_led_indicator_option.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.set_led_indicator_option.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that set_led_indicator_option sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Set HDD LED with HDD Activity Indicator
        expected_write_byte_list = [
            METHOD_ID,
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator')
        ]
        read_byte_list = [
            0x00,
            0x00,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_set_led_indicator_option = set_led_indicator_option(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
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

        self.assertEqual(returned_set_led_indicator_option, None)


    @patch('nuc_wmi.set_led_indicator_option.read_control_file')
    @patch('nuc_wmi.set_led_indicator_option.write_control_file')
    def test_set_led_indicator_option2(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `set_led_indicator_option` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.set_led_indicator_option.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.set_led_indicator_option.write_control_file is nuc_wmi_write_control_file)

        # Branch 2: Test that set_led_indicator_option raises an exception when the control file returns an
        #           error code.

        # Incorrect led
        expected_write_byte_list = [
            METHOD_ID,
            len(LED_TYPE['new']), # Incorrect led
            LED_INDICATOR_OPTION.index('HDD Activity Indicator')
        ]
        read_byte_list = [
            0xE4,
            0x00,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            set_led_indicator_option(
                len(LED_TYPE['new']), # Incorrect led
                LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
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


    @patch('nuc_wmi.set_led_indicator_option.read_control_file')
    @patch('nuc_wmi.set_led_indicator_option.write_control_file')
    def test_set_led_indicator_option3(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `set_led_indicator_option` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.set_led_indicator_option.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.set_led_indicator_option.write_control_file is nuc_wmi_write_control_file)

        # Branch 3: Test that set_led_indicator_option sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Set HDD LED with Software Indicator
        expected_write_byte_list = [
            METHOD_ID,
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('Software Indicator')
        ]
        read_byte_list = [
            0x00,
            0x00,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_set_led_indicator_option = set_led_indicator_option(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('Software Indicator'),
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

        self.assertEqual(returned_set_led_indicator_option, None)
