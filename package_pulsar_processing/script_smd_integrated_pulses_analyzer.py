# Python3
software_version = '2022.10.15'
software_name = 'Pulsar averaged pulse SMD analyzer'
# Program intended to read, show and analyze averaged pulse data of pulsar observation from SMD files
# SMD file is a result of data processing by the pipeline written in IDL by V. V. Zakharenko

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# source_path = 'e:/RA_DATA_ARCHIVE/SMD_pulsar_pulses_files/'
source_path = 'e:/RA_DATA_RESULTS/B1919+21_2020.04.04_UTR2_B1919+21/'
result_path = 'e:/RA_DATA_RESULTS/'

# filename = 'DSPZ-D140219_111305-D140219_183011_PSRJ0250+5854_Sum.ucd.smd'
filename = 'DSPZ_B1919+21_DM_12.4449_C040420_020109.jds_Data_chA - folded pulses.smp'

# pulsar_name = 'B0809+74' 'B0834+06' 'B1133+16' 'B1919+21' 'J0250+5854'
pulsar_name = 'B1919+21'

scale_factor = 10                # Time resolution scaling factor, use 1 as default
dm_already_compensated = True    # If data file has already compensated DM delay use True (new soft), False otherwise
auto_optimal_dm_search = True    # Automatically search optimal DM (1 - auto, 2 - use predefined value)
no_of_dm_steps = 181             # Number of DM steps to plot 361
dm_var_step = 0.002              # Step of optimal DM finding  0.002
cleaning_switch = 1              # Use cleaning? (1 - Yes, 0 - No)
rfi_std_const = 1.0              # Standard deviation of integrated profile to clean channels
save_intermediate_data = 1       # Plot intermediate figures? (1 = Yes)
average_channel_num = 128        # Number of points to average in frequency
aver_time_points_num = 8         # Number of points to average time
frequency_band_cut = True        # Plot profiles in small frequency bands?
specify_freq_range = False       # Specify particular frequency range (True) or use the whole range (False)

# frequency_cuts = [20.625, 24.750, 28.875]  # UTR-2 16.5 - 33 MHz divided into 4 bands
frequency_cuts = [18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0]  # UTR-2 16.5 - 33 MHz divided bands of 2 MHz or less
# frequency_cuts = [17.0,18.0,19.0,20.0,21.0,22.0,23.0,24.0,25.0,26.0,27.0,28.0,29.0,30.0,31.0,32.0]  # UTR-2 16.5 - 33
# frequency_cuts = [12.375, 16.5, 20.625, 24.750, 28.875]  # UTR-2 8.25 - 33 MHz divided into 6 bands
# frequency_cuts = [40.0, 50.0, 60.0]  # GURT 30-70 MHz divided into 4 bands

colormap = 'Greys'               # Possible: 'jet', 'Blues', 'Purples'
custom_dpi = 200

# Begin and end frequency of dynamic spectrum (MHz)
freq_start_array = 18.0
freq_stop_array =  28.0


# FEATURES TO ADD
# Make check of the frequencies to cut lag between the limits of the band
# make possible to average in time the raw dedispersed data to increase SNR
# Incorporate data on UTR-2 and GURT effective area, background temperatures and show data in fluxes
# Make the rolling of SNR curve for easy finding of the noise area
# https://stackoverflow.com/questions/9111711/get-coordinates-of-local-maxima-in-2d-array-above-certain-value
# https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.ndimage.filters.maximum_filter.html

################################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
from matplotlib.gridspec import GridSpec
from datetime import datetime
from matplotlib import rc
from os import path
import matplotlib.pyplot as plt
import numpy as np
import struct
import pylab
import time
import sys
import os
import matplotlib.ticker as mticker   # <---- Added to suppress warning

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_astronomy.f_pulsar_visible_period import pulsar_visible_period
from package_plot_formats.plot_formats import make_1d_plot, make_2d_plot
from package_plot_formats.plot_formats_for_pulsars import plot_average_profiles
from package_ra_data_processing.choose_frequency_range import choose_frequency_range  # Check if are the same
from package_ra_data_files_formats.specify_frequency_range import specify_frequency_range  # Check if are the same
from package_ra_data_files_formats.read_file_header_adr import file_header_adr_read_old
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_ra_data_files_formats.f_check_duration_of_dat_file import check_duration_of_dat_file
from package_pulsar_processing.f_pulsar_dm_variation import pulsar_dm_variation
from package_pulsar_processing.pulsar_dm_shift_calculation_aver_pulse import pulsar_dm_shift_calculation_aver_pulse
from package_pulsar_processing.pulsar_dm_full_shift_calculation import dm_full_shift_calculate
from package_pulsar_processing.pulsar_dm_compensation_with_indices_changes import \
    pulsar_DM_compensation_with_indices_changes


def simple_mask_clean(array, rfi_std_const):
    """
    Simplest cleaning of entire frequency channels polluted with RFI
    Input parameters:
        array: data array to clean (np.array)
        rfi_std_const: std of data to consider rgi and clean it
    Output parameters:
        array: cleaned data (np.array)
        mask: mask array (np.array)
    """
    # Search for polluted channels in averaged profile
    integr_profile = np.sum(array, axis=0)
    ip_mean = np.mean(integr_profile)
    ip_std = np.std(integr_profile)
    polluted_channels = []
    for k in range(len(integr_profile)):
        if integr_profile[k] > ip_mean + rfi_std_const * ip_std:
            polluted_channels.append(k)

    # Making mask array
    mask = np.zeros_like(array, dtype=bool)
    for k in range(len(polluted_channels)):
        mask[:, polluted_channels[k]] = 1

    # Mask polluted channels in array
    masked_array = np.ma.masked_array(array, mask=mask)

    # Calculate mean of array with masked polluted channels
    ma_mean = np.mean(masked_array)

    # Change the polluted channels to masked array mean value
    array = array * np.abs(mask - 1) + mask * ma_mean

    return array, mask


