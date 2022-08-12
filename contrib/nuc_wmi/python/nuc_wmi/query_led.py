"""
`nuc_wmi.query_led` provides an interface to the WMI query led set of functions.
"""

from nuc_wmi import CONTROL_ITEM, LED_INDICATOR_OPTION, LED_TYPE, NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file
from nuc_wmi.utils import byte_list_to_bitmap

LED_INDICATOR_OPTION_DISABLED = 0x06
METHOD_ID = 0x03

QUERY_TYPE = [
    'query_leds',
    'query_led_color_type',
    'query_led_indicator_options',
    'query_led_control_items'
]

def query_led_color_type(led_type, control_file=None, debug=False, quirks=None, quirks_metadata=None):
    """
    Query the LED color type for the LED type.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led_type: The LED type for which to query the LED color type.
      quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
      quirks_metadata: Metadata that may be required by various quirks in order for them to be applied.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
      `nuc_wmi.LED_COLOR_TYPE` index of current LED color type.
    """

    query_led_color_byte_list = [METHOD_ID, QUERY_TYPE.index('query_led_color_type'), led_type]

    write_control_file(query_led_color_byte_list, control_file=control_file, debug=debug, quirks=quirks,
                       quirks_metadata=quirks_metadata)

    # Bitmap [0:7], [8:15], [16:23]
    (
        error_code,
        led_color_type_bitmap_1,
        led_color_type_bitmap_2,
        led_color_type_bitmap_3
    ) = read_control_file(control_file=control_file, debug=debug, quirks=quirks, quirks_metadata=quirks_metadata)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    led_color_type_bitmaps = [
        led_color_type_bitmap_3,
        led_color_type_bitmap_2,
        led_color_type_bitmap_1
    ]

    if quirks is not None and 'NUC10_RETURN_VALUE' in quirks:
        led_color_type_bitmap = byte_list_to_bitmap(led_color_type_bitmaps)

        return int(led_color_type_bitmap, 2)

    led_color_type_bitmap = byte_list_to_bitmap(led_color_type_bitmaps)[::-1]

    if len(list(filter(lambda led_color_type_bit: led_color_type_bit == '1', [*led_color_type_bitmap]))) > 1:
        raise NucWmiError(
            'Error (Intel NUC WMI query_led_color_type function returned multiple led color types in bitmap)'
        )

    return led_color_type_bitmap.index('1')


def query_led_control_items(
        led_type,
        led_indicator_option,
        control_file=None,
        debug=False,
        quirks=None,
        quirks_metadata=None
):
    """
    Query the LED control items for the LED indicator option of the LED type.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led_indicator_option: The LED indicator option to use for the LED type when querying for the LED control items.
      led_type: The LED type for which to query the LED control items.
      quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
      quirks_metadata: Metadata that may be required by various quirks in order for them to be applied.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
      List of available `nuc_wmi.CONTROL_ITEM` indexes for the specified LED type and LED indicator option.
    """

    led_color_type = query_led_color_type(led_type, control_file=control_file, debug=debug, quirks=quirks,
                                          quirks_metadata=quirks_metadata)

    query_led_control_item_byte_list = [
        METHOD_ID,
        QUERY_TYPE.index('query_led_control_items'),
        led_type,
        led_indicator_option
    ]

    write_control_file(query_led_control_item_byte_list, control_file=control_file, debug=debug, quirks=quirks,
                       quirks_metadata=quirks_metadata)

    # Bitmap [0:7], [8:15], [16:23]
    (
        error_code,
        led_control_item_bitmap_1,
        led_control_item_bitmap_2,
        led_control_item_bitmap_3
    ) = read_control_file(control_file=control_file, debug=debug, quirks=quirks, quirks_metadata=quirks_metadata)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    led_control_item_bitmaps = [
        led_control_item_bitmap_3,
        led_control_item_bitmap_2,
        led_control_item_bitmap_1
    ]
    led_control_item_bitmap = byte_list_to_bitmap(led_control_item_bitmaps)[::-1]

    if led_indicator_option == LED_INDICATOR_OPTION_DISABLED or \
       CONTROL_ITEM[led_indicator_option][led_color_type] is None:
        return []

    if led_control_item_bitmap.rindex('1') >= len(CONTROL_ITEM[led_indicator_option][led_color_type]):
        raise NucWmiError(
            'Error (Intel NUC WMI query_led_control_items function returned more led control items than ' +
            'supported for the led type and led indicator provided)'
        )

    return [index for index, bit in enumerate(led_control_item_bitmap) if int(bit)]


def query_led_indicator_options(led_type, control_file=None, debug=False, quirks=None, quirks_metadata=None):
    """
    Query the LED indicator options available for the LED type.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led_type: The LED type for which to query the LED indicator options.
      quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
      quirks_metadata: Metadata that may be required by various quirks in order for them to be applied.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
      List of available `nuc_wmi.LED_INDICATOR_OPTION` indexes.
    """

    query_led_indicator_options_byte_list = [
        METHOD_ID,
        QUERY_TYPE.index('query_led_indicator_options'),
        led_type
    ]

    write_control_file(query_led_indicator_options_byte_list, control_file=control_file, debug=debug, quirks=quirks,
                       quirks_metadata=quirks_metadata)

    # Bitmap [0:7], [8:15], [16:23]
    (
        error_code,
        led_indicator_option_bitmap_1,
        led_indicator_option_bitmap_2,
        led_indicator_option_bitmap_3
    ) = read_control_file(control_file=control_file, debug=debug, quirks=quirks, quirks_metadata=quirks_metadata)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    led_indicator_option_bitmaps = [
        led_indicator_option_bitmap_3,
        led_indicator_option_bitmap_2,
        led_indicator_option_bitmap_1
    ]
    led_indicator_option_bitmap = byte_list_to_bitmap(led_indicator_option_bitmaps)[::-1]

    if led_indicator_option_bitmap.rindex('1') >= len(LED_INDICATOR_OPTION):
        raise NucWmiError(
            'Error (Intel NUC WMI query_led_indicator_options function returned more led indicator options than ' +
            'supported for the led type provided)'
        )

    return [index for index, bit in enumerate(led_indicator_option_bitmap) if int(bit)]


def query_leds(control_file=None, debug=False, quirks=None, quirks_metadata=None):
    """
    List all LED types supported.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      quirks: Enable NUC WMI quirks to work around various implementation issues or bugs.
      quirks_metadata: Metadata that may be required by various quirks in order for them to be applied.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
      List of available `nuc_wmi.LED_TYPE` indexes.
    """

    query_leds_byte_list = [METHOD_ID, QUERY_TYPE.index('query_leds')]

    write_control_file(query_leds_byte_list, control_file=control_file, debug=debug, quirks=quirks,
                       quirks_metadata=quirks_metadata)

    # Bitmap [0:7], [8:15], [16:23]
    (
        error_code,
        led_type_bitmap_1,
        led_type_bitmap_2,
        led_type_bitmap_3
    ) = read_control_file(control_file=control_file, debug=debug, quirks=quirks, quirks_metadata=quirks_metadata)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    led_type_bitmaps = [
        led_type_bitmap_3,
        led_type_bitmap_2,
        led_type_bitmap_1
    ]
    led_type_bitmap = byte_list_to_bitmap(led_type_bitmaps)[::-1]

    if led_type_bitmap.rindex('1') >= len(LED_TYPE['new']):
        raise NucWmiError('Error (Intel NUC WMI query_leds function returned more led types than supported)')

    return [index for index, bit in enumerate(led_type_bitmap) if int(bit)]
