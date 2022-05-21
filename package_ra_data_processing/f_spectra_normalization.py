
import numpy as np


def normalization_db(data, freq_points_num, num_of_spectra):
    """
    Normalizing amplitude-frequency responce (spectra) in dB!!!
    Input parameters:
        data - input array
        freq_points_num - number of frequency channels (data array dimension)
        Num_of_apectra - number of spectra (data array dimension)
    Output parameters:
        data - result normalized data array
    """
    # data_min_norm = [0 for col in range(freq_points_num)]
    data_min_norm = np.zeros(freq_points_num)
    for j in range(freq_points_num):
        data_min_find = data[:, j]  # taking 1 line of matrix to find 5 minimum values
        # calculating mean of 5 minimum values knowing their indexes
        data_min_norm[j] = np.mean(data_min_find[data_min_find.argsort()[:5]])

    for k in range(num_of_spectra):
        with np.errstate(invalid='ignore'):
            data[k, :] = data[k, :] - data_min_norm[:]
    return data


def normalization_lin(data, freq_points_num, num_of_spectra):
    """
    Normalization of amplitude-frequency response in linear scale!!!
    Input parameters:
        data - input array
        freq_points_num - number of frequency channels (data array dimension)
        Num_of_apectra - number of spectra (data array dimension)
    Output parameters:
        data - result normalized data array
    """
    # data_min_norm = [0 for col in range(freq_points_num)]
    data_min_norm = np.zeros(freq_points_num)
    for i in range(freq_points_num):
        data_min_findind = data[i, :]    # taking 1 line of matrix to find 5 minimum values
        # calculating mean of 5 minimum values knowing their indexes
        data_min_norm[i] = np.mean(data_min_findind[data_min_findind.argsort()[:5]])

    for k in range(num_of_spectra):
        data[:, k] = data[:, k] / data_min_norm[:]
    return data
