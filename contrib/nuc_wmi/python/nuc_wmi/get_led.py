"""
`nuc_wmi.get_led` provides an interface to the WMI get led state function.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file

METHOD_ID = 0x01

def get_led(led, control_file=None, debug=False, quirks=None, quirks_metadata=None):
    """
    Get legacy LED state with regard to brightness, frequency, and color.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led: Selects the legacy LED to get the state for.
      quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
      quirks_metadata: Metadata that may be required by various quirks in order for them to be applied.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
      Tuple of legacy brightness, frequency, and color indexes of the select LED.
    """

    get_led_byte_list = [METHOD_ID, led]

    write_control_file(get_led_byte_list, control_file=control_file, debug=debug, quirks=quirks,
                       quirks_metadata=quirks_metadata)

    (
        error_code,
        brightness,
        frequency,
        color
    ) = read_control_file(control_file=control_file, debug=debug, quirks=quirks, quirks_metadata=quirks_metadata)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    # Some factory refurbed NUC 7's are returning incorrect values that are outside the range of
    # valid values according to the specification for all fields. As we saw with the last quirks fix,
    # frequency used to be 0x00, but now some devices are returning values of 0xFF even though
    # the error code is 0.
    if quirks is not None and \
       ('NUC7_FREQUENCY_DEFAULT' in quirks or 'NUC7_OUT_OF_BOUND_READ' in quirks) \
       and quirks_metadata is not None:
        if 'brightness_range' in quirks_metadata and brightness not in quirks_metadata['brightness_range']:
            brightness = 0x00

        if 'color_range' in quirks_metadata and color not in quirks_metadata['color_range']:
            color = 0x00

        if 'frequency_range' in quirks_metadata and frequency not in quirks_metadata['frequency_range']:
            frequency = 0x01

    return tuple([brightness, frequency, color])
