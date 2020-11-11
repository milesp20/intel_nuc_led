"""
The `test.unit.nuc_wmi.version_test` module provides unit tests for the functions in
`nuc_wmi.version`.

Classes:
    TestVersion: A unit test class for the functions in `nuc_wmi.version`.
"""

import unittest

from mock import patch

from nuc_wmi import NucWmiError
from nuc_wmi.version import METHOD_ID, VERSION_TYPE, wmi_interface_spec_compliance_version

import nuc_wmi


class TestVersion(unittest.TestCase):
    """
    A unit test class for the functions of `nuc_wmi.version`

    Methods:
        setUp: Unit test initialization.
        test_wmi_interface_spec_compliance_version: Tests that it sends the expected byte list to the control file,
                                                    tests that the returned control file response is properly processed,
                                                    tests that it raises an exception when the control file returns an
                                                    error code.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name


    @patch('nuc_wmi.version.read_control_file')
    @patch('nuc_wmi.version.write_control_file')
    def test_wmi_interface_spec_compliance_version(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `wmi_interface_spec_compliance_version` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.version.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.version.write_control_file is nuc_wmi_write_control_file)

        # Branch 1: Test that wmi_interface_spec_compliance_version send the expected byte string to the control file
        #           and that the returned control file response is properly processed.
        expected_wmi_interface_spec_compliance_version = (0x01, 0x36)
        expected_write_byte_list = [METHOD_ID, VERSION_TYPE.index('wmi_interface_spec_compliance_version')]
        read_byte_list = [0x00, 0x36, 0x01, 0x00]

        nuc_wmi_read_control_file.return_value = read_byte_list
        returned_wmi_interface_spec_compliance_version = wmi_interface_spec_compliance_version(
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

        self.assertEqual(returned_wmi_interface_spec_compliance_version, expected_wmi_interface_spec_compliance_version)


    @patch('nuc_wmi.version.read_control_file')
    @patch('nuc_wmi.version.write_control_file')
    def test_wmi_interface_spec_compliance_version2(self, nuc_wmi_write_control_file, nuc_wmi_read_control_file):
        """
        Tests that `wmi_interface_spec_compliance_version` returns the expected exceptions, return values, or
        outputs.
        """

        self.assertTrue(nuc_wmi.version.read_control_file is nuc_wmi_read_control_file)
        self.assertTrue(nuc_wmi.version.write_control_file is nuc_wmi_write_control_file)

        # Branch 2: Test that wmi_interface_spec_compliance_version raises an exception when the control file returns an
        #           error code.
        expected_write_byte_list = [METHOD_ID, VERSION_TYPE.index('wmi_interface_spec_compliance_version')]
        read_byte_list = [0xE1, 0x00, 0x00, 0x00] # Return function not supported

        nuc_wmi_read_control_file.return_value = read_byte_list

        with self.assertRaises(NucWmiError) as err:
            wmi_interface_spec_compliance_version(
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

        self.assertEqual(str(err.exception), 'Error (Function not supported)')
