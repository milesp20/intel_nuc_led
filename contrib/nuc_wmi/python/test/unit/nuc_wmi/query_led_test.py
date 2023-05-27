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
from nuc_wmi.utils import defined_indexes

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
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_color_type(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                                  nuc_wmi_read_control_file):
        """
        Tests that `query_led_color_type` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that query_led_color_type send the expected byte string to the control file
        #           and that the returned control file response is properly processed with a return type of bitmap.

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
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        returned_query_led_color_type = query_led_color_type(
            {},
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_query_led_color_type, expected_query_led_color_type)


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_color_type2(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                                   nuc_wmi_read_control_file):
        """
        Tests that `query_led_color_type` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 2: Test that query_led_color_type raises an exception when the control file returns an
        #           error code.

        # Incorrect led
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
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        with self.assertRaises(NucWmiError) as err:
            query_led_color_type(
                {},
                len(LED_TYPE['new']), # Incorrect led index
                control_file=None,
                debug=False,
                metadata=None
            )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_color_type3(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                                   nuc_wmi_read_control_file):
        """
        Tests that `query_led_color_type` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

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
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        returned_query_led_color_type = query_led_color_type(
            {},
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_query_led_color_type, expected_query_led_color_type)


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_color_type4(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                                   nuc_wmi_read_control_file):
        """
        Tests that `query_led_color_type` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 4: Test that query_led_color_type raises an exception when an invalid bitmap is read
        #           from the control file with more than one led color type.

        # Query HDD LED that returns a color type of Single-color LED
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_color_type'),
            LED_TYPE['new'].index('HDD LED')
        ]
        read_byte_list = [
            0x00,
            0x09,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        with self.assertRaises(NucWmiError) as err:
            query_led_color_type(
                {},
                LED_TYPE['new'].index('HDD LED'),
                control_file=None,
                debug=False,
                metadata=None
            )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(
            str(err.exception),
            'Error (Intel NUC WMI query_led_color_type function returned either no led color type '
            'or multiple led color types in bitmap)'
        )


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_color_type5(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                                   nuc_wmi_read_control_file):
        """
        Tests that `query_led_color_type` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 5: Test that query_led_color_type send the expected byte string to the control file
        #           and that the returned control file response is properly processed with a return type of index.

        # Query HDD LED that returns a color type of Dual-color Blue / White
        expected_query_led_color_type = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_color_type'),
            LED_TYPE['new'].index('HDD LED')
        ]
        read_byte_list = [
            0x00,
            0x01,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('index', False)

        returned_query_led_color_type = query_led_color_type(
            {},
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_query_led_color_type, expected_query_led_color_type)


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_color_type6(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                                   nuc_wmi_read_control_file):
        """
        Tests that `query_led_color_type` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 6: Test that query_led_color_type raises the expected exception when an invalid LED color type is
        #           returned.

        # Query HDD LED that returns a color type of Dual-color Blue / White
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_color_type'),
            LED_TYPE['new'].index('HDD LED')
        ]
        led_color_type_range = defined_indexes(LED_COLOR_TYPE['new'])
        # Invalid LED color type
        read_byte_list = [
            0x00,
            0x09,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('index', False)

        with self.assertRaises(NucWmiError) as err:
            query_led_color_type(
                {},
                LED_TYPE['new'].index('HDD LED'),
                control_file=None,
                debug=False,
                metadata=None
            )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(
            str(err.exception),
            'Error (Intel NUC WMI query_led_color_type function returned invalid LED color type of %i, '
            'expected one of %s)' % (0x09, str(led_color_type_range))
        )


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_color_type7(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                                   nuc_wmi_read_control_file):
        """
        Tests that `query_led_color_type` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 7: Test that query_led_color_type returns the query_led_color_type hint.

        # Query HDD LED that returns a color type of Dual-color Blue / White
        expected_query_led_color_type = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_spec = {
            'function_return_type': {
                'query_led_color_type': 'index',
            },
            'function_oob_return_value_recover': {
                'query_led_color_type': False,
            },
            'led_hints': {
                'color_type': {
                    'HDD LED': 'Dual-color Blue / White',
                    'Power Button LED': 'Dual-color Blue / Amber'
                }
            }
        }
        read_byte_list = [
            0x00,
            0x02,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        returned_query_led_color_type = query_led_color_type(
            nuc_wmi_spec,
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )

        nuc_wmi_write_control_file.assert_not_called()

        self.assertEqual(returned_query_led_color_type, expected_query_led_color_type)


    @patch('nuc_wmi.query_led.query_led_color_type')
    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_control_items(
            self,
            nuc_wmi_write_control_file,
            nuc_wmi_verify_nuc_wmi_function_spec,
            nuc_wmi_read_control_file,
            nuc_wmi_query_led_color_type
    ):
        """
        Tests that `query_led_control_items` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

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

        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        returned_query_led_control_items = query_led_control_items(
            {},
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
            control_file=None,
            debug=False,
            metadata=None
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )
        nuc_wmi_query_led_color_type.assert_called_with(
            {},
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )

        self.assertEqual(returned_query_led_control_items, expected_query_led_control_items)


    @patch('nuc_wmi.query_led.query_led_color_type')
    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_control_items2(
            self,
            nuc_wmi_write_control_file,
            nuc_wmi_verify_nuc_wmi_function_spec,
            nuc_wmi_read_control_file,
            nuc_wmi_query_led_color_type
    ):
        """
        Tests that `query_led_control_items` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 2: Test that query_led_control_items send the expected byte string to the control file
        #           and that the returned control file response is properly processed.

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

        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        returned_query_led_control_items = query_led_control_items(
            {},
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION_DISABLED,
            control_file=None,
            debug=False,
            metadata=None
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )
        nuc_wmi_query_led_color_type.assert_called_with(
            {},
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )

        self.assertEqual(returned_query_led_control_items, expected_query_led_control_items)


    @patch('nuc_wmi.query_led.query_led_color_type')
    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_control_items3(
            self,
            nuc_wmi_write_control_file,
            nuc_wmi_verify_nuc_wmi_function_spec,
            nuc_wmi_read_control_file,
            nuc_wmi_query_led_color_type
    ):
        """
        Tests that `query_led_control_items` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 3: Test that query_led_control_items raises an exception when the control file returns an
        #           error code.

        # Incorrect led
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

        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        with self.assertRaises(NucWmiError) as err:
            query_led_control_items(
                {},
                len(LED_TYPE['new']), # Invalid led index
                LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
                control_file=None,
                debug=False,
                metadata=None
            )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )
        nuc_wmi_query_led_color_type.assert_called_with(
            {},
            len(LED_TYPE['new']),
            control_file=None,
            debug=False,
            metadata=None
        )

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')


    @patch('nuc_wmi.query_led.query_led_color_type')
    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_control_items4(
            self,
            nuc_wmi_write_control_file,
            nuc_wmi_verify_nuc_wmi_function_spec,
            nuc_wmi_read_control_file,
            nuc_wmi_query_led_color_type
    ):
        """
        Tests that `query_led_control_items` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.query_led_color_type is nuc_wmi_query_led_color_type)
        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 4: Test that query_led_control_items raises an exception when returned bitmap exceeds
        #           the number of bits supported by the selected led type and led indicator option.

        # Query control items of HDD LED with HDD Activity Indicator
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_control_items'),
            LED_TYPE['new'].index('HDD LED'),
            LED_INDICATOR_OPTION.index('HDD Activity Indicator')
        ]
        read_byte_list = [
            0x00,
            0xFF,
            0xFF,
            0xFF
        ]

        nuc_wmi_query_led_color_type.return_value = LED_COLOR_TYPE['new'].index('Dual-color Blue / White')
        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        with self.assertRaises(NucWmiError) as err:
            query_led_control_items(
                {},
                LED_TYPE['new'].index('HDD LED'),
                LED_INDICATOR_OPTION.index('HDD Activity Indicator'),
                control_file=None,
                debug=False,
                metadata=None
            )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )
        nuc_wmi_query_led_color_type.assert_called_with(
            {},
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )

        self.assertEqual(
            str(err.exception),
            'Error (Intel NUC WMI query_led_control_items function returned more led control items than ' +
            'supported for the led type and led indicator provided)'
        )


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_indicator_options(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                                         nuc_wmi_read_control_file):
        """
        Tests that `query_led_indicator_options` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
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
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        returned_query_led_indicator_options = query_led_indicator_options(
            {},
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_query_led_indicator_options, expected_query_led_indicator_options)


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_indicator_options2(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                                          nuc_wmi_read_control_file):
        """
        Tests that `query_led_indicator_options` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 2: Test that query_led_indicator_options raises an exception when the control file returns an
        #           error code.

        # Incorrect led
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
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        with self.assertRaises(NucWmiError) as err:
            query_led_indicator_options(
                {},
                len(LED_TYPE['new']), # Incorrect led index
                control_file=None,
                debug=False,
                metadata=None
            )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(str(err.exception), 'Error (Invalid Parameter)')


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_indicator_options3(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                                          nuc_wmi_read_control_file):
        """
        Tests that `query_led_indicator_options` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 3: Test that query_led_indicator_options raises an exception when the control file returns
        #           more indicator options in the bitmap than are available for the provided led type.

        # Query HDD LED indicator options
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_led_indicator_options'),
            LED_TYPE['new'].index('HDD LED')
        ]
        read_byte_list = [
            0x00,
            0xFF,
            0xFF,
            0xFF
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        with self.assertRaises(NucWmiError) as err:
            query_led_indicator_options(
                {},
                LED_TYPE['new'].index('HDD LED'),
                control_file=None,
                debug=False,
                metadata=None
            )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(
            str(err.exception),
            'Error (Intel NUC WMI query_led_indicator_options function returned more led indicator options than ' +
            'supported for the led type provided)'
        )


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_led_indicator_options4(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                                          nuc_wmi_read_control_file):
        """
        Tests that `query_led_indicator_options` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 4: Test that query_led_indicator_options returns query_led_indicator_options_hint.

        # Query HDD LED indicator options
        expected_query_led_indicator_options = [1, 4]
        nuc_wmi_spec = {
            'function_return_type': {
                'query_led_indicator_options': 'bitmap'
            },
            'function_oob_return_value_recover': {
                'query_led_indicator_options': False
            },
            'led_hints': {
                'indicator_options': {
                    'HDD LED': [
                        'HDD Activity Indicator',
                        'Software Indicator'
                    ],
                    'Power Button LED': [
                        'HDD Activity Indicator',
                        'Power State Indicator',
                        'Software Indicator'
                    ]
                }
            }
        }
        read_byte_list = [
            0x00,
            0x12,
            0x00,
            0x00
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        returned_query_led_indicator_options = query_led_indicator_options(
            nuc_wmi_spec,
            LED_TYPE['new'].index('HDD LED'),
            control_file=None,
            debug=False,
            metadata=None
        )

        nuc_wmi_write_control_file.assert_not_called()

        self.assertEqual(returned_query_led_indicator_options, expected_query_led_indicator_options)


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_leds(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                        nuc_wmi_read_control_file):
        """
        Tests that `query_leds` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
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
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        returned_query_leds = query_leds(
            {},
            control_file=None,
            debug=False,
            metadata=None
        )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(returned_query_leds, expected_query_leds)


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_leds2(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                         nuc_wmi_read_control_file):
        """
        Tests that `query_leds` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 2: Test that query_leds raises an exception when the control file returns an
        #           error code.

        # Incorrect led
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
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        with self.assertRaises(NucWmiError) as err:
            query_leds(
                {},
                control_file=None,
                debug=False,
                metadata=None
            )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(str(err.exception), 'Error (Function not supported)')


    @patch('nuc_wmi.query_led.read_control_file')
    @patch('nuc_wmi.query_led.verify_nuc_wmi_function_spec')
    @patch('nuc_wmi.query_led.write_control_file')
    def test_query_leds3(self, nuc_wmi_write_control_file, nuc_wmi_verify_nuc_wmi_function_spec,
                         nuc_wmi_read_control_file):
        """
        Tests that `query_leds` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.query_led.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.query_led.verify_nuc_wmi_function_spec is nuc_wmi_verify_nuc_wmi_function_spec)
        self.assertTrue(nuc_wmi.query_led.write_control_file is nuc_wmi_write_control_file)

        # Branch 3: Test that query_leds raises an exception when the control file returns
        #           a bitmap with more led types than supported.

        # Query HDD LED indicator options
        expected_write_byte_list = [
            METHOD_ID,
            QUERY_TYPE.index('query_leds')
        ]
        read_byte_list = [
            0x00,
            0xFF,
            0xFF,
            0xFF
        ]

        nuc_wmi_read_control_file.return_value = read_byte_list
        nuc_wmi_verify_nuc_wmi_function_spec.return_value = ('bitmap', False)

        with self.assertRaises(NucWmiError) as err:
            query_leds(
                {},
                control_file=None,
                debug=False,
                metadata=None
            )

        nuc_wmi_write_control_file.assert_called_with(
            expected_write_byte_list,
            control_file=None,
            debug=False
        )

        self.assertEqual(
            str(err.exception),
            'Error (Intel NUC WMI query_leds function returned more led types than supported)'
        )
