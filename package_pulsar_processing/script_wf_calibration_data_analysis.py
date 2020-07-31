# Python3
# pip install progress
Software_version = '2020.07.23'
Software_name = 'JDS Waveform calibarion data analysis'

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************

source_directory = 'DATA/'              # Directory with JDS files to be analyzed
result_directory = ''                   # Directory where DAT files to be stored (empty string means project directory)

no_of_points_for_fft = 16384            # Number of points for FFT on result spectra # 8192, 16384, 32768, 65536, 131072
#no_of_spectra_in_bunch = 16384          # Number of spectra samples to read while conversion to dat (depends on RAM)
#no_of_bunches_per_file = 16             # Number of bunches to read one WF file (depends on RAM)


# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import os
import sys
import time
import pylab
import numpy as np
from os import path
from progress.bar import IncrementalBar
import matplotlib.pyplot as plt

# To change system path to main source_directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_common_modules.find_and_check_files_in_current_folder import find_and_check_files_in_current_folder
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR
from package_ra_data_files_formats.JDS_waveform_time import JDS_waveform_time
from package_pulsar_processing.pulsar_DM_full_shift_calculation import DM_full_shift_calc
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import pulsar_period_DM_compensated_pics
from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import cut_needed_pulsar_period_from_dat
# ###############################################################################

# *******************************************************************************
#      W A V E F O R M   J D S   T O   W A V E F O R M    F L O A T 3 2         *
# *******************************************************************************


