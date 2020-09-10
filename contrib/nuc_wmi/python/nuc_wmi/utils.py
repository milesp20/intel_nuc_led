"""
`nuc_wmi.utils` provides utility functions for the WMI functions.
"""

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

    return ''.join(["{0:b}".format(int_byte).zfill(8) for int_byte in int_byte_list or [0]])
