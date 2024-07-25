import os
import pylab
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker   # <---- Added to suppress warning
from datetime import datetime
from matplotlib import rc
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader

# common_path = 'e:/RA_DATA_RESULTS/Transient_search_DSP_spectra_pulsar_UTR2_B0950+08/'
common_path = 'e:/RA_DATA_RESULTS/Transient_search_DSP_cross_spectra_B0809+74_URAN2/'
# dat_file_name = 'C250122_214003.jds'
dat_file_name = 'P130422_121607.jds'
data_type_to_process = 'chA'

time_res = 0.007944     # Time resolution, s
fig_time = 30           # Time on one figure, s

# central_dm = 2.972
# dm_range = 0.2
# dm_points = 51

central_dm = 5.755
dm_range = 0.5
dm_points = 101


def align_time_profiles(common_path, dat_file_name, data_type_to_process, central_dm, dm_range, dm_points, print_or_not=True):
    """
    Function aligns time profiles with their timelines for transient search
    Input parameters:
        common_path
        dat_file_name
        data_type_to_process
        dm_vector
    Output parameters:
        new_tl_file_name
        new_data_file_name

    """
    dm_vector = np.linspace(central_dm - dm_range, central_dm + dm_range, num=dm_points)

    if print_or_not:
        print('\n\n  Reading DM variation in range: ', dm_vector[0], ' - ', dm_vector[-1], 'pc / cm3')
        print('\n  Selecting common time segment... \n')

    data_filenames = []
    time_filenames = []
    for i in range(len(dm_vector)):
        data_filenames.append('Transient_DM_' + str(np.round(dm_vector[i], 6)) + '_' + dat_file_name + '_Data_' +
                              data_type_to_process + '_time_profile.txt')
        time_filenames.append('Transient_DM_' + str(np.round(dm_vector[i], 6)) + '_' + dat_file_name + '_Timeline.txt')

    start_times = np.zeros(len(data_filenames), dtype=datetime)
    stop_times = np.zeros(len(data_filenames), dtype=datetime)

    # Save the first and the last time in timeliest to find the common start and stop times
    for i in range(len(data_filenames)):
        timeline, dt_timeline = time_line_file_reader(os.path.join(common_path, time_filenames[i]))
        start_times[i] = dt_timeline[0]
        stop_times[i] = dt_timeline[-1]

    # Find the last starting time (common start time) and first stop time (common stop time)
    max_start_time = np.max(start_times)
    min_stop_time = np.min(stop_times)

    if print_or_not:
        print('  Common time range:', max_start_time, ' - ', min_stop_time)
        print('\n  Reading data... \n')

    for i in range(len(data_filenames)):

        # Reading timeline file
        timeline, dt_timeline = time_line_file_reader(os.path.join(common_path, time_filenames[i]))

        # Find indexes of common start time and common end time
        start_index = np.where(dt_timeline == np.datetime64(max_start_time))[0][0]
        stop_index = np.where(dt_timeline == np.datetime64(min_stop_time))[0][0]

        # print(len(timeline), stop_index - start_index, start_index, stop_index)

        if i == 0:
            # Prepare array to store all aligned data
            # data_array = np.empty((0, stop_index - start_index), float)
            data_array = np.empty((0, stop_index - start_index), dtype=np.float64)

            # Cut the timeline to proper indices and store to new common txt file
            common_timeline = timeline[start_index: stop_index]

            # Creating a long timeline TXT file
            new_tl_file_name = os.path.join(common_path, 'Transient_' + dat_file_name + '_Data_' + data_type_to_process +\
                               '_var_DM_' + str(np.round(dm_vector[0], 6)) + '-' + str(np.round(dm_vector[-1], 6)) + \
                               '_Timeline.txt')
            new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
            new_tl_file.close()

            with open(new_tl_file_name, 'a') as new_tl_file:
                for k in range(len(common_timeline)):
                    new_tl_file.write((common_timeline[k][:]))  # str

        data_file = open(os.path.join(common_path, data_filenames[i]), 'r')
        data_cur = []
        for line in data_file:
            data_cur.append(float(str(line)))
        data_file.close()
        data_cur = np.array(data_cur)
        data_cur = data_cur[start_index: stop_index]
        data_cur = np.expand_dims(data_cur, axis=0)

        data_array = np.append(data_array, data_cur, axis=0)

    if print_or_not:
        print('  Data shape:', data_array.shape)
        print('  Time line length:', len(common_timeline))
        print('  Data min and max values: ', np.min(data_array), np.max(data_array))
        print('\n  Saving data to a file... \n')

    # *** Creating a binary file with data for long data storage ***

    new_data_file_name = os.path.join(common_path, 'Transient_' + dat_file_name + '_Data_' + data_type_to_process + \
                         '_var_DM_' + str(np.round(dm_vector[0], 6)) + '-' + str(np.round(dm_vector[-1], 6)) + \
                         '.vdm')

    new_data_file = open(new_data_file_name, 'wb')
    time_points_num = np.int64(data_array.shape[1])
    new_data_file.write(time_points_num)             # Number of time points
    new_data_file.write(np.int64(len(dm_vector)))    # Number of DM points
    new_data_file.write(np.float64(central_dm))      # Central DM
    new_data_file.write(np.float64(dm_range))        # DM range
    new_data_file.write(data_array)                  # Data array
    # new_data_file.write(file_header)               # file header
    new_data_file.close()

    return new_data_file_name, new_tl_file_name


