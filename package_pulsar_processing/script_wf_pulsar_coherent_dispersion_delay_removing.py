# Python3
# pip install progress
Software_version = '2020.07.18'
Software_name = 'JDS Waveform coherent dispersion delay removing'
# Script intended to convert data from DSPZ receivers in waveform mode to waveform float 32 files
# and make coherent dispersion delay removing and saving found pulses
# !!! Time possibly is not correct !!!
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
pulsar_name = 'B0809+74'  # 'B0950+08'

make_sum = 1
dm_step = 1.0
no_of_points_for_fft_spectr = 16384     # Number of points for FFT on result spectra # 8192, 16384, 32768, 65536, 131072
no_of_points_for_fft_dedisp = 16384     # Number of points for FFT on dedispersion # 8192, 16384, 32768, 65536, 131072
no_of_spectra_in_bunch = 16384          # Number of spectra samples to read while conversion to dat (depends on RAM)
no_of_bunches_per_file = 16             # Number of bunches to read one WF file (depends on RAM)
source_directory = 'DATA/'              # Directory with JDS files to be analyzed
result_directory = ''                   # Directory where DAT files to be stored (empty string means project directory)
calibrate_phase = False                 # Do we need to calibrate phases between two channels? (True/False)
median_filter_window = 80               # Window of median filter to smooth the average profile

phase_calibr_txt_file = 'Calibration_E300120_232956.jds_cross_spectra_phase.txt'

# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import os
import sys
import time
import math
import pylab
import numpy as np
from os import path
from time import gmtime, strftime
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
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_ra_data_processing.filtering import median_filter
from package_pulsar_processing.pulsar_DM_full_shift_calculation import DM_full_shift_calc
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes
from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import pulsar_period_DM_compensated_pics
from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import cut_needed_pulsar_period_from_dat
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_ra_data_files_formats.f_convert_jds_wf_to_wf32 import convert_jds_wf_to_wf32
from package_ra_data_files_formats.f_convert_wf32_to_dat import convert_wf32_to_dat_without_overlap
# from package_ra_data_files_formats.f_convert_wf32_to_dat import convert_wf32_to_dat_with_overlap

# ###############################################################################

# *******************************************************************************
#      W A V E F O R M   J D S   T O   W A V E F O R M    F L O A T 3 2         *
# *******************************************************************************

