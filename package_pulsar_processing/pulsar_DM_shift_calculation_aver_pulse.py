'''
'''

import numpy as np
import math

def pulsar_DM_shift_calculation_aver_pulse(freq_points, fmin, fmax, df, TimeRes, DM0, pulsar_period):
    '''
    Calculation of the number of time point to shift each frequency channel
    in dynamic spectra to compensate the dispersion of the pulsar
    in an average pulse file (shift in limits of pulsar period)
    '''

    shift_par = np.zeros((freq_points), dtype = 'int')            # number of steps to shift each row

    for i in range (freq_points):
        dt = (DM0 / 2.410331) * ((10000./math.pow((fmin + df * i), 2)) - (10000./math.pow(fmax, 2)))
        shift_par[i] = -1 * round(pulsar_period * (dt / pulsar_period - math.floor(dt / pulsar_period)) / TimeRes)

    return shift_par
