"""
`nuc_wmi.utils` provides utility functions for the WMI functions.
"""

import fcntl
import json
import os
import pkg_resources

from nuc_wmi import NucWmiError

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
NUC_WMI_SPEC_FILE = [
    os.path.expanduser('~/.nuc_wmi/nuc_wmi_spec/nuc_wmi_spec.json'),
    '/etc/nuc_wmi/nuc_wmi_spec/nuc_wmi_spec.json',
    pkg_resources.resource_filename('nuc_wmi', 'etc/nuc_wmi/nuc_wmi_spec/nuc_wmi_spec.json')
]


def acquire_file_lock(filehandle):
    """
    Acquires a lock on the open file descriptor.

    Args:
      filehandle: File object handle to acquire file lock on. Must respond to fileno and name requests.
    Exceptions:
      Raises `NucWmiError` on failure to acquire the NUC WMI lock file.
    Returns:
      None
    """

    try:
        fcntl.flock(filehandle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
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