#
# def convert_jds_wf_to_wf32(source_directory, result_directory, no_of_bunches_per_file):
#     """
#     function converts jds waveform data to wf32 waveform data for further processing (coherent dedispersion) and
#     saves txt files with time data
#     Input parameters:
#         source_directory - directory where initial jds waveform data are stored
#         result_directory - directory where new wf32 files will be stored
#         no_of_bunches_per_file - number of data bunches per file to process (depends on RAM volume on the PC)
#     Output parameters:
#         result_wf32_files - list of results files
#     """
#
#     fileList = find_and_check_files_in_current_folder(source_directory, '.jds')
#
#     # To print in console the header of first file
#     print('\n  First file header parameters: \n')
#
#     # *** Data file header read ***
#     [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
#         clock_freq, df_creation_timeUTC, channel, receiver_mode, Mode, Navr, time_res, fmin, fmax,
#         df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(source_directory + fileList[0], 0, 1)
#     if Mode > 0:
#         sys.exit('  ERROR!!! Data recorded in wrong mode! Waveform mode needed.\n\n    Program stopped!')
#
#     result_wf32_files = []
#     # Main loop by files start
#     for file_no in range(len(fileList)):   # loop by files
#
#         fname = source_directory + fileList[file_no]
#
#         # Create long data files and copy first data file header to them
#         if file_no == 0:
#
#             with open(fname, 'rb') as file:
#                 # *** Data file header read ***
#                 file_header = file.read(1024)
#
#             # *** Creating a name for long timeline TXT file ***
#             tl_file_name = df_filename + '_Timeline.wtxt'
#             tl_file = open(tl_file_name, 'w')  # Open and close to delete the file with the same name
#             tl_file.close()
#
#             # *** Creating a binary file with data for long data storage ***
#             file_data_A_name = df_filename + '_Data_chA.wf32'
#             result_wf32_files.append(file_data_A_name)
#             file_data_A = open(file_data_A_name, 'wb')
#             file_data_A.write(file_header)
#             file_data_A.close()
#
#             if channel == 2:
#                 file_data_B_name = df_filename + '_Data_chB.wf32'
#                 result_wf32_files.append(file_data_B_name)
#                 file_data_B = open(file_data_B_name, 'wb')
#                 file_data_B.write(file_header)
#                 file_data_B.close()
#
#             del file_header
#
#         # Calculation of number of blocks and number of spectra in the file
#         if channel == 0 or channel == 1:    # Single channel mode
#             no_of_spectra_in_bunch = int((df_filesize - 1024) / (no_of_bunches_per_file * 2 * data_block_size))
#         else:                               # Two channels mode
#             no_of_spectra_in_bunch = int((df_filesize - 1024) / (no_of_bunches_per_file * 4 * data_block_size))
#
#         no_of_blocks_in_file = (df_filesize - 1024) / data_block_size
#
#         if file_no == 0:
#             print(' Number of blocks in file:               ', no_of_blocks_in_file)
#             print(' Number of bunches to read in file:      ', no_of_bunches_per_file)
#             print('\n  *** Reading data from file *** \n')
#
#         # *******************************************************************************
#         #                           R E A D I N G   D A T A                             *
#         # *******************************************************************************
#
#         with open(fname, 'rb') as file:
#             file.seek(1024)  # Jumping to 1024 byte from file beginning
#
#             # !!! Fake timing. Real timing to be done!!!
#             TimeFigureScaleFig = np.linspace(0, no_of_bunches_per_file, no_of_bunches_per_file+1)
#             for i in range(no_of_bunches_per_file):
#                 TimeFigureScaleFig[i] = str(TimeFigureScaleFig[i])
#
#             time_scale_bunch = []
#
#             bar = IncrementalBar(' File ' + str(file_no+1) + ' of ' + str(len(fileList)) + ' reading: ',
#                                  max=no_of_bunches_per_file, suffix='%(percent)d%%')
#
#             for bunch in range(no_of_bunches_per_file):
#
#                 bar.next()
#
#                 # Reading and reshaping all data with time data
#                 if channel == 0 or channel == 1:    # Single channel mode
#                     wf_data = np.fromfile(file, dtype='i2', count = no_of_spectra_in_bunch * data_block_size)
#                     wf_data = np.reshape(wf_data, [data_block_size, no_of_spectra_in_bunch], order='F')
#                 if channel == 2:                    # Two channels mode
#                     wf_data = np.fromfile(file, dtype='i2', count = 2 * no_of_spectra_in_bunch * data_block_size)
#                     wf_data = np.reshape(wf_data, [data_block_size, 2 * no_of_spectra_in_bunch], order='F')
#
#                 # Timing
#                 timeline_block_str = JDS_waveform_time(wf_data, clock_freq, data_block_size)
#                 if channel == 2:                    # Two channels mode
#                     timeline_block_str = timeline_block_str[0:int(len(timeline_block_str)/2)]  # Cut the timeline of second channel
#                 for i in range (len(timeline_block_str)):
#                     time_scale_bunch.append(df_creation_timeUTC[0:10] + ' ' +timeline_block_str[i])  # [0:12]
#
#                 # Deleting the time blocks from waveform data
#                 real_data_block_size = data_block_size - 4
#                 wf_data = wf_data[0 : real_data_block_size, :]
#
#                 # Separation data into channels
#                 if channel == 0 or channel == 1:    # Single channel mode
#                     wf_data_chA = np.reshape(wf_data, [real_data_block_size * no_of_spectra_in_bunch, 1], order='F')
#                     del wf_data                     # Deleting unnecessary array name just in case
#
#                 if channel == 2:  # Two channels mode
#
#                     # Separating the data into two channels
#                     wf_data = np.reshape(wf_data, [2 * real_data_block_size * no_of_spectra_in_bunch, 1], order='F')
#                     wf_data_chA = wf_data[0 : (2 * real_data_block_size * no_of_spectra_in_bunch) : 2]  # A
#                     wf_data_chB = wf_data[1 : (2 * real_data_block_size * no_of_spectra_in_bunch) : 2]  # B
#                     del wf_data
#
#                 # Saving WF data to dat file
#                 file_data_A = open(file_data_A_name, 'ab')
#                 file_data_A.write(np.float32(wf_data_chA).transpose().copy(order='C'))
#                 file_data_A.close()
#                 if channel == 2:
#                     file_data_B = open(file_data_B_name, 'ab')
#                     file_data_B.write(np.float32(wf_data_chB).transpose().copy(order='C'))
#                     file_data_B.close()
#
#                 # Saving time data to ling timeline file
#                 with open(tl_file_name, 'a') as tl_file:
#                     for i in range(no_of_spectra_in_bunch):
#                         tl_file.write((str(time_scale_bunch[i][:])) + ' \n')  # str
#
#             bar.finish()
#
#         file.close()  # Close the data file
#         del file_data_A
#         if channel == 2:
#             del file_data_B
#
#     return result_wf32_files


# *******************************************************************************
#             W A V E F O R M    P H A S E   C A L I B R A T I O N              *
# *******************************************************************************


