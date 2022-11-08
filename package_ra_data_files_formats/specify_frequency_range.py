################################################################################

def specify_frequency_range(array, frequency, freq_start, freq_stop):
    """
    The function cuts array to necessary frequency range
    Args:
        array: 
        frequency: 
        freq_start: 
        freq_stop: 

    Returns:
        new_array:
        frequency:
        ifmin:
        ifmax:
    """
    print('\n You have chosen the frequency range', round(freq_start, 6), '-', round(freq_stop, 6), 'MHz')
    tmp_list_a = []
    tmp_list_b = []
    for i in range(len(frequency)):
        tmp_list_a.append(abs(frequency[i] - freq_start))
        tmp_list_b.append(abs(frequency[i] - freq_stop))
    ifmin = tmp_list_a.index(min(tmp_list_a))
    ifmax = tmp_list_b.index(min(tmp_list_b))
    del tmp_list_a, tmp_list_b
    new_array = array[ifmin: ifmax, :]
    print('\n New data array shape is: ', array.shape)
    frequency = frequency[ifmin: ifmax]

    return new_array, frequency, ifmin, ifmax
