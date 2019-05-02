# Python3
#
#   !!!! NOT FINISHED !!! Works only for 2-channel files
#
Software_version = '2019.04.29'
# Program intended to read, show and analyze data from DSPZ receivers in wvaform mode

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Directory of files to be analyzed:
fname = 'DATA/E251015_050029 - wf.jds'
no_of_spectra_to_average = 64   # Number of spectra to average for dynamic spectra
skip_data_blocks = 0            # Number of data blocks to skip before reading
VminNorm = 0                    # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 6                    # Upper limit of figure dynamic range for normalized spectra
colormap = 'Greys'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
customDPI = 300                 # Resolution of images of dynamic spectra


################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
# Common functions
import os
import pylab
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
from datetime import datetime, timedelta

# My functions
from f_file_header_JDS import FileHeaderReaderDSP
from f_spectra_normalization import Normalization_dB
from f_ra_data_clean import simple_channel_clean
from f_plot_formats import OneImmedSpecterPlot, TwoImmedSpectraPlot, OneDynSpectraPlot, TwoDynSpectraPlot
from f_plot_formats import TwoOrOneValuePlot
################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************

for i in range(8): print (' ')
print ('   ****************************************************')
print ('   *     JDSwf data files reader  v.', Software_version,'      *      (c) YeS 2019')
print ('   ****************************************************')
for i in range(3): print (' ')


startTime = time.time()
previousTime = startTime
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, '\n')


# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = "JDS_WF_Results"
if not os.path.exists(newpath):
    os.makedirs(newpath)

'''
# *** Search JDS files in the directory ***
fileList=[]
i = 0
print ('  Directory: ', directory, '\n')
Log_File.write('  Directory: %s \n' %directory )
print ('  List of files to be analyzed: ')
Log_File.write('  List of files to be analyzed: \n')
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.jds'):
            i = i + 1
            print ('         ', i, ') ', file)
            Log_File.write('           '+str(i)+') %s \n' %file )
            fileList.append(str(os.path.join(root, file)))
Log_File.close()

for fileNo in range (len(fileList)):   # loop by files
    for i in range(3): print (' ')
    print ('  *  File ',  str(fileNo+1), ' of', str(len(fileList)))
    print ('  *  File path: ', str(fileList[fileNo]))
    Log_File = open("JDS_Results/Service/Log.txt", "a")
    Log_File.write('\n\n\n  * File '+str(fileNo+1)+' of %s \n' %str(len(fileList)))
    Log_File.write('  * File path: %s \n\n\n' %str(fileList[fileNo]) )
'''
#*********************************************************************************

# *** Data file header read ***
[df_filename, df_filesize, df_system_name, df_obs_place, df_description,
    CLCfrq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
    df, frequency, FreqPointsNum, data_block_size] = FileHeaderReaderDSP(fname, 0)

# !!! Make automatic calculations of time and frequency resolutions for waveform mode!!!
# Manually set frequencies
if (Channel == 0 and int(CLCfrq/1000000) == 66) or (Channel == 1 and int(CLCfrq/1000000) == 66):
    FreqPointsNum = 8192
    frequency = np.linspace(0.0, 33.0, FreqPointsNum)

if Channel == 2 or (Channel == 0 and int(CLCfrq/1000000) == 33) or (Channel == 1 and int(CLCfrq/1000000) == 33): # Two cahnnels mode
    FreqPointsNum = 8192
    frequency = np.linspace(16.5, 33.0, FreqPointsNum)

# Calculation of number of blocks and number of spectra in the file
if Channel == 0 or Channel == 1: # Single channel mode
    no_of_av_spectra_per_file = (df_filesize - 1024)/(2 * data_block_size * no_of_spectra_to_average)

if Channel == 2: # Two cahnnels mode
    no_of_av_spectra_per_file = (df_filesize - 1024)/(2 * data_block_size * no_of_spectra_to_average * 2)

no_of_blocks_in_file =  (df_filesize - 1024) / data_block_size

print (' Number of blocks in file:             ', no_of_blocks_in_file)
print (' Number of spectra to average:         ', no_of_spectra_to_average)
print (' Number of averaged spectra in file:   ', no_of_av_spectra_per_file)

no_of_av_spectra_per_file = int(no_of_av_spectra_per_file)

#*******************************************************************************
#                          R E A D I N G   D A T A                             *
#*******************************************************************************

print ('\n  *** Reading data from file *** \n')