def convert_jds_wf_to_wf32(source_directory, result_directory, no_of_bunches_per_file):
    '''
    function converts jds waveform data to wf32 waveform data for further processing (coherent dedispersion) and
    saves txt files with time data
    Input parameters:
        source_directory - directory where initial jds waveform data are stored
        result_directory - directory where new wf32 files will be stored
        no_of_bunches_per_file - number of data bunches per file to peocess (depends on RAM volume on the PC)
    Output parameters:
        result_wf32_files - list of results files
    '''

    fileList = find_and_check_files_in_current_folder(source_directory, '.jds')

    # To print in console the header of first file
    print('\n  First file header parameters: \n')

    # *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
     clock_freq, df_creation_timeUTC, channel, receiver_mode, Mode, Navr, time_res, fmin, fmax,
     df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(source_directory + fileList[0], 0, 1)
    if Mode > 0:
        sys.exit('  ERROR!!! Data recorded in wrong mode! Waveform mode needed.\n\n    Program stopped!')

    result_wf32_files = []
    # Main loop by files start
    for file_no in range(len(fileList)):  # loop by files

        fname = source_directory + fileList[file_no]

        # Create long data files and copy first data file header to them
        if file_no == 0:

            with open(fname, 'rb') as file:
                # *** Data file header read ***
                file_header = file.read(1024)

            # *** Creating a name for long timeline TXT file ***
            tl_file_name = df_filename + '_Timeline.wtxt'
            tl_file = open(tl_file_name, 'w')  # Open and close to delete the file with the same name
            tl_file.close()

            # *** Creating a binary file with data for long data storage ***
            file_data_A_name = df_filename + '_Data_chA.wf32'
            result_wf32_files.append(file_data_A_name)
            file_data_A = open(file_data_A_name, 'wb')
            file_data_A.write(file_header)
            file_data_A.close()

            if channel == 2:
                file_data_B_name = df_filename + '_Data_chB.wf32'
                result_wf32_files.append(file_data_B_name)
                file_data_B = open(file_data_B_name, 'wb')
                file_data_B.write(file_header)
                file_data_B.close()

            del file_header

        # Calculation of number of blocks and number of spectra in the file
        if channel == 0 or channel == 1:  # Single channel mode
            no_of_spectra_in_bunch = int((df_filesize - 1024) / (no_of_bunches_per_file * 2 * data_block_size))
        else:  # Two channels mode
            no_of_spectra_in_bunch = int((df_filesize - 1024) / (no_of_bunches_per_file * 4 * data_block_size))

        no_of_blocks_in_file = (df_filesize - 1024) / data_block_size

        if file_no == 0:
            print(' Number of blocks in file:               ', no_of_blocks_in_file)
            print(' Number of bunches to read in file:      ', no_of_bunches_per_file)
            print('\n  *** Reading data from file *** \n')

        # *******************************************************************************
        #                           R E A D I N G   D A T A                             *
        # *******************************************************************************

        with open(fname, 'rb') as file:
            file.seek(1024)  # Jumping to 1024 byte from file beginning

            # !!! Fake timing. Real timing to be done!!!
            TimeFigureScaleFig = np.linspace(0, no_of_bunches_per_file, no_of_bunches_per_file + 1)
            for i in range(no_of_bunches_per_file):
                TimeFigureScaleFig[i] = str(TimeFigureScaleFig[i])

            time_scale_bunch = []

            bar = IncrementalBar(' File ' + str(file_no + 1) + ' of ' + str(len(fileList)) + ' reading: ',
                                 max=no_of_bunches_per_file, suffix='%(percent)d%%')

            for bunch in range(no_of_bunches_per_file):

                bar.next()

                # Reading and reshaping all data with time data
                if channel == 0 or channel == 1:  # Single channel mode
                    wf_data = np.fromfile(file, dtype='i2', count=no_of_spectra_in_bunch * data_block_size)
                    wf_data = np.reshape(wf_data, [data_block_size, no_of_spectra_in_bunch], order='F')
                if channel == 2:  # Two channels mode
                    wf_data = np.fromfile(file, dtype='i2', count=2 * no_of_spectra_in_bunch * data_block_size)
                    wf_data = np.reshape(wf_data, [data_block_size, 2 * no_of_spectra_in_bunch], order='F')

                # Timing
                timeline_block_str = JDS_waveform_time(wf_data, clock_freq, data_block_size)
                if channel == 2:  # Two channels mode
                    timeline_block_str = timeline_block_str[
                                         0:int(len(timeline_block_str) / 2)]  # Cut the timeline of second channel
                for i in range(len(timeline_block_str)):
                    time_scale_bunch.append(df_creation_timeUTC[0:10] + ' ' + timeline_block_str[i])  # [0:12]

                # Deleting the time blocks from waveform data
                real_data_block_size = data_block_size - 4
                wf_data = wf_data[0: real_data_block_size, :]

                # Separation data into channels
                if channel == 0 or channel == 1:  # Single channel mode
                    wf_data_chA = np.reshape(wf_data, [real_data_block_size * no_of_spectra_in_bunch, 1], order='F')
                    del wf_data  # Deleting unnecessary array name just in case

                if channel == 2:  # Two channels mode

                    # Separating the data into two channels
                    wf_data = np.reshape(wf_data, [2 * real_data_block_size * no_of_spectra_in_bunch, 1], order='F')
                    wf_data_chA = wf_data[0: (2 * real_data_block_size * no_of_spectra_in_bunch): 2]  # A
                    wf_data_chB = wf_data[1: (2 * real_data_block_size * no_of_spectra_in_bunch): 2]  # B
                    del wf_data

                # Saving WF data to dat file
                file_data_A = open(file_data_A_name, 'ab')
                file_data_A.write(np.float32(wf_data_chA).transpose().copy(order='C'))
                file_data_A.close()
                if channel == 2:
                    file_data_B = open(file_data_B_name, 'ab')
                    file_data_B.write(np.float32(wf_data_chB).transpose().copy(order='C'))
                    file_data_B.close()

                # Saving time data to ling timeline file
                with open(tl_file_name, 'a') as tl_file:
                    for i in range(no_of_spectra_in_bunch):
                        tl_file.write((str(time_scale_bunch[i][:])) + ' \n')  # str

            bar.finish()

        file.close()  # Close the data file
        del file_data_A
        if channel == 2:
            del file_data_B

    return result_wf32_files


