# Python3
import sys

software_version = '2022.01.11'  # ######## NOT FINISHED !!! ############
software_name = 'DAT multicut data reader'
# Program intended to read and show data from DAT files (needs Timeline.txt as well) with several cuts in time
import os
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Path to data files
path_to_data = 'DATA/'  # ''

timeline_file_name = 'A190904_211631.adr_Timeline.txt'

# Path to intermediate data files and results
path_to_results = os.path.dirname(os.path.realpath(__file__)) + '/'  # Project folder or 'DATA/'

# Types of data to get
# data_types = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm', 'A+B', 'A-B'] # !-!
data_types = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm']

# List of frequencies to build intensity changes vs. time and save to TXT file:
# freq_list = [10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0]
# freq_list = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
freq_list = [4.0, 5.0, 6.0, 7.0, 8.0, 8.05, 8.1, 8.15, 8.5, 9.0]

aver_or_min = 0                    # Use average value (0) per data block or minimum value (1)
start_stop_switch = 0              # Read the whole file (0) or specified time limits (1)
spec_freq_range = 0                # Specify particular frequency range (1) or whole range (0)
v_min_man = -120                   # Manual lower limit of immediate spectrum figure color range
v_max_man = -10                    # Manual upper limit of immediate spectrum figure color range
v_min_norm_man = 0                 # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
v_max_norm_man = 12                # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
rfi_mean_const = 6                 # Constant of RFI mitigation (usually = 8)
custom_dpi = 300                   # Resolution of images of dynamic spectra
colormap = 'jet'                   # Colormap of images of dynamic spectra ('jet' or 'Greys')
channel_save_txt = 0               # Save intensities at specified frequencies to TXT file
channel_save_png = 0               # Save intensities at specified frequencies to PNG file
list_or_all_freqs = 0              # Take all frequencies of a list to save TXT and PNG? 1-All, 0-List
amplitude_re_im = 200000 * 10**(-12)  # Color range of Re and Im dynamic spectra
                                      # 10 * 10**(-12) is typical value for CasA for interferometer of 2 GURT subarrays

# Begin and end frequency of dynamic spectrum (MHz)
freq_start = 0.0
freq_stop = 10.0

# Begin and end time of dynamic spectrum first cut ('yyyy-mm-dd hh:mm:ss')
date_time_start = '2019-07-19 00:00:00'
date_time_stop =  '2019-07-23 04:00:00'
time_step_secs = 60  # step of the cuts in seconds 60 = 1 min, 3600 = 1 h, 86400 = 24 h.
cuts_number = 2      # number of cuts to make

# Begin and end frequency of TXT files to save (MHz)
freq_start_txt = 0.0
freq_stop_txt = 33.0

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import time
from datetime import datetime, timedelta

# My functions
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************

print('\n\n\n\n\n\n\n\n   ****************************************************')
print('   *   ', software_name, '  v.', software_version, '    *      (c) YeS 2019')
print('   **************************************************** \n\n\n')

start_time = time.time()
current_time = time.strftime("%H:%M:%S")
current_date = time.strftime("%d.%m.%Y")
print('   Today is ', current_date, ' time is ', current_time, '\n')


# Search needed files in the directory and subdirectories
file_name_list = find_files_only_in_current_folder(path_to_data, '.txt', 0)


# Find timeline files from TXT files
timeline_file_name_list = [timeline_file_name]
# for i in range(len(file_name_list)):
#     if file_name_list[i].endswith('_Timeline.txt'):
#         timeline_file_name_list.append(file_name_list[i])


# Find original data file name from timeline file name
data_files_name_list = []
for i in range(len(timeline_file_name_list)):
    data_files_name_list.append(timeline_file_name_list[i][-31:-13])


# print(' * Number of datasets (time line files) found: ', len(timeline_file_name_list), '\n')

# Read the time line file and find the time limits
time_line, dt_time_line = time_line_file_reader(path_to_data + timeline_file_name_list[0])


print('\n\n                               Start                           End \n')
print('  File time limits:   ', dt_time_line[0], '   ', dt_time_line[-1], '\n')
# print('  Chosen time limits: ', dt_dateTimeStart, '        ', dt_dateTimeStop, '\n')


date_time_start = '2019-07-19 00:00:00'
date_time_stop =  '2019-07-23 04:00:00'
time_step_secs = 60  # step of the cuts in seconds 60 = 1 min, 3600 = 1 h, 86400 = 24 h.
cuts_number = 2      # number of cuts to make


def str_date_and_time_to_datetime(str_date_time):
    """Converts string notation of date and time to datetime object"""
    datetime_date_time = datetime(int(str_date_time[0:4]), int(str_date_time[5:7]), int(str_date_time[8:10]),
                                  int(str_date_time[11:13]), int(str_date_time[14:16]), int(str_date_time[17:19]), 0)
    return datetime_date_time


# Convert strings dates and times to datetime library objects
dt_start = str_date_and_time_to_datetime(date_time_start)
dt_stop = str_date_and_time_to_datetime(date_time_stop)
dt_time_step_secs = timedelta(0, time_step_secs)
# file_begin_time = str_date_and_time_to_datetime(dt_time_line[0])
# file_end_time = str_date_and_time_to_datetime(dt_time_line[-1])

# Create lists of cuts begins and ends time
dt_start_list, dt_stop_list = [], []
for i in range(cuts_number):
    dt_start_list.append(dt_start + i * dt_time_step_secs)
    dt_stop_list.append(dt_stop + i * dt_time_step_secs)

# Check if time of the first cut begin is after the file time begin
if dt_start_list[0] < dt_time_line[0]:
    sys.exit('\n  ERROR! First cut start time is before the file begin time! \n')
# Check if time of the last cut end is before the file time end
if dt_stop_list[-1] > dt_time_line[-1]:
    sys.exit('\n  ERROR! First cut start time is before the file begin time! \n')

# Check if the time of next cut begin is after previous cut end


input()

# Loop by data types selected by user
for file_no in range(len(data_files_name_list)):
    print('   Dataset No: ', file_no + 1, ' of ', len(timeline_file_name_list), '\n')
    dat_types_list = []
    for type_of_data in range(len(data_types)):
        name = data_files_name_list[file_no] + '_Data_' + data_types[type_of_data] + '.dat'
        if os.path.isfile(path_to_data + name):
            dat_types_list.append(data_types[type_of_data])

    result_folder_name = data_files_name_list[file_no]

    done_or_not = DAT_file_reader(path_to_data, data_files_name_list[file_no], dat_types_list, '', result_folder_name,
                                  aver_or_min, start_stop_switch, spec_freq_range, v_min_man, v_max_man, v_min_norm_man,
                                  v_max_norm_man, rfi_mean_const, custom_dpi, colormap, channel_save_txt,
                                  channel_save_png, list_or_all_freqs, amplitude_re_im, freq_start, freq_stop,
                                  date_time_start, date_time_stop, freq_start_txt, freq_stop_txt, freq_list, 0)

stop_time = time.time()
print('\n\n\n  The program execution lasted for ',
      round((stop_time - start_time), 2), 'seconds (', round((stop_time - start_time)/60, 2), 'min. ) \n')
print('\n           *** Program ', software_name, ' has finished! *** \n\n\n')
