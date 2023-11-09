# Python3
Software_version = '2019.05.09'
# Program intended to read, show and analyze data from DSPZ receivers
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import os
import math
import numpy as np
import time
import gc
import datetime
from datetime import datetime, timedelta

# My functions
from package_plot_formats.plot_formats import TwoDynSpectraPlot, TwoOrOneValuePlot
from package_ra_data_processing.f_spectra_normalization import normalization_db
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_ra_data_files_formats.FPGA_to_PC_array import FPGAtoPCarrayJDS
from package_cleaning.simple_channel_clean import simple_channel_clean

# *******************************************************************************
#                         M A I N    F U N C T I O N                            *
# *******************************************************************************


def JDS_file_reader(file_list, result_path, max_sp_num, sp_skip, rfi_mean_const, v_min, v_max, v_min_norm, v_max_norm, 
                    v_min_corr_mag, v_max_corr_mag, colormap, custom_dpi, corr_process, 
                    long_file_save_ch_a, long_file_save_ch_b, long_file_save_cri, long_file_save_cmp,
                    dyn_spec_save_initial, dyn_spec_save_cleaned, corr_spectr_save_initial, corr_spectr_save_cleaned, 
                    spectra_file_save_switch, immediate_sp_no, dat_files_path='',
                    long_file_save_channels_sum=False, long_file_save_channels_diff=False, print_or_not=True):
    
    # current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")

    # *** Creating a folder where all pictures and results will be stored (if it doesn't exist) ***
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    if not os.path.exists(result_path + '/Service'):
        os.makedirs(result_path + '/Service')
    if dyn_spec_save_initial == 1:
        if not os.path.exists(result_path + '/Initial_spectra'):
            os.makedirs(result_path + '/Initial_spectra')
    if dyn_spec_save_cleaned == 1 and corr_process == 1:
        if not os.path.exists(result_path + '/Correlation_spectra'):
            os.makedirs(result_path + '/Correlation_spectra')

    print('\n JDS File reader: \n')
    print('  Data folder: ', "/".join(file_list[0].split('/')[:-1]), '\n')

    # Main loop
    for file_no in range(len(file_list)):   # loop by files
        print('  * ', str(datetime.now())[:19], ' File ',  str(file_no+1), ' of ', str(len(file_list)),
              ' : ', str(file_list[file_no].split('/')[-1]))

    # *********************************************************************************

        # *** Opening datafile ***
        fname = ''
        if len(fname) < 1: 
            fname = file_list[file_no]

        # *** Data file header read ***
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
            clc_freq, df_creation_time_utc, sp_in_file, receiver_mode, mode, n_avr, time_resol, fmin, fmax,
            df, frequency, freq_points_num, data_block_size] = file_header_jds_read(fname, 0, 0)

        # Initial time line settings
        time_scale_start_date = datetime(int(df_creation_time_utc[0:4]), int(df_creation_time_utc[5:7]), 
                                         int(df_creation_time_utc[8:10]), 0, 0, 0, 0)

        # timeLineMS = np.zeros(int(sp_in_file))  # List of ms values from ends of spectra

        # *** Creating a name for long timeline TXT file ***
        if file_no == 0 and (long_file_save_ch_a == 1 or long_file_save_ch_b == 1 or 
                             long_file_save_cri == 1 or long_file_save_cmp == 1):
            tl_file_name = dat_files_path + df_filename + '_Timeline.txt'
            tl_file = open(tl_file_name, 'wb')  # Open and close to delete the file with the same name
            tl_file.close()

        with open(fname, 'rb') as file:

            # *** If it is the first file - write the header to long data file
            if((long_file_save_ch_a == 1 or long_file_save_ch_b == 1 or long_file_save_cri == 1 or 
                    long_file_save_cmp == 1) and file_no == 0):
                file.seek(0)
                file_header = file.read(1024)

                dat_file_name = df_filename
                dat_file_list = []

                # *** Creating a binary file with data for long data storage ***
                if(mode == 1 or mode == 2) and long_file_save_ch_a == 1:
                    data_a_file_name = dat_files_path + df_filename+'_Data_chA.dat'
                    data_a_file = open(data_a_file_name, 'wb')
                    data_a_file.write(file_header)
                    data_a_file.close()
                    dat_file_list.append('chA')
                if long_file_save_ch_b == 1 and (mode == 1 or mode == 2):
                    data_b_file_name = dat_files_path + df_filename+'_Data_chB.dat'
                    data_b_file = open(data_b_file_name, 'wb')
                    data_b_file.write(file_header)
                    data_b_file.close()
                    dat_file_list.append('chB')
                if long_file_save_channels_sum is True and (mode == 1 or mode == 2):
                    data_sum_file_name = dat_files_path + df_filename+'_Data_A+B.dat'
                    data_sum_file = open(data_sum_file_name, 'wb')
                    data_sum_file.write(file_header)
                    data_sum_file.close()
                    dat_file_list.append('A+B')
                if long_file_save_channels_diff is True and (mode == 1 or mode == 2):
                    data_diff_file_name = dat_files_path + df_filename+'_Data_A-B.dat'
                    data_diff_file = open(data_diff_file_name, 'wb')
                    data_diff_file.write(file_header)
                    data_diff_file.close()
                    dat_file_list.append('A-B')
                if long_file_save_cri == 1 and corr_process == 1 and mode == 2:
                    data_cre_name = dat_files_path + df_filename+'_Data_CRe.dat'
                    data_cre_file = open(data_cre_name, 'wb')
                    data_cre_file.write(file_header)
                    data_cre_file.close()
                    dat_file_list.append('CRe')
                    data_cim_name = dat_files_path + df_filename+'_Data_CIm.dat'
                    data_cim_file = open(data_cim_name, 'wb')
                    data_cim_file.write(file_header)
                    data_cim_file.close()
                    dat_file_list.append('CIm')
                if long_file_save_cmp == 1 and corr_process == 1 and mode == 2:
                    data_cm_name = dat_files_path + df_filename+'_Data_C_m.dat'
                    data_cm_file = open(data_cm_name, 'wb')
                    data_cm_file.write(file_header)
                    data_cm_file.close()
                    dat_file_list.append('C_m')
                    data_cp_name = dat_files_path + df_filename+'_Data_C_p.dat'
                    data_cp_file = open(data_cp_name, 'wb')
                    data_cp_file.write(file_header)
                    data_cp_file.close()
                    dat_file_list.append('C_p')

                del file_header

    # *******************************************************************************
    #                          R E A D I N G   D A T A                              *
    # *******************************************************************************

            file.seek(1024)  # Jumping to 1024 byte from file beginning
            if mode == 0:
                print('\n\n  Data in waveform mode, use appropriate program!!! \n\n\n')

            if 0 < mode < 3:           # Spectra modes
                fig_id = -1
                fig_max = int(math.ceil((sp_in_file - sp_skip)/max_sp_num))
                if fig_max < 1: 
                    fig_max = 1
                for fig in range(fig_max):
                    fig_id = fig_id + 1
                    current_time = time.strftime("%H:%M:%S")
                    if print_or_not:
                        print(' File # ', str(file_no+1), ' of ', str(len(file_list)), ', figure # ', fig_id+1,
                              ' of ', fig_max, '   started at: ', current_time)
                    if (sp_in_file - sp_skip - max_sp_num * fig_id) < max_sp_num:
                        n_sp = int(sp_in_file - sp_skip - max_sp_num * fig_id)
                    else:
                        n_sp = max_sp_num

                    # *** Preparing empty matrices ***
                    if mode == 1 or mode == 2:
                        data_cha = np.zeros((n_sp, freq_points_num))

                    if mode == 1 or mode == 2:
                        data_chb = np.zeros((n_sp, freq_points_num))

                    if mode == 2:
                        data_cre = np.zeros((n_sp, freq_points_num))
                        data_cim = np.zeros((n_sp, freq_points_num))
                        corr_module = np.zeros((n_sp, freq_points_num))
                        corr_phase = np.zeros((n_sp, freq_points_num))

                    # *** Reading and reshaping all data for figure ***
                    if mode == 1:
                        raw = np.fromfile(file, dtype='u4', count=(2 * n_sp * freq_points_num))
                        raw = np.reshape(raw, [2*freq_points_num, n_sp], order='F')
                        data_cha = raw[0:(freq_points_num*2):2, :].transpose()
                        data_chb = raw[1:(freq_points_num*2):2, :].transpose()

                    if mode == 2:
                        raw = np.fromfile(file, dtype='u4', count=(4 * n_sp * freq_points_num))
                        raw = np.reshape(raw, [4*freq_points_num, n_sp], order='F')
                        data_cha = raw[0:(freq_points_num*4):4, :].transpose()
                        data_chb = raw[1:(freq_points_num*4):4, :].transpose()
                        data_cre = raw[2:(freq_points_num*4):4, :].transpose()
                        data_cim = raw[3:(freq_points_num*4):4, :].transpose()

                    del raw

                    # *** Single out timing from data ***
                    # counter_a2 = np.uint64(data_cha[:, -1])
                    # counter_b2 = np.uint64(data_chb[:, -1])
                    counter_a1 = np.uint64(data_cha[:, -2])
                    counter_b1 = np.uint64(data_chb[:, -2])

                    # A = np.uint64(int('01111111111111111111111111111111', 2))
                    # msCount = np.uint32(np.bitwise_and(counter_b2, A))        # number of ms since record started
                    # ftCount = np.uint32(np.bitwise_and(counter_a2, A))        # number of specter since record started

                    tmp = np.uint64(int('00000111111111111111111111111111', 2))
                    phase_of_sec = np.uint32(np.bitwise_and(counter_a1, tmp))        # phase of second for the spectr
                    tmp = np.uint64(int('00000000000000011111111111111111', 2))
                    sec_of_day = np.uint32(np.bitwise_and(counter_b1, tmp))        # second of the day for the specter

                    # *** Time line arranging ***

                    # Preparing/cleaning matrices for time scales
                    TimeScale = []              # New for each file
                    TimeFigureScale = []        # Timelime (new) for each figure (n_sp)
                    # Calculations
                    FigStartTime = timedelta(0, int(sec_of_day[0]), int(1000000 * phase_of_sec[0] / clc_freq))
                    for i in range(n_sp):
                        TimeAdd = timedelta(0, int(sec_of_day[i]), int(1000000 * phase_of_sec[i] / clc_freq))
                        TimeScale.append(str(str(time_scale_start_date + TimeAdd)))
                        TimeFigureScale.append(str((TimeAdd - FigStartTime)))

                    TimeFigureScaleFig = np.empty_like(TimeFigureScale)
                    TimeScaleFig = np.empty_like(TimeScale)
                    for i in range(len(TimeFigureScale)):
                        TimeFigureScaleFig[i] = TimeFigureScale[i][0:11]
                        TimeScaleFig[i] = TimeScale[i][11:23]

                    # *** Converting from FPGA to PC float format ***
                    if mode == 1 or mode == 2:
                        data_cha = FPGAtoPCarrayJDS(data_cha, n_avr)
                        data_chb = FPGAtoPCarrayJDS(data_chb, n_avr)
                    if mode == 2 and corr_process == 1:
                        data_cre = FPGAtoPCarrayJDS(data_cre, n_avr)
                        data_cim = FPGAtoPCarrayJDS(data_cim, n_avr)

                    '''
                    # *** Absolute correlation specter plot ***
                    if mode == 2 and fig_id == 0:   #  Immediate correlation spectrum channels A & B
                        TwoImmedSpectraPlot(frequency, data_cre[1][:], data_cim[1][:], 'Channel A', 'Channel B',
                                            frequency[0], frequency[freq_points_num-1], -0.001, 0.001,
                                            'Frequency, MHz', 'Amplitude, dB',
                                            'Immediate spectrum '+str(df_filename[0:18])+ ' channels A & B',
                                            'Initial parameters: dt = '+str(round(time_resol,3))+' Sec, df = '+str(round(df/1000,3))+' kHz',
                                            'JDS_Results/Service/'+df_filename[0:14]+' Correlation Spectrum Re and Im before log.png')
                    '''

                    # *** Saving data to a long-term file ***
                    if (mode == 1 or mode == 2) and long_file_save_ch_a == 1:
                        data_a_file = open(data_a_file_name, 'ab')
                        data_a_file.write(data_cha)
                        data_a_file.close()
                    if (mode == 1 or mode == 2) and long_file_save_ch_b == 1:
                        data_b_file = open(data_b_file_name, 'ab')
                        data_b_file.write(data_chb)
                        data_b_file.close()
                    if (mode == 1 or mode == 2) and long_file_save_channels_sum is True:
                        data_sum_file = open(data_sum_file_name, 'ab')
                        data_sum_file.write(data_cha + data_chb)
                        data_sum_file.close()
                    if (mode == 1 or mode == 2) and long_file_save_channels_diff is True:
                        data_diff_file = open(data_diff_file_name, 'ab')
                        data_diff_file.write(np.abs(data_cha - data_chb))
                        data_diff_file.close()
                    if  mode == 2 and long_file_save_cri == 1 and corr_process == 1:
                        data_cre_file = open(data_cre_name, 'ab')
                        data_cre_file.write(np.float64(data_cre))
                        data_cre_file.close()
                        data_cim_file = open(data_cim_name, 'ab')
                        data_cim_file.write(np.float64(data_cim))
                        data_cim_file.close()

                    if long_file_save_ch_a == 1 or long_file_save_ch_b == 1 or \
                            long_file_save_cri == 1 or long_file_save_cmp == 1:
                        with open(tl_file_name, 'a') as tl_file:
                            for i in range(n_sp):
                                tl_file.write((TimeScale[i][:]+' \n'))  # str.encode

                    # *** Converting to logarithmic scale matrices ***
                    if mode == 1 or mode == 2:
                        with np.errstate(invalid='ignore'):
                            data_cha = 10 * np.log10(data_cha)
                            data_chb = 10 * np.log10(data_chb)
                        data_cha[np.isnan(data_cha)] = -120
                        data_chb[np.isnan(data_chb)] = -120
                    if mode == 2 and corr_process == 1:
                        with np.errstate(invalid='ignore', divide='ignore'):
                            corr_module = 10 * np.log10((data_cre ** 2 + data_cim ** 2) ** 0.5)
                            corr_phase = np.arctan2(data_cim, data_cre)
                        corr_phase[np.isnan(corr_phase)] = 0
                        corr_module[np.isinf(corr_module)] = -135.5

                    # *** Saving correlation data to a long-term module and phase files ***
                    if mode == 2 and corr_process == 1 and long_file_save_cmp == 1:
                        data_cm_file = open(data_cm_name, 'ab')
                        data_cm_file.write(np.float64(corr_module))
                        data_cm_file.close()
                        data_cp_file = open(data_cp_name, 'ab')
                        data_cp_file.write(np.float64(corr_phase))
                        data_cp_file.close()

                    # *** Saving immediate spectrum to file ***
                    if spectra_file_save_switch == 1 and fig_id == 0:
                        SpFile = open(result_path + '/Service/' + 'Spectrum_' + df_filename[0:14] + '.txt', 'w')
                        for i in range(freq_points_num-1):
                            if mode == 1:
                                SpFile.write(str('{:10.6f}'.format(frequency[i])) + '  ' +
                                             str('{:16.10f}'.format(data_cha[immediate_sp_no][i])) + '  ' +
                                             str('{:16.10f}'.format(data_chb[immediate_sp_no][i])) + ' \n')
                            if mode == 2:
                                SpFile.write(str(frequency[i]) + '  ' +
                                             str(data_cha[immediate_sp_no][i]) + '  ' +
                                             str(data_chb[immediate_sp_no][i]) + '  ' +
                                             str(data_cre[immediate_sp_no][i]) + '  ' +
                                             str(data_cim[immediate_sp_no][i])+' \n')

                        SpFile.close()

    # *******************************************************************************
    #                                   F I G U R E S                               *
    # *******************************************************************************

                    # *** Plotting immediate spectra before cleaning and normalizing ***
                    if (mode == 1 or mode == 2) and fig_id == 0:

                        suptitle = ('Immediate spectrum ' + str(df_filename[0:18]) + ' channels A & B')
                        title = ('Place: ' + str(df_obs_place) + ', Receiver: ' + str(df_system_name) +
                                 '. Initial parameters: dt = ' + str(round(time_resol, 3)) + ' Sec, df = ' +
                                 str(round(df/1000, 3)) + ' kHz ' + 'Description: ' + str(df_description))
                        Filename = (result_path + '/Service/' + df_filename[0:14] +
                                    ' Channels A and B Immediate Spectrum before cleaning and normalizing.png')

                        TwoOrOneValuePlot(2, frequency,  data_cha[0][:], data_chb[0][:],
                                          'Channel A', 'Channel B', frequency[0], frequency[freq_points_num-1],
                                          -120, -20, -120, -20, 'Frequency, MHz', 'Intensity, dB', 'Intensity, dB',
                                          suptitle, title, Filename,
                                          current_date, current_time, Software_version)

                    if mode == 2 and corr_process == 1 and fig_id == 0:

                        suptitle = ('Immediate correlation spectrum ' + str(df_filename[0:18]) + ' channels A & B')
                        title = ('Place: '+str(df_obs_place)+', Receiver: '+str(df_system_name) +
                                 '. Initial parameters: dt = ' + str(round(time_resol, 3)) + ' Sec, df = ' +
                                 str(round(df/1000, 3)) + ' kHz ' + 'Description: ' + str(df_description))
                        Filename = (result_path + '/Service/' + df_filename[0:14] +
                                    ' Channels A and B Correlation' +
                                    'Immedaiate Spectrum before cleaning and normalizing.png')

                        TwoOrOneValuePlot(2, frequency,  corr_module[0][:], corr_phase[0][:],
                                          'Correlation module', 'Correlation phase', frequency[0],
                                          frequency[freq_points_num-1], v_min_corr_mag, v_max_corr_mag, -4, 4,
                                          'Frequency, MHz', 'Amplitude, dB', 'Phase, deg',
                                          suptitle, title, Filename,
                                          current_date, current_time, Software_version)

                    # *** FIGURE Initial dynamic spectrum channels A and B ***
                    if (mode == 1 or mode == 2) and dyn_spec_save_initial == 1:

                        suptitle = ('Dynamic spectrum (initial) ' + str(df_filename) + ' - Fig. ' +
                                    str(fig_id + 1) + ' of ' + str(fig_max) + '\n Initial parameters: dt = ' +
                                    str(round(time_resol*1000, 3)) + ' ms, df = ' + str(round(df/1000., 3)) +
                                    ' kHz, Receiver: ' + str(df_system_name) + ', Place: ' + str(df_obs_place) +
                                    '\n' + receiver_mode + ', Description: ' + str(df_description))

                        fig_file_name = (result_path + '/Initial_spectra/' + df_filename[0:14] +
                                         ' Initial dynamic spectrum fig.' + str(fig_id+1) + '.png')

                        TwoDynSpectraPlot(data_cha.transpose(), data_chb.transpose(), v_min, v_max, v_min, v_max, 
                                          suptitle, 'Intensity, dB', 'Intensity, dB', n_sp,
                                          TimeFigureScaleFig, TimeScaleFig, frequency,
                                          freq_points_num, colormap, 'Channel A', 'Channel B', fig_file_name,
                                          current_date, current_time, Software_version, custom_dpi)

                    # *** FIGURE Initial correlation spectrum Module and Phase (python 3 new version) ***
                    if mode == 2 and corr_spectr_save_initial == 1 and corr_process == 1:

                        suptitle = ('Correlation dynamic spectrum (initial) ' + str(df_filename) +
                                    ' - Fig. ' + str(fig_id+1) + ' of ' + str(fig_max) + 
                                    '\n Initial parameters: dt = ' + str(round(time_resol*1000, 3)) + 
                                    ' ms, df = ' + str(round(df/1000., 3)) + ' kHz, Receiver: ' +
                                    str(df_system_name) + ', Place: ' + str(df_obs_place) + '\n' + receiver_mode +
                                    ', Description: ' + str(df_description))

                        fig_file_name = (result_path + '/Correlation_spectra/' + df_filename[0:14] +
                                         ' Correlation dynamic spectrum fig.' + str(fig_id+1) + '.png')

                        TwoDynSpectraPlot(corr_module.transpose(), corr_phase.transpose(), 
                                          v_min_corr_mag, v_max_corr_mag, -3.15, 3.15, suptitle, 
                                          'Intensity, dB', 'Phase, rad', n_sp, TimeFigureScaleFig, TimeScaleFig, 
                                          frequency, freq_points_num, colormap, 
                                          'Correlation module', 'Correlation phase',
                                          fig_file_name, current_date, current_time, Software_version, custom_dpi)

                    # *** Normalizing amplitude-frequency response ***
                    if mode == 1 or mode == 2:
                        normalization_db(data_cha, freq_points_num, n_sp)
                        normalization_db(data_chb, freq_points_num, n_sp)
                    if mode == 2 and corr_process == 1 and corr_spectr_save_cleaned == 1:
                        normalization_db(corr_module, freq_points_num, n_sp)

                    # *** Deleting channels with strong RFI ***
                    if mode == 1 or mode == 2:
                        simple_channel_clean(data_cha, rfi_mean_const)
                        simple_channel_clean(data_chb, rfi_mean_const)
                    if mode == 2 and corr_process == 1 and corr_spectr_save_cleaned == 1:
                        simple_channel_clean(corr_module, 2 * rfi_mean_const)

                    #   *** Immediate spectra ***    (only for first figure in data file)
                    if (mode == 1 or mode == 2) and fig_id == 0:   # Immediate spectrum channels A & B

                        suptitle = ('Cleaned and normalized immediate spectrum ' + 
                                    str(df_filename[0:18]) + ' channels A & B')
                        title = ('Place: ' + str(df_obs_place) + ', Receiver: ' + str(df_system_name) +
                                 '. Initial parameters: dt = ' + str(round(time_resol, 3)) + ' Sec, df = ' +
                                 str(round(df/1000, 3)) + ' kHz ' + 'Description: ' + str(df_description))
                        Filename = (result_path + '/Service/' + df_filename[0:14] +
                                    ' Channels A and B Immediate Spectrum after cleaning and normalizing.png')

                        TwoOrOneValuePlot(2, frequency,  data_cha[1][:], data_chb[1][:], 'Channel A', 'Channel B', 
                                          frequency[0], frequency[freq_points_num-1], v_min_norm-5, v_max_norm, 
                                          v_min_norm-5, v_max_norm, 'Frequency, MHz', 'Intensity, dB', 'Intensity, dB',
                                          suptitle, title, Filename, current_date, current_time, Software_version)

                    # *** FIGURE Normalized dynamic spectrum channels A and B ***
                    if (mode == 1 or mode == 2) and dyn_spec_save_cleaned == 1:

                        suptitle = ('Dynamic spectrum (normalized) ' + str(df_filename) + ' - Fig. ' +
                                    str(fig_id+1) + ' of ' + str(fig_max) + '\n Initial parameters: dt = ' +
                                    str(round(time_resol * 1000, 3)) + ' ms, df = ' + str(round(df/1000., 3)) +
                                    ' kHz, Receiver: ' + str(df_system_name) + ', Place: ' + str(df_obs_place) +
                                    '\n' + receiver_mode + ', Description: ' + str(df_description))

                        fig_file_name = (result_path + '/' + df_filename[0:14] + ' Dynamic spectra fig.' +
                                         str(fig_id+1) + '.png')

                        TwoDynSpectraPlot(data_cha.transpose(), data_chb.transpose(), v_min_norm, v_max_norm, 
                                          v_min_norm, v_max_norm, suptitle, 'Intensity, dB', 'Intensity, dB', n_sp,
                                          TimeFigureScaleFig, TimeScaleFig, frequency, freq_points_num, colormap, 
                                          'Channel A', 'Channel B', fig_file_name, current_date, current_time, 
                                          Software_version, custom_dpi)

                    # *** FIGURE Normalized correlation spectrum Module and Phase ***
                    if mode == 2 and corr_spectr_save_cleaned == 1 and corr_process == 1:

                        suptitle = ('Correlation dynamic spectrum (normalized) ' + str(df_filename) +
                                    ' - Fig. ' + str(fig_id + 1) + ' of ' + str(fig_max) + 
                                    '\n Initial parameters: dt = ' + str(round(time_resol * 1000, 3)) + 
                                    ' ms, df = ' + str(round(df/1000., 3)) + ' kHz, Receiver: ' +
                                    str(df_system_name) + ', Place: ' + str(df_obs_place) + '\n' + receiver_mode +
                                    ', Description: ' + str(df_description))

                        fig_file_name = (result_path + '/Correlation_spectra/' + df_filename[0:14] +
                                         ' Correlation dynamic spectra cleaned fig.' + str(fig_id+1) + '.png')
                        TwoDynSpectraPlot(corr_module.transpose(), corr_phase.transpose(), 2*v_min_norm, 2*v_max_norm, 
                                          -3.15, 3.15, suptitle, 'Intensity, dB', 'Phase, rad', n_sp,
                                          TimeFigureScaleFig, TimeScaleFig, frequency, freq_points_num, colormap, 
                                          'Normalized correlation module', 'Correlation phase',
                                          fig_file_name, current_date, current_time, Software_version, custom_dpi)

                '''
                # Check of second counter data for linearity
                OneImmedSpecterPlot(list(range(ChunksInFile)), timeLineSecond, 'timeLineSecond',
                                    0, ChunksInFile, 0, 2000,
                                    'Time, sec', 'Second counter, sec',
                                    'Second counter',
                                    ' ',
                                    'ADR_Results/Service/' + df_filename[0:14] + ' Second counter fig.' + str(fig_id+1) + '.png')

                '''

                gc.collect()

            # print ('\n  Position in file: ', file.tell(), ' File size: ', df_filesize)
            # if (file.tell() == df_filesize): print ('\n  File was read till the end \n')
            if file.tell() < df_filesize:
                print('    The difference is ', (df_filesize - file.tell()), ' bytes')
                print('\n  File was NOT read till the end!!! ERROR')

        file.close()  # Here we close the data file

    ok = 1
    return ok, dat_file_name, dat_file_list


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    file_list = 'DATA/'
    result_path = ''

    done_or_not, dat_file_name, dat_file_list = JDS_file_reader(directory, result_path, MaxNim, rfi_mean_const, v_min, v_max, v_min_norm, v_max_norm,
            v_min_corr_mag, v_max_corr_mag, custom_dpi, colormap, corr_process, Sum_Diff_Calculate,
            long_file_save_ch_a, long_file_save_ch_b, long_file_save_cmp, long_file_save_cri, longFileSaveSSD,
            dyn_spec_save_initial, dyn_spec_save_cleaned, corr_spectr_save_initial, corr_spectr_save_cleaned,
            spectra_file_save_switch, immediate_sp_no)
