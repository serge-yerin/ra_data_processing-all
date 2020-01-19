# Python3
# pip install progress
#
#   !!!! NOT FINISHED !!!
# Add storing data files of raw and averaged data
# Improve time reading (for new receiver)
# Read frequency list from header, not create it
#
Software_version = '2020.01.19'
# Program intended to read, show and analyze data from DSPZ receivers in waveform mode

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Directory of files to be analyzed:
directory = 'DATA/'  #

no_of_spectra_to_average = 64   # Number of spectra to average for dynamic spectra (64)
skip_data_blocks = 0            # Number of data blocks to skip before reading
VminNorm = 0                    # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 10                   # Upper limit of figure dynamic range for normalized spectra
colormap = 'Greys'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
customDPI = 300                 # Resolution of images of dynamic spectra
save_long_file_aver = 1         # Save long data file of averaged spectra? (1 - yes, 0 - no)
dyn_spectr_save_init = 1        # Save dynamic spectra pictures before normalizing (1 = yes, 0 = no) ?
dyn_spectr_save_norm = 1        # Save dynamic spectra pictures after normalizing (1 = yes, 0 = no) ?

# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import os
import sys
import time
import numpy as np
from os import path
from progress.bar import IncrementalBar

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_ra_data_files_formats.check_if_JDS_files_of_equal_parameters import check_if_JDS_files_of_equal_parameters
from package_common_modules.check_if_all_files_of_same_size import check_if_all_files_of_same_size
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_processing.spectra_normalization import Normalization_dB
from package_cleaning.simple_channel_clean import simple_channel_clean
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.JDS_waveform_time import JDS_waveform_time
from package_plot_formats.plot_formats import TwoOrOneValuePlot, OneDynSpectraPlot, TwoDynSpectraPlot

# ###############################################################################
# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************

print('\n\n\n\n\n\n\n\n   ****************************************************')
print('   *     JDSwf data files reader  v.', Software_version, '      *      (c) YeS 2019')
print('   **************************************************** \n\n\n')


startTime = time.time()
previousTime = startTime
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print('  Today is ', currentDate, ' time is ', currentTime, '\n')


# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
result_folder = 'JDS_WF_Results_' + directory.split('/')[-2]
if not os.path.exists(result_folder):
    os.makedirs(result_folder)
service_folder = result_folder + '/Service'
if not os.path.exists(service_folder):
    os.makedirs(service_folder)
if dyn_spectr_save_init == 1:
    initial_spectra_folder = result_folder + '/Initial spectra'
    if not os.path.exists(initial_spectra_folder):
        os.makedirs(initial_spectra_folder)


# *** Search JDS files in the directory ***

fileList = find_files_only_in_current_folder(directory, '.jds', 1)
print('')

# Check if all files (except the last) have same size
same_or_not = check_if_all_files_of_same_size(directory, fileList, 1)

# Check if all files in this folder have the same parameters in headers
equal_or_not = check_if_JDS_files_of_equal_parameters(directory, fileList)

if same_or_not and equal_or_not:
    print('\n\n\n        :-)  All files seem to be of the same parameters!  :-) \n\n\n')
else:
    print('\n\n\n ************************************************************************************* \n *                                                                                   *')
    print(' *   Seems files in folders are different check the errors and restart the script!   *')
    print(' *                                                                                   *  '
          '\n ************************************************************************************* \n\n\n')

decision  = int(input('* Enter "1" to start processing, or "0" to stop the script:     '))
if decision != 1:
    sys.exit('\n\n\n              ***  Program stopped! *** \n\n\n')


# To print in console the header of first file
print('\n  First file header parameters: \n')
# *** Data file header read ***
[df_filename, df_filesize, df_system_name, df_obs_place, df_description,
    CLCfrq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
    df, frequency, FreqPointsNum, data_block_size] = FileHeaderReaderJDS(directory + fileList[0], 0, 1)

