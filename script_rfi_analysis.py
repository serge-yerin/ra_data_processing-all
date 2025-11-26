# Script for RFI analysis in radioastronomical data files in ADR format for Signal project

import os
import datetime
from datetime import date, timedelta
import scipy
import numpy as np
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.read_file_header_adr import file_header_adr_read
import matplotlib.pyplot as plt
from matplotlib import rc
from package_ra_data_processing.filtering import median_filter, average_filter  


path_to_data = os.path.normpath('../DATA_preprocessed/')
path_to_results = os.path.normpath('../DATA_results/')
f_min = 5.0  # Minimum frequency in MHz
f_max = 20.0  # Maximum frequency in MHz

if not os.path.exists(path_to_results):
    os.makedirs(path_to_results)

# Get list of .dat files in the specified folder
dat_file_name_list = find_files_only_in_current_folder(path_to_data, '.dat', 1)











min_data_array = []
max_data_array = []
min_min_data_array = []
date_array = []

print('\nReading files in a loop...\n')

# Loop through each .dat file (date of observations)
# for i in range(3):
for file_index in range(len(dat_file_name_list)):

    # Construct full file path
    filename = os.path.join(path_to_data, dat_file_name_list[file_index])
    
    with open(filename, 'rb') as file:
        # *** Data file header read ***
        df_filesize = os.stat(filename).st_size                       # Size of file
        df_filename = file.read(32).decode('utf-8').rstrip('\x00')    # Initial data file name

    if df_filename[-4:] == '.adr':
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description, CLCfrq, df_creation_timeUTC,
            ReceiverMode, Mode, sumDifMode, NAvr, time_res, fmin, fmax, df, frequency, fft_size, SLine, Width,
            BlockSize] = file_header_adr_read(filename, 0, 0)

        
        file_start_time_utc = datetime.datetime(int('20' + df_filename[1:3]), int(df_filename[3:5]), int(df_filename[5:7]), 
                                                int(df_creation_timeUTC[0:2]), int(df_creation_timeUTC[3:5]), int(df_creation_timeUTC[6:8]),
                                                int(df_creation_timeUTC[9:12]) * 1000)
        
        print(file_start_time_utc)

        date_array.append(file_start_time_utc)

    else:
        print(f'File: {dat_file_name_list[file_index]} is not an ADR file, skipping...')
        continue
    
    num_freq = len(frequency)  # Number of frequency channels
    num_samp = int((df_filesize - 1024) / (num_freq * 8))  # Number of samples in the file
    
    print(f'File: {df_filename},   Size: {df_filesize},   Time: {df_creation_timeUTC},   Freq: {num_freq},   Samp: {num_samp}')

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

        with np.errstate(divide='ignore', invalid='ignore'):
            min_data = 10 * np.log10(min_data)
            max_data = 10 * np.log10(max_data)  
            min_min_data = 10 * np.log10(min_min_data)  

        # min_data = median_filter(min_data, 25)
        # max_data = median_filter(max_data, 25)

        plt.figure(1, figsize=(10.0, 6.0))
        plt.plot(frequency, max_data, label='Max level', color='C0', alpha=0.6)
        plt.plot(frequency, min_data, label='Min level', color='C1', alpha=0.6)
        plt.plot(frequency, min_min_data, label='Filtered min level', color='C3')
        plt.title(f'Actual RFI levels for {df_filename}')
        plt.xlabel('Frequency, MHz')
        plt.ylabel('Power level, dB')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(path_to_results, f'Actual RFI levels - {df_filename[:-4]}.png'), dpi=350)
        # plt.show()
        plt.close('all')


        plt.figure(1, figsize=(10.0, 6.0))
        plt.plot(frequency, max_data - min_min_data, label='Max level', color='C0', alpha=0.6)
        plt.plot(frequency, min_data - min_min_data, label='Min level', color='C1', alpha=0.6)
        plt.title(f'Normalized RFI levels above background for {df_filename}')
        plt.xlabel('Frequency, MHz')
        plt.ylabel('Power level, dB')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(path_to_results, f'Normalized RFI levels - {df_filename[:-4]}.png'), dpi=350)
        # plt.show()
        plt.close('all')


        with np.errstate(divide='ignore', invalid='ignore'):
            plt.figure(1, figsize=(10.0, 6.0))
            plt.imshow(10*np.log10(data), aspect='auto', interpolation='none', origin='lower',   
                    extent=[0, num_samp, fmin, fmax], cmap='jet')
            plt.colorbar(label='Power levels, dB')
            plt.title(f'Dynamic sperctrum of {df_filename}')
            plt.xlabel('Sample number')
            plt.ylabel('Frequency, MHz')
            plt.tight_layout()
            plt.savefig(os.path.join(path_to_results, f'Dynamic spectrum of RFI - {df_filename[:-4]}.png'), dpi=350)
            # plt.show()
            plt.close('all')


        range_min_point = int(f_min * 8192 / fmax)
        range_max_point = int(f_max * 8192 / fmax)
        
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

date_array.sort()

start_date = date(date_array[0].year, date_array[0].month, date_array[0].day)
end_date = date(date_array[-1].year, date_array[-1].month, date_array[-1].day)

print(f'Start date: {start_date},   End date: {end_date}')

dates_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# for date in dates_list: 
#     print(date)


