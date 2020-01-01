'''
'''

################################################################################

def specify_frequency_range(array, frequency, freq_start, freq_stop):
    '''
    The function cuts array to necessary frequency range
    Input parameters:

    Output parameters:

    '''
    print ('\n You have chosen the frequency range', round(freq_start,6), '-', round(freq_stop,6), 'MHz')
    A = []
    B = []
    for i in range (len(frequency)):
        A.append(abs(frequency[i] - freq_start))
        B.append(abs(frequency[i] - freq_stop))
    ifmin = A.index(min(A))
    ifmax = B.index(min(B))
    new_array = array[ifmin : ifmax, :]
    print ('\n New data array shape is: ', array.shape)
    frequency = frequency[ifmin : ifmax]

    return new_array, frequency, ifmin, ifmax

################################################################################

################################################################################
