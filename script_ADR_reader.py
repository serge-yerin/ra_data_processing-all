# Python3
Software_version = '2019.05.06'
# Script intended to read, show and analyze data from ADR, to save
# data to long DAT files for further processing

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Directory of files to be analyzed:
directory = 'DATA/'  #'DATA/'

MaxNim = 8192                 # Number of data chunks for one figure
chunkSkip = 0                 # Number of chunks to skip from data beginning
RFImeanConst = 8              # Constant of RFI mitigation (usually 8)
Vmin = -120                   # Lower limit of figure dynamic range for initial spectra
Vmax = -50                    # Upper limit of figure dynamic range for initial spectra
VminNorm = 0                  # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 10                 # Upper limit of figure dynamic range for normalized spectra
VminCorrMag = -150            # Lower limit of figure dynamic range for correlation magnitude spectra
VmaxCorrMag = -30             # Upper limit of figure dynamic range for correlation magnitude spectra
customDPI = 200               # Resolution of images of dynamic spectra
colormap = 'jet'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
CorrelationProcess = 1        # Process correlation data or save time?  (1 = process, 0 = save)
Sum_Diff_Calculate = 0        # Calculate sum and diff of A & B channels?
longFileSaveAch = 0           # Save data A to long file? (1 = yes, 0 = no)
longFileSaveBch = 0           # Save data B to long file? (1 = yes, 0 = no)
longFileSaveCMP = 0           # Save correlation data (Module and Phase) to long file? (1 = yes, 0 = no)
longFileSaveCRI = 0           # Save correlation data (Real and Imaginary) to long file? (1 = yes, 0 = no)
longFileSaveSSD = 0           # Save sum / diff data to a long file?
DynSpecSaveInitial = 0        # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 1        # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 1       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
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
#import sys
import gc
import datetime
from datetime import datetime, timedelta
from matplotlib import rc
import warnings
warnings.filterwarnings("ignore")

from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR, ChunkHeaderReaderADR
from package_ra_data_files_formats.FPGA_to_PC_array import FPGAtoPCarrayADR
from package_cleaning.simple_channel_clean import simple_channel_clean
from package_plot_formats.plot_formats import TwoOrOneValuePlot, OneDynSpectraPlot, TwoDynSpectraPlot
from package_ra_data_processing.spectra_normalization import Normalization_dB

################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************