def correlate_two_wf32_signals(file_name_1, file_name_2, no_of_points_for_fft):
    '''
        function reads two wf32 waveform data files and make correlation of the data to calibrate observations
        Input parameters:
            file_name_1 - first input wf32 file
            file_name_2 - second input wf32 file
            no_of_points_for_fft - number of data points to calculate correlation
        Output parameters:
            xxx - xxx
        '''

    df_filesize_1 = os.stat(file_name_1).st_size                         # Size of file
    df_filesize_2 = os.stat(file_name_2).st_size                         # Size of file
    if df_filesize_1 != df_filesize_2:
        print('  Size of file 1:    ', df_filesize_1, '\n  Size of file 2:', df_filesize_2)
        sys.exit('   ERROR!!! Files have different sizes!')

    # Calculation of the dimensions of arrays to read
    ny = int((df_filesize_1 - 1024) / 4)   # number of samples to read: file size - 1024 bytes
    num_of_blocks = int(ny // (no_of_points_for_fft * 10000))

    file_1 = open(file_name_1, 'rb')
    file_2 = open(file_name_2, 'rb')
    file_1.seek(1024)
    file_2.seek(1024)

    #for block in range(num_of_blocks):
    for block in range(1):

        scale = 10000  #  10000
        #if block == (num_of_blocks - 1):
        #    samples_num_in_bunch = ny - (num_of_blocks - 1) * no_of_points_for_fft * scale
        #else:
        #    samples_num_in_bunch = no_of_points_for_fft * scale
        samples_num_in_bunch = no_of_points_for_fft * scale

        data_1 = np.fromfile(file_1, dtype=np.float32, count=samples_num_in_bunch)
        data_2 = np.fromfile(file_2, dtype=np.float32, count=samples_num_in_bunch)

        data_1 = np.reshape(data_1, [no_of_points_for_fft, scale], order='F')
        data_2 = np.reshape(data_2, [no_of_points_for_fft, scale], order='F')

        # preparing matrices for spectra
        spectrum_1 = np.zeros((no_of_points_for_fft, scale), dtype='complex')
        spectrum_2 = np.zeros((no_of_points_for_fft, scale), dtype='complex')

        # Calculation of spectra
        for i in range(scale):
            spectrum_1[:, i] = np.fft.fft(data_1[:, i])
            spectrum_2[:, i] = np.fft.fft(data_2[:, i])

        #spectrum_1 = np.fft.fft(data_1)
        #spectrum_2 = np.fft.fft(data_2)

        del data_1, data_2

        cross_spectrum = spectrum_1[:, :] * np.conj(spectrum_2[:, :])

        del spectrum_1, spectrum_2

        cross_spectrum_av = np.mean(cross_spectrum, axis=1)
        cross_spectrum_av[0] = 0

        #'''
        fig = plt.figure(figsize=(18, 10))
        ax1 = fig.add_subplot(211)
        ax1.plot(np.abs(cross_spectrum_av), linestyle='-', linewidth='1.00', label='Cross spectrum module')
        ax1.legend(loc='upper right', fontsize=10)
        ax2 = fig.add_subplot(212)
        ax2.plot(np.angle(cross_spectrum_av), linestyle='-', linewidth='1.00', label='Cross spectrum angle')
        ax2.legend(loc='upper right', fontsize=10)
        pylab.savefig('00_Cross_spectrum.png', bbox_inches='tight', dpi=160)
        plt.close('all')
        #'''

        corr_function = np.fft.ifft(cross_spectrum)
        corr_function_av = np.mean(corr_function, axis=1)
        corr_function_av[0] = 0

        #'''
        fig = plt.figure(figsize=(18, 10))
        ax1 = fig.add_subplot(211)
        ax1.plot(np.real(corr_function_av), linestyle='-', linewidth='1.00', label='Corr func Re')
        ax1.legend(loc='upper right', fontsize=10)
        ax2 = fig.add_subplot(212)
        ax2.plot(np.imag(corr_function_av), linestyle='-', linewidth='1.00', label='Corr func Im')
        ax2.legend(loc='upper right', fontsize=10)
        pylab.savefig('01_correlation.png', bbox_inches='tight', dpi=160)
        plt.close('all')
        #'''

    return


################################################################################
# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    print('\n\n\n\n\n\n\n\n   ********************************************************************')
    print('   * ', Software_name, ' v.', Software_version, ' *      (c) YeS 2020')
    print('   ******************************************************************** \n\n\n')
    
    startTime = time.time()
    previousTime = startTime
    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")
    print('  Today is ', currentDate, ' time is ', currentTime, '\n')

    '''
    print('\n\n  * Converting waveform from JDS to WF32 format... \n\n')

    initial_wf32_files = convert_jds_wf_to_wf32(source_directory, result_directory, no_of_points_for_fft)
    print('\n List of WF32 files: ', initial_wf32_files, '\n')
    '''
    initial_wf32_files = ['E300120_233404.jds_Data_chA.wf32', 'E300120_233404.jds_Data_chB.wf32']
    correlate_two_wf32_signals(initial_wf32_files[0], initial_wf32_files[1], no_of_points_for_fft)

    endTime = time.time()
    print('\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                    round((endTime - startTime)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
