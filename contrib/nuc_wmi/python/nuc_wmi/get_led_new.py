"""
`nuc_wmi.get_led_new` provides an interface to the new WMI get led set of functions.
"""

from nuc_wmi import NucWmiError, LED_INDICATOR_OPTION, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file
from nuc_wmi.utils import byte_list_to_index, verify_nuc_wmi_function_spec

GET_LED_CONTROL_ITEM_NUC_WMI_SPEC = {
    'nuc_wmi_function_return_types': ['bitmap', 'index'],
    'nuc_wmi_function_oob_return_value_recover_values': [False]
}
GET_LED_INDICATOR_OPTION_NUC_WMI_SPEC = {
    'nuc_wmi_function_return_types': ['bitmap', 'index'],
    'nuc_wmi_function_oob_return_value_recover_values': [False]
}
GET_LED_TYPE = [
    'get_led_indicator_option',
    'get_led_control_item'
]
METHOD_ID = 0x04


def get_led_control_item( # pylint: disable=too-many-arguments
        nuc_wmi_spec,
        led_type,
        led_indicator_option,
        control_item,
        control_file=None,
        debug=False,
        metadata=None # pylint: disable=unused-argument
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
      metadata: Metadata that may be required to change functional behavior.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      if `read_control_file` or `write_control_file` raise an exception, or if no or more than one led control item
      value is returned when evaluated as a bitmap.
    Returns:
      `nuc_wmi.CONTROL_ITEM` value for the control item of the indicator option for the specified LED type.
    """

    (function_return_type, function_oob_return_value_recover) = verify_nuc_wmi_function_spec( # pylint: disable=unused-variable
        'get_led_control_item',
        nuc_wmi_spec,
        *GET_LED_CONTROL_ITEM_NUC_WMI_SPEC
    )
    get_led_control_item_byte_list = [
        METHOD_ID,
        GET_LED_TYPE.index('get_led_control_item'),
        led_type,
        led_indicator_option,
        control_item
    ]

    write_control_file(get_led_control_item_byte_list, control_file=control_file, debug=debug)

    (
        error_code,
        control_item_value,
        reserved_byte_1,    # pylint: disable=unused-variable
        reserved_byte_2     # pylint: disable=unused-variable
    ) = read_control_file(control_file=control_file, debug=debug)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))

    control_item_value_index = byte_list_to_index([control_item_value], function_return_type)

    if function_return_type == 'index':
        return control_item_value_index

    if len(control_item_value_index) != 1:
        raise NucWmiError(
            'Error (Intel NUC WMI get_led_control_item function returned either no led control item value '
            'or multiple control item values in bitmap)'
        )

    return control_item_value_index[0]


def get_led_indicator_option(nuc_wmi_spec, led_type, control_file=None, debug=False, metadata=None): # pylint: disable=unused-argument
    """
    Get the current indicator option for the LED type.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      led_type: The LED type for which to retrieve the current indicator option.
      metadata: Metadata that may be required to change functional behavior.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      if `read_control_file` or `write_control_file` raise an exception, or if no or more than one led indicator option
      is returned when evaluated as a bitmap.
    Returns:
      `nuc_wmi.LED_INDICATOR_OPTION` index of the current LED indicator option.
    """

    (function_return_type, function_oob_return_value_recover) = verify_nuc_wmi_function_spec( # pylint: disable=unused-variable
        'get_led_indicator_option',
        nuc_wmi_spec,
        *GET_LED_INDICATOR_OPTION_NUC_WMI_SPEC
    )
    get_led_indicator_option_byte_list = [
        METHOD_ID,
        GET_LED_TYPE.index('get_led_indicator_option'),
        led_type
    ]

    write_control_file(get_led_indicator_option_byte_list, control_file=control_file, debug=debug)

    (
        error_code,
        led_indicator_option,
        reserved_byte_1,      # pylint: disable=unused-variable
        reserved_byte_2       # pylint: disable=unused-variable
    ) = read_control_file(control_file=control_file, debug=debug)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR[error_code])

    led_indicator_option_index = byte_list_to_index([led_indicator_option], function_return_type)

    if function_return_type == 'index':
        return led_indicator_option_index

    if len(led_indicator_option_index) != 1:
        raise NucWmiError(
            'Error (Intel NUC WMI get_led_indicator_option function returned either no led indicator option or '
            'multiple led indicator options in bitmap)'
        )

    if led_indicator_option_index[0] >= len(LED_INDICATOR_OPTION):
        raise NucWmiError(
            'Error (Intel NUC WMI get_led_indicator_option function returned invalid led indicator option)'
        )

    return led_indicator_option_index[0]
