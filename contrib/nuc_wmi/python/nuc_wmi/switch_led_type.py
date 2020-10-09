"""
`nuc_wmi.switch_led_type` provides an interface to the WMI switch led type function.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file

LED_COLOR_GROUP = [
    'Single color LED',
    'Multi color LED'
]

METHOD_ID=0x08

def switch_led_type(led_color_group, control_file=None):
    """
    Switches the LED color group type.

    Args:
       led_color_group: The LED color group type to set.
    Exceptions:
       Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
       or if `read_control_file` or `write_control_file` raise an exception.
    """

    switch_led_byte_list = [METHOD_ID, led_color_group]

    write_control_file(switch_led_byte_list, control_file=control_file)

    (
        error_code,
        reserved_byte_1,
        reserved_byte_2,
        reserved_byte_3
    ) = read_control_file(control_file=control_file)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))
