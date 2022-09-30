import numpy as np
import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('agg')
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader

common_path = 'e:/RA_DATA_RESULTS/Transient_search_DSP_spectra_pulsar_UTR2_B0950+08/'

data_filenames = ['Transient_DM_2.472_C250122_214003.jds_Data_chA_time_profile.txt',
                  'Transient_DM_2.672_C250122_214003.jds_Data_chA_time_profile.txt']
time_filenames = ['Transient_DM_2.472_C250122_214003.jds_Timeline.txt',
                  'Transient_DM_2.672_C250122_214003.jds_Timeline.txt']

time = []
data = []


for i in range(len(data_filenames)):

    timeline, dt_timeline = time_line_file_reader(common_path + time_filenames[i])

    file = open(common_path + data_filenames[i], 'r')
    data_cur = []
    for line in file:
        data_cur.append(float(str(line)))
    file.close()

    time.append(dt_timeline)
    data.append(data_cur)

# print(len(timeline), len(data))
n = 15000

plt.plot(time[0][:n], data[0][:n])
plt.plot(time[1][:n], data[1][:n])
plt.show()
