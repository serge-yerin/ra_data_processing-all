# Python3
#
#   !!!! NOT FINISHED !!! Do not use!
#
Software_version = '2019.04.29'
# Program intended to read, show and analyze data from DSPZ receivers in wvaform mode

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Directory of files to be analyzed:
fname = 'DATA/E251015_050029 - wf.jds'
no_of_blocks = 256
skip_data_blocks = 0
################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
# Common functions
import os
import sys
import pylab
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import gc
import datetime
from datetime import datetime, timedelta

# My functions
from f_file_header_JDS import FileHeaderReaderDSP
from f_FPGA_to_PC_array import FPGAtoPCarrayDSP
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
print ('  Today is ', currentDate, ' time is ', currentTime)
print (' ')

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


print (' ')
print ('  *** Reading data from file ***')
print (' ')


#************************************************************************************
#                            R E A D I N G   D A T A                                *
#************************************************************************************


with open(fname, 'rb') as file:
    file.seek(1024 + data_block_size * 4 * skip_data_blocks)  # Jumping to 1024 byte from file beginning #+ (sizeOfChunk+8) * chunkSkip

    # *** DATA READING process ***

    if Channel == 0 or Channel == 1: # Single channel mode
        pass
    if Channel == 2: # Two cahnnels mode

        # Reading and reshaping all data with readers
        wf_data = np.fromfile(file, dtype='i2', count = no_of_blocks * data_block_size)
        wf_data = np.reshape(wf_data, [data_block_size, no_of_blocks], order='F')


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


        # Nulling the time data
        wf_data[data_block_size-4 : data_block_size, :] = 0



        # Resizing to obtain the matrix for separation of channels

        no_of_spectra = int(no_of_blocks/2)
        #print(' Size = ', wf_data.shape)
        wf_data_new = np.zeros((2 * data_block_size, no_of_spectra))
        for i in range(2 * no_of_spectra):
            if i % 2 == 0:
                wf_data_new[0:data_block_size, int(i/2)] = wf_data[:, i]   # Even
            else:
                wf_data_new[data_block_size:2*data_block_size, int(i/2)] = wf_data[:, i]   # Odd
        del wf_data
        #print(' Size = ', wf_data.shape)

        # Separating the data into two channels
        wf_data_chA = np.zeros((data_block_size, no_of_spectra))
        wf_data_chB = np.zeros((data_block_size, no_of_spectra))
        wf_data_chA[:,:] = wf_data_new[0:(2 * data_block_size):2, :]
        wf_data_chB[:,:] = wf_data_new[1:(2 * data_block_size):2, :]

        #print(' Size wf_data_chA = ', wf_data_chA.shape)
        #print(' Size wf_data_chB = ', wf_data_chB.shape)


        # Calculation of spectra
        spectra_chA = np.zeros_like(wf_data_chA)
        spectra_chB = np.zeros_like(wf_data_chB)
        for i in range (no_of_spectra):
            with np.errstate(invalid='ignore', divide='ignore'):
                spectra_chA[:,i] = 10 * np.log10(np.power(np.abs(np.fft.fft(wf_data_chA[:,i])), 2))
                spectra_chB[:,i] = 10 * np.log10(np.power(np.abs(np.fft.fft(wf_data_chB[:,i])), 2))

        print ('\n  Data length = ', wf_data_chA.shape,' Specter length = ', spectra_chA.shape)

        del wf_data_chA, wf_data_chB

        spectra_chA = spectra_chA[int(data_block_size/2): data_block_size, :]
        spectra_chB = spectra_chB[int(data_block_size/2): data_block_size, :]


        nowTime = time.time()
        print ('\n  Data read and transformation         took ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime


        '''
        # Plotting each waveform block and each specter
        for i in range (no_of_spectra):

            fig = plt.figure(figsize = (16,12))
            ax1 = fig.add_subplot(211)
            ax1.plot(wf_data_chA[:,i], label = '1')
            ax1.set_ylim(-3500, 3500)
            ax1.legend(loc = 'upper right', fontsize = 8)
            ax2 = fig.add_subplot(212)
            ax2.plot(wf_data_chB[:,i], label = '2')
            ax2.set_ylim(-3500, 3500)
            ax2.legend(loc = 'upper right', fontsize = 8)
            pylab.savefig(newpath+'/Waveform '+str(i)+'.png', bbox_inches='tight', dpi = 300)
            plt.close('all')

            fig = plt.figure(figsize = (16,12))
            ax1 = fig.add_subplot(211)
            ax1.plot(spectra_chA[int(data_block_size/2): data_block_size, i], label = '1')
            ax1.set_ylim(10, 150)
            ax1.legend(loc = 'upper right', fontsize = 8)
            ax2 = fig.add_subplot(212)
            ax2.plot(spectra_chB[int(data_block_size/2): data_block_size, i], label = '2')
            ax2.set_ylim(10, 150)
            ax2.legend(loc = 'upper right', fontsize = 8)
            pylab.savefig(newpath+'/Spectra '+str(i)+'.png', bbox_inches='tight', dpi = 300)
            plt.close('all')

        '''

        # Plotting averaged specter
        aver_spectra_chA = spectra_chA.mean(axis=1)[:]
        aver_spectra_chB = spectra_chB.mean(axis=1)[:]

        fig = plt.figure(figsize = (16,12))
        ax1 = fig.add_subplot(211)
        ax1.plot(aver_spectra_chA, label = '1')
        ax1.set_ylim(10, 150)
        ax1.legend(loc = 'upper right', fontsize = 8)
        ax2 = fig.add_subplot(212)
        ax2.plot(aver_spectra_chB, label = '2')
        ax2.set_ylim(10, 150)
        ax2.legend(loc = 'upper right', fontsize = 8)
        pylab.savefig(newpath+'/Spectra_mean.png', bbox_inches='tight', dpi = 300)
        plt.close('all')

        nowTime = time.time()
        print ('\n  Figure plotiing                      took ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime

file.close()  #Here we close the file


endTime = time.time()    # Time of calculations

print (' ')
print ('  The program execution lasted for ', round((endTime - startTime),2), 'seconds')
for i in range (0,2) : print (' ')
print ('    *** Program JDS_reader has finished! ***')
for i in range (0,3) : print (' ')
