"""
`nuc_wmi.set_led` provides an interface to the WMI set led function.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file

METHOD_ID=0x02

def set_led(led, brightness, frequency, color, control_file=None):
    """
    Set LED state with regard to brightness, frequency, and color.

    Args:
       brightness: Controls the brightness level of the LED.
       color: Sets legacy RGB-color for LED.
       control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
       frequency: Sets the legacy LED frequency.
       led: Selects the legacy LED to set a state for.
    Exceptions:
       Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
       or if `read_control_file` or `write_control_file` raise an exception.
    """

    set_led_byte_list = [METHOD_ID, led, brightness, frequency, color]

    write_control_file(set_led_byte_list, control_file=control_file)

    (
        brightness_error,
        frequency_error,
        color_error,
        reserved_byte
    ) = read_control_file(control_file=control_file)

    if brightness_error > 0:
        raise NucWmiError(RETURN_ERROR[brightness_error])

    if frequency_error > 0:
        raise NucWmiError(RETURN_ERROR[frequency_error])

    if color_error > 0:
        raise NucWmiError(RETURN_ERROR[color_error])