def wf32_two_channel_phase_calibration(fname, no_of_points_for_fft_dedisp, no_of_spectra_in_bunch, phase_calibr_txt_file):
    """
    function reads waveform data in wf32 format, makes FFT, cuts the symmetrical half of the spectra and
    multiplies complex data by phase calibration data read from txt file. Then a symmetrcal part of spectra
    are made and joined to the shifted one, inverse FFT as applied and data are stored in waveform wf32 format
    Input parameters:
        fname -                         name of file with initial wf32 data
        no_of_points_for_fft_dedisp -   number of waveform data points to use for FFT
        phase_calibr_txt_file -         txt file with phase calibration data
    Output parameters:
        file_data_name -                name of file with calibrated data
    """

    # Rename the data file to make the new data file of the same name as initial one
    non_calibrated_fname = fname[:-5] + '_without_phase_calibration' + '.wf32'
    calibrated_fname = fname
    print('\n  Phase calibration of one channel \n')
    print('  Old filename of initial file:  ', calibrated_fname)
    print('  New filename of initial file:  ', non_calibrated_fname)

    os.rename(calibrated_fname, non_calibrated_fname)

    #  *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
     clock_freq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, time_resolution, fmin, fmax,
     df, frequency_list, freq_points_num, data_block_size] = FileHeaderReaderJDS(non_calibrated_fname, 0, 0)

    # Read phase calibration txt file
    phase_calibr_file = open(phase_calibr_txt_file, 'r')
    phase_vs_freq = []
    for line in phase_calibr_file:
        phase_vs_freq.append(np.float(line))
    phase_calibr_file.close()

    fig = plt.figure(figsize=(9, 5))
    ax1 = fig.add_subplot(111)
    ax1.plot(phase_vs_freq, linestyle='-', linewidth='1.00', label='Phase to add')
    ax1.legend(loc='upper right', fontsize=6)
    ax1.grid(b=True, which='both', color='silver', linestyle='-')
    ax1.set_ylabel('Phase, a.u.', fontsize=6, fontweight='bold')
    pylab.savefig('00_Phase to add.png', bbox_inches='tight', dpi=160)
    plt.close('all')

    # Converting phase to complex numbers
    cmplx_phase = np.zeros((len(phase_vs_freq)), dtype=np.complex)
    for i in range(len(phase_vs_freq)):
        cmplx_phase[i] = np.cos(phase_vs_freq[i]) + 1j * np.sin(phase_vs_freq[i])

    # Create long data files and copy first data file header to them
    non_calibr_file_data = open(non_calibrated_fname, 'rb')
    file_header = non_calibr_file_data.read(1024)

    # *** Creating a binary file with data for long data storage ***
    calibr_file_data = open(calibrated_fname, 'wb')
    calibr_file_data.write(file_header)
    calibr_file_data.close()
    del file_header

    # Calculation of number of blocks and number of spectra in the file
    no_of_spectra_per_file = int((df_filesize - 1024) / (no_of_points_for_fft_dedisp * 4))
    no_of_bunches_per_file = math.ceil(no_of_spectra_per_file / no_of_spectra_in_bunch)
    print('  Number of spectra in bunch:    ', no_of_spectra_in_bunch)
    print('  Number of batches per file:    ', no_of_bunches_per_file, '')
    print('  Number of spectra per file:    ', no_of_spectra_per_file, '\n')

    non_calibr_file_data.seek(1024)  # Jumping to 1024 byte from file beginning

    bar = IncrementalBar(' Phase calibration of the file: ', max=no_of_bunches_per_file - 1,
                         suffix='%(percent)d%%')

    for bunch in range(no_of_bunches_per_file):

        if bunch < no_of_bunches_per_file-1:
            pass
        else:
            no_of_spectra_in_bunch = no_of_spectra_per_file - bunch * no_of_spectra_in_bunch
            # print(' Last bunch ', bunch, ', spectra in bunch: ', no_of_spectra_in_bunch)

        bar.next()

        # Reading and reshaping all data with time data
        wf_data = np.fromfile(non_calibr_file_data, dtype='f4',
                              count=no_of_spectra_in_bunch * no_of_points_for_fft_dedisp)

        wf_data = np.reshape(wf_data, [no_of_points_for_fft_dedisp, no_of_spectra_in_bunch], order='F')

        # preparing matrices for spectra
        spectra = np.zeros((no_of_points_for_fft_dedisp, no_of_spectra_in_bunch), dtype='complex64')

        # Calculation of spectra
        for i in range(no_of_spectra_in_bunch):
            spectra[:, i] = np.fft.fft(wf_data[:, i])
        del wf_data

        # Add phase to the data (multiply by complex number)
        for i in range (no_of_spectra_in_bunch):
            spectra[:, i] = spectra[:, i] * cmplx_phase[:]

        # Preparing array for new waveform
        wf_data = np.zeros((no_of_points_for_fft_dedisp, no_of_spectra_in_bunch))

        # Making IFFT
        for i in range(no_of_spectra_in_bunch):
            wf_data[:, i] = np.real(np.fft.ifft(spectra[:, i]))
        del spectra

        # Reshaping the waveform to single dimension (real)
        wf_data = np.reshape(wf_data, [no_of_points_for_fft_dedisp * no_of_spectra_in_bunch, 1], order='F')

        # Saving waveform data to wf32 file
        calibr_file_data = open(calibrated_fname, 'ab')
        calibr_file_data.write(np.float32(wf_data).transpose().copy(order='C'))
        calibr_file_data.close()

    bar.finish()

    return


# *******************************************************************************
#      C O H E R E N T   S U M   O F   W A V E F O R M    F L O A T 3 2         *
# *******************************************************************************


