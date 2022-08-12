"""
The `test.unit.nuc_wmi.utils_test` module provides unit tests for the functions in
`nuc_wmi.utils`.

Classes:
    TestUtils: A unit test class for the functions in `nuc_wmi.utils`.
"""

import tempfile
import unittest

from nuc_wmi import NucWmiError
from nuc_wmi.utils import acquire_file_lock, byte_list_to_bitmap, defined_indexes


class TestUtils(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.utils`

    Methods:
        setUp: Unit test initialization.
        test_byte_list_to_bitmap: Tests that `byte_list_to_bitmap` raises the expected exception when any of the ints in
                                  byte list are outside of the 0-255 range, tests that it returns the proper bitmap
                                  string when the byte list is int or str, tests that returned bitmaps are properly
                                  explicitly padded to 8 bits, tests that we get an exception of the inputs are not
                                  proper ints.
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