with open(fname, 'rb') as file:
    file.seek(1024 + data_block_size * 4 * skip_data_blocks)  # Jumping to 1024 byte from file beginning #+ (sizeOfChunk+8) * chunkSkip

    # *** DATA READING process ***

    # Preparing arrays for dynamic spectra
    dyn_spectra_chA = np.zeros((int(data_block_size/2), no_of_av_spectra_per_file), float)
    if Channel == 2: # Two cahnnels mode
        dyn_spectra_chB = np.zeros((int(data_block_size/2), no_of_av_spectra_per_file), float)

    # !!! Fake timing. Real timing to be done!!!
    TimeFigureScaleFig = np.linspace(0, no_of_av_spectra_per_file, no_of_av_spectra_per_file+1)
    for i in range(no_of_av_spectra_per_file):
        TimeFigureScaleFig[i] = str(TimeFigureScaleFig[i])
    TimeScaleFig = TimeFigureScaleFig


    for av_sp in range (no_of_av_spectra_per_file):

        # Reading and reshaping all data with readers
        if Channel == 0 or Channel == 1: # Single channel mode
            wf_data = np.fromfile(file, dtype='i2', count = no_of_spectra_to_average * data_block_size)
            wf_data = np.reshape(wf_data, [data_block_size, no_of_spectra_to_average], order='F')
        if Channel == 2: # Two cahnnels mode
            wf_data = np.fromfile(file, dtype='i2', count = 2 * no_of_spectra_to_average * data_block_size)
            wf_data = np.reshape(wf_data, [data_block_size, 2 * no_of_spectra_to_average], order='F')


        '''
        !!! *** TO BE CLARIFIED *** !!!

        # Singling out time data
        word_1 = np.uint32(wf_data[data_block_size-4])
        word_2 = np.uint32(wf_data[data_block_size-3])
        new_1 = [bin(x)[2:].zfill(32) for x in word_1]
        new_2 = [bin(x)[2:].zfill(32) for x in word_2]
        for i in range(len(new_1)):
            print(new_1[i], '  ', new_2[i])
        '''

        phase_of_second = np.uint32(wf_data[data_block_size - 3, :])
        second_of_day = np.uint32(wf_data[data_block_size - 2, :])
        #print ('  Sec of day:', second_of_day)
        #print ('  Phase of sec:', phase_of_second)

        # Nulling the time blocks in waveform data
        wf_data[data_block_size-4 : data_block_size, :] = 0

        # Scaling of the data
        wf_data = wf_data / 32768.0

        if Channel == 0 or Channel == 1:    # Single channel mode
            wf_data_chA = wf_data           # All the data is channel A data
            del wf_data                     # Deleting unnecessary array to free the memory

        if Channel == 2: # Two cahnnels mode

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
        if Channel == 2: spectra_chB = np.zeros_like(wf_data_chB)


        for i in range (no_of_spectra_to_average):
            with np.errstate(invalid='ignore', divide='ignore'):
                spectra_chA[:,i] = 10 * np.log10(np.power(np.abs(np.fft.fft(wf_data_chA[:,i])), 2))
                if Channel == 2: # Two cahnnels mode
                    spectra_chB[:,i] = 10 * np.log10(np.power(np.abs(np.fft.fft(wf_data_chB[:,i])), 2))


        # Storing only second (right) mirror part of spectra
        spectra_chA = spectra_chA[int(data_block_size/2): data_block_size, :]

        # The normal sequence of spectra data in the script  is taken to be of
        # inverse spectra which is obtained with 33 MHz clock and 16.5-33 MHz
        # frequency range. To obtain the normal spectra for 1 channel, 66 MHz
        # clock and full 0-33 MHz range the spectra must be flipped, that's
        # what is done in the next two lines
        if (Channel == 0 and int(CLCfrq/1000000) == 66) or (Channel == 1 and int(CLCfrq/1000000) == 66):
            spectra_chA = np.flipud(spectra_chA)

        if Channel == 2: spectra_chB = spectra_chB[int(data_block_size/2): data_block_size, :]


        # Plotting first waveform block and first immediate spectrum in a file
        if av_sp == 0:      # First data block in a file
            i = 0           # First immediate spectrum in a block

            # Prepare parameters for plot
            data_1 = wf_data_chA[:,i]
            if Channel == 0 or Channel == 1: # Single channel mode
                no_of_sets = 1
                data_2 = []
            if Channel == 2:
                no_of_sets = 2
                data_2 = wf_data_chB[:,i]

            Suptitle = ('Waveform data, first block in file ' + str(df_filename))
            Title = (ReceiverMode+', Fclock = '+str(round(CLCfrq/1000000,1))+
                ' MHz, Description: '+str(df_description))
            A = np.linspace(1, data_block_size, data_block_size)

            TwoOrOneValuePlot(no_of_sets, np.linspace(no_of_sets, data_block_size, data_block_size), data_1, data_2,
                                            'Channel A', 'Channel B', 1, data_block_size,
                                            -0.6, 0.6, 'ADC clock counts', 'Amplitude, V',
                                            Suptitle, Title,
                                            newpath+'/'+ df_filename[0:14] +' Waveform first data block.png',
                                            currentDate, currentTime, Software_version)

            # Prepare parameters for plot
            data_1 = spectra_chA[:, i]
            if Channel == 0 or Channel == 1: # Single channel mode
                no_of_sets = 1
                data_2 = []
            if Channel == 2:
                no_of_sets = 2
                data_2 = spectra_chB[:, i]

            Suptitle = ('Immediate spectrum, first in file ' + str(df_filename))
            Title = (ReceiverMode+', Fclock = '+str(round(CLCfrq/1000000,1))+
                    ' MHz, Description: '+str(df_description))


            TwoOrOneValuePlot(no_of_sets, frequency, data_1, data_2,
                                            'Channel A', 'Channel B', frequency[0], frequency[len(frequency)-1],
                                            -80, 60, 'Frequency, MHz', 'Intensity, dB',
                                            Suptitle, Title,
                                            newpath+'/'+ df_filename[0:14] +' Immediate spectrum first in file.png',
                                            currentDate, currentTime, Software_version)
        # Deleting the unnecessary matrices
        del wf_data_chA
        if Channel == 2: del wf_data_chB


        # Calculation the averaged spectrum
        aver_spectra_chA = spectra_chA.mean(axis=1)[:]
        if Channel == 2:  aver_spectra_chB = spectra_chB.mean(axis=1)[:]


        # Plotting only first averaged spectrum
        if av_sp == 0:

            # Prepare parameters for plot
            data_1 = aver_spectra_chA
            if Channel == 0 or Channel == 1: # Single channel mode
                no_of_sets = 1
                data_2 = []
            if Channel == 2:
                no_of_sets = 2
                data_2 = aver_spectra_chB

            Suptitle = ('Average spectrum, first data block in file ' + str(df_filename))
            Title = (ReceiverMode+', Fclock = '+str(round(CLCfrq/1000000,1))+
                    ' MHz, Avergaed spectra: ' + str(no_of_spectra_to_average)+
                    ', Description: '+str(df_description))

            TwoOrOneValuePlot(no_of_sets, frequency, data_1, data_2,
                        'Channel A', 'Channel B', frequency[0], frequency[len(frequency)-1],
                        -80, 60, 'Frequency, MHz', 'Intensity, dB',
                        Suptitle, Title,
                        newpath+'/'+ df_filename[0:14] +' Average spectrum first data block in file.png',
                        currentDate, currentTime, Software_version)


        # Adding calculated averaged spectrum to dynamic spectra array
        dyn_spectra_chA[:, av_sp] = aver_spectra_chA[:]
        if Channel == 2: dyn_spectra_chB[:, av_sp] = aver_spectra_chB[:]

