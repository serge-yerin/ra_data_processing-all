# Python3
software_version = '2019.10.05'
software_name = 'DAT multifile data reader for CasA study'
# Program intended to read and show data from DAT files in special format for
# Cas A secular flux decrease relative interferometric measurements
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Path to data files
path_to_data = '../DATA/'

# Types of data to get
types_of_data = ['CRe', 'CIm']

# List of frequencies to build intensity changes vs. time and save to TXT file:
freq_list_UTR2 = [12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0,
                  28.0, 29.0, 30.0, 31.0, 32.0]
freq_list_GURT = [12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0,
                  28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0,
                  44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0,
                  60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0]

aver_or_min = 0                  # Use average value (0) per data block or minimum value (1)
auto_start_stop = 1              # 1 - calculate depending on source in comment, 0 - use manual values
auto_source_switch = 1           # 1 - find sources in comment, 0 - use manually set source
VminMan = -120                   # Manual lower limit of immediate spectrum figure color range
VmaxMan = -10                    # Manual upper limit of immediate spectrum figure color range
VminNormMan = 0                  # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
VmaxNormMan = 18                 # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
rfi_mean_const = 6               # Constant of RFI mitigation (usually = 8)
list_or_all_freq = 0             # Take all frequencies of a list to save TXT and PNG? 1-All, 0-List
ampl_re_im_UTR2 = 20000 * 10**(-12)
ampl_re_im_GURT = 20 * 10**(-12)

# Begin and end time of dynamic spectrum ('yyyy-mm-dd hh:mm:ss')
date_time_start = '2019-07-19 00:00:00'
date_time_stop =  '2019-07-23 04:00:00'

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
from datetime import datetime, timedelta
from astropy.time import Time, TimeDelta

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_ra_data_files_formats.read_file_header_adr import file_header_adr_read
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_astronomy.culmination_time_utc_astroplan import culmination_time_utc_astroplan


