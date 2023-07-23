
import struct
import os
import sys
import math
import numpy as np
import datetime

################################################################################


def file_header_adr_read(filepath, start_byte, print_or_not):
    """
    Reads info from ADR (.adr) data file header and returns needed parameters to the main script
    Input parameters:
        filepath (str) - a path to the file to read data
        start_byte (int) - number of byte from which start reading
        print_or_not (bool) - to print the parameters to terminal or to real silently
    Output parameters:
        df_filename (str) - initial file name (when it was created)
        df_filesize (int) - file size in bytes
        df_system_name (str) - data file system name (receiver name)
        df_obs_place (str) - data file observatory name
        df_description (str) - data file description
        adc_freq (int) - ADC clock frequency (Hz)
        df_creation_time_utc
        adr_mode_txt
        adr_mode
        sum_diff_mode
        n_avr
        time_resolution - temporal resolution of data in the file in seconds
        fmin - minimal frequency of observations in MHz
        fmax - minimal frequency of observations in MHz
        freq_resolution - frequency resolution in Hz ???
        frequency - list of channels frequencies in MHz
        fft_size
        s_line
        width
        block_size
   """

    file = open(filepath, 'rb')
    file.seek(start_byte)  # Jump to the start of the header info
    header_bytes = file.read(1024)
    file.close()

    # Reading FHEADER
    df_filesize = os.stat(filepath).st_size                                     # Size of file
    df_filename = header_bytes[0:32].decode('utf-8').rstrip('\x00')
    df_creation_time_loc = header_bytes[32:56].decode('utf-8').rstrip('\x00')   # Creation time in local time
    # temp = file.read(8)
    df_creation_time_utc = header_bytes[64:96].decode('utf-8').rstrip('\x00')   # Creation time in UTC time
    df_system_name = header_bytes[96:128].decode('utf-8').rstrip('\x00')        # System (receiver) name
    df_obs_place = header_bytes[128:256].decode('utf-8').rstrip('\x00')         # place of observations
    try:
        df_description = header_bytes[256:512].decode('utf-8').rstrip('\x00')       # File description
    except UnicodeDecodeError:
        df_description = 'unreadable'

    # reading FHEADER PP ADRS_PAR
    adr_mode = struct.unpack('i', header_bytes[512:516])[0]
    fft_size = struct.unpack('i', header_bytes[516:520])[0]
    n_avr = struct.unpack('i', header_bytes[520:524])[0]
    s_line = struct.unpack('i', header_bytes[524:528])[0]
    width = struct.unpack('i', header_bytes[528:532])[0]
    block_size = struct.unpack('i', header_bytes[532:536])[0]
    adc_freq = struct.unpack('i', header_bytes[536:540])[0]

    # FHEADER PP ADRS_OPT
    size_of_struct = struct.unpack('i', header_bytes[540:544])[0]  # the size of ADRS_OPT structure
    start_stop_bit = struct.unpack('i', header_bytes[544:548])[0]  # starts/stops DSP data processing
    start_sec = struct.unpack('i', header_bytes[548:552])[0]       # UTC abs.time.sec - processing starts
    stop_sec = struct.unpack('i', header_bytes[552:556])[0]        # UTC abs.time.sec - processing stops
    test_mode = struct.unpack('i', header_bytes[556:560])[0]
    # Normalization coefficient 1-CH: 1 ... 65535 (k = n / 8192), 1 < n < 65536
    norm_c1 = struct.unpack('i', header_bytes[560:564])[0]       
    norm_c2 = struct.unpack('i', header_bytes[564:568])[0]      
    delay = struct.unpack('i', header_bytes[568:572])[0]           # Delay in picoseconds	-1000000000 ... 1000000000
    temp = struct.unpack('i', header_bytes[572:576])[0]
    # ADRSoptions = bin(temp)

    if print_or_not:
        print('\n Initial data file name:        ', df_filename)
        print(' File size:                     ', round(df_filesize/1024/1024, 3), ' Mb (', df_filesize, ' bytes )')
        print(' Creation time in local time:   ', str(df_creation_time_loc))
        print(' Creation time in UTC time:     ', df_creation_time_utc)
        print(' System (receiver) name:        ', df_system_name)
        print(' Place of observations:         ', df_obs_place)
        print(' File description:              ', df_description)
        print('\n ADR operation mode             ', adr_mode)
        print(' FFT size                       ', fft_size)
        print(' Averaged spectra               ', n_avr)
        print(' Start line number              ', s_line)
        print(' Width in lines                 ', width)
        print(' Block size                     ', block_size)
        print(' Clock frequency                ', adc_freq * 10**-6, ' MHz')
        print('\n Size of structure              ', size_of_struct)
        print(' Start and Stop                 ', start_stop_bit)
        print(' Start Second                   ', start_sec)
        print(' Stop Second                    ', stop_sec)
        print(' Test mode                      ', test_mode)
        print(' Norm coeff 1                   ', norm_c1)
        print(' Norm coeff 2                   ', norm_c2)
        print(' Digital delay                  ', delay, 'picoseconds \n')

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
        if print_or_not:
            print(' Sum mode switch:                On')
        sum_diff_mode = ' Sum/diff mode'
    else:
        if print_or_not:
            print (' Sum mode switch:                Off')
        sum_diff_mode = ''

    if adr_mode == 0:
        if print_or_not:
            print('\n Mode:                           Waveform A channel')
        adr_mode_txt = 'Waveform mode'
    elif adr_mode == 1:
        if print_or_not:
            print('\n Mode:                           Waveform B channel')
        adr_mode_txt = 'Waveform mode'
    elif adr_mode == 2:
        if print_or_not:
            print('\n Mode:                           Waveform A and B channels')
        adr_mode_txt = 'Waveform mode'
    elif adr_mode == 3:
        if print_or_not:
            print('\n Mode:                           Power spectrum of A channel')
        adr_mode_txt = 'Spectra mode'
    elif adr_mode == 4:
        if print_or_not:
            print('\n Mode:                           Power spectrum of B channel')
        adr_mode_txt = 'Spectra mode'
    elif adr_mode == 5:
        if print_or_not:
            print('\n Mode:                           Power spectra of A and B channels')
        adr_mode_txt = 'Spectra mode'
    elif adr_mode == 6:
        if print_or_not:
            print('\n Mode:                           A and B spectra correlation mode')
        adr_mode_txt = 'Correlation mode'
    else:
        print('\n Mode:                           Error detecting mode!!!')
        sys.exit('         Program stopped')

    # *** Time resolution ***
    time_resolution = n_avr * (fft_size / float(adc_freq))
    if print_or_not:
        print('\n Time resolution:               ', round(time_resolution * 1000, 3), '  ms')

    # *** Frequency calculation (in MHz) ***
    freq_resolution = adc_freq / fft_size
    freq_points_num = int(width * 1024)                # Number of frequency points in specter
    f0 = (s_line * 1024 * freq_resolution)
    frequency = [0 for col in range(freq_points_num)]
    for i in range(0, freq_points_num):
        frequency[i] = (f0 + (i * freq_resolution)) * (10**-6)

    if print_or_not:
        print(' Real frequency resolution:     ', round(freq_resolution/1000., 3), ' kHz')
        print(' Frequency band:                ', round(frequency[0], 3), ' - ',
              round(frequency[-1] + (freq_resolution/pow(10, 6)), 3), ' MHz \n')
        print('')

    return df_filename, df_filesize, df_system_name, df_obs_place, df_description, adc_freq, df_creation_time_utc, \
           adr_mode_txt, adr_mode, sum_diff_mode, n_avr, time_resolution, frequency[0], frequency[-1], \
           freq_resolution, frequency, fft_size, s_line, width, block_size


