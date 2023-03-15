"""
The `test.unit.nuc_wmi.get_led_test` module provides unit tests for the functions in
`nuc_wmi.get_led`.

Classes:
    TestGetLed: A unit test class for the functions in `nuc_wmi.get_led`.
"""

import unittest

from mock import patch

from nuc_wmi import LED_BLINK_FREQUENCY, LED_BRIGHTNESS, LED_COLOR, LED_COLOR_TYPE, LED_TYPE, NucWmiError
from nuc_wmi.get_led import METHOD_ID, get_led
from nuc_wmi.utils import defined_indexes

import nuc_wmi


class TestGetLed(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.get_led`

    Methods:
        setUp: Unit test initialization.
        test_get_led: Tests that it sends the expected byte list to the control file, tests that the returned
                      control file response is properly processed, tests that it raises an exception when the
                      control file returns an error code.
    """

    def setUp(self):
        """
        Initializes the unit tests;
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('nuc_wmi.get_led.read_control_file')
    @patch('nuc_wmi.get_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.get_led.write_control_file')
    def test_get_led(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec, nuc_wmi_read_control_file):
        """
        Tests that `get_led` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.get_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that get_led sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Get legacy S0 Ring LED which is set to Yellow, Always on, and 63% brightness
        expected_write_byte_list = [
            METHOD_ID,
            LED_TYPE['legacy'].index('S0 Ring LED')
        ]
        read_byte_list = [
            0x00,
            LED_BRIGHTNESS['legacy'].index('63'),
            LED_BLINK_FREQUENCY['legacy'].index('Always on'),
            LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Yellow')
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('index', False)

        returned_get_led = get_led(
            {},
            LED_TYPE['legacy'].index('S0 Ring LED'),
            control_file=None,
            debug=False
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_get_led, tuple(read_byte_list[1:]))


    @patch('nuc_wmi.get_led.read_control_file')
    @patch('nuc_wmi.get_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.get_led.write_control_file')
    def test_get_led2(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                      nuc_wmi_read_control_file):
        """
        Tests that `get_led` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.get_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 2: Test that get_led raises an exception when the control file returns an
        #           error code.

        # Incorrect led
        expected_write_byte_list = [
            METHOD_ID,
            len(LED_TYPE['legacy']) # Set incorrect led
        ]
        read_byte_list = [0xE2, 0x00, 0x00, 0x00] # Return undefined device

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('index', False)

        with self.assertRaises(NucWmiError) as err:
            get_led(
                {},
                len(LED_TYPE['legacy']),
                control_file=None,
                debug=False
            ) # Set incorrect led

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(str(err.exception), 'Error (Undefined device)')


    @patch('nuc_wmi.get_led.read_control_file')
    @patch('nuc_wmi.get_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.get_led.write_control_file')
    def test_get_led3(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                      nuc_wmi_read_control_file):
        """
        Tests that `get_led` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.get_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 3: Test that get_led returns a non null value when we enable out of bound
        #           value recovery in NUC WMI specification.

        led_color_type = LED_COLOR_TYPE['legacy']['S0 Ring LED']

        brightness_range = defined_indexes(LED_BRIGHTNESS['legacy'])
        frequency_range = defined_indexes(LED_BLINK_FREQUENCY['legacy'])
        color_range = defined_indexes(LED_COLOR['legacy'][led_color_type])

        expected_write_byte_list = [
            METHOD_ID,
            LED_TYPE['legacy'].index('S0 Ring LED')
        ]
        metadata = {
            'brightness_range': brightness_range,
            'frequency_range': frequency_range,
            'color_range': color_range
        }
        read_byte_list = [0x00, 0x00, 0x00, 0x00]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('index', True)

        returned_get_led = get_led(
            {},
            LED_TYPE['legacy'].index('S0 Ring LED'),
            control_file=None,
            debug=False,
            metadata=metadata
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_get_led, tuple([0x00, 0x01, 0x00]))


    @patch('nuc_wmi.get_led.read_control_file')
    @patch('nuc_wmi.get_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.get_led.write_control_file')
    def test_get_led4(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                      nuc_wmi_read_control_file):
        """
        Tests that `get_led` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.get_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 4: Test that get_led returns values inside specification bounds when we enable out of bound
        #           value recovery in NUC WMI specification.

        led_color_type = LED_COLOR_TYPE['legacy']['S0 Ring LED']

        brightness_range = defined_indexes(LED_BRIGHTNESS['legacy'])
        frequency_range = defined_indexes(LED_BLINK_FREQUENCY['legacy'])
        color_range = defined_indexes(LED_COLOR['legacy'][led_color_type])

        expected_write_byte_list = [
            METHOD_ID,
            LED_TYPE['legacy'].index('S0 Ring LED')
        ]
        metadata = {
            'brightness_range': brightness_range,
            'frequency_range': frequency_range,
            'color_range': color_range
        }
        read_byte_list = [0x00, 0xFF, 0xFF, 0xFF]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('index', True)

        returned_get_led = get_led(
            {},
            LED_TYPE['legacy'].index('S0 Ring LED'),
            control_file=None,
            debug=False,
            metadata=metadata
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_get_led, tuple([0x00, 0x01, 0x00]))


    @patch('nuc_wmi.get_led.read_control_file')
    @patch('nuc_wmi.get_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.get_led.write_control_file')
    def test_get_led5(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                      nuc_wmi_read_control_file):
        """
        Tests that `get_led` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.get_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.get_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.get_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 5: Test that get_led returns values inside specification bounds (except frequency) when we enable out
        #           of bound value recovery in NUC WMI specification.
        led_color_type = LED_COLOR_TYPE['legacy']['S0 Ring LED']

        brightness_range = defined_indexes(LED_BRIGHTNESS['legacy'])
        color_range = defined_indexes(LED_COLOR['legacy'][led_color_type])

        expected_write_byte_list = [
            METHOD_ID,
            LED_TYPE['legacy'].index('S0 Ring LED')
        ]
        metadata = {
            'brightness_range': brightness_range,
            'color_range': color_range
        }
        read_byte_list = [0x00, 0xFF, 0x01, 0xFF]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('index', True)

        returned_get_led = get_led(
            {},
            LED_TYPE['legacy'].index('S0 Ring LED'),
            control_file=None,
            debug=False,
            metadata=metadata
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_get_led, tuple([0x00, 0x01, 0x00]))
