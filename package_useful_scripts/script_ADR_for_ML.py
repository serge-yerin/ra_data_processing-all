# Python3
Software_version = '2019.05.06'
# Script intended to read, show and analyze data from ADR, to save
# data to long DAT files for further processing

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Directory of files to be analyzed:
directory = 'DATA/'

MaxNim = 2048                 # Number of data chunks for one figure
chunkSkip = 0                 # Number of chunks to skip from data beginning
RFImeanConst = 8              # Constant of RFI mitigation (usually 8)
Vmin = -120                   # Lower limit of figure dynamic range for initial spectra
Vmax = -50                    # Upper limit of figure dynamic range for initial spectra
VminNorm = 0                  # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 10                 # Upper limit of figure dynamic range for normalized spectra
VminCorrMag = -150            # Lower limit of figure dynamic range for correlation magnitude spectra
VmaxCorrMag = -30             # Upper limit of figure dynamic range for correlation magnitude spectra
customDPI = 100               # Resolution of images of dynamic spectra
colormap = 'jet'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
CorrelationProcess = 0        # Process correlation data or save time?  (1 = process, 0 = save)
Sum_Diff_Calculate = 0        # Calculate sum and diff of A & B channels?
longFileSaveAch = 0           # Save data A to long file? (1 = yes, 0 = no)
longFileSaveBch = 0           # Save data B to long file? (1 = yes, 0 = no)
longFileSaveCMP = 0           # Save correlation data (Module and Phase) to long file? (1 = yes, 0 = no)
longFileSaveCRI = 0           # Save correlation data (Real and Imaginary) to long file? (1 = yes, 0 = no)
longFileSaveSSD = 0           # Save sum / diff data to a long file?
DynSpecSaveInitial = 0        # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 1        # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 0       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
SpecterFileSaveSwitch = 0     # Save 1 immediate specter to TXT file? (1 = yes, 0 = no)
ImmediateSpNo = 100           # Number of immediate specter to save to TXT file

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
import os
import struct
import math
import numpy as np
import pylab
import matplotlib.pyplot as plt
import time
import sys
import gc
import datetime
from datetime import datetime, timedelta
from matplotlib import rc
import warnings
warnings.filterwarnings("ignore")

from package_common_modules.find_all_files_in_folder_and_subfolders import find_all_files_in_folder_and_subfolders
from package_ra_data_files_formats.read_file_header_adr import FileHeaderReaderADR, ChunkHeaderReaderADR
from package_ra_data_files_formats.FPGA_to_PC_array import FPGAtoPCarrayADR
from package_cleaning.simple_channel_clean import simple_channel_clean
from package_plot_formats.plot_formats import TwoOrOneValuePlot, OneDynSpectraPlot, TwoDynSpectraPlot
from package_ra_data_processing.f_spectra_normalization import normalization_db


################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************

