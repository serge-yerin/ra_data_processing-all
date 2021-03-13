# Python3
# pip install progress
Software_version = '2021.02.18'
Software_name = 'JDS Waveform calibration data analysis'

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************

source_directory = 'DATA/'              # Directory with JDS files to be analyzed
result_directory = ''                   # Directory where DAT files to be stored (empty string means project directory)
no_of_points_for_fft = 16384            # Number of points for FFT on result spectra # 8192, 16384, 32768, 65536, 131072

# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import os
import sys
import time
import pylab
from scipy import ndimage
import numpy as np
from os import path
from progress.bar import IncrementalBar
from matplotlib import rc
import matplotlib.pyplot as plt

# To change system path to main source_directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_common_modules.find_and_check_files_in_current_folder import find_and_check_files_in_current_folder
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.JDS_waveform_time import JDS_waveform_time

# ###############################################################################


def phase_linearization_rad(matrix):
    """
    Makes a vector of phase values linear without 360 deg subtraction
    """
    matrix_lin = np.zeros((len(matrix)))
    matrix_lin[:] = matrix[:]
    const = 0
    for elem in range(1, len(matrix)):
        if (matrix[elem] - matrix[elem-1]) > 4:
            const = const + 2 * np.pi
        matrix_lin[elem] = matrix_lin[elem] - const
    const = 0
    for elem in range(1, len(matrix)):
        if (matrix[elem-1] - matrix[elem]) > 4:
            const = const + 2*np.pi
        matrix_lin[elem] = matrix_lin[elem] + const
    return matrix_lin


def median_filter(data, window_len):
    """
    A simple median filter to smooth the data
    """
    fitered_data = ndimage.median_filter(data, size=window_len)
    return fitered_data


