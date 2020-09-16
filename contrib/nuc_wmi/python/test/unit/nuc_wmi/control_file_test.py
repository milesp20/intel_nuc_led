"""
The `test.unit.nuc_wmi.control_file_test` module provides unit tests for the functions in
`nuc_wmi.control_file`.

Classes:
    TestControlFile: A unit test class for the functions in `nuc_wmi.control_file`.
"""

import os
import unittest

from mock import patch
from tempfile import NamedTemporaryFile

from nuc_wmi import NucWmiError
from nuc_wmi.control_file import read_control_file, write_control_file


class TestControlFile(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.control_file`

    Methods:
        setUp: Unit test initialization.
        tearDown: Unit test cleanup.
        test_read_control_file: Tests that `read_control_file` raises the expected exception when nuc_wmi.CONTROL_FILE
                                doesnt exist, tests that exception is raised if less than 4 bytes are returned, tests
                                that overriding control_file with existing file works, tests that overriding
                                control_file with non existing file raises exception, and tests that exception is raised
                                if NUC WMI provides a hex byte value outside of the 0-255 range.
        test_write_control_file: Tests that `write_control_file` raises the expected exception when nuc_wmi.CONTROL_FILE
                                 doesnt exist, tests that number of bytes written to control file are padded to 5 bytes
                                 if less than 5 bytes are passed in, tests that both integer and string bytes are
                                 accepted, tests that byte strings outside of 0-255 value raise an exception, tests that
                                 overriding control_file with different file works.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.control_file = NamedTemporaryFile(delete=False)
        self.maxDiff = None

        self.control_file.close()


    def tearDown(self):
        """
        Cleans up the unit tests.
        """

        self.control_file.close()

        os.unlink(self.control_file.name)


    def test_read_control_file(self):
        """
        Tests that `read_control_file` returns the expected exceptions, return values, or outputs.
        """

        # Branch 1: Test that `read_control_file` raises exception when `nuc_wmi.CONTROL_FILE` doesnt exist
        #           Assumes we are testing on a system without the driver installed.
        with self.assertRaises((IOError, OSError)) as err:
            read_control_file()

        # Reset
        with open(self.control_file.name, 'w') as fout:
            fout.truncate()

        # Branch 2: Test that `read_control_file` raise exception if less than 4 bytes are read
        with open(self.control_file.name, 'w') as fout:
            fout.write("00 00 00\n\x00")

        with self.assertRaises(NucWmiError) as byte_list_len_err:
            read_control_file(control_file=self.control_file.name)

        self.assertEqual(str(byte_list_len_err.exception),
                         'NUC WMI control file did not return an expected 4 bytes')

        # Reset
        with open(self.control_file.name, 'w') as fout:
            fout.truncate()

        # Branch 3: Test that overriding control file with existing file works
        with open(self.control_file.name, 'w') as fout:
            fout.write("0D 0E 0A 0D\n\x00")

        byte_list = (0x0D, 0x0E, 0x0A, 0x0D)

        self.assertEqual(read_control_file(control_file=self.control_file.name), byte_list)

        # Reset
        with open(self.control_file.name, 'w') as fout:
            fout.truncate()

        # Branch 4: Test that overriding control file with non existing file raises exception
        non_existent_file = NamedTemporaryFile()

        non_existent_file.close()

        with self.assertRaises((IOError, OSError)) as err:
            read_control_file(control_file=non_existent_file.name)

        # Bramch 5: Test that exception is raised if NUC WMI returns a hex byte outside 0-255 range
        with open(self.control_file.name, 'w') as fout:
            fout.write("FFF 0E 0A 0D\n\x00")

        with self.assertRaises(NucWmiError) as err:
            read_control_file(control_file=self.control_file.name)

        self.assertEqual(str(err.exception), 'NUC WMI returned hex byte outside of 0-255 range')


    def test_write_control_file(self):
        """
        Tests that `write_control_file` returns the expected exceptions, return values, or outputs.
        """

        # Branch 1: Tests that `write_control_file` raises the expected exception when `nuc_wmi.CONTROL_FILE` doesnt
        #           exist. Assumes we are testing on a system without the driver installed.
        with self.assertRaises((IOError, OSError)) as err:
            read_control_file()

        # Reset
        with open(self.control_file.name, 'w') as fout:
            fout.truncate()

        # Branch 2, 3: Tests that the number of bytes written to the control file are padded to 5 bytes, and that
        #              integer byte list is properly written to the control file.
        byte_list = [0x0D, 0x0E, 0x0A, 0x0D]
        expected_byte_string='0d 0e 0a 0d 00'

        write_control_file(byte_list, control_file=self.control_file.name)

        with open(self.control_file.name, 'r') as fin:
            written_byte_string = fin.read()

        self.assertEqual(expected_byte_string, written_byte_string)

        # Reset
        with open(self.control_file.name, 'w') as fout:
            fout.truncate()

        # Branch 4: Tests that an string byte list is properly written to the control file
        byte_list = [str(0x0D), str(0x0E), str(0x0A), str(0x0D)]
        expected_byte_string='0d 0e 0a 0d 00'

        write_control_file(byte_list, control_file=self.control_file.name)

        with open(self.control_file.name, 'r') as fin:
            written_byte_string = fin.read()

        self.assertEqual(expected_byte_string, written_byte_string)

        # Reset
        with open(self.control_file.name, 'w') as fout:
            fout.truncate()

        # Branch 5: Test that byte strings outside of the 0-255 value raise an excepton
        byte_list = [0xFFF]

        with self.assertRaises(NucWmiError) as err:
            write_control_file(byte_list, control_file=self.control_file.name)

        self.assertEqual(str(err.exception), 'Error (NUC LED byte values must be 0-255)')
