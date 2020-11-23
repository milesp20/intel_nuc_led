"""
`nuc_wmi.get_led` provides an interface to the WMI get led state function.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file

METHOD_ID = 0x01

def get_led(led, control_file=None, debug=False, quirks=None):
    """
    Get legacy LED state with regard to brightness, frequency, and color.

    Args:
       control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
       debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
       led: Selects the legacy LED to get the state for.
       quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
    Exceptions:
       Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
       or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
       Tuple of legacy brightness, frequency, and color indexes of the select LED.
    """

    get_led_byte_list = [METHOD_ID, led]

    write_control_file(get_led_byte_list, control_file=control_file, debug=debug, quirks=quirks)

    (
        error_code,
        brightness,
        frequency,
        color
    ) = read_control_file(control_file=control_file, debug=debug, quirks=quirks)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    # On a factory fresh NUC 7, the BIOS can return a default frequency value of 0 which
    # is not a valid enum range value and this causes the frequency value to be returned as
    # null due to how we implemented the enums.
    if quirks is not None and 'NUC7_FREQUENCY_DEFAULT' in quirks and frequency == 0:
        frequency = 0x01

    return tuple([brightness, frequency, color])
