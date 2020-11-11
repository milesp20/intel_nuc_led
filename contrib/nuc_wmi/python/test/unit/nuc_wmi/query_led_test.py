"""
The `test.unit.nuc_wmi.query_led_test` module provides unit tests for the functions in
`nuc_wmi.query_led`.

Classes:
    TestQueryLed: A unit test class for the functions in `nuc_wmi.query_led`.
"""

import unittest

from mock import patch

from nuc_wmi import LED_COLOR_TYPE, LED_INDICATOR_OPTION, LED_TYPE, NucWmiError
from nuc_wmi.query_led import LED_INDICATOR_OPTION_DISABLED, METHOD_ID, QUERY_TYPE, query_led_color_type
from nuc_wmi.query_led import query_led_control_items, query_led_indicator_options, query_leds

import nuc_wmi


class TestQueryLed(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.query_led`

    Methods:
        setUp: Unit test initialization.
        test_query_led_color_type: Tests that it sends the expected byte list to the control file,
                                   tests that the returned control file response is properly processed,
                                   tests that it raises an exception when the control file returns an
                                   error code.
        test_query_led_control_items: Tests that it sends the expected byte list to the control file,
                                      tests that the returned control file response is properly processed,
                                      tests that it raises an exception when the control file returns an
                                      error code.
        test_query_led_indicator_options: Tests that it sends the expected byte list to the control file,
                                          tests that the returned control file response is properly processed,
                                          tests that it raises an exception when the control file returns an
                                          error code.
        test_query_leds: Tests that it sends the expected byte list to the control file,
                         tests that the returned control file response is properly processed,
                         tests that it raises an exception when the control file returns an
                         error code.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_color_type(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `query_led_color_type` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that query_led_color_type send the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Query HDD LED that returns a color type of Dual-color Blue / White
        expected_query_led_color_type = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_color_type'),
            LED_TYPE['new'].index('HDD LED')
        ]
        read_byte_list = [
            0x00,
            0x02,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_query_led_color_type = query_led_color_type(
            LED_TYPE['new'].index('HDD LED')
        )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(returned_query_led_color_type, expected_query_led_color_type)

        # Reset
        nuc_wmi_read_control_file.return_value = None
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()

        # Branch 2: Test that query_led_color_type raises an exception when the control file returns an
        #           error code.

        # Incorrect led
        expected_query_led_color_type = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_color_type'),
            len(LED_TYPE['new']) # Incorrect led index
        ]
        read_byte_list = [
            0xE4,
            0x00,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            returned_query_led_color_type = query_led_color_type(
                len(LED_TYPE['new']) # Incorrect led index
            )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')

        # Reset
        nuc_wmi_read_control_file.return_value = None
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()

        # Branch 3: Test that query_led_color_type send the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Query HDD LED that returns a color type of Single-color LED
        expected_query_led_color_type = LED_COLOR_TYPE['new'].index('Single-color LED')
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_color_type'),
            LED_TYPE['new'].index('HDD LED')
        ]
        read_byte_list = [
            0x00,
            0x08,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_query_led_color_type = query_led_color_type(
            LED_TYPE['new'].index('HDD LED')
        )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(returned_query_led_color_type, expected_query_led_color_type)

        # Branch 4: Test that query_led_color_type changes the return value format when QUIRKS mode
        #           NUC10_RETURN_VALUE is enabled.

        # Query HDD LED that returns a color type of Single-color LED
        expected_query_led_color_type = LED_COLOR_TYPE['new'].index('Single-color LED')
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_color_type'),
            LED_TYPE['new'].index('HDD LED')
        ]
        read_byte_list = [
            0x00,
            0x03,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list

        with patch('nuc_wmi.query_led.QUIRKS_ENABLED', ['NUC10_RETURN_VALUE']):
            returned_query_led_color_type = query_led_color_type(
                LED_TYPE['new'].index('HDD LED')
            )

            nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

            self.assertEqual(returned_query_led_color_type, expected_query_led_color_type)


    @patch('nuc_wmi.query_led.query_led_color_type')
    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_control_items(
            self,
            nuc_wmi_write_control_file,
            nuc_wmi_read_control_file,
            nuc_wmi_query_led_color_type
    ):
        """
        Tests that `query_led_control_items` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)
        self.assertTrue(nuc_wmi.query_led.query_led_color_type is nuc_wmi_query_led_color_type)

        # Branch 1: Test that query_led_control_items send the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Query control items of HDD LED with HDD Activity Indicator
        expected_query_led_control_items = [0, 1, 2, 3]
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_control_items'),
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator')
        ]
        read_byte_list = [
            0x00,
            0x0F,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        returned_query_led_control_items = query_led_control_items(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator')
        )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)
        nuc_wmi_query_led_color_type.assert_called_with(LED_TYPE['new'].index('HDD LED'), control_file=None)

        self.assertEqual(returned_query_led_control_items, expected_query_led_control_items)

        # Reset
        nuc_wmi_read_control_file.return_value = None
        nuc_wmi_query_led_color_type.return_value = None
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()
        nuc_wmi_query_led_color_type.reset_mock()

        # Query control items of HDD LED with Disabled Indicator
        expected_query_led_control_items = []
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_control_items'),
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION_DISABLED
        ]
        read_byte_list = [
            0x00,
            0x00,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        returned_query_led_control_items = query_led_control_items(
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION_DISABLED
        )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)
        nuc_wmi_query_led_color_type.assert_called_with(LED_TYPE['new'].index('HDD LED'), control_file=None)

        self.assertEqual(returned_query_led_control_items, expected_query_led_control_items)

        # Reset
        nuc_wmi_read_control_file.return_value = None
        nuc_wmi_query_led_color_type.return_value = None
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()
        nuc_wmi_query_led_color_type.reset_mock()

        # Branch 2: Test that query_led_control_items raises an exception when the control file returns an
        #           error code.

        # Incorrect led
        expected_query_led_control_items = [0, 1, 2, 3]
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_control_items'),
            len(LED_TYPE['new']), # Invalid led index
            LED_INDICATOR_OPTION.index('HDD Activity Indicator')
        ]
        read_byte_list = [
            0xE4,
            0x00,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')

        with self.assertRaises(NucWmiError) as err:
            returned_query_led_control_items = query_led_control_items(
                len(LED_TYPE['new']), # Invalid led index
                LED_INDICATOR_OPTION.index('HDD Activity Indicator')
            )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)
        nuc_wmi_query_led_color_type.assert_called_with(len(LED_TYPE['new']), control_file=None)

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_indicator_options(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `query_led_indicator_options` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that query_led_indicator_options send the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Query HDD LED indicator options
        expected_query_led_indicator_options = [1, 4]
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_indicator_options'),
            LED_TYPE['new'].index('HDD LED')
        ]
        read_byte_list = [
            0x00,
            0x12,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_query_led_indicator_options = query_led_indicator_options(
            LED_TYPE['new'].index('HDD LED')
        )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(returned_query_led_indicator_options, expected_query_led_indicator_options)

        # Reset
        nuc_wmi_read_control_file.return_value = None
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()

        # Branch 2: Test that query_led_indicator_options raises an exception when the control file returns an
        #           error code.

        # Incorrect led
        expected_query_led_indicator_options = [1, 4]
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_indicator_options'),
            len(LED_TYPE['new']) # Incorrect led index
        ]
        read_byte_list = [
            0xE4,
            0x00,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            returned_query_led_indicator_options = query_led_indicator_options(
                len(LED_TYPE['new']) # Incorrect led index
            )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_leds(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `query_leds` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that query_leds send the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Query HDD LED indicator options
        expected_query_leds = [0, 1]
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_leds')
        ]
        read_byte_list = [
            0x00,
            0x03,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_query_leds = query_leds()

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(returned_query_leds, expected_query_leds)

        # Reset
        nuc_wmi_read_control_file.return_value = None
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()

        # Branch 2: Test that query_leds raises an exception when the control file returns an
        #           error code.

        # Incorrect led
        expected_query_leds = [0, 1]
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_leds')
        ]
        read_byte_list = [
            0xE1,
            0x00,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            returned_query_leds = query_leds()

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(str(err.exception), 'Error (Function not supported)')