def file_header_adr_read_old(filepath, start_byte, print_or_not):
    """
    !!! Deprecated as uses a lot of file read operations instead of one !!!
    Reads info from ADR (.adr) data file header and returns needed parameters to the main script
    Input parameters:
        filepath - a path to the file to read data
        start_byte - number of byte from which start reading
        print_or_not - to print the parameters to terminal or to real silently
    Output parameters:
        TimeRes - temporal resolution of data in the file in seconds
        fmin - minimal frequency of observations in MHz
        fmax - minimal frequency of observations in MHz
        df - frequency resolution in Hz ???
        frequencyList0 - list of channels frequencies in MHz
        Width*1024 - number of frequency points i.e. ( len(frequency) )
    """

    file = open(filepath, 'rb')
    file.seek(start_byte) # Jump to the start of the header info

    # reading FHEADER
    df_filesize = (os.stat(filepath).st_size)                            # Size of file
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
    size_of_struct = struct.unpack('i', file.read(4))[0]   # the size of ADRS_OPT structure
    StartStop = struct.unpack('i', file.read(4))[0]         # starts/stops DSP data processing
    StartSec = struct.unpack('i', file.read(4))[0];         # UTC abs.time.sec - processing starts
    StopSec = struct.unpack('i', file.read(4))[0];          # UTC abs.time.sec - processing stops
    Testmode = struct.unpack('i', file.read(4))[0];
    NormCoeff1 = struct.unpack('i', file.read(4))[0];       # Normalization coefficient 1-CH: 1 ... 65535 (k = n / 8192), 1 < n < 65536
    NormCoeff2 = struct.unpack('i', file.read(4))[0];       # Normalization coefficient 2-CH: 1 ... 65535 (k = n / 8192), 1 < n < 65536
    Delay = struct.unpack('i', file.read(4))[0];            # Delay in picoseconds	-1000000000 ... 1000000000
    temp = struct.unpack('i', file.read(4))[0];
    ADRSoptions = bin(temp)

    if (print_or_not == 1):
        print ('')
        print (' Initial data file name:        ', df_filename)
        print (' File size:                     ', round(df_filesize/1024/1024, 3), ' Mb (',df_filesize, ' bytes )')
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
        print (' Size of structure              ', size_of_struct)
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
        if (print_or_not == 1): print (' Sum mode switch:                On')
        sumDifMode = ' Sum/diff mode'
    else:
        if (print_or_not == 1): print (' Sum mode switch:                Off')
        sumDifMode = ''

    if (print_or_not == 1):
        print (' ')

    if ADRmode == 0:
        if (print_or_not == 1): print (' Mode:                           Waveform A channel')
        ReceiverMode = 'Waveform mode'
    elif ADRmode == 1:
        if (print_or_not == 1): print (' Mode:                           Waveform B channel')
        ReceiverMode = 'Waveform mode'
    elif ADRmode == 2:
        if (print_or_not == 1): print (' Mode:                           Waveform A and B channels')
        ReceiverMode = 'Waveform mode'
    elif ADRmode == 3:
        if (print_or_not == 1): print (' Mode:                           Power spectrum of A channel')
        ReceiverMode = 'Spectra mode'
    elif ADRmode == 4:
        if (print_or_not == 1): print (' Mode:                           Power spectrum of B channel')
        ReceiverMode = 'Spectra mode'
    elif ADRmode == 5:
        if (print_or_not == 1): print (' Mode:                           Power spectra of A and B channels')
        ReceiverMode = 'Spectra mode'
    elif ADRmode == 6:
        if (print_or_not == 1): print (' Mode:                           A and B spectra correlation mode')
        ReceiverMode = 'Correlation mode'
    else:
        print (' Mode:                           Error detecting mode!!!')
        sys.exit('         Program stopped')

    if (print_or_not == 1): print ('')


    # *** Time resolution ***
    TimeRes = NAvr * (FFT_Size / float(F_ADC));
    if (print_or_not == 1): print (' Time resolution:               ', round(TimeRes*1000, 3), '  ms')

    # *** Frequncy calculation (in MHz) ***
    df = F_ADC / FFT_Size
    FreqPointsNum = int(Width * 1024)                # Number of frequency points in specter
    f0 = (SLine * 1024 * df)
    frequency = [0 for col in range(FreqPointsNum)]
    for i in range (0, FreqPointsNum):
        frequency[i] = (f0 + (i * df)) * (10**-6)

    if (print_or_not == 1):
        print (' Real frequency resolution:     ', round(df/1000., 3), ' kHz')
        print (' Frequency band:                ', round(frequency[0],3), ' - ', round(frequency[FreqPointsNum-1]+(df/pow(10,6)),3), ' MHz')
        print ('')

    file.close()

    return df_filename, df_filesize, df_system_name, df_obs_place, df_description, F_ADC, df_creation_timeUTC, ReceiverMode, ADRmode, sumDifMode, NAvr, TimeRes, frequency[0], frequency[FreqPointsNum-1], df, frequency, FFT_Size, SLine, Width, BlockSize


