'''
'''
import numpy as np
from astropy.coordinates import AltAz
from package_astronomy.find_max_altitude import find_max_altitude
################################################################################

def find_rize_and_set_points(alt_az_list, degree):
    """
    """
    x = np.linspace(0, len(alt_az_list), len(alt_az_list))
    func = np.zeros(len(alt_az_list))
    for i in range (len(alt_az_list)):
        func[i] = float(alt_az_list[i].alt.degree)

    x_rise = []
    x_set = []
    func = func - degree
    for i in range (len(func) - 2):
        if (func[i] < 0) and (func[i+1] > 0):
            x_rise.append(i+1)
        if func[i] > 0 and func[i+1] < 0:
            x_set.append(i)

    return x_rise, x_set
