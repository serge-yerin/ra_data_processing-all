'''
'''
from scipy import ndimage


def median_filter(data, window_len):
    fitered_data = ndimage.median_filter(data, size=window_len)
    return fitered_data