with np.errstate(divide='ignore', invalid='ignore'):
    plt.figure(1, figsize=(10.0, 6.0))
    for i in range(len(min_data_array)):
        plt.plot(frequency, 10 * np.log10(min_data_array[i]), label=f'min levels {str(date_array[i])[0:19]}')
    # plt.plot(frequency, 10 * np.log10(min_3_data))
    plt.title('Minimal levels for all dates in full range')
    plt.xlabel('Frequency, MHz')
    plt.xlim(frequency[0], frequency[-1])
    plt.ylabel('Power level, dB')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(path_to_results, 'Minimal level of response across all dates - full range.png'), dpi=350) 
    # plt.show()
    plt.close('all')    



with np.errstate(divide='ignore', invalid='ignore'):
    plt.figure(1, figsize=(10.0, 6.0))
    for i in range(len(min_data_array)):
        plt.plot(frequency[range_min_point: range_max_point], 10 * np.log10(min_data_array[i][range_min_point: range_max_point]), 
                 label=f'min levels {str(date_array[i])[0:19]}')
    # plt.plot(frequency[range_min_point: range_max_point], 10 * np.log10(min_3_data[range_min_point: range_max_point]))
    plt.title(f'Minimal levels for all dates in selected range of {f_min} - {f_max} MHz')
    plt.xlabel('Frequency, MHz')
    plt.xlim(frequency[range_min_point], frequency[range_max_point-1])
    plt.ylabel('Power level, dB')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(path_to_results, 'Minimal level of response across all dates - selected range.png'), dpi=350) 
    # plt.show()
    plt.close('all')    

min_data_array = np.array(min_data_array)
max_data_array = np.array(max_data_array)
min_min_data_array = np.array(min_min_data_array)

# print(min_data_array.shape)

min_spectra_vs_date = min_data_array[:, range_min_point: range_max_point]
max_spectra_vs_date = max_data_array[:, range_min_point: range_max_point]
min_filterd_spectra_vs_date = min_min_data_array[:, range_min_point: range_max_point]

# array1[3, :] = np.nan  

len_x = range_max_point - range_min_point
x_values = np.linspace(0, len_x-1, len_x)

reduced_frequency = []
for i in range(len_x):
    reduced_frequency.append(np.round(frequency[range_min_point + i], 2))


y_values = np.linspace(0, len(date_array)-1, len(date_array))
reduced_timeline = []
for i in range(len(date_array)):
    reduced_timeline.append(str(date_array[i])[0:10])


# with np.errstate(divide='ignore', invalid='ignore'):
#     plt.figure(1, figsize=(10.0, 6.0))
#     plt.imshow(np.log10(min_spectra_vs_date), aspect='auto', interpolation='none', origin='lower',   
#                             cmap='jet')  # extent=[0, num_samp, fmin, fmax]
#     # plt.colorbar(label='Power (dB)')
#     # plt.title(f'RFI Analysis for {df_filename}')
#     plt.xticks(x_values, reduced_frequency)
#     plt.yticks(y_values, reduced_timeline)
#     plt.ylim(y_values[0]-0.5, y_values[-1]+0.5)
#     plt.locator_params(axis='x', nbins=11)
#     plt.ylabel('Date')
#     plt.xlabel('Frequency, MHz')
#     plt.tight_layout()
#     plt.show()
#     plt.close('all')


with np.errstate(divide='ignore', invalid='ignore'):
    rc('font', size=6, weight='bold')
    fig, ax = plt.subplots(1, figsize=(10.0, 6.0))
    im = ax.imshow(np.log10(min_spectra_vs_date / min_filterd_spectra_vs_date),
               vmin=-0.2, vmax=2.0, 
               aspect='auto', interpolation='none', origin='lower', cmap='jet')  # extent=[0, num_samp, fmin, fmax]
    fig.colorbar(im, ax=ax, label='Power level, dB')
    # plt.title(f'RFI Analysis for {df_filename}')
    # plt.xticks(x_values, reduced_frequency)
    ax.set_yticks(y_values, reduced_timeline)
    ax.set_ylim(y_values[0]-0.5, y_values[-1]+0.5)
    text = ax.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = reduced_frequency[k]
    ax.set_xticklabels(text, fontsize=6, fontweight='bold')
    ax.set_ylabel('Dates', fontsize=10, fontweight='bold')
    ax.set_xlabel('Frequency, MHz', fontsize=10, fontweight='bold')
    fig.tight_layout()
    fig.savefig(os.path.join(path_to_results, 'Normalized minimal level of response across all dates - selected range.png'), dpi=350)
    # plt.show()
    plt.close('all')


with np.errstate(divide='ignore', invalid='ignore'):
    rc('font', size=6, weight='bold')
    fig, ax = plt.subplots(1, figsize=(10.0, 6.0))
    im = ax.imshow(np.log10(max_spectra_vs_date / min_filterd_spectra_vs_date),
               vmin=-0.2, vmax=2.0, 
               aspect='auto', interpolation='none', origin='lower', cmap='jet')  # extent=[0, num_samp, fmin, fmax]
    fig.colorbar(im, ax=ax, label='Power level, dB')
    # plt.title(f'RFI Analysis for {df_filename}')
    # plt.xticks(x_values, reduced_frequency)
    ax.set_yticks(y_values, reduced_timeline)
    ax.set_ylim(y_values[0]-0.5, y_values[-1]+0.5)
    text = ax.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = reduced_frequency[k]
    ax.set_xticklabels(text, fontsize=6, fontweight='bold')
    ax.set_ylabel('Dates', fontsize=10, fontweight='bold')
    ax.set_xlabel('Frequency, MHz', fontsize=10, fontweight='bold')
    fig.tight_layout()
    fig.savefig(os.path.join(path_to_results, 'Normalized maximal level of response across all dates - selected range.png'), dpi=350)
    # plt.show()
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
    