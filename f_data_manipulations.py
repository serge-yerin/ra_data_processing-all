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
