import numpy as np
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS


def jds_waveform_time(wf_data, clock_frequency, data_block_size):
    """
    Takes raw data from JDS waveform file and returns string array of time for each data block
    Input:
        wf_data - batch of WF data several blocks from file
        clock_frequency - clock frequency from file header
        data_block_size - size of data block
    Output:
        timeline_block_str - string array of time for each data block in batch
    """

    # The frequency meter of the receiver measures frequency roughly, usually the clock frequency comes
    #  from precision clock generator, so we round the measured frequency to exact 66 or 33 MHz

    clock_frequency = int(clock_frequency/10**6) * 10**6
    tmp_a = np.uint32(int('00000000000000000000000000000001', 2))  # To separate 1 bit of second part of second of the day
    tmp_b = np.uint32(int('00000111111111111111111111111111', 2))  # To separate 0-26 bits of phase of second
    tmp_c = np.uint32(int('00000000000000001111111111111111', 2))  # To separate 0-26 bits of phase of second

    second_of_day = np.uint32(np.bitwise_and(wf_data[-2, :], tmp_c)) + \
                    np.power(2, 16) * np.uint32(np.bitwise_and(wf_data[-1, :], tmp_a))

    phase_of_second = np.uint32(wf_data[data_block_size - 4, :])  # + \
                      # np.power(2, 16) * np.uint32(wf_data[data_block_size - 3, :])

    # DSP receivers have a bug, sometimes all the elder 16 bits have ones in the counter
    # To have correct time we check if the elder 16 bits are ones
    probe = np.uint32(np.bitwise_and(phase_of_second[:], int('11111111111111110000000000000000', 2)))
    # Here we simply apply mask to separate 26 bit of counter as suggested in DSP manual
    phase_of_second[:] = np.uint32(np.bitwise_and(phase_of_second[:], tmp_b))

    # If probe shows we have 16 bit of ones, we correct it which cutting out the elder 16 bits
    for k in range(len(probe)):
        if probe[k] == 4294901760:
            phase_of_second[k] = np.uint32(np.bitwise_and(phase_of_second[k],
                                                          int('00000000000000001111111111111111', 2)))

    hour = np.floor(second_of_day[:] / 3600)
    minutes = np.floor((second_of_day[:] % 3600) / 60)
    seconds = np.zeros(len(hour))
    for nt in range(len(hour)):
        seconds[nt] = second_of_day[nt] - (hour[nt] * 3600) - (minutes[nt] * 60) + \
                     (float(phase_of_second[nt]) / clock_frequency)

    hour[hour > 24] = 0
    minutes[minutes > 59] = 59
    seconds[seconds > 59] = 59

    timeline_block_str = ['' for x in range(len(hour))]
    for nt in range(len(hour)):
        timeline_block_str[nt] = ''.join("{:02.0f}".format(hour[nt])) + ':' + \
                                 ''.join("{:02.0f}".format(minutes[nt])) + \
                                ':' + ''.join("{:09.6f}".format(seconds[nt]))

    del hour, minutes, seconds, phase_of_second
    return timeline_block_str


if __name__ == '__main__':

    fname = 'DATA/E010621_090610.jds'

    print('\n\n Parameters of the file: ')

    # *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        CLCfrq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
        df, frequency, FreqPointsNum, data_block_size] = FileHeaderReaderJDS(fname, 0, 1)

    # *******************************************************************************
    #                           R E A D I N G   D A T A                             *
    # *******************************************************************************
    no_of_spectra_to_average = 64

    print('\n  *** Reading data from file *** \n')

    with open(fname, 'rb') as file:
        file.seek(1024)  # Jumping to 1024 byte from file beginning #
        for av_sp in range(1):

            # Reading and reshaping all data with readers
            wf_data = np.fromfile(file, dtype='i2', count=no_of_spectra_to_average * data_block_size)
            wf_data = np.reshape(wf_data, [data_block_size, no_of_spectra_to_average], order='F')

            time_block = jds_waveform_time(wf_data, CLCfrq, data_block_size)
            for i in range(len(time_block)):
                print(time_block[i])