def sum_signal_of_wf32_files(file_name_1, file_name_2, no_of_spectra_in_bunch):
    """
    Function that takes two wf32 files and makes sum of signals from these files in output wf32 file
    """

    if 'chA' in file_name_1 and 'chB' in file_name_2:
        result_file_name = file_name_1.replace('chA', 'wfA+B')
    elif 'chB' in file_name_1 and 'chA' in file_name_2:
        result_file_name = file_name_1.replace('chB', 'wfA+B')
    else:
        result_file_name = file_name_1[:-4] + '_sum_' + file_name_2

    df_filesize_1 = os.stat(file_name_1).st_size                         # Size of file
    df_filesize_2 = os.stat(file_name_2).st_size                         # Size of file
    if df_filesize_1 != df_filesize_2:
        print('  Size of file 1:    ', df_filesize_1, '\n  Size of file 2:', df_filesize_2)
        sys.exit('   ERROR!!! Files have different sizes!')

    # Calculation of the dimensions of arrays to read
    ny = int((df_filesize_1 - 1024) / 4)   # number of samples to read: file size - 1024 bytes
    num_of_blocks = int(ny // (no_of_spectra_in_bunch * 10000))

    file_1 = open(file_name_1, 'rb')
    file_2 = open(file_name_2, 'rb')
    out_file = open(result_file_name, 'wb')

    file_header = file_1.read(1024)
    out_file.write(file_header)
    del file_header
    file_1.seek(1024)
    file_2.seek(1024)

    bar = IncrementalBar(' Making sum of two signals: ', max=num_of_blocks - 1,
                         suffix='%(percent)d%%')

    for block in range(num_of_blocks):

        bar.next()

        if block == (num_of_blocks - 1):
            samples_num_in_bunch = ny - (num_of_blocks - 1) * no_of_spectra_in_bunch * 10000
        else:
            samples_num_in_bunch = no_of_spectra_in_bunch * 10000

        data_1 = np.fromfile(file_1, dtype=np.float32, count=samples_num_in_bunch)
        data_2 = np.fromfile(file_2, dtype=np.float32, count=samples_num_in_bunch)
        data = data_1 + data_2
        out_file.write(np.float32(data).transpose().copy(order='C'))

    bar.finish()
    file_1.close()
    file_2.close()
    out_file.close()

    # Time line file copying

    # Making copy of timeline file with needed name and extension
    initial_timeline_name = file_name_1.split('_Data')[0] + '_Timeline.wtxt'
    result_timeline_name = result_file_name + '_Timeline.wtxt'

    # Creating a new timeline TXT file for results
    new_tl_file = open(result_timeline_name, 'w')  # Open and close to delete the file with the same name
    new_tl_file.close()

    # Reading timeline file
    old_tl_file = open(initial_timeline_name, 'r')
    new_tl_file = open(result_timeline_name, 'w')

    # Read time from timeline file
    time_scale_bunch = old_tl_file.readlines()

    # Saving time data to new file
    for i in range(len(time_scale_bunch)):
        new_tl_file.write((time_scale_bunch[i][:]) + '')

    old_tl_file.close()
    new_tl_file.close()

    return result_file_name


# *******************************************************************************
#        WAVEFORM FLOAT32 TO WAVEFORM FLOAT32 COHERENT DEDISPERSION             *
# *******************************************************************************


def coherent_wf_to_wf_dedispersion(DM, fname, no_of_points_for_fft_dedisp):
    """
    function reads waveform data in wf32 format, makes FFT, cuts the symmetrical half of the spectra and shifts the
    lines of complex data to provide coherent dedispersion. Then a symmetrcal part of spectra are made and joined
    to the shifted one, inverse FFT as applied and data are stored in waveform wf32 format
    Input parameters:
        DM -                            dispersion measure to compensate
        fname -                         name of file with initial wf32 data
        no_of_points_for_fft_dedisp -   number of waveform data points to use for FFT
    Output parameters:
        file_data_name -                name of file with processed data
    """

    #  *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        clock_freq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, time_resolution, fmin, fmax,
        df, frequency_list, freq_points_num, data_block_size] = FileHeaderReaderJDS(fname, 0, 0)

    # Manually set frequencies for one channel mode
    freq_points_num = int(no_of_points_for_fft_dedisp / 2)

    # Manually set frequencies for 33 MHz clock frequency
    if int(clock_freq / 1000000) == 33:
        fmin = 16.5
        fmax = 33.0
        df = 16500000 / freq_points_num

    # Create long data files and copy first data file header to them

    with open(fname, 'rb') as file:
        # *** Data file header read ***
        file_header = file.read(1024)

        # Removing old DM from file name and updating it to current value
        if fname.startswith('DM_'):
            prev_dm_str = fname.split('_')[1]
            prev_dm = np.float32(prev_dm_str)
            new_dm = prev_dm + DM
            # file_data_name = 'DM_' + str(np.round(new_dm, 6)) + '_' + fname.removeprefix('DM_' + prev_dm_str + '_')
            n = len('DM_' + prev_dm_str + '_')
            file_data_name = 'DM_' + str(np.round(new_dm, 6)) + '_' + fname[n:]
        else:
            file_data_name = 'DM_' + str(np.round(DM, 6)) + '_' + fname

        # *** Creating a binary file with data for long data storage ***
        file_data = open(file_data_name, 'wb')
        file_data.write(file_header)
        file_data.close()
        del file_header

        # *** Creating a new timeline TXT file for results ***
        new_tl_file_name = file_data_name.split("_Data_ch", 1)[0] + '_Timeline.wtxt'
        new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
        new_tl_file.close()

        # Calculation of the time shifts
        shift_vector = DM_full_shift_calc(freq_points_num, fmin, fmax, df / pow(10, 6), time_resolution, DM, 'jds')
        max_shift = np.abs(shift_vector[0])

        # Preparing buffer array
        buffer_array = np.zeros((freq_points_num, 2 * max_shift), dtype='complex64')

        print(' Maximal shift is:                            ', max_shift, ' pixels ')
        print(' Dispersion measure:                          ', DM, ' pc / cm3 ')

        # Calculation of number of blocks and number of spectra in the file
        no_of_spectra_in_bunch = max_shift
        no_of_bunches_per_file = int((df_filesize - 1024) / (no_of_spectra_in_bunch * no_of_points_for_fft_dedisp * 4))

        # Real time resolution of spectra
        fine_clock_freq = (int(clock_freq / 1000000.0) * 1000000.0)
        real_spectra_dt = float(no_of_points_for_fft_dedisp / fine_clock_freq)
        real_spectra_df = float((fine_clock_freq / 2) / (no_of_points_for_fft_dedisp / 2))

        print(' Number of spectra in bunch:                  ', no_of_spectra_in_bunch)
        print(' Number of bunches to read in file:           ', no_of_bunches_per_file)
        print(' Time resolution of calculated spectra:       ', round(real_spectra_dt*1000, 3), ' ms')
        print(' Frequency resolution of calculated spectra:  ', round(real_spectra_df/1000, 3), ' kHz \n')

        # !!! Fake timing. Real timing to be done!!!
        # *** Reading timeline file ***
        old_tl_file_name = fname.split("_Data_ch", 1)[0] + '_Timeline.wtxt'
        old_tl_file = open(old_tl_file_name, 'r')
        new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name

        file.seek(1024)  # Jumping to 1024 byte from file beginning

        bar = IncrementalBar(' Coherent dispersion delay removing: ', max=no_of_bunches_per_file-1, suffix='%(percent)d%%')

        for bunch in range(no_of_bunches_per_file-1):

            bar.next()

            # Read time from timeline file for the bunch
            time_scale_bunch = []
            for line in range(no_of_spectra_in_bunch):
                time_scale_bunch.append(str(old_tl_file.readline()))

            # Reading and reshaping all data with time data
            wf_data = np.fromfile(file, dtype='f4', count=no_of_spectra_in_bunch * no_of_points_for_fft_dedisp)
            
            '''
            fig = plt.figure(figsize=(9, 5))
            ax1 = fig.add_subplot(111)
            ax1.plot(wf_data, linestyle='-', linewidth='1.00', label='Initial waveform')
            ax1.legend(loc='upper right', fontsize=6)
            ax1.grid(b=True, which='both', color='silver', linestyle='-')
            ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
            pylab.savefig('00_Initial_waveform_' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
            plt.close('all')
            '''
            
            wf_data = np.reshape(wf_data, [no_of_points_for_fft_dedisp, no_of_spectra_in_bunch], order='F')

            # preparing matrices for spectra
            spectra = np.zeros((no_of_points_for_fft_dedisp, max_shift), dtype='complex64')

            # Calculation of spectra
            for i in range(no_of_spectra_in_bunch):
                spectra[:, i] = np.fft.fft(wf_data[:, i])
            del wf_data

            '''
            fig = plt.figure(figsize=(9, 5))
            ax1 = fig.add_subplot(111)
            ax1.plot(10 * np.log10(np.power(np.abs(spectra[:, 0]), 2)), linestyle='-', linewidth='1.00',
                     label='Initial spectra before cut')
            ax1.legend(loc='upper right', fontsize=6)
            ax1.grid(b=True, which='both', color='silver', linestyle='-')
            ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
            pylab.savefig('00a_Initial_doubled_imm_spectra' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
            plt.close('all')
            '''
            
            # Cut half of the spectra
            spectra = spectra[int(no_of_points_for_fft_dedisp/2):, :]

            ''' # making figures
            fig = plt.figure(figsize=(9, 5))
            ax1 = fig.add_subplot(111)
            ax1.imshow(np.flipud(10*np.log10(np.power(np.abs(spectra), 2))), aspect='auto', cmap='jet')
            ax1.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
            ax1.set_xlabel('Time points', fontsize=6, fontweight='bold')
            pylab.savefig('01_Initial_spectra_' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
            plt.close('all')

            fig = plt.figure(figsize=(9, 5))
            ax1 = fig.add_subplot(111)
            ax1.plot(10*np.log10(np.power(np.abs(spectra[:, 0]), 2)), linestyle='-', linewidth='1.00', label='Initial waveform')
            ax1.legend(loc='upper right', fontsize=6)
            ax1.grid(b=True, which='both', color='silver', linestyle='-')
            ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
            pylab.savefig('02_Initial_imm_spectra' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
            plt.close('all')
            '''
            
            #  Dispersion delay removing
            data_space = np.zeros((freq_points_num, 2 * max_shift), dtype='complex64')
            data_space[:, max_shift:] = spectra[:, :]
            data_space = pulsar_DM_compensation_with_indices_changes(data_space, shift_vector)
            del spectra

            # Adding the next data block
            buffer_array += data_space

            # Making and filling the array with fully ready data for plotting and saving to a file
            array_compensated_DM = buffer_array[:, 0: max_shift]

            if bunch > 0:

                # Saving time data to new file
                for i in range(len(time_scale_bunch)):
                    new_tl_file.write((time_scale_bunch[i][:]) + '')

                # Saving data with compensated DM
                spectra = array_compensated_DM.copy()

                '''
                # making figures
                fig = plt.figure(figsize=(9, 5))
                ax1 = fig.add_subplot(111)
                ax1.imshow(np.flipud(10*np.log10(np.power(np.abs(spectra), 2))), aspect='auto', cmap='jet')
                ax1.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
                ax1.set_xlabel('Time points', fontsize=6, fontweight='bold')
                pylab.savefig('03_Compensated_spectra_' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
                plt.close('all')

                fig = plt.figure(figsize=(9, 5))
                ax1 = fig.add_subplot(111)
                ax1.plot(10*np.log10(np.power(np.abs(spectra[:,0]), 2)), linestyle='-', linewidth='1.00', label='Initial waveform')
                ax1.legend(loc='upper right', fontsize=6)
                ax1.grid(b=True, which='both', color='silver', linestyle='-')
                ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
                pylab.savefig('04_Compensated_imm_spectra' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
                plt.close('all')
                '''

                wf_data = np.zeros((no_of_points_for_fft_dedisp, no_of_spectra_in_bunch))

                # Add lost half of the spectra

                second_spectra_half = spectra.copy()
                second_spectra_half = np.flipud(second_spectra_half)
                spectra = np.concatenate((second_spectra_half, spectra), axis=0)  # Changed places!!!

                '''
                fig = plt.figure(figsize=(9, 5))
                ax1 = fig.add_subplot(111)
                ax1.plot(10*np.log10(np.power(np.abs(spectra[:,0]), 2)), linestyle='-', linewidth='1.00', label='Initial waveform')
                ax1.legend(loc='upper right', fontsize=6)
                ax1.grid(b=True, which='both', color='silver', linestyle='-')
                ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
                pylab.savefig('05_Compensated_doubled_imm_spectra' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
                plt.close('all')
                '''

                # Making IFFT
                for i in range(no_of_spectra_in_bunch):
                    wf_data[:, i] = np.real(np.fft.ifft(spectra[:, i]))
                del spectra

                # Reshaping the waveform to single dimension (real)
                wf_data = np.reshape(wf_data, [no_of_points_for_fft_dedisp * no_of_spectra_in_bunch, 1], order='F')

                ''' # making figures
                fig = plt.figure(figsize=(9, 5))
                ax1 = fig.add_subplot(111)
                ax1.plot(wf_data, linestyle='-', linewidth='1.00', label='Initial waveform')
                ax1.legend(loc='upper right', fontsize=6)
                ax1.grid(b=True, which='both', color='silver', linestyle='-')
                ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
                pylab.savefig('06_Compensated_waveform_' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
                plt.close('all')
                '''
                
                # Saving waveform data to wf32 file
                file_data = open(file_data_name, 'ab')
                file_data.write(np.float32(wf_data).transpose().copy(order='C'))
                file_data.close()

                # !!! Saving time data to timeline file !!!

            # Rolling temp_array to put current data first
            buffer_array = np.roll(buffer_array, - max_shift)
            buffer_array[:, max_shift:] = 0

        bar.finish()
        old_tl_file.close()
        new_tl_file.close()

    return file_data_name


