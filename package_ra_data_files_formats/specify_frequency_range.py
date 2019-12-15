'''
'''
#import numpy as np
#from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR, ChunkHeaderReaderADR

################################################################################

def specify_frequency_range(array, frequency, freqStart, freqStop):
    '''
    The function cuts array to necessary frequency range
    Input parameters:

    Output parameters:

    '''
    print ('\n You have chosen the frequency range', freqStart, '-', freqStop, 'MHz')
    A = []
    B = []
    for i in range (len(frequency)):
        A.append(abs(frequency[i] - freqStart))
        B.append(abs(frequency[i] - freqStop))
    ifmin = A.index(min(A))
    ifmax = B.index(min(B))
    array = array[ifmin:ifmax, :]
    print ('\n New data array shape is: ', array.shape)
    frequency = frequency[ifmin:ifmax]

    return array, frequency, ifmin, ifmax

################################################################################

################################################################################
'''
if __name__ == '__main__':

    folder_path = 'DATA/'
    file_list = ['A170712_160219.adr', 'File 10 2048FFT A 100 ms 141119_164450.adr']
    equal_or_not = chaeck_if_ADR_files_of_equal_parameters(folder_path, file_list)
'''
