# *************************************************************
#                        PARAMETERS                          *
# *************************************************************
# Directory of files to be analyzed:
directory = 'e:/2017.05.22_UTR2_B1919p21/' 

# *************************************************************
#                    IMPORT LIBRARIES                         *
# *************************************************************
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

# *************************************************************
#                        FUNCTIONS                            *
# *************************************************************

# *** FPGAtoPC Transforms FPGA array data format to ordinary PC numbers ***
def FindTimeOfSpecter (file, byteNumber, TimeScaleStartDate):

    file.seek(byteNumber)
    #print 'Current position is', file.tell(), ' bytes \n' # tells the position in the file
    Nsp = 1

    # *** Preparing empty matrices ***
    if Mode == 1 or Mode == 2:
        Data_ChA = np.zeros((Nsp, FreqPointsNum))
        Data_ChB = np.zeros((Nsp, FreqPointsNum)) 
    if Mode == 2:            
        Data_CRe = np.zeros((Nsp, FreqPointsNum))
        Data_CIm = np.zeros((Nsp, FreqPointsNum))
        CorrModule = np.zeros((Nsp, FreqPointsNum))
        CorrPhase = np.zeros((Nsp, FreqPointsNum))
            
    # *** Reading and reshaping all daFindTimeOfSpecter (file, byteNumber):ta for figure ***
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
    counterA1 = np.uint64(Data_ChA[:,-2])
    counterB1 = np.uint64(Data_ChB[:,-2])
    
    A = np.uint64(int('00000111111111111111111111111111', 2))
    phaOfSec = np.uint32(np.bitwise_and (counterA1, A))        # phase of second for the spectr
    A = np.uint64(int('00000000000000011111111111111111', 2))
    secOfDay = np.uint32(np.bitwise_and (counterB1, A))        # second of the day for the specter
    
    # *** Time line arranging ***
    for i in range (Nsp):
        TimeAdd = timedelta(0, int(secOfDay[i]), int(1000000*phaOfSec[i]/CLCfrq))
        timeOfSpecter = (TimeScaleStartDate + TimeAdd)
        
    return timeOfSpecter


# *************************************************************
#                        MAIN PROGRAM                         *
# *************************************************************


