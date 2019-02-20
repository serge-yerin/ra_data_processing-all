'''
'''
import struct
import os
import numpy as np

def FileHeaderReaderDSP(filename, file):
    '''
    Reads info from ADR data file header and returnt needed parameters
    '''
    
    # reading FHEADER
    df_filesize = (os.stat(filename).st_size)                               # Size of file
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
    CHselect = np.right_shift (DSPmode & 32, 5)
    opMode = np.right_shift (DSPmode & 64, 6)
    FFTwindow = np.right_shift (DSPmode & 128, 7)
    DCrem = np.right_shift (DSPmode & 256, 8)
    Clock = np.right_shift (DSPmode & 512, 9)    
    ChAon = np.right_shift (DSPmode & 1024, 10)
    ChBon = np.right_shift (DSPmode & 2048, 11)    
    SynchroStart = np.right_shift (DSPmode & 4096, 12)    
    waitGPS = np.right_shift (DSPmode & 8192, 13)
    extWeight = np.right_shift (DSPmode & 16384, 14)    
    DMAinter = np.right_shift ((DSPmode & 2147483648), 31) 
    
    dataBlockSize = struct.unpack('i', file.read(4))[0] # No info
    print (' Data block size:               ', dataBlockSize)
    
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
    
    
    print ('\n')
        
        
    # *** Temporal and frequency resolutions ***
    Sfft = 8192.0
    TimeRes = Navr * (Sfft / CLCfrq);
    df = float((float(CLCfrq) / 2.0 / float(Sfft) ))
    print (' Temporal resolution:           ', round((TimeRes*1000),3), '  ms')
    print (' Real frequency resolution:     ', round((df/1000),3), ' kHz')
    
 
    # *** Frequncy calculation (in MHz) ***
    f0 = (Lb * df)
    FreqPointsNum = Wb
    frequency = [0 for col in range(FreqPointsNum)]
    for i in range (0, FreqPointsNum):
        frequency[i] = (f0 + (i * df)) * (10**-6)    
        
    fmin = round(frequency[0],3)
    fmax = round(frequency[FreqPointsNum-1]+(df/pow(10,6)),3)
    print (' Frequency band:                ', fmin, ' - ', fmax, ' MHz')
    print ('')    
     
    
    return TimeRes, fmin, fmax, df / pow(10,6), frequency, Wb
    
