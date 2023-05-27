"""
`nuc_wmi.query_led` provides an interface to the WMI query led set of functions.
"""

from nuc_wmi import CONTROL_ITEM, LED_COLOR_TYPE, LED_INDICATOR_OPTION, LED_TYPE, NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file
from nuc_wmi.utils import byte_list_to_index, defined_indexes, query_led_color_type_hint
from nuc_wmi.utils import query_led_indicator_options_hint, verify_nuc_wmi_function_spec

LED_INDICATOR_OPTION_DISABLED = 0x06
METHOD_ID = 0x03
QUERY_LED_COLOR_TYPE_NUC_WMI_SPEC = {
    'nuc_wmi_function_return_types': ['bitmap', 'index'],
    'nuc_wmi_function_oob_return_value_recover_values': [False]
}
QUERY_LED_CONTROL_ITEMS_NUC_WMI_SPEC = {
    'nuc_wmi_function_return_types': ['bitmap'],
    'nuc_wmi_function_oob_return_value_recover_values': [False]
}
QUERY_LED_INDICATOR_OPTIONS_NUC_WMI_SPEC = {
    'nuc_wmi_function_return_types': ['bitmap'],
    'nuc_wmi_function_oob_return_value_recover_values': [False]
}
QUERY_LEDS_NUC_WMI_SPEC = {
    'nuc_wmi_function_return_types': ['bitmap'],
    'nuc_wmi_function_oob_return_value_recover_values': [False]
}
QUERY_TYPE = [
    'query_leds',
    'query_led_color_type',
    'query_led_indicator_options',
    'query_led_control_items'
]


def query_led_color_type(nuc_wmi_spec, led_type, control_file=None, debug=False, metadata=None): # pylint: disable=too-many-locals,unused-argument
    """
    Query the LED color type for the LED type.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led_type: The LED type for which to query the LED color type.
      metadata: Metadata that may be required to change functional behavior.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      if `read_control_file` or `write_control_file` raise an exception, if no or more than one color type, or if an out
       of bound value is returned for the LED color type.
      is returned when evaluated as a bitmap.
    Returns:
      `nuc_wmi.LED_COLOR_TYPE` index of current LED color type.
    """

    (function_return_type, function_oob_return_value_recover) = verify_nuc_wmi_function_spec( # pylint: disable=unused-variable
        'query_led_color_type',
        nuc_wmi_spec,
        **QUERY_LED_COLOR_TYPE_NUC_WMI_SPEC
    )
    led_color_type_index_hint = query_led_color_type_hint(nuc_wmi_spec, led_type)
    query_led_color_type_byte_list = [METHOD_ID, QUERY_TYPE.index('query_led_color_type'), led_type]


    if led_color_type_index_hint is None:
        write_control_file(query_led_color_type_byte_list, control_file=control_file, debug=debug)

        # Bitmap [0:7], [8:15], [16:23]
        (
            error_code,
            led_color_type_bitmap_1,
            led_color_type_bitmap_2,
            led_color_type_bitmap_3
        ) = read_control_file(control_file=control_file, debug=debug)

        if error_code > 0:
            raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

        led_color_type_bitmaps = [
            led_color_type_bitmap_3,
            led_color_type_bitmap_2,
            led_color_type_bitmap_1
        ]

        led_color_type_index = byte_list_to_index(led_color_type_bitmaps, function_return_type)

        if function_return_type == 'bitmap':
            if len(led_color_type_index) != 1:
                raise NucWmiError(
                    'Error (Intel NUC WMI query_led_color_type function returned either no led color type '
                    'or multiple led color types in bitmap)'
                )

            led_color_type_index = led_color_type_index[0]
    else:
        led_color_type_index = led_color_type_index_hint

    led_color_type_range = defined_indexes(LED_COLOR_TYPE['new'])

    if led_color_type_index not in led_color_type_range:
        raise NucWmiError(
            'Error (Intel NUC WMI query_led_color_type function returned invalid LED color type of %i, '
            'expected one of %s)' % (led_color_type_index, str(led_color_type_range))
        )

    return led_color_type_index


