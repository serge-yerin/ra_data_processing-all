'''
'''
import numpy as np


def phase_linearization_rad(matrix):
    '''
    Makes a vector of phase values linear without 360 deg subtraction
    '''
    matrix_lin = np.zeros((len(matrix)))
    matrix_lin[:] = matrix[:]
    const = 0
    for elem in range(1, len(matrix)):
        if (matrix[elem] - matrix[elem-1]) > 4:
            const = const + 2*np.pi
        matrix_lin[elem] = matrix_lin[elem] - const
    const = 0
    for elem in range(1, len(matrix)):
        if (matrix[elem-1] - matrix[elem]) > 4:
            const = const + 2*np.pi
        matrix_lin[elem] = matrix_lin[elem] + const
    return matrix_lin
