#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
# Common functions
import matplotlib.pyplot as plt
import sys
import numpy as np
import pylab
from os import path
from progress.bar import IncrementalBar

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read




def check_long_spectra_files_from_wf(directory, file_re, file_im):
    '''
    Checks spectra from the long data files
    '''

    # Preparing long data files
    fname = directory + fileList[0]
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
     CLCfrq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
     df, frequency, FreqPointsNum, data_block_size] = file_header_jds_read(fname, 0, 1)

    no_of_blocks_in_file = (df_filesize - 1024) / data_block_size
    print(' Number of blocks in file:             ', no_of_blocks_in_file)

    no_of_blocks_in_batch = int(no_of_blocks_in_file / (2 * no_of_batches_in_file))
    print(' Number of blocks in batch:            ', no_of_blocks_in_batch)






    # *** Calculation of the dimensions of arrays to read ***

    nx = len(frequency)                  # the first dimension of the array

    ny = int(((df_filesize-1024)/(nx*8))) # the second dimension of the array: file size - 1024 bytes
    istart = 0
    istop = len(timeline)


    print (' Number of frequency channels:     ', nx, '\n')
    print (' Number of spectra:                ', ny, '\n')
    print (' Recomended spectra number for averaging is:  ', int(ny/1024))

    averageConst = int(ny/1024)
    if int(averageConst) < 1: averageConst = 1

    # *** Data reading and averaging ***

    print ('\n\n\n  *** Data reading and averaging *** \n\n')

    file1 = open(file_re, 'rb')
    file2 = open(file_im, 'rb')

    file1.seek(1024+istart*8*nx, os.SEEK_SET)   # Jumping to 1024+number of spectra to skip byte from file beginning
    file2.seek(1024+istart*8*nx, os.SEEK_SET)   # Jumping to 1024+number of spectra to skip byte from file beginning

    array = np.empty((nx, 0), float)
    numOfBlocks = int(ny/averageConst)
    for block in range (numOfBlocks):

        data1 = np.fromfile(file1, dtype=np.float64, count = nx * averageConst)
        data2 = np.fromfile(file2, dtype=np.float64, count = nx * averageConst)

        data = np.power(np.abs(data1[:,:] + 1j * data2[:,:]),2)

        del data1, data2

        data = np.reshape(data, [nx, averageConst], order='F')

        dataApp = np.empty((nx, 1), float)

        with np.errstate(invalid='ignore'):
            dataApp[:,0] = 10*np.log10(data.mean(axis=1)[:])

        array = np.append(array, dataApp, axis=1)
        array[np.isnan(array)] = -120


        del dataApp, data

    file1.close()
    if (typesOfData[j] == 'A+B' or typesOfData[j] == 'A-B'): file2.close()









    return

################################################################################

if __name__ == '__main__':

    directory = 'DATA/'
    file_re = 'E220213_201455.jds_Data_WRe.dat'
    file_im = 'E220213_201455.jds_Data_WIm.dat'
    check_long_spectra_files_from_wf(directory, file_re, file_im)