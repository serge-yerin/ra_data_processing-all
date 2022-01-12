# Python3
import os
import sys

# Program intended to read and show data from DAT files (needs Timeline.txt as well) with several cuts in time
software_version = '2022.01.11'
software_name = 'DAT multicut data reader'

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Path to data files
path_to_data = 'DATA/'  # ''

timeline_file_name = 'B210622_162805.adr_Timeline.txt'

# Path to intermediate data files and results
path_to_results = os.path.dirname(os.path.realpath(__file__)) + '/'  # Project folder or 'DATA/'

# Types of data to get
# data_types = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm', 'A+B', 'A-B'] # !-!
data_types = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm']

# List of frequencies to build intensity changes vs. time and save to TXT file:
# freq_list = [4.0, 5.0, 6.0, 7.0, 8.0, 8.05, 8.1, 8.15, 8.5, 9.0]
freq_list = []

aver_or_min = 0                    # Use average value (0) per data block or minimum value (1)
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
date_time_start = '2021-06-22 16:28:10'
date_time_stop =  '2021-06-22 16:30:10'
time_step_secs = 180  # step of the cuts in seconds 60 = 1 min, 3600 = 1 h, 86400 = 24 h.
cuts_number = 7       # number of cuts to make

# Begin and end frequency of TXT files to save (MHz)
freq_start_txt = 0.0
freq_stop_txt = 33.0

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import time
from datetime import timedelta

# My libs
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
from package_ra_data_files_formats.f_time_convertions import str_date_and_time_to_datetime

# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


print('\n\n\n\n\n\n\n\n   ****************************************************')
print('   *   ', software_name, '  v.', software_version, '    *      (c) YeS 2022')
print('   **************************************************** \n\n\n')

start_time = time.time()
current_time = time.strftime("%H:%M:%S")
current_date = time.strftime("%d.%m.%Y")
print('   Today is ', current_date, ' time is ', current_time, '\n')


# Search needed files in the directory and subdirectories
file_name_list = find_files_only_in_current_folder(path_to_data, '.txt', 0)


# Find timeline files from TXT files
timeline_file_name_list = [timeline_file_name]


# Find original data file name from timeline file name
data_files_name_list = []
for i in range(len(timeline_file_name_list)):
    data_files_name_list.append(timeline_file_name_list[i][-31:-13])


# Read the time line file and find the time limits
time_line, dt_time_line = time_line_file_reader(path_to_data + timeline_file_name_list[0])


print('\n\n                               Start                           End \n')
print('  File time limits:   ', dt_time_line[0], '   ', dt_time_line[-1], '\n')


# Convert strings dates and times to datetime library objects
dt_start = str_date_and_time_to_datetime(date_time_start)
dt_stop = str_date_and_time_to_datetime(date_time_stop)
dt_time_step_secs = timedelta(0, time_step_secs)


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


print('\n  Seems the time and the number of cuts are selected correctly! \n')
print('\n\n                               Start                           End \n')
print('  File time limits:   ', dt_time_line[0], '\n')
for i in range(cuts_number):
    print('  Chosen time limits: ', str(dt_start_list[i]), '          ', str(dt_stop_list[i]), '')
print('\n  File time limits:                                  ', dt_time_line[-1], '\n\n')


# Loop by time cuts
for cut in range(cuts_number):

    print('\n  * Cut # ', cut+1, ' of ', cuts_number,' from ', dt_start_list[cut], ' till ', dt_stop_list[cut], '\n')

    result_folder_name = data_files_name_list[0] + '_cut_' + \
        str(dt_start_list[cut]).replace(':', '-').replace(' ', '_') + '_-_' + \
        str(dt_stop_list[cut]).replace(':', '-').replace(' ', '_')

    done_or_not = DAT_file_reader(path_to_data, data_files_name_list[0], data_types, '', result_folder_name,
                                  aver_or_min, 1, spec_freq_range, v_min_man, v_max_man, v_min_norm_man, v_max_norm_man,
                                  rfi_mean_const, custom_dpi, colormap, channel_save_txt, channel_save_png,
                                  list_or_all_freqs, amplitude_re_im, freq_start, freq_stop, str(dt_start_list[cut]),
                                  str(dt_stop_list[cut]), freq_start_txt, freq_stop_txt, freq_list, 0)

stop_time = time.time()
print('\n\n\n  The program execution lasted for ',
      round((stop_time - start_time), 2), 'seconds (', round((stop_time - start_time)/60, 2), 'min. ) \n')
print('\n           *** Program ', software_name, ' has finished! *** \n\n\n')
