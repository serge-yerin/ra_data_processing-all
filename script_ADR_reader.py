# Python3
Software_version = '2019.03.28'
# Program intended to read, show and analyze data from ADR

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************
# Directory of files to be analyzed:
directory = 'DATA/'           # 'h:/2019.04.02_UTR2_3C461_interferometer/'


MaxNim = 8192                 # Number of data chunks for one figure
chunkSkip = 0                 # Number of chunks to skip from data beginning
RFImeanConst = 8              # Constant of RFI mitigation (usually 8)
Vmin = -120                   # Lower limit of figure dynamic range for initial spectra
Vmax = -50                    # Upper limit of figure dynamic range for initial spectra
VminNorm = 0                  # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 15                 # Upper limit of figure dynamic range for normalized spectra
VminCorrMag = -150            # Lower limit of figure dynamic range for correlation magnitude spectra
VmaxCorrMag = -30             # Upper limit of figure dynamic range for correlation magnitude spectra
customDPI = 300               # Resolution of images of dynamic spectra
colormap = 'jet'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
CorrelationProcess = 1        # Process correlation data or save time?  (1 = process, 0 = save)
Sum_Diff_Calculate = 0        # Calculate sum and diff of A & B channels?
longFileSaveAch = 1           # Save data A to long file? (1 = yes, 0 = no)
longFileSaveBch = 1           # Save data B to long file? (1 = yes, 0 = no)
longFileSaveCMP = 0           # Save correlation data (Module and Phase) to long file? (1 = yes, 0 = no)
longFileSaveCRI = 0           # Save correlation data (Real and Imaginary) to long file? (1 = yes, 0 = no)
longFileSaveSSD = 0           # Save sum / diff data to a long file?
DynSpecSaveInitial = 0        # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 1        # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 1       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
ColorBarSwitch = 1            # Add ColorBarSwitch to dynamic spectrum picture? (1 = yes, 0 = no)
SpecterFileSaveSwitch = 1     # Save 1 immediate specter to TXT file? (1 = yes, 0 = no)
ImmediateSpNo = 100           # Number of immediate specter to save to TXT file

#*************************************************************



#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************
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


from f_file_header_ADR import FileHeaderReaderADR, ChunkHeaderReaderADR
from f_FPGA_to_PC_array import FPGAtoPCarrayADR
from f_ra_data_clean import simple_channel_clean
from f_plot_formats import OneImmedSpecterPlot, TwoImmedSpectraPlot, TwoDynSpectraPlot
from f_spectra_normalization import Normalization_dB



#*************************************************************
#                       MAIN PROGRAM                         *
#*************************************************************


for i in range(8): print (' ')
print ('   ****************************************************')
print ('   *      ADR data files reader  v.',Software_version,'       *      (c) YeS 2018')
print ('   ****************************************************')
for i in range(3): print (' ')


startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)
print (' ')


# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = "ADR_Results/Service"
if not os.path.exists(newpath):
    os.makedirs(newpath)
if DynSpecSaveInitial == 1:
    if not os.path.exists('ADR_Results/Initial_spectra'):
        os.makedirs('ADR_Results/Initial_spectra')
if (DynSpecSaveCleaned == 1 and CorrelationProcess == 1):
    if not os.path.exists('ADR_Results/Correlation_spectra'):
        os.makedirs('ADR_Results/Correlation_spectra')


# *** Creating a TXT logfile ***
Log_File = open("ADR_Results/Service/Log.txt", "w")


Log_File.write('\n\n    ****************************************************\n' )
Log_File.write('    *     ADR data files reader  v.%s LOG      *      (c) YeS 2018\n' %Software_version )
Log_File.write('    ****************************************************\n\n' )

Log_File.write('  Date of data processing: %s   \n' %currentDate )
Log_File.write('  Time of data processing: %s \n\n' %currentTime )


# *** Search ADR files in the directory ***
fileList=[]
i = 0
print ('  Directory: ', directory, '\n')
Log_File.write('  Directory: %s \n' %directory )
print ('  List of files to be analyzed: ')
Log_File.write('  List of files to be analyzed: \n')
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.adr'):
            i = i + 1
            print ('         ', i, ') ', file)
            Log_File.write('           '+str(i)+') %s \n' %file )
            fileList.append(str(os.path.join(root, file)))
Log_File.close()

for fileNo in range (len(fileList)):   # loop by files
    for i in range(3): print (' ')
    print ('  *  File ',  str(fileNo+1), ' of', str(len(fileList)))
    print ('  *  File path: ', str(fileList[fileNo]))
    Log_File = open("ADR_Results/Service/Log.txt", "a")
    Log_File.write('\n\n\n  * File '+str(fileNo+1)+' of %s \n' %str(len(fileList)))
    Log_File.write('  * File path: %s \n\n\n' %str(fileList[fileNo]) )


