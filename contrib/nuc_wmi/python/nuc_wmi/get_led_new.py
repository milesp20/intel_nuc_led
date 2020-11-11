"""
`nuc_wmi.get_led_new` provides an interface to the new WMI get led set of functions.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file
from nuc_wmi.utils import byte_list_to_bitmap

GET_LED_TYPE = [
    'get_led_indicator_option',
    'get_led_control_item'
]
METHOD_ID = 0x04

def get_led_control_item( # pylint: disable=too-many-arguments
        led_type,
        led_indicator_option,
        control_item,
        control_file=None,
        debug=False,
        quirks=None
):
    """
    Get the current control item value for the control item of the indicator option for the specified LED type.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      control_item: The control item of the specified LED type indicator option for which to retrieve the value.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led_indicator_option: The indicator option for the specified LED type for which to retrieve the current control
                            item value.
      led_type: The LED type for which to retrieve the current control item.
      quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
    Exceptions:
       Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
       or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
       `nuc_wmi.CONTROL_ITEM` value for the control item of the indicator option for the specified LED type.
    """

    get_led_control_item_byte_list = [
        METHOD_ID,
        GET_LED_TYPE.index('get_led_control_item'),
        led_type,
        led_indicator_option,
        control_item
    ]

    write_control_file(get_led_control_item_byte_list, control_file=control_file, debug=debug, quirks=quirks)

    (
        error_code,
        control_item_value,
        reserved_byte_1,    # pylint: disable=unused-variable
        reserved_byte_2     # pylint: disable=unused-variable
    ) = read_control_file(control_file=control_file, debug=debug, quirks=quirks)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    return control_item_value


def get_led_indicator_option(led_type, control_file=None, debug=False, quirks=None):
    """
    Get the current indicator option for the LED type.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led_type: The LED type for which to retrieve the current indicator option.
      quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.

    Exceptions:
       Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
       or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
       `nuc_wmi.LED_INDICATOR_OPTION` index of the current LED indicator option.
    """

    get_led_indicator_option_byte_list = [
        METHOD_ID,
        GET_LED_TYPE.index('get_led_indicator_option'),
        led_type
    ]

    write_control_file(get_led_indicator_option_byte_list, control_file=control_file, debug=debug, quirks=quirks)

    (
        error_code,
        led_indicator_option,
        reserved_byte_1,      # pylint: disable=unused-variable
        reserved_byte_2       # pylint: disable=unused-variable
    ) = read_control_file(control_file=control_file, debug=debug, quirks=quirks)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR[error_code])

    if quirks is not None and 'NUC10_RETURN_VALUE' in quirks:
        return led_indicator_option

    led_indicator_option_bitmaps = [led_indicator_option]
    led_indicator_option_bitmap = byte_list_to_bitmap(led_indicator_option_bitmaps)[::-1]

    return led_indicator_option_bitmap.index('1')
