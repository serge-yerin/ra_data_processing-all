'''
'''
import numpy as np

def average_some_lines_of_array(array, no_of_lines_to_average = 2):
    '''
    Averaging of several lines of array to one line
    '''
    avergaed_array = np.cumsum(array, 0)[no_of_lines_to_average-1::no_of_lines_to_average]/float(no_of_lines_to_average)
    avergaed_array[1:] = avergaed_array[1:] - avergaed_array[:-1]
    return avergaed_array


def DM_compensation_with_indices_changes (array, shift_vector):

    rows, column_indices = np.ogrid[:array.shape[0], :array.shape[1]]
    result = np.zeros_like(array)

    # Use always a negative shift, so that column_indices are valid.
    # (could also use module operation)

    shift_vector[shift_vector < 0] += array.shape[1]
    column_indices = column_indices - shift_vector[:, np.newaxis]

    result = array[rows, column_indices]
    return result
