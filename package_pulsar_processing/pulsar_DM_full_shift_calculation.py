'''
'''

import numpy as np
import math

def DM_full_shift_calc(freq_points, fmin, fmax, df, TimeRes, DM0, receiver_type):
    '''
    !!!! To delete receiver type for this function as an input argument
    Calculation of the number of time point to shift each frequency channel
    in dynamic spectra to compensate the dispersion opf the pulsar
    '''

    dt = np.zeros((freq_points), dtype = 'float')                # time of shifting channel to dedisperse
    shiftPar = np.zeros((freq_points), dtype = 'int')            # number of steps to shift each row

    for i in range (freq_points):
        #dt[i] = (DM0 / 2.410331) * ((10000./math.pow((fmin + df * i), 2)) - (10000./math.pow(fmax, 2)))
        dt[i] = (DM0 / 2.4102873860269) * ((10000./math.pow((fmin + df * (i+1)), 2)) - (10000./math.pow(fmax, 2)))  # Constant from Alice
        #if receiver_type == '.adr':
        #    shiftPar[i] = -1 * round((1/2.) * pulsarPeriod * (dt[i] / pulsarPeriod - math.floor(dt[i] / pulsarPeriod)) / TimeRes)
        #if receiver_type == '.jds':
        shiftPar[i] = -1 * round(dt[i] / TimeRes)

    return shiftPar
