# from package_pulsar_processing.f_cut_needed_pulsar_period_from_dat import cut_needed_pulsar_period_from_dat_to_dat  
# from package_pulsar_processing.f_cut_needed_time_points_from_txt import cut_needed_time_points_from_dat_to_txt

import os
import sys
import time
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt

from os import path
# To change system path to main source_directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_ra_data_files_formats.read_file_header_adr import file_header_adr_read
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
from package_ra_data_processing.filtering import median_filter, average_filter

initial_dat_file_path = "../ra_data_processing-all/P130725_075910.jds_Data_chA.dat"
# initial_dat_file_path = "../ra_data_processing-all/P130725_082052.jds_Data_chA.dat"
# initial_dat_file_path = "../ra_data_processing-all/P130725_084023.jds_Data_chA.dat"
print_or_not = True
spec_freq_range = True

window_start_index = [3000, 4000, 5000]  #3500 
window_stop_index = [4000, 5000, 6000]  #6500
target_freq_index = 1  #800
block_length_in_spectra = 100
num_of_points = [120, 60, 60] # number of minima to be used for RM calculation 100    

speed_of_light = 2.99792458e8 # meters per second



def find_closest_value(data_list, target_value):
    """
    Finds the value in a list that is closest to a given target value.

    Args:
        data_list (list): The list of numbers to search within.
        target_value (int or float): The value to find the closest element to.

    Returns:
        int or float: The value from the list that is closest to the target_value.
    """
    if not data_list:
        raise ValueError("The input list cannot be empty.")

    closest_value = min(data_list, key=lambda x: abs(x - target_value))
    return closest_value



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
num_frequencies = len(frequency_list)  

num_of_blocks = int(dat_sp_in_file / block_length_in_spectra)
# num_of_blocks = 20

print(dat_sp_in_file)

# ************************************************************************************
#                             R E A D I N G   D A T A                                *
# ************************************************************************************

# Timeline file reading
timeline, dt_timeline = time_line_file_reader(initial_time_line_file_name)

reduced_timeline = timeline[::block_length_in_spectra]

for i in range(len(reduced_timeline)):
    reduced_timeline[i] = reduced_timeline[i][11:19]  # To remove milliseconds from time strings


dat_file = open(initial_dat_file_path, 'rb')
# dat_file.seek(1024)    # Jumping to 1024 byte from file beginning


jupiter_rm_vs_time_vs_freq = np.empty((3, num_of_blocks))
freq_bands_str = []

