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
no_of_spectra_to_average = 32   # Number of spectra to average for dynamic spectra
skip_data_blocks = 0            # Number of data blocks to skip before reading
VminNorm = 0                    # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 30                   # Upper limit of figure dynamic range for normalized spectra
colormap = 'jet'                # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
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
from f_plot_formats import OneImmedSpecterPlot, TwoImmedSpectraPlot, TwoDynSpectraPlot

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
FreqPointsNum = 8192
frequency = np.linspace(16.5, 33.0, FreqPointsNum)

no_of_blocks_in_file =  (df_filesize - 1024) / data_block_size
print (' Number of blocks in file:             ', no_of_blocks_in_file)


#*******************************************************************************
#                          R E A D I N G   D A T A                             *
#*******************************************************************************

print ('\n  *** Reading data from file *** \n')

with open(fname, 'rb') as file:
    file.seek(1024 + data_block_size * 4 * skip_data_blocks)  # Jumping to 1024 byte from file beginning #+ (sizeOfChunk+8) * chunkSkip

    # *** DATA READING process ***

    if Channel == 0 or Channel == 1: # Single channel mode
        pass # To be developed

    if Channel == 2: # Two cahnnels mode
        no_of_av_spectra_per_file = (df_filesize - 1024)/(2 * data_block_size * no_of_spectra_to_average * 2)
        print (' Number of averaged spectra in file:   ', no_of_av_spectra_per_file)
        no_of_av_spectra_per_file = int(no_of_av_spectra_per_file)
        dyn_spectra_chA = np.zeros((int(data_block_size/2), no_of_av_spectra_per_file), float)
        dyn_spectra_chB = np.zeros((int(data_block_size/2), no_of_av_spectra_per_file), float)

        # !!! Fake timing. Real timing to be done!!!
        TimeFigureScaleFig = np.linspace(0, no_of_av_spectra_per_file, no_of_av_spectra_per_file+1)
        for i in range(no_of_av_spectra_per_file):
            TimeFigureScaleFig[i] = str(TimeFigureScaleFig[i])
        TimeScaleFig = TimeFigureScaleFig


        for av_sp in range (no_of_av_spectra_per_file):
            # Reading and reshaping all data with readers
            wf_data = np.fromfile(file, dtype='i2', count = no_of_spectra_to_average * data_block_size)
            wf_data = np.reshape(wf_data, [data_block_size, no_of_spectra_to_average], order='F')

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

            # Resizing to obtain the matrix for separation of channels
            no_of_spectra = int(no_of_spectra_to_average/2)
            wf_data_new = np.zeros((2 * data_block_size, no_of_spectra))
            for i in range(2 * no_of_spectra):
                if i % 2 == 0:
                    wf_data_new[0:data_block_size, int(i/2)] = wf_data[:, i]   # Even
                else:
                    wf_data_new[data_block_size:2*data_block_size, int(i/2)] = wf_data[:, i]   # Odd
            del wf_data     # Deleting unnecessary array to free the memory


            # Separating the data into two channels
            wf_data_chA = np.zeros((data_block_size, no_of_spectra))        # Preparing empty array
            wf_data_chB = np.zeros((data_block_size, no_of_spectra))        # Preparing empty array
            wf_data_chA[:,:] = wf_data_new[0:(2 * data_block_size):2, :]    # Separation to channel A
            wf_data_chB[:,:] = wf_data_new[1:(2 * data_block_size):2, :]    # Separation to channel B


            # Calculation of spectra
            spectra_chA = np.zeros_like(wf_data_chA)
            spectra_chB = np.zeros_like(wf_data_chB)
            for i in range (no_of_spectra):
                with np.errstate(invalid='ignore', divide='ignore'):
                    spectra_chA[:,i] = 10 * np.log10(np.power(np.abs(np.fft.fft(wf_data_chA[:,i])), 2))
                    spectra_chB[:,i] = 10 * np.log10(np.power(np.abs(np.fft.fft(wf_data_chB[:,i])), 2))


            # Storing only second (right) mirror part of spectra
            spectra_chA = spectra_chA[int(data_block_size/2): data_block_size, :]
            spectra_chB = spectra_chB[int(data_block_size/2): data_block_size, :]


            # Plotting first waveform block and first immediate spectrum in a file
            if av_sp == 0:      # First data block in a file
                i = 0           # First immediate spectrum in a block
                fig = plt.figure(figsize = (16,12))
                ax1 = fig.add_subplot(211)
                ax1.plot(wf_data_chA[:,i], label = 'Channel A')
                ax1.set_ylim(-3500, 3500)
                ax1.legend(loc = 'upper right', fontsize = 10)
                ax2 = fig.add_subplot(212)
                ax2.plot(wf_data_chB[:,i], label = 'Channel B')
                ax2.set_ylim(-3500, 3500)
                ax2.legend(loc = 'upper right', fontsize = 10)
                pylab.savefig(newpath+'/'+ df_filename[0:14] +' Waveform first data block'+str(i)+'.png', bbox_inches='tight', dpi = 300)
                plt.close('all')

                fig = plt.figure(figsize = (16,12))
                ax1 = fig.add_subplot(211)
                ax1.plot(spectra_chA[:, i], label = 'Channel A')
                ax1.set_ylim(10, 150)
                ax1.legend(loc = 'upper right', fontsize = 10)
                ax2 = fig.add_subplot(212)
                ax2.plot(spectra_chB[:, i], label = 'Channel B')
                ax2.set_ylim(10, 150)
                ax2.legend(loc = 'upper right', fontsize = 10)
                pylab.savefig(newpath+'/'+ df_filename[0:14] +' Immediate spectrum first data block'+str(i)+'.png', bbox_inches='tight', dpi = 300)
                plt.close('all')

            del wf_data_chA, wf_data_chB


            # Calculation the averaged spectrum
            aver_spectra_chA = spectra_chA.mean(axis=1)[:]
            aver_spectra_chB = spectra_chB.mean(axis=1)[:]


            # Plotting only first averaged spectrum
            if av_sp == 0:
                fig = plt.figure(figsize = (16,12))
                ax1 = fig.add_subplot(211)
                ax1.plot(aver_spectra_chA, label = 'Channel A')
                ax1.set_ylim(10, 150)
                ax1.legend(loc = 'upper right', fontsize = 10)
                ax2 = fig.add_subplot(212)
                ax2.plot(aver_spectra_chB, label = 'Channel B')
                ax2.set_ylim(10, 150)
                ax2.legend(loc = 'upper right', fontsize = 10)
                pylab.savefig(newpath+'/'+ df_filename[0:14] +' Average spectrum first data block '+str(av_sp)+'.png', bbox_inches='tight', dpi = 300)
                plt.close('all')


            # Adding calculated averaged spectrum to dynamic spectra array
            dyn_spectra_chA[:, av_sp] = aver_spectra_chA[:]
            dyn_spectra_chB[:, av_sp] = aver_spectra_chB[:]