print ('\n\n\n\n\n\n\n\n   ****************************************************')
print ('   *      ADR data files reader  v.',Software_version,'       *      (c) YeS 2018')
print ('   **************************************************** \n\n\n')

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

    # Reading the file header
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
            F_ADC, df_creation_timeUTC, ReceiverMode, ADRmode,
            sumDifMode, NAvr, TimeRes, fmin, fmax, df, frequency,
            FFT_Size, SLine, Width, BlockSize] = FileHeaderReaderADR(fname, 0, 1)

    # Reading the chunk header
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

                # Exact string timescales to show on plots
                TimeFigureScaleFig = np.empty_like(TimeFigureScale)
                TimeScaleFig = np.empty_like(TimeScale)
                for i in range (len(TimeFigureScale)):
                    TimeFigureScaleFig[i] = TimeFigureScale[i][0:11]
                    TimeScaleFig[i] = TimeScale[i][11:23]

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



                # *** FIGURE Immediate spectra before cleaning and normalizing ***
                if figID == 0:
                    if ADRmode == 3:
                        Data_1 = Data_Ch_A[0][:]
                        Legend_1 = 'Channel A'
                    if ADRmode == 4:
                        Data_1 = Data_Ch_B[0][:]
                        Legend_1 = 'Channel B'
                    if ADRmode == 3 or ADRmode == 4:
                        no_of_sets = 1
                        Data_2 = []
                        Suptitle = ('Immediate spectrum '+str(df_filename[0:18])+ ' ' + Legend_1)
                        Title = ('Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+
                                ' kHz'+sumDifMode + ', Description: '+str(df_description))
                        Filename = ('ADR_Results/Service/'+df_filename[0:14]+' '+
                                    Legend_1 + ' Immediate Spectrum before cleaning and normalizing.png')

                    if (ADRmode == 5 or ADRmode == 6) :     # Immediate spectrum channels A & B
                        Data_1 = Data_Ch_A[0][:]
                        Data_2 = Data_Ch_B[0][:]
                        Legend_1 = 'Channel A'
                        no_of_sets = 2
                        Suptitle = ('Immediate spectrum '+str(df_filename[0:18])+ ' channels A & B')
                        Title = ('Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+
                                ' kHz,'+sumDifMode + ' Description: '+str(df_description))
                        Filename = ('ADR_Results/Service/' + df_filename[0:14] +
                                    ' Channels A and B Immediate Spectrum before cleaning and normalizing.png')

                    TwoOrOneValuePlot(no_of_sets, frequency,  Data_1, Data_2,
                                Legend_1, 'Channel B', frequency[0], frequency[FreqPointsNum-1],
                                -120, -20, -120, -20, 'Frequency, MHz', 'Intensity, dB', 'Intensity, dB',
                                Suptitle, Title, Filename,
                                currentDate, currentTime, Software_version)

                # *** FIGURE Correlation amplitude and phase immediate spectrum ***
                if (ADRmode == 6 and figID == 0 and CorrelationProcess == 1):   #  Immediate correlation spectrum channels A & B

                    Suptitle = ('Immediate correlation spectrum '+str(df_filename[0:18])+ ' channels A & B')
                    Title = ('Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+
                                ' kHz,'+sumDifMode + ' Description: '+str(df_description))
                    Filename = ('ADR_Results/Service/' + df_filename[0:14] +
                                ' Channels A and B Correlation module and phase spectrum.png')

                    TwoOrOneValuePlot(2, frequency,   CorrModule[0][:], CorrPhase[0][:],
                                'Correlation module', 'Correlation phase', frequency[0], frequency[FreqPointsNum-1],
                                -150, -20, -4, 4, 'Frequency, MHz', 'Intensity, dB', 'Phase, rad',
                                Suptitle, Title, Filename,
                                currentDate, currentTime, Software_version)


                # *** FIGURE Initial dynamic spectrum of 1 channel (A or B) ***
                if ((ADRmode == 3 or ADRmode == 4) and DynSpecSaveInitial == 1):
                    if ADRmode == 3:
                        Data = Data_Ch_A.transpose()
                    if ADRmode == 4:
                        Data = Data_Ch_B.transpose()

                    Suptitle = ('Dynamic spectrum (initial) '+str(df_filename[0:18])+
                                ' - Fig. '+str(figID+1)+ ' of '+str(figMAX)+
                                '\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+
                                ' ms, df = '+str(round(df/1000.,3))+' kHz, '+sumDifMode+
                                ' Receiver: '+str(df_system_name)+
                                ', Place: '+str(df_obs_place) +
                                '\n Description: '+str(df_description))

                    fig_file_name = ('ADR_Results/Initial_spectra/' + df_filename[0:14] +
                                        ' Initial dynamic spectrum fig.' + str(figID+1) + '.png')

                    OneDynSpectraPlot(Data, -120, -30, Suptitle,
                        'Intensity, dB', Nim * SpInFrame * FrameInChunk, TimeScaleFig,
                        frequency, FreqPointsNum, colormap, 'UTC Time, HH:MM:SS.msec',
                        fig_file_name, currentDate, currentTime, Software_version, customDPI)



                # *** FIGURE Initial dynamic spectrum channels A and B ***
                if ((ADRmode == 5 or ADRmode == 6) and DynSpecSaveInitial == 1):

                    fig_file_name = ('ADR_Results/Initial_spectra/' + df_filename[0:14] +
                                    ' Initial dynamic spectrum fig.' + str(figID+1) + '.png')
                    Suptitle = ('Dynamic spectrum (initial) ' + str(df_filename) + ' - Fig. ' +
                                str(figID+1) + ' of ' + str(figMAX) + '\n Initial parameters: dt = ' +
                                str(round(TimeRes*1000,3)) + ' ms, df = ' + str(round(df/1000.,3)) + ' kHz, ' +
                                sumDifMode + ' Receiver: ' + str(df_system_name)+', Place: '+str(df_obs_place) +
                                '\n' + ReceiverMode + ', Description: ' + str(df_description))


                    TwoDynSpectraPlot(Data_Ch_A.transpose(), Data_Ch_B.transpose(), Vmin, Vmax, Vmin, Vmax, Suptitle,
                                            'Intensity, dB', 'Intensity, dB', Nim * SpInFrame * FrameInChunk,
                                            TimeFigureScaleFig, TimeScaleFig, frequency,
                                            FreqPointsNum, colormap, 'Channel A', 'Channel B', fig_file_name,
                                            currentDate, currentTime, Software_version, customDPI)


                # *** FIGURE Initial correlation spectrum module and phase ***
                if (ADRmode == 6 and CorrSpecSaveInitial == 1 and CorrelationProcess == 1):

                    fig_file_name = ('ADR_Results/Correlation_spectra/' + df_filename[0:14] +
                                    ' Correlation dynamic spectrum fig.' + str(figID+1) + '.png')
                    Suptitle = ('Correlation dynamic spectrum (initial) ' + str(df_filename)+' - Fig. '+
                                str(figID+1)+' of '+str(figMAX)+'\n Initial parameters: dt = '+
                                str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz, '+
                                sumDifMode+' Receiver: '+str(df_system_name)+', Place: '+str(df_obs_place)+
                                '\n'+ReceiverMode+', Description: '+str(df_description))

                    TwoDynSpectraPlot(CorrModule.transpose(), CorrPhase.transpose(), VminCorrMag, VmaxCorrMag, -3.15, 3.15, Suptitle,
                                            'Intensity, dB', 'Phase, rad', Nim * SpInFrame * FrameInChunk,
                                            TimeFigureScaleFig, TimeScaleFig, frequency,
                                            FreqPointsNum, colormap, 'Correlation module', 'Correlation phase',
                                            fig_file_name, currentDate, currentTime, Software_version, customDPI)


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
                if figID == 0 and DynSpecSaveCleaned == 1:
                    if ADRmode == 3:
                        Data_1 = Data_Ch_A[0][:]
                        Legend_1 = 'Channel A'
                    if ADRmode == 4:
                        Data_1 = Data_Ch_B[0][:]
                        Legend_1 = 'Channel B'
                    if ADRmode == 3 or ADRmode == 4:
                        no_of_sets = 1
                        Data_2 = []
                        Suptitle = ('Normalized immediate spectrum '+str(df_filename[0:18])+ ' ' + Legend_1)
                        Title = ('Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+
                                ' kHz'+sumDifMode + ', Description: '+str(df_description))
                        Filename = ('ADR_Results/Service/'+df_filename[0:14]+' '+
                                Legend_1 + ' Immediate Spectrum after cleaning and normalizing.png')

                    if (ADRmode == 5 or ADRmode == 6):   # Immediate spectrum channels A & B
                        no_of_sets = 2
                        Data_1 = Data_Ch_A[0][:]
                        Data_2 = Data_Ch_B[0][:]
                        Legend_1 = 'Channel A'
                        Suptitle = ('Normalized immediate spectrum '+str(df_filename[0:18])+ ' channels A & B')
                        Title = ('Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+
                                ' kHz'+sumDifMode + ', Description: '+str(df_description))
                        Filename = ('ADR_Results/Service/'+df_filename[0:14]+
                                ' Channels A and B Immediate Spectrum after cleaning and normalizing.png')

                    TwoOrOneValuePlot(no_of_sets, frequency,  Data_1,  Data_2,
                                        Legend_1, 'Channel B', frequency[0], frequency[FreqPointsNum-1],
                                        -10, 40, -10, 40, 'Frequency, MHz', 'Intensity, dB', 'Intensity, dB',
                                        Suptitle, Title, Filename, currentDate, currentTime, Software_version)



                # *** FIGURE Cleaned and normalized dynamic spectrum of 1 channel A or B

                if ((ADRmode == 3 or ADRmode == 4) and DynSpecSaveCleaned == 1):
                    if ADRmode == 3:
                        Data = Data_Ch_A.transpose()
                    if ADRmode == 4:
                        Data = Data_Ch_B.transpose()

                    Suptitle = ('Dynamic spectrum (normalized) '+str(df_filename[0:18])+
                                ' - Fig. '+str(figID+1)+ ' of '+str(figMAX)+
                                '\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+
                                ' ms, df = '+str(round(df/1000.,3))+' kHz, '+sumDifMode+
                                ' Receiver: '+str(df_system_name)+
                                ', Place: '+str(df_obs_place) +
                                '\n Description: '+str(df_description))

                    fig_file_name = ('ADR_Results/' + df_filename[0:14] +
                                        ' Dynamic spectrum fig.' + str(figID+1) + '.png')

                    OneDynSpectraPlot(Data, VminNorm, VmaxNorm, Suptitle,
                        'Intensity, dB', Nim * SpInFrame * FrameInChunk, TimeScaleFig,
                        frequency, FreqPointsNum, colormap, 'UTC Time, HH:MM:SS.msec',
                        fig_file_name, currentDate, currentTime, Software_version, customDPI)


                # *** FIGURE Dynamic spectrum channels A and B cleaned and normalized (python 3 new version) ***

                if ((ADRmode == 5 or ADRmode == 6) and DynSpecSaveCleaned == 1):

                    fig_file_name = ('ADR_Results/' + df_filename[0:14] + ' Dynamic spectrum fig.' +
                                    str(figID+1) + '.png')
                    Suptitle = ('Dynamic spectrum (normalized) ' + str(df_filename)+' - Fig. '+str(figID+1)+
                                ' of '+str(figMAX)+'\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+
                                ' ms, df = '+str(round(df/1000.,3))+' kHz, '+sumDifMode+' Receiver: '+
                                str(df_system_name)+', Place: '+str(df_obs_place)+'\n'+ReceiverMode+', Description: '+
                                str(df_description))

                    TwoDynSpectraPlot(Data_Ch_A.transpose(), Data_Ch_B.transpose(), VminNorm, VmaxNorm, VminNorm, VmaxNorm, Suptitle,
                                            'Intensity, dB', 'Intensity, dB', Nim * SpInFrame * FrameInChunk,
                                            TimeFigureScaleFig, TimeScaleFig, frequency,
                                            FreqPointsNum, colormap, 'Channel A', 'Channel B', fig_file_name,
                                            currentDate, currentTime, Software_version, customDPI)


                # *** FIGURE Correlation spectrum module and phase cleaned and normalized (python 3 new version) ***
                if (ADRmode == 6 and CorrSpecSaveCleaned == 1 and CorrelationProcess == 1):

                    Suptitle = 'Correlation dynamic spectrum (nolmalized) ' + str(df_filename)+' - Fig. '+str(figID+1)+' of '+str(figMAX)+'\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz, '+sumDifMode+' Receiver: '+str(df_system_name)+', Place: '+str(df_obs_place)+'\n'+ReceiverMode+', Description: '+str(df_description)

                    fig_file_name = 'ADR_Results/Correlation_spectra/' + df_filename[0:14] + ' Correlation dynamic spectrum cleaned fig.' + str(figID+1) + '.png'

                    TwoDynSpectraPlot(CorrModule.transpose(), CorrPhase.transpose(), VminNorm, 3*VmaxNorm, -3.15, 3.15, Suptitle,
                                            'Intensity, dB', 'Phase, rad', Nim * SpInFrame * FrameInChunk,
                                            TimeFigureScaleFig, TimeScaleFig, frequency, FreqPointsNum, colormap,
                                            'Normalized and cleaned correlation module', 'Correlation phase',
                                            fig_file_name, currentDate, currentTime, Software_version, customDPI)

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
