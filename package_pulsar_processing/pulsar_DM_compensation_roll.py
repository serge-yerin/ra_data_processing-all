'''
'''

import numpy as np
import math
from f_plot_formats import plot1D


def pulsar_DM_compensation_roll(matrix_0, freq_points, fmin, fmax, df, TimeRes, pulsarPeriod, DM0, save_intermediate_data, customDPI):
    '''
    Plots 1D plots of variable
    '''
    dt = np.zeros((freq_points), dtype = 'float')                # time of shifting channel to dedisperse
    for i in range (freq_points):
        dt[i] = (DM0 / 2.410331) * ((10000./math.pow((fmin + df * i), 2)) - (10000./math.pow(fmax, 2)))
    shiftPar = np.zeros((freq_points), dtype = 'int')            # number of steps to shift each row
    for i in range (freq_points):
        shiftPar[i] = -1 * round(pulsarPeriod * (dt[i] / pulsarPeriod - math.floor(dt[i] / pulsarPeriod)) / TimeRes)
        matrix_0[i] = np.roll(matrix_0[i], shiftPar[i])

    return matrix_0, shiftPar