file.close()  # Close the data file

# If the data contains minus infinity values change them to particular values
dyn_spectra_chA[np.isinf(dyn_spectra_chA)] = 40
if Channel == 2: dyn_spectra_chB[np.isinf(dyn_spectra_chB)] = 40

#*******************************************************************************
#            P L O T T I N G    D Y N A M I C    S P E C T R A                 *
#*******************************************************************************

print ('\n  *** Making figures of dynamic spectra *** \n')

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

Suptitle = ('Dynamic spectrum (initial) ' + str(df_filename)+' - Fig. '+str(0+1)+' of '+
            str(1)+'\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+
            str(round(df/1000.,3))+' kHz, Receiver: '+str(df_system_name)+', Place: '+
            str(df_obs_place)+'\n'+ReceiverMode+', Fclock = '+str(round(CLCfrq/1000000,1))+
            ' MHz, Avergaed spectra: ' + str(no_of_spectra_to_average)+', Description: '+str(df_description))

fig_file_name = (newpath + '/' + df_filename[0:14] + ' Initial dynamic spectrum fig.' +
                str(0+1) + '.png')

if Channel == 0 or Channel == 1: # Single channel mode
    OneDynSpectraPlot(dyn_spectra_chA, VminA, VmaxA, Suptitle,
                    'Intensity, dB', no_of_av_spectra_per_file, TimeScaleFig,
                    frequency, FreqPointsNum, colormap, 'UTC Time, HH:MM:SS.msec',
                    fig_file_name, currentDate, currentTime, Software_version, customDPI)

if Channel == 2:
    TwoDynSpectraPlot(dyn_spectra_chA, dyn_spectra_chB,
                    VminA, VmaxA, VminB, VmaxB, Suptitle,
                    'Intensity, dB', 'Intensity, dB', no_of_av_spectra_per_file,
                    TimeFigureScaleFig, TimeScaleFig, frequency,
                    FreqPointsNum, colormap, 'Channel A', 'Channel B', fig_file_name,
                    currentDate, currentTime, Software_version, customDPI)


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
            ' MHz, Avergaed spectra: ' + str(no_of_spectra_to_average)+
            ', Description: '+str(df_description))

fig_file_name = (newpath + '/' + df_filename[0:14] + ' Normalized and cleaned dynamic spectrum fig.' +
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
                TimeFigureScaleFig, TimeScaleFig, frequency,
                FreqPointsNum, colormap, 'Channel A', 'Channel B', fig_file_name,
                currentDate, currentTime, Software_version, customDPI)



endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program JDS_WF_reader has finished! *** \n\n\n')
