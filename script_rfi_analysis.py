

import os
import datetime
import scipy
import numpy as np
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.read_file_header_adr import file_header_adr_read
import matplotlib.pyplot as plt
from package_ra_data_processing.filtering import median_filter, average_filter  

path_to_data = os.path.normpath('../DATA_preprocessed/')

dat_file_name_list = find_files_only_in_current_folder(path_to_data, '.dat', 1)

# print(dat_file_name_list)

f_min = 5.0  # Minimum frequency in MHz
f_max = 7.0  # Maximum frequency in MHz

min_data_array = []
max_data_array = []
min_min_data_array = []
date_array = []

for i in range(len(dat_file_name_list)):
# for i in range(3):
    filename = os.path.join(path_to_data, dat_file_name_list[i])
    
    with open(filename, 'rb') as file:
        # *** Data file header read ***
        df_filesize = os.stat(filename).st_size                       # Size of file
        df_filename = file.read(32).decode('utf-8').rstrip('\x00')    # Initial data file name
    
    if df_filename[-4:] == '.adr':
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description, CLCfrq, df_creation_timeUTC,
            ReceiverMode, Mode, sumDifMode, NAvr, time_res, fmin, fmax, df, frequency, fft_size, SLine, Width,
            BlockSize] = file_header_adr_read(filename, 0, 0)

        print(f'File: {df_filename}, Size: {df_filesize}, Time: {df_creation_timeUTC}')

        file_start_time_utc = datetime.datetime(int('20' + df_filename[1:3]), int(df_filename[3:5]), int(df_filename[5:7]), 
                                                int(df_creation_timeUTC[0:2]), int(df_creation_timeUTC[3:5]), int(df_creation_timeUTC[6:8]),
                                                int(df_creation_timeUTC[9:12]) * 1000)
        
        date_array.append(file_start_time_utc)

    else:
        print(f'File: {df_filename} is not an ADR file, skipping...')
        continue
    
    num_freq = len(frequency)  # Number of frequency channels
    num_samp = int((df_filesize - 1024) / (num_freq * 8))  # Number of samples in the file
    
    print(num_freq, num_samp)

    with open(filename, 'rb') as file:
    
        file.seek(1024, os.SEEK_SET)
        data = np.fromfile(file, dtype=np.float64, count=num_freq * num_samp)

        data = np.reshape(data, [num_freq, num_samp], order='F')
        min_data = np.min(data, axis=1)
        max_data = np.max(data, axis=1) 

        min_min_data = scipy.ndimage.minimum_filter(min_data, size=50)
        min_min_data = median_filter(min_min_data, 100)

        min_data_array.append(min_data)
        max_data_array.append(max_data) 
        min_min_data_array.append(min_min_data)

        data = 10 * np.log10(data)
        min_data = 10 * np.log10(min_data)
        max_data = 10 * np.log10(max_data)  
        min_min_data = 10 * np.log10(min_min_data)  

        # min_data = median_filter(min_data, 25)
        # max_data = median_filter(max_data, 25)



        # plt.figure(1, figsize=(10.0, 6.0))
        # plt.plot(frequency, min_data, label='Min Data', color='blue')
        # plt.plot(frequency, min_min_data, label='Min-min Data', color='red')
        # plt.title(f'Min/Max Data for {df_filename}')
        # plt.xlabel('Frequency (Hz)')
        # plt.ylabel('Power (dB)')
        # plt.legend()
        # plt.tight_layout()
        # plt.show()
        # plt.close('all')


        # plt.figure(1, figsize=(10.0, 6.0))
        # plt.imshow(data, aspect='auto', interpolation='none', origin='lower',   
        #            extent=[0, num_samp, fmin, fmax], cmap='jet')
        # plt.colorbar(label='Power (dB)')
        # plt.title(f'RFI Analysis for {df_filename}')
        # plt.xlabel('Sample Number')
        # plt.ylabel('Frequency (Hz)')
        # # plt.grid(True)
        # plt.tight_layout()
        # plt.show()
        # plt.close('all')


        # plt.figure(1, figsize=(10.0, 6.0))
        # plt.plot(frequency, min_data, label='Min Data', color='blue')
        # plt.plot(frequency, max_data, label='Max Data', color='red')
        # plt.title(f'Min/Max Data for {df_filename}')
        # plt.xlabel('Frequency (Hz)')
        # plt.ylabel('Power (dB)')
        # plt.legend()
        # plt.tight_layout()
        # plt.show()
        # plt.close('all')

        range_min_point = int(f_min * 8192 / 80)
        range_max_point = int(f_max * 8192 / 80)
        
        # plt.figure(1, figsize=(10.0, 6.0))
        # plt.plot(frequency[range_min_point: range_max_point], min_data[range_min_point: range_max_point], label='Min Data', color='blue')
        # plt.plot(frequency[range_min_point: range_max_point], max_data[range_min_point: range_max_point], label='Max Data', color='red')
        # plt.title(f'Min/Max Data for {df_filename}')
        # plt.xlabel('Frequency (Hz)')
        # plt.ylabel('Power (dB)')
        # plt.legend()
        # plt.tight_layout()
        # plt.show()
        # plt.close('all')

        # plt.figure(1, figsize=(10.0, 6.0))
        # plt.plot(frequency[range_min_point: range_max_point], min_data[range_min_point: range_max_point], label='Min Data', color='blue')
        # plt.plot(frequency[range_min_point: range_max_point], min_min_data[range_min_point: range_max_point], label='Max Data', color='red')
        # plt.title(f'Min/Max Data for {df_filename}')
        # plt.xlabel('Frequency (Hz)')
        # plt.ylabel('Power (dB)')
        # plt.legend()
        # plt.tight_layout()
        # plt.show()
        # plt.close('all')
    
