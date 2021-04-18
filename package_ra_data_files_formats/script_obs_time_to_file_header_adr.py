# the script finds the .adr file, finds its duration and saves the
# time of start, time of end and the duration to the file header
# The purpose of the script is to use the duration in the header
# for processing of spectral data of pulsar observations in IDL

# *************************************************************
#                         PARAMETERS                          *
# *************************************************************
# Directory of files to be analyzed:
directory = 'h:/tmp_data_to_delete/2019.09.04_GURT_Sun_3C405_3C461_int_R/'

# *************************************************************
#                    IMPORT LIBRARIES                         *
# *************************************************************
import os
import struct
import numpy as np
import time
import sys
from datetime import datetime, timedelta

# *************************************************************
#                        MAIN PROGRAM                         *
# *************************************************************
print('\n\n\n\n\n   ****************************************************')
print('   *     ADR data files header add time  v1.0         *      (c) YeS 2017')
print('   **************************************************** \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print('  Today is ', currentDate, ' time is ', currentTime, ' \n')

# Search ADR files in the directory
fileList = []
i = 0
print('  Directory: ', directory, '\n')
print('  List of files to be analyzed: ')

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.adr'):
            i = i + 1
            print('         ', i, ') ', file)
            fileList.append(str(os.path.join(root, file)))

for fileNo in range(len(fileList)):                                        # loop by files
    print('\n\n\n  *  File ',  str(fileNo+1), ' of', str(len(fileList)))
    print('  *  File path: ', str(fileList[fileNo]))
    Log_File = open('Log.txt', 'w')
    Log_File.write('\n\n\n  * File ' + str(fileNo+1) + ' of %s \n' % str(len(fileList)))
    Log_File.write('  * File path: %s \n\n\n' % str(fileList[fileNo]))
    
# *********************************************************************************
  
    # *** Opening datafile ***
    fname = ''
    if len(fname) < 1:
        fname = fileList[fileNo]
    file = open(fname, 'r+b')
    
    # reading FHEADER
    df_filesize = os.stat(fname).st_size                                 # Size of file
    df_filename = file.read(32).decode('utf-8').rstrip('\x00')
    df_creation_timeLOC = file.read(24).decode('utf-8').rstrip('\x00')   # Creation time in local time
    temp = file.read(8)
    df_creation_timeUTC = file.read(32).decode('utf-8').rstrip('\x00')   # Creation time in UTC time
    df_system_name = file.read(32).decode('utf-8').rstrip('\x00')        # System (receiver) name
    df_obs_place = file.read(128).decode('utf-8').rstrip('\x00')         # place of observations
    df_description = file.read(256).decode('utf-8').rstrip('\x00')       # File description

    # reading FHEADER PP ADRS_PAR
    ADRmode = struct.unpack('i', file.read(4))[0]
    FFT_Size = struct.unpack('i', file.read(4))[0]
    NAvr = struct.unpack('i', file.read(4))[0]
    SLine = struct.unpack('i', file.read(4))[0]
    Width = struct.unpack('i', file.read(4))[0]
    BlockSize = struct.unpack('i', file.read(4))[0]
    F_ADC = struct.unpack('i', file.read(4))[0]

    # FHEADER PP ADRS_OPT
    SizeOfStructure = struct.unpack('i', file.read(4))[0]  # the size of ADRS_OPT structure
    StartStop = struct.unpack('i', file.read(4))[0]        # starts/stops DSP data processing
    StartSec = struct.unpack('i', file.read(4))[0]         # UTC abs.time.sec - processing starts
    StopSec = struct.unpack('i', file.read(4))[0]          # UTC abs.time.sec - processing stops
    Testmode = struct.unpack('i', file.read(4))[0]
    NormCoeff1 = struct.unpack('i', file.read(4))[0]       # Normalization coefficient 1-CH: 1 ... 65535
    NormCoeff2 = struct.unpack('i', file.read(4))[0]       # Normalization coefficient 2-CH: 1 ... 65535
    Delay = struct.unpack('i', file.read(4))[0]            # Delay in picoseconds	-1000000000 ... 1000000000
    temp = struct.unpack('i', file.read(4))[0]
    ADRSoptions = bin(temp) 

    print('\n Initial data file name:        ', df_filename)
    print(' File size:                     ', df_filesize/1024/1024, ' Mb (', df_filesize, ' bytes )')
    print(' Creation time in local time:   ', str(df_creation_timeLOC))
    print(' Creation time in UTC time:     ', df_creation_timeUTC)
    print(' System (receiver) name:        ', df_system_name)
    print(' Place of observations:         ', df_obs_place)
    print(' File description:              ', df_description, '\n')
    print(' ADR operation mode             ', ADRmode)
    print(' FFT size                       ', FFT_Size)
    print(' Averaged spectra               ', NAvr)
    print(' Start line number              ', SLine)
    print(' Width in lines                 ', Width)
    print(' Block size                     ', BlockSize)
    print(' Clock frequency                ', F_ADC*10**-6, ' MHz  \n')
    print(' Size of structure              ', SizeOfStructure)
    print(' Start and Stop                 ', StartStop)
    print(' Start Second                   ', StartSec)
    print(' Stop Second                    ', StopSec)
    print(' Testmode                       ', Testmode)
    print(' Norm coeff 1                   ', NormCoeff1)
    print(' Norm coeff 2                   ', NormCoeff2)
    print(' Digital delay                  ', Delay, '\n')
    # print(' ADRSoptions                    ', ADRSoptions)

    if (int(temp) & int('1000')) == 8:
        print(' Start by sec:                   Yes')
    else:
        print(' Start by sec:                   No')
    if (int(temp) & int('0100')) == 4:
        print(' CLC:                            External')
    else:
        print(' CLC:                            Internal')
    if (int(temp) & int('0010')) == 2:
        print(' FFT Window type:                Rectangle')
    else:
        print(' FFT Window type:                Hanning')
    if (int(temp) & int('0001')) == 1: 
        print(' Sum mode switch:                On')
        sumDifMode = ' Sum/diff mode'
    else: 
        print(' Sum mode switch:                Off')
        sumDifMode = ''
    print('')
    
    if ADRmode == 0:
        print(' Mode:                           Waveform A channel')
    elif ADRmode == 1:
        print(' Mode:                           Waveform B channel')
    elif ADRmode == 2:
        print(' Mode:                           Waveform A and B channels')
    elif ADRmode == 3:
        print(' Mode:                           Power spectrum of A channel')
    elif ADRmode == 4:
        print(' Mode:                           Power spectrum of B channel')
    elif ADRmode == 5:
        print(' Mode:                           Power spectra of A and B channels')
    elif ADRmode == 6:
        print(' Mode:                           A and B spectra correlation mode')
    else: 
        print(' Mode:                           Error detecting mode!!!')
        sys.exit('         Program stopped')
    
    TimeRes = NAvr * (16384. / F_ADC)
    df = F_ADC / FFT_Size                                
    print('\n Temporal resolution:           ', TimeRes, '  sec')
    print(' Real frequency resolution:     ', df, ' Hz \n')
    print(' Current position is', file.tell(), ' bytes \n')  # tells the position in the file

    file.seek(1024 - 2 * 26 - 16)
    print(' Current position is', file.tell(), ' bytes \n')   # tells the position in the file
    # temp = file.read(2 * 26 + 16).rstrip('\x00')                  # Checking if the place is empty
    print(' End of header (must be empty): ')
    temp = file.read(26).decode('utf-8').rstrip('\x00')
    print('  ', str(temp))
    temp = file.read(26).decode('utf-8').rstrip('\x00')
    print('  ', str(temp))
    temp = file.read(16).decode('utf-8').rstrip('\x00')
    print('  ', str(temp))
    print('  |****************|*********|')
    print('\n\n')
    
    file.seek(1024)
    # print 'Current position is', file.tell(), ' bytes' # tells the position in the file

    # *** DSP_INF reading ***
    temp = file.read(4)
    sizeOfChunk = struct.unpack('i', file.read(4))[0]
    frm_size = struct.unpack('i', file.read(4))[0]
    frm_count = struct.unpack('i', file.read(4))[0]
    frm_sec = struct.unpack('i', file.read(4))[0]
    frm_phase = struct.unpack('i', file.read(4))[0]
    AligningDSPINFtag = file.read(4072)
    
    # *** Setting the time reference (file beginning) ***
    TimeFirstFramePhase = float(frm_phase)/F_ADC
    TimeFirstFrameFloatSec = frm_sec + TimeFirstFramePhase
    TimeScaleStartTime = datetime(int('20' + df_filename[1:3]), int(df_filename[3:5]), int(df_filename[5:7]),
                                  int(df_creation_timeUTC[0:2]), int(df_creation_timeUTC[3:5]),
                                  int(df_creation_timeUTC[6:8]), int(df_creation_timeUTC[9:12]) * 1000)
    
    SpInFrame = frm_size / BlockSize
    FrameInChunk = int(sizeOfChunk / frm_size)
    ChunksInFile = ((df_filesize - 1024) / (sizeOfChunk+8))
    FramesInFile = ChunksInFile * FrameInChunk
    SpInFile = FramesInFile * SpInFrame         # Number of frequency points in specter 
    FreqPointsNum = Width * 1024                # Number of frequency points in specter

    print(' Number of spectra in frame:    ', SpInFrame)
    print(' Number of frames in chunk:     ', FrameInChunk)
    print(' Number of chunks in file:      ', ChunksInFile)
    print(' Number of frames in file:      ', FramesInFile)
    print(' Number of spectra in file:     ', SpInFile, '\n')
    print(' Header of the first data chunk: \n')
    print(' Data header:                   ', temp)
    print(' Size of data chunk:            ', sizeOfChunk, ' bytes')
    print(' Frame size:                    ', frm_size, ' bytes')
    print(' Frame count:                   ', frm_count)
    print(' Frame second:                  ', frm_sec)
    print(' Frame phase:                   ', frm_phase, '\n')

    file.seek(df_filesize - (sizeOfChunk + 8))  # Jumping to byte from file beginning
    
    # *** DSP_INF reading ***
    temp = file.read(4)
    sizeOfChunk = struct.unpack('i', file.read(4))[0]
    frm_size = struct.unpack('i', file.read(4))[0]
    frm_count = struct.unpack('i', file.read(4))[0]
    frm_sec = struct.unpack('i', file.read(4))[0]
    frm_phase = struct.unpack('i', file.read(4))[0]
    AligningDSPINFtag = file.read(4072)
    
    print(' Header of the last data chunk:')
    print(' Data header:                   ', temp)
    print(' Size of data chunk:            ', sizeOfChunk, ' bytes')
    print(' Frame size:                    ', frm_size, ' bytes')
    print(' Frame count:                   ', frm_count)
    print(' Frame second:                  ', frm_sec)
    print(' Frame phase:                   ', frm_phase, '\n')

    TimeCurrentFramePhase = float(frm_phase)/F_ADC
    TimeCurrentFrameFloatSec = frm_sec + TimeCurrentFramePhase
    TimeSecondDiff = TimeCurrentFrameFloatSec - TimeFirstFrameFloatSec
    TimeAdd = timedelta(0, int(np.fix(TimeSecondDiff)),
                        int(np.fix((TimeSecondDiff - int(np.fix(TimeSecondDiff))) * 1000000)))
    TimeOfLastChunk = TimeScaleStartTime + TimeAdd
                               
    print(' Time of first chunk:           ', TimeScaleStartTime)
    print(' Time of last chunk:            ', TimeOfLastChunk)
    print(' Time period of file (init):    ', TimeAdd)
    print(' Time period of file (calc):    ', (TimeOfLastChunk - TimeScaleStartTime), '\n')

    timeLengthOfFile = str(TimeAdd)
    if len(timeLengthOfFile) == 14:
        timeLengthOfFile = '  ' + timeLengthOfFile
    if len(timeLengthOfFile) == 15:
        timeLengthOfFile = ' ' + timeLengthOfFile
    
    # Checking if the place for time data is empty
    file.seek(1024 - 2 * 26 - 16)
    print(' Current position is', file.tell(), ' bytes \n')   # tells the position in the file
    print(' End of header (must be empty): ')
    temp = file.read(26).decode('utf-8').rstrip('\x00')
    print('  ', str(temp))
    temp = file.read(26).decode('utf-8').rstrip('\x00')
    print('  ', str(temp))
    temp = file.read(16).decode('utf-8').rstrip('\x00')
    print('  ', str(temp))
    print('  |****************|*********|')
    print('\n\n')

    checkConst = input('\n Enter "1" if the place is empty and you want to write time data there:  ')
    if len(checkConst) < 0 or checkConst != '1':
        print('\n\n\n         You have chosen not to change the file header!!! \n\n')
        sys.exit('\n                         Program stopped\n\n')

    # Writing time data to file header
    file.seek(1024 - 2 * 26 - 16)
    file.write(bytearray(str(TimeScaleStartTime), 'utf-8'))
    file.write(bytearray(str(TimeOfLastChunk), 'utf-8'))
    file.write(bytearray(str(timeLengthOfFile), 'utf-8'))

    print('\n\n Data have been written to the file \n\n')

    # Checking if the data was written correctly
    file.seek(1024 - 2 * 26 - 16)
    print(' Current position is', file.tell(), ' bytes \n\n')   # tells the position in the file
    print(' End of header ( new version ): ')
    temp = file.read(26).decode('utf-8').rstrip('\x00')
    print('  ', str(temp))
    temp = file.read(26).decode('utf-8').rstrip('\x00')
    print('  ', str(temp))
    temp = file.read(16).decode('utf-8').rstrip('\x00')
    print('  ', str(temp))
    print('  |****************|*********|')
    print('\n\n\n\n')
    
    file.close()

endTime = time.time()    # Time of calculations      

print('\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds')
print('\n\n\n    *** Program has finished! ***  \n\n\n')

