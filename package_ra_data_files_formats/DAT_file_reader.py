# Python3
Software_version = '2020.07.17'

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import os
import sys
import numpy as np
import time
from os import path
from datetime import datetime, timedelta
import warnings
import matplotlib
matplotlib.use('agg')
warnings.filterwarnings("ignore")

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_ra_data_files_formats.read_file_header_adr import file_header_adr_read
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
from package_plot_formats.plot_formats import OneDynSpectraPlot, TwoOrOneValuePlot,  OneValueWithTimePlot
from package_ra_data_processing.f_spectra_normalization import normalization_db
from package_cleaning.simple_channel_clean import simple_channel_clean
################################################################################

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************


def DAT_file_reader(dat_file_path, dat_file_name, types_of_data, dat_result_path, result_folder_name,
                    aver_or_min, start_stop_switch, freq_range_switch, v_min_man, v_max_man,
                    v_min_norm_man, v_max_norm_man, rfi_mean_const, custom_dpi, colormap,
                    channel_save_txt, channel_save_png, list_or_all_freqs, amplitude_re_im,
                    freq_start, freq_stop, date_time_start, date_time_stop, freq_start_txt, freq_stop_txt,
                    freq_list, print_or_not):
    """
    Function intended to visualize long spectra '.dat' files of radio astronomy data
    Parameters:
        dat_file_path - path to folder with initial dat files to process
        dat_file_name - a part of dat file name which relates to initial data like "E170519_234344.jds"
        types_of_data - list of strings which indicate types of data to process like "chA", "CRe" etc.
        dat_result_path - path to folder where folders with results will be stored
        result_folder_name - name of the result folder after "'DAT_Results_'"
        aver_or_min - if 0 - use averaging of data bunch, if 1 - use minimal value of a data bunch
        start_stop_switch - set to 1 if you want to specify particular time range to cut out of the data
        freq_range_switch - set to 1 if you want to specify particular frequency range to cut out of the data
        v_min_man -
        v_max_man -
        v_min_norm_man -
        v_max_norm_man -
        rfi_mean_const -
        custom_dpi -
        colormap -
        channel_save_txt -
        channel_save_png -
        list_or_all_freqs -
        amplitude_re_im -
        freq_start -
        freq_stop -
        date_time_start -
        date_time_stop -
        freq_start_txt -
        freq_stop_txt -
        freq_list -
        print_or_not - if 1 - prints to console the detailed info, of 0 - does not print

    Returns:
        ok - an integer indicating everything went well
    """

    current_date = time.strftime("%d.%m.%Y")

    # Files to be analyzed:
    filename = os.path.join(dat_file_path, dat_file_name + '_Data_chA.dat')
    tl_file_name = os.path.join(dat_file_path, dat_file_name + '_Timeline.txt')

    for j in range(len(types_of_data)):  # Main loop by types of data to analyze

        # Current name of DAT file to be analyzed dependent on data type:
        temp = list(filename)
        temp[-7:-4] = types_of_data[j]
        filename = "".join(temp)
        temp = list(dat_file_name + '_Data_chA.dat')
        temp[-7:-4] = types_of_data[j]
        only_file_name = "".join(temp)

        if types_of_data[j] == 'A+B' or types_of_data[j] == 'A-B':
            temp = list(filename)
            temp[-7:-4] = 'chA'
            filename01 = "".join(temp)
            temp[-7:-4] = 'chB'
            filename02 = "".join(temp)
            filename = filename01

        if types_of_data[j] == 'wfA+B':
            temp = list(filename)
            temp[-7:-4] = 'A+B'
            filename = "".join(temp)

        # Print the type of data to be analyzed
        if print_or_not == 1: 
            print('\n\n   Processing data type: ', types_of_data[j], '\n')

        current_time = time.strftime("%H:%M:%S")
        print('   Processing file: ', only_file_name, '   started at: ', current_time)
        if print_or_not == 1: 
            print('\n')

        # *************************************************************
        #          WHAT TO PLOT AND CORRESPONDING PARAMETERS          *
        # *************************************************************

        y_ax_name = 'Intensity, dB'
        label = 'Intensity'
        name_to_add = ''
        filename_to_add = ''
        filename_to_add_norm = ''
        filename_to_add_sp = ''
        v_min = v_min_man              # Switch once more to initial manual settings after changes in previous loop
        v_max = v_max_man
        v_min_norm = v_min_norm_man
        v_max_norm = v_max_norm_man
        if aver_or_min == 0: 
            reducing_type = 'Averaging '
        if aver_or_min == 1: 
            reducing_type = 'Least of '

        if types_of_data[j] == 'chA':
            name_to_add = ' channel A'
            filename_to_add = ''
            filename_to_add_norm = '001_'
            filename_to_add_sp = '008_'

        if types_of_data[j] == 'chB':
            name_to_add = ' channel B'
            filename_to_add = ''
            filename_to_add_norm = '001_'
            filename_to_add_sp = '008_'

        if types_of_data[j] == 'C_m':
            name_to_add = ' cross-spectra module'
            v_min = -160
            v_max_norm = 2 * v_max_norm_man
            filename_to_add = ''
            filename_to_add_norm = '004_'
            filename_to_add_sp = '011_'

        if types_of_data[j] == 'C_p':
            name_to_add = ' cross-spectra phase'
            y_ax_name = 'Phase, rad'
            label = 'Phase'
            v_min = -3.5
            v_max = 3.5
            filename_to_add = '005_'
            filename_to_add_sp = '012_'

        if types_of_data[j] == 'CRe':
            name_to_add = ' cross-spectra RE part'
            y_ax_name = 'Amplitude'
            filename_to_add = '006_'
            filename_to_add_sp = '013_'

        if types_of_data[j] == 'CIm':
            name_to_add = ' cross-spectra IM part'
            y_ax_name = 'Amplitude'
            filename_to_add = '007_'
            filename_to_add_sp = '014_'

        if types_of_data[j] == 'A+B':
            name_to_add = ' sum A + B'
            filename_to_add_norm = '003_'
            filename_to_add_sp = '009_'

        if types_of_data[j] == 'A-B':
            name_to_add = ' difference |A - B|'
            v_min = v_min - 20
            v_max = v_max - 20
            filename_to_add = ''
            filename_to_add_norm = '002_'
            filename_to_add_sp = '010_'

        if types_of_data[j] == 'wfA+B':
            name_to_add = ' wfsum A + B'
            filename_to_add = ''
            filename_to_add_norm = '001_'
            filename_to_add_sp = '008_'

        # *********************************************************************************

        # *** Creating a folder where all pictures and results will be stored (if it doesn't exist) ***
        newpath = os.path.join(dat_result_path, 'DAT_Results_' + result_folder_name)
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        # *** Opening DAT datafile ***
        file = open(filename, 'rb')

        # *** Data file header read ***
        df_filename = file.read(32).decode('utf-8').rstrip('\x00')      # Initial data file name
        file.close()

        if df_filename[-4:] == '.adr':

            [df_filename, df_filesize, df_system_name, df_obs_place, df_description, clock_freq, df_creation_time_utc,
                receiver_mode, mode, sum_diff_mode, n_avr, time_resolution, fmin, fmax, df, frequency, fft_size, s_line,
                width, block_size] = file_header_adr_read(filename, 0, 0)

            freq_points_num = len(frequency)

        elif df_filename[-4:] == '.jds':     # If data obtained from DSPZ receiver

            [df_filename, df_filesize, df_system_name, df_obs_place, df_description, clock_freq, df_creation_time_utc, 
                sp_in_file, receiver_mode, mode, n_avr, time_resolution, fmin, fmax, df, frequency, freq_points_num,
                data_block_size] = file_header_jds_read(filename, 0, 0)

            sum_diff_mode = ''
        else:
            sys.exit('  Unknown file format')
        # ************************************************************************************
        #                             R E A D I N G   D A T A                                *
        # ************************************************************************************

        # # Reading timeline file
        timeline, dt_timeline = time_line_file_reader(tl_file_name)

        if start_stop_switch == 1:  # If we read only specified time limits of files

            dt_date_time_start = datetime(int(date_time_start[0:4]), int(date_time_start[5:7]),
                                          int(date_time_start[8:10]), int(date_time_start[11:13]),
                                          int(date_time_start[14:16]), int(date_time_start[17:19]), 0)

            dt_date_time_stop = datetime(int(date_time_stop[0:4]), int(date_time_stop[5:7]),
                                         int(date_time_stop[8:10]), int(date_time_stop[11:13]),
                                         int(date_time_stop[14:16]), int(date_time_stop[17:19]), 0)

            # *** Showing the time limits of file and time limits of chosen part
            if print_or_not == 1:
                print('\n\n                               Start                         End \n')
                print('  File time limits:   ', dt_timeline[0], ' ', dt_timeline[len(timeline)-1], '\n')
                print('  Chosen time limits: ', dt_date_time_start, '        ', dt_date_time_stop, '\n')

            # Verifying that chosen time limits are inside file and are correct
            if (dt_timeline[len(timeline)-1] >= dt_date_time_start > dt_timeline[0]) and \
                    (dt_timeline[len(timeline)-1] > dt_date_time_stop >= dt_timeline[0]) and \
                    (dt_date_time_stop > dt_date_time_start):
                if print_or_not == 1:  
                    print('  Time is chosen correctly! \n\n')
            else:
                print('  ERROR! Time is chosen out of file limits!!! \n\n')
                sys.exit('           Program stopped')

            # Finding the closest spectra to the chosen time limits
            limit_a = []
            limit_b = []
            for i in range(len(timeline)):
                dt_diff_start = dt_timeline[i] - dt_date_time_start
                dt_diff_stop  = dt_timeline[i] - dt_date_time_stop
                limit_a.append(abs(divmod(dt_diff_start.total_seconds(), 60)[0] * 60 +
                             divmod(dt_diff_start.total_seconds(), 60)[1]))
                limit_b.append(abs(divmod(dt_diff_stop.total_seconds(), 60)[0] * 60 +
                             divmod(dt_diff_stop.total_seconds(), 60)[1]))

            istart = limit_a.index(min(limit_a))
            istop = limit_b.index(min(limit_b))
            del limit_a, limit_b
            if print_or_not == 1:
                print(' Start spectrum number is:         ', istart)
                print(' Stop spectrum number is:          ', istop)
                print(' Total number of spectra to read:  ', istop - istart)
        else:
            istart = 0
            istop = len(timeline)

        # Calculation of the dimensions of arrays to read
        nx = len(frequency)                  # the first dimension of the array
        if start_stop_switch == 1:             # If we read only specified time limits of files
            ny = int(istop - istart)         # the second dimension of the array: number of spectra to read
        else:
            ny = int(((df_filesize-1024)/(nx*8)))  # the second dimension of the array: file size - 1024 bytes
            # istart = 0
            # istop = len(timeline)

        if print_or_not == 1:
            print(' Number of frequency channels:     ', nx)
            print(' Number of spectra:                ', ny)
            print(' Recommended spectra number for averaging is: ', int(ny/1024))
        # average_const = raw_input('\n Enter number of spectra to be averaged:       ')

        # if (len(average_const) < 1 or int(average_const) < 1):
        #    average_const = 1
        # else:
        #    average_const = int(average_const)
        average_const = int(ny/1024)
        if int(average_const) < 1:
            average_const = 1

        # Data reading and averaging 
        if print_or_not == 1: 
            print('\n\n\n  *** Data reading and averaging *** \n\n')

        file1 = open(filename, 'rb')
        if types_of_data[j] == 'A+B' or types_of_data[j] == 'A-B': 
            file2 = open(filename02, 'rb')

        file1.seek(1024+istart*8*nx, os.SEEK_SET)  # Jumping to 1024+number of spectra to skip byte from file beginning
        if types_of_data[j] == 'A+B' or types_of_data[j] == 'A-B': 
            file2.seek(1024+istart*8*nx, os.SEEK_SET)   

        array = np.empty((nx, 0), float)
        num_of_blocks = int(ny/average_const)
        for block in range(num_of_blocks):

            data1 = np.fromfile(file1, dtype=np.float64, count=nx * average_const)
            if types_of_data[j] == 'A+B' or types_of_data[j] == 'A-B': 
                data2 = np.fromfile(file2, dtype=np.float64, count=nx * average_const)

            if types_of_data[j] == 'A+B' or types_of_data[j] == 'A-B':
                if types_of_data[j] == 'A+B': 
                    data = data1 + data2
                if types_of_data[j] == 'A-B': 
                    data = data1 - data2
            else:
                data = data1

            del data1
            if types_of_data[j] == 'A+B' or types_of_data[j] == 'A-B': 
                del data2

            data = np.reshape(data, [nx, average_const], order='F')

            data_append = np.empty((nx, 1), float)

            if types_of_data[j] == 'chA' or types_of_data[j] == 'chB' or \
                    types_of_data[j] == 'A+B' or types_of_data[j] == 'wfA+B':
                # If analyzing intensity - average and log data
                if aver_or_min == 0:
                    with np.errstate(invalid='ignore'):
                        data_append[:, 0] = 10 * np.log10(data.mean(axis=1)[:])
                elif aver_or_min == 1:
                    with np.errstate(invalid='ignore'):
                        data_append[:, 0] = 10 * np.log10(np.amin(data, axis=1)[:])
                else:
                    print('\n\n Error!!! Wrong value of parameters!')
                array = np.append(array, data_append, axis=1)
                array[np.isnan(array)] = -120

            if types_of_data[j] == 'A-B':
                # If analyzing intensity - average and log absolute values of data
                with np.errstate(invalid='ignore'):
                    data_append[:, 0] = 10 * np.log10(np.abs(data.mean(axis=1)[:]))
                array = np.append(array, data_append, axis=1)
                array[np.isnan(array)] = -120

            if types_of_data[j] == 'C_p' or types_of_data[j] == 'CRe' or types_of_data[j] == 'CIm':
                # If analyzing phase of Re/Im we do not log data, only averaging
                data_append[:, 0] = (data.mean(axis=1)[:])
                array = np.append(array, data_append, axis=1)
                array[np.isnan(array)] = 0

            if types_of_data[j] == 'C_m':
                data_append[:, 0] = (data.mean(axis=1)[:])
                array = np.append(array, data_append, axis=1)
                # array[np.isinf(array)] = -120

            del data_append, data
        file1.close()
        if types_of_data[j] == 'A+B' or types_of_data[j] == 'A-B': 
            file2.close()

        if print_or_not == 1:
            print('\n Array shape is now             ', array.shape)

        # *** Cutting timeline to time limits ***
        date_time_new = timeline[istart:istop:average_const]
        del date_time_new[num_of_blocks:]
        if print_or_not == 1:
            print('\n TimeLine length is now:        ', len(date_time_new))

    # *******************************************************************************
    #                                 F I G U R E S                                 *
    # *******************************************************************************

        if print_or_not == 1:
            print('\n\n\n  *** Building images *** \n\n')

        # Exact string timescales to show on plots
        time_scale_fig = np.empty_like(date_time_new)
        for i in range(len(date_time_new)):
            time_scale_fig[i] = str(date_time_new[i][0:11] + '\n' + date_time_new[i][11:23])

        # Limits of figures for common case or for Re/Im parts to show the interferometric picture
        if types_of_data[j] == 'CRe' or types_of_data[j] == 'CIm':
            v_min = 0 - amplitude_re_im
            v_max = 0 + amplitude_re_im

        # *** Immediate spectrum ***

        plot_suptitle = ('Immediate spectrum ' + str(df_filename[0:18]) + ' ' + name_to_add)
        plot_title = ('Initial parameters: dt = ' + str(round(time_resolution, 3)) + ' Sec, df = ' +
                      str(round(df/1000, 3)) + ' kHz ' + sum_diff_mode + 'Processing: ' + reducing_type +
                      str(average_const) + ' spectra (' + str(round(average_const * time_resolution, 3)) + ' sec.)')

        TwoOrOneValuePlot(1, frequency, array[:,[1]], [], 'Spectrum', ' ', frequency[0], frequency[-1], v_min, v_max,
                          v_min, v_max, 'Frequency, MHz', y_ax_name, ' ', plot_suptitle, plot_title,
                          newpath + '/' + filename_to_add_sp + df_filename[0:14] + '_'+types_of_data[j] +
                          ' Immediate Spectrum full.png', current_date, current_time, Software_version)

        # *** Decide to use only list of frequencies or all frequencies in range
        if list_or_all_freqs == 0:
            freq_list = np.array(freq_list)
        if list_or_all_freqs == 1:
            freq_list = np.array(frequency)

        # *** Finding frequency most close to specified by user ***
        for fc in range(len(freq_list)):
            if (freq_list[fc] > freq_start_txt) and (freq_list[fc] < freq_stop_txt):
                new_freq = np.array(frequency)
                new_freq = np.absolute(new_freq - freq_list[fc])
                index = np.argmin(new_freq) + 1
                # tempArr1 = np.arrange(0, len(date_time_new), 1)

                if channel_save_png == 1 or types_of_data[j] == 'CRe' or types_of_data[j] == 'CIm':
                    if types_of_data[j] == 'CRe' or types_of_data[j] == 'CIm':
                        v_min = 0 - amplitude_re_im
                        v_max = 0 + amplitude_re_im

                    # *** Plotting intensity changes at particular frequency ***
                    timeline = []
                    for i in range(len(date_time_new)):
                        timeline.append(str(date_time_new[i][0:11] + '\n' + date_time_new[i][11:23]))

                    plot_suptitle = 'Intensity variation ' + str(df_filename[0:18]) + ' ' + name_to_add
                    plot_title = ('Initial parameters: dt = ' + str(round(time_resolution, 3)) + ' Sec, df = ' +
                                  str(round(df/1000, 3)) + ' kHz, Frequency = ' + str(round(frequency[index], 3)) +
                                  ' MHz ' + sum_diff_mode + ' Processing: ' + reducing_type + str(average_const) +
                                  ' spectra (' + str(round(average_const*time_resolution, 3)) + ' sec.)')

                    file_name = (newpath + '/' + df_filename[0:14] + '_' + types_of_data[j] + df_filename[-4:] +
                                 ' variation at ' + str(round(frequency[index], 3)) + ' MHz.png')

                    OneValueWithTimePlot(timeline, array[[index],:].transpose(), label, 0, len(date_time_new),
                                         v_min, v_max, 0, 0, 'UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', y_ax_name,
                                         plot_suptitle, plot_title, file_name, current_date, current_time,
                                         Software_version)

                # Saving value changes at particular frequency to TXT file
                if channel_save_txt == 1:
                    single_channel_data = open(newpath + '/' + df_filename[0:14] + '_' + filename[-7:-4:]
                                               + df_filename[-4:] + ' variation at ' + str(round(frequency[index], 3)) +
                                               ' MHz.txt', "w")
                    for i in range(len(date_time_new)):
                        single_channel_data.write(str(date_time_new[i]).rstrip() + '   ' +
                                                  str(array.transpose()[i, index]) + ' \n')
                    single_channel_data.close()

        # Cutting the array inside frequency range specified by user
        if freq_range_switch == 1 and (frequency[0] <= freq_start <= frequency[freq_points_num-1]) and \
                (frequency[0] <= freq_stop <= frequency[freq_points_num-1]) and (freq_start < freq_stop):

            print('\n You have chosen the frequency range', freq_start, '-', freq_stop, 'MHz')
            limit_a = []
            limit_b = []
            for i in range(len(frequency)):
                limit_a.append(abs(frequency[i] - freq_start))
                limit_b.append(abs(frequency[i] - freq_stop))
            ifmin = limit_a.index(min(limit_a))
            ifmax = limit_b.index(min(limit_b))
            array = array[ifmin:ifmax, :]
            print('\n New data array shape is: ', array.shape)
            freq_line = frequency[ifmin:ifmax]
            del limit_a, limit_b
        else:
            freq_line = frequency

        #####################################################################################
        if freq_range_switch == 1:
            # *** Immediate spectrum in narrow frequency range ***

            plot_suptitle = ('Immediate spectrum ' + str(df_filename[0:18]) + ' ' + name_to_add)
            plot_title = ('Initial parameters: dt = ' + str(round(time_resolution, 3)) + ' Sec, df = ' +
                          str(round(df / 1000, 3)) +
                          ' kHz ' + sum_diff_mode + 'Processing: ' + reducing_type + str(average_const) +
                          ' spectra (' + str(round(average_const * time_resolution, 3)) + ' sec.)')

            TwoOrOneValuePlot(1, freq_line, array[:, [1]], [],
                              'Spectrum', ' ', freq_line[0], freq_line[-1], v_min, v_max, v_min, v_max,
                              'Frequency, MHz', y_ax_name, ' ', plot_suptitle, plot_title,
                              newpath + '/' + filename_to_add_sp + df_filename[0:14] + '_' +
                              types_of_data[j] + ' Immediate Spectrum narrow range.png',
                              current_date, current_time, Software_version)
        #####################################################################################

        # Limits of figures for common case or for Re/Im parts to show the interferometric picture
        v_min = np.min(array)
        v_max = np.max(array)
        if types_of_data[j] == 'CRe' or types_of_data[j] == 'CIm':
            v_min = 0 - amplitude_re_im
            v_max = 0 + amplitude_re_im

        # Dynamic spectrum of initial signal

        plot_suptitle = ('Dynamic spectrum starting from file ' + str(df_filename[0:18]) + ' ' + name_to_add +
                         '\n Initial parameters: dt = ' + str(round(time_resolution, 3)) +
                         ' Sec, df = ' + str(round(df/1000, 3)) + ' kHz, ' + sum_diff_mode +
                         ' Processing: ' + reducing_type + str(average_const) + ' spectra (' +
                         str(round(average_const * time_resolution, 3)) + ' sec.)\n' +
                         ' Receiver: ' + str(df_system_name) + ', Place: ' + str(df_obs_place) +
                         ', Description: ' + str(df_description))
        
        fig_file_name = (newpath + '/' + filename_to_add + df_filename[0:14]+'_' + 
                         types_of_data[j] + ' Dynamic spectrum.png')

        OneDynSpectraPlot(array, v_min, v_max, plot_suptitle, 'Intensity, dB', len(date_time_new), time_scale_fig,
                          freq_line, len(freq_line), colormap, 'UTC Date and time, YYYY-MM-DD HH:MM:SS.msec', 
                          fig_file_name, current_date, current_time, Software_version, custom_dpi)

        if types_of_data[j] != 'C_p' and types_of_data[j] != 'CRe' and types_of_data[j] != 'CIm':
            # Normalization and cleaning of dynamic spectra 
            normalization_db(array.transpose(), len(freq_line), len(date_time_new))
            simple_channel_clean(array.transpose(), rfi_mean_const)

            # *** Dynamic spectra of cleaned and normalized signal ***

            plot_suptitle = ('Dynamic spectrum cleaned and normalized starting from file ' + str(df_filename[0:18]) +
                             ' ' + name_to_add + '\n Initial parameters: dt = ' + str(round(time_resolution, 3)) +
                             ' Sec, df = ' + str(round(df/1000, 3)) + ' kHz, ' + sum_diff_mode +
                             ' Processing: ' + reducing_type + str(average_const) + ' spectra (' +
                             str(round(average_const * time_resolution, 3)) +
                             ' sec.)\n' + ' Receiver: ' + str(df_system_name) +
                             ', Place: ' + str(df_obs_place) + ', Description: ' + str(df_description))
            fig_file_name = (newpath + '/' + filename_to_add_norm + df_filename[0:14] + '_' + types_of_data[j] +
                             ' Dynamic spectrum cleaned and normalized' + '.png')

            OneDynSpectraPlot(array, v_min_norm, v_max_norm, plot_suptitle, 'Intensity, dB', len(date_time_new), 
                              time_scale_fig, freq_line, len(freq_line), colormap, 
                              'UTC Date and time, YYYY-MM-DD HH:MM:SS.msec',
                              fig_file_name, current_date, current_time, Software_version, custom_dpi)

            '''
            # *** TEMPLATE FOR JOURNLS Dynamic spectra of cleaned and normalized signal ***
            plt.figure(2, figsize=(16.0, 7.0))
            ImA = plt.imshow(np.flipud(array), aspect='auto', extent=[0,len(date_time_new),freq_line[0],
                             freq_line[len(freq_line)-1]], vmin=v_min_norm, vmax=v_max_norm, cmap=colormap) #
            plt.ylabel('Frequency, MHz', fontsize=12, fontweight='bold')
            #plt.suptitle('Dynamic spectrum cleaned and normalized starting from file ' + str(df_filename[0:18]) + 
            #            ' ' + name_to_add +
            #            '\n Initial parameters: dt = '+str(round(time_resolution,3))+
            #            ' Sec, df = '+str(round(df/1000,3))+' kHz, '+sum_diff_mode+
            #            ' Processing: ' + reducing_type + str(average_const) + 
            #            ' spectra ('+str(round(average_const*time_resolution,3))+' sec.)\n'+
            #            ' Receiver: '+str(df_system_name)+
            #            ', Place: '+str(df_obs_place) +
            #            ', Description: '+str(df_description),
            #            fontsize=10, fontweight='bold', x = 0.46, y = 0.96)
            plt.yticks(fontsize=12, fontweight='bold')
            rc('font', weight='bold')
            cbar = plt.colorbar(ImA, pad=0.005)
            cbar.set_label('Intensity, dB', fontsize=12, fontweight='bold')
            cbar.ax.tick_params(labelsize=12)
            ax1 = plt.figure(2).add_subplot(1,1,1)
            a = ax1.get_xticks().tolist()
            for i in range(len(a)-1):   #a-1
                k = int(a[i])
                #a[i] = str(date_time_new[k][0:11]+'\n'+date_time_new[k][11:23])
                a[i] = str(date_time_new[k][11:19])
            ax1.set_xticklabels(a)
            plt.xticks(fontsize=12, fontweight='bold')
            plt.xlabel('UTC time, HH:MM:SS', fontsize=12, fontweight='bold')
            #plt.text(0.72, 0.04,'Processed '+current_date+ ' at '+current_time, fontsize=6, 
            transform=plt.gcf().transFigure)
            pylab.savefig('DAT_Results/' + filename_to_add_norm + df_filename[0:14]+'_'+types_of_data[j]+
            ' Dynamic spectrum cleaned and normalized'+'.png', bbox_inches='tight', dpi = custom_dpi)
            #pylab.savefig('DAT_Results/' +filename_to_add_norm+ df_filename[0:14]+'_'+types_of_data[j]+ 
            ' Dynamic spectrum cleaned and normalized'+'.eps', bbox_inches='tight', dpi = custom_dpi)
                                                                                 #filename[-7:-4:]
            plt.close('all')
            '''
    ok = 1
    return ok

# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    dat_file_path = 'DATA/'
    result_path = ''
    dat_file_name = ''
    types_of_data = ['chA, chB']
    dat_result_path = ''
    result_folder_name = ''
    start_stop_switch = 0
    freq_range_switch = 0
    rfi_mean_const = 8  # Constant of RFI mitigation (usually 8)
    aver_or_min = 0  # Use average value (0) per data block or minimum value (1)
    v_min_man = -120  # Manual lower limit of immediate spectrum figure color range
    v_max_man = -10  # Manual upper limit of immediate spectrum figure color range
    v_min_norm_man = 0  # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
    v_max_norm_man = 12  # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
    amplitude_re_im = 1 * 10 ** (-12)  # Color range of Re and Im dynamic spectra
    # 10 * 10**(-12) is typical value enough for CasA for interferometer of 2 GURT subarrays
    custom_dpi = 200  # Resolution of images of dynamic spectra
    colormap = 'jet'  # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
    channel_save_txt = 0
    channel_save_png = 0
    list_or_all_freqs = 0
    freq_start = 0
    freq_stop = 0
    date_time_start = ''
    date_time_stop = ''
    freq_start_txt = 0
    freq_stop_txt = 0
    freq_list = []
    print_or_not = 1

    ok = DAT_file_reader(dat_file_path, dat_file_name, types_of_data, dat_result_path, result_folder_name,
                         aver_or_min, start_stop_switch, freq_range_switch, v_min_man, v_max_man,
                         v_min_norm_man, v_max_norm_man, rfi_mean_const, custom_dpi, colormap,
                         channel_save_txt, channel_save_png, list_or_all_freqs,
                         amplitude_re_im, freq_start, freq_stop, date_time_start, date_time_stop,
                         freq_start_txt, freq_stop_txt, freq_list, print_or_not)
