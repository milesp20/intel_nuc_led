"""
`nuc_wmi.get_led` provides an interface to the WMI get led state function.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file
from nuc_wmi.utils import byte_list_to_index, verify_nuc_wmi_function_spec

GET_LED_NUC_WMI_SPEC = {
    'nuc_wmi_function_return_types': ['index'],
    'nuc_wmi_function_oob_return_value_recover_values': [False, True]
}
METHOD_ID = 0x01


def get_led(nuc_wmi_spec, led, control_file=None, debug=False, metadata=None):
    """
    Get legacy LED state with regard to brightness, frequency, and color.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led: Selects the legacy LED to get the state for.
      metadata: Metadata that may be required to change functional behavior.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception, or NUC WMI spec error.
    Returns:
      Tuple of legacy brightness, frequency, and color indexes of the select LED.
    """

    (function_return_type, function_oob_return_value_recover) = verify_nuc_wmi_function_spec(
        'get_led',
        nuc_wmi_spec,
        *GET_LED_NUC_WMI_SPEC
    )
    get_led_byte_list = [METHOD_ID, led]

    write_control_file(get_led_byte_list, control_file=control_file, debug=debug)

    (
        error_code,
        brightness,
        frequency,
        color
    ) = read_control_file(control_file=control_file, debug=debug)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    brightness = byte_list_to_index([brightness], function_return_type)
    color = byte_list_to_index([color], function_return_type)
    frequency = byte_list_to_index([frequency], function_return_type)

    if function_oob_return_value_recover:
        if 'brightness_range' in metadata and brightness not in metadata['brightness_range']:
            brightness = metadata['brightness_range'][0]

        if 'color_range' in metadata and color not in metadata['color_range']:
            color = metadata['color_range'][0]

        if 'frequency_range' in metadata and frequency not in metadata['frequency_range']:
            frequency = metadata['frequency_range'][0]

    return tuple([brightness, frequency, color])