def cut_culmination_times_from_dat(path_to_data, types_of_data, freq_list_UTR2, freq_list_GURT, aver_or_min, 
                                   auto_start_stop, auto_source_switch, VminMan, VmaxMan, VminNormMan, VmaxNormMan, 
                                   rfi_mean_const, list_or_all_freq, ampl_re_im_UTR2, ampl_re_im_GURT,
                                   date_time_start, date_time_stop, freq_start_txt, freq_stop_txt):
    """
    
    """
    # Search needed files in the directory and subdirectories
    file_name_list = find_files_only_in_current_folder(path_to_data, '.txt', 0)

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
    for type_of_data in types_of_data:
        dat_files_list = []
        for i in range(len(data_files_name_list)):
            name = data_files_name_list[i] + '_Data_' + type_of_data + '.dat'
            if os.path.isfile(path_to_data + name):
                dat_files_list.append(name)

        # Loop by DAT files
        for file_no in range(len(dat_files_list)):

            #  *** Find if the file is CasA of SygA ***
            file = open(path_to_data + dat_files_list[file_no], 'rb')

            # Check is it the file of ADR or JDS data
            df_filename = file.read(32).decode('utf-8').rstrip('\x00')      # Initial data file name
            file.close()

            if df_filename[-4:] == '.adr':

                freq_list = freq_list_GURT
                ampl_re_im = ampl_re_im_GURT
                [df_filename, df_filesize, df_system_name, df_obs_place, df_description, clc_freq, df_creation_time_utc,
                 receiver_mode, mode, sum_diff_mode, n_avr, time_res, fmin, fmax, df, frequency, fft_size, s_line, 
                 width, block_size] = file_header_adr_read(path_to_data + dat_files_list[file_no], 0, 0)

            elif df_filename[-4:] == '.jds':  # If data obtained from DSPZ receiver

                freq_list = freq_list_UTR2
                ampl_re_im = ampl_re_im_UTR2
                [df_filename, df_filesize, df_system_name, df_obs_place, df_description, clc_freq, df_creation_time_utc,
                    spec_in_file, receiver_mode, mode, n_avr, time_res, fmin, fmax, df, frequency, freq_points_num,
                    block_size] = file_header_jds_read(path_to_data + dat_files_list[file_no], 0, 0)
            
            else:
                sys.exit('   Error! Wrong file type!')
            
            if auto_source_switch == 1:
                if df_filename[-4:] == '.jds':     # If data obtained from DSPZ receiver
                    '''
                    if '3c461' in df_description.lower() or 'cas' in df_description.lower() or 
                    '461' in df_description.lower():
                        source = '3C461'
                    elif '3c405' in df_description.lower() or 'cyg' in df_description.lower() or 
                    '405' in df_description.lower():
                        source = '3C405'
                    else:
                        print('  Source not detected !!!')
                        source  = str(input(' * Enter source name like 3C405 or 3C461:            '))
                    '''
                    if file_no == 0:
                        source = '3C405'
                    elif file_no == 1:
                        source = '3C461'
                    else:
                        print('  Source not detected !!!')
                        source = str(input(' * Enter source name like 3C405 or 3C461:            '))

                elif df_filename[-4:] == '.adr':
                    if file_no == 0:
                        source = '3C405'
                    elif file_no == 1:
                        source = '3C461'
                    else:
                        print('  Source not detected !!!')
                        source = str(input(' * Enter source name like 3C405 or 3C461:            '))
                else:
                    sys.exit('    Error! Wrong file type!')

            elif auto_source_switch == 0:
                print('\n   !!! Enter source name manually !!!')
                print('   Filename:   ', dat_files_list[file_no])
                source = str(input('   Enter source name like 3C405 or 3C461:            '))
            else:
                sys.exit('Error! auto_source_switch is wrong')

            add = 0
            if type_of_data == 'CIm':
                add = 2

            print('\n\n * File', file_no+1+add, 'of 4:     ', dat_files_list[file_no])
            if auto_source_switch == 1:
                print('   Detected source: ', source, '\n   Description:     ', df_description)
            if auto_source_switch == 0:
                print('   Manual source:   ', source, '\n   Description:     ', df_description)

            # Take the date of the file and find the culmination time of the source

            if auto_start_stop == 1:
                if df_filename[-4:] == '.jds':
                    date = '20' + df_filename[5:7] + '-' + df_filename[3:5] + '-' + df_filename[1:3]
                if df_filename[-4:] == '.adr':
                    date = '20' + df_filename[1:3] + '-' + df_filename[3:5] + '-' + df_filename[5:7]

                culm_time = culmination_time_utc_astroplan(source, date, 0)
                culm_time = Time(culm_time)
                start_obs_time = culm_time - TimeDelta(3600, format='sec')
                end_obs_time = culm_time + TimeDelta(3600, format='sec')

            # *** Reading timeline file ***
            name = path_to_data + data_files_name_list[file_no] + '_Timeline.txt'
            tl_file = open(name, 'r')
            timeline = []
            for line in tl_file:
                timeline.append(str(line))
            tl_file.close()

            # *** Converting text to ".datetime" format ***
            dt_timeline = []
            for i in range(len(timeline)):  # converting text to ".datetime" format

                # Check is the uS field is empty. If so it means it is equal to '000000'
                u_second = timeline[i][20:26]
                if len(u_second) < 2:
                    u_second = '000000'

                dt_timeline.append(datetime(int(timeline[i][0:4]), int(timeline[i][5:7]), int(timeline[i][8:10]),
                                            int(timeline[i][11:13]), int(timeline[i][14:16]), int(timeline[i][17:19]),
                                            int(u_second)))

            if auto_start_stop == 0:  # If switch is off - use manually set time and date
                start_obs_time = datetime(int(date_time_start[0:4]), int(date_time_start[5:7]), 
                                          int(date_time_start[8:10]), int(date_time_start[11:13]), 
                                          int(date_time_start[14:16]), int(date_time_start[17:19]), 0)
                end_obs_time = datetime(int(date_time_stop[0:4]), int(date_time_stop[5:7]), 
                                        int(date_time_stop[8:10]), int(date_time_stop[11:13]), 
                                        int(date_time_stop[14:16]), int(date_time_stop[17:19]), 0)

            # *** Showing the time limits of file and time limits of chosen part
            print('\n                                Start                         End \n')
            print('   File time limits:   ', dt_timeline[0], ' ', dt_timeline[len(timeline)-1], '\n')
            print('   Chosen time limits: ', start_obs_time, '    ', end_obs_time, '\n')

            # Verifying that chosen time limits are inside file and are correct
            if (dt_timeline[len(timeline)-1] >= start_obs_time > dt_timeline[0]) and \
                    (dt_timeline[len(timeline)-1] > end_obs_time >= dt_timeline[0]) and (end_obs_time > start_obs_time):
                print('   Time is chosen correctly! \n\n')
            elif(dt_timeline[len(timeline)-1] >= start_obs_time + TimeDelta(86400, format='sec') > dt_timeline[0]) and \
                    (dt_timeline[len(timeline)-1] > end_obs_time + TimeDelta(86400, format='sec') >= dt_timeline[0]) and \
                    (end_obs_time > start_obs_time):
                start_obs_time = start_obs_time + TimeDelta(86400, format='sec')
                end_obs_time = end_obs_time + TimeDelta(86400, format='sec')
                culm_time = culm_time + TimeDelta(86400, format='sec')
                print('   Time is chosen correctly but adjusted for 1 day ahead! \n')
            else:
                print('   ERROR! Culmination time is calculated chosen out of file limits!!! \n\n')
                sys.exit('           Program stopped! \n\n')

            # DAT_result_path = 'DAT_Results_' + data_files_name_list[file_no]
            if auto_start_stop == 1:
                date_time_start = str(start_obs_time)[0:19]
                date_time_stop = str(end_obs_time)[0:19]
   
            done_or_not = DAT_file_reader(path_to_data, data_files_name_list[file_no], [type_of_data],
                                          path_to_data, data_files_name_list[file_no] + '_' + source,   
                                          aver_or_min, 1, 0, VminMan, VmaxMan, VminNormMan, VmaxNormMan, 
                                          rfi_mean_const, 300, 'jet', 1, 1, list_or_all_freq,
                                          ampl_re_im, 0.0, 30.0, date_time_start, date_time_stop, 
                                          freq_start_txt, freq_stop_txt, freq_list, 0)

            # Saving TXT file with parameters from file header
            path = path_to_data + 'DAT_Results_' + data_files_name_list[file_no]+'_' + source + '/'
            txt_file = open(path + data_files_name_list[file_no] + '_'+source + '_header.info', "w")
            txt_file.write(' Observatory:           ' + df_obs_place + '\n')
            txt_file.write(' Receiver:              ' + df_system_name + '\n')
            txt_file.write(' Initial filename:      ' + df_filename + '\n')
            txt_file.write(' Description:           ' + df_description + '\n')
            txt_file.write(' Source for processing: ' + source + '\n')
            txt_file.write(' Culmination time:      ' + str(culm_time) + '\n')
            txt_file.write(' Receiver mode:         ' + receiver_mode + '\n')
            txt_file.write(' Time resolution:       ' + str(np.round(time_res, 6)) + ' s \n')
            txt_file.write(' Frequency range:       ' + str(fmin) + ' - ' + str(fmax) + ' MHz \n')
            txt_file.write(' Frequency resolution:  ' + str(np.round(df, )) + ' Hz \n')
            txt_file.close()

    return


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':
    
    print('\n\n\n\n\n\n\n\n   *********************************************************************')
    print('   *    ', software_name, '  v.', software_version, '     *      (c) YeS 2019')
    print('   ********************************************************************* \n\n\n')

    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")
    print('   Today is ', current_date, ' time is ', current_time, '\n')

    cut_culmination_times_from_dat(path_to_data, types_of_data, freq_list_UTR2, freq_list_GURT, aver_or_min,
                                   auto_start_stop, auto_source_switch, VminMan, VmaxMan, VminNormMan, VmaxNormMan,
                                   rfi_mean_const, list_or_all_freq, ampl_re_im_UTR2, ampl_re_im_GURT,
                                   date_time_start, date_time_stop, freq_start_txt, freq_stop_txt)

    end_time = time.time()
    print('\n\n\n  The program execution lasted for ',
          round((end_time - start_time), 2), 'seconds (', round((end_time - start_time)/60, 2), 'min. ) \n')
    print('\n           *** Program ', software_name, ' has finished! *** \n\n\n')
