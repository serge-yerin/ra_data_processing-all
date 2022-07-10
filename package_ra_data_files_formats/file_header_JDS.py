
import struct
import os
import numpy as np


def FileHeaderReaderJDS(filepath, start_byte, print_or_not):
    """
    Reads info from DSP (.jds) data file header and returns needed parameters to main script
    Input parameters:
        filepath - a path to the file to read data
        start_byte - number of byte from which start reading
        print_or_not - to print the parameters to terminal or to real silently
    Output parameters:
        time_res - temporal resolution of data in the file in seconds
        fmin - minimal frequency of observations in MHz
        fmax - minimal frequency of observations in MHz
        df / pow(10,6) - frequyency resolution in MHz
        frequency - list of channels frequencies in MHz
        Wb - number of frequency points i.e. ( len(frequency) )
    """

    file = open(filepath, 'rb')
    file.seek(start_byte)  # Jump to the start of the header info

    # reading FHEADER
    df_filesize = os.stat(filepath).st_size                              # Size of file
    df_filename = file.read(32).decode('utf-8').rstrip('\x00')           # Initial data file name
    df_creation_timeLOC = file.read(32).decode('utf-8').rstrip('\x00')   # Creation time in local time
    df_creation_timeUTC = file.read(32).decode('utf-8').rstrip('\x00')   # Creation time in UTC time
    df_system_name = file.read(32).decode('utf-8').rstrip('\x00')        # System (receiver) name
    df_UTC_time = np.fromfile(file, dtype=np.uint16, count=8)
    df_system_time = file.read(16).decode('utf-8').rstrip('\x00')        # System (receiver) time UTC
    df_obs_place = file.read(96).decode('utf-8').rstrip('\x00')          # place of observations
    df_description = file.read(256).decode('utf-8').rstrip('\x00')       # File description
    if print_or_not == 1:
        print('')
        print(' Initial data file name:        ', df_filename)
        print(' File size:                     ', round(df_filesize/1024/1024, 3), ' Mb (', df_filesize, ' bytes )')
        print(' Creation time in local time:   ', str(df_creation_timeLOC.rstrip()))
        print(' Creation time in UTC time:     ', df_creation_timeUTC)
        print(' System (receiver) name:        ', df_system_name)
        print(' System (receiver) UTC:         ', df_UTC_time[0], '/', df_UTC_time[1], '/', df_UTC_time[3], ' ',
              df_UTC_time[4], ':', df_UTC_time[5], ':', df_UTC_time[6], ',', df_UTC_time[7])
        print(' System (receiver) time:        ', df_system_time)
        print(' Place of observations:         ', df_obs_place)
        print(' File description:              ', df_description, ' \n')

    # *** Parameters that are poor described in file format specification ***
    # reading FHEADER PP and DSPP0 ((16+5)*32 bit)
    dsp_mode = np.fromfile(file, dtype=np.uint16, count=1)

    # mode = int(dsp_mode & 7)
    # CHselect = np.right_shift(dsp_mode & 32, 5)
    # opmode = np.right_shift(dsp_mode & 64, 6)
    # FFTwindow = np.right_shift(dsp_mode & 128, 7)
    # DCrem = np.right_shift(dsp_mode & 256, 8)
    # Clock = np.right_shift(dsp_mode & 512, 9)
    # ChAon = np.right_shift(dsp_mode & 1024, 10)
    # ChBon = np.right_shift(dsp_mode & 2048, 11)
    # SynchroStart = np.right_shift(dsp_mode & 4096, 12)
    # waitGPS = np.right_shift(dsp_mode & 8192, 13)
    # extWeight = np.right_shift(dsp_mode & 16384, 14)
    # DMAinter = np.right_shift((dsp_mode & 2147483648), 31)

    data_block_size = struct.unpack('i', file.read(4))[0]  # No info

    # Only for test recordings of new receiver
    if data_block_size == 0:
        data_block_size = 16384

    if print_or_not == 1:
        print(' Data block size:               ', data_block_size)

    prcmode = struct.unpack('i', file.read(4))[0]

    # NAvr = (prcmode & 4095) + 1
    # SLine = np.right_shift((prcmode & 458752), 16)
    # Width = np.right_shift((prcmode & 7340032), 19)
    testGen = struct.unpack('i', file.read(4))[0]  # No info
    clc     = struct.unpack('i', file.read(4))[0]  # No info
    fftsize = struct.unpack('i', file.read(4))[0]
    temp = file.read(40)  # No info
    fft_size   = struct.unpack('i', file.read(4))[0]  # FFT size
    MinDSPSize = struct.unpack('i', file.read(4))[0]
    MinDMASize = struct.unpack('i', file.read(4))[0]
    DMASizeCnt = struct.unpack('i', file.read(4))[0]
    DMASize    = struct.unpack('i', file.read(4))[0]
    temp = file.read(2)       # Skipping

    # *** Parameters that are well described in file format specification ***

    clock_freq = struct.unpack('f', file.read(4))[0]  #
    Synch      = struct.unpack('i', file.read(4))[0]  #
    SSht       = struct.unpack('i', file.read(4))[0]  #
    mode       = struct.unpack('i', file.read(4))[0]  #
    Wch        = struct.unpack('i', file.read(4))[0]  #
    Smd        = struct.unpack('i', file.read(4))[0]  #
    Offt       = struct.unpack('i', file.read(4))[0]  #
    Lb         = struct.unpack('i', file.read(4))[0]  #
    Hb         = struct.unpack('i', file.read(4))[0]  #
    Wb         = struct.unpack('i', file.read(4))[0]  #
    Navr       = struct.unpack('i', file.read(4))[0]  #
    CAvr       = struct.unpack('i', file.read(4))[0]  #
    Weight     = struct.unpack('i', file.read(4))[0]  #
    DCRem      = struct.unpack('i', file.read(4))[0]  #
    ExtSyn     = struct.unpack('i', file.read(4))[0]  #
    Ch1        = struct.unpack('i', file.read(4))[0]  #
    Ch2        = struct.unpack('i', file.read(4))[0]  #
    ExtWin     = struct.unpack('i', file.read(4))[0]  #
    Clip       = struct.unpack('i', file.read(4))[0]  #
    HPF0       = struct.unpack('i', file.read(4))[0]  #
    HPF1       = struct.unpack('i', file.read(4))[0]  #
    LPF0       = struct.unpack('i', file.read(4))[0]  #
    LPF1       = struct.unpack('i', file.read(4))[0]  #
    ATT0       = struct.unpack('i', file.read(4))[0]  #
    ATT1       = struct.unpack('i', file.read(4))[0]  #

    df_softname = file.read(16).decode('utf-8').rstrip('\x00')       #
    df_softvers = file.read(16).decode('utf-8').rstrip('\x00')       #
    df_dsp_vers = file.read(32).decode('utf-8').rstrip('\x00')       #

    # Only for test recordings of new receiver
    if clock_freq == 0.0:
        clock_freq = 80000000.0
    if Hb == 0:
        Hb = 8192
    if Wb == 0:
        Wb = 8192

    if print_or_not == 1:
        print('')
        if mode == 0:
            print(' mode:                           Waveform')
            if Wch == 0:
                print(' Channel:                        A')
            if Wch == 1:
                print(' Channel:                        B')
            if Wch == 2:
                print(' Channels                        A & B')
        if mode == 1:
            print(' mode:                           Spectra A & B')
        if mode == 2:
            print(' mode:                           Correlation A & B')

        print(' Sampling ADC frequency:        ', clock_freq / 10**6, ' MHz')
        if ExtSyn == 0:
            print(' Synchronization:                Internal')
        if ExtSyn == 1:
            print(' Synchronization:                External')
        print(' GPS synchronization (0-On):    ', Synch)
        if mode == 0:
            print(' Navr:                          ', Navr, '\n\n')
            if Navr == 2:
                print(' Data records:                   without time gaps \n\n')
            else:
                print(' Data records:                   probable time gaps \n\n')
        else:
            print(' Number of averaged spectra:    ', Navr, '\n\n')

        if mode == 0:
            print(' IN WAVEFORM mode FREQUENCY AND TIME PARAMETERS DO NOT HAVE SENSE !')
            print(' They are listed here just to show all possible parameters of file \n\n')

        print(' Snap shot mode (always 1):     ', SSht)
        print(' Smd:                           ', Smd)
        print(' Offt:                          ', Offt)
        print(' FFT size                       ', fft_size)
        print(' Lowest channel number:         ', Lb)
        print(' Highest channel number:        ', Hb)
        print(' Number of channels:            ', Wb)
        print(' CAvr:                          ', CAvr)
        if Weight == 0: print(' Weightning window:              On')
        if Weight == 1: print(' Weightning window:              Off')
        if DCRem == 0:  print(' DC removing:                    No')
        if DCRem == 1:  print(' DC removing:                    Yes')
        if Ch1 == 0:    print(' Channel 1:                      On')
        if Ch1 == 1:    print(' Channel 1:                      Off')
        if Ch2 == 0:    print(' Channel 2:                      On')
        if Ch2 == 1:    print(' Channel 2:                      Off')
        if ExtWin == 0: print(' External FFT window:            No')
        if ExtWin == 1: print(' External FFT window:            Yes')
        print(' Clip:                          ', Clip)
        print(' HPF0:                          ', HPF0)
        print(' HPF1:                          ', HPF1)
        print(' LPF0:                          ', LPF0)
        print(' LPF1:                          ', LPF1)
        print(' ATT0:                          ', ATT0)
        print(' ATT1:                          ', ATT1)

        print(' Software name:                 ', df_softname)
        print(' Software version:              ', df_softvers)
        print(' DSP soft version:              ', df_dsp_vers)
        print('\n')

    # Receiver developers made NAvr = 2 for single spectrum, so for waveform we correct the value:
    # if mode == 0:   # For waveform mode correct NAvr = 2
    #    Navr = 2
    if Navr == 0:
        Navr = 2

    # *** Temporal and frequency resolutions ***
    if fft_size < 1:
        fft_size = 16384.0
    # else:
    #    Sfft = float(fft_size/2)
    time_res = Navr * (fft_size / clock_freq / 2)
    df = float((float(clock_freq) / 2) / float(fft_size / 2))
    # df = float((float(clock_freq) / 2.0 / float(Sfft) ))
    if print_or_not == 1:
        print(' Temporal resolution:           ', round((time_res*1000), 3), '  ms')
        print(' Real frequency resolution:     ', round((df/1000), 3), ' kHz')

    # *** Frequency calculation (in MHz) ***
    f0 = Lb * df
    freq_points_num = Wb
    frequency = [0 for col in range(freq_points_num)]
    for i in range(0, freq_points_num):
        frequency[i] = (f0 + (i * df)) * (10**-6)

    fmin = round(frequency[0], 3)
    fmax = round(frequency[freq_points_num-1] + (df / pow(10, 6)), 3)
    if print_or_not == 1:
        print(' Frequency band:                ', fmin, ' - ', fmax, ' MHz \n')

    file.close()

    if mode == 0:
        sp_in_file = Wch
        receiver_mode = 'Waveform mode'
    if mode == 1:
        sp_in_file = int(df_filesize - 1024) / (2 * 4 * freq_points_num)  # Number of frequency points in specter
        receiver_mode = 'Spectra mode'
    if mode == 2:
        sp_in_file = int(df_filesize - 1024) / (4 * 4 * freq_points_num)  # Number of frequency points in specter
        receiver_mode = 'Correlation mode'
    if mode == 1 or mode == 2:
        if print_or_not == 1:
            print('\n Number of JDS spectra in file:     ', sp_in_file, '\n\n')

    return df_filename, df_filesize, df_system_name, df_obs_place, df_description, clock_freq, df_creation_timeUTC, \
           sp_in_file, receiver_mode, mode, Navr, time_res, fmin, fmax, df, frequency, Wb, data_block_size


if __name__ == '__main__':

    filename = '../RA_DATA_ARCHIVE/DSP_waveform_66_MHz_B0950p08/E220213_201439.jds'

    print('\n\n Parameters of the file: ')

    FileHeaderReaderJDS(filename, 0, 1)
