"""
The `test.unit.nuc_wmi.get_led_new_test` module provides unit tests for the functions in
`nuc_wmi.get_led_new`.

Classes:
    TestGetLed: A unit test class for the functions in `nuc_wmi.get_led_new`.
"""

import unittest

from mock import patch

from nuc_wmi import CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR, LED_BRIGHTNESS_MULTI_COLOR, LED_INDICATOR_OPTION
from nuc_wmi import LED_TYPE, NucWmiError
from nuc_wmi.get_led_new import GET_LED_TYPE, METHOD_ID, get_led_control_item, get_led_indicator_option

import nuc_wmi


class TestGetLedNew(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.get_led_new`

    Methods:
        setUp: Unit test initialization.
        test_get_led_control_item: Tests that it sends the expected byte list to the control file, tests that the
                                   returned control file response is properly processed, tests that it raises an
                                   exception when the control file returns an error code.
        test_get_led_indicator_option: Tests that it sends the expected byte list to the control file, tests that the
                                       returned control file response is properly processed, tests that it raises an
                                       exception when the control file returns an error code.
    """

    def setUp(self):
        """
        Initializes the unit tests;
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('nuc_wmi.get_led_new.read_control_file')
    @patch('nuc_wmi.get_led_new.write_control_file')
    def test_get_led_control_item(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `get_led_control_item` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led_new.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led_new.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that get_led_control_item sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Get HDD LED HDD Activity Indicator Brightness of 30% for multi color led
        expected_write_byte_list = [
            METHOD_ID,
            GET_LED_TYPE.index('get_led_control_item'),
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Brightness',
                    'Options': LED_BRIGHTNESS_MULTI_COLOR
                }
            ),
        ]
        read_byte_list = [
            0x00,
            LED_BRIGHTNESS_MULTI_COLOR.index('30'),
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_get_led_control_item = get_led_control_item(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Brightness',
                    'Options': LED_BRIGHTNESS_MULTI_COLOR
                }
            )
        )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(returned_get_led_control_item, read_byte_list[1])

        # Reset
        nuc_wmi_read_control_file.return_value = None
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()

        # Branch 2: Test that get_led_control_item raises an exception when the control file returns an
        #           error code.

        # Incorrect led
        expected_write_byte_list = [
            METHOD_ID,
            GET_LED_TYPE.index('get_led_control_item'),
            len(LED_TYPE['new']), # Incorrect led
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Brightness',
                    'Options': LED_BRIGHTNESS_MULTI_COLOR
                }
            )
        ]
        read_byte_list = [
            0xE4,
            0x00,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            returned_get_led_control_item = get_led_control_item(
                len(LED_TYPE['new']), # Incorrect led
                LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                    {
                        'Control Item': 'Brightness',
                        'Options': LED_BRIGHTNESS_MULTI_COLOR
                    }
                )
            )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')


    @patch('nuc_wmi.get_led_new.read_control_file')
    @patch('nuc_wmi.get_led_new.write_control_file')
    def test_get_led_indicator_option(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `get_led_indicator_option` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led_new.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led_new.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that get_led_indicator_option sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Get HDD LED with HDD Activity Indicator
        expected_write_byte_list = [
            METHOD_ID,
            GET_LED_TYPE.index('get_led_indicator_option'),
            LED_TYPE['new'].index('HDD LED')
        ]
        read_byte_list = [
            0x00,
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_get_led_indicator_option = get_led_indicator_option(
            LED_TYPE['new'].index('HDD LED')
        )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(returned_get_led_indicator_option, read_byte_list[1])

        # Reset
        nuc_wmi_read_control_file.return_value = None
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()

        # Branch 2: Test that get_led_indicator_option raises an exception when the control file returns an
        #           error code.

        # Incorrect led
        expected_write_byte_list = [
            METHOD_ID,
            GET_LED_TYPE.index('get_led_indicator_option'),
            len(LED_TYPE['new']) # Incorrect led
        ]
        read_byte_list = [
            0xE4,
            0x00,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            returned_get_led_indicator_option = get_led_indicator_option(
                len(LED_TYPE['new']) # Incorrect led
            )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')