def averaging_in_frequency(matrix, freq_num, frequency_list, samples_per_period, average_channel_num, roll_number,
                           result_path, filename, save_intermediate_data):
    """

    Args:
        matrix: input data array to analyze (np.array)
        freq_num: number of frequencies in the data array (int)
        frequency_list: list of frequencies used
        samples_per_period: number of samples per period
        average_channel_num: number of frequency channels to average
        roll_number: number of indexes to roll to make the pulse in the center of the picture
        result_path: path to results
        filename: name of the file to display in the plot
        save_intermediate_data: do we need to save a plot? (int)

    Returns:
        reduced_matrix: averaged array (np.array)
        reduced_frequency_list list of frequencies after reduction
    """

    # *** Averaging data in frequency domain ***
    reduced_matrix = \
        np.array([[0.0 for col in range(samples_per_period)] for row in range(int(freq_num / average_channel_num))])
    for j in range(int(freq_num / average_channel_num)):
        for k in range(samples_per_period):
            reduced_matrix[j, k] = sum(matrix[j * average_channel_num: (j+1) * average_channel_num, k])

    reduced_matrix = np.roll(reduced_matrix, roll_number)  # Rolling the array to make the pulse in the center

    print('\n    Length of initial frequency axis: ', len(frequency_list))
    reduced_frequency_list = frequency_list[::average_channel_num]
    print('    Length of new frequency axis:     ', len(reduced_frequency_list), ' \n')

    # *** Plot of raw data with DM compensation and data reduction ***

    if save_intermediate_data == 1:
        make_2d_plot(reduced_matrix, result_path + '/03 - Dedispersed integrated data.png', reduced_frequency_list,
                     colormap, 'Dedispersed and averaged in frequency pulsar pulse \n File: ' + filename, custom_dpi)

    return reduced_matrix, reduced_frequency_list


# *******************************************************************************
#  ***        Calculations and figures for various frequency bands            ***
# *******************************************************************************