#*********************************************************************************

    # *** Opening datafile ***
    fname = ''
    if len(fname) < 1 : fname = fileList[fileNo]

    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
            F_ADC, df_creation_timeUTC, ReceiverMode, ADRmode,
            sumDifMode, NAvr, TimeRes, fmin, fmax, df, frequency,
            FFT_Size, SLine, Width, BlockSize] = FileHeaderReaderADR(fname, 0)

    [SpInFile, SpInFrame, FrameInChunk, ChunksInFile, sizeOfChunk,
            frm_sec, frm_phase] = ChunkHeaderReaderADR(fname, 0, BlockSize)

    FreqPointsNum = int(Width * 1024)
    Log_File.close()


    # *** Setting the time reference (file beginning) ***
    TimeFirstFramePhase = float(frm_phase)/F_ADC
    TimeFirstFrameFloatSec = frm_sec + TimeFirstFramePhase
    TimeScaleStartTime = datetime(int('20' + df_filename[1:3]), int(df_filename[3:5]), int(df_filename[5:7]), int(df_creation_timeUTC[0:2]), int(df_creation_timeUTC[3:5]), int(df_creation_timeUTC[6:8]), int(df_creation_timeUTC[9:12])*1000)


    with open(fname, 'rb') as file:


        # *** Reading indexes of data from index file '*.fft' ***
        indexes = []
        ifname = str(int(FFT_Size/2)) + '.fft'
        indexfile = open(ifname, 'r')
        num = 0
        for line in indexfile:
            ind = int(line)
            if (ind >= SLine*1024) & (ind < ((SLine+Width)*1024)):
                indexes.append(ind - SLine*1024)
            num = num + 1
        indexfile.close()


        timeLineSecond = np.zeros(ChunksInFile) # List of second values from DSP_INF field


        # *** If it is the first file - write the header to long data file ***
        if((longFileSaveAch == 1 or longFileSaveBch == 1 or longFileSaveCRI == 1 or longFileSaveCMP == 1 or longFileSaveSSD == 1) and fileNo == 0):
            file.seek(0)
            file_header = file.read(1024)

            # *** Creating a name for long timeline TXT file ***
            TLfile_name = df_filename + '_Timeline.txt'
            TLfile = open(TLfile_name, 'w')  # Open and close to delete the file with the same name
            TLfile.close()

            # *** Creating a binary file with data for long data storage ***
            if(longFileSaveAch == 1 and (ADRmode == 3 or ADRmode == 5 or ADRmode == 6)):
                fileData_A_name = df_filename+'_Data_chA.dat'
                fileData_A = open(fileData_A_name, 'wb')
                fileData_A.write(file_header)
                fileData_A.close()
            if(longFileSaveBch == 1 and (ADRmode == 4 or ADRmode == 5 or ADRmode == 6)):
                fileData_B_name = df_filename+'_Data_chB.dat'
                fileData_B = open(fileData_B_name, 'wb')
                fileData_B.write(file_header)
                fileData_B.close()
            if(CorrelationProcess == 1 and longFileSaveCRI == 1 and ADRmode == 6):
                fileData_CRe_name = df_filename+'_Data_CRe.dat'
                fileData_C_Re = open(fileData_CRe_name, 'wb')
                fileData_C_Re.write(file_header)
                fileData_C_Re.close()
                fileData_CIm_name = df_filename+'_Data_CIm.dat'
                fileData_C_Im = open(fileData_CIm_name, 'wb')
                fileData_C_Im.write(file_header)
                fileData_C_Im.close()
            if(CorrelationProcess == 1 and longFileSaveCMP == 1 and ADRmode == 6):
                fileData_CM_name = df_filename+'_Data_C_m.dat'
                fileData_C_M = open(fileData_CM_name, 'wb')
                fileData_C_M.write(file_header)
                fileData_C_M.close()
                fileData_CP_name = df_filename+'_Data_C_p.dat'
                fileData_C_P = open(fileData_CP_name, 'wb')
                fileData_C_P.write(file_header)
                fileData_C_P.close()
            if(Sum_Diff_Calculate == 1 and longFileSaveSSD == 1 and (ADRmode == 5 or ADRmode == 6)):
                fileData_Sum_name = df_filename+'_Data_Sum.dat'
                fileData_Sum = open(fileData_Sum_name, 'wb')
                fileData_Sum.write(file_header)
                fileData_Sum.close()
                fileData_Dif_name = df_filename+'_Data_Dif.dat'
                fileData_Dif = open(fileData_Dif_name, 'wb')
                fileData_Dif.write(file_header)
                fileData_Dif.close()

            del file_header


        print (' ')
        print ('  *** Reading data from file ***')
        print (' ')



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

                TimeScale = []
                TimeFigureScale = [] # Timelime (new) for each figure
                TimeFigureStartTime = datetime(2016, 1, 1, 0, 0, 0, 0)



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


                # *** TimeLine calculations ***
                for i in range (Nim):

                # *** DSP_INF ***
                    frm_count = headers[3][i]
                    frm_sec = headers[4][i]
                    frm_phase = headers[5][i]

                    # * Abosolute time calculation *
                    timeLineSecond[figID*MaxNim+i] = frm_sec # to check the linearity of seconds
                    TimeCurrentFramePhase = float(frm_phase)/F_ADC
                    TimeCurrentFrameFloatSec = frm_sec + TimeCurrentFramePhase
                    TimeSecondDiff = TimeCurrentFrameFloatSec - TimeFirstFrameFloatSec
                    TimeAdd = timedelta(0, int(np.fix(TimeSecondDiff)), int(np.fix((TimeSecondDiff - int(np.fix(TimeSecondDiff)))*1000000)))

                    # Adding of time point to time line is in loop by spectra because
                    # for each spectra in frame there is one time point but it should
                    # appear for all spectra to fit the dimensions of arrays

                    # * Time from figure start calculation *
                    if (i == 0): TimeFigureStart = TimeCurrentFrameFloatSec
                    TimeFigureSecondDiff = TimeCurrentFrameFloatSec - TimeFigureStart
                    TimeFigureAdd = timedelta(0, int(np.fix(TimeFigureSecondDiff)), int(np.fix((TimeFigureSecondDiff - int(np.fix(TimeFigureSecondDiff)))*1000000)))

                    for iframe in range (0, SpInFrame):
                        TimeScale.append(str((TimeScaleStartTime + TimeAdd)))  #.time()
                        TimeFigureScale.append(str((TimeFigureStartTime+TimeFigureAdd).time()))


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


                # *** Calculating Sum and Difference of A and B channels ***
                if((ADRmode == 5 or ADRmode == 6) and Sum_Diff_Calculate == 1):
                    Data_Sum = Data_Ch_A + Data_Ch_B
                    Data_Dif = abs(Data_Ch_A - Data_Ch_B)



                # *** Saving data to a long-term file ***
                if (ADRmode == 3 or ADRmode == 5 or ADRmode == 6) and longFileSaveAch == 1:
                    fileData_A = open(fileData_A_name, 'ab')
                    fileData_A.write(Data_Ch_A)
                    fileData_A.close()
                if (ADRmode == 4 or ADRmode == 5 or ADRmode == 6) and longFileSaveBch == 1:
                    fileData_B = open(fileData_B_name, 'ab')
                    fileData_B.write(Data_Ch_B)
                    fileData_B.close()
                if  ADRmode == 6 and longFileSaveCRI == 1 and CorrelationProcess == 1:
                    fileData_C_Re = open(fileData_CRe_name, 'ab')
                    fileData_C_Re.write(Data_C_Re)
                    fileData_C_Re.close()
                    fileData_C_Im = open(fileData_CIm_name, 'ab')
                    fileData_C_Im.write(Data_C_Im)
                    fileData_C_Im.close()
                if((ADRmode == 5 or ADRmode == 6) and Sum_Diff_Calculate == 1 and longFileSaveSSD == 1):
                    fileData_Sum = open(fileData_Sum_name, 'ab')
                    fileData_Sum.write(Data_Sum)
                    fileData_Sum.close()
                    fileData_Dif = open(fileData_Dif_name, 'ab')
                    fileData_Dif.write(Data_Dif)
                    fileData_Dif.close()
                    del Data_Sum, Data_Dif


                if(longFileSaveAch == 1 or longFileSaveBch == 1 or longFileSaveCRI == 1 or longFileSaveCMP == 1 or longFileSaveSSD == 1):
                    with open(TLfile_name, 'a') as TLfile:
                        for i in range(SpInFrame * FrameInChunk * Nim):
                            TLfile.write((TimeScale[i][:])+' \n')   # str



                '''
                # *** Plotting Im and Re parts of correlation (before logarythm) ***
                if (ADRmode == 6) and figID == 0:   #  Immediate correlation spectrum channels A & B
                    TwoImmedSpectraPlot(frequency, Data_C_Re[1][:], Data_C_Im[1][:], 'Channel A', 'Channel B',
                                        frequency[0], frequency[wb-1], -0.001, 0.001,
                                        'Frequency, MHz', 'Amplitude, dB',
                                        'Immediate spectrum '+str(df_filename[0:18])+ ' channels A & B',
                                        'Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+str(round(df/1000.,3))+' kHz',
                                        'ADR_Results/Service/'+df_filename[0:14]+' Correlation Spectrum Re and Im before log.png')
                '''



                # *** Converting to logarythmic scale matrices ***
                if ADRmode == 3 or ADRmode == 5 or ADRmode == 6:
                    with np.errstate(divide='ignore'):
                        Data_Ch_A = 10*np.log10(Data_Ch_A)

                if ADRmode == 4 or ADRmode == 5 or ADRmode == 6:
                    with np.errstate(divide='ignore'):
                        Data_Ch_B = 10*np.log10(Data_Ch_B)

                if (ADRmode == 6 and CorrelationProcess == 1):
                    with np.errstate(divide='ignore'):
                        CorrModule = ((Data_C_Re)**2 + (Data_C_Im)**2)**(0.5)
                        CorrModule = 10*np.log10(CorrModule)
                        CorrPhase = np.arctan2(Data_C_Im, Data_C_Re)
                    CorrModule[np.isnan(CorrModule)] = 0
                    CorrPhase[np.isnan(CorrPhase)] = 0


                # *** Writing correlation data to long files ***
                if (ADRmode == 6 and longFileSaveCMP == 1 and CorrelationProcess == 1):
                    fileData_C_M = open(fileData_CM_name, 'ab')
                    fileData_C_M.write(np.float64(CorrModule))
                    fileData_C_M.close()
                    fileData_C_P = open(fileData_CP_name, 'ab')
                    fileData_C_P.write(np.float64(CorrPhase))
                    fileData_C_P.close()



                # *** Saving immediate spectrum to file ***
                if(SpecterFileSaveSwitch == 1 and figID == 0):
                    SpFile = open('ADR_Results/Service/Specter_'+df_filename[0:14]+'.txt', 'w')
                    for i in range(FreqPointsNum-1):
                        if ADRmode == 3:
                            SpFile.write(str('{:10.6f}'.format(frequency[i]))+'  '+str('{:16.10f}'.format(Data_Ch_A[ImmediateSpNo][i]))+' \n')
                        if ADRmode == 4:
                            SpFile.write(str('{:10.6f}'.format(frequency[i]))+'  '+str('{:16.10f}'.format(Data_Ch_B[ImmediateSpNo][i]))+' \n')
                        if ADRmode == 5 or ADRmode == 6:
                            SpFile.write(str('{:10.6f}'.format(frequency[i]))+'  '+str('{:16.10f}'.format(Data_Ch_A[ImmediateSpNo][i]))+'  '+str('{:16.10f}'.format(Data_Ch_B[ImmediateSpNo][i]))+' \n')
                        #if ADRmode == 6:
                        #    SpFile.write(str(frequency[i])+'  '+str(Data_Ch_A[ImmediateSpNo][i])+'  '+str(Data_Ch_B[ImmediateSpNo][i])+'  '+str(Data_C_Re[ImmediateSpNo][i])+'  '+str(Data_C_Im[ImmediateSpNo][i])+' \n')
                    SpFile.close()



                # *** Plotting immediate spectra before cleaning and normalizing ***
                if ADRmode == 3 and figID == 0:   # Immediate spectrum channel A
                    OneImmedSpecterPlot(frequency, Data_Ch_A[0][:], 'Channel A',
                                        frequency[0], frequency[FreqPointsNum-1], -120.0, -40.0,
                                        'Frequency, MHz', 'Amplitude, dB',
                                        'Immediate spectrum '+str(df_filename[0:18])+ ' channel A',
                                        'Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz'+sumDifMode + '\nDescription: '+str(df_description),
                                        'ADR_Results/Service/'+df_filename[0:14]+' Channel A Immediate Spectrum before cleaning and normalizing.png')

                if ADRmode == 4 and figID == 0:   # Immediate spectrum channel B
                    OneImmedSpecterPlot(frequency, Data_Ch_B[0][:], 'Channel B',
                                        frequency[0], frequency[FreqPointsNum-1], -120.0, -40.0,
                                        'Frequency, MHz', 'Amplitude, dB',
                                        'Immediate spectrum '+str(df_filename[0:18])+ ' channel B',
                                        'Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz'+sumDifMode + '\nDescription: '+str(df_description),
                                        'ADR_Results/Service/'+df_filename[0:14]+' Channel B Immediate Spectrum before cleaning and normalizing.png')

                if (ADRmode == 5 or ADRmode == 6) and figID == 0: # Immediate spectrum channels A & B
                    TwoImmedSpectraPlot(frequency, Data_Ch_A[0][:], Data_Ch_B[0][:], 'Channel A', 'Channel B',
                                        frequency[0], frequency[FreqPointsNum-1], -120, -20.0,
                                        'Frequency, MHz', 'Amplitude, dB',
                                        'Immediate spectrum '+str(df_filename[0:18])+ ' channels A & B',
                                        'Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz'+sumDifMode + '\nDescription: '+str(df_description),
                                        'ADR_Results/Service/' + df_filename[0:14] + ' Channels A and B Immediate Spectrum before cleaning and normalizing.png',
                                        currentDate, currentTime, Software_version)

                if (ADRmode == 6 and figID == 0 and CorrelationProcess == 1):   #  Immediate correlation spectrum channels A & B
                    OneImmedSpecterPlot(frequency, CorrModule[0][:], 'Correlation module',
                                        frequency[0], frequency[FreqPointsNum-1], -150.0, -20.0,
                                        'Frequency, MHz', 'Amplitude, dB',
                                        'Immediate spectrum '+str(df_filename[0:18])+ ' channels A & B',
                                        'Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz'+sumDifMode + '\nDescription: '+str(df_description),
                                        'ADR_Results/Service/'+df_filename[0:14]+' Correlation module spectrum.png')

                if ADRmode == 6 and CorrelationProcess == 1:
                    OneImmedSpecterPlot(frequency, CorrPhase[0][:], 'Correlation phase',
                                        frequency[0], frequency[FreqPointsNum-1], -4, 4,
                                        'Frequency, MHz', 'Phase, rad',
                                        'Immediate correlation phase spectrum '+str(df_filename[0:18])+ ' channels A & B',
                                        'Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz'+sumDifMode + '\nDescription: '+str(df_description),
                                        'ADR_Results/Service/' + df_filename[0:14] + ' Correlation phase spectrum.png')



                # Initial dynamic specter channel A
                if (ADRmode == 3 and DynSpecSaveInitial == 1):
                    plt.figure(4, figsize=(16.0, 6.0))
                    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
                    ImA = plt.imshow(np.flipud(Data_Ch_A.transpose()), aspect='auto', vmin=-120, vmax=-30, extent=[0,SpectrNum,frequency[0],frequency[FreqPointsNum-1]], cmap=colormap)
                    plt.ylabel('Frequency, MHz', fontsize=10, fontweight='bold')
                    plt.title('Channel A', fontsize=10, fontweight='bold', style='italic', y = 1.025)
                    plt.suptitle('Dynamic spectrum (initial) '+str(df_filename[0:18])+
                                ' - Fig. '+str(figID+1)+ ' of '+str(figMAX)+
                                '\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+
                                ' ms, df = '+str(round(df/1000.,3))+' kHz, '+sumDifMode+
                                ' Receiver: '+str(df_system_name)+
                                ', Place: '+str(df_obs_place) +
                                '\n Description: '+str(df_description),
                                fontsize=10, fontweight='bold', x = 0.46, y = 1.01)
                    plt.yticks(fontsize=8, fontweight='bold')
                    if (ColorBarSwitch == 1):
                        rc('font', weight='bold')
                        cbar = plt.colorbar(ImA, pad=0.005)
                        cbar.set_label('Intensity, dB', fontsize=9, fontweight='bold')
                        cbar.ax.tick_params(labelsize=8)
                    ax1 = plt.figure(4).add_subplot(1,1,1)
                    a = ax1.get_xticks().tolist()
                    for i in range(len(a)-1):
                        k = int(a[i])
                        a[i] = TimeScale[k][11:23]
                    ax1.set_xticklabels(a)
                    plt.xticks(fontsize=8, fontweight='bold')
                    plt.xlabel('UTC Time, HH:MM:SS.msec', fontsize=10, fontweight='bold')
                    ax2 = ax1.twiny()
                    ax2.set_xlim(0, Nim*SpInFrame*FrameInChunk)
                    b = ax2.get_xticks().tolist()
                    for i in range(len(b)-1):
                        k = int(b[i])
                        b[i] = TimeFigureScale[k][0:12]
                    ax2.set_xticklabels(b)
                    plt.xticks(fontsize=8, fontweight='bold')
                    pylab.savefig('ADR_Results/Initial_spectra/' + df_filename[0:14] + ' Initial dynamic spectrum fig.' + str(figID+1) + '.png', bbox_inches='tight', dpi = customDPI)
                    plt.close('all')



                # Initial dynamic specter channel B
                if (ADRmode == 4 and DynSpecSaveInitial == 1):
                    plt.figure(4, figsize=(16.0, 6.0))
                    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
                    ImA = plt.imshow(np.flipud(Data_Ch_B.transpose()), aspect='auto', vmin=-120, vmax=-30, extent=[0,SpectrNum,frequency[0],frequency[FreqPointsNum-1]], cmap=colormap)
                    plt.ylabel('Frequency, MHz', fontsize=10, fontweight='bold')
                    plt.title('Channel B', fontsize=10, fontweight='bold', style='italic', y=1.025)
                    plt.suptitle('Dynamic spectrum (initial) '+str(df_filename[0:18])+
                                ' - Fig. '+str(figID+1)+ ' of '+str(figMAX)+
                                '\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+
                                ' ms, df = '+str(round(df/1000.,3))+' kHz, '+sumDifMode+
                                ' Receiver: '+str(df_system_name)+
                                ', Place: '+str(df_obs_place) +
                                '\n Description: '+str(df_description),
                                fontsize=10, fontweight='bold', x = 0.46, y = 1.01)
                    plt.yticks(fontsize=8, fontweight='bold')
                    if (ColorBarSwitch == 1):
                        rc('font', weight='bold')
                        cbar = plt.colorbar(ImA, pad=0.005)
                        cbar.set_label('Intensity, dB', fontsize=9, fontweight='bold')
                        cbar.ax.tick_params(labelsize=8)
                    ax1 = plt.figure(4).add_subplot(1,1,1)
                    a = ax1.get_xticks().tolist()
                    for i in range(len(a)-1):
                        k = int(a[i])
                        a[i] = TimeScale[k][11:23]
                    ax1.set_xticklabels(a)
                    plt.xticks(fontsize=8, fontweight='bold')
                    plt.xlabel('UTC Time, HH:MM:SS.msec', fontsize=10, fontweight='bold')
                    ax2 = ax1.twiny()
                    ax2.set_xlim(0, Nim*SpInFrame*FrameInChunk)
                    b = ax2.get_xticks().tolist()
                    for i in range(len(b)-1):
                        k = int(b[i])
                        b[i] = TimeFigureScale[k][0:12]
                    ax2.set_xticklabels(b)
                    plt.xticks(fontsize=8, fontweight='bold')
                    pylab.savefig('ADR_Results/Initial_spectra/' + df_filename[0:14] + ' Initial dynamic spectrum fig.' + str(figID+1) + '.png', bbox_inches='tight', dpi = customDPI)
                    plt.close('all')


                # *** FIGURE Initial dynamic spectrum channels A and B (python 3 new version) ***
                if ((ADRmode == 5 or ADRmode == 6) and DynSpecSaveInitial == 1):
                    TwoDynSpectraPlot(Data_Ch_A, Data_Ch_B, Vmin, Vmax, Vmin, Vmax,
                        'Dynamic spectrum (initial) ',
                        figID, figMAX, TimeRes, df, sumDifMode, df_system_name, df_obs_place,
                        df_filename, df_description, 'Intensity, dB', 'Intensity, dB', Nim,
                        SpInFrame, FrameInChunk, ReceiverMode, TimeFigureScale, TimeScale,
                        SpectrNum, frequency, FreqPointsNum, colormap,
                        'Channel A', 'Channel B',
                        'ADR_Results/Initial_spectra/',
                        ' Initial dynamic spectrum fig.',
                        currentDate, currentTime, Software_version, customDPI)


                # *** FIGURE Initial correlation spectrum module and phase (python 3 new version) ***
                if (ADRmode == 6 and CorrSpecSaveInitial == 1 and CorrelationProcess == 1):
                    TwoDynSpectraPlot(CorrModule, CorrPhase, VminCorrMag, VmaxCorrMag, -3.15, 3.15,
                        'Dynamic spectrum (correlation) ',
                        figID, figMAX, TimeRes, df, sumDifMode, df_system_name, df_obs_place,
                        df_filename, df_description, 'Intensity, dB', 'Phase, rad', Nim,
                        SpInFrame, FrameInChunk, ReceiverMode, TimeFigureScale, TimeScale,
                        SpectrNum, frequency, FreqPointsNum, colormap,
                        'Correlation module', 'Correlation phase',
                        'ADR_Results/Correlation_spectra/',
                        ' Correlation dynamic Spectrum fig.',
                        currentDate, currentTime, Software_version, customDPI)


                # *** Normalizing amplitude-frequency responce ***
                if (ADRmode == 3 or ADRmode == 5 or ADRmode == 6) and DynSpecSaveCleaned == 1:
                    Normalization_dB(Data_Ch_A, FreqPointsNum, Nim * SpInFrame * FrameInChunk)
                if (ADRmode == 4 or ADRmode == 5 or ADRmode == 6) and DynSpecSaveCleaned == 1:
                    Normalization_dB(Data_Ch_B, FreqPointsNum, Nim * SpInFrame * FrameInChunk)
                if ADRmode == 6 and CorrelationProcess == 1 and CorrSpecSaveCleaned == 1:
                    Normalization_dB(CorrModule, FreqPointsNum, Nim * SpInFrame * FrameInChunk)



                # *** Deleting cahnnels with strong RFI ***
                if (ADRmode == 3 or ADRmode == 5 or ADRmode == 6) and DynSpecSaveCleaned == 1:
                    simple_channel_clean(Data_Ch_A, RFImeanConst)
                if (ADRmode == 4 or ADRmode == 5 or ADRmode == 6) and DynSpecSaveCleaned == 1:
                    simple_channel_clean(Data_Ch_B, RFImeanConst)
                if ADRmode == 6 and CorrelationProcess == 1 and CorrSpecSaveCleaned == 1:
                    simple_channel_clean(CorrModule, 2 * RFImeanConst)


                #   *** Immediate spectra of normalyzed data ***    (only for first figure in data file)

                if ADRmode == 3 and figID == 0 and DynSpecSaveCleaned == 1:   # Immediate spectrum channel A
                    OneImmedSpecterPlot(frequency, Data_Ch_A[0][:], 'Channel A',
                                        frequency[0], frequency[FreqPointsNum-1], -10.0, 40.0,
                                        'Frequency, MHz', 'Amplitude, dB',
                                        'Immediate spectrum '+str(df_filename[0:18])+ ' channel A',
                                        'Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz'+sumDifMode + '\nDescription: '+str(df_description),
                                        'ADR_Results/Service/'+df_filename[0:14]+' Channel A Immediate Spectrum after cleaning and normalizing.png')

                if ADRmode == 4 and figID == 0 and DynSpecSaveCleaned == 1:   # Immediate spectrum channel B
                    OneImmedSpecterPlot(frequency, Data_Ch_B[0][:], 'Channel B',
                                        frequency[0], frequency[FreqPointsNum-1], -10.0, 40.0,
                                        'Frequency, MHz', 'Amplitude, dB',
                                        'Immediate spectrum '+str(df_filename[0:18])+ ' channel B',
                                        'Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz'+sumDifMode + '\nDescription: '+str(df_description),
                                        'ADR_Results/Service/'+df_filename[0:14]+' Channel B Immediate Spectrum after cleaning and normalizing.png')

                if (ADRmode == 5 or ADRmode == 6) and figID == 0 and DynSpecSaveCleaned == 1:   # Immediate spectrum channels A & B
                    TwoImmedSpectraPlot(frequency, Data_Ch_A[0][:], Data_Ch_B[0][:], 'Channel A', 'Channel B',
                                        frequency[0], frequency[FreqPointsNum-1], -10.0, 40.0,
                                        'Frequency, MHz', 'Amplitude, dB',
                                        'Immediate spectrum '+str(df_filename[0:18])+ ' channels A & B',
                                        'Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz'+sumDifMode + '\nDescription: '+str(df_description),
                                        'ADR_Results/Service/'+df_filename[0:14]+' Channels A and B Immediate Spectrum after cleaning and normalizing.png',
                                        currentDate, currentTime, Software_version)



                # Dynamic specter channel A
                if (ADRmode == 3 and DynSpecSaveCleaned == 1):
                    plt.figure(4, figsize=(16.0, 6.0))
                    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
                    ImA = plt.imshow(np.flipud(Data_Ch_A.transpose()), aspect='auto', vmin=Vmin, vmax=Vmax, extent=[0,SpectrNum,frequency[0],frequency[FreqPointsNum-1]], cmap=colormap)
                    plt.ylabel('Frequency, MHz', fontsize=10, fontweight='bold')
                    plt.title('Channel A', fontsize=10, fontweight='bold', style='italic', y=1.025)
                    plt.suptitle('Dynamic spectrum (normalized) '+str(df_filename[0:18])+
                                ' - Fig. '+str(figID+1)+ ' of '+str(figMAX)+
                                '\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+
                                ' ms, df = '+str(round(df/1000.,3))+' kHz, '+sumDifMode+
                                ' Receiver: '+str(df_system_name)+
                                ', Place: '+str(df_obs_place) +
                                '\n Description: '+str(df_description),
                                fontsize=10, fontweight='bold', x = 0.46, y = 1.01)
                    plt.yticks(fontsize=8, fontweight='bold')
                    if (ColorBarSwitch == 1):
                        rc('font', weight='bold')
                        cbar = plt.colorbar(ImA, pad = 0.005)
                        cbar.set_label('Intensity, dB', fontsize=9, fontweight='bold')
                        cbar.ax.tick_params(labelsize=8)
                    ax1 = plt.figure(4).add_subplot(1,1,1)
                    a = ax1.get_xticks().tolist()
                    for i in range(len(a)-1):
                        k = int(a[i])
                        a[i] = TimeScale[k][11:23]
                    ax1.set_xticklabels(a)
                    plt.xticks(fontsize=8, fontweight='bold')
                    plt.xlabel('UTC Time, HH:MM:SS.msec', fontsize=10, fontweight='bold')
                    ax2 = ax1.twiny()
                    ax2.set_xlim(0, Nim*SpInFrame*FrameInChunk)
                    b = ax2.get_xticks().tolist()
                    for i in range(len(b)-1):
                        k = int(b[i])
                        b[i] = TimeFigureScale[k][0:12]
                    ax2.set_xticklabels(b)
                    plt.xticks(fontsize=8, fontweight='bold')
                    pylab.savefig('ADR_Results/' + df_filename[0:14] + ' Dynamic spectrum fig.' + str(figID+1) + '.png', bbox_inches='tight', dpi = customDPI)
                    plt.close('all')



                # Dynamic specter channel B
                if (ADRmode == 4 and DynSpecSaveCleaned == 1):
                    plt.figure(4, figsize=(16.0, 6.0))
                    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
                    ImA = plt.imshow(np.flipud(Data_Ch_B.transpose()), aspect='auto', vmin=Vmin, vmax=Vmax, extent=[0,SpectrNum,frequency[0],frequency[FreqPointsNum-1]], cmap=colormap)
                    plt.ylabel('Frequency, MHz', fontsize=10, fontweight='bold')
                    plt.title('Channel B', fontsize=10, fontweight='bold', style='italic', y=1.025)
                    plt.suptitle('Dynamic spectrum (normalized) '+str(df_filename[0:18])+
                                ' - Fig. '+str(figID+1)+ ' of '+str(figMAX)+
                                '\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+
                                ' ms, df = '+str(round(df/1000.,3))+' kHz, '+sumDifMode+
                                ' Receiver: '+str(df_system_name)+
                                ', Place: '+str(df_obs_place) +
                                '\n Description: '+str(df_description),
                                fontsize=10, fontweight='bold', x = 0.46, y = 1.01)
                    plt.yticks(fontsize=8, fontweight='bold')
                    if (ColorBarSwitch == 1):
                        rc('font', weight='bold')
                        cbar = plt.colorbar(ImA, pad=0.005)
                        cbar.set_label('Intensity, dB', fontsize=9, fontweight='bold')
                        cbar.ax.tick_params(labelsize=8)
                    ax1 = plt.figure(4).add_subplot(1,1,1)
                    a = ax1.get_xticks().tolist()
                    for i in range(len(a)-1):
                        k = int(a[i])
                        a[i] = TimeScale[k][11:23]
                    ax1.set_xticklabels(a)
                    plt.xticks(fontsize=8, fontweight='bold')
                    plt.xlabel('UTC Time, HH:MM:SS.msec', fontsize=10, fontweight='bold')
                    ax2 = ax1.twiny()
                    ax2.set_xlim(0, Nim*SpInFrame*FrameInChunk)
                    b = ax2.get_xticks().tolist()
                    for i in range(len(b)-1):
                        k = int(b[i])
                        b[i] = TimeFigureScale[k][0:12]
                    ax2.set_xticklabels(b)
                    plt.xticks(fontsize=8, fontweight='bold')
                    pylab.savefig('ADR_Results/' + df_filename[0:14] + ' Dynamic spectrum fig.' + str(figID+1) + '.png', bbox_inches='tight', dpi = customDPI)
                    plt.close('all')



                # *** FIGURE Dynamic spectrum channels A and B cleaned and normalized (python 3 new version) ***
                if ((ADRmode == 5 or ADRmode == 6) and DynSpecSaveCleaned == 1):
                    TwoDynSpectraPlot(Data_Ch_A, Data_Ch_B, VminNorm, VmaxNorm, VminNorm, VmaxNorm,
                        'Dynamic spectrum (normalized) ',
                        figID, figMAX, TimeRes, df, sumDifMode, df_system_name, df_obs_place,
                        df_filename, df_description, 'Intensity, dB', 'Intensity, dB', Nim,
                        SpInFrame, FrameInChunk, ReceiverMode, TimeFigureScale, TimeScale,
                        SpectrNum, frequency, FreqPointsNum, colormap,
                        'Channel A', 'Channel B',
                        'ADR_Results/',
                        ' Dynamic spectrum fig.',
                        currentDate, currentTime, Software_version, customDPI)



                # *** FIGURE Correlation spectrum module and phase cleaned and normalized (python 3 new version) ***
                if (ADRmode == 6 and CorrSpecSaveCleaned == 1 and CorrelationProcess == 1):
                    TwoDynSpectraPlot(CorrModule, CorrPhase, VminNorm, 3*VmaxNorm, -3.15, 3.15,
                        'Dynamic spectrum (correlation) ',
                        figID, figMAX, TimeRes, df, sumDifMode, df_system_name, df_obs_place,
                        df_filename, df_description, 'Intensity, dB', 'Phase, rad', Nim,
                        SpInFrame, FrameInChunk, ReceiverMode, TimeFigureScale, TimeScale,
                        SpectrNum, frequency, FreqPointsNum, colormap,
                        'Correlation module', 'Correlation phase',
                        'ADR_Results/Correlation_spectra/',
                        ' Correlation dynamic spectrum cleaned fig.',
                        currentDate, currentTime, Software_version, customDPI)




            # Check of second counter data for linearity
            #OneImmedSpecterPlot(list(range(ChunksInFile)), timeLineSecond, 'timeLineSecond',
            #                    0, ChunksInFile, 0, 2000,
            #                    'Time, sec', 'Second counter, sec',
            #                    'Second counter',
            #                    ' ',
            #                    'ADR_Results/Service/' + df_filename[0:14] + ' Second counter fig.' + str(figID+1) + '.png')

            gc.collect()
        del timeLineSecond
        print ('\n  Position in file: ', file.tell(), ' File size: ', df_filesize)
        if (file.tell() == df_filesize): print ('\n  File was read till the end')
        if (file.tell() < df_filesize):  print ('\n  File was NOT read till the end!!! ERROR')

    # Here we close the data file



endTime = time.time()    # Time of calculations


print (' ')
print ('  The program execution lasted for ', round((endTime - startTime),2), 'seconds')
for i in range (0,2) : print (' ')
print ('    *** Program ADR reader has finished! ***')
for i in range (0,3) : print (' ')
