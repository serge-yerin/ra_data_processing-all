# Python3
#
#   !!!! NOT FINISHED !!!
#
Software_version = '2020.01.04'
Software_name = 'Coherent dispersion compensation'
# Program intended to read, show and analyze data from DSPZ receivers in waveform mode

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Directory of files to be analyzed:
directory = 'DATA/' # 'DATA/'

pulsar_name = 'B0950+08'
no_of_spectra_to_average = 128
VminNorm = 0                    # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 5                    # Upper limit of figure dynamic range for normalized spectra
colormap = 'Greys'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
customDPI = 300                 # Resolution of images of dynamic spectra


################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
# Common functions
import matplotlib.pyplot as plt
import os
import numpy as np
import time
import pylab

# My functions
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.JDS_waveform_time import JDS_waveform_time



def make_long_spectra_files_from_wf(directory, fileList, result_folder):
    '''
    Makes fft and saves spectra to the long data files
    '''
    # Preparing long data files
    # Writing first WF data file header to the header of long data file
    fname = directory + fileList[0]
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
     CLCfrq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
     df, frequency, FreqPointsNum, data_block_size] = FileHeaderReaderJDS(fname, 0, 1)

    no_of_av_spectra_per_file = int((df_filesize - 1024) / (2 * data_block_size * no_of_spectra_to_average))

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

    for fileNo in range(1):  # len(fileList) loop by files
        print('\n\n\n  *  File ', str(fileNo + 1), ' of', str(len(fileList)))
        print('  *  File path: ', str(fileList[fileNo]))

        # *** Opening datafile ***
        fname = directory + fileList[fileNo]

        # *********************************************************************************

        # *** Data file header read ***
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
         CLCfrq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
         df, frequency, FreqPointsNum, data_block_size] = FileHeaderReaderJDS(fname, 0, 1)

        # *******************************************************************************
        #                          R E A D I N G   D A T A                             *
        # *******************************************************************************

        print('\n  *** Reading data from file *** \n')

        with open(fname, 'rb') as file:
            file.seek(1024)  # Jumping to 1024 byte from file beginning #+ (sizeOfChunk+8) * chunkSkip

            for av_sp in range(no_of_av_spectra_per_file):  # no_of_av_spectra_per_file

                # Reading and reshaping all data with readers
                if Channel == 0 or Channel == 1:  # Single channel mode

                    wf_data = np.fromfile(file, dtype='i2', count=no_of_spectra_to_average * data_block_size)
                    wf_data = np.reshape(wf_data, [data_block_size, no_of_spectra_to_average], order='F')

                # Timing aquirement
                # timeline_block_str = JDS_waveform_time(wf_data, CLCfrq, data_block_size)
                # TimeScaleFig.append(timeline_block_str[-1][0:12])

                # Nulling the time blocks in waveform data
                wf_data[data_block_size - 4: data_block_size, :] = 0

                # Scaling of the data - seems to be wrong in absolute value
                wf_data = wf_data / 32768.0

                spectra_chA = np.zeros([data_block_size, no_of_spectra_to_average], dtype=complex)
                for i in range(no_of_spectra_to_average):
                    spectra_chA[:, i] = np.fft.fft(wf_data[:, i])

                # Storing only second (right) mirror part of spectra
                spectra_chA = spectra_chA[0: int(data_block_size / 2), :]

                if av_sp == 0:
                    plt.figure(1, figsize=(10.0, 6.0))
                    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
                    plt.plot(np.log10(np.power(np.abs(spectra_chA[:, 0]), 2)), label='Label')
                    plt.title('Title', fontsize=10, fontweight='bold', style='italic', y=1.025)
                    plt.legend(loc='upper right', fontsize=10)
                    plt.ylabel('label', fontsize=10, fontweight='bold')
                    plt.xlabel('label', fontsize=10, fontweight='bold')
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

    return file_data_re_name, file_data_im_name, TLfile_name





################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************

print ('\n\n\n\n\n\n\n\n   **************************************************************')
print ('   *    ', Software_name,' v.',Software_version,'     *      (c) YeS 2020')
print ('   ************************************************************** \n\n\n')

startTime = time.time()
previousTime = startTime
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, ' \n')


# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
result_folder = directory + 'TEMP_WF'
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

# *** Search JDS files in the directory ***
fileList = find_files_only_in_current_folder(directory, '.jds', 1)


# Make long data files

# file_data_re_name, file_data_im_name, TLfile_name = make_long_spectra_files_from_wf(directory, fileList, result_folder)


file_data_re_name = 'DATA/TEMP_WF/E220213_201455.jds_Data_WRe.dat'
file_data_im_name = 'DATA/TEMP_WF/E220213_201455.jds_Data_WIm.dat'
TLfile_name = 'DATA/TEMP_WF/E220213_201455.jds_Timeline.txt'

# Compensate DM for both long data files

pulsar_ra, pulsar_dec, DM = catalogue_pulsar(pulsar_name)
print ('\n\n Dispersion measure from catalogue =  ', DM, ' pc / cm3 \n')











endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program JDS_WF_reader has finished! *** \n\n\n')
