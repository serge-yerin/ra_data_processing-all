

import numpy as np
import math


def DM_full_shift_calc(freq_points, fmin, fmax, df, time_resolution, disp_meas, receiver_type):
    """
    !!!! To delete receiver type for this function as an input argument !!!
    Calculation of the number of time point to shift each frequency channel
    in dynamic spectra to remove the dispersion delay of the pulsar
    freq_points - number of frequency points in the range
    fmin - minimal frequency, MHz
    fmax - maximal frequency, MHz
    df - frequency resolution, MHz
    time_resolution - time resolution, seconds
    disp_meas - pulsar dispersion measure, pc * cm-3
    """

    dt = np.zeros(freq_points, dtype='float')                # time of shifting channel to remove dispersion delay
    shift_pix_vector = np.zeros(freq_points, dtype='int')    # number of steps to shift each row

    for i in range(freq_points):
        # New constant from Alice (previously was 2.410331)
        dt[i] = (disp_meas / 2.4102873860269) * ((10000./math.pow((fmin + df * (i+1)), 2)) - (10000./math.pow(fmax, 2)))

        # if receiver_type == '.adr':
        #    shift_pix_vector[i] = -1 * round((1/2.) * pulsarPeriod *
        #    (dt[i] / pulsarPeriod - math.floor(dt[i] / pulsarPeriod)) / time_resolution)
        # if receiver_type == '.jds':

        shift_pix_vector[i] = -1 * round(dt[i] / time_resolution)

    return shift_pix_vector
