"""
`nuc_wmi.version` provides an interface to the WMI version functions.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file

METHOD_ID = 0x09

VERSION_TYPE = [
    'wmi_interface_spec_compliance_version'
]

def wmi_interface_spec_compliance_version(control_file=None, debug=False, quirks=None):
    """
    Returns the version for the WMI interface spec compliance.

    Args:
       control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
       debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
       quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
    Exceptions:
       Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
       or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
       Tuple of two bytes representing the version number.
    """

    wmi_version_byte_list = [
        METHOD_ID,
        VERSION_TYPE.index('wmi_interface_spec_compliance_version')
    ]

    write_control_file(wmi_version_byte_list, control_file=control_file, debug=debug, quirks=quirks)

    (
        error_code,
        version_byte_1,
        version_byte_2,
        reserved_byte   # pylint: disable=unused-variable
    ) = read_control_file(control_file=control_file, debug=debug, quirks=quirks)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    return tuple([version_byte_2, version_byte_1])