print ('\n\n\n\n\n\n\n\n\n   ****************************************************')
print ('   *      ADR data files reader  v.',Software_version,'       *      (c) YeS 2018')
print ('   **************************************************** \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)
print (' ')


# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = 'ADR_for_ML_Results/'
if not os.path.exists(newpath):
    os.makedirs(newpath)


# *** Search ADR files in the directory ***

fileList, file_name_list = find_all_files_in_folder_and_subfolders(directory, '.adr', 1)


for fileNo in range (len(fileList)):   # loop by files
    print ('\n\n\n')
    print ('  *  File ',  str(fileNo+1), ' of', str(len(fileList)))
    print ('  *  File path: ', str(fileList[fileNo]))



#*********************************************************************************

    # *** Opening datafile ***
    fname = fileList[fileNo]

    # Reading the file header
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
            F_ADC, df_creation_timeUTC, ReceiverMode, ADRmode,
            sumDifMode, NAvr, TimeRes, fmin, fmax, df, frequency,
            FFT_Size, SLine, Width, BlockSize] = FileHeaderReaderADR(fname, 0, 1)

    # Reading the chunk header
    [SpInFile, SpInFrame, FrameInChunk, ChunksInFile, sizeOfChunk,
            frm_sec, frm_phase] = ChunkHeaderReaderADR(fname, 0, BlockSize, 1)

    FreqPointsNum = int(Width * 1024)

    with open(fname, 'rb') as file:


        # *** Reading indexes of data from index file '*.fft' ***
        indexes = []
        ifname = 'package_ra_data_files_formats/' + str(int(FFT_Size/2)) + '.fft'
        indexfile = open(ifname, 'r')
        num = 0
        for line in indexfile:
            ind = int(line)
            if (ind >= SLine*1024) & (ind < ((SLine+Width)*1024)):
                indexes.append(ind - SLine*1024)
            num = num + 1
        indexfile.close()


        print ('\n  *** Reading data from file *** \n')


        #************************************************************************************
        #                            R E A D I N G   D A T A                                *
        #************************************************************************************

        file.seek(1024 + (sizeOfChunk+8) * chunkSkip)  # Jumping to 1024 byte from file beginning


        if ADRmode > 2 and ADRmode < 7:           # Specter modes
            figID = -1
            figMAX = int(math.ceil((ChunksInFile-chunkSkip)/MaxNim))
            if figMAX < 1: figMAX = 1
            for fig in range (figMAX):
                Time1 = time.time()               # Timing
                figID = figID + 1
                currentTime = time.strftime("%H:%M:%S")
                print (' File # ', str(fileNo+1), ' of ', str(len(fileList)), ', figure # ', figID+1, ' of ', figMAX, '   started at: ', currentTime)
                if (ChunksInFile - chunkSkip - MaxNim * figID) < MaxNim:
                    Nim = (ChunksInFile - chunkSkip - MaxNim * figID)
                else:
                    Nim = MaxNim
                SpectrNum = Nim * SpInFrame * FrameInChunk # Number of specra in the figure



                # *** Preparing empty matrices ***
                if ADRmode == 3 or ADRmode == 5 or ADRmode == 6:
                    Data_Ch_A = np.zeros((Nim * SpInFrame * FrameInChunk, FreqPointsNum))
                    Data_Ch_A0 = np.zeros((Nim * SpInFrame * FrameInChunk, FreqPointsNum))

                if ADRmode == 4 or ADRmode == 5 or ADRmode == 6:
                    Data_Ch_B = np.zeros((Nim * SpInFrame * FrameInChunk, FreqPointsNum))
                    Data_Ch_B0 = np.zeros((Nim * SpInFrame * FrameInChunk, FreqPointsNum))

                if ADRmode == 6:
                    Data_C_Im = np.zeros((Nim * SpInFrame * FrameInChunk, FreqPointsNum))
                    Data_C_Re = np.zeros((Nim * SpInFrame * FrameInChunk, FreqPointsNum))
                    Data_C_Im0 = np.zeros((Nim * SpInFrame * FrameInChunk, FreqPointsNum))
                    Data_C_Re0 = np.zeros((Nim * SpInFrame * FrameInChunk, FreqPointsNum))
                    CorrModule = np.zeros((Nim * SpInFrame * FrameInChunk, FreqPointsNum))
                    CorrPhase = np.zeros((Nim * SpInFrame * FrameInChunk, FreqPointsNum))

                # *** DATA READING process ***

                # Reading and reshaping all data with readers
                raw = np.fromfile(file, dtype='i4', count = int((Nim * (sizeOfChunk+8))/4))
                raw = np.reshape(raw, [int((sizeOfChunk+8)/4), Nim], order='F')

                # Splitting headers from data
                headers = raw[0:1024, :]
                data = raw[1024:, :]
                del raw

                # Arranging data in right order
                if ADRmode == 3:
                    data = np.reshape(data, [FreqPointsNum, Nim*FrameInChunk*SpInFrame], order='F')
                    Data_Ch_A0 = data[0:FreqPointsNum:1, :].transpose()

                if ADRmode == 4:
                    data = np.reshape(data, [FreqPointsNum, Nim*FrameInChunk*SpInFrame], order='F')
                    Data_Ch_B0 = data[0:FreqPointsNum:1, :].transpose()

                if ADRmode == 5:
                    data = np.reshape(data, [FreqPointsNum*2, Nim*FrameInChunk*SpInFrame], order='F')
                    Data_Ch_B0 = data[0:(FreqPointsNum*2):2, :].transpose()
                    Data_Ch_A0 = data[1:(FreqPointsNum*2):2, :].transpose()

                if (ADRmode == 6):
                    data = np.reshape(data, [FreqPointsNum*4, Nim*FrameInChunk*SpInFrame], order='F')
                    Data_C_Im0 = data[0:(FreqPointsNum*4):4, :].transpose()
                    Data_C_Re0 = data[1:(FreqPointsNum*4):4, :].transpose()
                    Data_Ch_B0 = data[2:(FreqPointsNum*4):4, :].transpose()
                    Data_Ch_A0 = data[3:(FreqPointsNum*4):4, :].transpose()

                del data


                # *** Performing index changes ***
                for i in range (0, FreqPointsNum):
                    n = indexes[i]
                    if ADRmode == 3 or ADRmode == 5 or ADRmode == 6:
                        Data_Ch_A[:,n] = Data_Ch_A0[:,i]
                    if ADRmode == 4 or ADRmode == 5 or ADRmode == 6:
                        Data_Ch_B[:,n] = Data_Ch_B0[:,i]
                    if (ADRmode == 6 and CorrelationProcess == 1):
                        Data_C_Im[:,n] = Data_C_Im0[:,i]
                        Data_C_Re[:,n] = Data_C_Re0[:,i]

                # *** Deleting matrices which were nessesary for index changes ***
                del n
                if ADRmode == 3 or ADRmode == 5 or ADRmode == 6:
                    del Data_Ch_A0
                if ADRmode == 4 or ADRmode == 5 or ADRmode == 6:
                    del Data_Ch_B0
                if (ADRmode == 6 and CorrelationProcess == 1):
                    del Data_C_Im0, Data_C_Re0


                # *** Converting from FPGA to PC float format ***
                if ADRmode == 3 or ADRmode == 5 or ADRmode == 6:
                    Data_Ch_A = FPGAtoPCarrayADR(Data_Ch_A, NAvr)

                if ADRmode == 4 or ADRmode == 5 or ADRmode == 6:
                    Data_Ch_B = FPGAtoPCarrayADR(Data_Ch_B, NAvr)

                if (ADRmode == 6 and CorrelationProcess == 1):
                    Data_C_Re = FPGAtoPCarrayADR(Data_C_Re, NAvr)
                    Data_C_Im = FPGAtoPCarrayADR(Data_C_Im, NAvr)


                # *** Converting to logarythmic scale matrices ***
                if ADRmode == 3 or ADRmode == 5 or ADRmode == 6:
                    with np.errstate(divide='ignore'):
                        Data_Ch_A = 10*np.log10(Data_Ch_A)

                if ADRmode == 4 or ADRmode == 5 or ADRmode == 6:
                    with np.errstate(divide='ignore'):
                        Data_Ch_B = 10*np.log10(Data_Ch_B)


                # *** Normalizing amplitude-frequency responce ***
                if (ADRmode == 3 or ADRmode == 5 or ADRmode == 6) and DynSpecSaveCleaned == 1:
                    normalization_db(Data_Ch_A, FreqPointsNum, Nim * SpInFrame * FrameInChunk)
                if (ADRmode == 4 or ADRmode == 5 or ADRmode == 6) and DynSpecSaveCleaned == 1:
                    normalization_db(Data_Ch_B, FreqPointsNum, Nim * SpInFrame * FrameInChunk)
                if ADRmode == 6 and CorrelationProcess == 1 and CorrSpecSaveCleaned == 1:
                    normalization_db(CorrModule, FreqPointsNum, Nim * SpInFrame * FrameInChunk)

                # *** Deleting cahnnels with strong RFI ***
                if (ADRmode == 3 or ADRmode == 5 or ADRmode == 6) and DynSpecSaveCleaned == 1:
                    simple_channel_clean(Data_Ch_A, RFImeanConst)
                if (ADRmode == 4 or ADRmode == 5 or ADRmode == 6) and DynSpecSaveCleaned == 1:
                    simple_channel_clean(Data_Ch_B, RFImeanConst)
                if ADRmode == 6 and CorrelationProcess == 1 and CorrSpecSaveCleaned == 1:
                    simple_channel_clean(CorrModule, 2 * RFImeanConst)




                # *** FIGURE Cleaned and normalized dynamic spectrum of 1 channel A or B

                if ((ADRmode == 3 or ADRmode == 4) and DynSpecSaveCleaned == 1):
                    if ADRmode == 3: Data = Data_Ch_A.transpose()
                    if ADRmode == 4: Data = Data_Ch_B.transpose()

                    fig_file_name = (newpath + df_filename[0:14] +
                                        ' Dynamic spectrum fig.' + str(figID+1) + '.png')

                    fig, axarr = plt.subplots(1, 1, figsize=(10.0, 5.0))
                    im0 = axarr.imshow(np.flipud(Data), aspect='auto', vmin=Vmin, vmax=Vmax, cmap=colormap)
                    pylab.savefig(fig_file_name, bbox_inches='tight', dpi = customDPI)
                    plt.close('all')



                # *** FIGURE Dynamic spectrum channels A and B cleaned and normalized (python 3 new version) ***

                if ((ADRmode == 5 or ADRmode == 6) and DynSpecSaveCleaned == 1):


                    fig_file_name = (newpath + df_filename[0:14] + ' Dynamic spectrum fig.' + str(figID+1) + ' A.png')
                    fig = plt.figure(frameon=False)
                    fig.set_size_inches(9,6)
                    ax = fig.add_axes([0., 0., 1., 1.])
                    ax.set_axis_off()
                    fig.add_axes(ax)
                    ax.imshow(np.flipud(Data_Ch_A.transpose()), aspect='auto', vmin=VminNorm, vmax=VmaxNorm, cmap=colormap)
                    fig.savefig(fig_file_name, dpi = customDPI)
                    plt.close('all')


                    fig_file_name = (newpath + df_filename[0:14] + ' Dynamic spectrum fig.' + str(figID+1) + ' B.png')
                    fig = plt.figure(frameon=False)
                    fig.set_size_inches(9,6)
                    ax = fig.add_axes([0., 0., 1., 1.])
                    ax.set_axis_off()
                    fig.add_axes(ax)
                    ax.imshow(np.flipud(Data_Ch_B.transpose()), aspect='auto', vmin=VminNorm, vmax=VmaxNorm, cmap=colormap)
                    fig.savefig(fig_file_name, dpi = customDPI)
                    plt.close('all')





            gc.collect()

        print ('\n  Position in file: ', file.tell(), ' File size: ', df_filesize)
        if (file.tell() == df_filesize): print ('\n  File was read till the end')
        if (file.tell() < df_filesize):  print ('\n  File was NOT read till the end!!! ERROR')


endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program ADR for ML has finished! *** \n\n\n')
