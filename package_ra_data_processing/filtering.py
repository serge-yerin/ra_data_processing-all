"""
Simple 1D data filters
"""

from scipy import ndimage
from scipy.ndimage.filters import uniform_filter1d


def median_filter(data, window_len):
    fitered_data = ndimage.median_filter(data, size=window_len)
    return fitered_data


def average_filter(data, window_len):
    fitered_data = uniform_filter1d(data, size=window_len)
    return fitered_data
