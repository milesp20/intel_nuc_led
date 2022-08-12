"""
`nuc_wmi.utils` provides utility functions for the WMI functions.
"""

import fcntl

from nuc_wmi import NucWmiError


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
    Turns an list of integer bytes into a bitmap string.

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
