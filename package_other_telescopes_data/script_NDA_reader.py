# Python3
software_version = '2019.04.17'
# Program intended to read, show and analyze data from Routine receiver of Nancay Decametric Array

# *************************************************************
#                         PARAMETERS                          *
# *************************************************************
# Directory of files to be analyzed:
directory = '../RA_DATA_ARCHIVE/NDA_data/'  # 'DATA/'

MaxNim = 1024
RFImeanConst = 8        # Constant of RFI mitigation (usually 8)
# Vmin = -120            # Lower limit of figure dynamic range for initial spectra
# Vmax = -30             # Upper limit of figure dynamic range for initial spectra
VminNorm = 0            # Lower limit of figure dynamic range for normalized spectra of LHP and RHP
VmaxNorm = 15           # Upper limit of figure dynamic range for normalized spectra of LHP and RHP
VmaxNormTotal = 30      # Upper limit of figure dynamic range for normalized spectra of total intensity

FileInitDynSpectra = 1
FileAverDynSpectra = 1

StartStopSwitch = 0     # Read the whole file (0) or specified time limits (1)
StartStopFreqRg = 0     # Specify particular frequency range (1) or whole range (0)

DynSpecSaveInitial = 1  # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 1  # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
TotalIntPolSavePic = 1  # Save dynamic spectra of total intensity and polarization (1 = yes, 0 = no) ?
colormap = 'jet'        # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
custom_dpi = 300         # Resolution of images of dynamic spectra
ImedSpectNum = 20       # Number of specter in portion of data to plot immediate spectrum

# # Begin and end frequency of dynamic spectrum (MHz)
# freq_start = 8
# freq_stop = 33

# Begin and end time of dynamic spectrum ('yyyy-mm-dd hh:mm:ss')
dateTimeStart = '2018-03-31 09:10:00'
dateTimeStop =  '2018-03-31 10:30:00'

# *************************************************************
#                    IMPORT LIBRARIES                         *
# *************************************************************

import os
import sys
import math
import time
import numpy as np
from os import path
from datetime import datetime

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_plot_formats.plot_formats import TwoImmedSpectraPlot, TwoDynSpectraPlot
from package_ra_data_processing.f_spectra_normalization import normalization_db
from package_cleaning.simple_channel_clean import simple_channel_clean

# *************************************************************
#                        MAIN PROGRAM                         *
# *************************************************************


print('\n\n\n\n\n\n\n\n   ****************************************************')
print('   *      NDA data files reader  v.', software_version, '       *      (c) YeS 2019')
print('   **************************************************** \n\n\n')


startTime = time.time()
current_time = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print('  Today is ', currentDate, ' time is ', current_time, '\n')


# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = "NDA_Results/Service"
if not os.path.exists(newpath):
    os.makedirs(newpath)
if DynSpecSaveInitial == 1 and FileInitDynSpectra == 1:
    if not os.path.exists('NDA_Results/Initial_spectra'):
        os.makedirs('NDA_Results/Initial_spectra')
if TotalIntPolSavePic == 1 and FileInitDynSpectra == 1:
    if not os.path.exists('NDA_Results/Total_intensity_and_polarization'):
        os.makedirs('NDA_Results/Total_intensity_and_polarization')
if FileAverDynSpectra == 1:
    if not os.path.exists('NDA_Results/Averaged'):
        os.makedirs('NDA_Results/Averaged')


# *** Search NDA files in the directory ***
file_list = []
i = 0
print('  Directory: ', directory, '\n')
print('  List of files to be analyzed: ')
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.RT1'):
            i = i + 1
            print('         ', i, ') ', file)
            file_list.append(str(os.path.join(root, file)))
print(' ')

# -------------------
fileNo = 0
fname = file_list[0]
# -------------------

df_filesize = os.stat(fname).st_size                  # Size of file

# *** NDA special values ***

# number_of_blocks = df_filesize / 405
sumDifMode = ''
df_system_name = 'NDA receiver'
df_obs_place = 'Nancay observatory, France'
ReceiverMode = 'Spectra mode'
freq_points_num = 400


