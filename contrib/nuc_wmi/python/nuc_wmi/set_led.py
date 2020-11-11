"""
`nuc_wmi.set_led` provides an interface to the WMI set led function.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file

METHOD_ID = 0x02

def set_led( # pylint: disable=too-many-arguments
        led,
        brightness,
        frequency,
        color,
        control_file=None,
        debug=False,
        quirks=None
):
    """
    Set LED state with regard to brightness, frequency, and color.

    Args:
       brightness: Controls the brightness level of the LED.
       color: Sets legacy RGB-color for LED.
       control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
       debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
       frequency: Sets the legacy LED frequency.
       led: Selects the legacy LED to set a state for.
       quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
    Exceptions:
       Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
       or if `read_control_file` or `write_control_file` raise an exception.
    """

    set_led_byte_list = [METHOD_ID, led, brightness, frequency, color]

    write_control_file(set_led_byte_list, control_file=control_file, debug=debug, quirks=quirks)

    (
        brightness_error,
        frequency_error,
        color_error,
        reserved_byte     # pylint: disable=unused-variable
    ) = read_control_file(control_file=control_file, debug=debug, quirks=quirks)

    if brightness_error > 0:
        raise NucWmiError(RETURN_ERROR.get(brightness_error, 'Error (Unknown NUC WMI error code)'))

    if frequency_error > 0:
        raise NucWmiError(RETURN_ERROR.get(frequency_error, 'Error (Unknown NUC WMI error code)'))

    if color_error > 0:
        raise NucWmiError(RETURN_ERROR.get(color_error, 'Error (Unknown NUC WMI error code)'))
