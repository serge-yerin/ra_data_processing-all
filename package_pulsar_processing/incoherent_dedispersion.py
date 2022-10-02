# Python3
software_version = '2022.06.08'
software_name = 'Pulsar single pulses processing pipeline'
# Program intended to read and show individual pulses of pulsars from DAT files
# *******************************************************************************
#                     M A N U A L    P A R A M E T E R S                        *
# *******************************************************************************
# Path to data files
common_path = 'e:/RA_DATA_RESULTS/Transient_search_DSP_spectra_pulsar_UTR2_B0950+08/'

# DAT file to be analyzed:
filename = 'Transient_DM_2.472_C250122_214003.jds_Data_chA.dat'  # 'E220213_201439.jds_Data_chA.dat'

source_name = 'Transient'  # 'B0809+74'  # 'B1919+21' #'B0809+74' #'B1133+16' #  'B1604-00' 'B0950+08'

average_const = 512            # Number of frequency channels to appear in result picture
profile_pic_min = -0.15        # Minimum limit of profile picture
profile_pic_max = 0.55         # Maximum limit of profile picture

current_add_dm = 0.1
batch_factor = 10

SpecFreqRange = 0              # Specify particular frequency range (1) or whole range (0)
freqStart = 2.0                # Lower frequency of dynamic spectrum (MHz)
freqStop = 8.0                 # Higher frequency of dynamic spectrum (MHz)

save_profile_txt = True        # Save profile data to TXT file?
save_compensated_data = True   # Save data with compensated DM to DAT file?
custom_dpi = 300               # Resolution of images of dynamic spectra
colormap = 'Greys'             # Colormap of images of dynamic spectra ('jet' or 'Greys')
# *******************************************************************************

# *******************************************************************************
#                     I M P O R T   L I B R A R I E S                           *
# *******************************************************************************
import os
import sys
import time
import pylab
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker   # <---- Added to suppress warning
from os import path
from matplotlib import rc
from progress.bar import IncrementalBar
import matplotlib
matplotlib.use('agg')

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_ra_data_processing.f_spectra_normalization import normalization_lin
from package_ra_data_processing.average_some_lines_of_array import average_some_lines_of_array
from package_ra_data_files_formats.read_file_header_adr import file_header_adr_read
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
from package_ra_data_files_formats.specify_frequency_range import specify_frequency_range
from package_ra_data_files_formats.f_jds_header_new_channels_numbers import jds_header_new_channels_numbers
from package_pulsar_processing.pulsar_DM_full_shift_calculation import DM_full_shift_calc
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes
from package_pulsar_processing.pulsar_pulses_time_profile_FFT import pulsar_pulses_time_profile_FFT
from package_astronomy.catalogue_pulsar import catalogue_pulsar

from package_pulsar_processing.pulsar_incoherent_dedispersion import plot_integrated_profile_and_spectra
# from package_plot_formats.plot_formats_for_pulsars import plot_pulse_profile_and_spectra

# *******************************************************************************
#                              F U N C T I O N S                                *
# *******************************************************************************