# Main loop by files start
for fileNo in range(len(fileList)):   # loop by files
    print('\n\n  *  File ', str(fileNo+1), ' of', str(len(fileList)))
    print('  *  File path: ', str(fileList[fileNo]))

    # *** Opening datafile ***
    fname = directory + fileList[fileNo]

    # *********************************************************************************

    # *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        CLCfrq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
        df, frequency, FreqPointsNum, data_block_size] = FileHeaderReaderJDS(fname, 0, 0)

    # Create long data files and copy first data file header to them
    if fileNo == 0 and save_long_file_aver == 1:

        with open(fname, 'rb') as file:
            # *** Data file header read ***
            file_header = file.read(1024)

        # *** Creating a name for long timeline TXT file ***
        TLfile_name = df_filename + '_Timeline.txt'
        TLfile = open(TLfile_name, 'w')  # Open and close to delete the file with the same name
        TLfile.close()

        # *** Creating a binary file with data for long data storage ***
        file_data_A_name = df_filename + '_Data_chA.dat'
        file_data_A = open(file_data_A_name, 'wb')
        file_data_A.write(file_header)
        file_data_A.close()

        if Channel == 2:
            file_data_B_name = df_filename + '_Data_chB.dat'
            file_data_B = open(file_data_B_name, 'wb')
            file_data_B.write(file_header)
            file_data_B.close()
        
        del file_header
        
    # !!! Make automatic calculations of time and frequency resolutions for waveform mode!!!

    # Manually set frequencies for one channel mode

    # if (Channel == 0 and int(CLCfrq/1000000) == 66) or (Channel == 1 and int(CLCfrq/1000000) == 66):
    #    FreqPointsNum = 8192
    #    frequency = np.linspace(0.0, 33.0, FreqPointsNum)

    # Manually set frequencies for two channels mode
    if Channel == 2 or (Channel == 0 and int(CLCfrq/1000000) == 33) or (Channel == 1 and int(CLCfrq/1000000) == 33):
        FreqPointsNum = 8192
        frequency = np.linspace(16.5, 33.0, FreqPointsNum)

    # Calculation of number of blocks and number of spectra in the file
    if Channel == 0 or Channel == 1:    # Single channel mode
        no_of_av_spectra_per_file = (df_filesize - 1024)/(2 * data_block_size * no_of_spectra_to_average)
    else:                               # Two channels mode
        no_of_av_spectra_per_file = (df_filesize - 1024)/(4 * data_block_size * no_of_spectra_to_average)

    no_of_blocks_in_file = (df_filesize - 1024) / data_block_size

    print(' Number of blocks in file:             ', no_of_blocks_in_file)
    print(' Number of spectra to average:         ', no_of_spectra_to_average)
    print(' Number of averaged spectra in file:   ', no_of_av_spectra_per_file)

    no_of_av_spectra_per_file = int(no_of_av_spectra_per_file)
    fine_CLCfrq = (int(CLCfrq/1000000.0) * 1000000.0)

    # Real time resolution of averaged spectra
    real_av_spectra_dt = (1 / fine_CLCfrq) * (data_block_size-4) * no_of_spectra_to_average
    print(' Time resolution of averaged spectrum:  ', round(real_av_spectra_dt*1000, 3), ' ms.')

    # *******************************************************************************
    #                           R E A D I N G   D A T A                             *
    # *******************************************************************************

    print('\n  *** Reading data from file *** \n')

    with open(fname, 'rb') as file:
        file.seek(1024 + data_block_size * 4 * skip_data_blocks)  # Jumping to 1024 byte from file beginning

        # *** DATA READING process ***

        # Preparing arrays for dynamic spectra
        dyn_spectra_chA = np.zeros((int(data_block_size/2), no_of_av_spectra_per_file), float)
        if Channel == 2:  # Two channels mode
            dyn_spectra_chB = np.zeros((int(data_block_size/2), no_of_av_spectra_per_file), float)

        # !!! Fake timing. Real timing to be done!!!
        TimeFigureScaleFig = np.linspace(0, no_of_av_spectra_per_file, no_of_av_spectra_per_file+1)
        for i in range(no_of_av_spectra_per_file):
            TimeFigureScaleFig[i] = str(TimeFigureScaleFig[i])

        TimeScaleFig = []
        TimeScaleFull = []
        bar = IncrementalBar(' File ' + str(fileNo+1) + ' of ' + str(len(fileList)) + ' progress: ',
                             max=no_of_av_spectra_per_file, suffix='%(percent)d%%')

        for av_sp in range(no_of_av_spectra_per_file):

            bar.next()

            # Reading and reshaping all data with readers
            if Channel == 0 or Channel == 1:  # Single channel mode
                wf_data = np.fromfile(file, dtype='i2', count = no_of_spectra_to_average * data_block_size)
                wf_data = np.reshape(wf_data, [data_block_size, no_of_spectra_to_average], order='F')
            if Channel == 2:  # Two channels mode
                wf_data = np.fromfile(file, dtype='i2', count = 2 * no_of_spectra_to_average * data_block_size)
                wf_data = np.reshape(wf_data, [data_block_size, 2 * no_of_spectra_to_average], order='F')

            # Timing
            timeline_block_str = JDS_waveform_time(wf_data, CLCfrq, data_block_size)
            TimeScaleFig.append(timeline_block_str[-1][0:12])
            TimeScaleFull.append(df_creation_timeUTC[0:10] + ' ' + timeline_block_str[-1][0:12])

            # Nulling the time blocks in waveform data
            wf_data[data_block_size-4 : data_block_size, :] = 0

            # Scaling of the data - seems to be wrong in absolute value
            wf_data = wf_data / 32768.0

            if Channel == 0 or Channel == 1:    # Single channel mode
                wf_data_chA = wf_data           # All the data is channel A data
                del wf_data                     # Deleting unnecessary array to free the memory

            if Channel == 2:  # Two channels mode

                # Resizing to obtain the matrix for separation of channels
                wf_data_new = np.zeros((2 * data_block_size, no_of_spectra_to_average))
                for i in range(2 * no_of_spectra_to_average):
                    if i % 2 == 0:
                        wf_data_new[0:data_block_size, int(i/2)] = wf_data[:, i]   # Even
                    else:
                        wf_data_new[data_block_size:2*data_block_size, int(i/2)] = wf_data[:, i]   # Odd
                del wf_data     # Deleting unnecessary array to free the memory

                # Separating the data into two channels
                wf_data_chA = np.zeros((data_block_size, no_of_spectra_to_average)) # Preparing empty array
                wf_data_chB = np.zeros((data_block_size, no_of_spectra_to_average)) # Preparing empty array
                wf_data_chA[:,:] = wf_data_new[0:(2 * data_block_size):2, :]        # Separation to channel A
                wf_data_chB[:,:] = wf_data_new[1:(2 * data_block_size):2, :]        # Separation to channel B
                del wf_data_new

            # Calculation of spectra
            spectra_chA = np.zeros_like(wf_data_chA)
            if Channel == 2:
                spectra_chB = np.zeros_like(wf_data_chB)

            for i in range(no_of_spectra_to_average):
                spectra_chA[:, i] = np.power(np.abs(np.fft.fft(wf_data_chA[:, i])), 2)
                if Channel == 2:  # Two channels mode
                    spectra_chB[:, i] = np.power(np.abs(np.fft.fft(wf_data_chB[:, i])), 2)

            # Storing only second (right) mirror part of spectra
            spectra_chA = spectra_chA[int(data_block_size/2): data_block_size, :]

            # The normal sequence of spectra data in the script  is taken to be of
            # inverse spectra which is obtained with 33 MHz clock and 16.5-33 MHz
            # frequency range. To obtain the normal spectra for 1 channel, 66 MHz
            # clock and full 0-33 MHz range the spectra must be flipped, that's
            # what is done in the next two lines
            if (Channel == 0 and int(CLCfrq/1000000) == 66) or (Channel == 1 and int(CLCfrq/1000000) == 66):
                spectra_chA = np.flipud(spectra_chA)

            if Channel == 2:
                spectra_chB = spectra_chB[int(data_block_size/2): data_block_size, :]

            # Plotting first waveform block and first immediate spectrum in a file
            if av_sp == 0:      # First data block in a file
                i = 0           # First immediate spectrum in a block

                # Prepare parameters for plot
                data_1 = wf_data_chA[:, i]
                if Channel == 0 or Channel == 1:  # Single channel mode
                    no_of_sets = 1
                    data_2 = []
                if Channel == 2:
                    no_of_sets = 2
                    data_2 = wf_data_chB[:, i]

                Suptitle = ('Waveform data, first block in file ' + str(df_filename))
                Title = (ReceiverMode+', Fclock = '+str(round(CLCfrq/1000000,1))+
                    ' MHz, Description: '+str(df_description))
                A = np.linspace(1, data_block_size, data_block_size)

                TwoOrOneValuePlot(no_of_sets, np.linspace(no_of_sets, data_block_size, data_block_size), data_1, data_2,
                                                'Channel A', 'Channel B', 1, data_block_size,
                                                -0.6, 0.6, -0.6, 0.6, 'ADC clock counts', 'Amplitude, V', 'Amplitude, V',
                                                Suptitle, Title,
                                                service_folder+'/'+ df_filename[0:14] +' Waveform first data block.png',
                                                currentDate, currentTime, Software_version)

                # Prepare parameters for plot
                data_1 = 10 * np.log10(spectra_chA[:, i])
                if Channel == 0 or Channel == 1: # Single channel mode
                    no_of_sets = 1
                    data_2 = []
                if Channel == 2:
                    no_of_sets = 2
                    data_2 = 10 * np.log10(spectra_chB[:, i])

                Suptitle = ('Immediate spectrum, first in file ' + str(df_filename))
                Title = (ReceiverMode+', Fclock = '+str(round(CLCfrq/1000000,1))+
                        ' MHz, Description: '+str(df_description))

                TwoOrOneValuePlot(no_of_sets, frequency, data_1, data_2,
                                                'Channel A', 'Channel B', frequency[0], frequency[-1],
                                                -80, 60, -80, 60, 'Frequency, MHz', 'Intensity, dB', 'Intensity, dB',
                                                Suptitle, Title,
                                                service_folder+'/'+ df_filename[0:14] +' Immediate spectrum first in file.png',
                                                currentDate, currentTime, Software_version)

            # Deleting the unnecessary matrices
            del wf_data_chA
            if Channel == 2:
                del wf_data_chB

            # Calculation the averaged spectrum
            aver_spectra_chA = spectra_chA.mean(axis=1)[:]
            if Channel == 2:
                aver_spectra_chB = spectra_chB.mean(axis=1)[:]

            # Plotting only first averaged spectrum
            if av_sp == 0:

                # Prepare parameters for plot
                data_1 = 10 * np.log10(aver_spectra_chA)
                if Channel == 0 or Channel == 1: # Single channel mode
                    no_of_sets = 1
                    data_2 = []
                if Channel == 2:
                    no_of_sets = 2
                    data_2 = 10 * np.log10(aver_spectra_chB)

                Suptitle = ('Average spectrum, first data block in file ' + str(df_filename))
                Title = (ReceiverMode+', Fclock = '+str(round(CLCfrq/1000000,1))+
                        ' MHz, Avergaed spectra: ' + str(no_of_spectra_to_average)+
                        ', Description: '+str(df_description))

                TwoOrOneValuePlot(no_of_sets, frequency, data_1, data_2, 'Channel A', 'Channel B',
                           frequency[0], frequency[-1], -80, 60, -80, 60,
                            'Frequency, MHz', 'Intensity, dB', 'Intensity, dB', Suptitle, Title,
                            service_folder+'/'+ df_filename[0:14] +' Average spectrum first data block in file.png',
                            currentDate, currentTime, Software_version)

            # Adding calculated averaged spectrum to dynamic spectra array
            dyn_spectra_chA[:, av_sp] = aver_spectra_chA[:]
            if Channel == 2: dyn_spectra_chB[:, av_sp] = aver_spectra_chB[:]

        bar.finish()

    file.close()  # Close the data file

    # Saving averaged spectra to long data files
    if save_long_file_aver == 1:
        temp = dyn_spectra_chA.transpose().copy(order='C')
        file_data_A = open(file_data_A_name, 'ab')
        file_data_A.write(temp)
        file_data_A.close()
        if Channel == 2:
            temp = dyn_spectra_chB.transpose().copy(order='C')
            file_data_B = open(file_data_B_name, 'ab')
            file_data_B.write(temp)
            file_data_B.close()

        # Saving time data to ling timeline file
        with open(TLfile_name, 'a') as TLfile:
            for i in range(no_of_av_spectra_per_file):
                TLfile.write((TimeScaleFull[i][:]) + ' \n')  # str

    # Log data (make dB scale)
    with np.errstate(invalid='ignore', divide='ignore'):
        dyn_spectra_chA = 10 * np.log10(dyn_spectra_chA)
        if Channel == 2:
            dyn_spectra_chB = 10 * np.log10(dyn_spectra_chB)

    # If the data contains minus infinity values change them to particular values
    dyn_spectra_chA[np.isinf(dyn_spectra_chA)] = 40
    if Channel == 2:
        dyn_spectra_chB[np.isinf(dyn_spectra_chB)] = 40



    # *******************************************************************************
    #             P L O T T I N G    D Y N A M I C    S P E C T R A                 *
    # *******************************************************************************

    if dyn_spectr_save_init == 1 or dyn_spectr_save_norm == 1:
        print('\n  *** Making figures of dynamic spectra *** \n')


    if dyn_spectr_save_init == 1:
        # Plot of initial dynamic spectra

        VminA = np.min(dyn_spectra_chA)
        VmaxA = np.max(dyn_spectra_chA)
        VminB = VminA
        VmaxB = VmaxA
        if Channel == 2:
            VminB = np.min(dyn_spectra_chB)
            VmaxB = np.max(dyn_spectra_chB)

        if Channel == 0 or Channel == 1: # Single channel mode
            dyn_spectra_chB = dyn_spectra_chA

        Suptitle = ('Dynamic spectrum (initial) ' + str(df_filename) + ' - Fig. '+str(1)+' of ' +
                    str(1)+'\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = ' +
                    str(round(df/1000.,3)) + ' kHz, Receiver: ' + str(df_system_name) + ', Place: ' +
                    str(df_obs_place)+'\n'+ReceiverMode+', Fclock = '+str(round(CLCfrq/1000000,1)) +
                    ' MHz, Avergaed spectra: ' + str(no_of_spectra_to_average) +
                    ' (' + str(round(no_of_spectra_to_average*TimeRes, 3)) + ' sec.), Description: ' + str(df_description))

        fig_file_name = (initial_spectra_folder + '/' + df_filename[0:14] + ' Initial dynamic spectrum fig.' +
                        str(0+1) + '.png')

        if Channel == 0 or Channel == 1: # Single channel mode
            OneDynSpectraPlot(dyn_spectra_chA, VminA, VmaxA, Suptitle,
                            'Intensity, dB', no_of_av_spectra_per_file, TimeScaleFig,
                            frequency, FreqPointsNum, colormap, 'UTC Time, HH:MM:SS.msec',
                            fig_file_name, currentDate, currentTime, Software_version, customDPI)

        if Channel == 2:
            TwoDynSpectraPlot(dyn_spectra_chA, dyn_spectra_chB, VminA, VmaxA, VminB, VmaxB, Suptitle,
                    'Intensity, dB', 'Intensity, dB', no_of_av_spectra_per_file,
                     TimeScaleFig, TimeScaleFig, frequency,
                     FreqPointsNum, colormap, 'Channel A', 'Channel B', fig_file_name,
                     currentDate, currentTime, Software_version, customDPI)

    if dyn_spectr_save_norm == 1:

        # Normalization and cleaning of data

        Normalization_dB(dyn_spectra_chA.transpose(), FreqPointsNum, no_of_av_spectra_per_file)
        if Channel == 2: Normalization_dB(dyn_spectra_chB.transpose(), FreqPointsNum, no_of_av_spectra_per_file)

        simple_channel_clean(dyn_spectra_chA, 8)
        if Channel == 2: simple_channel_clean(dyn_spectra_chB, 8)


        # Plot of normalized and cleaned dynamic spectra

        Suptitle = ('Normalized and cleaned dynamic spectrum (initial) ' + str(df_filename)+' - Fig. '+str(0+1)+' of '+
                    str(1)+'\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+
                    str(round(df/1000.,3))+' kHz, Receiver: '+str(df_system_name)+', Place: '+
                    str(df_obs_place)+'\n'+ReceiverMode+', Fclock = '+str(round(CLCfrq/1000000,1))+
                    ' MHz, Avergaed spectra: ' + str(no_of_spectra_to_average)+' ('+str(round(no_of_spectra_to_average*TimeRes, 3))+
                    ' sec.), Description: '+str(df_description))

        fig_file_name = (result_folder + '/' + df_filename[0:14] + ' Normalized and cleaned dynamic spectrum fig.' +
                        str(0+1) + '.png')

        if Channel == 0 or Channel == 1: # Single channel mode
            OneDynSpectraPlot(dyn_spectra_chA, VminNorm, VmaxNorm, Suptitle,
                                'Intensity, dB', no_of_av_spectra_per_file, TimeScaleFig,
                                frequency, FreqPointsNum, colormap, 'UTC Time, HH:MM:SS.msec',
                                fig_file_name, currentDate, currentTime, Software_version, customDPI)
        if Channel == 2:
            TwoDynSpectraPlot(dyn_spectra_chA, dyn_spectra_chB,
                        VminNorm, VmaxNorm, VminNorm, VmaxNorm, Suptitle,
                        'Intensity, dB', 'Intensity, dB', no_of_av_spectra_per_file,
                        TimeScaleFig, TimeScaleFig, frequency,
                        FreqPointsNum, colormap, 'Channel A', 'Channel B', fig_file_name,
                        currentDate, currentTime, Software_version, customDPI)

endTime = time.time()
print('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                         round((endTime - startTime)/60, 2), 'min. ) \n')
print('\n           *** Program JDS_WF_reader has finished! *** \n\n\n')