# *******************************************************************************
#          W A V E F O R M   F L O A T 3 2   T O   S P E C T R A                *
# *******************************************************************************


# def convert_wf32_to_dat(fname, no_of_points_for_fft_spectr, no_of_spectra_in_bunch):
#     '''
#     function converts waveform data in .wf32 format to spectra in .dat format
#     Input parameters:
#         fname -                 name of .wf32 file with waveform data
#         no_of_points_for_fft -  number of points for FFT to provide necessary time-frequency resolution
#     Output parameters:
#         file_data_name -        name of .dat file with result spectra
#     '''
#
#     # *** Data file header read ***
#     [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
#         clock_freq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, time_resolution, fmin, fmax,
#         df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(fname, 0, 0)
#
#     freq_points_num = int(no_of_points_for_fft_spectr/2)
#
#     with open(fname, 'rb') as file:
#         # *** Data file header read ***
#         file_header = file.read(1024)
#
#         # *** Creating a binary file with spectra data for long data storage ***
#         file_data_name = fname[:-5] + '.dat'
#         file_data = open(file_data_name, 'wb')
#         file_data.write(file_header)
#         file_data.seek(574)  # FFT size place in header
#         file_data.write(np.int32(no_of_points_for_fft_spectr).tobytes())
#         file_data.seek(624)  # Lb place in header
#         file_data.write(np.int32(0).tobytes())
#         file_data.seek(628)  # Hb place in header
#         file_data.write(np.int32(freq_points_num).tobytes())
#         file_data.seek(632)  # Wb place in header
#         file_data.write(np.int32(freq_points_num).tobytes())
#         file_data.seek(636)  # Navr place in header
#         file_data.write(np.int32(1).tobytes()) # !!! Check for correctness !!!
#         file_data.close()
#         del file_header
#
#         # Calculation of number of blocks and number of spectra in the file
#         no_of_bunches_per_file = int((df_filesize - 1024) / (no_of_spectra_in_bunch * no_of_points_for_fft_spectr * 4))
#
#         # Real time resolution of averaged spectra
#         fine_clock_freq = (int(clock_freq / 1000000.0) * 1000000.0)
#         real_spectra_dt = float(no_of_points_for_fft_spectr / fine_clock_freq)
#         real_spectra_df = float((fine_clock_freq / 2) / (no_of_points_for_fft_spectr / 2 ))
#
#         print(' Number of spectra in bunch:                  ', no_of_spectra_in_bunch)
#         print(' Number of bunches to read in file:           ', no_of_bunches_per_file)
#         print(' Time resolution of calculated spectra:       ', round(real_spectra_dt*1000, 3), ' ms')
#         print(' Frequency resolution of calculated spectra:  ', round(real_spectra_df/1000, 3), ' kHz')
#         print('\n  *** Reading data from file *** \n')
#
#         file.seek(1024)  # Jumping to 1024 byte from file beginning
#
#         # *** Creating a new timeline TXT file for results ***
#         new_tl_file_name = file_data_name.split('_Data_', 1)[0] + '_Timeline.txt'
#         new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
#         new_tl_file.close()
#
#         # *** Reading timeline file ***
#         old_tl_file_name = fname.split("_Data_", 1)[0] + '_Timeline.wtxt'
#         old_tl_file = open(old_tl_file_name, 'r')
#         new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
#
#         bar = IncrementalBar(' Conversion from waveform to spectra: ',
#                              max=no_of_bunches_per_file-1, suffix='%(percent)d%%')
#
#         for bunch in range(no_of_bunches_per_file-1):
#
#             bar.next()
#
#             # Read time from timeline file for the bunch
#             time_scale_bunch = []
#             for line in range(no_of_spectra_in_bunch):
#                 time_scale_bunch.append(str(old_tl_file.readline()))
#             # Saving time data to new file
#             for i in range(len(time_scale_bunch)):
#                 new_tl_file.write((time_scale_bunch[i][:]) + '')
#
#             # Reading and reshaping data of the bunch
#             wf_data = np.fromfile(file, dtype='f4', count = no_of_spectra_in_bunch * no_of_points_for_fft_spectr)
#             wf_data = np.reshape(wf_data, [no_of_points_for_fft_spectr, no_of_spectra_in_bunch], order='F')
#
#             # preparing matrices for spectra
#             spectra = np.zeros_like(wf_data)
#
#             # Calculation of spectra
#             for i in range(no_of_spectra_in_bunch):
#                 spectra[:, i] = np.power(np.abs(np.fft.fft(wf_data[:, i])), 2)
#
#             # Storing only first (left) mirror part of spectra
#             spectra = spectra[: int(no_of_points_for_fft_spectr/2), :]
#
#             # At 33 MHz the specter is usually upside down, to correct it we use flip up/down
#             if int(clock_freq/1000000) == 33:
#                 spectra = np.flipud(spectra)
#
#             # Saving spectra data to dat file
#             temp = spectra.transpose().copy(order='C')
#             file_data = open(file_data_name, 'ab')
#             file_data.write(np.float64(temp))
#             file_data.close()
#
#         bar.finish()
#
#     file.close()  # Close the data file
#     return file_data_name


