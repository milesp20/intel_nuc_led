"""
The `test.unit.nuc_wmi.utils_test` module provides unit tests for the functions in
`nuc_wmi.utils`.

Classes:
    TestUtils: A unit test class for the functions in `nuc_wmi.utils`.
"""

import fcntl
import json
import tempfile
import unittest

from threading import Thread

import pkg_resources

from mock import patch

from nuc_wmi import LED_COLOR_TYPE, LED_INDICATOR_OPTION, LED_TYPE, NucWmiError
from nuc_wmi.utils import acquire_file_lock, byte_list_to_bitmap, byte_list_to_index, defined_indexes, load_nuc_wmi_spec
from nuc_wmi.utils import NUC_WMI_SPEC_FILE, query_led_color_type_hint, query_led_indicator_options_hint
from nuc_wmi.utils import query_led_rgb_color_type_dimensions_hint, verify_nuc_wmi_function_spec

import nuc_wmi


class TestUtils(unittest.TestCase): # pylint: disable=too-many-public-methods
    """
    A unit test class for the functions of `nuc_wmi.utils`

    Methods:
        setUp: Unit test initialization.
        test_acquire_file_lock: Tests that `acquire_file_lock` raises the expected exception when it cannot acquire
                                the lock file and that it successfully acquires the lock file otherwise.
        test_byte_list_to_bitmap: Tests that `byte_list_to_bitmap` raises the expected exception when any of the ints in
                                  byte list are outside of the 0-255 range, tests that it returns the proper bitmap
                                  string when the byte list is int or str, tests that returned bitmaps are properly
                                  explicitly padded to 8 bits, tests that we get an exception of the inputs are not
                                  proper ints.
        test_byte_list_to_index: Tests that `byte_list_index` raises the expected exception when the byte list type is
                                 invalid, that valid indexes of enabled bits are returned for a byte list type of
                                 bitmap, and that a valid integer index is return for a byte list of index.
        test_defined_indexes: Tests that `defined_indexes` returns the indices of indexes with defined values.
        test_load_nuc_wmi_spec: Test that `load_nuc_wmi_spec` returns the NUC WMI specification configuration correctly.
        test_query_led_color_type_hint: Tests that `query_led_color_type_hint` returns the expected exceptions, return
                                        values, or outputs.
        test_query_led_indicator_options_hint: Tests that `query_led_indicator_options_hint` returns the expected
                                               exceptions, return values, or outputs.
        test_query_led_rgb_color_type_dimensions_hint: Tests that `query_led_rgb_color_type_dimensions_hint` returns the
                                                       expected exceptions, return values, or outputs.
        test_verify_nuc_wmi_function_spec: Tests that `verify_nuc_wmi_function_spec` raises the expected exception when
                                           the function_return_type or function_oob_return_recover values are undefined
                                           or unsupport by the NUC WMI method or the expected tuple for
                                           function_return_type and function_oob_return_recover values is returned.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name


    def test_acquire_file_lock(self):
        """
        Test that `acquire_file_lock` returns the expected exceptions, return values, or outputs.
        """

        # Branch 1: Test that `acquire_file_lock` can successfully acquire a file lock and returns None.

        with tempfile.NamedTemporaryFile(delete=True) as temp_lock_file:
            returned_acquire_file_lock = acquire_file_lock(temp_lock_file)

            self.assertEqual(returned_acquire_file_lock, None)


    def test_acquire_file_lock2(self):
        """
        Test that `acquire_file_lock` returns the expected exceptions, return values, or outputs.
        """

        # Branch 2: Test that `acquire_file_lock` raises an exception when the file lock is already acquired.

        with tempfile.NamedTemporaryFile(delete=True) as temp_lock_file:
            returned_acquire_file_lock = acquire_file_lock(temp_lock_file)

            self.assertEqual(returned_acquire_file_lock, None)

            with open(temp_lock_file.name, 'w', encoding='utf8') as temp_lock_file2:
                with self.assertRaises(NucWmiError) as err:
                    acquire_file_lock(temp_lock_file2)

                self.assertEqual(
                    str(err.exception),
                    'Error (Intel NUC WMI failed to acquire lock file %s: %s)' % \
                    (temp_lock_file2.name, '[Errno 11] Resource temporarily unavailable')
                )


    def test_acquire_file_lock3(self):
        """
        Test that `acquire_file_lock` returns the expected exceptions, return values, or outputs.
        """

        # Branch 3: Test that `acquire_file_lock` can successfully acquire a blocking file lock and returns None.

        with tempfile.NamedTemporaryFile(delete=True) as temp_lock_file:
            returned_acquire_file_lock = acquire_file_lock(temp_lock_file, blocking_file_lock=True)

            self.assertEqual(returned_acquire_file_lock, None)


    def test_acquire_file_lock4(self):
        """
        Test that `acquire_file_lock` returns the expected exceptions, return values, or outputs.
        """

        # Branch 4: Test that `acquire_file_lock` hangs when acquiring a blocking file lock on file thats already
        #           locked.

        with tempfile.NamedTemporaryFile(delete=True) as temp_lock_file:
            blocking_thread = None
            returned_acquire_file_lock = acquire_file_lock(temp_lock_file)

            self.assertEqual(returned_acquire_file_lock, None)

            with open(temp_lock_file.name, 'w', encoding='utf8') as temp_lock_file2:
                blocking_thread = Thread(
                    target=acquire_file_lock,
                    args=[temp_lock_file2],
                    kwargs={'blocking_file_lock': True}
                )

                blocking_thread.start()
                blocking_thread.join(10.0)

                self.assertEqual(blocking_thread.is_alive(), True)


            fcntl.flock(temp_lock_file.fileno(), fcntl.LOCK_UN)

            blocking_thread.join(2.0)

            self.assertEqual(blocking_thread.is_alive(), False)


    def test_byte_list_to_bitmap(self):
        """
        Tests that `byte_list_to_bitmap` returns the expected exceptions, return values, or outputs.
        """

        # Branch 1: Test that `byte_list_to_bitmap` raises an exception when any of the ints provided is outside the
        #           0-255 range.
        with self.assertRaises(ValueError) as err:
            byte_list_to_bitmap([0xFFF])

        self.assertEqual(str(err.exception), 'int byte values must be 0-255')


    def test_byte_list_to_bitmap2(self):
        """
        Tests that `byte_list_to_bitmap` returns the expected exceptions, return values, or outputs.
        """

        # Branch 2: Test that `byte_list_to_bitmap` returns the proper bitmap string regardless of whether the inputs
        #           are ints or str.
        self.assertEqual(
            byte_list_to_bitmap([0x0D, 0x0E, 0x0A, 0x0D]),
            '00001101000011100000101000001101'
        )

        self.assertEqual(
            byte_list_to_bitmap(['13', '14', '10', '13']),
            '00001101000011100000101000001101'
        )


    def test_byte_list_to_bitmap3(self):
        """
        Tests that `byte_list_to_bitmap` returns the expected exceptions, return values, or outputs.
        """

        # Branch 3: Tests that `byte_list_to_bitmap` explicitly pads each byte to 8 bits.
        self.assertEqual(
            byte_list_to_bitmap([0x00]),
            '00000000'
        )


    def test_byte_list_to_bitmap4(self):
        """
        Tests that `byte_list_to_bitmap` returns the expected exceptions, return values, or outputs.
        """

        # Branch 4: Test that `byte_list_bitmap` raises an exception when the input value is not an int
        with self.assertRaises(ValueError):
            byte_list_to_bitmap(["0xZ"])


    def test_byte_list_to_index(self):
        """
        Tests that `byte_list_to_index` returns the expected exceptions, return values, or outputs.
        """

        byte_list = [0x0D, 0x0E, 0x0A, 0x0D]
        byte_list_type = 'invalid_byte_list_type'

        # Branch 1: Test that `byte_list_index` raises an exception when the return type is invalid.
        with self.assertRaises(NucWmiError) as err:
            byte_list_to_index(byte_list, byte_list_type)

        self.assertEqual(
            str(err.exception),
            'Error (Invalid byte list type specified, cannot cast byte list to index: %s)' % byte_list_type
        )


    def test_byte_list_to_index2(self):
        """
        Tests that `byte_list_to_index` returns the expected exceptions, return values, or outputs.
        """

        byte_list = [0x0D, 0x0E, 0x0A, 0x0D]
        byte_list_indexes = [0, 2, 3, 9, 11, 17, 18, 19, 24, 26, 27]
        byte_list_type = 'bitmap'

        # Branch 2: Test that `byte_list_index` casts the byte list to a bitmap and returns indexes of enabled bits.
        index = byte_list_to_index(byte_list, byte_list_type)

        self.assertEqual(
            index,
            byte_list_indexes
        )


    def test_byte_list_to_index3(self):
        """
        Tests that `byte_list_to_index` returns the expected exceptions, return values, or outputs.
        """

        byte_list = [0x0D, 0x0E, 0x0A, 0x0D]
        byte_list_index = 219023885
        byte_list_type = 'index'

        # Branch 3: Test that `byte_list_index` casts the byte list to a index and returns an integer.
        index = byte_list_to_index(byte_list, byte_list_type)

        self.assertEqual(
            index,
            byte_list_index
        )


    def test_defined_indexes(self):
        """
        Tests that `defined_indexes` returns the expected exceptions, return values, or outputs.
        """

        # Branch 1: Test that a list input returns a list of indexes with non None values.
        defined_list = [None, "some value", "some value 2"]
        expected_defined_indexes = [1, 2]

        returned_defined_indexes = defined_indexes(defined_list)

        self.assertEqual(
            returned_defined_indexes,
            expected_defined_indexes
        )


    def test_defined_indexes2(self):
        """
        Tests that `defined_indexes` returns the expected exceptions, return values, or outputs.
        """

        # Branch 2: Test that a non list input returns an emptylist of indexes.
        defined_list = None
        expected_defined_indexes = []

        returned_defined_indexes = defined_indexes(defined_list)

        self.assertEqual(
            returned_defined_indexes,
            expected_defined_indexes
        )


    @patch('nuc_wmi.utils.NUC_WMI_SPEC_FILE',
           ['/tmp/nonexistant_file',
            pkg_resources.resource_filename('nuc_wmi', 'etc/nuc_wmi/nuc_wmi_spec/nuc_wmi_spec.json')])
    def test_load_nuc_wmi_spec(self):
        """
        Tests that `load_nuc_wmi_sec` returns the expected exceptions, return values, or outputs.
        """

        # Branch 1: Test that the default NUC WMI spec file in the pip package is returned by package resources.
        with open(NUC_WMI_SPEC_FILE[-1], 'r', encoding='utf8') as fin:
            nuc_wmi_spec_default = json.load(fin)

        nuc_wmi_spec = load_nuc_wmi_spec()

        self.assertDictEqual(
            nuc_wmi_spec_default,
            nuc_wmi_spec
        )


    @patch('nuc_wmi.utils.NUC_WMI_SPEC_FILE', [])
    def test_load_nuc_wmi_spec2(self):
        """
        Tests that `load_nuc_wmi_sec` returns the expected exceptions, return values, or outputs.
        """

        # Branch 2: Test that an exception is raised if there is no NUC WMI spec file found
        with self.assertRaises(NucWmiError) as err:
            load_nuc_wmi_spec()

        self.assertEqual(
            str(err.exception),
            'Error (Intel NUC WMI failed to find NUC WMI spec configuration file: %s)' % str([])
        )


    def test_load_nuc_wmi_spec3(self):
        """
        Tests that `load_nuc_wmi_sec` returns the expected exceptions, return values, or outputs.
        """

        # Branch 3: Test that an exception is raised if the NUC WMI spec file has invalid schema
        with tempfile.NamedTemporaryFile(delete=True) as temp_nuc_wmi_spec_file:
            with patch('nuc_wmi.utils.NUC_WMI_SPEC_FILE', [temp_nuc_wmi_spec_file.name]):
                with open(temp_nuc_wmi_spec_file.name, 'w', encoding='utf8') as fout:
                    fout.write("{}")

                with self.assertRaises(NucWmiError) as err:
                    load_nuc_wmi_spec()

                self.assertEqual(
                    str(err.exception),
                    'Error (Intel NUC WMI NUC WMI spec configuration file schema is invalid: %s)' % \
                    (temp_nuc_wmi_spec_file.name)
                )


    @patch('nuc_wmi.utils.NUC_WMI_SPEC_FILE',
           [pkg_resources.resource_filename('nuc_wmi', 'etc/nuc_wmi/nuc_wmi_spec/nuc_wmi_spec.json')])
    @patch('nuc_wmi.utils.json.load')
    def test_load_nuc_wmi_spec4(self, json_load):
        """
        Tests that `load_nuc_wmi_sec` returns the expected exceptions, return values, or outputs.
        """

        self.assertTrue(nuc_wmi.utils.json.load is json_load)

        json_load.side_effect = Exception('json.load error')

        # Branch 4: Test that an exception is raised if the NUC WMI spec file json loading fails
        with self.assertRaises(NucWmiError) as err:
            load_nuc_wmi_spec()

        self.assertEqual(
            str(err.exception),
            'Error (Intel NUC WMI failed to load NUC WMI spec configuration file %s: %s)' % \
                (pkg_resources.resource_filename('nuc_wmi', 'etc/nuc_wmi/nuc_wmi_spec/nuc_wmi_spec.json'),
                 'json.load error')
        )


    def test_query_led_color_type_hint(self):
        """
        Tests that `query_led_color_type_hint` returns the expected exceptions, return values, or outputs.
        """

        # Branch 1: Test that the LED color type hint is properly returned from the NUC WMI spec file.
        led_type = 'Power Button LED'
        nuc_wmi_spec = {
            'led_hints': {
                'color_type': {
                    'HDD LED': 'RGB-color',
                    'Power Button LED': 'Dual-color Blue / Amber',
                    'RGB Header': 'RGB-color'
                }
            }
        }

        led_color_type_index = query_led_color_type_hint(
            nuc_wmi_spec,
            LED_TYPE['new'].index(led_type)
        )

        self.assertEqual(
            led_color_type_index,
            LED_COLOR_TYPE['new'].index(
                nuc_wmi_spec['led_hints']['color_type'][led_type]
            )
        )


    def test_query_led_color_type_hint2(self):
        """
        Tests that `query_led_color_type_hint` returns the expected exceptions, return values, or outputs.
        """

        # Branch 2: Test that the LED color type hint returns None for invalid LED type from the NUC WMI spec file.
        nuc_wmi_spec = {
            'led_hints': {
                'color_type': {
                    'HDD LED': 'RGB-color',
                    'Power Button LED': 'Dual-color Blue / Amber',
                    'RGB Header': 'RGB-color'
                }
            }
        }

        led_color_type_index = query_led_color_type_hint(nuc_wmi_spec, 10)

        self.assertEqual(
            led_color_type_index,
            None
        )


    def test_query_led_indicator_options_hint(self):
        """
        Tests that `query_led_indicator_options_hint` returns the expected exceptions, return values, or outputs.
        """

        # Branch 1: Test that the LED indicator options hint is properly returned from the NUC WMI spec file.
        expected_indicator_options_indexes = []
        led_type = 'Power Button LED'
        nuc_wmi_spec = {
            'led_hints': {
                'indicator_options': {
                    'HDD LED': [
                        'Disable',
                        'HDD Activity Indicator',
                        'Software Indicator'
                    ],
                    'Power Button LED': [
                        'Disable',
                        'HDD Activity Indicator',
                        'Power State Indicator',
                        'Software Indicator'
                    ],
                    'RGB Header': [
                        'Disable',
                        'HDD Activity Indicator',
                        'Power State Indicator',
                        'Software Indicator'
                    ]
                }
            }
        }

        for index, indicator_option in enumerate(LED_INDICATOR_OPTION):
            if indicator_option in nuc_wmi_spec['led_hints']['indicator_options'][led_type]:
                expected_indicator_options_indexes.append(index)

        expected_indicator_options_indexes.sort()

        indicator_options_indexes = query_led_indicator_options_hint(
            nuc_wmi_spec,
            LED_TYPE['new'].index(led_type)
        )

        self.assertListEqual(
            indicator_options_indexes,
            expected_indicator_options_indexes
        )


    def test_query_led_indicator_options_hint2(self):
        """
        Tests that `query_led_indicator_options_hint` returns the expected exceptions, return values, or outputs.
        """

        # Branch 2: Test that the LED indicator options hint returns an empty list for an invalid LED type from the
        #           NUC WMI spec file.
        expected_indicator_options_indexes = []
        nuc_wmi_spec = {
            'led_hints': {
                'indicator_options': {
                    'HDD LED': [
                        'Disable',
                        'HDD Activity Indicator',
                        'Software Indicator'
                    ],
                    'Power Button LED': [
                        'Disable',
                        'HDD Activity Indicator',
                        'Power State Indicator',
                        'Software Indicator'
                    ],
                    'RGB Header': [
                        'Disable',
                        'HDD Activity Indicator',
                        'Power State Indicator',
                        'Software Indicator'
                    ]
                }
            }
        }

        indicator_options_indexes = query_led_indicator_options_hint(
            nuc_wmi_spec,
            10
        )

        self.assertListEqual(
            indicator_options_indexes,
            expected_indicator_options_indexes
        )


    def test_query_led_rgb_color_type_dimensions_hint(self):
        """
        Tests that `query_led_rgb_color_type_dimensions_hint` returns the expected exceptions, return values, or
        outputs.
        """

        # Branch 1: Test that the LED rgb color type dimensions hint is properly returned from the NUC WMI spec file.
        led_type = 'HDD LED'
        nuc_wmi_spec = {
            'led_hints': {
                'rgb_color_type_dimensions': {
                    'HDD LED': 1,
                    'RGB Header': 1
                }
            }
        }

        led_rgb_color_type_dimensions = query_led_rgb_color_type_dimensions_hint(
            nuc_wmi_spec,
            led_type
        )

        self.assertEqual(
            led_rgb_color_type_dimensions,
            nuc_wmi_spec['led_hints']['rgb_color_type_dimensions'][led_type]
        )


    def test_query_led_rgb_color_type_dimensions_hint2(self):
        """
        Tests that `query_led_rgb_color_type_dimensions_hint` returns the expected exceptions, return values, or
        outputs.
        """

        # Branch 2: Test that the LED rgb color type dimensions hint is properly returned when an invalid LED type is
        #           provided.
        led_type = 'Invalid LED'
        nuc_wmi_spec = {
            'led_hints': {
                'rgb_color_type_dimensions': {
                    'HDD LED': 1,
                    'RGB Header': 1
                }
            }
        }

        led_rgb_color_type_dimensions = query_led_rgb_color_type_dimensions_hint(
            nuc_wmi_spec,
            led_type
        )

        self.assertEqual(
            led_rgb_color_type_dimensions,
            None
        )


    def test_query_led_rgb_color_type_dimensions_hint3(self):
        """
        Tests that `query_led_rgb_color_type_dimensions_hint` returns the expected exceptions, return values, or
        outputs.
        """

        # Branch 3: Test that the LED rgb color type dimensions raises the proper exception when the NUC WMI
        #           specification value is invalid.
        led_type = 'HDD LED'
        nuc_wmi_spec = {
            'led_hints': {
                'rgb_color_type_dimensions': {
                    'HDD LED': 3.14,
                    'RGB Header': 3.14
                }
            }
        }

        with self.assertRaises(NucWmiError) as err:
            query_led_rgb_color_type_dimensions_hint(
                nuc_wmi_spec,
                led_type
            )

        self.assertEqual(
            str(err.exception),
            'Error (Intel NUC WMI spec has an invalid rgb_color_type_dimensions led_hint for LED %s, '
            'expected one of: [1, 3]' % led_type
        )


    def test_verify_nuc_wmi_function_spec(self):
        """
        Tests that `verify_nuc_wmi_function_spec` returns the expected exceptions, return values, or outputs.
        """

        nuc_wmi_function_name = 'test_nuc_wmi_function'
        nuc_wmi_spec = {}

        # Branch 1: Test that an exception is raised if the NUC WMI function name is not defined in the
        #           function_return_type definition of the NUC WMI spec.
        with self.assertRaises(NucWmiError) as err:
            verify_nuc_wmi_function_spec(nuc_wmi_function_name, nuc_wmi_spec)

        self.assertEqual(
            str(err.exception),
            'Error (NUC WMI specification does not include a function_return_type definition for NUC WMI function: '
            '%s' % nuc_wmi_function_name
        )


    def test_verify_nuc_wmi_function_spec2(self):
        """
        Tests that `verify_nuc_wmi_function_spec` returns the expected exceptions, return values, or outputs.
        """

        nuc_wmi_function_name = 'test_nuc_wmi_function'
        nuc_wmi_spec = {
            'function_return_type': {
                'test_nuc_wmi_function': 'bitmap'
            }
        }

        # Branch 2: Test that an exception is raised if the NUC WMI function name is not defined in the
        #           function_oob_return_value_recover definition of the NUC WMI spec.
        with self.assertRaises(NucWmiError) as err:
            verify_nuc_wmi_function_spec(nuc_wmi_function_name, nuc_wmi_spec)

        self.assertEqual(
            str(err.exception),
            'Error (NUC WMI specification does not include a function_oob_return_value_recover definition for NUC WMI'
            ' function: %s' % nuc_wmi_function_name
        )


    def test_verify_nuc_wmi_function_spec3(self):
        """
        Tests that `verify_nuc_wmi_function_spec` returns the expected exceptions, return values, or outputs.
        """

        nuc_wmi_function_name = 'test_nuc_wmi_function'
        nuc_wmi_function_return_types = ['int']
        nuc_wmi_spec = {
            'function_return_type': {
                'test_nuc_wmi_function': 'bitmap'
            },
            'function_oob_return_value_recover': {
                'test_nuc_wmi_function': False
            }
        }

        # Branch 3: Test that an exception is raised if the NUC WMI function name function_return_type specified in
        #           NUC WMI spec is not supported by the NUC WMI function.
        with self.assertRaises(NucWmiError) as err:
            verify_nuc_wmi_function_spec(
                nuc_wmi_function_name,
                nuc_wmi_spec,
                nuc_wmi_function_return_types=nuc_wmi_function_return_types
            )

        self.assertEqual(
            str(err.exception),
            'Error (Intel NUC WMI spec has an invalid function_return_type for function %s, allowed return types:'
            ' %s)' % (nuc_wmi_function_name, json.dumps(nuc_wmi_function_return_types))
        )


    def test_verify_nuc_wmi_function_spec4(self):
        """
        Tests that `verify_nuc_wmi_function_spec` returns the expected exceptions, return values, or outputs.
        """

        nuc_wmi_function_name = 'test_nuc_wmi_function'
        nuc_wmi_function_oob_return_value_recover_values = [True]
        nuc_wmi_spec = {
            'function_return_type': {
                'test_nuc_wmi_function': 'bitmap'
            },
            'function_oob_return_value_recover': {
                'test_nuc_wmi_function': False
            }
        }

        # Branch 4: Test that an exception is raised if the NUC WMI function name function_oob_return_value_recover
        #           specified in NUC WMI spec is not supported by the NUC WMI function.
        with self.assertRaises(NucWmiError) as err:
            verify_nuc_wmi_function_spec(
                nuc_wmi_function_name,
                nuc_wmi_spec,
                nuc_wmi_function_oob_return_value_recover_values=nuc_wmi_function_oob_return_value_recover_values
            )

        self.assertEqual(
            str(err.exception),
            'Error (Intel NUC WMI spec has an invalid function_oob_return_value_recover for function %s, allowed OOB '
            'recover values: %s)' % \
            (nuc_wmi_function_name, json.dumps(nuc_wmi_function_oob_return_value_recover_values))
        )


    def test_verify_nuc_wmi_function_spec5(self):
        """
        Tests that `verify_nuc_wmi_function_spec` returns the expected exceptions, return values, or outputs.
        """

        nuc_wmi_function_name = 'test_nuc_wmi_function'
        nuc_wmi_spec = {
            'function_return_type': {
                'test_nuc_wmi_function': 'bitmap'
            },
            'function_oob_return_value_recover': {
                'test_nuc_wmi_function': False
            }
        }
        verification_return_value_expected = ('bitmap', False)

        # Branch 5: Test that the expected tuple with function return type and function oob return value recover values
        #           are returned upon successful NUC WMI function verification.
        verification_return_value = verify_nuc_wmi_function_spec(
            nuc_wmi_function_name,
            nuc_wmi_spec
        )

        self.assertEqual(
            verification_return_value_expected,
            verification_return_value
        )