for band in range(3):  


    jupiter_rm_vs_time = []
    jupiter_rm_std_vs_time = []

    dat_file.seek(1024)    # Jumping to 1024 byte from file beginning

    f_low = str(np.round(window_start_index[band] * (66.0 / 16384), 3))  # MHz   
    f_high = str(np.round(window_stop_index[band] * (66.0 / 16384), 3))  # MHz

    print('\n\n\nLowest frequency to be analyzed:', f_low, 'MHz')
    print('\nHighest frequency to be analyzed:', f_high, 'MHz\n\n\n')

    freq_bands_str.append(f_low + ' - ' + f_high + ' MHz')  

    for block in range(num_of_blocks):   # main loop by number of blocks in file

        if print_or_not:
            print('\n * Data block # ', block + 1, ' of ', num_of_blocks,
                    '\n ******************************************************************')

        # Timeline arrangements:
        fig_time_scale = []
        fig_date_time_scale = []
        for i in range(block * block_length_in_spectra, (block+1) * block_length_in_spectra):  
            fig_time_scale.append(timeline[i][11:23])
            fig_date_time_scale.append(timeline[i][:])
        if print_or_not:
            print(' Time: ', fig_time_scale[0], ' - ', fig_time_scale[-1], ', number of points: ', len(fig_time_scale))

        # Data block reading
        if receiver_type == '.jds':
            data = np.fromfile(dat_file, dtype=np.float64, count=(num_frequencies) * block_length_in_spectra)   # 2
            data = np.reshape(data, [(num_frequencies), block_length_in_spectra], order='F')  # 2
            data = data[:num_frequencies-4, :]  # To delete the last channels of DSP data where time is stored


        data_init = data.copy()

        # plt.imshow(10 * np.log10(data), aspect='auto', origin='lower', cmap='jet')
        # plt.show()

        # Preparing single averaged data profile for figure
        profile = data_init.mean(axis=1)[:]

        # plt.plot(10 * np.log10(profile))
        # plt.show()

        lf_profile = median_filter(profile, 120)

        # plt.plot(10 * np.log10(lf_profile))
        # plt.show()

        profile = profile / lf_profile

        # plt.plot(10 * np.log10(profile))
        # plt.show()

        # window_start_index = 3500
        # window_stop_index = 6500
        profile = profile[window_start_index[band]: window_stop_index[band]]

        # plt.plot(10 * np.log10(profile))
        # plt.show()

        from scipy.ndimage import uniform_filter1d
        mean_profile = uniform_filter1d(profile, size=20)

        from scipy.signal import argrelmin
        indices = argrelmin(profile)[0]
        # print(indices)

        # plt.plot(10 * np.log10(profile))
        # plt.plot(10 * np.log10(mean_profile))
        # plt.plot(indices, 10 * np.log10(profile[indices]), 'ro')
        # plt.show()

        filtered_indices = []
        for i in range(len(indices)-1):

            if profile[indices[i]] < mean_profile[indices[i]]:
                filtered_indices.append(indices[i]) 

        if block == 0:
            plt.plot(10 * np.log10(profile))
            plt.plot(10 * np.log10(mean_profile))
            plt.plot(filtered_indices, 10 * np.log10(profile[filtered_indices]), 'ro')
            plt.show()

        # plt.plot(indices, 'bo')
        # plt.plot(filtered_indices, 'ro')
        # plt.show()

        only_minima_profile = profile[filtered_indices]

        # fig, axs = plt.subplots(2, 1) # Create a figure and a 1x2 grid of axes
        # axs[0].plot(10 * np.log10(profile))
        # axs[0].plot(10 * np.log10(mean_profile))
        # # axs[0].plot(filtered_indices, 10 * np.log10(profile[filtered_indices]), 'ro')
        # axs[0].plot(filtered_indices, 10 * np.log10(only_minima_profile), 'ro')
        # axs[0].set_title("Plot 1")
        # axs[1].plot(indices, 'bo')
        # axs[1].plot(filtered_indices, 'ro')
        # axs[1].set_title("Plot 2")
        # plt.tight_layout()
        # plt.show()
        # plt.close('all')    

        # print(filtered_indices)


        # target_freq_index = 800
        closest = find_closest_value(filtered_indices, target_freq_index)
        index_of_closest = filtered_indices.index(closest)
        print("\n Index of closest value:", index_of_closest)


        f_target = (66000000.0 / 16384) * (window_start_index[band] + target_freq_index)

        print("\n Target Frequency:", f_target, "Hz")


        if closest < target_freq_index:
            index_of_closest += 1
            closest = filtered_indices[index_of_closest]

        print("Closest frequency index above target:", closest)

        # n = 100
        list_of_closest_indices = list(range(0, num_of_points[band]))  # 100
        for i in range(len(list_of_closest_indices)):
            list_of_closest_indices[i] += index_of_closest
        # print("List of closest frequency indices above target:", list_of_closest_indices)

        list_of_closest_points = []
        for i in range(len(list_of_closest_indices)):
            list_of_closest_points.append( filtered_indices[list_of_closest_indices[i]] )
        # print("\nList of closest frequency points above target:", list_of_closest_points, "\n")

        list_minima_frequencies = []
        for i in range(len(list_of_closest_indices)):
            list_minima_frequencies.append( (66000000.0 / 16384) * (window_start_index[band] + list_of_closest_points[i]) )
        # print("\nList of minima frequencies above target:", list_minima_frequencies, "\n")

        list_delta_frequencies = []
        for i in range(len(list_minima_frequencies)-1):
            list_delta_frequencies.append( list_minima_frequencies[i+1] - list_minima_frequencies[i] )
        # print("\nList of delta frequencies above target:", list_delta_frequencies, "\n")

        list_central_frequencies = []
        for i in range(len(list_minima_frequencies)-1):
            list_central_frequencies.append( (list_minima_frequencies[i+1] + list_minima_frequencies[i]) / 2 )
        # print("\nList of central frequencies above target:", list_central_frequencies, "\n")


        list_rm_values = []
        main_const = np.pi / speed_of_light**2
        for i in range(len(list_delta_frequencies)):
            
            # list_rm_values.append( (np.pi / speed_of_light**2) * list_central_frequencies[i]**3 / (2 * list_delta_frequencies[i]))
            
            numerator = list_central_frequencies[i]**2 * (list_central_frequencies[i] + list_delta_frequencies[i])**2
            denominator = (list_central_frequencies[i] + list_delta_frequencies[i])**2 - list_central_frequencies[i]**2
            
            list_rm_values.append(main_const * numerator / denominator)
            
        # print("\nList of RM values:", list_rm_values, "\n")

        time_point_median_rm = np.median(list_rm_values)
        time_point_std_rm = np.std(list_rm_values)
        print(time_point_median_rm, time_point_std_rm)
        
        list_rm_values = np.array(list_rm_values)
        
        import numpy.ma as ma
        mask = np.abs(list_rm_values - time_point_median_rm) > 2 * time_point_std_rm
        masked_data = ma.masked_array(list_rm_values, mask=mask)
        time_point_std_rm = np.std(masked_data)
        
        print(time_point_median_rm, time_point_std_rm)
        
        jupiter_rm_vs_time.append(time_point_median_rm)
        jupiter_rm_std_vs_time.append(time_point_std_rm)
    
    jupiter_rm_vs_time_vs_freq[band, :] = jupiter_rm_vs_time

x_values = np.arange(1, len(reduced_timeline) + 1, 1)

print(jupiter_rm_vs_time_vs_freq.shape)

x = np.linspace(0, len(jupiter_rm_vs_time)-1, len(jupiter_rm_vs_time))
plt.plot(x, jupiter_rm_vs_time_vs_freq[0,:], 'o', color = 'C0', alpha=0.6, label=f'{freq_bands_str[0]}')
plt.plot(x, jupiter_rm_vs_time_vs_freq[1,:], 'o', color = 'C1', alpha=0.6, label=f'{freq_bands_str[1]}')
plt.plot(x, jupiter_rm_vs_time_vs_freq[2,:], 'o', color = 'C3', alpha=0.6, label=f'{freq_bands_str[2]}')
# plt.plot(x, jupiter_rm_vs_time, 'ro')
# plt.errorbar(x, jupiter_rm_vs_time, yerr = jupiter_rm_std_vs_time) # , fmt ='o'
plt.xticks(x_values, reduced_timeline, rotation=45)
plt.xlim(x_values[0], x_values[-1])
plt.grid()
plt.legend()
plt.locator_params(axis='x', nbins=12)
plt.ylim(1.5, 14.0) 
plt.show()