def analysis_in_frequency_bands(array, frequency_list, frequency_cuts, samples_per_period, result_path, filename,
                                begin_index, end_index, roll_number):
    no_of_freq_bands = len(frequency_cuts) + 1
    band_freq_name = ["" for t in range(no_of_freq_bands)]
    snr_max_in_band = np.zeros((no_of_freq_bands))
    snr_per_mhz_in_band = np.zeros((no_of_freq_bands))
    band_frequencies = np.zeros((no_of_freq_bands, 2))  # matrix of bands frequency limits
    profiles_var_in_band = np.zeros((no_of_freq_bands, samples_per_period))  # matrix for all profiles

    for band in range(no_of_freq_bands):

        # Find the limits of the frequency range
        if band == 0:
            freq_start = frequency_list[0]
            freq_stop = frequency_cuts[band]
        elif band == no_of_freq_bands-1:
            freq_start = frequency_cuts[band-1]
            freq_stop = frequency_list[len(frequency_list)-1]
        else:
            freq_start = frequency_cuts[band-1]
            freq_stop = frequency_cuts[band]

        # Cutting the current frequency range
        array_band_cut, frequency_band_list, ifmin, ifmax = \
            specify_frequency_range(array, frequency_list, freq_start, freq_stop)

        # Plot dedispersed data
        make_2d_plot(array_band_cut, result_path + '/12-' + str(band + 1) + ' - Dedispersed data for subband ' +
                     str(round(freq_start, 3)) + '-' + str(round(freq_stop, 3)) + ' MHz.png',
                     frequency_band_list, colormap, 'Dedispersed pulsar pulse in frequency range ' +
                     str(round(freq_start, 3)) + '-' + str(round(freq_stop, 3)) + ' MHz \n File: ' + filename,
                     custom_dpi)

        # ***   Matrix sum in one dimension   ***
        for k in range(len(frequency_band_list)):
            array_band_cut[k, :] = array_band_cut[k, :] - np.mean(array_band_cut[k, begin_index: end_index])
        integr_band_profile = np.sum(array_band_cut, axis=0)

        # Calculations of SNR
        noise_in_band = integr_band_profile[begin_index: end_index]
        integr_band_profile = (integr_band_profile - np.mean(noise_in_band)) / np.std(noise_in_band)

        #  Rolling the pulse to the center of the plot
        integr_band_profile = np.roll(integr_band_profile, roll_number)  # Roll to make the pulse in the center

        #  Plotting and saving the SNR curve
        make_1d_plot(integr_band_profile, result_path + '/14-' + str(band + 1) + ' - SNR for subband ' +
                     str(round(freq_start, 3)) + '-' + str(round(freq_stop, 3)) + ' MHz.png',
                     'Averaged profile', 'Pulsar average pulse profile in range ' +
                     str(round(freq_start, 3)) + '-' + str(round(freq_stop, 3)) + ' MHz  \n File: ' + filename,
                     'SNR', 'Samples in pulsar period', custom_dpi)

        profiles_var_in_band[band, :] = integr_band_profile
        band_frequencies[band, 0] = freq_start
        band_frequencies[band, 1] = freq_stop
        snr_max_in_band[band] = np.max(integr_band_profile)
        band_freq_name[band] = str(round(freq_start, 3)) + '-' + str(round(freq_stop, 3))
        snr_per_mhz_in_band[band] = (snr_max_in_band[band] / (band_frequencies[band, 1] - band_frequencies[band, 0]))

    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    for band in range(no_of_freq_bands):
        plt.plot(profiles_var_in_band[band, :], label=str(round(band_frequencies[band, 0], 3)) + ' - ' +
                                                      str(round(band_frequencies[band, 1], 3)) + ' MHz')
    plt.title('All subbands profiles on single figure \n File: ' + filename,
              fontsize=10, fontweight='bold', style='italic', y=1.025)
    plt.legend(loc='upper right', fontsize=10)
    plt.ylabel('SNR', fontsize=10, fontweight='bold')
    plt.xlabel('Samples in pulsar period', fontsize=10, fontweight='bold')
    plt.yticks(fontsize=8, fontweight='bold')
    plt.xticks(fontsize=8, fontweight='bold')
    pylab.savefig(result_path + '/16.1 - SNR of pulse profile in subbands.png', bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')

    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    for band in range(no_of_freq_bands):
        plt.plot(profiles_var_in_band[band, :] / np.max(profiles_var_in_band[band, :]),
                 label=str(round(band_frequencies[band, 0], 3)) + ' - ' +
                       str(round(band_frequencies[band, 1], 3)) + ' MHz')
    plt.title('All subbands normalized profiles on single figure \n File: ' + filename,
              fontsize=10, fontweight='bold', style='italic', y=1.025)
    plt.legend(loc='upper right', fontsize=10)
    plt.ylabel('Normalized SNR', fontsize=10, fontweight='bold')
    plt.xlabel('Samples in pulsar period', fontsize=10, fontweight='bold')
    plt.yticks(fontsize=8, fontweight='bold')
    plt.xticks(fontsize=8, fontweight='bold')
    pylab.savefig(result_path + '/16.2 - Normalized SNR of pulse profile in subbands.png',
                  bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')

    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    for band in range(no_of_freq_bands):
        plt.plot(profiles_var_in_band[band, :] - np.max(profiles_var_in_band[band, :]),
                 label=str(round(band_frequencies[band, 0], 3)) + ' - ' +
                       str(round(band_frequencies[band, 1], 3)) + ' MHz')
    plt.title('All subbands profiles with maximums at the same level \n File: ' + filename,
              fontsize=10, fontweight='bold', style='italic', y=1.025)
    plt.legend(loc='upper right', fontsize=10)
    plt.ylabel('SNR', fontsize=10, fontweight='bold')
    plt.xlabel('Samples in pulsar period', fontsize=10, fontweight='bold')
    plt.yticks(fontsize=8, fontweight='bold')
    plt.xticks(fontsize=8, fontweight='bold')
    pylab.savefig(result_path + '/16.3 - SNR of pulse profile with same maximum levels in subbands.png',
                  bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')

    fig, ax = plt.subplots(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    plt.plot(snr_max_in_band, label='SNR vs. frequency band')
    plt.plot(snr_max_in_band, 'ro', markersize=3)
    plt.title('SNR values in subbands of analysis  \n File: ' + filename,
              fontsize=10, fontweight='bold', style='italic', y=1.025)
    plt.legend(loc='upper left', fontsize=10)
    plt.ylabel('SNR', fontsize=10, fontweight='bold')
    plt.xlabel('Bands of analysis, MHz', fontsize=10, fontweight='bold')
    plt.yticks(fontsize=8, fontweight='bold')
    plt.xticks(fontsize=8, fontweight='bold', rotation=0)
    a = ax.get_xticks().tolist()
    for i in range(len(a)-1):
        k = int(a[i])
        a[i] = band_freq_name[k]
    ticks_loc = ax.get_xticks().tolist()                         # <---- Added to suppress warning
    ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))  # <---- Added to suppress warning
    ax.set_xticklabels(a)
    pylab.savefig(result_path + '/16.4 - SNR value vs. subbands.png', bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')

    fig, ax = plt.subplots(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    plt.plot(snr_per_mhz_in_band, label='SNR / MHz vs. frequency band')
    plt.plot(snr_per_mhz_in_band, 'ro', markersize=3)
    plt.title('SNR per MHz values in subbands of analysis  \n File: '+filename,
              fontsize=10, fontweight='bold', style='italic', y=1.025)
    plt.legend(loc='upper left', fontsize=10)
    plt.ylabel('SNR / MHz', fontsize=10, fontweight='bold')
    plt.xlabel('Bands of analysis, MHz', fontsize=10, fontweight='bold')
    plt.yticks(fontsize=8, fontweight='bold')
    plt.xticks(fontsize=8, fontweight='bold', rotation=0)
    a = ax.get_xticks().tolist()
    for i in range(len(a)-1):
        k = int(a[i])
        a[i] = band_freq_name[k]
    ticks_loc = ax.get_xticks().tolist()                         # <---- Added to suppress warning
    ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))  # <---- Added to suppress warning
    ax.set_xticklabels(a)
    pylab.savefig(result_path + '/16.5 - SNR per MHz value vs. subbands.png', bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')

    return


def average_profile_analysis(type, matrix, initial_matrix, filename, result_path, dm_already_compensated,
                             frequency_list, time_res, scale_factor, samples_per_period,
                             pulsar_dm, no_of_dm_steps, pulsar_period, save_intermediate_data,
                             average_channel_num, record_date_time, pulsar_name,
                             software_version, current_time, current_date, df_filename, df_obs_place,
                             df_description, receiver_mode, df_system_name, obs_duration):

    """
    Analyze average pulsar pulse profile with its time-frequency data
    There are 2 modes (types): 'first' (initial DM) or 'final'  (optimal DM)
    Args:
        type: 'first' or 'final'
        matrix:
        initial_matrix:
        filename:
        result_path:
        freq_num:
        fmin:
        fmax:
        df:
        frequency_list:
        time_res:
        samples_per_period:
        pulsar_dm:
        no_of_dm_steps:
        pulsar_period:
        save_intermediate_data:
        average_channel_num:
        record_date_time:
        pulsar_name:
        software_version:
        current_time:
        current_date:
        df_filename:
        df_obs_place:
        df_description:
        receiver_mode:
        df_system_name:

    Returns:
        dm_optimal:
    """

    fig_number = '0' if type == 'first' else '1'
    dm_type = 'initial' if type == 'first' else 'optimal'
    freq_num = len(frequency_list)
    df = frequency_list[1] - frequency_list[0]

    # Find pulsar parameters from catalogue
    pulsar_ra, pulsar_dec, catalogue_pulsar_dm, p_bar = catalogue_pulsar(pulsar_name)
    #  Calculation of shift in pixels to compensate dispersion to display on result figure
    shift_param = dm_full_shift_calculate(freq_num, frequency_list[0], frequency_list[-1], df, time_res, pulsar_dm, '')

    # Calculation of maximal time shift to display on result figure
    max_time_shift_cat_dm = time_res * np.abs(shift_param[0])
    del shift_param

    # If target DM delay was compensated by previous processing, skip compensation here
    if not dm_already_compensated:

        #  Calculation of shift in pixels to compensate dispersion
        shift_param = pulsar_dm_shift_calculation_aver_pulse(freq_num, frequency_list[0], frequency_list[-1], df,
                                                             time_res, pulsar_dm, pulsar_period)

        #  Saving shift parameter for dispersion delay compensation vs. frequency to file and plot
        if save_intermediate_data == 1:

            shift_param_txt = open(result_path + '/Shift parameter (' + dm_type + ').txt', "w")
            for i in range(freq_num):
                shift_param_txt.write(str(frequency_list[0] + df * i) + '   ' + str(shift_param[i]) + ' \n')
            shift_param_txt.close()

            make_1d_plot(shift_param, result_path + '/' + fig_number + '3.1 - Shift parameter (' + dm_type + ' DM).png',
                         'Shift parameter', 'Shift parameter', 'Shift parameter', 'Frequency channel number',
                         custom_dpi)

        #  Compensation of dispersion delay
        matrix = pulsar_DM_compensation_with_indices_changes(matrix, shift_param)

    else:
        # Anyway for the final (optimal) DM we need to compensate a difference between optimal and catalog DMs
        if type == 'final':
            delta_optimal_dm = pulsar_dm - catalogue_pulsar_dm

            #  Calculation of shift in pixels to compensate dispersion
            shift_param = pulsar_dm_shift_calculation_aver_pulse(freq_num, frequency_list[0], frequency_list[-1], df,
                                                                 time_res, delta_optimal_dm, pulsar_period)

            #  Compensation of dispersion delay
            matrix = pulsar_DM_compensation_with_indices_changes(matrix, shift_param)

        else:
            delta_optimal_dm = 0

    #  Plot of the data with DM compensation but without data reduction
    if save_intermediate_data == 1:
        make_2d_plot(matrix, result_path + '/' + fig_number + '1.3 - Dedispersed data.png', frequency_list, colormap,
                     'Dedispersed pulsar pulse \n File: ' + filename, custom_dpi)

    #  Integrated over band pulsar profile in time (matrix sum in one dimension)
    integrated_profile = np.sum(matrix, axis=0)

    #  Specifying the noise segment to calculate SNR
    print('\n  * Check the noise segment and close the plot, then enter needed data ')

    import matplotlib
    matplotlib.use('TkAgg')

    plt.figure()
    plt.plot(integrated_profile)
    plt.xlabel('Phase of pulsar period')
    plt.ylabel('Data')
    plt.xticks(fontsize=12)  # To make sure previous functions do not affect text size
    plt.yticks(fontsize=12)  # To make sure previous functions do not affect text size
    if save_intermediate_data == 1:
        pylab.savefig(result_path + '/' + fig_number + '4 - Raw integrated data to find pulse.png',
                      bbox_inches='tight', dpi=250)
    plt.show()
    plt.close('all')

    #  Manual input of the first and last index of noise segment in integrated plot
    begin_index = int(input('\n    First index of noise segment:           '))
    end_index   = int(input('\n    Last index of noise segment:            '))

    #  Mean value extraction from the matrix
    for i in range(freq_num):
        matrix[i, :] = matrix[i, :] - np.mean(matrix[i, begin_index: end_index])

    integrated_profile = np.sum(matrix, axis=0)

    #  Calculation of SNR
    noise = integrated_profile[begin_index: end_index]
    noise_mean = np.mean(noise)
    noise_std = np.std(noise)
    integrated_profile = (integrated_profile - noise_mean) / noise_std

    #  Calculation of number of points to roll the pulse to the centre of the plot
    roll_number = int((len(integrated_profile)/2) - np.argmax(integrated_profile))

    #  Rolling the pulse to the center of the plot
    integrated_profile = np.roll(integrated_profile, roll_number)  # Rolling the vector to make the pulse in the center
    # snr_init_max = np.max(integrated_profile)

    #  Plotting and saving the SNR curve
    make_1d_plot(integrated_profile, result_path + '/' + fig_number + '5 - SNR.png',
                 'Averaged profile for DM = ' + str(round(pulsar_dm, 3)),
                 'Averaged pulse profile in band ' + str(round(frequency_list[0], 3)) + ' - ' +
                 str(round(frequency_list[len(frequency_list)-1], 3)) + ' MHz \n File: ' + filename,
                 'SNR', 'Phase of pulsar period', custom_dpi)

    #   Calculations of DM variation

    if type == 'final' and frequency_band_cut:     # Plot profiles in small frequency bands?
        tmp_array_copy = matrix.copy()

        analysis_in_frequency_bands(tmp_array_copy, frequency_list, frequency_cuts, samples_per_period, result_path,
                                    filename, begin_index, end_index, roll_number)
        del tmp_array_copy

    previous_time = time.time()

    # If DM delay was already compensated in data file, we use zero DM as a center value
    if not dm_already_compensated:

        # Integrated profiles with DM variation calculation (using DM)
        profiles_var_dm, dm_vector = pulsar_dm_variation(initial_matrix, no_of_dm_steps,
                                                         freq_num, frequency_list[0], frequency_list[-1], df,
                                                         time_res, pulsar_period, samples_per_period, pulsar_dm,
                                                         noise_mean, noise_std, begin_index, end_index, dm_var_step,
                                                         roll_number)
    else:

        # Integrated profiles with DM variation calculation (delta_optimal_dm)
        profiles_var_dm, dm_vector = pulsar_dm_variation(initial_matrix, no_of_dm_steps, freq_num,
                                                         frequency_list[0], frequency_list[-1], df,
                                                         time_res, pulsar_period, samples_per_period, delta_optimal_dm,
                                                         noise_mean, noise_std, begin_index, end_index, dm_var_step,
                                                         roll_number)

        dm_vector = dm_vector + pulsar_dm - delta_optimal_dm

    # Find the maximal SNR for current DM
    snr_init_max = np.max(profiles_var_dm[int(no_of_dm_steps / 2) + 1, :])

    # **************************************************************************
    #          Calculation the accuracy of optimal DM determination            *
    # **************************************************************************
    if type == 'final':
        # Profile of maximal SNR for each DM value
        max_profile_var_dm = np.max(profiles_var_dm, axis=1)

        # Index of the optimal DM value in vector
        max_x = np.argmax(max_profile_var_dm)

        # Indexes of optimal DM value with error interval
        indexes = np.where(max_profile_var_dm >= np.max(max_profile_var_dm) * 0.95)
        x_index_min = indexes[0][0] - 1 if indexes[0][0] > 0 else indexes[0][0]  # Min index
        x_index_max = indexes[0][len(indexes[0])-1] + 1 if \
            indexes[0][len(indexes[0])-1] < len(max_profile_var_dm)-1 else indexes[0][len(indexes[0])-1]  # Max index
        diff_max = np.abs(x_index_max - max_x)  # Index error to upper limit
        diff_min = np.abs(x_index_min - max_x)  # Index error to lower limit
        index_error = np.max([diff_max, diff_min])
        dm_determination_error = index_error * dm_var_step
        print('\n\n  Error of optimal DM determination is ', index_error, ' steps, or ',
              dm_determination_error, ' pc / cm3')

        # Figure optimal DM determination error
        rc('font', size=7, weight='bold')
        fig = plt.figure(1, figsize=(10.0, 6.0))
        ax1 = fig.add_subplot(111)
        ax1.plot(dm_vector - pulsar_dm, max_profile_var_dm, label='Max of SNR profile vs. DM')
        ax1.axvline(x=dm_vector[max_x] - pulsar_dm, color='C4', linestyle='-', linewidth=1.0)
        ax1.axvline(x=dm_vector[x_index_min] - pulsar_dm, color='C1', linestyle='-', linewidth=1.0)
        ax1.axvline(x=dm_vector[x_index_max] - pulsar_dm, color='C1', linestyle='-', linewidth=1.0)
        ax1.axhline(y=max_profile_var_dm[max_x] * 0.95,
                    label='Max error = ' + str(np.round(dm_determination_error, 4)) + r' $\mathrm{pc \cdot cm^{-3}}$',
                    color='r', linestyle='-', linewidth=0.5)
        ax1.legend(loc='upper right')
        ax1.set_xlabel(r'$\mathrm{\Delta DM}$', fontsize=7, fontweight='bold')
        ax1.set_ylabel('Max SNR', fontsize=7, fontweight='bold')
        ax2 = ax1.twiny()
        ax2.set_xlabel('DM value', fontsize=7, fontweight='bold')
        ax2.set_xlim(ax1.get_xlim())
        text = ax2.get_xticks().tolist()
        for i in range(len(text)-1):
            k = float(text[i])
            text[i] = k + pulsar_dm

        ticks_loc = ax2.get_xticks().tolist()                           # <---- Added to suppress warning
        ax2.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))    # <---- Added to suppress warning

        ax2.set_xticklabels(np.round(text, 4))
        fig.subplots_adjust(top=0.90)
        fig.suptitle('Maxima of SNR profiles vs. DM variation \n File: ' + filename,
                     fontsize=10, fontweight='bold', style='italic', y=1.025)
        pylab.savefig(result_path + '/' + fig_number + '6 - SNR vs DM.png', bbox_inches='tight', dpi=custom_dpi)
        plt.close('all')

    # **************************************************************************
    #         Averaging data in frequency domain for final figure
    # **************************************************************************
    if type == 'final':
        reduced_array, reduced_frequency_list = averaging_in_frequency(matrix, freq_num, frequency_list,
                                                                       samples_per_period,
                                                                       average_channel_num,
                                                                       roll_number, result_path,
                                                                       filename,
                                                                       save_intermediate_data)

    # **************************************************************************

    now_time = time.time()
    print('\n  DM variation took ', round((now_time - previous_time), 2), 'seconds (',
                                    round((now_time - previous_time)/60, 2), 'min. )')

    # Preparing indexes for showing the maximal SNR value and its coordinates
    dm_steps_real, time_points = profiles_var_dm.shape
    phase_vector = np.linspace(0, 1, num=time_points)
    optimal_dm_indexes = np.unravel_index(np.argmax(profiles_var_dm, axis=None), profiles_var_dm.shape)
    optimal_dm_index = optimal_dm_indexes[0]
    optimal_pulse_phase = optimal_dm_indexes[1]
    max_point_x = phase_vector[optimal_pulse_phase]
    max_point_y = - (dm_vector[optimal_dm_index] - pulsar_dm)
    dm_optimal = round(dm_vector[optimal_dm_index], 5)

    print('\n\n    Initial DM (from file) =               ', pulsar_dm, ' pc / cm3')
    print('    Optimal DM =                           ', dm_optimal, ' pc / cm3  \n')
    print('    SNR for current DM =                   ', round(snr_init_max, 3))
    # print('    SNR averaged in time for initial DM  = ', round(SNRinitDMtimeAver, 3), ' \n')

    # Saving integrated profiles with DM variation calculation to TXT file
    if save_intermediate_data == 1 and type == 'final':
        dm_var_txt = open(result_path + '/Average profile vs DM 2D (' + dm_type + ' DM).txt', "w")
        for step in range(dm_steps_real-1):
            dm_var_txt.write(''.join(format(dm_vector[step], "8.5f")) +
                             '   '.join(format(profiles_var_dm[step, k], "12.5f") for k in range(time_points)) + ' \n')
        dm_var_txt.close()

    # Making figure
    rc('font', size=7, weight='bold')
    fig = plt.figure(1, figsize=(10.0, 6.0))
    ax1 = fig.add_subplot(111)
    fig.subplots_adjust(left=None, bottom=None, right=None, top=0.86, wspace=None, hspace=None)
    im1 = ax1.imshow(np.flipud(profiles_var_dm), aspect='auto',
                     vmin=np.min(profiles_var_dm), vmax=np.max(profiles_var_dm),
                     extent=[0, 1, dm_vector[0] - pulsar_dm, dm_vector[no_of_dm_steps-1] - pulsar_dm], cmap=colormap)
    ax1.set_title('Pulse profile vs DM in band ' + str(round(frequency_list[0], 3)) +
                  ' - ' + str(round(frequency_list[len(frequency_list)-1], 3)) + ' MHz \n File: ' +
                  filename, fontweight='bold', y=1.025)
    ax2 = ax1.twinx()
    ax1.yaxis.set_label_coords(-0.04, 1.01)
    ax2.yaxis.set_label_coords(1.04, 1.03)
    ax1.set_xlabel('Phase of pulsar period', fontsize=7, fontweight='bold')
    ax2.set_ylim(ax1.get_ylim())
    text = ax2.get_yticks().tolist()
    for t in range(len(text)-1):
        k = float(text[t])
        text[t] = pulsar_dm + k

    ticks_loc = ax2.get_yticks().tolist()  # <---- Added to suppress warning
    ax2.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))  # <---- Added to suppress warning

    ax2.set_yticklabels(np.round(text, 4))
    fig.colorbar(im1, ax=ax1, pad=0.1)
    fig.text(0.76, 0.89, 'Current SNR \n    ' + str(round(snr_init_max, 3)),
             fontsize=7, fontweight='bold', transform=plt.gcf().transFigure)
    fig.text(0.75, 0.05, '    Current DM  \n' + str(round(pulsar_dm, 4)) + r' $\mathrm{pc \cdot cm^{-3}}$',
             fontsize=7, fontweight='bold', transform=plt.gcf().transFigure)

    ax1.set_ylabel(r'$\mathrm{\Delta DM}$', rotation=0)
    ax2.set_ylabel('DM', rotation=0, fontsize=7, fontweight='bold')

    pylab.savefig(result_path + '/' + fig_number + '8 - SNR vs DM.png', bbox_inches='tight', dpi=custom_dpi)

    ax1.axhline(y=0, color='r', linestyle='-', linewidth=0.4)
    ax1.axvline(x=0.5 + (0.5/samples_per_period), color='r', linestyle='-', linewidth=0.4)
    ax1.plot(max_point_x, - max_point_y, marker='o', markersize=1.5, color='chartreuse')
    pylab.savefig(result_path + '/' + fig_number + '7 - SNR vs DM.png', bbox_inches='tight', dpi=custom_dpi)
    if type == 'first':
        plt.show()
    plt.close('all')

    if type == 'final':
        # Calculating pulsar visible period for particular observation time and julian day of observation
        p_visible, jd = pulsar_visible_period(pulsar_name, record_date_time, print_or_not=False)

        # Final figure with full information
        fig = plt.figure(constrained_layout=True, figsize=(12.0, 6.75))
        gs = GridSpec(2, 3, figure=fig)
        rc('font', size=7, weight='bold')

        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(integrated_profile)
        ax1.set_xlim(xmin=0, xmax=samples_per_period)
        ax1.set_ylabel(r'$\mathrm{T_{pulsar}\, /\, T_{sys}}$', fontsize=7, fontweight='bold')
        ax1.set_xlabel('Phase of pulsar period in samples', fontsize=7, fontweight='bold')
        ax1.set_title('Average profile in band', fontsize=8, fontweight='bold')

        ax2 = fig.add_subplot(gs[1, 0])  # [1, :-1]
        ax2.imshow(np.flipud(reduced_array), aspect='auto',
                   extent=[0, 1, reduced_frequency_list[0], reduced_frequency_list[-1]], cmap=colormap)
        # vmin=np.min(reduced_array), vmax=np.max(reduced_array)/10,
        ax2.set_ylabel('Frequency, MHz', fontsize=7, fontweight='bold')
        ax2.set_xlabel('Phase of pulsar period', fontsize=7, fontweight='bold')
        ax2.set_title('Pulse profiles in ' + str(np.round(reduced_frequency_list[1] - reduced_frequency_list[0], 3)) +
                      ' MHz bands', fontsize=8, fontweight='bold')

        ax3 = fig.add_subplot(gs[0:, 1])
        im3 = ax3.imshow(np.flipud(profiles_var_dm), aspect='auto',
                         vmin=np.min(profiles_var_dm), vmax=np.max(profiles_var_dm),
                         extent=[0, 1, dm_vector[0] - pulsar_dm, dm_vector[no_of_dm_steps - 1] - pulsar_dm],
                         cmap=colormap)
        ax3.set_ylabel(r'$\mathrm{\Delta DM, pc \cdot cm^{-3}}$')
        ax3.set_xlabel('Phase of pulsar period', fontsize=7, fontweight='bold')
        ax3.set_title('Pulse profile vs DM', fontsize=8, fontweight='bold')
        fig.colorbar(im3, ax=ax3, aspect=50, pad=0.001)

        ax4 = fig.add_subplot(gs[0:, -1])
        ax4.axis('off')

        fig.suptitle('Pulsar ' + pulsar_name + ' in band ' + str(round(frequency_list[0], 1)) + ' - ' +
                     str(round(frequency_list[-1], 1)) + ' MHz \n File: ' + filename, fontsize=10, fontweight='bold')
        fig.text(0.03, 0.960, pulsar_name + '\n' + str(record_date_time[:10]),
                 fontsize=10, transform=plt.gcf().transFigure)

        fig.text(0.72, 0.880, 'Pulsar name: ' + pulsar_name,
                 fontsize=10, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.845, r'$\mathrm{T_{pulsar}\, /\, T_{sys}}:~$' + str(round(snr_init_max, 3)),
                 fontsize=10, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.810, 'DM: ' + str(round(pulsar_dm, 4)) + r' $\mathrm{\pm}$ ' +
                 str(np.round(dm_determination_error, 4)) + r' $\mathrm{pc \cdot cm^{-3}}$',
                 fontsize=10, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.775, 'Date: ' + str(record_date_time[:10]),
                 fontsize=10, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.740, 'Start time: ' + str(record_date_time[11:19]) + ' UTC',
                 fontsize=10, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.705, 'Duration: ' + str(obs_duration).split('.')[0],
                 fontsize=10, fontweight='bold', transform=plt.gcf().transFigure)

        fig.text(0.72, 0.640, 'Time shift in range: ' + str(np.round(max_time_shift_cat_dm, 3)) + ' s.',
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.610, 'Julian day: ' + str(jd),
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.580, 'Data time resolution: ' + str(np.round(time_res * 1000 * scale_factor, 4)) + ' ms.',
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.550, 'Time resolution scaled: ' + str(np.round(time_res * 1000, 4)) + ' ms.',
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)

        fig.text(0.72, 0.520, 'Number of samples per period: ' + str(samples_per_period),
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.490, 'Period from file: ' + str(pulsar_period) + ' s.',
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.460, 'Visible period:    ' + str(p_visible) + ' s.',
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)

        fig.text(0.72, 0.430, 'Catalogue Pbar: ' + str(p_bar) + ' s.',
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)

        fig.text(0.72, 0.400, 'Catalogue DM: ' + str(catalogue_pulsar_dm) + r' $\mathrm{pc \cdot cm^{-3}}$',
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.370, r'$\mathrm{RA_{J2000}}: $' + pulsar_ra.replace('h', 'h ').replace('m', 'm '),
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.340, r'$\mathrm{DEC_{J2000}}: $' + pulsar_dec.replace('d', r'$^\circ$ ').replace('m', 'm '),
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)

        fig.text(0.72, 0.310, 'First data file name: ' + df_filename,
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.280, 'Receiver mode: ' + str(receiver_mode),
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.250, 'Receiver ID: ' + str(df_system_name),
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.220, 'Observation place: ', fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.190, df_obs_place, fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.160, 'Observation description: ',
                 fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)

        # If description is longer then 42 symbols, symbols after 41 will be moved to the next line
        if len(df_description) > 41:
            desc_first_line = df_description[0:41]
            desc_second_line = df_description[41:]
        else:
            desc_first_line = df_description
            desc_second_line = ''

        fig.text(0.72, 0.130, desc_first_line, fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)
        fig.text(0.72, 0.100, desc_second_line, fontsize=9, fontweight='bold', transform=plt.gcf().transFigure)

        fig.text(0.85, -0.015, 'Processed ' + current_date + ' at ' + current_time,
                 fontsize=6, transform=plt.gcf().transFigure)
        fig.text(0.02, -0.015, 'Software version: ' + software_version + ', yerin.serge@gmail.com, IRA NASU',
                 fontsize=6, transform=plt.gcf().transFigure)

        pylab.savefig(result_path + '/' + filename[:-4] + ' result.png', bbox_inches='tight', dpi=custom_dpi)
        plt.show()
        plt.close('all')

    return dm_optimal