# If the data contains minus infinity values change them to particular values
dyn_spectra_chA[np.isinf(dyn_spectra_chA)] = 40
dyn_spectra_chB[np.isinf(dyn_spectra_chB)] = 40

#*******************************************************************************
#            P L O T T I N G    D Y N A M I C    S P E C T R A                 *
#*******************************************************************************

print ('\n  *** Making figures of dynamic spectra *** \n')

# Plot of initial dynamic spectra

VminA = np.min(dyn_spectra_chA)
VmaxA = np.max(dyn_spectra_chA)
VminB = np.min(dyn_spectra_chB)
VmaxB = np.max(dyn_spectra_chB)

Suptitle = ('Dynamic spectrum (initial) ' + str(df_filename)+' - Fig. '+str(0+1)+' of '+
            str(1)+'\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+
            str(round(df/1000.,3))+' kHz, Receiver: '+str(df_system_name)+', Place: '+
            str(df_obs_place)+'\n'+ReceiverMode+', Description: '+str(df_description))

fig_file_name = (newpath + '/' + df_filename[0:14] + ' Initial dynamic spectrum fig.' +
                str(0+1) + '.png')


TwoDynSpectraPlot(dyn_spectra_chA.transpose(), dyn_spectra_chB.transpose(),
                VminA, VmaxA, VminB, VmaxB, Suptitle,
                'Intensity, dB', 'Intensity, dB', no_of_av_spectra_per_file,
                TimeFigureScaleFig, TimeScaleFig, frequency,
                FreqPointsNum, colormap, 'Channel A', 'Channel B', fig_file_name,
                currentDate, currentTime, Software_version, customDPI)


# Normalization and cleaning of data

Normalization_dB(dyn_spectra_chA.transpose(), FreqPointsNum, no_of_av_spectra_per_file)
Normalization_dB(dyn_spectra_chB.transpose(), FreqPointsNum, no_of_av_spectra_per_file)

simple_channel_clean(dyn_spectra_chA, 8)
simple_channel_clean(dyn_spectra_chB, 8)


# Plot of normalized and cleaned dynamic spectra

Suptitle = ('Normalized and cleaned dynamic spectrum (initial) ' + str(df_filename)+' - Fig. '+str(0+1)+' of '+
            str(1)+'\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+
            str(round(df/1000.,3))+' kHz, Receiver: '+str(df_system_name)+', Place: '+
            str(df_obs_place)+'\n'+ReceiverMode+', Description: '+str(df_description))

fig_file_name = (newpath + '/' + df_filename[0:14] + ' Normalized and cleaned dynamic spectrum fig.' +
                str(0+1) + '.png')

TwoDynSpectraPlot(dyn_spectra_chA.transpose(), dyn_spectra_chB.transpose(),
                VminNorm, VmaxNorm, VminNorm, VmaxNorm, Suptitle,
                'Intensity, dB', 'Intensity, dB', no_of_av_spectra_per_file,
                TimeFigureScaleFig, TimeScaleFig, frequency,
                FreqPointsNum, colormap, 'Channel A', 'Channel B', fig_file_name,
                currentDate, currentTime, Software_version, customDPI)


file.close()  # Close the data file


endTime = time.time()    # Time of calculations
print ('\n The program execution lasted for ', round((endTime - startTime),2), 'seconds')
print ('\n\n    *** Program JDS_WF_reader has finished! *** \n\n\n')
