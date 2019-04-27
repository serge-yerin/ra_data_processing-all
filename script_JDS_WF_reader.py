# Python3
#
#   !!!! NOT FINISHED !!! Do not use!
#
Software_version = '2019.04.13'
# Program intended to read, show and analyze data from DSPZ receivers in wvaform mode

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Directory of files to be analyzed:
fname = 'DATA/E251015_050029 - wf.jds'
N_samples = 16384

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
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)
print (' ')



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
    CLCfrq, df_creation_timeUTC, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
    df, frequency, FreqPointsNum, Channel] = FileHeaderReaderDSP(fname, 0)


print (' ')
print ('  *** Reading data from file ***')
print (' ')


#************************************************************************************
#                            R E A D I N G   D A T A                                *
#************************************************************************************
'''
n_points = 16384 # number of points in one frame
n_frames = np.power(2, 11*16)
#N_frames = 2^16;  --- ???

Nf = n_points
Nav = 16
Nt = n_frames / Nav
# print('Time frame is ', Nt * Nav * Nf * 1 / 66000000,  ' sec.')
# print('Time resolution is ', (1/66000000) * Nf * Nav * 1000, ' ms for one channel and ', (1 / 33000000 * Nf * Nav * 1000), ' ms for two channels')
'''

with open(fname, 'rb') as file:
    file.seek(1024)  # Jumping to 1024 byte from file beginning #+ (sizeOfChunk+8) * chunkSkip

    # *** DATA READING process ***

    if Channel == 0 or Channel == 1: # Single channel mode
        pass
    if Channel == 2: # Two cahnnels mode
        # Reading and reshaping all data with readers
        wf_data = np.fromfile(file, dtype='i2', count = 2 * N_samples)
        wf_data = np.reshape(wf_data, [N_samples, 2], order='F')

        wf_data_chA = wf_data[:, 0]
        wf_data_chB = wf_data[:, 1]

        Sp1 = 10 * np.log10(np.power(np.abs(np.fft.fft(wf_data_chA)), 2))
        Sp2 = 10 * np.log10(np.power(np.abs(np.fft.fft(wf_data_chB)), 2))

        print (' Data length = ', len(wf_data_chA),' Specter length = ', len(Sp1))

        fig = plt.figure(figsize = (16,12))
        ax1 = fig.add_subplot(111)
        ax1.plot(Sp1, label = '1')
        ax1.plot(Sp2, label = '2')
        ax1.legend(loc = 'upper right', fontsize = 8)
        pylab.savefig('Spectra.png', bbox_inches='tight', dpi = 300)
        plt.close('all')




'''
        kk = 1 : N/2;
        for i = 1 : N_frames
           data = fread(fid, N, '*int16'); % read  data
           %fseek(fid, 1024 + N*cnt*100, -1);
           data = single(data');
           if length(data) < N
              data = [data, zeros(1, N - length(data))];
           end

           % data without  time markers --- 'wtm'
           data(end - 3 : end) = [0, 0, 0, 0];

           %WF1 = data(2*kk - 1); % odd channel A
           %WF2 = data(2*kk); % even channel B

           N2 = N/2;
           WF1(N2*(i-1)+1 : N2 * i) = data(2*kk - 1); % odd channel A
           WF2(N2*(i-1)+1 : N2 * i) = data(2*kk); % even channel B

'''

file.close()  #Here we close the file


endTime = time.time()    # Time of calculations

print (' ')
print ('  The program execution lasted for ', round((endTime - startTime),2), 'seconds')
for i in range (0,2) : print (' ')
print ('    *** Program JDS_reader has finished! ***')
for i in range (0,3) : print (' ')
