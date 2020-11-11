"""
`nuc_wmi.switch_led_type` provides an interface to the WMI switch led type function.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file

LED_COLOR_GROUP = [
    'Single color LED',
    'Multi color LED'
]

METHOD_ID = 0x08

def switch_led_type(led_color_group, control_file=None, debug=False, quirks=None):
    """
    Switches the LED color group type.

    Args:
       debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
       led_color_group: The LED color group type to set.
       quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
    Exceptions:
       Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
       or if `read_control_file` or `write_control_file` raise an exception.
    """

    switch_led_byte_list = [METHOD_ID, led_color_group]

    write_control_file(switch_led_byte_list, control_file=control_file, debug=debug, quirks=quirks)

    (
        error_code,
        reserved_byte_1, # pylint: disable=unused-variable
        reserved_byte_2, # pylint: disable=unused-variable
        reserved_byte_3  # pylint: disable=unused-variable
    ) = read_control_file(control_file=control_file, debug=debug, quirks=quirks)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))
