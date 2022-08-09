"""
The `test.unit.nuc_wmi.utils_test` module provides unit tests for the functions in
`nuc_wmi.utils`.

Classes:
    TestUtils: A unit test class for the functions in `nuc_wmi.utils`.
"""

import unittest

from nuc_wmi.utils import byte_list_to_bitmap


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
