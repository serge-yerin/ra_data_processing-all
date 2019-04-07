'''
'''
#import struct
#import os
#import math
#import numpy as np
#import datetime
from astropy.io import fits

################################################################################

def FileHeaderReaderFITS(filepath):
    '''
    Reads info from FITS (.fits) data file header and returns needed parameters to the main script
    Input parameters:

    Output parameters:

    '''

    file = open(filepath, 'rb')

    hdul = fits.open(filepath)
    #hdul.info()

    hdr = hdul[0].header

    print(' \n\n')
    print(' Length of header = ', len(hdr), '\n')

    for i in range (len(hdr)):
        print (' %2i' % i, ' %50s: ' % hdr.comments[i], hdr[i])

    print(' \n\n\n')

    # print(repr(hdr)) - representation as it is in file
    # print(list(hdr.keys())) - prints all keywords in header

    hdr1 = hdul[1].header

    print(' \n\n')
    print(' Length of header = ', len(hdr1), '\n')

    for i in range (len(hdr1)):
        print (' %2i' % i, ' %50s: ' % hdr1.comments[i], hdr1[i])

    print(' \n\n\n')

    data = hdul[1].data
    print(data.shape)
    print(data.dtype.name)
    array0 = [8, 10, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41]
    array1 = [5, 12, 5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  43]
    for i in range (17):
        print('   * ', hdr1[array0[i]], ',   ', hdr1[array1[i]])
        print(data.field(i))
        print(' \n')


    hdr2 = hdul[2].header

    print(' \n\n')
    print(' Length of header = ', len(hdr2), '\n')

    for i in range (len(hdr2)):
        print (' %2i' % i, ' %50s: ' % hdr2.comments[i], hdr2[i])

    print(' \n\n\n')


    data = hdul[2].data
    print(data.shape)
    print(data.dtype.name, ' \n')
    array0 = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38]
    for i in range (16):
        print('   * %20s' % hdr2[array0[i]], '   ', data.field(i))

    print(' \n\n\n')

    hdul.close()




    #return df_filename, df_filesize, df_system_name, df_obs_place, df_description, F_ADC, df_creation_timeUTC, ReceiverMode, ADRmode, sumDifMode, NAvr, TimeRes, frequency[0], frequency[FreqPointsNum-1], df, frequency, FFT_Size, SLine, Width, BlockSize


################################################################################

if __name__ == '__main__':

    filename = 'DATA/20190329_102000_BST.fits'

    print('\n\n * Parameters of the file: ')

    FileHeaderReaderFITS(filename)
