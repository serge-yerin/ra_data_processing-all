# Python3

Software_version = '2023.06.18'
Software_name = 'ADR multifile data reader for CasA study long data'
# Program intended to read and show data from DAT files
import os
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Path to data files
path_to_adr_data = 'f:/2019.07.29_GURT_int_sun_405_461_R_part/'
path_to_store_dat = 'e:/RA_DATA_RESULTS/2019.07.29_GURT_int_sun_405_461_R_part/'
path_to_results = 'e:/RA_DATA_RESULTS/2019.07.29_GURT_int_sun_405_461_R_part/'

# Types of data to get
types_of_data = ['CRe', 'CIm']

# List of frequencies to build intensity changes vs. time and save to TXT file:
freq_list_gurt = [12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0,
                  28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0,
                  44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0,
                  60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0]

print_or_not = True          # Print progress of data processing and figures making (1) or not (0)
aver_or_min = 0              # Use average value (0) per data block or minimum value (1)
start_stop_switch = 1        # Read the whole file (0) or specified time limits (1)
spec_freq_range = 0          # Specify particular frequency range (1) or whole range (0)
VminMan = -120               # Manual lower limit of immediate spectrum figure color range
VmaxMan = -10                # Manual upper limit of immediate spectrum figure color range
VminNormMan = 0              # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
VmaxNormMan = 18             # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
rfi_mean_const = 6           # Constant of RFI mitigation (usually = 8)
custom_dpi = 300             # Resolution of images of dynamic spectra
colormap = 'jet'             # Colormap of images of dynamic spectra ('jet' or 'Greys')
channel_save_txt = 1         # Save intensities at specified frequencies to TXT file
channel_save_png = 1         # Save intensities at specified frequencies to PNG file
list_or_all_freq = 0         # Take all frequencies of a list to save TXT and PNG? 1-All, 0-List
AmplitudeReIm = 20 * 10**(-12)   # Color range of Re and Im dynamic spectra
                                 # 10 * 10**(-12) is typical value for CasA for interferometer of 2 GURT subarrays
AmplitudeReIm_UTR2 = 20000 * 10**(-12)
AmplitudeReIm_GURT = 20 * 10**(-12)

y_auto = 1
v_min = -1500 * 10**(-12)
v_max =  1500 * 10**(-12)
interferometer_base = 0  # 400  # 900

# Begin and end frequency of dynamic spectrum (MHz)
freq_start = 0.0
freq_stop = 10.0

# Begin and end frequency of TXT files to save (MHz)
freq_start_txt = 8.0
freq_stop_txt = 80.0

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import numpy as np
import time
import sys
import os
from os import path
# from datetime import datetime, timedelta
from astropy.time import Time, TimeDelta

# To change system path to the directory where script is running:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.ADR_file_reader import ADR_file_reader
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_ra_data_files_formats.read_file_header_adr import file_header_adr_read
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
from package_astronomy.culmination_time_utc_astroplan import culmination_time_utc_astroplan
from package_cas_a_secular_decrease.f_cas_syg_filter_response_calculate_ratio import \
    filter_interf_response_and_calculate_ratio

# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************
print('\n\n\n\n\n\n\n\n   *************************************************************************')
print('   *  ', Software_name, ' v.', Software_version, '  *  (c) YeS 2019')
print('   ************************************************************************* \n\n\n')

script_start_time = time.time()
current_time = time.strftime("%H:%M:%S")
current_date = time.strftime("%d.%m.%Y")
print('   Today is ', current_date, ' time is ', current_time, '\n')


# Find all files in folder once more:
file_name_list_current = find_files_only_in_current_folder(path_to_adr_data, '.adr', 0)
file_name_list_current.sort()

# Making a name of folder for storing the result figures and txt files
result_folder_name = path_to_adr_data.split('/')[-2]
result_path = path_to_store_dat + 'ADR_Results_' + result_folder_name

for file in range(len(file_name_list_current)):
    file_name_list_current[file] = path_to_adr_data + file_name_list_current[file]

# Run ADR reader for the current folder
done_or_not, DAT_file_name, DAT_file_list = ADR_file_reader(file_name_list_current, result_path, 2048,
                                                            8, -120, -50, 0, 10, -150, -30, 200, 'jet',
                                                            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                                                            0, 0, print_or_not, dat_file_path=path_to_store_dat)


# Search needed files in the directory and subdirectories
file_name_list = find_files_only_in_current_folder(path_to_store_dat, '.txt', 0)

