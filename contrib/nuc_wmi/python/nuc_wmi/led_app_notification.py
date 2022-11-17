"""
`nuc_wmi.led_app_notification` provides an interface to the WMI notification functions.
"""

from nuc_wmi import NucWmiError, RETURN_ERROR
from nuc_wmi.control_file import read_control_file, write_control_file
from nuc_wmi.utils import verify_nuc_wmi_function_spec

METHOD_ID = 0x07
NOTIFICATION_TYPE = [
    None,
    'save_led_config'
]
SAVE_LED_CONFIG_NUC_WMI_SPEC = {
    'nuc_wmi_function_return_types': [None],
    'nuc_wmi_function_oob_return_value_recover_values': [False]
}


def save_led_config(nuc_wmi_spec, control_file=None, debug=False, metadata=None): # pylint: disable=unused-argument
    """
    Send a save LED configuration LED app notification.

    Args:
      control_file: Sets the control file to use if provided, otherwise `nuc_wmi.CONTROL_FILE` is used.
      debug: Whether or not to enable debug logging of read and write to the NUC LED control file to stderr.
      metadata: Metadata that may be required to change functional behavior.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Exceptions:
      Raises `nuc_wmi.NucWmiError` exception if kernel module returns an error code,
      or if `read_control_file` or `write_control_file` raise an exception.
    """

    (function_return_type, function_oob_return_value_recover) = verify_nuc_wmi_function_spec( # pylint: disable=unused-variable
        'save_led_config',
        nuc_wmi_spec,
        *SAVE_LED_CONFIG_NUC_WMI_SPEC
    )
    notification_byte_list = [
        METHOD_ID,
        NOTIFICATION_TYPE.index('save_led_config')
    ]

    write_control_file(notification_byte_list, control_file=control_file, debug=debug)

    (
        error_code,
        reserved_byte_1, # pylint: disable=unused-variable
        reserved_byte_2, # pylint: disable=unused-variable
        reserved_byte_3  # pylint: disable=unused-variable
    ) = read_control_file(control_file=control_file, debug=debug)

    if error_code > 0:
        raise NucWmiError(RETURN_ERROR.get(error_code, 'Error (Unknown NUC WMI error code)'))