for i in range(len(date_array)):
    print(f'File: {dat_file_name_list[i]}, Date: {date_array[i]}')  


min_3_data = np.min(min_min_data_array, axis=0)



# plt.figure(1, figsize=(10.0, 6.0))
# for i in range(len(min_data_array)):
#     plt.plot(frequency, 10 * np.log10(min_data_array[i]), label=f'Min Data {date_array[i]}')
# plt.plot(frequency, 10 * np.log10(min_3_data))
# plt.title('Min Data Across Files')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Power (dB)')
# plt.legend()
# plt.tight_layout()
# plt.show()
# plt.close('all')    


plt.figure(1, figsize=(10.0, 6.0))
for i in range(len(min_data_array)):
    plt.plot(frequency[range_min_point: range_max_point], 10 * np.log10(min_data_array[i][range_min_point: range_max_point]), label=f'Min Data {date_array[i]}')
plt.plot(frequency[range_min_point: range_max_point], 10 * np.log10(min_3_data[range_min_point: range_max_point]))
plt.title('Min Data Across Files')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (dB)')
plt.legend()
plt.tight_layout()
plt.show()
plt.close('all')    

min_data_array = np.array(min_data_array)

print(min_data_array.shape)

array1 = np.log10(min_data_array[:, range_min_point: range_max_point])

print(array1.shape)

plt.figure(1, figsize=(10.0, 6.0))
plt.imshow(array1, aspect='auto', interpolation='none', origin='lower',   
                         cmap='jet')  # extent=[0, num_samp, fmin, fmax]
# plt.colorbar(label='Power (dB)')
# plt.title(f'RFI Analysis for {df_filename}')
# plt.xlabel('Sample Number')
# plt.ylabel('Frequency (Hz)')
plt.tight_layout()
plt.show()
plt.close('all')

# plt.figure(1, figsize=(10.0, 6.0))
# for i in range(len(max_data_array)):
#     plt.plot(frequency, 10 * np.log10(max_data_array[i]), label=f'Max Data {date_array[i]}')
# plt.title('Max Data Across Files')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Power (dB)')
# plt.legend()
# plt.tight_layout()
# plt.show()
# plt.close('all')   
    