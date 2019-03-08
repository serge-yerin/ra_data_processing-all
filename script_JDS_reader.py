# Python3
Software_version = '2019.03.08'
# Program intended to read, show and analyze data from DSPZ receivers

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************
# Directory of files to be analyzed:
directory = 'd:/PYTHON/ra_data_processing-all/DATA/'

MaxNsp = 2048                 # Number of spectra to read for one figure
spSkip = 0                    # Number of chunks to skip from data beginning
RFImeanConst = 8              # Constant of RFI mitigation (usually 8)
Vmin = -100                   # Lower limit of figure dynamic range
Vmax = -40                    # Upper limit of figure dynamic range
VminNorm = 0                  # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 20                 # Upper limit of figure dynamic range for normalized spectra
VminCorrMag = -150            # Lower limit of figure dynamic range for correlation magnitude spectra
VmaxCorrMag = -30             # Upper limit of figure dynamic range for correlation magnitude spectra
colormap = 'jet'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
customDPI = 300               # Resolution of images of dynamic spectra
CorrelationProcess = 1        # Process correlation data or save time?  (1 = process, 0 = save)
longFileSaveAch = 1           # Save data A to long file? (1 = yes, 0 = no)
longFileSaveBch = 1           # Save data B to long file? (1 = yes, 0 = no)
longFileSaveCRI = 0           # Save correlation data (Real and Imaginary) to long file? (1 = yes, 0 = no)
longFileSaveCMP = 0           # Save correlation data (Module and Phase) to long file? (1 = yes, 0 = no)
DynSpecSaveInitial = 0        # Save dynamic spectra pictures before claning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 1        # Save dynamic spectra pictures after claning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 1       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
SpecterFileSaveSwitch = 0     # Save 1 immediate specter to TXT file? (1 = yes, 0 = no)
ImmediateSpNo = 0             # Number of immediate specter to save to TXT file



#*************************************************************


#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************
# Common functions
import os
import sys
import struct
import math
import numpy as np
import pylab
import matplotlib.pyplot as plt
import time
import gc
import datetime
from datetime import datetime, timedelta
#from matplotlib import rc

# My functions

from f_FPGA_to_PC_array import FPGAtoPCarray
from f_spectra_normalization import Normalization_dB
from f_ra_data_clean import simple_channel_clean
from f_plot_formats import OneImmedSpecterPlot, TwoImmedSpectraPlot, TwoDynSpectraPlot






#*************************************************************
#                       MAIN PROGRAM                         *
#*************************************************************

for i in range(8): print (' ')
print ('   ****************************************************')
print ('   *      JDS data files reader  v.', Software_version,'       *      (c) YeS 2019')
print ('   ****************************************************')
for i in range(3): print (' ')


startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)
print (' ')


# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = "JDS_Results/Service" 
if not os.path.exists(newpath):
    os.makedirs(newpath)
if DynSpecSaveInitial == 1:
    if not os.path.exists('JDS_Results/Initial_spectra'):
        os.makedirs('JDS_Results/Initial_spectra')
if (DynSpecSaveCleaned == 1 and CorrelationProcess == 1):
    if not os.path.exists('JDS_Results/Correlation_spectra'):
        os.makedirs('JDS_Results/Correlation_spectra')
    
# *** Creating a TXT logfile ***
Log_File = open("JDS_Results/Service/Log.txt", "w")


Log_File.write('\n\n    ****************************************************\n' )
Log_File.write('    *    JDS data files reader  v.%s LOG     *      (c) YeS 2016\n' %Software_version )
Log_File.write('    ****************************************************\n\n' )

Log_File.write('  Date of data processing: %s   \n' %currentDate )
Log_File.write('  Time of data processing: %s \n\n' %currentTime )


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
    