def query_led_control_items( # pylint: disable=too-many-locals
        nuc_wmi_spec,
        led_type,
        led_indicator_option,
        control_file=None,
        debug=False,
        metadata=None # pylint: disable=unused-argument
):
    """
    Query the LED control items for the LED indicator option of the LED type.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led_indicator_option: The LED indicator option to use for the LED type when querying for the LED control items.
      led_type: The LED type for which to query the LED control items.
      metadata: Metadata that may be required to change functional behavior.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
      List of available `nuc_wmi.CONTROL_ITEM` indexes for the specified LED type and LED indicator option.
    """

    (function_return_type, function_oob_return_value_recover) = verify_nuc_wmi_function_spec( # pylint: disable=unused-variable
        'query_led_control_items',
        nuc_wmi_spec,
        **QUERY_LED_CONTROL_ITEMS_NUC_WMI_SPEC
    )
    led_color_type = query_led_color_type(nuc_wmi_spec, led_type, control_file=control_file, debug=debug,
                                          metadata=metadata)

    query_led_control_item_byte_list = [
        METHOD_ID,
        QUERY_TYPE.index('query_led_control_items'),
        led_type,
        led_indicator_option
    ]

    write_control_file(query_led_control_item_byte_list, control_file=control_file, debug=debug)

    # Bitmap [0:7], [8:15], [16:23]
    (
        error_code,
        led_control_item_bitmap_1,
        led_control_item_bitmap_2,
        led_control_item_bitmap_3
    ) = read_control_file(control_file=control_file, debug=debug)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    led_control_item_bitmaps = [
        led_control_item_bitmap_3,
        led_control_item_bitmap_2,
        led_control_item_bitmap_1
    ]
    led_control_item_index = byte_list_to_index(led_control_item_bitmaps, function_return_type)

    led_control_item_index.sort()

    if led_indicator_option == LED_INDICATOR_OPTION_DISABLED or \
       CONTROL_ITEM[led_indicator_option][led_color_type] is None:
        return []

    if led_control_item_index and \
       led_control_item_index[-1] >= len(CONTROL_ITEM[led_indicator_option][led_color_type]):
        raise NucWmiError(
            'Error (Intel NUC WMI query_led_control_items function returned more led control items than ' +
            'supported for the led type and led indicator provided)'
        )

    return led_control_item_index


def query_led_indicator_options(nuc_wmi_spec, led_type, control_file=None, debug=False, metadata=None): # pylint: disable=unused-argument
    """
    Query the LED indicator options available for the LED type.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led_type: The LED type for which to query the LED indicator options.
      metadata: Metadata that may be required to change functional behavior.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
      List of available `nuc_wmi.LED_INDICATOR_OPTION` indexes.
    """

    (function_return_type, function_oob_return_value_recover) = verify_nuc_wmi_function_spec( # pylint: disable=unused-variable
        'query_led_indicator_options',
        nuc_wmi_spec,
        **QUERY_LED_INDICATOR_OPTIONS_NUC_WMI_SPEC
    )
    led_indicator_options_indexes_hint = query_led_indicator_options_hint(nuc_wmi_spec, led_type)
    query_led_indicator_options_byte_list = [
        METHOD_ID,
        QUERY_TYPE.index('query_led_indicator_options'),
        led_type
    ]

    if not led_indicator_options_indexes_hint:
        write_control_file(query_led_indicator_options_byte_list, control_file=control_file, debug=debug)

        # Bitmap [0:7], [8:15], [16:23]
        (
            error_code,
            led_indicator_option_bitmap_1,
            led_indicator_option_bitmap_2,
            led_indicator_option_bitmap_3
        ) = read_control_file(control_file=control_file, debug=debug)

        if error_code > 0:
            raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

        led_indicator_option_bitmaps = [
            led_indicator_option_bitmap_3,
            led_indicator_option_bitmap_2,
            led_indicator_option_bitmap_1
        ]
        led_indicator_option_index = byte_list_to_index(led_indicator_option_bitmaps, function_return_type)

        led_indicator_option_index.sort()
    else:
        led_indicator_option_index = led_indicator_options_indexes_hint

    if led_indicator_option_index and \
       led_indicator_option_index[-1] >= len(LED_INDICATOR_OPTION):
        raise NucWmiError(
            'Error (Intel NUC WMI query_led_indicator_options function returned more led indicator options than ' +
            'supported for the led type provided)'
        )

    return led_indicator_option_index


def query_leds(nuc_wmi_spec, control_file=None, debug=False, metadata=None): # pylint: disable=unused-argument
    """
    List all LED types supported.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      metadata: Metadata that may be required to change functional behavior.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    Returns:
      List of available `nuc_wmi.LED_TYPE` indexes.
    """

    (function_return_type, function_oob_return_value_recover) = verify_nuc_wmi_function_spec( # pylint: disable=unused-variable
        'query_leds',
        nuc_wmi_spec,
        **QUERY_LEDS_NUC_WMI_SPEC
    )
    query_leds_byte_list = [METHOD_ID, QUERY_TYPE.index('query_leds')]

    write_control_file(query_leds_byte_list, control_file=control_file, debug=debug)

    # Bitmap [0:7], [8:15], [16:23]
    (
        error_code,
        led_type_bitmap_1,
        led_type_bitmap_2,
        led_type_bitmap_3
    ) = read_control_file(control_file=control_file, debug=debug)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    led_type_bitmaps = [
        led_type_bitmap_3,
        led_type_bitmap_2,
        led_type_bitmap_1
    ]
    led_type_bitmap_index = byte_list_to_index(led_type_bitmaps, function_return_type)

    led_type_bitmap_index.sort()

    if led_type_bitmap_index and \
       led_type_bitmap_index[-1] >= len(LED_TYPE['new']):
        raise NucWmiError('Error (Intel NUC WMI query_leds function returned more led types than supported)')

    return led_type_bitmap_index
