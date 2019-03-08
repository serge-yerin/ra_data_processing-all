'''
'''

import struct
import os
import math
import numpy as np

def FileHeaderReaderADR(file):
    '''
    Reads info from ADR (.adr) data file header and returns needed parameters to the main script
    Input parameters:
        file - a handle of opened in main script file to read data
    Output parameters:
        TimeRes - temporal resolution of data in the file in seconds
        fmin - minimal frequency of observations in MHz
        fmax - minimal frequency of observations in MHz
        df - frequyency resolution in Hz ???
        frequencyList0 - list of channels frequencies in MHz
        Width*1024 - number of frequency points i.e. ( len(frequency) )
    '''
    

    # reading FHEADER
    #df_filesize = (os.stat(filename).st_size)                            # Size of file

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
    SizeOfStructure = struct.unpack('i', file.read(4))[0]   # the size of ADRS_OPT structure
    StartStop = struct.unpack('i', file.read(4))[0]         # starts/stops DSP data processing
    StartSec = struct.unpack('i', file.read(4))[0];         # UTC abs.time.sec - processing starts
    StopSec = struct.unpack('i', file.read(4))[0];          # UTC abs.time.sec - processing stops
    Testmode = struct.unpack('i', file.read(4))[0];         
    NormCoeff1 = struct.unpack('i', file.read(4))[0];       # Normalization coefficient 1-CH: 1 ... 65535 (k = n / 8192), 1 < n < 65536
    NormCoeff2 = struct.unpack('i', file.read(4))[0];       # Normalization coefficient 2-CH: 1 ... 65535 (k = n / 8192), 1 < n < 65536
    Delay = struct.unpack('i', file.read(4))[0];            # Delay in picoseconds	-1000000000 ... 1000000000
    temp = struct.unpack('i', file.read(4))[0];
    ADRSoptions = bin(temp) 

    print ('')
    print (' Initial data file name:        ', df_filename)
    #print (' File size:                     ', round(df_filesize/1024/1024, 3), ' Mb (',df_filesize, ' bytes )')
    print (' Creation time in local time:   ', str(df_creation_timeLOC))
    print (' Creation time in UTC time:     ', df_creation_timeUTC)
    print (' System (receiver) name:        ', df_system_name)
    print (' Place of observations:         ', df_obs_place)
    print (' File description:              ', df_description)
    print ('')
    print (' ADR operation mode             ', ADRmode)
    print (' FFT size                       ', FFT_Size)
    print (' Averaged spectra               ', NAvr)
    print (' Start line number              ', SLine)
    print (' Width in lines                 ', Width)
    print (' Block size                     ', BlockSize)
    print (' Clock frequency                ', F_ADC*10**-6 , ' MHz')
    print ('')
    print (' Size of structure              ', SizeOfStructure)
    print (' Start and Stop                 ', StartStop)
    print (' Start Second                   ', StartSec)
    print (' Stop Second                    ', StopSec)
    print (' Testmode                       ', Testmode)
    print (' Norm coeff 1                   ', NormCoeff1)
    print (' Norm coeff 2                   ', NormCoeff2)
    print (' Digital delay                  ', Delay)
    print ('')

    if (int(temp) & int('1000')) == 8: print (' Start by sec:                   Yes')
    else: print (' Start by sec:                   No')
    if (int(temp) & int('0100')) == 4: print (' CLC:                            External')
    else: print (' CLC:                            Internal')
    if (int(temp) & int('0010')) == 2: print (' FFT Window type:                Rectangle')
    else: print (' FFT Window type:                Hanning')    
    if (int(temp) & int('0001')) == 1: 
        print (' Sum mode switch:                On')
        sumDifMode = ' Sum/diff mode'
    else: 
        print (' Sum mode switch:                Off')
        sumDifMode = ''
    print (' ')
    
    if ADRmode == 0:   
        print (' Mode:                           Waveform A channel')
    elif ADRmode == 1: 
        print (' Mode:                           Waveform B channel')
    elif ADRmode == 2: 
        print (' Mode:                           Waveform A and B channels')
    elif ADRmode == 3: 
        print (' Mode:                           Power spectrum of A channel')
        ReceiverMode = 'Spectra mode'
    elif ADRmode == 4: 
        print (' Mode:                           Power spectrum of B channel')
        ReceiverMode = 'Spectra mode'
    elif ADRmode == 5: 
        print (' Mode:                           Power spectra of A and B channels')
        ReceiverMode = 'Spectra mode'
    elif ADRmode == 6: 
        print (' Mode:                           A and B spectra correlation mode')
        ReceiverMode = 'Correlation mode'
    else: 
        print (' Mode:                           Error detecting mode!!!')
        sys.exit('         Program stopped')
    
    print ('')
    
    
    
    TimeRes = NAvr * (16384. / F_ADC);
    df = F_ADC / FFT_Size                                
    print (' Time resolution:               ', round(TimeRes*1000, 3), '  ms')
    print (' Real frequency resolution:     ', round(df/1000, 3), ' kHz')
    print ('')
    
    # *** Frequncy calculation (in MHz) ***
    fmin = ((SLine) * 1024. * df)/10**6
    fmax = ((SLine + Width) * 1024. * df)/10**6
    df = df * math.pow(10, -6)
    print (' Lower frequency bounnd:        ', fmin, ' MHz')
    print (' Higher frequency bounnd:       ', fmax, ' MHz')
    for i in range (3): print (' ')
    frequencyList0 = [0 for col in range(Width * 1024)]
    for i in range (0, Width * 1024):
        frequencyList0[i] = (fmin + ((i+1) * df))
    
    return TimeRes, fmin, fmax, df, frequencyList0, Width*1024
    
    
    
    
if __name__ == '__main__':
    
    filename = 'd:/PYTHON/ra_data_processing-all/DATA/A170712_160219.adr'
    
    print('\n\n Parameters of the file: ')
    
    with open(filename, 'rb') as file:
        
        FileHeaderReaderADR(file)
        
        
        
        
        
        