#*********************************************************************************     
  
    # *** Opening datafile ***
    fname = ''
    if len(fname) < 1 : fname = fileList[fileNo]



    with open(fname, 'rb') as file:
    
        # reading FHEADER
        df_filesize = (os.stat(fname).st_size)               # Size of file
        df_filename = file.read(32).decode('utf-8').rstrip('\x00')           # Initial data file name
        df_creation_timeLOC = file.read(32).decode('utf-8').rstrip('\x00')   # Creation time in local time
        df_creation_timeUTC = file.read(32).decode('utf-8').rstrip('\x00')   # Creation time in UTC time
        df_system_name = file.read(32).decode('utf-8').rstrip('\x00')        # System (receiver) name
        df_UTC_time = np.fromfile(file, dtype=np.uint16, count = 8)
        df_system_time = file.read(16).decode('utf-8').rstrip('\x00')        # System (receiver) time UTC
        df_obs_place = file.read(96).decode('utf-8').rstrip('\x00')          # place of observations
        df_description = file.read(256).decode('utf-8').rstrip('\x00')       # File description
        
        print ('')
        print (' Initial data file name:        ', df_filename)
        print (' File size:                     ', round(df_filesize/1024/1024,3), ' Mb (',df_filesize, ' bytes )')
        print (' Creation time in local time:   ', str(df_creation_timeLOC.rstrip()))
        print (' Creation time in UTC time:     ', df_creation_timeUTC)
        print (' System (receiver) name:        ', df_system_name)
        print (' System (receiver) UTC:         ', df_UTC_time[0],'/',df_UTC_time[1],'/',df_UTC_time[3],' ', df_UTC_time[4],':',df_UTC_time[5],':',df_UTC_time[6],',',df_UTC_time[7])
        print (' System (receiver) time:        ', df_system_time)
        print (' Place of observations:         ', df_obs_place)
        print (' File description:              ', df_description)
    
        print ('')
        
        # *** Parameters that are poor descibed in file description ***
        # reading FHEADER PP and DSPP0 ((16+5)*32 bit)
        DSPmode = np.fromfile(file, dtype=np.uint16, count = 1)
    
        Mode = int(DSPmode & 7)
        #print ' Old mode switch:               ', Mode
            
        CHselect = np.right_shift (DSPmode & 32, 5)
        #if CHselect == 0:   print (' Channel:                        A')
        #if CHselect == 1:   print (' Channel:                        B')
    
        opMode = np.right_shift (DSPmode & 64, 6)
        #if opMode == 0:   print ' Operational Mode:               Normal'
        #if opMode == 1:   print ' Operational Mode:               Decimation (spectrum averaging off)'
    
        FFTwindow = np.right_shift (DSPmode & 128, 7)
        #if FFTwindow == 0:   print ' FFT window:                     Hanning'
        #if FFTwindow == 1:   print ' FFT window:                     Rectangle'
        
        DCrem = np.right_shift (DSPmode & 256, 8)
        #if DCrem == 0:   print ' DC removing:                    No'
        #if DCrem == 1:   print ' DC removing:                    Yes'
    
        Clock = np.right_shift (DSPmode & 512, 9)    
        #if Clock == 0:   print ' Clock:                          Internal'
        #if Clock == 1:   print ' Clock:                          External'
    
        ChAon = np.right_shift (DSPmode & 1024, 10)
        #if ChAon == 0:   print ' Channel A:                      On'
        #if ChAon == 1:   print ' Channel A:                      Off'
    
        ChBon = np.right_shift (DSPmode & 2048, 11)    
        #if ChBon == 0:   print ' Channel B:                      On'
        #if ChBon == 1:   print ' Channel B:                      Off'
        
        SynchroStart = np.right_shift (DSPmode & 4096, 12)    
        #if SynchroStart == 0:   print ' Synchro start:                  On'
        #if SynchroStart == 1:   print ' Synchro start:                  Off'
        
        waitGPS = np.right_shift (DSPmode & 8192, 13)
        #if waitGPS == 0:   print ' GPS start:                      Off'
        #if waitGPS == 1:   print ' GPS start:                      On'
        
        extWeight = np.right_shift (DSPmode & 16384, 14)    
        #if extWeight == 0:   print ' Weighting window:               Internal Hanning'
        #if extWeight == 1:   print ' Weighting window:               External'
        
        DMAinter = np.right_shift ((DSPmode & 2147483648), 31) 
        #if DMAinter == 0:   print ' DMA interrupt:                  Disable'
        #if DMAinter == 1:   print ' DMA interrupt:                  Enable'
    
        
        dataBlockSize = struct.unpack('i', file.read(4))[0] # No info
        print (' Data block size:               ', dataBlockSize)
        
        prcMode       = struct.unpack('i', file.read(4))[0]
        
        NAvr = (prcMode & 4095) + 1
        SLine = np.right_shift ((prcMode & 458752), 16)
        Width = np.right_shift ((prcMode & 7340032), 19)
        #print (' NAvr (?):                      ', NAvr)
        #print (' Start line number (?):         ', SLine)
        #print (' Width of spectra (?):          ', Width)
        
        testGen = struct.unpack('i', file.read(4))[0] # No info
        clc     = struct.unpack('i', file.read(4))[0] # No info
        fftsize = struct.unpack('i', file.read(4))[0] # 
        #print (' testGen (?):                   ', testGen)
        #print (' fftsize (?):                   ', fftsize)
        #print (' clc (?):                       ', clc)
        
        temp    = file.read(40) # No info
        
        FFT_Size   = struct.unpack('i', file.read(4))[0] # FFT size
        MinDSPSize = struct.unpack('i', file.read(4))[0] # e
        MinDMASize = struct.unpack('i', file.read(4))[0] # 
        DMASizeCnt = struct.unpack('i', file.read(4))[0] # 
        DMASize    = struct.unpack('i', file.read(4))[0] # 
        #print (' FFT_Size (?):                  ', FFT_Size)
        #print (' MinDSPSize (?):                ', MinDSPSize)
        #print (' MinDMASize (?):                ', MinDMASize)
        #print (' DMASizeCnt (?):                ', DMASizeCnt)
        #print (' DMASize (?):                   ', DMASize)
    
        temp = file.read(2)       # Skipping
        
        print ('')
        
        # *** Parameters that are well descibed in file description ***
        
        CLCfrq     = struct.unpack('f', file.read(4))[0] # 
        Synch      = struct.unpack('i', file.read(4))[0] # 
        SSht       = struct.unpack('i', file.read(4))[0] # 
        Mode       = struct.unpack('i', file.read(4))[0] # 
        Wch        = struct.unpack('i', file.read(4))[0] # 
        Smd        = struct.unpack('i', file.read(4))[0] # 
        Offt       = struct.unpack('i', file.read(4))[0] # 
        Lb         = struct.unpack('i', file.read(4))[0] # 
        Hb         = struct.unpack('i', file.read(4))[0] # 
        Wb         = struct.unpack('i', file.read(4))[0] # 
        Navr       = struct.unpack('i', file.read(4))[0] # 
        CAvr       = struct.unpack('i', file.read(4))[0] # 
        Weight     = struct.unpack('i', file.read(4))[0] # 
        DCRem      = struct.unpack('i', file.read(4))[0] # 
        ExtSyn     = struct.unpack('i', file.read(4))[0] # 
        Ch1        = struct.unpack('i', file.read(4))[0] # 
        Ch2        = struct.unpack('i', file.read(4))[0] # 
        ExtWin     = struct.unpack('i', file.read(4))[0] # 
        Clip       = struct.unpack('i', file.read(4))[0] # 
        HPF0       = struct.unpack('i', file.read(4))[0] # 
        HPF1       = struct.unpack('i', file.read(4))[0] # 
        LPF0       = struct.unpack('i', file.read(4))[0] # 
        LPF1       = struct.unpack('i', file.read(4))[0] # 
        ATT0       = struct.unpack('i', file.read(4))[0] # 
        ATT1       = struct.unpack('i', file.read(4))[0] # 
        
        df_softname = file.read(16).decode('utf-8').rstrip('\x00')       # 
        df_softvers = file.read(16).decode('utf-8').rstrip('\x00')       # 
        df_DSP_vers = file.read(32).decode('utf-8').rstrip('\x00')       # 
        
    
        if Mode == 0:
            print (' Mode:                            Waveform')
            if Wch == 0:
                print (' Channel:                        A')
            if Wch == 1:
                print (' Channel:                        B')
            if Wch == 2:
                print (' Channels                        A & B')
        if Mode == 1:
            print (' Mode:                           Spectra A & B')
        if Mode == 2:
            print (' Mode:                           Correlation A & B')
    
    
        print (' Sampling ADC frequency:        ', CLCfrq/10**6, ' MHz')
        if ExtSyn == 0:  print (' Synchronization:                Internal')
        if ExtSyn == 1:  print (' Synchronization:                External')   
        print (' GPS synchronization (0-On):    ', Synch)
        print (' Number of averaged spectra:    ', Navr, '\n\n')
        print (' Snap shot Mode (always 1):     ', SSht)
        print (' Smd:                           ', Smd)
        print (' Offt:                          ', Offt)
        print (' Lowest channel number:         ', Lb)
        print (' Highest channel number:        ', Hb)
        print (' Number of channels:            ', Wb)
        print (' CAvr:                          ', CAvr)
        if Weight == 0:  print (' Weightning window:              On')
        if Weight == 1:  print (' Weightning window:              Off')
        if DCRem == 0:   print (' DC removing:                    No')
        if DCRem == 1:   print (' DC removing:                    Yes')
        if Ch1 == 0:     print (' Channel 1:                      On')
        if Ch1 == 1:     print (' Channel 1:                      Off')    
        if Ch2 == 0:     print (' Channel 2:                      On')
        if Ch2 == 1:     print (' Channel 2:                      Off')
        if ExtWin == 0:  print (' External FFT window:            No')
        if ExtWin == 1:  print (' External FFT window:            Yes')    
        print (' Clip:                          ', Clip)
        print (' HPF0:                          ', HPF0)
        print (' HPF1:                          ', HPF1)
        print (' LPF0:                          ', LPF0)
        print (' LPF1:                          ', LPF1)
        print (' ATT0:                          ', ATT0)
        print (' ATT1:                          ', ATT1)   
            
        print (' Softvare name:                 ', df_softname)
        print (' Softvare version:              ', df_softvers)
        print (' DSP soft version:              ', df_DSP_vers)
    
    
        # *** Saving to LOG FILE ***
        Log_File.write(' Initial data file name:         %s \n' % df_filename)
        Log_File.write(' File size:                      %s Mb \n' % str(df_filesize/1024/1024))
        Log_File.write(' Creation time in local time:    %s \n' % str(df_creation_timeLOC))
        Log_File.write(' Creation time in UTC time:      %s \n' % str(df_creation_timeUTC))
        Log_File.write(' System (receiver) name:         %s \n' % df_system_name)
        Log_File.write(' Place of observations:          %s \n' % df_obs_place)
        Log_File.write(' File description:               %s \n' % df_description)
        Log_File.write(' Averaged spectra:               %s \n' % Navr)
        Log_File.write(' Clock frequency:                %s MHz \n' % str(CLCfrq*10**-6))
        
    
        print ('\n')
        
        
        # *** Temporal and frequency resolutions ***
        Sfft = 8192.0
        TimeRes = Navr * (Sfft / CLCfrq);
        df = CLCfrq / 2 / Sfft
        print (' Temporal resolution:           ', round((TimeRes*1000),3), '  ms')
        print (' Real frequency resolution:     ', round((df/1000),3), ' kHz')
        
        
    
        # *** Frequncy calculation (in MHz) ***
        f0 = (Lb * df)
        FreqPointsNum = Wb
        frequency = [0 for col in range(FreqPointsNum)]
        for i in range (0, FreqPointsNum):
            frequency[i] = (f0 + (i * df)) * (10**-6)    
        if Mode == 1: 
            SpInFile = int(df_filesize - 1024)/(2*4*FreqPointsNum)    # Number of frequency points in specter 
            ReceiverMode = 'Spectra mode'
        if Mode == 2: 
            SpInFile = int(df_filesize - 1024)/(4*4*FreqPointsNum)    # Number of frequency points in specter 
            ReceiverMode = 'Correlation mode'
        print (' Frequency band:                ', round(frequency[0],3), ' - ', round(frequency[FreqPointsNum-1]+(df/pow(10,6)),3), ' MHz')
        print ('')    
        print (' Number of spectra in file:     ', SpInFile, '\n\n')
        
    
        
        # Initial time line settings
        TimeScaleStartDate = datetime(int(df_creation_timeUTC[0:4]), int(df_creation_timeUTC[5:7]), int(df_creation_timeUTC[8:10]), 0, 0, 0, 0)
        
        timeLineMS = np.zeros(int(SpInFile)) # List of ms values from ends of spectra
    
        
        
        # *** Creating a name for long timeline TXT file ***
        if fileNo == 0 and (longFileSaveAch == 1 or longFileSaveBch == 1 or longFileSaveCRI == 1 or longFileSaveCMP == 1): 
            TLfile_name = df_filename + '_Timeline.txt'
            TLfile = open(TLfile_name, 'wb')  # Open and close to delete the file with the same name
            TLfile.close()
        
        
        # *** If it is the first file - write the header to long data file
        if((longFileSaveAch == 1 or longFileSaveBch == 1 or longFileSaveCRI == 1 or longFileSaveCMP == 1) and fileNo == 0): 
            file.seek(0)
            file_header = file.read(1024)
    
            # *** Creating a binary file with data for long data storage ***
            if(longFileSaveAch == 1 and (Mode == 1 or Mode == 2)): 
                Data_A_name = df_filename+'_Data_chA.dat'
                Data_AFile = open(Data_A_name, 'wb')
                Data_AFile.write(file_header)
                Data_AFile.close()
            if(longFileSaveBch == 1 and (Mode == 1 or Mode == 2)): 
                Data_B_name = df_filename+'_Data_chB.dat'
                Data_BFile = open(Data_B_name, 'wb')
                Data_BFile.write(file_header)
                Data_BFile.close()
            if(longFileSaveCRI == 1 and Mode == 2): 
                Data_CRe_name = df_filename+'_Data_CRe.dat'
                Data_CReFile = open(Data_CRe_name, 'wb')
                Data_CReFile.write(file_header)
                Data_CReFile.close()
                Data_CIm_name = df_filename+'_Data_CIm.dat'
                Data_CImFile = open(Data_CIm_name, 'wb')
                Data_CImFile.write(file_header)
                Data_CImFile.close()
            if(longFileSaveCMP == 1 and Mode == 2): 
                Data_Cm_name = df_filename+'_Data_C_m.dat'
                Data_CmFile = open(Data_Cm_name, 'wb')
                Data_CmFile.write(file_header)
                Data_CmFile.close()
                Data_Cp_name = df_filename+'_Data_C_p.dat'
                Data_CpFile = open(Data_Cp_name, 'wb')
                Data_CpFile.write(file_header)
                Data_CpFile.close()   
                
                
                
            
            del file_header
            
        Log_File.close()
        print (' ')
        print ('  *** Reading data from file ***')
        print (' ')   
        
        
        #************************************************************************************
        #                            R E A D I N G   D A T A                                *
        #************************************************************************************
        
        file.seek(1024)  # Jumping to 1024 byte from file beginning #+ (sizeOfChunk+8) * chunkSkip
        
        
        if Mode > 0 and Mode < 3:           # Spectra modes
            figID = -1
            figMAX = int(math.ceil((SpInFile - spSkip)/MaxNsp))
            if figMAX < 1: figMAX = 1
            for fig in range (figMAX):
                Time1 = time.time()               # Timing
                figID = figID + 1
                currentTime = time.strftime("%H:%M:%S")
                print (' File # ', str(fileNo+1), ' of ', str(len(fileList)), ', figure # ', figID+1, ' of ', figMAX, '   started at: ', currentTime)
                if (SpInFile - spSkip - MaxNsp * figID) < MaxNsp:
                    Nsp = int(SpInFile - spSkip - MaxNsp * figID)
                else:
                    Nsp = MaxNsp
    
    
                # *** Preparing empty matrices ***
                if Mode == 1 or Mode == 2:
                    Data_ChA = np.zeros((Nsp, FreqPointsNum))
                
                if Mode == 1 or Mode == 2:            
                    Data_ChB = np.zeros((Nsp, FreqPointsNum)) 
            
                if Mode == 2:            
                    Data_CRe = np.zeros((Nsp, FreqPointsNum))
                    Data_CIm = np.zeros((Nsp, FreqPointsNum))
                    CorrModule = np.zeros((Nsp, FreqPointsNum))
                    CorrPhase = np.zeros((Nsp, FreqPointsNum))
                
                # *** Reading and reshaping all data for figure ***
                if Mode == 1: 
                    raw = np.fromfile(file, dtype='u4', count = (2 * Nsp * FreqPointsNum)) 
                    raw = np.reshape(raw, [2*FreqPointsNum, Nsp], order='F')
                    Data_ChA = raw[0:(FreqPointsNum*2):2, :].transpose()    
                    Data_ChB = raw[1:(FreqPointsNum*2):2, :].transpose()  
                    
                if Mode == 2: 
                    raw = np.fromfile(file, dtype='u4', count = (4 * Nsp * FreqPointsNum)) 
                    raw = np.reshape(raw, [4*FreqPointsNum, Nsp], order='F')  
                    Data_ChA = raw[0:(FreqPointsNum*4):4, :].transpose()    
                    Data_ChB = raw[1:(FreqPointsNum*4):4, :].transpose()
                    Data_CRe = raw[2:(FreqPointsNum*4):4, :].transpose()
                    Data_CIm = raw[3:(FreqPointsNum*4):4, :].transpose()
                
                del raw
                    
                # *** Single out timing from data ***
                counterA2 = np.uint64(Data_ChA[:,-1])
                counterB2 = np.uint64(Data_ChB[:,-1])
                counterA1 = np.uint64(Data_ChA[:,-2])
                counterB1 = np.uint64(Data_ChB[:,-2])
                
                A = np.uint64(int('01111111111111111111111111111111', 2))
                msCount = np.uint32(np.bitwise_and (counterB2, A))        # number of ms since record started
                ftCount = np.uint32(np.bitwise_and (counterA2, A))        # number of specter since record started
                    
                A = np.uint64(int('00000111111111111111111111111111', 2))
                phaOfSec = np.uint32(np.bitwise_and (counterA1, A))        # phase of second for the spectr
                A = np.uint64(int('00000000000000011111111111111111', 2))
                secOfDay = np.uint32(np.bitwise_and (counterB1, A))        # second of the day for the specter
                
    
    
                # *** Time line arranging ***
                
                # Preparing/cleaning matrices for time scales 
                TimeScale = []              # New for each file
                TimeFigureScale = []        # Timelime (new) for each figure (Nsp)
                # Calculations
                FigStartTime = timedelta(0, int(secOfDay[0]), int(1000000*phaOfSec[0]/CLCfrq))
                for i in range (Nsp):
                    TimeAdd = timedelta(0, int(secOfDay[i]), int(1000000*phaOfSec[i]/CLCfrq))
                    TimeScale.append(str(str(TimeScaleStartDate + TimeAdd)))  
                    TimeFigureScale.append(str((TimeAdd - FigStartTime)))
                    
                
                
                # *** Converting from FPGA to PC float format ***
                if Mode == 1 or Mode == 2:
                    Data_ChA = FPGAtoPCarray(Data_ChA, Navr)
                    Data_ChB = FPGAtoPCarray(Data_ChB, Navr)
                if (Mode == 2 and CorrelationProcess == 1):
                    Data_CRe = FPGAtoPCarray(Data_CRe, Navr)
                    Data_CIm = FPGAtoPCarray(Data_CIm, Navr)
                    
                
                
                '''
                # *** Absolute correlation specter plot ***
                if Mode == 2 and figID == 0:   #  Immediate correlation spectrum channels A & B  
                    TwoImmedSpectraPlot(frequency, Data_CRe[1][:], Data_CIm[1][:], 'Channel A', 'Channel B', 
                                        frequency[0], frequency[FreqPointsNum-1], -0.001, 0.001, 
                                        'Frequency, MHz', 'Amplitude, dB', 
                                        'Immediate spectrum '+str(df_filename[0:18])+ ' channels A & B',
                                        'Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+str(round(df/1000,3))+' kHz',
                                        'JDS_Results/Service/'+df_filename[0:14]+' Correlation Spectrum Re and Im before log.png')
                '''
                
                
                
                # *** Saving data to a long-term file ***
                if (Mode == 1 or Mode == 2) and longFileSaveAch == 1:
                    Data_AFile = open(Data_A_name, 'ab')
                    Data_AFile.write(Data_ChA)
                    Data_AFile.close()
                if (Mode == 1 or Mode == 2) and longFileSaveBch == 1:
                    Data_BFile = open(Data_B_name, 'ab')
                    Data_BFile.write(Data_ChB)
                    Data_BFile.close()
                if  Mode == 2 and longFileSaveCRI == 1:
                    Data_CReFile = open(Data_CRe_name, 'ab')
                    Data_CReFile.write(np.float64(Data_CRe))
                    Data_CReFile.close()
                    Data_CImFile = open(Data_CIm_name, 'ab')
                    Data_CImFile.write(np.float64(Data_CIm))
                    Data_CImFile.close()
                    
                if(longFileSaveAch == 1 or longFileSaveBch == 1 or longFileSaveCRI == 1 or longFileSaveCMP == 1):
                    with open(TLfile_name, 'a') as TLfile:
                        for i in range(Nsp):
                            TLfile.write((TimeScale[i][:]+' \n'))  #str.encode
                    
                    
                    #TLfile = open(TLfile_name, 'ab')
                    #for i in range(Nsp):
                    #    TLfile.write(str.encode(TimeScale[i][:]+' \n')) 
                    #TLfile.close
                
                
                
                # *** Converting to logarythmic scale matrices ***
                if (Mode == 1 or Mode == 2):
                    with np.errstate(invalid='ignore'):            
                        Data_ChA = 10*np.log10(Data_ChA)
                        Data_ChB = 10*np.log10(Data_ChB)
                    Data_ChA[np.isnan(Data_ChA)] = -120
                    Data_ChB[np.isnan(Data_ChB)] = -120
                if (Mode == 2 and CorrelationProcess == 1):
                    with np.errstate(invalid='ignore'):
                        CorrModule = 10*np.log10(((Data_CRe)**2 + (Data_CIm)**2)**(0.5))
                        CorrPhase = np.arctan2(Data_CIm, Data_CRe)
                    CorrPhase[np.isnan(CorrPhase)] = 0
                
                
                if (Mode == 2 and CorrelationProcess == 1 and longFileSaveCMP == 1):
                    Data_CmFile = open(Data_Cm_name, 'ab')
                    Data_CmFile.write(np.float64(CorrModule))
                    Data_CmFile.close()
                    Data_CpFile = open(Data_Cp_name, 'ab')
                    Data_CpFile.write(np.float64(CorrPhase))
                    Data_CpFile.close()
                    
                
                    
                # *** Saving immediate spectrum to file ***
                if(SpecterFileSaveSwitch == 1 and figID == 0):
                    SpFile = open('JDS_Results/Service/Specter_'+df_filename[0:14]+'.txt', 'w')
                    for i in range(FreqPointsNum-1):
                        if Mode == 1:
                            SpFile.write(str('{:10.6f}'.format(frequency[i]))+'  '+str('{:16.10f}'.format(Data_ChA[ImmediateSpNo][i]))+'  '+str('{:16.10f}'.format(Data_ChB[ImmediateSpNo][i]))+' \n')
                        if Mode == 2:
                            SpFile.write(str(frequency[i])+'  '+str(Data_ChA[ImmediateSpNo][i])+'  '+str(Data_ChB[ImmediateSpNo][i])+'  '+str(Data_CRe[ImmediateSpNo][i])+'  '+str(Data_CIm[ImmediateSpNo][i])+' \n')
                        
                    SpFile.close()    
                    
                    
                    
    
    #************************************************************************************
    #                                  F I G U R E S
    #************************************************************************************
                    
    
                
                # *** Plotting immediate spectra before cleaning and normalizing ***
                if (Mode == 1 or Mode == 2) and figID == 0:
                    TwoImmedSpectraPlot(frequency, Data_ChA[0][:], Data_ChB[0][:], 'Channel A', 'Channel B', 
                                                frequency[0], frequency[FreqPointsNum-1], -120, -20, 
                                                'Frequency, MHz', 'Amplitude, dB', 
                                                'Immediate spectrum '+str(df_filename[0:18])+ ' channels A & B',
                                                'Place: '+str(df_obs_place)+', Receiver: '+str(df_system_name)+'. Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+str(round(df/1000,3))+' kHz '+'\n Description: '+str(df_description),
                                                'JDS_Results/Service/' + df_filename[0:14] + ' Channels A and B Immediate Spectrum before cleaning and normalizing.png', 
                                                currentDate, currentTime, Software_version)
            
                if Mode == 2 and CorrelationProcess == 1 and figID == 0:
                    OneImmedSpecterPlot(frequency, CorrModule[0][:], 'Correlation module',  
                                                frequency[0], frequency[FreqPointsNum-1], -140, -20, 
                                                'Frequency, MHz', 'Amplitude, dB', 
                                                'Immediate correlation spectrum '+str(df_filename[0:18])+ ' channels A & B',
                                                'Place: '+str(df_obs_place)+', Receiver: '+str(df_system_name)+'. Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+str(round(df/1000,3))+' kHz '+'\n Description: '+str(df_description),
                                                'JDS_Results/Service/' + df_filename[0:14] + ' Channels A and B Correlation Immedaiate Spectrum before cleaning and normalizing.png', 
                                                currentDate, currentTime, Software_version)
            
                if Mode == 2 and CorrelationProcess == 1 and figID == 0:
                    OneImmedSpecterPlot(frequency, CorrPhase[0][:], 'Correlation phase', 
                                                frequency[0], frequency[FreqPointsNum-1], -4, 4, 
                                                'Frequency, MHz', 'Phase, deg', 
                                                'Immediate correlation phase spectrum '+str(df_filename[0:18])+ ' channels A & B',
                                                'Place: '+str(df_obs_place)+', Receiver: '+str(df_system_name)+'. Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+str(round(df/1000,3))+' kHz '+'\n Description: '+str(df_description),
                                                'JDS_Results/Service/' + df_filename[0:14] + ' Channels A and B Correlation Immedaiate phase before cleaning and normalizing.png', 
                                                currentDate, currentTime, Software_version)
    
    
                                                
                                                
                # *** FIGURE Initial dynamic spectrum channels A and B (python 3 new version) ***
                if (Mode == 1 or Mode == 2) and DynSpecSaveInitial == 1:
                    TwoDynSpectraPlot(Data_ChA, Data_ChB, Vmin, Vmax, Vmin, Vmax,
                        'Dynamic spectrum (initial) ',
                        figID, figMAX, TimeRes, df, '', df_system_name, df_obs_place, 
                        df_filename, df_description, 'Intensity, dB', 'Intensity, dB', Nsp, 
                        1, 1, ReceiverMode, TimeFigureScale, TimeScale,
                        Nsp, frequency, FreqPointsNum, colormap,
                        'Channel A', 'Channel B', 
                        'JDS_Results/Initial_spectra/',
                        ' Initial dynamic spectrum fig.', 
                        currentDate, currentTime, Software_version, customDPI) 
                                                
                
                # *** FIGURE Initial correlation spectrum Module and Phase (python 3 new version) ***
                if (Mode == 2 and CorrSpecSaveInitial == 1 and CorrelationProcess == 1):
                    TwoDynSpectraPlot(CorrModule, CorrPhase, VminCorrMag, VmaxCorrMag, -3.15, 3.15,
                        'Correlation spectrum (initial) ',
                        figID, figMAX, TimeRes, df, '', df_system_name, df_obs_place, 
                        df_filename, df_description, 'Intensity, dB', 'Phase, deg', Nsp, 
                        1, 1, ReceiverMode, TimeFigureScale, TimeScale,
                        Nsp, frequency, FreqPointsNum, colormap,
                        'Module', 'Phase', 
                        'JDS_Results/Correlation_spectra/',
                        ' Correlation dynamic spectra fig.', 
                        currentDate, currentTime, Software_version, customDPI)
                
                                                
                # *** Normalizing amplitude-frequency responce ***
                if Mode == 1 or Mode == 2:
                    Normalization_dB(Data_ChA, FreqPointsNum, Nsp)
                    Normalization_dB(Data_ChB, FreqPointsNum, Nsp)
                if Mode == 2 and CorrelationProcess == 1 and CorrSpecSaveCleaned == 1:
                    Normalization_dB(CorrModule, FreqPointsNum, Nsp)
                    
                    
                # *** Deleting cahnnels with strong RFI ***
                if Mode == 1 or Mode == 2:
                    simple_channel_clean(Data_ChA, RFImeanConst)
                    simple_channel_clean(Data_ChB, RFImeanConst)
                if Mode == 2 and CorrelationProcess == 1 and CorrSpecSaveCleaned == 1:
                    simple_channel_clean(CorrModule, 2 * RFImeanConst)
        
    
                
                #   *** Immediate spectra ***    (only for first figure in data file)
                if (Mode == 1 or Mode == 2) and figID == 0:   # Immediate spectrum channels A & B  
                    TwoImmedSpectraPlot(frequency, Data_ChA[1][:], Data_ChB[1][:], 'Channel A', 'Channel B', 
                                        frequency[0], frequency[FreqPointsNum-1], -10.0, 40.0, 
                                        'Frequency, MHz', 'Amplitude, dB', 
                                        'Immediate spectrum '+str(df_filename[0:18])+ ' channels A & B',
                                        'Place: '+str(df_obs_place)+', Receiver: '+str(df_system_name)+'. Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+str(round(df/1000,3))+' kHz '+'\n Description: '+str(df_description),
                                        'JDS_Results/Service/'+df_filename[0:14]+' Channels A and B Immediate Spectrum after cleaning and normalizing.png', currentDate, currentTime, Software_version)
    
    
    
                # *** FIGURE Normalized dynamic spectrum channels A and B (python 3 new version) ***
                if (Mode == 1 or Mode == 2) and DynSpecSaveCleaned == 1:
                    TwoDynSpectraPlot(Data_ChA, Data_ChB, VminNorm, VmaxNorm, VminNorm, VmaxNorm,
                        'Dynamic spectrum (normalized) ',
                        figID, figMAX, TimeRes, df, '', df_system_name, df_obs_place, 
                        df_filename, df_description, 'Intensity, dB', 'Intensity, dB', Nsp, 
                        1, 1, ReceiverMode, TimeFigureScale, TimeScale,
                        Nsp, frequency, FreqPointsNum, colormap,
                        'Channel A', 'Channel B', 
                        'JDS_Results/',
                        ' Dynamic spectra fig.', currentDate, currentTime, Software_version, customDPI) 
    
                        
                # *** FIGURE Normalized correlation spectrum Module and Phase (python 3 new version) ***
                if (Mode == 2 and CorrSpecSaveCleaned == 1 and CorrelationProcess == 1):
                    TwoDynSpectraPlot(CorrModule, CorrPhase, 2*VminNorm, 2*VmaxNorm, -3.15, 3.15,
                        'Correlation spectrum (normalized) ',
                        figID, figMAX, TimeRes, df, '', df_system_name, df_obs_place, 
                        df_filename, df_description, 'Intensity, dB', 'Phase, deg', Nsp, 
                        1, 1, ReceiverMode, TimeFigureScale, TimeScale,
                        Nsp, frequency, FreqPointsNum, colormap,
                        'Module', 'Phase', 
                        'JDS_Results/Correlation_spectra/',
                        ' Correlation dynamic spectra cleaned fig.', currentDate, currentTime, Software_version, customDPI)
                
    
    
            '''
            # Check of second counter data for linearity
            OneImmedSpecterPlot(list(range(ChunksInFile)), timeLineSecond, 'timeLineSecond', 
                                0, ChunksInFile, 0, 2000, 
                                'Time, sec', 'Second counter, sec', 
                                'Second counter',
                                ' ',
                                'ADR_Results/Service/' + df_filename[0:14] + ' Second counter fig.' + str(figID+1) + '.png')
            
            '''
            
            gc.collect()
    
        print ('\n  Position in file: ', file.tell(), ' File size: ', df_filesize)
        if (file.tell() == df_filesize): print ('\n  File was read till the end \n')
        if (file.tell() < df_filesize):  
            print ('    The difference is ', (df_filesize - file.tell()), ' bytes')
            print ('\n  File was NOT read till the end!!! ERROR')
    
    #file.close()  #Here we close the file


endTime = time.time()    # Time of calculations      
      
        
print (' ')
print ('  The program execution lasted for ', round((endTime - startTime),2), 'seconds')
for i in range (0,2) : print (' ')
print ('    *** Program JDS_reader has finished! ***')
for i in range (0,3) : print (' ')
