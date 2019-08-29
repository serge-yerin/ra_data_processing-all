'''
'''
import numpy as np
from astropy.coordinates import AltAz
################################################################################

def find_max_altitude(alt_az_list):
    """
    """
    x = np.linspace(0, len(alt_az_list), len(alt_az_list))
    func = [0] * len(alt_az_list)
    for i in range (len(alt_az_list) - 1):
        func[i] = float(alt_az_list[i].alt.degree)
    ymax = max(func)
    xpos = func.index(ymax)
    xmax = x[xpos] - 1
    return xmax, ymax
