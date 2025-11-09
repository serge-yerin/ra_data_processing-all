# from package_pulsar_processing.f_cut_needed_pulsar_period_from_dat import cut_needed_pulsar_period_from_dat_to_dat  
# from package_pulsar_processing.f_cut_needed_time_points_from_txt import cut_needed_time_points_from_dat_to_txt


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

initial_dat_file_path = "../ra_data_processing-all/P130725_075910.jds_Data_chA.dat"
print_or_not = True

 # Path to timeline file to be analyzed:
initial_time_line_file_name = initial_dat_file_path[-31:-13] + '_Timeline.txt'

initial_dat_file_path = os.path.normpath(initial_dat_file_path)
initial_time_line_file_name = os.path.normpath(initial_time_line_file_name)


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

       #     ifmin = int(np.round(fmin * 1e6 / df))
    #     ifmax = int(np.round(fmax * 1e6 / df)) - 4


      #     # Change number of frequency channels in the header
    #     file_header = jds_header_new_channels_numbers(file_header, ifmin, ifmax)


 #     # *** Creating a binary file with data for long data storage ***
    #     new_data_file_name = os.path.join(common_path, pulsar_name + '_DM_' +
    #                                       str(np.round(pulsar_dm, 6)) + '_' + filename)
    #     new_data_file = open(new_data_file_name, 'wb')
    #     new_data_file.write(file_header)
    #     new_data_file.close()

       # # *** Creating a name for long timeline TXT file ***
    # data_filename = data_filepath.split(os.sep)[-1]
    # new_tl_file_name = os.path.join(common_path, pulsar_name + '_DM_' + str(np.round(pulsar_dm, 6)) + '_' +
    #                                 data_filename[:-13] + '_Timeline.txt')
    # new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
    # new_tl_file.close()


 # if receiver_type == '.jds':
    #     num_frequencies_initial = len(frequency_list) - 4

  # frequency_list_initial = np.empty_like(frequency_list)
    # frequency_list_initial[:] = frequency_list[:]

    # dat_file = open(data_filepath, 'rb')
    # dat_file.seek(1024)                     # Jumping to 1024 byte from file beginning

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

    #     # Cutting the array in predefined frequency range
    #     if spec_freq_range:
    #         data, frequency_list, fi_start, fi_stop = specify_frequency_range(data, frequency_list_initial,
    #                                                                           freq_start, freq_stop)
    #         num_frequencies = len(frequency_list)
    #     else:
    #         num_frequencies = num_frequencies_initial  # + 4
