'''
'''
import numpy as np

def pulsar_DM_compensation_with_indices_changes (array, shift_vector):

    rows, column_indices = np.ogrid[:array.shape[0], :array.shape[1]]
    result = np.zeros_like(array)

    # Use always a negative shift, so that column_indices are valid (could also use module operation).
    shift_vector[shift_vector < 0] += array.shape[1]

    column_indices = column_indices - shift_vector[:, np.newaxis]

    result = array[rows, column_indices]
    return result