################################################################################

def chunk_header_reader_adr(filepath, start_byte, block_size, print_or_not):
    """
    Reads info from ADR (.adr) data file from chunk headerand returns parameters to the main script
    Input parameters:
        filepath - a path to the file to read data
        start_byte - number of byte from which starts the heaer of ADR file (for now always 0)
    Output parameters:
        SpInFile -
        SpInFrame -
        FrameInChunk -
        ChunksInFile -
        sizeOfChunk -
        frm_sec -
        frm_phase -
    """

    df_filesize = os.stat(filepath).st_size                            # Size of file

    file = open(filepath, 'rb')
    file.seek(start_byte + 1024)  # Jump to the start of the header info
    header_bytes = file.read(4096)
    file.close()

    # *** DSP_INF reading ***
    temp = header_bytes[0:4].decode('utf-8')                 # Header of the chunk
    sizeOfChunk = struct.unpack('i', header_bytes[4:8])[0]
    frm_size = struct.unpack('i', header_bytes[8:12])[0]
    frm_count = struct.unpack('i', header_bytes[12:16])[0]
    frm_sec = struct.unpack('i', header_bytes[16:20])[0]
    frm_phase = struct.unpack('i', header_bytes[20:24])[0]

    if print_or_not:
        print('\n Data header:                   ', temp)
        print(' Size of data chunk:            ', sizeOfChunk, ' bytes')
        print(' Frame size:                    ', frm_size, ' bytes')
        print(' Frame count:                   ', frm_count)
        print(' Frame second:                  ', frm_sec)
        print(' Frame phase:                   ', frm_phase, ' \n')

    sp_in_frame = int(frm_size / block_size)
    frame_in_chunk = int(sizeOfChunk / frm_size)
    chunks_in_file = int(((df_filesize - 1024) / (sizeOfChunk+8)))
    frames_in_file = int(chunks_in_file * frame_in_chunk)
    sp_in_file = frames_in_file * sp_in_frame
    if print_or_not:
        print(' Number of spectra in frame:    ', sp_in_frame)
        print(' Number of frames in chunk:     ', frame_in_chunk)
        print(' Number of chunks in file:      ', chunks_in_file)
        print(' Number of frames in file:      ', frames_in_file)
        print(' Number of spectra in file:     ', sp_in_file, ' \n')
    file.close()

    return sp_in_file, sp_in_frame, frame_in_chunk, chunks_in_file, sizeOfChunk, frm_sec, frm_phase


################################################################################


if __name__ == '__main__':

    filename = '../../RA_DATA_ARCHIVE/ADR_GURT_typical_Sun_data_J_burst/A200605_084324.adr'

    print('\n\n * Parameters of the file: ')

    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        F_ADC, df_creation_timeUTC, ReceiverMode, ADRmode, sumDifMode,
        NAvr, TimeRes, fmin, fmax, df, frequencyList0,
        FFTsize, SLine, Width, block_size] = file_header_adr_read(filename, 0, True)

    print('\n\n * Parameters of the chunk in data file: ')

    SpInFile, SpInFrame, FrameInChunk, ChunksInFile, sizeOfChunk,\
        frm_sec, frm_phase = chunk_header_reader_adr(filename, 0, block_size, True)
