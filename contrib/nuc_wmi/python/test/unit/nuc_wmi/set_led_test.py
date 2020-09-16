"""
The `test.unit.nuc_wmi.set_led_test` module provides unit tests for the functions in
`nuc_wmi.set_led`.

Classes:
    TestSetLed: A unit test class for the functions in `nuc_wmi.set_led`.
"""

import unittest

from mock import patch

from nuc_wmi import LED_BLINK_FREQUENCY, LED_BRIGHTNESS, LED_COLOR, LED_COLOR_TYPE, LED_TYPE, NucWmiError
from nuc_wmi.set_led import METHOD_ID, set_led

import nuc_wmi


class TestSetLed(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.set_led`

    Methods:
        setUp: Unit test initialization.
        test_set_led: Tests that it sends the expected byte list to the control file, tests that the returned
                      control file response is properly processed, tests that it raises an exception when the
                      control file returns an error code.
    """

    def setUp(self):
        """
        Initializes the unit tests;
        """

        self.maxDiff = None


    @patch('nuc_wmi.set_led.read_control_file')
    @patch('nuc_wmi.set_led.write_control_file')
    def test_set_led(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `set_led` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.set_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.set_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that set_led sends the expected byte string to the control file
        #           and that the returned control file response is properly processed.

        # Set legacy S0 Ring LED to Yellow, Always on, and 63% brightness
        expected_write_byte_list = [
            METHOD_ID,
            LED_TYPE['legacy'].index('S0 Ring LED'),
            LED_BRIGHTNESS['legacy'].index('63'),
            LED_BLINK_FREQUENCY['legacy'].index('Always on'),
            LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Yellow')
        ]
        read_byte_list = [0x00, 0x00, 0x00, 0x00]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_set_led = set_led(
            LED_TYPE['legacy'].index('S0 Ring LED'),
            LED_BRIGHTNESS['legacy'].index('63'),
            LED_BLINK_FREQUENCY['legacy'].index('Always on'),
            LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Yellow')
        )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(returned_set_led, None)

        # Reset
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()

        # Branch 2: Test that set_led raises an exception when the control file returns an
        #           error code.

        # Incorrect led
        expected_write_byte_list = [
            METHOD_ID,
            len(LED_TYPE['legacy']), # Set incorrect led
            LED_BRIGHTNESS['legacy'].index('63'),
            LED_BLINK_FREQUENCY['legacy'].index('Always on'),
            LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Yellow')
        ]
        read_byte_list = [0xE1, 0x00, 0x00, 0x00] # Return function not supported

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            returned_set_led = set_led(
                len(LED_TYPE['legacy']), # Set incorrect led
                LED_BRIGHTNESS['legacy'].index('63'),
                LED_BLINK_FREQUENCY['legacy'].index('Always on'),
                LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Yellow')
            )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(str(err.exception), 'Error (Function not supported)')

        # Reset
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()

        # Incorrect brightness
        expected_write_byte_list = [
            METHOD_ID,
            LED_TYPE['legacy'].index('S0 Ring LED'),
            len(LED_BRIGHTNESS['legacy']), # Set incorrect brightness
            LED_BLINK_FREQUENCY['legacy'].index('Always on'),
            LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Yellow')
        ]
        read_byte_list = [0xE4, 0x00, 0x00, 0x00] # Return invalid parameter

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            returned_set_led = set_led(
                LED_TYPE['legacy'].index('S0 Ring LED'),
                len(LED_BRIGHTNESS['legacy']), # Set incorrect brightness
                LED_BLINK_FREQUENCY['legacy'].index('Always on'),
                LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Yellow')
            )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')

        # Reset
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()

        # Incorrect frequency
        expected_write_byte_list = [
            METHOD_ID,
            LED_TYPE['legacy'].index('S0 Ring LED'),
            LED_BRIGHTNESS['legacy'].index('63'),
            len(LED_BLINK_FREQUENCY['legacy']), # Set incorrect frequency
            LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Yellow')
        ]
        read_byte_list = [0x00, 0xE4, 0x00, 0x00] # Return invalid parameter

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            returned_set_led = set_led(
                LED_TYPE['legacy'].index('S0 Ring LED'),
                LED_BRIGHTNESS['legacy'].index('63'),
                len(LED_BLINK_FREQUENCY['legacy']), # Set incorrect frequency
                LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']].index('Yellow')
            )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')

        # Reset
        nuc_wmi_read_control_file.reset_mock()
        nuc_wmi_write_control_file.reset_mock()

        # Incorrect color
        expected_write_byte_list = [
            METHOD_ID,
            LED_TYPE['legacy'].index('S0 Ring LED'),
            LED_BRIGHTNESS['legacy'].index('63'),
            LED_BLINK_FREQUENCY['legacy'].index('Always on'),
            len(LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']]) # Set incorrect color
        ]
        read_byte_list = [0x00, 0x00, 0xE4, 0x00] # Return invalid parameter

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            returned_set_led = set_led(
                LED_TYPE['legacy'].index('S0 Ring LED'),
                LED_BRIGHTNESS['legacy'].index('63'),
                LED_BLINK_FREQUENCY['legacy'].index('Always on'),
                len(LED_COLOR['legacy'][LED_COLOR_TYPE['legacy']['S0 Ring LED']]) # Set incorrect color
            )

        nuc_wmi_write_control_file.assert_called_with(expected_write_byte_list, control_file=None)

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')