# Find timeline files from TXT files
timeline_file_name_list = []
for i in range(len(file_name_list)):
    if file_name_list[i].endswith('_Timeline.txt'):
        timeline_file_name_list.append(file_name_list[i])

# Find original data file name from timeline file name
data_files_name_list = []
for i in range(len(timeline_file_name_list)):
    data_files_name_list.append(timeline_file_name_list[i][-31:-13])


# Loop by data types selected by user
print('\n Data files found: \n')
dat_files_list = []
for type_of_data in types_of_data:
    name = data_files_name_list[0] + '_Data_' + type_of_data + '.dat'
    print(' - ' + path_to_store_dat + name)
    if os.path.isfile(path_to_store_dat + name):
        dat_files_list.append(name)


# *** Reading timeline file ***
name = path_to_store_dat + timeline_file_name_list[0]
timeline, dt_timeline = time_line_file_reader(name)

# *** Showing the time limits of file
print('\n                                Start                         End \n')
print('   File time limits:   ', dt_timeline[0], ' ', dt_timeline[len(timeline)-1], '\n')


# Number of days in the file
dt_period = dt_timeline[0].date() - dt_timeline[-1].date()
no_of_days = int(abs(dt_period.days))


# Find culminations of both sources within timeline of the file and check the 1-hour gap before and after
culm_time_3C405 = []
culm_time_3C461 = []


print('\n * Calculations of culminations time for all days of observations... \n')


for day in range(no_of_days+1):
    current_time = time.strftime("%H:%M:%S")
    print(' Day # ', str(day+1), ' of ', str(no_of_days+1), '   started at: ', current_time)

    date = str((Time(dt_timeline[0]) + TimeDelta(day * 86400, format='sec')))[0:10]
    culm_time = Time(culmination_time_utc_astroplan('3C405', str(date), 0))
    if (culm_time > Time(dt_timeline[0]) + TimeDelta(3600, format='sec')) and \
            (culm_time < Time(dt_timeline[-1]) - TimeDelta(3600, format='sec')):
        culm_time_3C405.append(culm_time)

    culm_time = Time(culmination_time_utc_astroplan('3C461', str(date), 0))
    if (culm_time > Time(dt_timeline[0]) + TimeDelta(3600, format='sec')) and \
            (culm_time < Time(dt_timeline[-1]) - TimeDelta(3600, format='sec')):
        culm_time_3C461.append(culm_time)

print('\n * Culminations number: ' + str(len(culm_time_3C405)) + ' for 3C405 and ' +
      str(len(culm_time_3C461)) + ' for 3C461 \n')


# In a loop take a two-hour fragments of data and make text files with responses
################################################################################
#                               3C405 Cygnus A                                 #
################################################################################
print('\n * Saving responses for each culmination of 3C405... ')

source = '3C405'
for i in range(len(culm_time_3C405)):
    current_time = time.strftime("%H:%M:%S")
    print('\n Culmination ' + str(culm_time_3C405[i]) + ' # ', str(i+1), ' of ', str(len(culm_time_3C405)),
          '       started at: ', current_time)

    start_time = culm_time_3C405[i] - TimeDelta(3600, format='sec')
    end_time = culm_time_3C405[i] + TimeDelta(3600, format='sec')

    date_time_start = str(start_time)[0:19]
    date_time_stop = str(end_time)[0:19]

    [df_filename, df_filesize, df_system_name, df_obs_place, df_description, clc_freq,
        df_creation_time_utc, receiver_mode, mode, sum_diff_mode, n_avr, time_res,
        fmin, fmax, df, frequency, fft_size, SLine, Width, BlockSize] = \
        file_header_adr_read(path_to_store_dat + dat_files_list[0], 0, 0)

    result_folder = data_files_name_list[0] + '_' + str(i+1) + '_of_' + str(len(culm_time_3C405)) + '_' + source

    done_or_not = DAT_file_reader(path_to_store_dat, data_files_name_list[0], types_of_data, path_to_store_dat,
                                  result_folder, aver_or_min, start_stop_switch, spec_freq_range, VminMan, VmaxMan,
                                  VminNormMan, VmaxNormMan, rfi_mean_const, custom_dpi, colormap,
                                  channel_save_txt, channel_save_png, list_or_all_freq,
                                  AmplitudeReIm_GURT, freq_start, freq_stop,
                                  date_time_start, date_time_stop, freq_start_txt,
                                  freq_stop_txt, freq_list_gurt, False)

    # Saving TXT file with parameters from file header
    path = path_to_store_dat + 'DAT_Results_' + result_folder + '/'
    TXT_file = open(path + data_files_name_list[0] + '_' + source + '_header.info', "w")
    TXT_file.write(' Observatory:           ' + df_obs_place + '\n')
    TXT_file.write(' Receiver:              ' + df_system_name + '\n')
    TXT_file.write(' Initial filename:      ' + df_filename + '\n')
    TXT_file.write(' Description:           ' + df_description + '\n')
    TXT_file.write(' Source for processing: ' + source + '\n')
    TXT_file.write(' Culmination time:      ' + str(culm_time_3C405[i]) + '\n')
    TXT_file.write(' Receiver mode:         ' + receiver_mode + '\n')
    TXT_file.write(' Time resolution:       ' + str(np.round(time_res, 6)) + ' s \n')
    TXT_file.write(' Frequency range:       ' + str(fmin) + ' - ' + str(fmax) + ' MHz \n')
    TXT_file.write(' Frequency resolution:  ' + str(np.round(df, )) + ' Hz \n')
    TXT_file.close()