def smd_integrated_pulses_analyzer(source_path, result_path, filename, pulsar_name, scale_factor,
                                   dm_already_compensated, auto_optimal_dm_search,
                                   no_of_dm_steps, dm_var_step, cleaning_switch, rfi_std_const,
                                   save_intermediate_data, average_channel_num, aver_time_points_num,
                                   frequency_band_cut, specify_freq_range, frequency_cuts, colormap,
                                   custom_dpi, freq_start_array, freq_stop_array):
    """

    Args:
        source_path:
        result_path:
        filename:
        pulsar_name:
        scale_factor:
        dm_already_compensated:
        auto_optimal_dm_search:
        no_of_dm_steps:
        dm_var_step:
        cleaning_switch:
        rfi_std_const:
        save_intermediate_data:
        average_channel_num:
        aver_time_points_num:
        frequency_band_cut:
        specify_freq_range:
        frequency_cuts:
        colormap:
        custom_dpi:
        freq_start_array:
        freq_stop_array:

    Returns:

    """

    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")
    print(' Today is ', current_date, ' time is ', current_time, ' \n')

    filepath = source_path + filename
    
    pulsar_ra, pulsar_dec, pulsar_dm, p_bar = catalogue_pulsar(pulsar_name)
    
    # **************************************************************
    #  ***           Open datafile and read data                 ***
    # **************************************************************

    smd_filesize = os.stat(filepath).st_size       # Size of file
    print(' File size: ', round(smd_filesize/1024/1024, 6), ' Mb')
    
    # *** Creating a folder where all pictures and results will be stored (if it doesn't exist) ***
    result_path = result_path + 'SMD_results_' + filename
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    
    # Jumping to the end of the file to read the data file header with parameters of data record
    
    if filename[0:3] == 'ADR':
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description, clc_freq, df_creation_time_utc,
            receiver_mode, adr_mode, sum_diff_mode, n_avr, time_res, fmin, fmax, df, frequency_list, fft_size,
            s_line, width, block_size] = file_header_adr_read_old(filepath, smd_filesize - 1024 - 131096, 1)
    
        record_date_time_dt = datetime(int('20' + df_filename[1:3]), int(df_filename[3:5]), int(df_filename[5:7]),
                                       int(df_creation_time_utc[0:2]), int(df_creation_time_utc[3:5]),
                                       int(df_creation_time_utc[6:8]), int(df_creation_time_utc[9:12]) * 1000)
        record_date_time = str(record_date_time_dt)

    elif filename[0:3] == 'DSP':
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description, clc_freq, df_creation_time_utc,
            sp_in_file, receiver_mode, mode, n_avr, time_res, fmin, fmax, df, frequency_list,
            fft_size, block_size] = file_header_jds_read(filepath, smd_filesize - 1024, 1)

        record_date_time_dt = datetime(int('20' + df_filename[5:7]), int(df_filename[3:5]), int(df_filename[1:3]),
                                       int(df_creation_time_utc[11:13]), int(df_creation_time_utc[14:16]),
                                       int(df_creation_time_utc[17:19]), 0)
        record_date_time = str(record_date_time_dt)
    
    else:
        sys.exit('\n\n  Unidentified initial format! Program stopped.')

    time_res = time_res / scale_factor  # Scale the time resolution if it was scaled during pulse folding
    freq_num = len(frequency_list)  # Just the number of frequencies
    
    file = open(filepath, 'rb')
    
    # Reading pulsar period and number of samples per period
    pulsar_period = struct.unpack('d', file.read(8))[0]
    samples_per_period = struct.unpack('h', file.read(2))[0]

    file.seek(12)   # Jump to 12 byte of the file, where pulse spectra array begins
    initial_pulse_array = np.fromfile(file, dtype='f4', count=samples_per_period * freq_num)
    initial_pulse_array = np.reshape(initial_pulse_array, [samples_per_period, freq_num])
    initial_pulse_array = initial_pulse_array.transpose()
    file.close()

    print('\n  * Parameters of analysis: \n')
    print(' Path to folder:  ', source_path, '\n')
    print(' File name:  ', filename, '\n')
    print(' Number of DM analysis steps:         ', no_of_dm_steps)
    print(' Step of DM analysis:                 ', dm_var_step)
    print(' Save intermediate data?              ', save_intermediate_data)
    print(' Number of samples in time:           ', samples_per_period)
    print(' Time resolution (scaled):            ', time_res, ' s.')
    print(' Number of time points to average:    ', aver_time_points_num)
    print(' Number of frequency channels:        ', freq_num)
    print(' Number of channels to average:       ', average_channel_num)
    print(' Make cuts of frequency bands?        ', frequency_band_cut)
    print(' Specify particular frequency range?  ', specify_freq_range)
    print(' Frequencies to cut the range:        ', frequency_cuts)
    print(' Color map:                           ', colormap)
    print(' DPI of plots:                        ', custom_dpi)
    print(' Lowest frequency of the band:        ', freq_start_array)
    print(' Highest frequency of the band:       ', freq_stop_array)
    print(' Pulsar period from file?             ', pulsar_period, ' s')
    print(' Dispersion measure from catalogue:   ', pulsar_dm, ' pc / cm3 \n')
    print(' Average pulse dynamic spectrum shape:', initial_pulse_array.shape)
    
    # **************************************************************
    #  ***   Calculations and figures plotting for specified DM  ***
    # **************************************************************
    
    print('\n  * Calculations and figures... \n')
    
    # Cutting the array inside frequency range specified by user
    if specify_freq_range:
        frequency_list, initial_pulse_array, freq_num, fmin, fmax = \
            choose_frequency_range(frequency_list, initial_pulse_array, freq_start_array, freq_stop_array,
                                   freq_num, fmin, fmax)
    
    # To save initial matrix for further processing with the same name with or without cut of frequencies
    copied_pulse_array = initial_pulse_array.copy()

    if save_intermediate_data == 1:

        # Plot average time and frequency profiles to examine RFI levels
        plot_average_profiles(copied_pulse_array, 'Raw', filename, result_path, custom_dpi)

        # Plot initial average pulse
        make_2d_plot(copied_pulse_array, result_path + '/01.1 - Raw data.png', frequency_list,
                     colormap, 'Raw' + ' pulsar pulse \n File: ' + filename, custom_dpi)
    
    # Cleaning data if necessary
    if cleaning_switch == 1:
        copied_pulse_array, mask = simple_mask_clean(np.rot90(copied_pulse_array), rfi_std_const)
        copied_pulse_array = np.rot90(copied_pulse_array, 3)
    
        # Plotting averaged profiles of initial cleaned data
        if save_intermediate_data == 1:

            # Plot average time and frequency profiles to examine RFI levels after cleaning
            plot_average_profiles(copied_pulse_array, 'Cleaned', filename, result_path, custom_dpi)

            # Plot cleaned average pulse
            make_2d_plot(copied_pulse_array, result_path + '/01.2 - Cleaned data.png',
                         frequency_list, colormap, 'Cleaned' + ' pulsar pulse \n File: ' + filename, custom_dpi)

            # Plot mask for pulse cleaning
            make_2d_plot(mask.transpose(), result_path + '/01.0 - RFI cleaning mask.png', frequency_list, colormap,
                         'Mask \n File: ' + filename, custom_dpi)
    
        del mask

    # Find observation time limits if the timeline file exists near the SMD file
    obs_start_time, obs_stop_time, obs_duration = check_duration_of_dat_file(source_path, filename[5:])
    
    # *******************************************************************************
    #  ***                            Find optimal DM                             ***
    # *******************************************************************************

    if auto_optimal_dm_search:

        pulsar_dm = average_profile_analysis('first', copied_pulse_array, initial_pulse_array, filename, result_path,
                                             dm_already_compensated, frequency_list,
                                             time_res, scale_factor, samples_per_period, pulsar_dm, no_of_dm_steps,
                                             pulsar_period, save_intermediate_data, average_channel_num,
                                             record_date_time, pulsar_name, software_version,
                                             current_time, current_date, df_filename, df_obs_place, df_description,
                                             receiver_mode, df_system_name, obs_duration)

    # *******************************************************************************
    #  ***                      Analyze data with optimal DM                      ***
    # *******************************************************************************

    pulsar_dm = average_profile_analysis('final', copied_pulse_array, initial_pulse_array, filename, result_path,
                                         dm_already_compensated, frequency_list, time_res, scale_factor,
                                         samples_per_period, pulsar_dm, no_of_dm_steps, pulsar_period,
                                         save_intermediate_data, average_channel_num, record_date_time, pulsar_name,
                                         software_version, current_time, current_date, df_filename, df_obs_place,
                                         df_description, receiver_mode, df_system_name, obs_duration)

    '''
    # Make the rolling of the data to make noise interval at the beginning
    # ***   Calculation of number of points to roll the pulse   ***
    roll_number = int((len(integrated_profile)*9/10) - np.argmax(integrated_profile))
    
    # ***   Rolling the pulse to the center of the plot  ***
    integrated_profile = np.roll(integrated_profile, roll_number) # Rolling the vector to make the pulse in the center
    '''
    return 


# ###############################################################################
# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************

if __name__ == '__main__':

    print('\n\n\n\n\n\n\n\n   **************************************************************')
    print('   *    ', software_name, ' v.', software_version, '     *      (c) YeS 2019')
    print('   ************************************************************** \n\n\n')

    smd_integrated_pulses_analyzer(source_path, result_path, filename, pulsar_name, scale_factor,
                                   dm_already_compensated, auto_optimal_dm_search, no_of_dm_steps, dm_var_step,
                                   cleaning_switch, rfi_std_const, save_intermediate_data, average_channel_num,
                                   aver_time_points_num, frequency_band_cut, specify_freq_range, frequency_cuts,
                                   colormap, custom_dpi, freq_start_array, freq_stop_array)

    print('\n\n       *** Program has finished! ***   \n\n')