# *******************************************************************************
#         N O R M A L I Z A T I O N   O F   D A T   S P E C T R A               *
# *******************************************************************************


def normalize_dat_file(directory, filename, no_of_spectra_in_bunch, median_filter_window):
    """
    function calculates the average spectrum  in DAT file and normalizes all spectra in file to average spectra
    Input parameters:
        directory - name of directory with initial dat file
        filename - name of initial dat file
    Output parameters:
        output_file_name -  name of result normalized .dat file
    """

    output_file_name = directory + 'Norm_' + filename
    filename = directory + filename

    # Opening DAT datafile
    file = open(filename, 'rb')

    # *** Data file header read ***
    df_filesize = os.stat(filename).st_size                         # Size of file
    df_filename = file.read(32).decode('utf-8').rstrip('\x00')      # Initial data file name
    file.close()

    if df_filename[-4:] == '.adr':

        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
                CLCfrq, df_creation_timeUTC, ReceiverMode, Mode, sumDifMode,
                NAvr, TimeRes, fmin, fmax, df, frequency, FFTsize, SLine,
                Width, BlockSize] = FileHeaderReaderADR(filename, 0, 0)

    if df_filename[-4:] == '.jds':     # If data obrained from DSPZ receiver

        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
        df, frequency, FreqPointsNum, dataBlockSize] = FileHeaderReaderJDS(filename, 0, 0)

    # Calculation of the dimensions of arrays to read
    nx = len(frequency)                           # the first dimension of the array
    ny = int(((df_filesize - 1024) / (nx * 8)))   # the second dimension of the array: file size - 1024 bytes

    num_of_blocks = int(ny // no_of_spectra_in_bunch)

    file = open(filename, 'rb')
    file.seek(1024)
    average_array = np.empty((nx, 0), float)
    for block in range(num_of_blocks):
        if block == (num_of_blocks-1):
            spectra_num_in_bunch = ny - (num_of_blocks-1) * no_of_spectra_in_bunch
        else:
            spectra_num_in_bunch = no_of_spectra_in_bunch

        data = np.fromfile(file, dtype=np.float64, count=nx * spectra_num_in_bunch)
        data = np.reshape(data, [nx, spectra_num_in_bunch], order='F')
        tmp = np.empty((nx, 1), float)
        tmp[:, 0] = data.mean(axis=1)[:]
        average_array = np.append(average_array, tmp, axis=1)  #

    average_profile = average_array.mean(axis=1)

    fig = plt.figure(figsize=(9, 5))
    ax1 = fig.add_subplot(111)
    ax1.plot(10 * np.log10(average_profile), linestyle='-', linewidth='1.00', label='Average spectra')
    ax1.legend(loc='upper right', fontsize=6)
    ax1.grid(b=True, which='both', color='silver', linestyle='-')
    ax1.set_xlabel('Frequency points, num.', fontsize=6, fontweight='bold')
    ax1.set_ylabel('Intensity, dB', fontsize=6, fontweight='bold')
    pylab.savefig('Averaged_spectra_'+filename[:-4]+'_before_filtering.png', bbox_inches='tight', dpi=160)
    plt.close('all')

    # Apply median filter to average profile
    average_profile = median_filter(average_profile, median_filter_window)

    fig = plt.figure(figsize=(9, 5))
    ax1 = fig.add_subplot(111)
    ax1.plot(10 * np.log10(average_profile), linestyle='-', linewidth='1.00', label='Average spectra')
    ax1.legend(loc='upper right', fontsize=6)
    ax1.grid(b=True, which='both', color='silver', linestyle='-')
    ax1.set_xlabel('Frequency points, num.', fontsize=6, fontweight='bold')
    ax1.set_ylabel('Intensity, dB', fontsize=6, fontweight='bold')
    pylab.savefig('Averaged_spectra_'+filename[:-4]+'_after_filtering.png', bbox_inches='tight', dpi=160)
    plt.close('all')

    # Normalization
    file.seek(0)
    file_header = file.read(1024)
    normalized_file = open(output_file_name, 'wb')
    normalized_file.write(file_header)
    del file_header

    for block in range(num_of_blocks):
        if block == (num_of_blocks - 1):
            spectra_num_in_bunch = ny - (num_of_blocks - 1) * no_of_spectra_in_bunch
        else:
            spectra_num_in_bunch = no_of_spectra_in_bunch

        data = np.fromfile(file, dtype=np.float64, count=nx * spectra_num_in_bunch)
        data = np.reshape(data, [nx, spectra_num_in_bunch], order='F')
        for j in range(spectra_num_in_bunch):
            data[:, j] = data[:, j] / average_profile[:]
        temp = data.transpose().copy(order='C')
        normalized_file.write(np.float64(temp))
    file.close()
    normalized_file.close()

    # *** Creating a new timeline TXT file for results ***
    new_tl_file_name = output_file_name.split('_Data_', 1)[0] + '_Timeline.txt'
    new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
    new_tl_file.close()

    # *** Reading timeline file ***
    old_tl_file_name = filename.split('_Data_', 1)[0] + '_Timeline.txt'
    old_tl_file = open(old_tl_file_name, 'r')
    new_tl_file = open(new_tl_file_name, 'w')

    # Read time from timeline file
    time_scale_bunch = old_tl_file.readlines()

    # Saving time data to new file
    for j in range(len(time_scale_bunch)):
        new_tl_file.write((time_scale_bunch[j][:]) + '')

    old_tl_file.close()
    new_tl_file.close()

    return output_file_name


# ###############################################################################
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

    dedispersed_wf32_files = []
    dedispersed_dat_files = []
    pulsar_ra, pulsar_dec, pulsar_dm, p_bar = catalogue_pulsar(pulsar_name)

    # '''
    print('\n\n  * Converting waveform from JDS to WF32 format... \n\n')

    initial_wf32_files = convert_jds_wf_to_wf32(source_directory, result_directory, no_of_bunches_per_file)
    print('\n List of WF32 files: ', initial_wf32_files, '\n')
    # '''

    if len(initial_wf32_files) > 1 and calibrate_phase:
        print('\n\n  * Making phase calibration of wf32 file... \n')
        wf32_two_channel_phase_calibration(initial_wf32_files[1], no_of_points_for_fft_dedisp, no_of_spectra_in_bunch,
                                           phase_calibr_txt_file)

    # initial_wf32_files = ['E310120_225419.jds_Data_chA.wf32', 'E310120_225419.jds_Data_chB.wf32']

    if len(initial_wf32_files) > 1 and make_sum > 0:
        print('\n\n  * Making sum of two WF32 files... \n')
        file_name = sum_signal_of_wf32_files(initial_wf32_files[0], initial_wf32_files[1], no_of_spectra_in_bunch)
        print('  Sum file:', file_name, '\n')
        typesOfData = ['wfA+B']
    else:
        file_name = initial_wf32_files[0]  # [0] or [1]
        typesOfData = ['chA']  # ['chA'] or ['chB']

    print('\n\n  * Making coherent dispersion delay removing... \n')

    # file_name = 'E280120_205409.jds_Data_chA.wf32'
    for i in range(int(pulsar_dm // dm_step)):  #
        t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print('\n Step ', i+1, ' of ', int((pulsar_dm // dm_step) + 1), ' started at: ', t, '\n')
        file_name = coherent_wf_to_wf_dedispersion(dm_step, file_name, no_of_points_for_fft_dedisp)
    print('\n Last step of ', np.round(pulsar_dm % dm_step, 6), ' pc/cm3 \n')
    file_name = coherent_wf_to_wf_dedispersion(pulsar_dm % dm_step, file_name, no_of_points_for_fft_dedisp)
    print('\n List of dedispersed WF32 files: ', initial_wf32_files, '\n')

    print('\n\n  * Making DAT files spectra of dedispersed wf32 data... \n\n')

    # file_name = 'DM_0.752_DM_1.0_DM_1.0_DM_1.0_DM_1.0_DM_1.0_E280120_205546.jds_Data_chA.wf32'
    # typesOfData = ['wfA']

    # initial_tl_fname = file_name + '_Timeline.wtxt'
    # new_tl_fname = file_name.split('.jds_')[0] + '.jds_Timeline.wtxt'
    # os.rename(initial_tl_fname, new_tl_fname)

    file_name = convert_wf32_to_dat_without_overlap(file_name, no_of_points_for_fft_spectr, no_of_spectra_in_bunch)
    # file_name = convert_wf32_to_dat_with_overlap(file_name, no_of_points_for_fft_spectr, no_of_spectra_in_bunch)

    print('\n Dedispersed DAT file: ', file_name, '\n')

    print('\n\n  * Making normalization of the dedispersed data... \n\n')

    # !!! Check the normalization of the file !!!
    # Why do not we use the smooth average spectrum? Is it necessary?
    output_file_name = normalize_dat_file('', file_name, no_of_spectra_in_bunch, median_filter_window)
    # '''
    print('!!! ', output_file_name)

    print('\n\n  * Making figures of 3 pulsar periods... \n\n')

    pulsar_period_DM_compensated_pics('', output_file_name, pulsar_name, 0, -0.15, 0.55, -0.2, 3.0, 3, 500, 'Greys')

    print('\n\n  * Making dynamic spectra figures of the dedispersed data... \n\n')

    result_folder_name = source_directory.split('/')[-2] + '_dedispersed'
    file_name = output_file_name.split('_Data_', 1)[0]  # + '.dat'
    ok = DAT_file_reader('', file_name, typesOfData, '', result_folder_name, 0, 0, 0, -120, -10, 0, 6, 6, 300, 'jet',
                         0, 0, 0, 20 * 10 ** (-12), 16.5, 33.0, '', '', 16.5, 33.0, [], 0)

    # output_file_name = 'Norm_DM_5.755_E280120_205546.jds_Data_chA.dat'

    print('!!! ', output_file_name)

    print('\n\n  * Cutting the data of found pulse ... ')
    print('\n\n  Examine 3 pulses pics and enter the number of period to cut:')
    #  Manual input of the pulsar period where pulse is found
    period_number = int(input('\n    Enter the number of period where the pulse is:  '))
    periods_per_fig = int(input('\n    Enter the length of wanted data in periods:     '))

    cut_needed_pulsar_period_from_dat('', output_file_name, pulsar_name, period_number, -0.15,
                                      0.55, -0.2, 3.0, periods_per_fig, 500, 'Greys')

    endTime = time.time()

    print('\n\n  The program execution lasted for ',
          round((endTime - startTime), 2), 'seconds (', round((endTime - startTime)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
