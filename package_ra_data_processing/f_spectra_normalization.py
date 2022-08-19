
import numpy as np


def normalization_db(data, freq_points_num, num_of_spectra):
    """
    Normalizing amplitude-frequency response (spectra) in dB!!!
    Input parameters:
        data - input array
        freq_points_num - number of frequency channels (data array dimension array.shape[1])
        num_of_spectra - number of spectra (data array dimension array.shape[0])
    Output parameters:
        data - result normalized data array
    """
    data_min_norm = np.zeros(freq_points_num, dtype=np.float64)
    for j in range(freq_points_num):
        data_min_find = data[:, j]  # taking 1 line of matrix to find 5 minimum values
        # calculating mean of 5 minimal values knowing their indexes
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
        Num_of_spectra - number of spectra (data array dimension)
    Output parameters:
        data - result normalized data array
    """
    data_min_norm = np.zeros(freq_points_num, dtype=np.float64)
    for i in range(freq_points_num):
        data_min_findind = data[i, :]    # taking 1 line of matrix to find 5 minimum values
        # calculating mean of 5 minimal values knowing their indexes
        data_min_norm[i] = np.mean(data_min_findind[data_min_findind.argsort()[:5]])

    data_min_norm[data_min_norm == 0] = 1e-16

    for k in range(num_of_spectra):
        data[:, k] = data[:, k] / data_min_norm[:]
    return data
