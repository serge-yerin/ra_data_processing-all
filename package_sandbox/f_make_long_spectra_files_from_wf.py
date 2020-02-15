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
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.JDS_waveform_time import JDS_waveform_time



def make_long_spectra_files_from_wf(directory, fileList, result_folder):
    '''
    Makes fft and saves spectra to the long data files
    '''

    # Preparing long data files
    fname = directory + fileList[0]
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
     CLCfrq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
     df, frequency, FreqPointsNum, data_block_size] = FileHeaderReaderJDS(fname, 0, 1)

    no_of_blocks_in_file = (df_filesize - 1024) / data_block_size
    print(' Number of blocks in file:             ', no_of_blocks_in_file)

    no_of_blocks_in_batch = int(no_of_blocks_in_file / (2 * no_of_batches_in_file))
    print(' Number of blocks in batch:            ', no_of_blocks_in_batch)

    with open(fname, 'rb') as file:
        # *** Data file header read ***
        file_header = file.read(1024)

    # *** Creating a name for long timeline TXT file ***
    TLfile_name = result_folder + '/' + df_filename + '_Timeline.txt'
    TLfile = open(TLfile_name, 'w')  # Open and close to delete the file with the same name
    TLfile.close()

    # *** Creating a binary file with data for long data storage ***
    file_data_re_name = result_folder + '/' + df_filename + '_Data_WRe.dat'
    file_data_re = open(file_data_re_name, 'wb')
    file_data_re.write(file_header)
    file_data_re.close()

    file_data_im_name = result_folder + '/' + df_filename + '_Data_WIm.dat'
    file_data_im = open(file_data_im_name, 'wb')
    file_data_im.write(file_header)
    file_data_im.close()

    for fileNo in range(len(fileList)):  # loop by files
        #print('\n\n\n  *  File ', str(fileNo + 1), ' of', str(len(fileList)))
        #print('  *  File path: ', str(fileList[fileNo]))

        # *** Opening datafile ***
        fname = directory + fileList[fileNo]

        # *********************************************************************************

        # *** Data file header read ***
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
         CLCfrq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
         df, frequency, FreqPointsNum, data_block_size] = FileHeaderReaderJDS(fname, 0, 0)

        # *******************************************************************************
        #                          R E A D I N G   D A T A                             *
        # *******************************************************************************

        #print('\n  *** Reading data from file *** \n')

        with open(fname, 'rb') as file:
            file.seek(1024)  # Jumping to 1024 byte from file beginning #+ (sizeOfChunk+8) * chunkSkip
            TimeScaleFull = []

            bar = IncrementalBar(' File ' + str(fileNo + 1) + ' of ' + str(len(fileList)) + ' progress: ',
                                 max=no_of_batches_in_file, suffix='%(percent)d%%')

            for batch in range(no_of_batches_in_file):  #

                bar.next()

                # Reading and reshaping all data with readers
                if Channel == 0 or Channel == 1:  # Single channel mode

                    wf_data = np.fromfile(file, dtype='i2', count=no_of_blocks_in_batch * data_block_size)
                    wf_data = np.reshape(wf_data, [data_block_size, no_of_blocks_in_batch], order='F')

                # Timing
                timeline_block_str = JDS_waveform_time(wf_data, CLCfrq, data_block_size)
                #TimeScaleFig.append(timeline_block_str[-1][0:12])
                for j in range (no_of_blocks_in_batch):
                    TimeScaleFull.append(df_creation_timeUTC[0:10] + ' ' + timeline_block_str[j][0:12])

                # Nulling the time blocks in waveform data
                wf_data[data_block_size - 4: data_block_size, :] = 0

                # Scaling of the data - seems to be wrong in absolute value
                wf_data = wf_data / 32768.0

                spectra_chA = np.zeros([data_block_size, no_of_blocks_in_batch], dtype=complex)
                for i in range(no_of_blocks_in_batch):
                    spectra_chA[:, i] = np.fft.fft(wf_data[:, i])

                # Storing only second (right) mirror part of spectra
                spectra_chA = spectra_chA[0: int(data_block_size / 2), :]

                if batch == 0:
                    plt.figure(1, figsize=(10.0, 6.0))
                    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
                    plt.plot(np.log10(np.power(np.abs(spectra_chA[:, 0]), 2)), label='First specter')
                    plt.title('Title', fontsize=10, fontweight='bold', style='italic', y=1.025)
                    plt.legend(loc='upper right', fontsize=10)
                    plt.ylabel('Amplitude, a.u.', fontsize=10, fontweight='bold')
                    plt.xlabel('Frequency, counts', fontsize=10, fontweight='bold')
                    plt.yticks(fontsize=8, fontweight='bold')
                    plt.xticks(fontsize=8, fontweight='bold')
                    pylab.savefig(result_folder + '/Fig. 1.png', bbox_inches='tight', dpi=customDPI)
                    plt.close('all')

                temp = np.real(spectra_chA).copy(order='C')

                file_data_re = open(file_data_re_name, 'ab')
                file_data_re.write(temp)
                file_data_re.close()

                temp = np.imag(spectra_chA).copy(order='C')

                file_data_im = open(file_data_im_name, 'ab')
                file_data_im.write(temp)
                file_data_im.close()

                # Saving time data to ling timeline file
                with open(TLfile_name, 'a') as TLfile:
                    for i in range(no_of_blocks_in_batch):
                        TLfile.write((TimeScaleFull[i][:]) + ' \n')

    return file_data_re_name, file_data_im_name, TLfile_name
