"""
`nuc_wmi.control_file` module provides interfaces for interacting with Intel NUC LED kernel module control file.
"""

from __future__ import print_function

import sys

from nuc_wmi import CONTROL_FILE, NucWmiError

def read_control_file(control_file=None, debug=False, quirks=None): # pylint: disable=unused-argument
    """
    Read the NUC LED control file hex bytes string.

    Args:
       control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
       debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
       quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
    Exceptions:
       Raises normal `IOError`/`OSError` on failure to read the control file, or `ValueError` for hex conversion error.
    Returns:
       Tuple of ints representing the hex numbers read in from the control file.
    """

    with open(control_file or CONTROL_FILE, 'r') as fin:
        raw_hex_byte_string = fin.read()

    # Remove the new line and null char the driver leaves
    raw_hex_byte_string = raw_hex_byte_string.rstrip("\x00").rstrip("\n")

    if debug:
        print('r: ', raw_hex_byte_string, file=sys.stderr)

    byte_list = [int(hex_byte_str, 16) for hex_byte_str in raw_hex_byte_string.split(' ')]

    for hex_byte in byte_list:
        if hex_byte < 0 or hex_byte > 255:
            raise NucWmiError('NUC WMI returned hex byte outside of 0-255 range')

    if len(byte_list) != 4:
        raise NucWmiError('NUC WMI control file did not return an expected 4 bytes')

    return tuple(byte_list)


def write_control_file(int_byte_list, control_file=None, debug=False, quirks=None): # pylint: disable=unused-argument
    """
    Converts the integer byte list into a hex byte string and writes it to the NUC control file.

    Args:
       control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
       debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
       int_byte_list: List of integers bytes to be converted into a hex byte string to send to the NUC control file. May
                       be int byte strings. Integers must be 0-255.
       quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
    Exceptions:
       Raises normal `IOError`/`OSError` on failure to read the control file, `ValueError` for hex conversion error, or
       `nuc_wmi.NucWmiError` for input value errors.
    """

    for int_byte in int_byte_list:
        if int(int_byte) < 0 or int(int_byte) > 255:
            raise NucWmiError('Error (NUC LED byte values must be 0-255)')

    raw_hex_byte_string = ' '.join(
        ['{:02x}'.format(int(int_byte)) for int_byte in int_byte_list + ([0] * (5 - len(int_byte_list)))]
    )

    if debug:
        print('w: ', raw_hex_byte_string, file=sys.stderr)

    with open(control_file or CONTROL_FILE, 'w') as fout:
        fout.write(raw_hex_byte_string)
