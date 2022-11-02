import numpy as np
import math


def pulsar_DM_compensation_roll(data_array, freq_points, fmin, fmax, df, time_res, pulsar_period, pulsar_dm):

    """
    Function compensates dispersion delay with rolling each row of the array
    Args:
        data_array: array of data to compensate dispersion delay (np.array)
        freq_points: a list of frequency points (np.float)
        fmin: minimal frequency (float)
        fmax: maximal frequency (float)
        df: frequency resolution (float)
        time_res: time resolution (float)
        pulsar_period: pulsar period (np.float64)
        pulsar_dm: pulsar dispersion measure (np.float)

    Returns:
        data_array: data array with compensated dispersion delay
        shift_parameter: a vector of shift numbers for each array row
    """

    time_shift = np.zeros((freq_points), dtype='float')  # time of shifting channel to dedisperse
    for i in range(freq_points):
        time_shift[i] = (pulsar_dm / 2.410331) * ((10000./math.pow((fmin + df * i), 2)) - (10000./math.pow(fmax, 2)))
    shift_parameter = np.zeros((freq_points), dtype='int')  # number of steps to shift each row
    for i in range(freq_points):
        shift_parameter[i] = -1 * round(pulsar_period * (time_shift[i] / pulsar_period -
                                                         math.floor(time_shift[i] / pulsar_period)) / time_res)
        data_array[i] = np.roll(data_array[i], shift_parameter[i])

    return data_array, shift_parameter
