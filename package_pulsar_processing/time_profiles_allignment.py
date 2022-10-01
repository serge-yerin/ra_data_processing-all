import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader

common_path = 'e:/RA_DATA_RESULTS/Transient_search_DSP_spectra_pulsar_UTR2_B0950+08/'
dat_file_name = 'C250122_214003.jds'
data_type_to_process = 'chA'

central_dm = 2.972
dm_range = 0.4
dm_points = 41
dm_vector = np.linspace(central_dm - dm_range, central_dm + dm_range, num=dm_points)


def align_time_profiles(common_path, dat_file_name, data_type_to_process, dm_vector):
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
    data_filenames = []
    time_filenames = []
    for i in range(len(dm_vector)):
        data_filenames.append('Transient_DM_' + str(dm_vector[i]) + '_' + dat_file_name + '_Data_' +
                              data_type_to_process + '_time_profile.txt')
        time_filenames.append('Transient_DM_' + str(dm_vector[i]) + '_' + dat_file_name + '_Timeline.txt')

    start_times = np.zeros(len(data_filenames), dtype=datetime)
    stop_times = np.zeros(len(data_filenames), dtype=datetime)

    # Save the first and the last time in timeliest to find the common start and stop times
    for i in range(len(data_filenames)):
        timeline, dt_timeline = time_line_file_reader(common_path + time_filenames[i])
        start_times[i] = dt_timeline[0]
        stop_times[i] = dt_timeline[-1]

    # Find the last starting time (common start time) and first stop time (common stop time)
    max_start_time = np.max(start_times)
    min_stop_time = np.min(stop_times)

    # print(max_start_time)
    # print(min_stop_time)

    for i in range(len(data_filenames)):

        # Reading timeline file
        timeline, dt_timeline = time_line_file_reader(common_path + time_filenames[i])

        # Find indexes of common start time and common end time
        start_index = np.where(dt_timeline == np.datetime64(max_start_time))[0][0]
        stop_index = np.where(dt_timeline == np.datetime64(min_stop_time))[0][0]

        # print(len(timeline), stop_index - start_index, start_index, stop_index)

        if i == 0:
            # Prepare array to store all aligned data
            data_array = np.empty((0, stop_index - start_index), float)

            # Cut the timeline to proper indices and store to new common txt file
            timeline = timeline[start_index: stop_index]

            # Creating a long timeline TXT file
            new_tl_file_name = common_path + 'Transient_VarDM_' + dat_file_name + '_Timeline.txt'
            new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
            new_tl_file.close()

            with open(new_tl_file_name, 'a') as new_tl_file:
                for k in range(len(timeline)):
                    new_tl_file.write((timeline[k][:]))  # str

        data_file = open(common_path + data_filenames[i], 'r')
        data_cur = []
        for line in data_file:
            data_cur.append(float(str(line)))
        data_file.close()
        data_cur = np.array(data_cur)
        data_cur = data_cur[start_index: stop_index]
        data_cur = np.expand_dims(data_cur, axis=0)

        data_array = np.append(data_array, data_cur, axis=0)

    print(data_array.shape)
    print(np.min(data_array), np.max(data_array))

    new_data_file_name = ''

    plt.imshow(data_array[0:1000, 0:1000], aspect='auto', cmap='Greys')
    plt.show()

    return new_tl_file_name, new_data_file_name


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    align_time_profiles(common_path, dat_file_name, data_type_to_process, dm_vector)
