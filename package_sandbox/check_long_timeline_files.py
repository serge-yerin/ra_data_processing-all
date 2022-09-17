from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
import numpy as np
import matplotlib.pyplot as plt

# timeline_filepath = 'e:/python/B0950+08_DSP_waveform_B0950p08_high_band/E310120_225419.jds_Timeline.wtxt'
#
# timeline, dt_timeline = time_line_file_reader(timeline_filepath)
#
# print(len(timeline), len(dt_timeline))
# array = np.empty(0)
# for i in range(30):
#     print(i, timeline[i][:-1], dt_timeline[i])
#     dt = dt_timeline[i+1] - dt_timeline[i]
#     array = np.append(array, float(dt.total_seconds()))
#     # print(i, dt.total_seconds())
# print(array)
# # fig, ax = plt.figure((1,1))
# plt.plot(array)
# plt.show()
# plt.close()


timeline_filepath = 'e:/python/B0950+08_DSP_waveform_B0950p08_high_band/E310120_225419.jds_Second_phase.xtxt'


def merge_wf_timeline_and_phase_of_second(timeline_filepath):

    file = open(timeline_filepath, 'r')
    array = []
    for line in file:
        array.append(str(line))
    file.close()
    array = np.int64(array[2:])

    # print(array[0:10])

    line = array.copy()

    diff = []
    for i in range(len(line)-1):
        diff.append(line[i+1] - line[i])

    values, counts = np.unique(diff, return_counts=True)
    step = values[np.argmax(counts)]
    # print(step)

    for i in range(len(line)-1):
        if np.abs(line[i+1] - line[i]) > step:
            line[i+1] = line[i] + step

    max_diff = np.max(diff)
    print('max: ', max_diff)

    max_line = line + max_diff - 8190

    plt.plot(array[0:])
    plt.plot(line[0:])
    plt.plot(max_line[0:])
    plt.show()
    plt.close()

    return


merge_wf_timeline_and_phase_of_second(timeline_filepath)