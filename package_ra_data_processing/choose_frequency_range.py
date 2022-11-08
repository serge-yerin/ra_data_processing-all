

def choose_frequency_range(frequency_list, data_array, freq_start, freq_stop, fft_size, fmin, fmax):
    """
    Cut from array of data the range of needed frequencies

    Args:
        frequency_list:
        data_array:
        freq_start:
        freq_stop:
        fft_size:
        fmin:
        fmax:

    Returns:

    """
    if (frequency_list[0] < freq_start < frequency_list[-1]) and \
            (frequency_list[0] < freq_stop < frequency_list[-1]) and (freq_start < freq_stop):

        print('\n  * You have chosen the frequency range', freq_start, '-', freq_stop, 'MHz')

        tmp_list_a = []
        tmp_list_b = []
        for i in range(len(frequency_list)):
            tmp_list_a.append(abs(frequency_list[i] - freq_start))
            tmp_list_b.append(abs(frequency_list[i] - freq_stop))
        ifmin = tmp_list_a.index(min(tmp_list_a))
        ifmax = tmp_list_b.index(min(tmp_list_b))
        data_array = data_array[ifmin: ifmax, :]  # Reshaping array

        print('\n    New data array shape is: ', data_array.shape)

        # Changing other data for further processing
        frequency_list = frequency_list[ifmin:ifmax]
        fft_size = len(frequency_list)
        fmin = frequency_list[0]
        fmax = frequency_list[fft_size-1]

        del tmp_list_a, tmp_list_b, ifmin, ifmax
    else:
        print('  !!! Error of frequency limits !!! \n    Continue processing the whole array')

    return frequency_list, data_array, fft_size, fmin, fmax
