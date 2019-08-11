'''
'''
import numpy as np
from astropy.coordinates import AltAz
from package_astronomy.find_max_altitude import find_max_altitude
################################################################################

def find_rize_and_set_points(alt_az_list):
    """
    """
    x = np.linspace(0, len(alt_az_list), len(alt_az_list))
    func = np.zeros(len(alt_az_list))
    for i in range (len(alt_az_list)):
        func[i] = float(alt_az_list[i].alt.degree)

    xmax, ymax = find_max_altitude(alt_az_list)

    not_find_before = 0
    not_find_after = 0

    # Finding the value closest to zero before culmination
    test_func = func[0 : int(xmax)]
    abs_func = np.abs(test_func)
    closest_to_zero_index = np.argmin(abs_func)
    if (func[closest_to_zero_index-1] < 0) and (func[closest_to_zero_index+1] > 0):
        x_rise = closest_to_zero_index
    elif func[closest_to_zero_index-1] > 0 and func[closest_to_zero_index+1] < 0:
        x_set = closest_to_zero_index
    else:
        x_rise = 0

    # Finding the value closest to zero after culmination

    test_func = func[int(xmax) : len(alt_az_list)-1]
    abs_func = np.abs(test_func)
    closest_to_zero_index = np.argmin(abs_func)
    closest_to_zero_index = closest_to_zero_index + int(xmax)

    if func[closest_to_zero_index-1] < 0 and func[closest_to_zero_index+1] > 0:
        x_rise = closest_to_zero_index
    elif func[closest_to_zero_index-1] > 0 and func[closest_to_zero_index+1] < 0:
        x_set = closest_to_zero_index
    else:
        x_set = len(alt_az_list) - 1

    return x_rise, x_set