print('\n\n\n\n\n\n\n   ****************************************************')
print('   *     JDS data files header add time  v1.0         *      (c) YeS 2017')
print('   **************************************************** \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print('  Today is ', currentDate, ' time is ', currentTime, ' \n')

# *** Search JDS files in the directory ***
fileList = []
i = 0
print('  Directory: ', directory, '\n')
print('  List of files to be analyzed: ')
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.jds'):
            i = i + 1
            print('         ', i, ') ', file)
            fileList.append(str(os.path.join(root, file)))

for fileNo in range(len(fileList)):   # loop by files
    print('\n\n  *  File ',  str(fileNo+1), ' of', str(len(fileList)))
    print('  *  File path: ', str(fileList[fileNo]))

# *********************************************************************************
  
    # *** Opening datafile ***
    fname = ''
    if len(fname) < 1 : fname = fileList[fileNo]
    file = open(fname, 'rb')
    
    # reading FHEADER
    df_filesize = os.stat(fname).st_size                 # Size of file
    df_filename = file.read(32).rstrip('\x00')           # Initial data file name
    df_creation_timeLOC = file.read(32).rstrip('\x00')   # Creation time in local time
    df_creation_timeUTC = file.read(32).rstrip('\x00')   # Creation time in UTC time
    df_system_name = file.read(32).rstrip('\x00')        # System (receiver) name
    df_UTC_time = np.fromfile(file, dtype=np.uint16, count = 8)
    df_system_time = file.read(16).rstrip('\x00')        # System (receiver) time UTC
    df_obs_place = file.read(96).rstrip('\x00')          # place of observations
    df_description = file.read(256).rstrip('\x00')       # File description
    
    print('\n Initial data file name:        ', df_filename)
    print(' File description:              ', df_description)
    
    # reading FHEADER PP and DSPP0 ((16+5)*32 bit)
    DSPmode = np.fromfile(file, dtype=np.uint16, count = 1)
    dataBlockSize = struct.unpack('i', file.read(4))[0] # No info
    prcMode       = struct.unpack('i', file.read(4))[0]
    NAvr = (prcMode & 4095) + 1
    SLine = np.right_shift ((prcMode & 458752), 16)
    Width = np.right_shift ((prcMode & 7340032), 19)
    testGen = struct.unpack('i', file.read(4))[0] # No info
    clc     = struct.unpack('i', file.read(4))[0] # No info
    fftsize = struct.unpack('i', file.read(4))[0] # 
    temp    = file.read(40) # No info
    FFT_Size   = struct.unpack('i', file.read(4))[0] # FFT size
    MinDSPSize = struct.unpack('i', file.read(4))[0] # e
    MinDMASize = struct.unpack('i', file.read(4))[0] # 
    DMASizeCnt = struct.unpack('i', file.read(4))[0] # 
    DMASize    = struct.unpack('i', file.read(4))[0] # 
    temp = file.read(2)       # Skipping
    
    # *** Parameters that are well described in file description ***
    
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
    
    df_softname = file.read(16).rstrip('\x00')       # 
    df_softvers = file.read(16).rstrip('\x00')       # 
    df_DSP_vers = file.read(32).rstrip('\x00')       # 

    if Mode == 0:
        print(' Mode:                            Waveform')
        if Wch == 0:
            print(' Channel:                        A')
        if Wch == 1:
            print(' Channel:                        B')
        if Wch == 2:
            print(' Channels                        A & B')
    if Mode == 1:
        print(' Mode:                           Spectra A & B')
    if Mode == 2:
        print(' Mode:                           Correlation A & B')

    Sfft = 8192.0
    TimeRes = Navr * (Sfft / CLCfrq)
    df = CLCfrq / 2 / Sfft
    print(' Temporal resolution:           ', round((TimeRes*1000), 3), '  ms')
    print(' Real frequency resolution:     ', round((df/1000), 3), ' kHz')
    
    # *** Frequency calculation (in MHz) ***
    f0 = Lb * df
    FreqPointsNum = Wb
    frequency = [0 for col in range(FreqPointsNum)]
    for i in range(0, FreqPointsNum):
        frequency[i] = (f0 + (i * df)) * (10**-6)    
    if Mode == 1:
        SpInFile = (df_filesize - 1024) / (2*4*FreqPointsNum)    # Number of frequency points in specter
    if Mode == 2:
        SpInFile = (df_filesize - 1024) / (4*4*FreqPointsNum)    # Number of frequency points in specter
    print(' Number of spectra in file:     ', SpInFile)
    
    # Initial time line settings
    TimeScaleStartDate = datetime(int(df_creation_timeUTC[0:4]), int(df_creation_timeUTC[5:7]),
                                  int(df_creation_timeUTC[8:10]), 0, 0, 0, 0)
    
    print(' ')
    #print ' Current position is', file.tell(), ' bytes \n' # tells the position in the file

    file.seek(1024 - 2 * 26 - 16)
    #print ' Current position is', file.tell(), ' bytes \n'   # tells the position in the file
    print(' End of header (must be empty): ')
    temp = file.read(26).rstrip('\x00')
    print('  ', str(temp))
    temp = file.read(26).rstrip('\x00')
    print('  ', str(temp))
    temp = file.read(16).rstrip('\x00')
    print('  ', str(temp))
    print('  |****************|*********|')

    if fileNo == 0:
        byteNo = 1024
        startObsTime = FindTimeOfSpecter (file, byteNo, TimeScaleStartDate)
    
    if fileNo == (len(fileList)-1):
        if Mode == 1: byteNo = 1024 + 4 * (SpInFile-1) * 2 * FreqPointsNum
        if Mode == 2: byteNo = 1024 + 4 * (SpInFile-1) * 4 * FreqPointsNum
        endObsTime = FindTimeOfSpecter (file, byteNo, TimeScaleStartDate)

    file.close()
        
duration = endObsTime - startObsTime
print('\n ************************************************************ \n')
print(' Observation begun: ', startObsTime)
print(' Observation ended: ', endObsTime)
print('\n Duration of observations: ', duration)

startObsTime = str(startObsTime)
endObsTime = str(endObsTime)
duration = str(duration)
if len(duration) == 14: duration = '  ' + duration
if len(duration) == 15: duration = ' '  + duration

checkConst = input('\n Enter "1" if the place is empty and you want to write time data there:  ')
if len(checkConst) < 0 or checkConst != '1':
    print('\n\n\n         You have chosen not to change the file header!!! \n\n')
    sys.exit('\n                         Program stopped\n\n')

# Writing the duration of observations to headers of all files    
for fileNo in range(len(fileList)):   # loop by files
    print('\n\n  *  File ',  str(fileNo+1), ' of', str(len(fileList)))
    print('  *  File path: ', str(fileList[fileNo]))

    # *** Opening datafile ***
    fname = ''
    if len(fname) < 1 : fname = fileList[fileNo]
    file = open(fname, 'r+b')    

    # Writing time data to file header    
    file.seek(1024 - 2 * 26 - 16)
    file.write(str(startObsTime))
    file.write(str(endObsTime))
    file.write(str(duration))
    print('\n Data have been written to the file \n')

    # Checking if the data was written correctly
    file.seek(1024 - 2 * 26 - 16)
    #print ' Current position is', file.tell(), ' bytes \n\n'   # tells the position in the file
    #temp = file.read(2 * 26 + 16).rstrip('\x00')                  # Checking if the place is empty
    print(' End of header ( new version ): ')
    temp = file.read(26).rstrip('\x00')
    print('  ', str(temp))
    temp = file.read(26).rstrip('\x00')
    print('  ', str(temp))
    temp = file.read(16).rstrip('\x00')
    print('  ', str(temp))
    print('  |****************|*********|')
    print('\n\n')
    
    file.close()
    
endTime = time.time()    # Time of calculations

print('  The program execution lasted for ', round((endTime - startTime),2), 'seconds')
print('\n\n    *** Program has finished! *** \n\n\n')
