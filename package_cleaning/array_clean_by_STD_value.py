'''
'''
import numpy as np
import matplotlib.pyplot as plt
import pylab
import math
import time


def array_clean_by_STD_value(array, theshold_sigm):

    startTime = time.time()
    previousTime = startTime

    no_of_lines, no_of_columns = array.shape
    init_sigm = np.std(array)
    init_mean = np.mean(array)

    print ('\n * Simple standard deviation cleaning ')
    print (' ****************************************************************** \n')
    print(' * Array shape:                               ', no_of_lines,' * ', no_of_columns)
    print(' * Initial mean value of array:               ', init_mean)
    print(' * Initial standard deviation value of array: ', init_sigm,'\n')

    # Masking the initial array outside the value interval
    array = np.ma.masked_outside(array, init_mean - theshold_sigm * init_sigm, init_mean + theshold_sigm * init_sigm)

    nowTime = time.time()
    print ('\n  *** Masking took                            ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime

    new_mean = np.mean(array)
    new_sigm = np.std(array)

    mask = array.mask.astype(int)
    array.mask = False
    array = array * np.abs(mask - 1) + mask * new_mean
    cleaned_pixels_num = np.sum(mask)

    print(' * New mean value of array:                   ', new_mean)
    print(' * New standard deviation value of array:     ', new_sigm)
    print(' * Number of cleaned pixels:                  ', int(cleaned_pixels_num))
    print(' * In percent to the array dimensions:        ', np.round(100 * (cleaned_pixels_num / (no_of_lines * no_of_columns)), 2),' % \n')

    nowTime = time.time()
    print ('\n  *** Applying mask and printing took        ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime

    return array, mask, cleaned_pixels_num
