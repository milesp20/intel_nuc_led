"""
The `test.unit.nuc_wmi.get_led_new_test` module provides unit tests for the functions in
`nuc_wmi.get_led_new`.

Classes:
    TestGetLed: A unit test class for the functions in `nuc_wmi.get_led_new`.
"""

import unittest

from mock import patch

from nuc_wmi import CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR, CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR
from nuc_wmi import LED_BLINK_FREQUENCY, LED_BRIGHTNESS_MULTI_COLOR, LED_INDICATOR_OPTION, LED_TYPE
from nuc_wmi import NucWmiError
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
            0x30,
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
            ),
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

        self.assertEqual(returned_get_led_control_item, read_byte_list[1])


    @patch('nuc_wmi.get_led_new.read_control_file')
    @patch('nuc_wmi.get_led_new.write_control_file')
    def test_get_led_control_item2(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `get_led_control_item` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led_new.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led_new.write_control_file is nuc_wmi_write_control_file)

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
            get_led_control_item(
                len(LED_TYPE['new']), # Incorrect led
                LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
                CONTROL_ITEM_HDD_ACTIVITY_INDICATOR_MULTI_COLOR.index(
                    {
                        'Control Item': 'Brightness',
                        'Options': LED_BRIGHTNESS_MULTI_COLOR
                    }
                ),
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


    @patch('nuc_wmi.get_led_new.read_control_file')
    @patch('nuc_wmi.get_led_new.write_control_file')
    def test_get_led_control_item3(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `get_led_control_item` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led_new.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led_new.write_control_file is nuc_wmi_write_control_file)

        # Branch 3: Test that get_led_control_item sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Get RGB Header Software Indicator Brightness of 30% for multi color led
        expected_write_byte_list = [
            METHOD_ID,
            GET_LED_TYPE.index('get_led_control_item'),
            LED_TYPE['new'].index('RGB Header'),
            LED_INDICATOR_OPTION.index('Software Indicator'),
            CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Brightness',
                    'Options': LED_BRIGHTNESS_MULTI_COLOR
                }
            ),
        ]
        read_byte_list = [
            0x00,
            0x30,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_get_led_control_item = get_led_control_item(
            LED_TYPE['new'].index('RGB Header'),
            LED_INDICATOR_OPTION.index('Software Indicator'),
            CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Brightness',
                    'Options': LED_BRIGHTNESS_MULTI_COLOR
                }
            ),
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

        self.assertEqual(returned_get_led_control_item, read_byte_list[1])

    @patch('nuc_wmi.get_led_new.read_control_file')
    @patch('nuc_wmi.get_led_new.write_control_file')
    def test_get_led_control_item4(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `get_led_control_item` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led_new.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led_new.write_control_file is nuc_wmi_write_control_file)

        # Branch 4: Test that get_led_control_item sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Get RGB Header Software Indicator Blinking Frequency of 1 Hz for multi color led
        expected_write_byte_list = [
            METHOD_ID,
            GET_LED_TYPE.index('get_led_control_item'),
            LED_TYPE['new'].index('RGB Header'),
            LED_INDICATOR_OPTION.index('Software Indicator'),
            CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Blinking Frequency',
                    'Options': LED_BLINK_FREQUENCY['new']
                }
            ),
        ]
        read_byte_list = [
            0x00,
            0x0A,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_get_led_control_item = get_led_control_item(
            LED_TYPE['new'].index('RGB Header'),
            LED_INDICATOR_OPTION.index('Software Indicator'),
            CONTROL_ITEM_SOFTWARE_INDICATOR_MULTI_COLOR.index(
                {
                    'Control Item': 'Blinking Frequency',
                    'Options': LED_BLINK_FREQUENCY['new']
                }
            ),
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

        self.assertEqual(returned_get_led_control_item, LED_BLINK_FREQUENCY['new'].index('1.0Hz'))


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
            0x02,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_get_led_indicator_option = get_led_indicator_option(
            LED_TYPE['new'].index('HDD LED'),
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

        self.assertEqual(returned_get_led_indicator_option, LED_INDICATOR_OPTION.index('HDD Activity Indicator'))


    @patch('nuc_wmi.get_led_new.read_control_file')
    @patch('nuc_wmi.get_led_new.write_control_file')
    def test_get_led_indicator_option2(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `get_led_indicator_option` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led_new.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led_new.write_control_file is nuc_wmi_write_control_file)

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
            get_led_indicator_option(
                len(LED_TYPE['new']), # Incorrect led
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


    @patch('nuc_wmi.get_led_new.read_control_file')
    @patch('nuc_wmi.get_led_new.write_control_file')
    def test_get_led_indicator_option3(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `get_led_indicator_option` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led_new.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led_new.write_control_file is nuc_wmi_write_control_file)

        # Branch 3: Test that get_led_indicator_option sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Get HDD LED with Software Indicator
        expected_write_byte_list = [
            METHOD_ID,
            GET_LED_TYPE.index('get_led_indicator_option'),
            LED_TYPE['new'].index('HDD LED')
        ]
        read_byte_list = [
            0x00,
            0x10,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_get_led_indicator_option = get_led_indicator_option(
            LED_TYPE['new'].index('HDD LED'),
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

        self.assertEqual(returned_get_led_indicator_option, LED_INDICATOR_OPTION.index('Software Indicator'))


    @patch('nuc_wmi.get_led_new.read_control_file')
    @patch('nuc_wmi.get_led_new.write_control_file')
    def test_get_led_indicator_option4(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `get_led_indicator_option` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led_new.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led_new.write_control_file is nuc_wmi_write_control_file)

        # Branch 4: Test that get_led_indicator_option changes the return value format when QUIRKS mode
        #           NUC10_RETURN_VALUE is enabled.

        # Get HDD LED with HDD Activity Indicator
        expected_write_byte_list = [
            METHOD_ID,
            GET_LED_TYPE.index('get_led_indicator_option'),
            LED_TYPE['new'].index('HDD LED')
        ]
        read_byte_list = [
            0x00,
            0x01,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list

        returned_get_led_indicator_option = get_led_indicator_option(
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            quirks=['NUC10_RETURN_VALUE']
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False,
            quirks=['NUC10_RETURN_VALUE']
        )

        self.assertEqual(returned_get_led_indicator_option, LED_INDICATOR_OPTION.index('HDD Activity Indicator'))