def visualize_time_profile(common_path, data_file_name, time_filename):

    timeline, dt_timeline = time_line_file_reader(os.path.join(common_path, time_filename))

    data_file = open(os. path.join(common_path, data_file_name), 'r')
    data_cur = []
    for line in data_file:
        data_cur.append(float(str(line)))
    data_file.close()
    data_cur = np.array(data_cur)

    fig, ax = plt.subplots(1, 1, figsize=(16.0, 7.0))
    ax.plot(data_cur)
    text = ax.get_xticks().tolist()
    for i in range(len(text) - 2):
        k = int(text[i])
        text[i] = timeline[k][11:23]

    ticks_loc = ax.get_xticks().tolist()  # <---- Added to suppress warning
    ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))  # <---- Added to suppress warning

    ax.set_xticklabels(text, fontsize=8, fontweight='bold')
    plt.show()

    return


def read_and_plot_var_dm_file(data_path, data_file_name, tl_file_name, result_path, time_res, fig_time,
                              print_or_not=True, plot_or_not=True):
    """Function reads, returns ad optionally make plots of the array of time profiles 
    dedispersed with varoius DM values from vdm file and its timeline

    Args:
        data_path (str): path to data file folder
        data_file_name (str): name of the data file with various dm profiles
        tl_file_name (str): name of the timeline file for the data file with various dm profiles
        result_path (str): path to fiolder where resuls will be stored (usually the same as data_path)
        time_res (float32): time resolution of the data
        fig_time (float32): time in seconds the 1 figure contains while plotting data in sequence of figures
        print_or_not (bool, optional): print verbose info on what's going on to terminal. Defaults to True.
        plot_or_not (bool, optional): make plots or just read the file and return the array. Defaults to True.

    Returns:
        data_array (np.array float64): the array of time profiles dedispersed with varoius DM values
        dm_vector (list float32): list of DM values used for data_array making
    """    

    # Reading timeline file
    timeline, dt_timeline = time_line_file_reader(os.path.join(data_path, tl_file_name))

    # Reading (.vdm) data file
    data_file = open(os.path.join(data_path, data_file_name), 'rb')
    time_points_num = struct.unpack('q', data_file.read(8))[0]
    dm_points = struct.unpack('q', data_file.read(8))[0]
    central_dm = struct.unpack('d', data_file.read(8))[0]
    dm_range = struct.unpack('d', data_file.read(8))[0]
    # data_file.seek(32)
    data_array = np.fromfile(data_file, dtype=np.float64, count=time_points_num * dm_points)
    data_array = np.reshape(data_array, [dm_points, time_points_num])
    data_file.close()

    # Recalculating DM vector to display DM values
    dm_vector = np.linspace(central_dm - dm_range, central_dm + dm_range, num=dm_points)

    if plot_or_not:
        
        # Calculating number of samples per figure and number of figures
        samples_per_fig = int(fig_time / time_res)
        fig_num = int(data_array.shape[1] / samples_per_fig)

        if print_or_not:
            print('\n  Making figures... \n')
            print('  Number of figures:', fig_num)
            print('  Samples per figure:', samples_per_fig)

        # Making a folder to save the figures
        newpath = os.path.join(result_path, 'DM_search_' + dat_file_name + '_Data_' + data_type_to_process + \
                '_var_DM_' + str(np.round(dm_vector[0], 6)) + '-' + str(np.round(dm_vector[-1], 6)))
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        for j in range(fig_num):
            rc('font', size=8, weight='bold')
            fig, ax = plt.subplots(1, 1, figsize=(16.0, 7.0))
            ax.imshow(data_array[:, j * samples_per_fig: (j+1) * samples_per_fig], aspect='auto', cmap='Greys',
                    extent=[0, samples_per_fig, dm_vector[0], dm_vector[-1]])
            ax.set_xlabel('Time, UTC', fontsize=8, fontweight='bold')
            ax.set_ylabel('Dispersion measure, pc*cm-3', fontsize=8, fontweight='bold')
            text = ax.get_xticks().tolist()
            for i in range(len(text) - 1):
                k = int(text[i])
                text[i] = timeline[k + j * samples_per_fig][11:23]
            ticks_loc = ax.get_xticks().tolist()                                 # <---- Added to suppress warning
            ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))          # <---- Added to suppress warning
            ax.set_xticklabels(text, fontsize=8, fontweight='bold')
            fig.suptitle('Single pulses of ' + ' ' + str(len(dm_vector)) + ' DM points' +
                        'fig. ' + str(j+1) + ' of ' + str(fig_num),
                        fontsize=8, fontweight='bold')
            pylab.savefig(os.path.join(newpath, data_file_name + '_var_DM_fig. ' + str(j + 1) + '.png'),
                        bbox_inches='tight', dpi=300)
            plt.close('all')

    return data_array, dm_vector

# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    # Calculating DM vector to display DM values
    dm_vector = np.linspace(central_dm - dm_range, central_dm + dm_range, num=dm_points)

    data_file_name, tl_file_name = align_time_profiles(common_path, dat_file_name, data_type_to_process, dm_vector)
                                                       

    from package_common_modules.text_manipulations import separate_filename_and_path
    # data_path, data_file_name = separate_filename_and_path(data_file_name)
    data_path, data_file_name = os.path.split(data_file_name)
    # data_path, tl_file_name = separate_filename_and_path(tl_file_name)
    data_path, tl_file_name = os.path.split(tl_file_name)

    # data_path = common_path
    result_path = common_path
    # data_file_name = 'Transient_P130422_121607.jds_Data_chA_var_DM_5.255-6.255.vdm'
    # tl_file_name = 'Transient_P130422_121607.jds_Data_chA_var_DM_5.255-6.255_Timeline.txt'

    read_and_plot_var_dm_file(data_path, data_file_name, tl_file_name, result_path, time_res, fig_time,
                              print_or_not=True)

    # time_profile_file_name = 'Transient_DM_2.972_C250122_214003.jds_Data_chA_time_profile.txt'
    # time_filename = 'Transient_DM_2.972_C250122_214003.jds_Timeline.txt'
    # visualize_time_profile(common_path, time_profile_file_name, time_filename)
