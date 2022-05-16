
import os
import numpy as np
import matplotlib.pyplot as plt
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_processing.spectra_normalization import Normalization_dB
# Files to be analyzed:
filepath = 'P250322_082507.jds_Data_chA.dat'
# tl_file_name = common_path + DAT_file_name + '_Timeline.txt'


# *** Data file header read ***
df_filesize = os.stat(filepath).st_size  # Size of file

# Opening DAT datafile and data file header read
file = open(filepath, 'rb')
df_filepath = file.read(32).decode('utf-8').rstrip('\x00')  # Initial data file name
file.close()

if df_filepath[-4:] == '.jds':  # If data obtained from DSPZ receiver

    [df_filepath, df_filesize, df_system_name, df_obs_place, df_description, clock_frq,
     df_creation_time_utc, sp_in_file, receiver_mode, mode, n_avr, time_resolution, fmin, fmax,
     df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(filepath, 0, 1)


# Time line file reading
# timeline, dt_timeline = time_line_file_reader(timeline_filepath)

data_file = open(filepath, 'rb')
data_file.seek(1024, os.SEEK_SET)  # Jumping to 1024+number of spectra to skip byte from file beginning

spectra_to_read = 4000

# Reading and preparing block of data (3 periods)
data = np.fromfile(data_file, dtype=np.float64, count=spectra_to_read * len(frequency))
data = np.reshape(data, [len(frequency), spectra_to_read], order='F')


# Preparing single averaged data profile for figure
# profile = data.mean(axis=0)[:]
# profile = profile - np.mean(profile)
# data = data - np.mean(data)


data = 10 * np.log10(data)
data[np.isnan(data)] = -120

Normalization_dB(data.transpose(), len(frequency), spectra_to_read)
data = data[:-4, :]
print(data.shape)
data = data - np.mean(data)
print(np.max(data), np.min(data), np.mean(data))

profile_0 = np.mean(data, axis=0)
profile_1 = np.mean(data, axis=1)

fig, [ax0, ax1] = plt.subplots(1, 2, figsize=(8, 4))
ax0.plot(profile_0)
ax1.plot(profile_1)
plt.show()

plt.plot()
plt.imshow(data, vmin=-0.1, vmax=2, cmap='Greys')
plt.show()
