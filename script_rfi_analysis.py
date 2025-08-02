

import os
import datetime
import numpy as np
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.read_file_header_adr import file_header_adr_read
import matplotlib.pyplot as plt

path_to_data = os.path.normpath('../DATA_preprocessed/')

dat_file_name_list = find_files_only_in_current_folder(path_to_data, '.dat', 1)

# print(dat_file_name_list)

# for i in range(len(dat_file_name_list)):
for i in range(3):
    filename = os.path.join(path_to_data, dat_file_name_list[i])
    print(f'Processing file: {filename}')
    
    with open(filename, 'rb') as file:
        # *** Data file header read ***
        df_filesize = os.stat(filename).st_size                       # Size of file
        df_filename = file.read(32).decode('utf-8').rstrip('\x00')    # Initial data file name
    
    if df_filename[-4:] == '.adr':
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description, CLCfrq, df_creation_timeUTC,
            ReceiverMode, Mode, sumDifMode, NAvr, time_res, fmin, fmax, df, frequency, fft_size, SLine, Width,
            BlockSize] = file_header_adr_read(filename, 0, 1)

        print(f'File: {df_filename}, Size: {df_filesize}, Time: {df_creation_timeUTC}')

        file_start_time_utc = datetime.datetime(int('20' + df_filename[1:3]), int(df_filename[3:5]), int(df_filename[5:7]), 
                                                int(df_creation_timeUTC[0:2]), int(df_creation_timeUTC[3:5]), int(df_creation_timeUTC[6:8]),
                                                int(df_creation_timeUTC[9:12]) * 1000)
        
        print(file_start_time_utc)

    else:
        print(f'File: {df_filename} is not an ADR file, skipping...')
        continue
    
    num_freq = len(frequency)  # Number of frequency channels
    num_samp = int((df_filesize - 1024) / (num_freq * 8))  # Number of samples in the file
    
    with open(filename, 'rb') as file:
    
        file.seek(1024, os.SEEK_SET)
        data = np.fromfile(file, dtype=np.float64, count=num_freq * num_samp)

        data = np.reshape(data, [num_freq, num_samp], order='F')
        min_data = np.min(data, axis=1)
        max_data = np.max(data, axis=1) 

        data = 10 * np.log10(data)
        min_data = 10 * np.log10(min_data)
        max_data = 10 * np.log10(max_data)  



        plt.figure(1, figsize=(10.0, 6.0))
        plt.imshow(data, aspect='auto', interpolation='none', origin='lower',   
                   extent=[0, num_samp, fmin, fmax], cmap='jet')
        plt.colorbar(label='Power (dB)')
        plt.title(f'RFI Analysis for {df_filename}')
        plt.xlabel('Sample Number')
        plt.ylabel('Frequency (Hz)')
        # plt.grid(True)
        plt.tight_layout()
        plt.show()
        plt.close('all')


        plt.figure(1, figsize=(10.0, 6.0))
        plt.plot(frequency, min_data, label='Min Data', color='blue')
        plt.plot(frequency, max_data, label='Max Data', color='red')
        plt.title(f'Min/Max Data for {df_filename}')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power (dB)')
        plt.legend()
        plt.tight_layout()
        plt.show()
        plt.close('all')