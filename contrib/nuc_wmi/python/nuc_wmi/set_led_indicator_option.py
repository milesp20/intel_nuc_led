"""
`nuc_wmi.set_led_indicator_option` provides an interface to the WMI set indicator function.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file

METHOD_ID = 0x05

def set_led_indicator_option(led_type, led_indicator_option, control_file=None, debug=False, quirks=None):
    """
    Set the LED indicator option for the specified LED type,

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led_indicator_option: The LED indicator option to set for the LED type.
      led_type: The LED type for which to set the LED indicator option.
      quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
    Exceptions:
       Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
       or if `read_control_file` or `write_control_file` raise an exception.
    """

    set_led_indicator_option_byte_list = [METHOD_ID, led_type, led_indicator_option]

    write_control_file(set_led_indicator_option_byte_list, control_file=control_file, debug=debug, quirks=quirks)

    (
        error_code,
        reserved_byte_1, # pylint: disable=unused-variable
        reserved_byte_2, # pylint: disable=unused-variable
        reserved_byte_3  # pylint: disable=unused-variable
    ) = read_control_file(control_file=control_file, debug=debug, quirks=quirks)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))
