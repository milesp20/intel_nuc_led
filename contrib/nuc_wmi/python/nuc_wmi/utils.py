"""
`nuc_wmi.utils` provides utility functions for the WMI functions.
"""

import fcntl
import json
import os
import pkg_resources

from nuc_wmi import LED_COLOR_TYPE, LED_INDICATOR_OPTION, LED_TYPE, NucWmiError

BYTE_LIST_RETURN_TYPES = [
    'bitmap',
    'index'
]
DEFAULT_NUC_WMI_FUNCTION_RETURN_TYPES = [
    None,
    'bitmap',
    'index'
]
DEFAULT_NUC_WMI_FUNCTION_OOB_RETURN_VALUE_RECOVER_VALUES = [
    False,
    True
]
EXCLUSIVE_BLOCKING_FILE_LOCK = fcntl.LOCK_EX
EXCLUSIVE_NON_BLOCKING_FILE_LOCK = fcntl.LOCK_EX | fcntl.LOCK_NB
NUC_WMI_SPEC_FILE = [
    os.path.expanduser('~/.nuc_wmi/nuc_wmi_spec/nuc_wmi_spec.json'),
    '/etc/nuc_wmi/nuc_wmi_spec/nuc_wmi_spec.json',
    pkg_resources.resource_filename('nuc_wmi', 'etc/nuc_wmi/nuc_wmi_spec/nuc_wmi_spec.json')
]


def acquire_file_lock(filehandle, blocking_file_lock=False):
    """
    Acquires a lock on the open file descriptor.

    Args:
      filehandle: File object handle to acquire file lock on. Must respond to fileno and name requests.
    Exceptions:
      Raises `NucWmiError` on failure to acquire the NUC WMI lock file.
    Returns:
      None
    """

    if blocking_file_lock:
        lock_type = EXCLUSIVE_BLOCKING_FILE_LOCK
    else:
        lock_type = EXCLUSIVE_NON_BLOCKING_FILE_LOCK

    try:
        fcntl.flock(filehandle.fileno(), lock_type)
    except (IOError, OSError) as err:
        raise NucWmiError(
            'Error (Intel NUC WMI failed to acquire lock file %s: %s)' % (filehandle.name, str(err))
        ) from err


def byte_list_to_bitmap(int_byte_list):
    """
    Turns an list of integer bytes into a little endian binary bitmap string.

    Args:
      int_byte_list: List of integers to be converted into a bitmap string. May
                     be int strings. Integers must be 0-255.
    Exceptions:
      Raises `ValueError` for int conversion error.
    Returns:
      Bitmap string of the integer byte list.
    """

    for int_byte in int_byte_list:
        if int(int_byte) < 0 or int(int_byte) > 255:
            raise ValueError('int byte values must be 0-255')

    return ''.join(["{0:b}".format(int(int_byte)).zfill(8) for int_byte in int_byte_list or [0]])


def byte_list_to_index(byte_list, byte_list_type):
    """
    Returns the byte list converted to an index or a list of indexes by casting the byte list based on the byte list
    type of either bitmap or index.
    """

    if byte_list_type not in BYTE_LIST_RETURN_TYPES:
        raise NucWmiError(
            'Error (Invalid byte list type specified, cannot cast byte list to index: %s)' % str(byte_list_type)
        )

    byte_list_bitmap = byte_list_to_bitmap(byte_list)

    if byte_list_type == 'bitmap':
        # Reverse the bitmap so its in big endian instead of little endian so that it matches
        # the alignment of entries in configuration element lists.
        byte_list_bitmap_reversed = byte_list_bitmap[::-1]

        # Extract the indexes of defined/enabled bits
        return [index for index, bit in enumerate(byte_list_bitmap_reversed) if int(bit)]

    # Cast the little endian binary bitmap string into an integer.
    return int(byte_list_bitmap, 2)


def defined_indexes(items):
    """
    Returns the indexes from the items list with a non None value.

    Args:
      items: Item list for which to return non None indexes.
    Returns:
      List of index numbers that had non None values.
    """

    if issubclass(items.__class__, list):
        return [index for index, value in enumerate(items) if value is not None]

    return []


def load_nuc_wmi_spec():
    """
    Loads the NUC WMI specification configuration JSON file.

    Exceptions:
      Raises `NucWmiError` if no specification file is found or the file loaded does not contain an object with a
      `nuc_wmi_spec` key.
    Returns:
      Dict of nuc_wmi specification definition.
    """

    for nuc_wmi_spec_file in NUC_WMI_SPEC_FILE:
        if not os.path.exists(nuc_wmi_spec_file):
            continue

        try:
            with open(nuc_wmi_spec_file, 'r', encoding='utf8') as fin:
                nuc_wmi_spec = json.load(fin)
        except Exception as err:
            raise NucWmiError(
                'Error (Intel NUC WMI failed to load NUC WMI spec configuration file %s: %s)' % \
                (nuc_wmi_spec_file, str(err))
            ) from err

        if not issubclass(nuc_wmi_spec.__class__, dict) or \
           'nuc_wmi_spec' not in nuc_wmi_spec:
            raise NucWmiError(
                'Error (Intel NUC WMI NUC WMI spec configuration file schema is invalid: %s)' % nuc_wmi_spec_file
            )

        return nuc_wmi_spec

    raise NucWmiError(
        'Error (Intel NUC WMI failed to find NUC WMI spec configuration file: %s)' % str(NUC_WMI_SPEC_FILE)
    )


