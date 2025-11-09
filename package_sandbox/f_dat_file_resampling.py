

# Not event started - the idea is to make dat file resampling from the function of  pulsar incoherent dedispersion


import os
import sys
import time
import numpy as np
from datetime import timedelta

from os import path
# To change system path to main source_directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_ra_data_files_formats.read_file_header_adr import file_header_adr_read
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader


# def pulsar_incoherent_dedispersion(common_path, filename, pulsar_name, average_const, profile_pic_min, profile_pic_max,
#                                    spec_freq_range, freq_start, freq_stop, save_profile_txt, save_compensated_data,
#                                    custom_dpi, colormap, use_mask_file=False, save_pics=True, source_dm=0,
#                                    result_path='', make_fourier=False, print_or_not=True):
    
def dat_file_resampling(initial_dat_file_path, output_dat_file_path, resampling_in_time, resampling_in_frequency, print_or_not=True):    
    
    """
    Args:
        common_path: path to initial data (str)
        filename: name of file to process (str)
        pulsar_name: name of the pulsar in catalogue (str)
        average_const: average constant - the number of frequency channels to appear in result picture (int)
        profile_pic_min: minimum limit of profile picture (float)
        profile_pic_max: maximum limit of profile picture (float)
        spec_freq_range: do we specify particular frequency range (bool)
        freq_start: start frequency of the specified range (float)
        freq_stop: finish frequency of the specified range (float)
        save_profile_txt:
        save_compensated_data:
        custom_dpi:
        colormap:
        use_mask_file:
        save_pics:
        source_dm:
        result_path:
        make_fourier:
        print_or_not: to print the current operation and file info into terminal

    Returns:
        new_data_file_name
    """


    # Path to timeline file to be analyzed:
    initial_time_line_file_name = initial_dat_file_path[-31:-13] + '_Timeline.txt'
    output_time_line_file_name = output_dat_file_path[-31:-13] + '_Timeline.txt'

    initial_dat_file_path = os.path.normpath(initial_dat_file_path)
    initial_time_line_file_name = os.path.normpath(initial_time_line_file_name)

    output_dat_file_path = os.path.normpath(output_dat_file_path)
    output_time_line_file_name = os.path.normpath(output_time_line_file_name)

    # Opening DAT datafile to check the initial file type

    file = open(initial_dat_file_path, 'rb')
    df_filename = file.read(32).decode('utf-8').rstrip('\x00')            # Initial data file name
    file.close()

    receiver_type = df_filename[-4:]

    # Reading file header to obtain main parameters of the file
    if receiver_type == '.adr':
        [time_res, fmin, fmax, df, frequency_list, fft_size, clc_freq, mode] = file_header_adr_read(initial_dat_file_path, 0, 1)

    elif receiver_type == '.jds':
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description, clc_freq, df_creation_time_utc,
            sp_in_file, receiver_mode, mode, n_avr, time_res, fmin, fmax, df, frequency_list, fft_size,
            data_block_size] = file_header_jds_read(initial_dat_file_path, 0, print_or_not)
    else:
        sys.exit(' Error! Unknown data type!')

    # Number of spectra in the file   #   file size - 1024 bytes of header
    dat_sp_in_file = int((df_filesize - 1024) / (len(frequency_list) * 8))

    print(dat_sp_in_file)

    # ************************************************************************************
    #                             R E A D I N G   D A T A                                *
    # ************************************************************************************

    # Timeline file reading
    timeline, dt_timeline = time_line_file_reader(initial_time_line_file_name)

    # # Selecting the frequency range of data to be analyzed
    # if spec_freq_range:
    #     tmp_list_a = []
    #     tmp_list_b = []
    #     for i in range(len(frequency_list)):
    #         tmp_list_a.append(abs(frequency_list[i] - freq_start))
    #         tmp_list_b.append(abs(frequency_list[i] - freq_stop))
    #     ifmin = tmp_list_a.index(min(tmp_list_a))
    #     ifmax = tmp_list_b.index(min(tmp_list_b))
    #     del tmp_list_a, tmp_list_b

    #     shift_vector = dm_full_shift_calculate(ifmax - ifmin, frequency_list[ifmin], frequency_list[ifmax], df / pow(10, 6),
    #                                            time_res, pulsar_dm, receiver_type)
    #     if print_or_not:
    #         print(' Number of frequency channels:  ', ifmax - ifmin)

    # else:
    #     shift_vector = dm_full_shift_calculate(len(frequency_list) - 4, fmin, fmax, df / pow(10, 6),
    #                                            time_res, pulsar_dm, receiver_type)
    #     if print_or_not:
    #         print(' Number of frequency channels:  ', len(frequency_list) - 4)
        
    #     ifmin = int(np.round(fmin * 1e6 / df))
    #     ifmax = int(np.round(fmax * 1e6 / df)) - 4

    # if save_compensated_data > 0:
    #     with open(data_filepath, 'rb') as file:
    #         file_header = file.read(1024)  # Data file header read

    #     # Change number of frequency channels in the header
    #     file_header = jds_header_new_channels_numbers(file_header, ifmin, ifmax)

    #     # *** Creating a binary file with data for long data storage ***
    #     new_data_file_name = os.path.join(common_path, pulsar_name + '_DM_' +
    #                                       str(np.round(pulsar_dm, 6)) + '_' + filename)
    #     new_data_file = open(new_data_file_name, 'wb')
    #     new_data_file.write(file_header)
    #     new_data_file.close()

    #     if use_mask_file:
    #         new_mask_file_name = os.path.join(common_path, pulsar_name + '_DM_' +
    #                                           str(np.round(pulsar_dm, 6)) + '_' + filename[:-3] + 'msk')
    #         new_mask_file = open(new_mask_file_name, 'wb')
    #         new_mask_file.write(file_header)
    #         new_mask_file.close()
    #     del file_header

    # # *** Creating a name for long timeline TXT file ***
    # data_filename = data_filepath.split(os.sep)[-1]
    # new_tl_file_name = os.path.join(common_path, pulsar_name + '_DM_' + str(np.round(pulsar_dm, 6)) + '_' +
    #                                 data_filename[:-13] + '_Timeline.txt')
    # new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
    # new_tl_file.close()

    # # Maximal shift calculation
    # max_shift = np.abs(shift_vector[0])

    # buffer_array = np.zeros((ifmax - ifmin, 2 * max_shift))
    # if use_mask_file:
    #     buffer_msk_array = np.zeros((ifmax - ifmin, 2 * max_shift), dtype=bool)

    # num_of_blocks = int(dat_sp_in_file / max_shift)

    # if print_or_not:
    #     print(' Number of spectra in file:     ', dat_sp_in_file)
    #     print(' Maximal shift is:              ', max_shift, ' pixels ')
    #     print(' Number of blocks in file:      ', num_of_blocks)
    #     print(' Pulsar name:                   ', pulsar_name)
    #     print(' Dispersion measure:            ', pulsar_dm, ' pc / cm3 \n')

    # if receiver_type == '.jds':
    #     num_frequencies_initial = len(frequency_list) - 4

    # frequency_list_initial = np.empty_like(frequency_list)
    # frequency_list_initial[:] = frequency_list[:]

    # dat_file = open(data_filepath, 'rb')
    # dat_file.seek(1024)                     # Jumping to 1024 byte from file beginning

    # if use_mask_file:
    #     msk_file = open(data_filepath[:-3] + 'msk', 'rb')
    #     msk_file.seek(1024)  # Jumping to 1024 byte from file beginning

    # for block in range(num_of_blocks):   # main loop by number of blocks in file

    #     if print_or_not:
    #         print('\n * Data block # ', block + 1, ' of ', num_of_blocks,
    #               '\n ******************************************************************')

    #     # Timeline arrangements:
    #     fig_time_scale = []
    #     fig_date_time_scale = []
    #     for i in range(block * max_shift, (block+1) * max_shift):  # Shows the time of pulse end (at lowest frequency)
    #         fig_time_scale.append(timeline[i][11:23])
    #         fig_date_time_scale.append(timeline[i][:])
    #     if print_or_not:
    #         print(' Time: ', fig_time_scale[0], ' - ', fig_time_scale[-1], ', number of points: ', len(fig_time_scale))

    #     # Data block reading
    #     if receiver_type == '.jds':
    #         data = np.fromfile(dat_file, dtype=np.float64, count=(num_frequencies_initial + 4) * max_shift)   # 2
    #         data = np.reshape(data, [(num_frequencies_initial + 4), max_shift], order='F')  # 2
    #         data = data[:num_frequencies_initial, :]  # To delete the last channels of DSP data where time is stored

    #     if use_mask_file:
    #         mask = np.fromfile(msk_file, dtype=bool, count=(num_frequencies_initial + 4) * max_shift)
    #         mask = np.reshape(mask, [(num_frequencies_initial + 4), max_shift], order='F')
    #         mask = mask[:num_frequencies_initial, :]

    #     # Cutting the array in predefined frequency range
    #     if spec_freq_range:
    #         data, frequency_list, fi_start, fi_stop = specify_frequency_range(data, frequency_list_initial,
    #                                                                           freq_start, freq_stop)
    #         num_frequencies = len(frequency_list)
    #     else:
    #         num_frequencies = num_frequencies_initial  # + 4

    #     # Normalization of data
    #     normalization_lin(data, num_frequencies, 1 * max_shift)

    #     now_time = time.time()
    #     if print_or_not:
    #         print('\n  *** Preparation of data took:              ', round((now_time - a_previous_time), 2), 'seconds ')
    #     a_previous_time = now_time

    #     # Dispersion delay removing
    #     data_space = np.zeros((num_frequencies, 2 * max_shift))
    #     data_space[:, max_shift:] = data[:, :]
    #     temp_array = pulsar_DM_compensation_with_indices_changes(data_space, shift_vector)
    #     del data, data_space

    #     if use_mask_file:
    #         mask_space = np.zeros((num_frequencies, 2 * max_shift), dtype=bool)
    #         mask_space[:, max_shift:] = mask[:, :]
    #         temp_mask_array = pulsar_DM_compensation_with_indices_changes(mask_space, shift_vector)
    #         temp_mask_array = np.array(temp_mask_array, dtype=bool)

    #     now_time = time.time()
    #     if print_or_not:
    #         print('\n  *** Dispersion delay removing took:        ', round((now_time - a_previous_time), 2), 'seconds ')
    #     a_previous_time = now_time

    #     # Adding the next data block
    #     buffer_array += temp_array
    #     if use_mask_file:
    #         buffer_msk_array += temp_mask_array

    #     # Making and filling the array with fully ready data for plotting and saving to a file
    #     array_compensated_pulsar_dm = buffer_array[:, 0: max_shift]
    #     if use_mask_file:
    #         mask_compensated_pulsar_dm = buffer_msk_array[:, 0: max_shift]

    #     if block > 0:
    #         # Saving data with compensated pulsar_dm to DAT file
    #         if save_compensated_data > 0:  # and block > 0
    #             temp_to_write = np.transpose(array_compensated_pulsar_dm).copy(order='C')
    #             new_data_file = open(new_data_file_name, 'ab')
    #             new_data_file.write(temp_to_write)
    #             new_data_file.close()
    #             del temp_to_write

    #             if use_mask_file:
    #                 temp_to_write = np.transpose(mask_compensated_pulsar_dm).copy(order='C')
    #                 new_mask_file = open(new_mask_file_name, 'ab')
    #                 new_mask_file.write(temp_to_write)
    #                 new_mask_file.close()
    #                 del temp_to_write

    #         # Saving time data to ling timeline file
    #         with open(new_tl_file_name, 'a') as new_tl_file:
    #             for i in range(max_shift):
    #                 new_tl_file.write((fig_date_time_scale[i][:]))  # str

    #         # Logging the data
    #         with np.errstate(divide='ignore'):
    #             array_compensated_pulsar_dm[:, :] = 10 * np.log10(array_compensated_pulsar_dm[:, :])
    #         array_compensated_pulsar_dm[array_compensated_pulsar_dm == -np.inf] = 0
    #         array_compensated_pulsar_dm[array_compensated_pulsar_dm == np.nan] = 0
    #         array_compensated_pulsar_dm[np.isinf(array_compensated_pulsar_dm)] = 0

    #         # Normalizing log data
    #         array_compensated_pulsar_dm = array_compensated_pulsar_dm - np.mean(array_compensated_pulsar_dm)

    #         if use_mask_file:
    #             masked_data_raw = np.ma.masked_where(mask_compensated_pulsar_dm, array_compensated_pulsar_dm)
    #             data_raw_mean = np.mean(masked_data_raw)
    #             del masked_data_raw

    #             # Apply as mask to data (change masked data with mean values of data outside mask)
    #             array_compensated_pulsar_dm = array_compensated_pulsar_dm * np.invert(mask_compensated_pulsar_dm)
    #             array_compensated_pulsar_dm = array_compensated_pulsar_dm + mask_compensated_pulsar_dm * data_raw_mean

    #         # Preparing single averaged data profile for figure
    #         profile = array_compensated_pulsar_dm.mean(axis=0)[:]
    #         profile = profile - np.mean(profile)

    #         # Save full profile to TXT file
    #         if save_profile_txt > 0:
    #             profile_txt_file = open(profile_file_name, 'a')
    #             for i in range(len(profile)):
    #                 profile_txt_file.write(str(profile[i]) + ' \n')
    #             profile_txt_file.close()


    #     # Rolling temp_array to put current data first
    #     buffer_array = np.roll(buffer_array, - max_shift)
    #     buffer_array[:, max_shift:] = 0
    #     if use_mask_file:
    #         buffer_msk_array = np.roll(buffer_msk_array, - max_shift)
    #         buffer_msk_array[:, max_shift:] = 0

    # dat_file.close()

    # # Fourier analysis of the obtained time profile of pulses
    # if not save_compensated_data:
    #     new_data_file_name = ''
    # return new_data_file_name


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    import os

    # print('\n\n\n\n\n\n\n\n   *****************************************************************')
    # print('   *   ', software_name, ' v.', software_version, '   *      (c) YeS 2020')
    # print('   ***************************************************************** \n\n\n')

    start_time = time.time()

    initial_dat_file_path = "../ra_data_processing-all/P130725_075910.jds_Data_chA.dat"
    output_dat_file_path = "../ra_data_processing-all/P130725_075910.jds_Data_chA_new.dat"
    resampling_in_time = 2  # e.g., 2 means to double time resolution (half time samples)
    resampling_in_frequency = 2  # e.g., 2 means to double frequency resolution (half frequency channels)   


    dat_file_resampling(initial_dat_file_path, output_dat_file_path, resampling_in_time, resampling_in_frequency, print_or_not=True)

    print('  Dedispersed data stored in:', output_dat_file_path)

    end_time = time.time()    # Time of calculations

    print('\n\n  The program execution lasted for ', round((end_time - start_time), 2), 'seconds (',
                                                     round((end_time - start_time)/60, 2), 'min. ) \n')
    # print('\n\n                 *** ', software_name, ' has finished! *** \n\n\n')