def incoherent_dedispersion(common_path, filename, current_add_dm, source_name, batch_factor, average_const,
                            profile_pic_min, profile_pic_max, SpecFreqRange, freqStart, freqStop, save_profile_txt,
                            save_compensated_data, custom_dpi, colormap,
                            start_dm=0, use_mask_file=False, result_path=''):

    """
    Makes incoherent compensation of time delays in each frequency channel with its shift
    It assumes we obtain raw dat files from ADR or JDS readers where for JDS the last channels are not deleted
    """

    # a_previous_time = time.time()
    # a_current_time = time.strftime("%H:%M:%S")
    # a_current_date = time.strftime("%d.%m.%Y")

    # Removing old DM from file name and updating it to current value
    if 'DM_' in filename:
        part_after_dm = filename.split('DM_')[1]
        prev_dm_str = part_after_dm.split('_')[0]
        prev_dm = np.float32(prev_dm_str)
        new_dm = prev_dm + current_add_dm
        new_filename = filename.split('DM_'+prev_dm_str)[0] + 'DM_' + str(np.round(new_dm, 6)) + \
                       filename.split('DM_'+prev_dm_str)[1]
    else:
        new_filename = 'DM_' + str(np.round(current_add_dm + start_dm, 6)) + '_' + filename
        prev_dm = 0

    # rc('font', size=6, weight='bold')  # -----------------------------------------------------------
    data_filepath = common_path + filename

    # # *** Creating a folder where all pictures and results will be stored (if it doesn't exist) ***
    # newpath = result_path + source_name + '_' + new_filename[:-4]
    # if not os.path.exists(newpath):
    #     os.makedirs(newpath)

    # Path to timeline file to be analyzed:
    time_line_file_name = common_path + filename.split('_Data_')[0] + '_Timeline.txt'

    if save_profile_txt > 0:
        # *** Creating a name for long timeline TXT file ***
        profile_file_name = common_path + new_filename[:-4] + '_time_profile.txt'
        profile_txt_file = open(profile_file_name, 'w')  # Open and close to delete the file with the same name
        profile_txt_file.close()

    # *** Opening DAT datafile to check the initial file type ***
    file = open(data_filepath, 'rb')
    df_filename = file.read(32).decode('utf-8').rstrip('\x00')            # Initial data file name
    file.close()

    receiver_type = df_filename[-4:]

    # Reading file header to obtain main parameters of the file
    if receiver_type == '.adr':
        [time_res, fmin, fmax, df, frequency_list,
            fft_size, clc_freq, mode] = file_header_adr_read(data_filepath, 0, False)

    elif receiver_type == '.jds':
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description, clc_freq, df_creation_time_utc, 
            sp_in_file, receiver_mode, mode, n_avr, time_res, fmin, fmax, df, frequency_list, fft_size,
            data_block_size] = file_header_jds_read(data_filepath, 0, False)
    else:
        sys.exit(' Error! Unknown data type!')

    # Manually set frequencies for two channels mode
    if int(clc_freq / 1000000) == 33:
        # fft_size = 8192
        fmin = 16.5
        fmax = 33.0
        frequency_list = np.linspace(fmin, fmax, fft_size)

    # Number of spectra in the file   #   file size - 1024 bytes of header
    dat_sp_in_file = int(((df_filesize - 1024) / (len(frequency_list) * 8)))

    # ************************************************************************************
    #                             R E A D I N G   D A T A                                *
    # ************************************************************************************

    # Timeline file reading
    timeline, dt_timeline = time_line_file_reader(time_line_file_name)

    # Selecting the frequency range of data to be analyzed
    if SpecFreqRange == 1:
        A = []
        B = []
        for i in range(len(frequency_list)):
            A.append(abs(frequency_list[i] - freqStart))
            B.append(abs(frequency_list[i] - freqStop))
        ifmin = A.index(min(A))
        ifmax = B.index(min(B))
        shift_vector = DM_full_shift_calc(ifmax - ifmin, frequency_list[ifmin], frequency_list[ifmax], df / pow(10, 6),
                                          time_res, current_add_dm, receiver_type)
        print(' Number of frequency channels:  ', ifmax - ifmin)

    else:
        shift_vector = DM_full_shift_calc(len(frequency_list) - 4, fmin, fmax, df / pow(10, 6),
                                          time_res, current_add_dm, receiver_type)
        print(' Number of frequency channels:  ', len(frequency_list) - 4)
        ifmin = int(fmin * 1e6 / df)
        ifmax = int(fmax * 1e6 / df) - 4

    if save_compensated_data > 0:
        with open(data_filepath, 'rb') as file:
            file_header = file.read(1024)  # Data file header read

        # Change number of frequency channels in the header
        file_header = jds_header_new_channels_numbers(file_header, ifmin, ifmax)

        # *** Creating a binary file with data for long data storage ***
        new_data_file_name = common_path + new_filename
        new_data_file = open(new_data_file_name, 'wb')
        new_data_file.write(file_header)
        new_data_file.close()

        if use_mask_file:
            new_mask_file_name = common_path + new_filename[:-3] + 'msk'
            new_mask_file = open(new_mask_file_name, 'wb')
            new_mask_file.write(file_header)
            new_mask_file.close()
        del file_header

    # Creating a long timeline TXT file
    new_tl_file_name = common_path + new_filename[:-13] + '_Timeline.txt'
    new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
    new_tl_file.close()

    # Take a maximal shift and multiply to factor to speed up calculations
    max_shift = np.abs(shift_vector[0])
    max_shift = max_shift * batch_factor

    buffer_array = np.zeros((ifmax - ifmin, 2 * max_shift))
    if use_mask_file:
        buffer_msk_array = np.zeros((ifmax - ifmin, 2 * max_shift), dtype=bool)

    num_of_blocks = int(dat_sp_in_file / max_shift)

    print(' Number of spectra in file:     ', dat_sp_in_file)
    print(' Maximal shift is:              ', max_shift, ' pixels ')
    print(' Number of blocks in file:      ', num_of_blocks)
    print(' Source name:                   ', source_name)
    print(' Full dispersion measure:       ', np.round(prev_dm + current_add_dm, 6), ' pc / cm3')
    print(' Start dispersion measure:      ', prev_dm, ' pc / cm3')
    print(' Current add to start DM:       ', np.round(current_add_dm, 6), ' pc / cm3 \n')

    if receiver_type == '.jds':
        num_frequencies_initial = len(frequency_list) - 4

    frequency_list_initial = np.empty_like(frequency_list)
    frequency_list_initial[:] = frequency_list[:]

    dat_file = open(data_filepath, 'rb')
    dat_file.seek(1024)                     # Jumping to 1024 byte from file beginning

    if use_mask_file:
        msk_file = open(data_filepath[:-3] + 'msk', 'rb')
        msk_file.seek(1024)  # Jumping to 1024 byte from file beginning

    bar = IncrementalBar(' Coherent dispersion delay removing: ', max=num_of_blocks,
                         suffix='%(percent)d%%')
    bar.start()

    for block in range(num_of_blocks):   # main loop by number of blocks in file

        # Timeline arrangements:
        fig_time_scale = []
        fig_date_time_scale = []
        for i in range(block * max_shift, (block+1) * max_shift):  # Shows the time of pulse end (at lowest frequency)
            fig_time_scale.append(timeline[i][11:23])
            fig_date_time_scale.append(timeline[i][:])
        # print(' Time: ', fig_time_scale[0], ' - ', fig_time_scale[-1], ', number of points: ', len(fig_time_scale))

        # Data block reading
        if receiver_type == '.jds':
            data = np.fromfile(dat_file, dtype=np.float64, count=(num_frequencies_initial + 4) * max_shift)   # 2
            data = np.reshape(data, [(num_frequencies_initial + 4), max_shift], order='F')  # 2
            data = data[:num_frequencies_initial, :]  # To delete the last channels of DSP data where time is stored

        if use_mask_file:
            mask = np.fromfile(msk_file, dtype=bool, count=(num_frequencies_initial + 4) * max_shift)
            mask = np.reshape(mask, [(num_frequencies_initial + 4), max_shift], order='F')
            mask = mask[:num_frequencies_initial, :]

        # Cutting the array in predefined frequency range
        if SpecFreqRange == 1:
            data, frequency_list, fi_start, fi_stop = specify_frequency_range(data, frequency_list_initial,
                                                                              freqStart, freqStop)
            num_frequencies = len(frequency_list)
        else:
            num_frequencies = num_frequencies_initial  # + 4

        # Normalization of data
        normalization_lin(data, num_frequencies, 1 * max_shift)

        # Dispersion delay removing
        data_space = np.zeros((num_frequencies, 2 * max_shift))
        data_space[:, max_shift:] = data[:, :]
        temp_array = pulsar_DM_compensation_with_indices_changes(data_space, shift_vector)
        del data, data_space

        if use_mask_file:
            mask_space = np.zeros((num_frequencies, 2 * max_shift), dtype=bool)
            mask_space[:, max_shift:] = mask[:, :]
            temp_mask_array = pulsar_DM_compensation_with_indices_changes(mask_space, shift_vector)
            temp_mask_array = np.array(temp_mask_array, dtype=bool)

        # Adding the next data block
        buffer_array += temp_array
        if use_mask_file:
            buffer_msk_array += temp_mask_array

        # Making and filling the array with fully ready data for plotting and saving to a file
        array_compensated_pulsar_dm = buffer_array[:, 0: max_shift]
        if use_mask_file:
            mask_compensated_pulsar_dm = buffer_msk_array[:, 0: max_shift]

        if block > 0:
            # Saving data with compensated pulsar_dm to DAT file
            if save_compensated_data > 0 and block > 0:
                temp_to_write = np.transpose(array_compensated_pulsar_dm).copy(order='C')
                new_data_file = open(new_data_file_name, 'ab')
                new_data_file.write(temp_to_write)
                new_data_file.close()
                del temp_to_write

                if use_mask_file:
                    temp_to_write = np.transpose(mask_compensated_pulsar_dm).copy(order='C')
                    new_mask_file = open(new_mask_file_name, 'ab')
                    new_mask_file.write(temp_to_write)
                    new_mask_file.close()
                    del temp_to_write

            # Saving time data to long timeline file
            with open(new_tl_file_name, 'a') as new_tl_file:
                for i in range(max_shift):
                   new_tl_file.write((fig_date_time_scale[i][:]))  # str

            # Logging the data
            with np.errstate(divide='ignore'):
                array_compensated_pulsar_dm[:, :] = 10 * np.log10(array_compensated_pulsar_dm[:, :])
            array_compensated_pulsar_dm[array_compensated_pulsar_dm == -np.inf] = 0
            array_compensated_pulsar_dm[array_compensated_pulsar_dm == np.nan] = 0
            array_compensated_pulsar_dm[np.isinf(array_compensated_pulsar_dm)] = 0

            # Normalizing log data
            array_compensated_pulsar_dm = array_compensated_pulsar_dm - np.mean(array_compensated_pulsar_dm)

            # Find mean array value with masked noise
            masked_data_raw = np.ma.masked_where(mask_compensated_pulsar_dm, array_compensated_pulsar_dm)
            data_raw_mean = np.mean(masked_data_raw)
            del masked_data_raw

            # Apply as mask to data (change masked data with mean values of data outside mask)
            array_compensated_pulsar_dm = array_compensated_pulsar_dm * np.invert(mask_compensated_pulsar_dm)
            array_compensated_pulsar_dm = array_compensated_pulsar_dm + mask_compensated_pulsar_dm * data_raw_mean

            # Preparing single averaged data profile for figure
            profile = array_compensated_pulsar_dm.mean(axis=0)[:]
            profile = profile - np.mean(profile)

            # Save full profile to TXT file
            if save_profile_txt > 0:
                profile_txt_file = open(profile_file_name, 'a')
                for i in range(len(profile)):
                    profile_txt_file.write(str(profile[i]) + ' \n')
                profile_txt_file.close()

            # # Averaging of the array with pulses for figure
            # averaged_array = average_some_lines_of_array(array_compensated_pulsar_dm, int(num_frequencies/average_const))
            # freq_resolution = (df * int(num_frequencies/average_const)) / 1000.
            # max_time_shift = max_shift * time_res
            #
            # averaged_array = averaged_array - np.mean(averaged_array)

            # plot_integrated_profile_and_spectra(profile, averaged_array, frequency_list, num_frequencies, fig_time_scale,
            #                                     newpath, filename, source_name, pulsar_dm, freq_resolution, time_res,
            #                                     max_time_shift, block, num_of_blocks-1, block,
            #                                     profile_pic_min, profile_pic_max, df_description, colormap,
            #                                     custom_dpi, a_current_date, a_current_time, software_version)

        # Rolling temp_array to put current data first
        buffer_array = np.roll(buffer_array, - max_shift)
        buffer_array[:, max_shift:] = 0
        if use_mask_file:
            buffer_msk_array = np.roll(buffer_msk_array, - max_shift)
            buffer_msk_array[:, max_shift:] = 0

        bar.next()

    bar.finish()
    dat_file.close()

    if not save_compensated_data:
        new_data_file_name = ''

    return new_data_file_name


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    print(' \n\n\n\n\n\n\n\n')
    print('   *****************************************************************')
    print('   *   ', software_name, ' v.', software_version, '   *      (c) YeS 2020')
    print('   ***************************************************************** \n\n\n')

    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")
    print('  Today is ', current_date, ' time is ', current_time, ' \n')

    data_file_name = incoherent_dedispersion(common_path, filename, current_add_dm, source_name, batch_factor,
                                             average_const, profile_pic_min, profile_pic_max, SpecFreqRange,
                                             freqStart, freqStop, save_profile_txt, save_compensated_data, custom_dpi,
                                             colormap, use_mask_file=True)

    print('\n  Dedispersed data stored in:', data_file_name)

    end_time = time.time()    # Time of calculations

    print('\n\n  The program execution lasted for ', round((end_time - start_time), 2), 'seconds (',
                                                     round((end_time - start_time)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', software_name, ' has finished! *** \n\n\n')