def query_led_color_type_hint(nuc_wmi_spec, led_type_index):
    """
    Checks the NUC WMI specification configration file for LED color type hint to avoid having to call
    query_led_color_type WMI function.

    Args:
      led_type_index: The LED type index for which to query the LED color type hint.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Returns:
      None or the LED color type string as its `nuc_wmi.LED_COLOR_TYPE` index.
    """

    if led_type_index < len(LED_TYPE['new']):
        led_color_type_hint = nuc_wmi_spec.get('led_hints', {}).get('color_type', {}).get(
            LED_TYPE['new'][led_type_index]
        )
    else:
        return None

    try:
        return LED_COLOR_TYPE['new'].index(led_color_type_hint)
    except ValueError:
        pass

    return None


def query_led_indicator_options_hint(nuc_wmi_spec, led_type_index):
    """
    Checks the NUC WMI specification configuration file for LED indicator options hint to avoid having to call
    query_led_indicator_options WMI function.

    Args:
      led_type_index: The LED type index for which to query the LED indicator options hint.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Returns:
      Empty list or the list of indicator option strings as its `nuc_wmi.LED_INDICATOR_OPTION` index for the specified
      LED type index.
    """

    indicator_options_indexes = []

    if led_type_index < len(LED_TYPE['new']):
        indicator_options_hint = nuc_wmi_spec.get('led_hints', {}).get('indicator_options', {}).get(
            LED_TYPE['new'][led_type_index],
            []
        )
    else:
        return indicator_options_indexes

    for index, indicator_option in enumerate(LED_INDICATOR_OPTION):
        if indicator_option in indicator_options_hint:
            indicator_options_indexes.append(index)

    indicator_options_indexes.sort()

    return indicator_options_indexes


def query_led_rgb_color_type_dimensions_hint(nuc_wmi_spec, led_type):
    """
    Checks the NUC WMI specification configration file for LED RGB color type dimensions hint to avoid having to call
    query_led_color_type WMI function.

    Args:
      led_type: The LED type for which to query the LED RGB color type dimensions hint.
      nuc_wmi_spec: The NUC WMI specification configuration.
    Returns:
      None or 1 or 3 for the RGB color dimensions.
    """

    rgb_color_type_dimensions = nuc_wmi_spec.get('led_hints', {}).get('rgb_color_type_dimensions', {}).get(led_type)

    if rgb_color_type_dimensions is not None and rgb_color_type_dimensions not in [1, 3]:
        raise NucWmiError(
            'Error (Intel NUC WMI spec has an invalid rgb_color_type_dimensions led_hint for LED %s, '
            'expected one of: [1, 3]' % led_type
        )

    return rgb_color_type_dimensions



def verify_nuc_wmi_function_spec(nuc_wmi_function_name, nuc_wmi_spec, nuc_wmi_function_return_types=None,
                                 nuc_wmi_function_oob_return_value_recover_values=None):
    """
    Verifies the the specified NUC WMI function against the NUC WMI specification and ensures the specification matches
    the allowed return types and OOB recover values.

    Args:
       nuc_wmi_function_name: The NUC WMI function being verified.
       nuc_wmi_function_return_types: The return types supported for the current NUC WMI function being verified.
       nuc_wmi_oob_return_value_recover_values: The OOB return recover values supported for the current NUC WMI function
                                                being verified.
       nuc_wmi_spec: The NUC WMI specification definition that the function is being verified against.
    Exceptions:
       Raises `NucWmiError` if the NUC WMI function name in the NUC WMI spec isnt using a supported function return type
       or OOB recover value.
    Returns:
       A tuple of NUC WMI function return type and NUC WMI function OOB recover value.
    """

    if nuc_wmi_function_return_types is None:
        nuc_wmi_function_return_types = DEFAULT_NUC_WMI_FUNCTION_RETURN_TYPES

    if nuc_wmi_function_oob_return_value_recover_values is None:
        nuc_wmi_function_oob_return_value_recover_values = DEFAULT_NUC_WMI_FUNCTION_OOB_RETURN_VALUE_RECOVER_VALUES

    if nuc_wmi_function_name not in nuc_wmi_spec.get('function_return_type', {}):
        raise NucWmiError(
            'Error (NUC WMI specification does not include a function_return_type definition for NUC WMI function: '
            '%s' % nuc_wmi_function_name
        )

    if nuc_wmi_function_name not in nuc_wmi_spec.get('function_oob_return_value_recover', {}):
        raise NucWmiError(
            'Error (NUC WMI specification does not include a function_oob_return_value_recover definition for NUC WMI'
            ' function: %s' % nuc_wmi_function_name
        )

    function_return_type = nuc_wmi_spec.get('function_return_type', {}).get(nuc_wmi_function_name)

    if function_return_type not in nuc_wmi_function_return_types:
        raise NucWmiError(
            'Error (Intel NUC WMI spec has an invalid function_return_type for function %s, allowed return types:'
            ' %s)' % (nuc_wmi_function_name, json.dumps(nuc_wmi_function_return_types))
        )

    function_oob_return_value_recover = bool(
        nuc_wmi_spec.get('function_oob_return_value_recover', {}).get(nuc_wmi_function_name)
    )

    if function_oob_return_value_recover not in nuc_wmi_function_oob_return_value_recover_values:
        raise NucWmiError(
            'Error (Intel NUC WMI spec has an invalid function_oob_return_value_recover for function %s, allowed OOB '
            'recover values: %s)' % \
            (nuc_wmi_function_name, json.dumps(nuc_wmi_function_oob_return_value_recover_values))
        )

    return (function_return_type, function_oob_return_value_recover)