with open(fname, 'rb') as file:

    temp = file.read(1)                                  # First byte has no meaning
    min_freq = float(file.read(2).decode('utf-8'))       # Minimum frequency, in MHz (2 bytes)
    max_freq = float(file.read(2).decode('utf-8'))       # Maximum frequency, in MHz (2 bytes)
    resolution = float(file.read(3).decode('utf-8'))     # Spectral resolution, in kHz (3 bytes)
    ref_intensity = float(file.read(3).decode('utf-8'))  # Reference intensity, in dBm (3 bytes)
    scan_rate = float(file.read(5).decode('utf-8'))      # Spectral scanning rate, in ms (5 bytes)
    dyn_scale = float(file.read(2).decode('utf-8'))      # Dynamic scale of analyzer, in dB/division (2 bytes)
    solar_culm = file.read(4).decode('utf-8')            # Hour min of passage of Sun at the meridian (4 bytes: hhmm)

    print(' File size:                   ', round(df_filesize/1024/1024, 3), ' Mb (', df_filesize, ' bytes )')
    print(' Minimum frequency:           ', min_freq, ' MHz')
    print(' Maximum frequency:           ', max_freq, ' MHz')
    print(' Spectral resolution:         ', resolution, ' kHz')
    print(' Reference intensity:         ', ref_intensity, ' dBm')
    print(' Spectral scanning rate:      ', scan_rate, ' ms')
    print(' Dynamic scale of analyzer:   ', dyn_scale, 'dB/division')
    print(' Local solar culmination:     ', solar_culm[0:2], ' hour ', solar_culm[2:4], ' min, UTC')

    temp = file.read(383)                        # Bytes 23-405 - Nothing (383 bytes)

    SpInFile = int((df_filesize/(2*405)) - 405)
    print('\n Number of spectra in file:   ', SpInFile, '\n')

    frequency = [0 for col in range(freq_points_num)]
    df = (max_freq - min_freq) / freq_points_num
    for i in range(0, freq_points_num):
        frequency[i] = min_freq + i * df
    print(' Calculated spectral resolution:      ', df, ' MHz  \n\n')

    timeLineSecond = np.zeros(SpInFile)  # List of second values

    # *** Reading and plotting spectra without averaging ***
    if FileInitDynSpectra == 1:
        figID = -1
        figMAX = int(math.ceil(SpInFile / MaxNim))
        if figMAX < 1:
            figMAX = 1
        for fig in range(figMAX):
            Time1 = time.time()  # Timing
            figID = figID + 1
            current_time = time.strftime("%H:%M:%S")
            print(' File # ', str(fileNo+1), ' of ', str(len(file_list)), ', figure # ', figID+1, ' of ', figMAX,
                  '   started at: ', current_time)
            if (SpInFile - MaxNim * figID) < MaxNim:
                Nsp = (SpInFile - MaxNim * figID)
            else:
                Nsp = MaxNim

            # *** DATA READING process ***

            # Reading and reshaping all data with readers
            raw = np.fromfile(file, dtype='uint8', count=int(2 * Nsp * (freq_points_num + 5)))
            raw = np.reshape(raw, [2 * (freq_points_num + 5), Nsp], order='F')

            # Splitting time stamps and points from data
            time_stamps = raw[0: 4, :]
            dataLHP = raw[5: freq_points_num + 5, :]
            point = raw[freq_points_num + 4: freq_points_num + 5]
            dataRHP = raw[freq_points_num + 6: 2 * freq_points_num + 6, :]
            del raw

            TimeScale = []              # New for each file
            for i in range(Nsp):
                TimeScale.append(datetime(int('20' + fname[-10:-8]), int(fname[-8:-6]), int(fname[-6:-4]),
                                          int(time_stamps[0, i]), int(time_stamps[1, i]), int(time_stamps[2, i]),
                                          int(time_stamps[3, i])*1000))

            # *** Time resolution in ms ***
            time_res_dt = TimeScale[1] - TimeScale[0]
            time_res = float(str(time_res_dt)[5:11])

            TimeFigureScale = []        # Timelime (new) for each figure (Nsp)
            for i in range(Nsp):
                TimeFigureScale.append(str((TimeScale[i] - TimeScale[0])))

            TimeScaleStr = ['' for x in range(Nsp)]
            for i in range(Nsp):
                TimeScaleStr[i] = str(TimeScale[i])
            del TimeScale

            TimeFigureScaleFig = np.empty_like(TimeFigureScale)
            TimeScaleFig = np.empty_like(TimeScaleStr)
            for i in range(len(TimeFigureScale)):
                TimeFigureScaleFig[i] = TimeFigureScale[i][0:11]
                TimeScaleFig[i] = TimeScaleStr[i][11:23]

            # ??? Converting to dB scale ???
            dataLHP = 0.3125 * dataLHP
            dataRHP = 0.3125 * dataRHP

            # *** FIGURE Initial immediate spectrum channels A and B ***
            TwoImmedSpectraPlot(frequency, dataLHP.transpose()[ImedSpectNum][:], dataRHP.transpose()[ImedSpectNum][:],
                                'Channel A', 'Channel B', frequency[0], frequency[freq_points_num-1], 0, 80,
                                'Frequency, MHz', 'Amplitude, dB', 'Immediate spectrum ' + str(fname[-11:]) +
                                ' channels A & B', 'Initial parameters: dt = ' + str(round(time_res*1000, 3)) +
                                ' ms, df = ' + str(round(df*1000, 3)) + ' kHz' + sumDifMode + '\nDescription: ' +
                                'Local solar culmination at ' + solar_culm[0:2] + ' hour ' + solar_culm[2:4] +
                                ' min, UTC', 'NDA_Results/Service/' + fname[-11:] +
                                ' Channels A and B Initial immediate spectrum fig.' + str(figID+1)+'.png',
                                currentDate, current_time, software_version)

            # *** FIGURE Initial dynamic spectrum channels A and B (python 3 new version) ***
            VminL = np.min(dataLHP)
            VmaxL = np.max(dataLHP)
            VminR = np.min(dataRHP)
            VmaxR = np.max(dataRHP)

            fig_file_name = 'NDA_Results/Initial_spectra/' + fname[-11:] + \
                            ' Initial dynamic spectrum fig.' + str(figID + 1) + '.png'

            Suptitle = ('Dynamic spectrum (initial) ' + str(fname[-11:]) + ' - Fig. ' + str(figID+1) + ' of ' +
                        str(figMAX) + '\n Initial parameters: dt = ' + str(round(time_res * 1000, 3)) + ' ms, df = ' +
                        str(round(df*1000., 3)) + ' kHz, ' + sumDifMode + ' Receiver: ' + str(df_system_name) +
                        ', Place: ' + str(df_obs_place) + '\n' + ReceiverMode + ' Local solar culmination at ' +
                        solar_culm[0:2] + ' hour ' + solar_culm[2:4] + ' min, UTC')

            TwoDynSpectraPlot(dataLHP, dataRHP, VminL, VmaxL, VminR, VmaxR, Suptitle, 'Intensity, dB', 'Intensity, dB',
                              Nsp, TimeFigureScaleFig, TimeScaleFig, frequency, freq_points_num, colormap,
                              'Left-hand circular polarization', 'Right-hand circular polarization', fig_file_name,
                              currentDate, current_time, software_version, custom_dpi)

            if DynSpecSaveCleaned == 1:

                # *** Normalizing amplitude-frequency response ***
                normalization_db(dataLHP.transpose(), freq_points_num, Nsp)
                normalization_db(dataRHP.transpose(), freq_points_num, Nsp)

                # *** Deleting channels with strong RFI ***
                simple_channel_clean(dataLHP.transpose(), RFImeanConst)
                simple_channel_clean(dataRHP.transpose(), RFImeanConst)

                # *** FIGURE Dynamic spectrum channels A and B cleaned and normalized (python 3 new version) ***

                fig_file_name = ('NDA_Results/' + fname[-11:] +
                                 ' Normalized dynamic spectrum fig.' + str(figID+1) + '.png')
                Suptitle = ('Dynamic spectrum (normalized) ' + str(fname[-11:]) + ' - Fig. ' + str(figID+1) +
                            ' of ' + str(figMAX) + '\n Initial parameters: dt = ' + str(round(time_res*1000, 3)) +
                            ' ms, df = ' + str(round(df*1000., 3)) + ' kHz, ' + sumDifMode + ' Receiver: ' +
                            str(df_system_name) + ', Place: '+str(df_obs_place) + '\n' + ReceiverMode +
                            ' Local solar culmination at ' + solar_culm[0:2] + ' hour ' + solar_culm[2:4] + ' min, UTC')

                TwoDynSpectraPlot(dataLHP, dataRHP, VminNorm, VmaxNorm, VminNorm, VmaxNorm, Suptitle, 'Intensity, dB',
                                  'Intensity, dB', Nsp, TimeFigureScaleFig, TimeScaleFig, frequency, freq_points_num,
                                  colormap, 'Left-hand circular polarization', 'Right-hand circular polarization',
                                  fig_file_name, currentDate, current_time, software_version, custom_dpi)

            if TotalIntPolSavePic == 1:

                # *** Finding Polarization Characteristics ***

                Data_sum  = np.power(10, (dataLHP/10)) + np.power(10, (dataRHP/10))  # Total intensity
                Data_diff = np.power(10, (dataLHP/10)) - np.power(10, (dataRHP/10))  # Residual intensity
                LevelCirculPol = (Data_diff / Data_sum)           # Level of Circular Polarization

                TotalIntensity = 10 * np.log10(Data_sum)

                # *** Normalizing amplitude-frequency response of total intensity ***
                normalization_db(TotalIntensity.transpose(), freq_points_num, Nsp)

                # *** Deleting channels with strong RFI ***
                simple_channel_clean(TotalIntensity.transpose(), RFImeanConst)

                # *** FIGURE Dynamic spectrum total intensity and polarization level ***

                fig_file_name = ('NDA_Results/Total_intensity_and_polarization/' + fname[-11:] +
                                 ' Dynamic spectrum (total and polarization) fig.' + str(figID + 1) + '.png')
                Suptitle = ('Dynamic spectrum (Total) ' + str(fname[-11:]) + ' - Fig. ' + str(figID + 1) + ' of ' +
                            str(figMAX) + '\n Initial parameters: dt = ' + str(round(time_res*1000, 3)) +
                            ' ms, df = ' + str(round(df*1000., 3)) + ' kHz, ' + sumDifMode + ' Receiver: ' +
                            str(df_system_name) + ', Place: ' + str(df_obs_place) + '\n' + ReceiverMode +
                            ' Local solar culmination at ' + solar_culm[0:2] + ' hour ' + solar_culm[2:4] + ' min, UTC')

                TwoDynSpectraPlot(TotalIntensity, LevelCirculPol, VminNorm, VmaxNormTotal, -1, 1, Suptitle,
                                  'Intensity, dB', 'Relative units', Nsp, TimeFigureScaleFig, TimeScaleFig, frequency,
                                  freq_points_num, colormap, 'Total intensity', 'Level of circular polarization',
                                  fig_file_name, currentDate, current_time, software_version, custom_dpi)

        del TotalIntensity, LevelCirculPol, Data_sum, Data_diff, dataLHP, dataRHP, time_stamps

    # *** Reading and plotting spectra with averaging for the whole or the part of the file ***
    if FileAverDynSpectra == 1:

        if StartStopSwitch == 0:

            istart = 0
            istop = SpInFile

        if StartStopSwitch == 1:  # If we read only specified time limits of files

            timeline = []
            for spectr in range(SpInFile):
                temp = np.fromfile(file, dtype='uint8', count=int(2 * (freq_points_num + 5)))
                time_stamps = temp[0:4]  # Splitting time stamps from data
                timeline.append(str(datetime(int('20' + fname[-10:-8]), int(fname[-8:-6]), int(fname[-6:-4]),
                                             int(time_stamps[0]), int(time_stamps[1]), int(time_stamps[2]),
                                             int(time_stamps[3]) * 1000)))

            dt_timeline = []
            for i in range(len(timeline)):  # converting text to ".datetime" format

                # Check is the uS field is empty. If so it means it is equal to '000000'
                uSecond = str(timeline[i][20:26])
                if len(uSecond) < 2:
                    uSecond = '000000'

                dt_timeline.append(datetime(int(timeline[i][0:4]), int(timeline[i][5:7]), int(timeline[i][8:10]),
                                            int(timeline[i][11:13]), int(timeline[i][14:16]), int(timeline[i][17:19]),
                                            int(uSecond)))

            dt_dateTimeStart = datetime(int(dateTimeStart[0:4]), int(dateTimeStart[5:7]), int(dateTimeStart[8:10]),
                                        int(dateTimeStart[11:13]), int(dateTimeStart[14:16]), int(dateTimeStart[17:19]),
                                        0)
            dt_dateTimeStop = datetime(int(dateTimeStop[0:4]), int(dateTimeStop[5:7]), int(dateTimeStop[8:10]),
                                       int(dateTimeStop[11:13]), int(dateTimeStop[14:16]), int(dateTimeStop[17:19]), 0)

            # *** Showing the time limits of file and time limits of chosen part
            print('\n\n                               Start                         End \n')
            print('  File time limits:   ', dt_timeline[0], ' ', dt_timeline[len(timeline)-1], '\n')
            print('  Chosen time limits: ', dt_dateTimeStart, '        ', dt_dateTimeStop, '\n')

            # Verifying that chosen time limits are inside file and are correct
            if (dt_timeline[len(timeline)-1] >= dt_dateTimeStart > dt_timeline[0]) and \
                    (dt_timeline[len(timeline)-1] > dt_dateTimeStop >= dt_timeline[0]) and\
                    (dt_dateTimeStop > dt_dateTimeStart):
                print('  Time is chosen correctly! \n\n')
            else:
                print('  ERROR! Time is chosen out of file limits!!! \n\n')
                sys.exit('                Program stopped \n\n\n\n')

            # Finding the closest spectra to the chosen time limits
            A = []
            B = []
            for i in range(len(timeline)):
                dt_diff_start = dt_timeline[i] - dt_dateTimeStart
                dt_diff_stop  = dt_timeline[i] - dt_dateTimeStop
                A.append(abs(divmod(dt_diff_start.total_seconds(), 60)[0]*60 +
                             divmod(dt_diff_start.total_seconds(), 60)[1]))
                B.append(abs(divmod(dt_diff_stop.total_seconds(), 60)[0]*60 +
                             divmod(dt_diff_stop.total_seconds(), 60)[1]))

            istart = A.index(min(A))
            istop = B.index(min(B))
            print('\n Start specter number is:            ', istart)
            print(' Stop specter number is:             ', istop)
            print(' Total number of spectra to read:    ', istop - istart)

        # *** Calculation of the dimensions of arrays to read ***

        ny = int(istop - istart)         # the second dimension of the array: number of spectra to read
        num_spectra_to_average = int(ny/1024)
        if num_spectra_to_average < 1:
            num_spectra_to_average = 1

        print('\n Number of frequency channels:       ', freq_points_num)
        print(' Number of spectra:                  ', ny)
        print('\n Recommended spectra number for averaging is:  ', num_spectra_to_average)

        print('\n\n\n  *** Data reading and averaging *** \n\n\n')

        # *** DATA READING process ***

        file.seek((freq_points_num + 5) * 2 * (istart + 1))
        TimeScale = []              # Time scale for averaged data
        block_num = int(ny / num_spectra_to_average)

        # *** Preparing empty matrices ***

        dataLHP = np.zeros((block_num, freq_points_num))
        dataRHP = np.zeros((block_num, freq_points_num))

        for block in range(block_num):

            # Reading and reshaping all data with readers
            raw = np.fromfile(file, dtype='uint8', count=int(2 * num_spectra_to_average * (freq_points_num + 5)))
            raw = np.reshape(raw, [2 * (freq_points_num + 5), num_spectra_to_average], order='F')

            # Splitting data from the read array
            dataLHP[block, :] = raw[5:freq_points_num + 5, :].mean(axis=1)[:]
            dataRHP[block, :] = raw[freq_points_num + 6: 2 * freq_points_num + 6, :].mean(axis=1)[:]
            time_stamps = raw[0:4, :]
            del raw

            TimeScale.append(datetime(int('20' + fname[-10:-8]), int(fname[-8:-6]), int(fname[-6:-4]),
                                      int(time_stamps[0, num_spectra_to_average-1]),
                                      int(time_stamps[1, num_spectra_to_average-1]),
                                      int(time_stamps[2, num_spectra_to_average-1]),
                                      int(time_stamps[3, num_spectra_to_average-1]) * 1000))

        # *** Time resolution in ms ***
        time_res_dt = TimeScale[1] - TimeScale[0]
        time_res = float(str(time_res_dt)[5:11])

        TimeFigureScale = []        # Timelime (new) for each figure (Nsp)
        for i in range(block_num):
            TimeFigureScale.append(str((TimeScale[i] - TimeScale[0])))

        TimeScaleStr = ['' for x in range(block_num)]
        for i in range(block_num):
            TimeScaleStr[i] = str(TimeScale[i])
        del TimeScale

        TimeFigureScaleFig = np.empty_like(TimeFigureScale)
        TimeScaleFig = np.empty_like(TimeScaleStr)
        for i in range(len(TimeFigureScale)):
            TimeFigureScaleFig[i] = TimeFigureScale[i][0:11]
            TimeScaleFig[i] = TimeScaleStr[i][11:23]

        # ??? Converting to dB scale ???
        dataLHP = 0.3125 * dataLHP
        dataRHP = 0.3125 * dataRHP

        # *** FIGURE Initial immediate spectrum channels A and B ***
        TwoImmedSpectraPlot(frequency, dataLHP[ImedSpectNum][:], dataRHP[ImedSpectNum][:], 'Channel A', 'Channel B',
                            frequency[0], frequency[freq_points_num-1], 0, 80, 'Frequency, MHz', 'Amplitude, dB',
                            'Immediate spectrum ' + str(fname[-11:]) + ' channels A & B', 'Initial parameters: dt = ' +
                            str(round(time_res*1000, 3)) + ' ms, df = ' + str(round(df*1000, 3)) + ' kHz' +
                            sumDifMode + '\nDescription: ' + 'Local solar culmination at ' + solar_culm[0:2] +
                            ' hour ' + solar_culm[2:4] + ' min, UTC', 'NDA_Results/Averaged/' + fname[-11:] +
                            ' 01 - Channels A and B Initial immediate spectrum.png', currentDate, current_time,
                            software_version)

        # *** FIGURE Initial dynamic spectrum channels A and B (python 3 new version) ***
        VminL = np.min(dataLHP)
        VmaxL = np.max(dataLHP)
        VminR = np.min(dataRHP)
        VmaxR = np.max(dataRHP)

        fig_file_name = ('NDA_Results/Averaged/' + fname[-11:] +
                         ' 03 - Initial dynamic spectrum fig. ' + str(figID+1) + '.png')
        Suptitle = ('Dynamic spectrum (initial) ' + str(fname[-11:]) + ' - Fig. ' + str(1) + ' of ' + str(1) +
                    '\n Initial parameters: dt = '+str(round(time_res*1000, 3)) + ' ms, df = ' +
                    str(round(df*1000., 3)) + ' kHz, ' + sumDifMode + ' Receiver: ' + str(df_system_name) +
                    ', Place: ' + str(df_obs_place) + '\n' + ReceiverMode + ' Local solar culmination at ' +
                    solar_culm[0:2] + ' hour ' + solar_culm[2:4] + ' min, UTC')

        TwoDynSpectraPlot(dataLHP.transpose(), dataRHP.transpose(), VminL, VmaxL, VminR, VmaxR, Suptitle,
                          'Intensity, dB', 'Intensity, dB', block_num, TimeFigureScaleFig, TimeScaleFig, frequency,
                          freq_points_num, colormap, 'Left-hand circular polarization',
                          'Right-hand circular polarization', fig_file_name, currentDate, current_time,
                          software_version, custom_dpi)

        if DynSpecSaveCleaned == 1:

            # *** Normalizing amplitude-frequency response ***
            normalization_db(dataLHP, freq_points_num, block_num)
            normalization_db(dataRHP, freq_points_num, block_num)

            # *** Deleting channels with strong RFI ***
            simple_channel_clean(dataLHP, RFImeanConst)
            simple_channel_clean(dataRHP, RFImeanConst)

            # *** FIGURE Dynamic spectrum channels A and B cleaned and normalized (python 3 new version) ***

            fig_file_name = ('NDA_Results/Averaged/' + fname[-11:] +
                             ' 04 - Normalized dynamic spectrum fig. ' + str(figID+1) + '.png')
            Suptitle = ('Dynamic spectrum (normalized) ' + str(fname[-11:]) + ' - Fig. ' + str(1) + ' of ' + str(1) +
                        '\n Initial parameters: dt = ' + str(round(time_res*1000, 3)) + ' ms, df = ' +
                        str(round(df*1000., 3)) + ' kHz, ' + sumDifMode + ' Receiver: ' + str(df_system_name) +
                        ', Place: ' + str(df_obs_place) + '\n' + ReceiverMode + ' Local solar culmination at ' +
                        solar_culm[0:2] + ' hour ' + solar_culm[2:4] + ' min, UTC')

            TwoDynSpectraPlot(dataLHP.transpose(), dataRHP.transpose(), VminNorm, VmaxNorm, VminNorm, VmaxNorm,
                              Suptitle, 'Intensity, dB', 'Intensity, dB', block_num, TimeFigureScaleFig, TimeScaleFig,
                              frequency, freq_points_num, colormap, 'Left-hand circular polarization',
                              'Right-hand circular polarization', fig_file_name, currentDate, current_time,
                              software_version, custom_dpi)

        if TotalIntPolSavePic == 1:

            # *** Finding Polarization Characteristics ***

            Data_sum  = np.power(10, (dataLHP/10)) + np.power(10, (dataRHP/10))  # Total intensity
            Data_diff = np.power(10, (dataLHP/10)) - np.power(10, (dataRHP/10))  # Residual intensity
            LevelCirculPol = (Data_diff / Data_sum)           # Level of Circular Polarization

            TotalIntensity = 10 * np.log10(Data_sum)

            # *** Normalizing amplitude-frequency response of total intensity ***
            normalization_db(TotalIntensity, freq_points_num, block_num)

            # *** Deleting channels with strong RFI ***
            simple_channel_clean(TotalIntensity, RFImeanConst)

            # *** FIGURE Initial immediate spectrum channels A and B ***
            TwoImmedSpectraPlot(frequency, dataLHP[ImedSpectNum][:], dataRHP[ImedSpectNum][:], 'Channel A', 'Channel B',
                                frequency[0], frequency[freq_points_num-1], 0, 80, 'Frequency, MHz', 'Amplitude, dB',
                                'Immediate spectrum (normalized) ' + str(fname[-11:]) + ' channels A & B',
                                'Initial parameters: dt = ' + str(round(time_res * 1000, 3)) + ' ms, df = ' +
                                str(round(df*1000, 3)) + ' kHz' + sumDifMode + '\nDescription: ' +
                                'Local solar culmination at ' + solar_culm[0:2] + ' hour ' + solar_culm[2:4] +
                                ' min, UTC', 'NDA_Results/Averaged/' + fname[-11:] +
                                ' 02 - Channels A and B Normalized immediate spectrum.png', currentDate,
                                current_time, software_version)

            # *** FIGURE Dynamic spectrum total intensity and polarization level (python 3 new version) ***

            fig_file_name = ('NDA_Results/Averaged/' + fname[-11:] +
                             ' 05 - Dynamic spectrum (total and polarization) fig. ' + str(figID+1) + '.png')
            Suptitle = ('Dynamic spectrum (Total) ' + str(fname[-11:]) + ' - Fig. ' + str(0+1) + ' of ' + str(1) +
                        '\n Initial parameters: dt = '+str(round(time_res*1000, 3)) + ' ms, df = ' +
                        str(round(df*1000., 3)) + ' kHz, ' + sumDifMode + ' Receiver: ' + str(df_system_name) +
                        ', Place: ' + str(df_obs_place) + '\n' + ReceiverMode + ' Local solar culmination at ' +
                        solar_culm[0:2] + ' hour ' + solar_culm[2:4] + ' min, UTC')

            TwoDynSpectraPlot(TotalIntensity.transpose(), LevelCirculPol.transpose(), VminNorm, VmaxNormTotal, -1, 1,
                              Suptitle, 'Intensity, dB', 'Intensity, dB', block_num, TimeFigureScaleFig, TimeScaleFig,
                              frequency, freq_points_num, colormap, 'Total intensity', 'Level of circular polarization',
                              fig_file_name, currentDate, current_time, software_version, custom_dpi)

        del TotalIntensity, LevelCirculPol, Data_sum, Data_diff, dataLHP, dataRHP, time_stamps

endTime = time.time()    # Time of calculations

print('\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds')
print('\n\n    *** Program NDA reader has finished! *** \n\n\n')