def correlate_two_wf32_signals(file_name_1, file_name_2, no_of_points_for_fft, filter_or_not, plot_or_not):
    """
    Function reads two wf32 waveform data files and make correlation of the data to calibrate observations
    Input parameters:
        file_name_1 - first input wf32 file
        file_name_2 - second input wf32 file
        no_of_points_for_fft - number of data points to calculate correlation
    Output parameters:
        xxx - xxx
    """

    df_filesize_1 = os.stat(file_name_1).st_size                         # Size of file
    df_filesize_2 = os.stat(file_name_2).st_size                         # Size of file
    if df_filesize_1 != df_filesize_2:
        print('  Size of file 1:    ', df_filesize_1, '\n  Size of file 2:', df_filesize_2)
        sys.exit('   ERROR!!! Files have different sizes!')

    # Calculation of the dimensions of arrays to read
    ny = int((df_filesize_1 - 1024) / 4)   # number of samples to read: file size - 1024 bytes
    num_of_spectra_in_files = int(ny // no_of_points_for_fft)

    print('\n  Correlation calculation... \n')
    print('  Number of time samples in files:           ', ny)
    print('  Number of spectra in files:                ', num_of_spectra_in_files)
    if num_of_spectra_in_files > 16384:
        num_of_spectra_in_files = 16384
        print('  Number of spectra in files is limited to:  ', num_of_spectra_in_files)

    file_1 = open(file_name_1, 'rb')
    file_2 = open(file_name_2, 'rb')
    file_1.seek(1024)
    file_2.seek(1024)

    # Data reading

    data_1 = np.fromfile(file_1, dtype=np.float32, count=num_of_spectra_in_files * no_of_points_for_fft)
    data_2 = np.fromfile(file_2, dtype=np.float32, count=num_of_spectra_in_files * no_of_points_for_fft)

    data_1 = np.reshape(data_1, [no_of_points_for_fft, num_of_spectra_in_files], order='F')
    data_2 = np.reshape(data_2, [no_of_points_for_fft, num_of_spectra_in_files], order='F')

    # preparing matrices for spectra
    spectrum_1 = np.zeros((no_of_points_for_fft, num_of_spectra_in_files), dtype='complex')
    spectrum_2 = np.zeros((no_of_points_for_fft, num_of_spectra_in_files), dtype='complex')

    # Calculation of spectra
    for i in range(num_of_spectra_in_files):
        spectrum_1[:, i] = np.fft.fft(data_1[:, i])
        spectrum_2[:, i] = np.fft.fft(data_2[:, i])

    del data_1, data_2

    # Calculation of cross signal spectra
    cross_spectrum = spectrum_1[:, :] * np.conj(spectrum_2[:, :])

    # Cutting the half of the full signal spectra
    spectrum_1 = np.log10(np.power(np.abs(spectrum_1[no_of_points_for_fft // 2:, :]), 2))
    spectrum_2 = np.log10(np.power(np.abs(spectrum_2[no_of_points_for_fft // 2:, :]), 2))

    # Calculation of averaged signal spectra
    spectrum_av_1 = np.mean(spectrum_1, axis=1)
    spectrum_av_2 = np.mean(spectrum_2, axis=1)
    first_spectrum_1 = spectrum_1[:, 0]
    first_spectrum_2 = spectrum_2[:, 0]
    del spectrum_1, spectrum_2

    if plot_or_not:
        # Figure of averaged and non-averaged spectra
        rc('font', size=10, weight='bold')
        fig = plt.figure(figsize=(18, 10))
        fig.suptitle('Comparison of current and averaged cross spectra of waveform signals', fontsize=12, fontweight='bold')
        ax1 = fig.add_subplot(211)
        ax1.plot(first_spectrum_1, linestyle='-', linewidth='1.00', label='Current spectrum')
        ax1.plot(spectrum_av_1, linestyle='-', linewidth='1.00', label='Averaged spectrum')
        ax1.set(xlim=(0, no_of_points_for_fft // 2))
        ax1.legend(loc='upper right', fontsize=10)
        ax2 = fig.add_subplot(212)
        ax2.plot(first_spectrum_2, linestyle='-', linewidth='1.00', label='Current spectrum')
        ax2.plot(spectrum_av_2, linestyle='-', linewidth='1.00', label='Averaged spectrum')
        ax2.set(xlim=(0, no_of_points_for_fft // 2))
        ax2.set_xlabel('Frequency channels, #', fontsize=10, fontweight='bold')
        ax2.legend(loc='upper right', fontsize=10)
        fig.subplots_adjust(hspace=0.07, top=0.94)
        pylab.savefig('00_Signal_spectra.png', bbox_inches='tight', dpi=160)
        plt.close('all')

    # Calculation of average cross spectrum
    cross_spectrum_av = np.mean(cross_spectrum, axis=1)
    cross_spectrum_av[0] = 0

    if plot_or_not:
        rc('font', size=10, weight='bold')
        fig = plt.figure(figsize=(18, 10))
        fig.suptitle('Waveform signals averaged cross spectra without filter', fontsize=12, fontweight='bold')
        ax1 = fig.add_subplot(211)
        # ax1.set_title('Files: ' + file_names[0] + ' - ' + file_names[-1], fontsize=12)
        ax1.plot(np.log10(np.abs(cross_spectrum_av[8192:])), linestyle='-', linewidth='1.00', label='Cross spectrum module')
        # ax1.set_ylabel('Signal, A.U.', fontsize=10, fontweight='bold')
        ax1.set(xlim=(0, no_of_points_for_fft // 2))
        ax1.legend(loc='upper right', fontsize=10)
        ax2 = fig.add_subplot(212)
        ax2.plot(np.angle(cross_spectrum_av[8192:]), linestyle='-', linewidth='1.00', label='Cross spectrum angle')
        # ax2.set_ylabel('Signal, A.U.', fontsize=10, fontweight='bold')
        ax2.set(xlim=(0, no_of_points_for_fft // 2))
        ax2.set_xlabel('Frequency channels, #', fontsize=10, fontweight='bold')
        ax2.legend(loc='upper right', fontsize=10)
        fig.subplots_adjust(hspace=0.07, top=0.94)
        pylab.savefig('01_Cross_spectra.png', bbox_inches='tight', dpi=160)
        plt.close('all')

    cross_spectrum_abs = np.abs(cross_spectrum_av[no_of_points_for_fft//2:])
    if filter_or_not:
        cross_spectrum_abs = median_filter(cross_spectrum_abs, 30)

    # cross_spectrum_arg = np.angle(cross_spectrum_av[no_of_points_for_fft//2:])
    cross_spectrum_arg = np.angle(cross_spectrum_av[:])

    cross_spectrum_arg = phase_linearization_rad(cross_spectrum_arg)
    if filter_or_not:
        cross_spectrum_arg = median_filter(cross_spectrum_arg, 30)

    if plot_or_not:
        rc('font', size=10, weight='bold')
        fig = plt.figure(figsize=(18, 10))
        fig.suptitle('Waveform signals averaged cross spectra with median filter', fontsize=12, fontweight='bold')
        ax1 = fig.add_subplot(211)
        # ax1.set_title('Files: ' + file_names[0] + ' - ' + file_names[-1], fontsize=12)
        ax1.plot(np.log10(cross_spectrum_abs), linestyle='-', linewidth='1.00', label='Cross spectrum module')
        # ax1.set_ylabel('Signal, A.U.', fontsize=10, fontweight='bold')
        ax1.set(xlim=(0, no_of_points_for_fft // 2))
        ax1.legend(loc='upper right', fontsize=10)
        ax2 = fig.add_subplot(212)
        ax2.plot(cross_spectrum_arg[no_of_points_for_fft//2:], linestyle='-', linewidth='1.00', label='Cross spectrum angle')
        # ax2.set_ylabel('Signal, A.U.', fontsize=10, fontweight='bold')
        ax2.set(xlim=(0, no_of_points_for_fft // 2))
        ax2.set_xlabel('Frequency channels, #', fontsize=10, fontweight='bold')
        ax2.legend(loc='upper right', fontsize=10)
        fig.subplots_adjust(hspace=0.07, top=0.94)
        pylab.savefig('02_Cross_spectrum_linear.png', bbox_inches='tight', dpi=160)
        plt.close('all')

    corr_function = np.fft.ifft(cross_spectrum)
    print(' Corr function size ', corr_function.shape)
    corr_function_av = np.mean(corr_function, axis=1)
    print(' Av corr function size ', corr_function_av.shape)
    corr_function_av[0] = 0
    corr_function_av_abs = np.abs(corr_function_av)
    corr_function_av_re = np.real(corr_function_av)
    corr_function_av_arg = np.angle(corr_function_av)
    # corr_function_av_arg = phase_linearization_rad(corr_function_av_arg)
    #if filter_or_not:
    #    cross_spectrum_arg = median_filter(cross_spectrum_arg, 30)

    if plot_or_not:
        rc('font', size=10, weight='bold')
        fig = plt.figure(figsize=(18, 10))
        fig.suptitle('Waveform signals averaged correlation function', fontsize=12, fontweight='bold')
        ax1 = fig.add_subplot(211)
        # ax1.set_title('Files: ' + file_names[0] + ' - ' + file_names[-1], fontsize=12)
        ax1.plot(np.log10(corr_function_av_abs[8192:]), linestyle='-', linewidth='1.00', label='Correlation Abs')
        # ax1.set_ylabel('Signal, A.U.', fontsize=10, fontweight='bold')
        ax1.set(xlim=(0, no_of_points_for_fft // 2))
        ax1.legend(loc='upper right', fontsize=10)
        ax2 = fig.add_subplot(212)
        ax2.plot(corr_function_av_arg[8192:], linestyle='-', linewidth='1.00', label='Correlation Phase')
        # ax2.set_ylabel('Signal, A.U.', fontsize=10, fontweight='bold')
        ax2.set(xlim=(0, no_of_points_for_fft // 2))
        ax2.set_xlabel('Frequency channels, #', fontsize=10, fontweight='bold')
        ax2.legend(loc='upper right', fontsize=10)
        fig.subplots_adjust(hspace=0.07, top=0.94)
        pylab.savefig('03_Correlation_function_Abs-Ang.png', bbox_inches='tight', dpi=160)
        plt.close('all')

    return cross_spectrum_abs, cross_spectrum_arg, spectrum_av_1, spectrum_av_2, first_spectrum_1, first_spectrum_2, \
            corr_function_av_abs, corr_function_av_arg, corr_function_av_re


def convert_one_jds_wf_to_wf32(source_file, result_directory, no_of_bunches_per_file):
    """
    function converts jds waveform data to wf32 waveform data for further processing (coherent dedispersion) and
    saves txt files with time data
    Input parameters:
        source_directory - directory where initial jds waveform data are stored
        result_directory - directory where new wf32 files will be stored
        no_of_bunches_per_file - number of data bunches per file to peocess (depends on RAM volume on the PC)
    Output parameters:
        result_wf32_files - list of results files
    """

    # *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
     clock_freq, df_creation_timeUTC, channel, receiver_mode, Mode, Navr, time_res, fmin, fmax,
     df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(source_file, 0, 0)
    if Mode > 0:
        sys.exit('  ERROR!!! Data recorded in wrong mode! Waveform mode needed.\n\n    Program stopped!')

    result_wf32_files = []

    fname = source_file

    # Create long data files and copy first data file header to them
    with open(fname, 'rb') as file:
        # *** Data file header read ***
        file_header = file.read(1024)

    # *** Creating a name for long timeline TXT file ***
    tl_file_name = df_filename + '_Timeline.wtxt'
    tl_file = open(result_directory + tl_file_name, 'w')  # Open and close to delete the file with the same name
    tl_file.close()

    # *** Creating a binary file with data for long data storage ***
    file_data_A_name = result_directory + df_filename + '_Data_chA.wf32'
    result_wf32_files.append(file_data_A_name)
    file_data_A = open(file_data_A_name, 'wb')
    file_data_A.write(file_header)
    file_data_A.close()

    if channel == 2:
        file_data_B_name = result_directory + df_filename + '_Data_chB.wf32'
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

    print('  Number of blocks in file:                  ', no_of_blocks_in_file)
    print('  Number of bunches to read in file:         ', no_of_bunches_per_file, '\n')

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

        bar = IncrementalBar('  File reading: ', max=no_of_bunches_per_file, suffix='%(percent)d%%')

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


def obtain_calibr_matrix_for_2_channel_wf_calibration(path_to_calibr_data, no_of_points_for_fft):
    """
    The function reads 2-channel waveform calibration files (UTR-2 noise generator calibration with a set of
    attenuators) calculates the cross-spectra of two channels in each file and provides a phase difference txt file
    for pulsar waveform observations calibration

    """

    file_list = find_and_check_files_in_current_folder(path_to_calibr_data, '.jds')

    labels = []
    cross_sp_ampl = []
    cross_sp_angl = []
    file_names = []
    spectrum_ch_1 = []
    spectrum_ch_2 = []
    imed_spectrum_ch_1 = []
    imed_spectrum_ch_2 = []
    corr_f_abs = []
    corr_f_ang = []
    corr_f_re = []

    result_path = 'RESULTS_WF_calibration_analyzer/'
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    # Main loop by files start
    for file_no in range(len(file_list)):  # loop by files

        fname = path_to_calibr_data + file_list[file_no]

        # *** Data file header read ***
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
         clock_freq, df_creation_timeUTC, channel, receiver_mode, Mode, Navr, time_res, fmin, fmax,
         df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(fname, 0, 0)

        labels.append(df_system_name + ' ' + df_description.replace('_', ' '))
        file_names.append(df_filename)

        print('\n  Processing file: ', df_description.replace('_', ' '), ',  # ', file_no+1, ' of ', len(file_list), '\n')

        wf32_files = convert_one_jds_wf_to_wf32(fname, result_directory, 16)


        ampl_corr, angle_corr, av_sp_1, av_sp_2, sp_1, sp_2, cf_abs, cf_arg, cf_re = correlate_two_wf32_signals(wf32_files[0],
                                    wf32_files[1], no_of_points_for_fft, True, False)

        cross_sp_ampl.append(ampl_corr)
        cross_sp_angl.append(angle_corr)
        spectrum_ch_1.append(av_sp_1)
        spectrum_ch_2.append(av_sp_2)
        imed_spectrum_ch_1.append(sp_1)
        imed_spectrum_ch_2.append(sp_2)
        corr_f_abs.append(cf_abs)
        corr_f_ang.append(cf_arg)
        corr_f_re.append(cf_re)

    # Figures of initial and averaged spectra for each file
    for i in range(len(file_list)):
        # Figure of averaged and non-averaged spectra
        rc('font', size=10, weight='bold')
        fig = plt.figure(figsize=(18, 10))
        fig.suptitle('Comparison of current and averaged cross spectra of waveform signals for ' + file_list[i] +
                     ' (' + labels[i] + ')', fontsize=12, fontweight='bold')
        ax1 = fig.add_subplot(211)
        ax1.plot(imed_spectrum_ch_1[i], linestyle='-', linewidth='1.00', label='Current spectrum')
        ax1.plot(spectrum_ch_1[i], linestyle='-', linewidth='1.00', label='Averaged spectrum')
        ax1.set(xlim=(0, no_of_points_for_fft // 2))
        ax1.legend(loc='upper right', fontsize=10)
        ax2 = fig.add_subplot(212)
        ax2.plot(imed_spectrum_ch_2[i], linestyle='-', linewidth='1.00', label='Current spectrum')
        ax2.plot(spectrum_ch_2[i], linestyle='-', linewidth='1.00', label='Averaged spectrum')
        ax2.set(xlim=(0, no_of_points_for_fft // 2))
        ax2.set_xlabel('Frequency channels, #', fontsize=10, fontweight='bold')
        ax2.legend(loc='upper right', fontsize=10)
        fig.subplots_adjust(hspace=0.07, top=0.94)
        pylab.savefig(result_path + 'Signal_spectra_' + file_names[i] + '.png', bbox_inches='tight', dpi=160)
        plt.close('all')

        # Plot cross spectra matrix
        rc('font', size=10, weight='bold')
        fig = plt.figure(figsize=(18, 10))
        fig.suptitle('Calibration matrix of waveform signals correlation for ' + file_list[i] +
                     ' (' + labels[i] + ')', fontsize=12, fontweight='bold')
        ax1 = fig.add_subplot(211)
        ax1.set_title('Files: ' + file_names[0] + ' - ' + file_names[-1], fontsize=12)
        ax1.plot(np.log10(cross_sp_ampl[i]), linestyle='-', linewidth='1.30', label='Cross spectra amplitude')
        ax1.legend(loc='upper right', fontsize=10)
        ax1.set(xlim=(0, no_of_points_for_fft // 2))
        ax1.set_ylabel('Amplitude, A.U.', fontsize=10, fontweight='bold')
        ax2 = fig.add_subplot(212)
        ax2.plot(cross_sp_angl[i], linestyle='-', linewidth='1.30', label='Cross spectra phase')
        ax2.set(xlim=(0, no_of_points_for_fft // 2))
        ax2.set_xlabel('Frequency channels, #', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Phase, rad', fontsize=10, fontweight='bold')
        ax2.legend(loc='upper right', fontsize=10)
        fig.subplots_adjust(hspace=0.07, top=0.94)
        pylab.savefig(result_path + 'WF_signal_correlation_' + file_names[i] + '.png', bbox_inches='tight', dpi=160)
        plt.close('all')

    # Plot calibration spectra matrix
    rc('font', size=10, weight='bold')
    fig = plt.figure(figsize=(18, 10))
    fig.suptitle('Calibration matrix of waveform signals', fontsize=12, fontweight='bold')
    ax1 = fig.add_subplot(211)
    ax1.set_title('Files: ' + file_names[0] + ' - ' + file_names[-1], fontsize=12)
    for i in range(len(spectrum_ch_1)):
        ax1.plot(spectrum_ch_1[i], linestyle='-', linewidth='1.30', label=labels[i])
    ax1.legend(loc='upper right', fontsize=10)
    ax1.set(xlim=(0, no_of_points_for_fft//2))
    ax1.set_ylabel('Signal, A.U.', fontsize=10, fontweight='bold')
    ax2 = fig.add_subplot(212)
    for i in range(len(spectrum_ch_2)):
        ax2.plot(spectrum_ch_2[i], linestyle='-', linewidth='1.30', label=labels[i])
    ax2.set(xlim=(0, no_of_points_for_fft//2))
    ax2.set_xlabel('Frequency channels, #', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Signal, A.U.', fontsize=10, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=10)
    fig.subplots_adjust(hspace=0.07, top=0.94)
    pylab.savefig(result_path + 'Calibration_matrix_wf_spectra.png', bbox_inches='tight', dpi=160)
    plt.close('all')

    # Plot cross spectra matrix
    rc('font', size=10, weight='bold')
    fig = plt.figure(figsize=(18, 10))
    fig.suptitle('Cross spectra matrix of waveform signals correlation', fontsize=12, fontweight='bold')
    ax1 = fig.add_subplot(211)
    ax1.set_title('Files: ' + file_names[0] + ' - ' + file_names[-1], fontsize=12)
    for i in range(len(cross_sp_ampl)):
        ax1.plot(np.log10(cross_sp_ampl[i]), linestyle='-', linewidth='1.30', label=labels[i])
    ax1.legend(loc='upper right', fontsize=10)
    ax1.set(xlim=(0, no_of_points_for_fft//2))
    ax1.set_ylabel('Amplitude, A.U.', fontsize=10, fontweight='bold')
    ax2 = fig.add_subplot(212)
    for i in range(len(cross_sp_angl)):
        ax2.plot(cross_sp_angl[i], linestyle='-', linewidth='1.30', label=labels[i])
    ax2.set(xlim=(0, no_of_points_for_fft//2))
    ax2.set_xlabel('Frequency channels, #', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Phase, rad', fontsize=10, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=10)
    fig.subplots_adjust(hspace=0.07, top=0.94)
    pylab.savefig(result_path + 'Calibration_matrix_wf_cross_spectra.png', bbox_inches='tight', dpi=160)
    plt.close('all')

    # Plot correlation matrix
    rc('font', size=10, weight='bold')
    fig = plt.figure(figsize=(18, 10))
    fig.suptitle('Cross spectra matrix of waveform signals correlation', fontsize=12, fontweight='bold')
    ax1 = fig.add_subplot(211)
    ax1.set_title('Files: ' + file_names[0] + ' - ' + file_names[-1], fontsize=12)
    for i in range(len(corr_f_abs)):
        ax1.plot(np.log10(corr_f_abs[i]), linestyle='-', linewidth='1.30', label=labels[i])
    ax1.legend(loc='upper right', fontsize=10)
    ax1.set(xlim=(0, no_of_points_for_fft // 1))
    ax1.set_ylabel('Amplitude, A.U.', fontsize=10, fontweight='bold')
    ax2 = fig.add_subplot(212)
    for i in range(len(corr_f_ang)):
        ax2.plot(corr_f_ang[i], linestyle='-', linewidth='1.30', label=labels[i])
    ax2.set(xlim=(0, no_of_points_for_fft // 1))
    ax2.set_xlabel('Frequency channels, #', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Phase, rad', fontsize=10, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=10)
    fig.subplots_adjust(hspace=0.07, top=0.94)
    pylab.savefig(result_path + 'Calibration_matrix_wf_correlation.png', bbox_inches='tight', dpi=160)
    plt.close('all')

    # Plot mutual correlation function
    rc('font', size=10, weight='bold')
    fig = plt.figure(figsize=(18, 10))
    fig.suptitle('Mutual correlation matrix of waveform signals', fontsize=12, fontweight='bold')
    ax1 = fig.add_subplot(111)
    ax1.set_title('Files: ' + file_names[0] + ' - ' + file_names[-1], fontsize=12)
    for i in range(len(corr_f_re)):
        ax1.plot(corr_f_re[i], linestyle='-', linewidth='1.30', label=labels[i])
    ax1.legend(loc='upper right', fontsize=10)
    ax1.set(xlim=(0, no_of_points_for_fft // 1))
    ax1.set_ylabel('Amplitude, A.U.', fontsize=10, fontweight='bold')
    fig.subplots_adjust(top=0.94)
    pylab.savefig(result_path + 'Calibration_matrix_of_wf_mutual_correlation_function.png', bbox_inches='tight', dpi=160)
    plt.close('all')

    # Save phase matrix to txt files
    for i in range(len(file_list)):
        phase_txt_file = open(result_path + 'Calibration_' + file_names[i] + '_cross_spectra_phase.txt', "w")
        for freq in range(no_of_points_for_fft // 1):  # //2
            phase_txt_file.write(''.join(' {:+12.7E}'.format(cross_sp_angl[i][freq])) + ' \n')
        phase_txt_file.close()

    return 0


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

    # print('\n\n  * Converting waveform from JDS to WF32 format... \n\n')
    #
    # initial_wf32_files = convert_jds_wf_to_wf32(source_directory, result_directory, no_of_points_for_fft)
    # print('\n List of WF32 files: ', initial_wf32_files, '\n')
    #
    # # initial_wf32_files = ['E300120_233404.jds_Data_chA.wf32', 'E300120_233404.jds_Data_chB.wf32']
    # correlate_two_wf32_signals(initial_wf32_files[0], initial_wf32_files[1], no_of_points_for_fft, False)

    obtain_calibr_matrix_for_2_channel_wf_calibration(source_directory, no_of_points_for_fft)

    endTime = time.time()
    print('\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                     round((endTime - startTime)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
