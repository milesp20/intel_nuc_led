"""
`nuc_wmi.get_led` provides an interface to the WMI get led state function.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file

METHOD_ID=0x01

def get_led(led, control_file=None):
    """
    Get LED state with regard to brightness, frequency, and color.

    Args:
       control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
       led: Selects the legacy LED to set a state for.
    Exceptions:
       Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
       or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
       Tuple of legacy brightness, frequency, and color of the select LED.
    """

    get_led_byte_list = [METHOD_ID, led]

    write_control_file(get_led_byte_list, control_file=control_file)

    (
        error_code,
        brightness,
        frequency,
        color
    ) = read_control_file(control_file=control_file)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR[error_code])

    return tuple([brightness, frequency, color])