del start_time, end_time, date_time_start, date_time_stop

# In a loop take a two-hour fragments of data and make text files with responses
################################################################################
#                            3C461 Cassiopeia A                                #
################################################################################

print('\n\n\n * Saving responses for each culmination of 3C461... ')
source = '3C461'
for i in range(len(culm_time_3C461)):
    current_time = time.strftime("%H:%M:%S")
    print('\n Culmination ' + str(culm_time_3C461[i]) + ' # ', str(i+1), ' of ', str(len(culm_time_3C461)),
          '       started at: ', current_time)

    start_time = culm_time_3C461[i] - TimeDelta(3600, format='sec')
    end_time = culm_time_3C461[i] + TimeDelta(3600, format='sec')

    date_time_start = str(start_time)[0:19]
    date_time_stop = str(end_time)[0:19]

    [df_filename, df_filesize, df_system_name, df_obs_place, df_description, clc_freq,
        df_creation_time_utc, receiver_mode, Mode, sum_diff_mode, n_avr, time_res,
        fmin, fmax, df, frequency, fft_size, SLine, Width, BlockSize] = \
        file_header_adr_read(path_to_store_dat + dat_files_list[0], 0, 0)

    result_folder = data_files_name_list[0] + "_" + str(i+1) + '_of_' + str(len(culm_time_3C461)) + '_' + source

    done_or_not = DAT_file_reader(path_to_store_dat, data_files_name_list[0], types_of_data, path_to_store_dat,
                                  result_folder,  aver_or_min, start_stop_switch, spec_freq_range, VminMan, VmaxMan,
                                  VminNormMan, VmaxNormMan, rfi_mean_const, custom_dpi, colormap, 
                                  channel_save_txt, channel_save_png, list_or_all_freq,
                                  AmplitudeReIm_GURT, freq_start, freq_stop, 
                                  date_time_start, date_time_stop, freq_start_txt,
                                  freq_stop_txt, freq_list_gurt, False)

    # Saving TXT file with parameters from file header
    path = path_to_store_dat + 'DAT_Results_' + result_folder + '/'
    TXT_file = open(path + data_files_name_list[0] + '_' + source + '_header.info', "w")
    TXT_file.write(' Observatory:           ' + df_obs_place + '\n')
    TXT_file.write(' Receiver:              ' + df_system_name + '\n')
    TXT_file.write(' Initial filename:      ' + df_filename + '\n')
    TXT_file.write(' Description:           ' + df_description + '\n')
    TXT_file.write(' Source for processing: ' + source + '\n')
    TXT_file.write(' Culmination time:      ' + str(culm_time_3C461[i]) + '\n')
    TXT_file.write(' Receiver mode:         ' + receiver_mode + '\n')
    TXT_file.write(' Time resolution:       ' + str(np.round(time_res, 6)) + ' s \n')
    TXT_file.write(' Frequency range:       ' + str(fmin) + ' - ' + str(fmax) + ' MHz \n')
    TXT_file.write(' Frequency resolution:  ' + str(np.round(df, )) + ' Hz \n')
    TXT_file.close()


filter_interf_response_and_calculate_ratio(path_to_store_dat, y_auto, v_min, v_max, interferometer_base,
                                               160, False)

script_end_time = time.time()
print('\n\n\n  The program execution lasted for ',
      round((script_end_time - script_start_time), 2), 'seconds (',
      round((script_end_time - script_start_time)/60, 2), 'min. ) \n')
print('\n           *** Program ', Software_name, ' has finished! *** \n\n\n')
