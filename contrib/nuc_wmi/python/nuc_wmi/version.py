"""
`nuc_wmi.version` provides an interface to the WMI version functions.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file
from nuc_wmi.utils import byte_list_to_index, verify_nuc_wmi_function_spec

METHOD_ID = 0x09
VERSION_TYPE = [
    'wmi_interface_spec_compliance_version'
]
WMI_INTERFACE_SPEC_COMPLIANCE_VERSION_NUC_WMI_SPEC = {
    'nuc_wmi_function_return_types': ['index'],
    'nuc_wmi_function_oob_return_value_recover_values': [False]
}


def wmi_interface_spec_compliance_version(nuc_wmi_spec, control_file=None, debug=False, metadata=None): # pylint: disable=unused-argument
    """
    Returns the version for the WMI interface spec compliance.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      metadata: Metadata that may be required to change functional behavior.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
      Tuple of two bytes representing the version number.
    """

    (function_return_type, function_oob_return_value_recover) = verify_nuc_wmi_function_spec( # pylint: disable=unused-variable
        'wmi_interface_spec_compliance_version',
        nuc_wmi_spec,
        *WMI_INTERFACE_SPEC_COMPLIANCE_VERSION_NUC_WMI_SPEC
    )
    wmi_version_byte_list = [
        METHOD_ID,
        VERSION_TYPE.index('wmi_interface_spec_compliance_version')
    ]

    write_control_file(wmi_version_byte_list, control_file=control_file, debug=debug)

    (
        error_code,
        version_byte_1,
        version_byte_2,
        reserved_byte   # pylint: disable=unused-variable
    ) = read_control_file(control_file=control_file, debug=debug)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    version_byte_1_index = byte_list_to_index([version_byte_1], function_return_type)
    version_byte_2_index = byte_list_to_index([version_byte_2], function_return_type)

    return tuple([version_byte_2_index, version_byte_1_index])
