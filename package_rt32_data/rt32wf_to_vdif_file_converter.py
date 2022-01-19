# Python3
Software_version = '2022.01.19'
Software_name = 'RT-32 Zolochiv waveform reader and converter to vdif'
# Script intended to read, show and analyze data from MARK5 receiver
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
directory = '../RA_DATA_ARCHIVE/RT-32_Zolochiv_waveform_first_sample/'
filename = 'A210612_075610_rt32_waveform_first_sample.adr'
filepath = directory + filename
result_path = ''

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import sys
import numpy as np
from os import path
import time
# import matplotlib.pyplot as plt
from matplotlib import pylab as plt
import os
import matplotlib
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import *
matplotlib.use('TkAgg')

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_rt32_data.rt32_zolochiv_waveform_reader import rpr_wf_header_reader_dict


def word_to_bytearray(word):
    """
    The function converts formed 4 byte unsigned integers (words) to bytearray of 4 bytes
    """
    ones_byte = int('11111111', 2)
    byte_0 = ones_byte & word
    byte_1 = ones_byte & word >> 8
    byte_2 = ones_byte & word >> 16
    byte_3 = ones_byte & word >> 24
    word_bytearray = bytearray([byte_3, byte_2, byte_1, byte_0])
    return word_bytearray


def big_to_little_endian(data_bytearray):
    """
    The function takes input bytearray data type and returns little endian encoded bytearray
    """
    for offset in range(0, len(data_bytearray), 4):
        chunk = data_bytearray[offset:offset + 4]
        if len(chunk) != 4:
            raise ValueError('alignment error')
        data_bytearray[offset:offset + 4] = chunk[::-1]
    return data_bytearray


# Forming the word from values
def int8_to_32_bit_word(v_int_1, v_int_2, v_int_3, v_int_4):
    """
    The function takes 4 uint8 or int8 values and form a 32 bit word
    (actually can be changed by appropriate array operations)
    """
    if 0 > v_int_1 > 256 or 0 > v_int_2 > 256 or 0 > v_int_3 > 256 or 0 > v_int_4 > 256:
        raise ValueError('\n\n      Error! Invalid value!  \n\n')
    byte_4 = v_int_4 << 24
    byte_3 = v_int_3 << 16
    byte_2 = v_int_2 << 8
    word = byte_4 | byte_3 | byte_2 | v_int_1
    word_bytearray = word_to_bytearray(word)
    return word_bytearray


def change_thread_id_in_header(a_vdif_header, thread_id):
    """
    The function changes the thread_id in bytearray header to specified number
    a_vdif_header - the bytearray header to change the thread_id
    thread_id - integer number of the thread_in from 0 to 1023!
    at the output we have the header with changed thread_id
    """

    # current thread id in header:
    data_2_bytes = int.from_bytes(a_vdif_header[12:14], byteorder='big', signed=False)
    # mask_1 = int('0000001111111111', 2)
    mask_2 = int('1111110000000000', 2)
    # t_id = (mask_1 & data_2_bytes)  # t_id = (mask & data_2_bytes) >> 16
    # print(' Tread:', t_id)
    part_without_changes = (mask_2 & data_2_bytes)
    word_2_bytes = part_without_changes | thread_id
    # Convert 2 byte number to separate bytes and save to header bytearray
    ones_byte = int('11111111', 2)
    byte_0 = ones_byte & word_2_bytes
    byte_1 = ones_byte & word_2_bytes >> 8
    a_vdif_header[12:14] = bytearray([byte_1, byte_0])

    # # Code to check the thread_id in header
    # t_id = int.from_bytes(a_vdif_header[12:14], byteorder='big', signed=False)
    # print(' Read bytes:', t_id)
    # mask_1 = int('0000001111111111', 2)
    # t_id = (mask_1 & t_id)
    # print(' Tread:', t_id)

    return a_vdif_header


def change_data_frame_no_in_header(a_vdif_header, a_data_frame_no):
    """
    The function changes the data frame number within second in bytearray header to specified number
    a_vdif_header - the bytearray header to change the thread_id
    a_data_frame_no - integer number of the data frame within second less then 8388607
    at the output we have the header with changed a_data_frame_no
    """

    # current data frame number within second in header:
    data_4_bytes = int.from_bytes(a_vdif_header[4:8], byteorder='big', signed=False)
    # mask_1 = int('00000000111111111111111111111111', 2)
    mask_2 = int('11111111000000000000000000000000', 2)
    # current_frame_no = (mask_1 & data_4_bytes)
    # print(' Current frame number within second:', current_frame_no)
    part_without_changes = (mask_2 & data_4_bytes)
    word_4_bytes = part_without_changes | a_data_frame_no
    a_vdif_header[4:8] = word_to_bytearray(word_4_bytes)

    # # Code to check the data frame number within second in header
    # data_4_bytes = int.from_bytes(a_vdif_header[4:8], byteorder='big', signed=False)
    # current_frame_no = (mask_1 & data_4_bytes)
    # print(' Current frame number: ', current_frame_no)

    return a_vdif_header


def change_secs_from_ref_epoch_in_header(a_vdif_header, a_sec_from_ref_epoch):
    """
    The function changes the second from reference epoch number in bytearray header to specified number
    a_vdif_header - the bytearray header to change the thread_id
    a_data_frame_no - integer number of the second from reference epoch number
    at the output we have the header with changed second from reference epoch number
    """

    # current second from reference epoch number in header:
    data_4_bytes = int.from_bytes(a_vdif_header[0:4], byteorder='big', signed=False)
    # mask_1 = int('00111111111111111111111111111111', 2)
    mask_2 = int('11000000000000000000000000000000', 2)
    # current_sec_from_ref = (mask_1 & data_4_bytes)
    # print(' Current second from reference epoch: ', current_sec_from_ref)
    part_without_changes = (mask_2 & data_4_bytes)
    word_4_bytes = part_without_changes | a_sec_from_ref_epoch
    a_vdif_header[0:4] = word_to_bytearray(word_4_bytes)

    # # Code to check the second from reference epoch number in header
    # data_4_bytes = int.from_bytes(a_vdif_header[0:4], byteorder='big', signed=False)
    # current_sec_from_ref = (mask_1 & data_4_bytes)
    # print(' Current second from reference epoch number: ', current_sec_from_ref)

    return a_vdif_header


def rt32wf_to_vdf_frame_header(filepath):
    """
    The function forms a vdif data frame header
    """
    # Reading the rpr header parameters
    file_header_param_dict = rpr_wf_header_reader_dict(filepath)

    # Configure Words of VDIF header
    header_bytearray = bytearray([])
    # ------------------------------------------------------------------------------------------------------------------
    # Word 0 Bits 31-30
    b31 = 0  # Invalid data marker (valid - 0, invalid - 1)
    b30 = 0  # Standard 32-byte VDIF Data Frame header

    # Word 0 Bits 29-0 Seconds from reference epoch
    # For now we will use the time of file creation but in general we need to use actual time of each sample
    # There is a problem because UTC file time does not have a date, and the date from local time can vary vs. UTC
    # We take the date from initial file name, which is odd but solves a lot of problems without changing of file header
    reference_epoch = '2020.01.01 00:00:00'

    # print(file_header_param_dict["File creation utc time"])
    # print(file_header_param_dict["File creation local time"])

    dt_reference_epoch = datetime(int(reference_epoch[0:4]),
                                  int(reference_epoch[5:7]),
                                  int(reference_epoch[8:10]),
                                  int(reference_epoch[11:13]),
                                  int(reference_epoch[14:16]),
                                  int(reference_epoch[17:19]), 0)

    # Datetime object of the file creation time
    dt_data_time = datetime(int('20' + file_header_param_dict["Initial file name"][1:3]),
                            int(file_header_param_dict["Initial file name"][3:5]),
                            int(file_header_param_dict["Initial file name"][5:7]),
                            int(file_header_param_dict["File creation utc time"][0:2]),
                            int(file_header_param_dict["File creation utc time"][3:5]),
                            int(file_header_param_dict["File creation utc time"][6:8]),
                            int(file_header_param_dict["File creation utc time"][9:12]) * 1000)

    seconds_from_epoch = int((dt_data_time - dt_reference_epoch).total_seconds())
    file_header_param_dict["Seconds from reference epoch"] = seconds_from_epoch
    file_header_param_dict["dt File creation time UT"] = dt_data_time

    print(' Data time:                                  ', dt_data_time)
    print(' Reference epoch:                            ', dt_reference_epoch)
    print(' Number of seconds from the reference epoch: ', seconds_from_epoch, ' \n\n')

    # Forming the word from values
    if seconds_from_epoch > 1073741823:
        raise ValueError('Seconds from Epoch got the wrong (too high) value! ')
    b31 = b31 << 31
    b30 = b30 << 30
    word = b31 | b30 | seconds_from_epoch
    word_bytearray = word_to_bytearray(word)
    header_bytearray += word_bytearray

    # ------------------------------------------------------------------------------------------------------------------
    # Word 1 Bits 31-30 Unassigned (should be 0)
    b31 = 0
    b30 = 0
    # Word 1 Bits 29-24 - Reference Epoch for second count

    epoch_no = 40
    first_epoch = '2000.01.01 00:00:00'
    dt_first_epoch = datetime(int(first_epoch[0:4]),
                              int(first_epoch[5:7]),
                              int(first_epoch[8:10]),
                              int(first_epoch[11:13]),
                              int(first_epoch[14:16]),
                              int(first_epoch[17:19]), 0)

    epoch_duration = relativedelta(months=+6)
    dt_reference_epoch = dt_first_epoch + epoch_no * epoch_duration

    # epoch_no = (dt_reference_epoch - dt_first_epoch) / epoch_duration  --- impossible to divide
    # print(' Reference epoch No:                     ', epoch_no)

    # Word 1 Bits 23-0 - Data Frame # within second, starting at zero; must be integral number of Data Frames per second
    frame_no = 0  # Temporary value!!!

    # Forming the word from values
    if epoch_no > 63:
        raise ValueError('Epoch number got the wrong (too high) value! ')
    if frame_no >= 8388607:
        raise ValueError('Frame number got the wrong (too high) value! ')
    b31 = b31 << 31
    b30 = b30 << 30
    epoch_no = epoch_no << 24
    word = b31 | b30 | epoch_no | frame_no
    word_bytearray = word_to_bytearray(word)
    header_bytearray += word_bytearray

    # ------------------------------------------------------------------------------------------------------------------

    # Word 2 Bits 31-29: VDIF version number; see Note 3
    vdif_version = 0  # Temporary value!!!

    # Word 2 Bits 28-24: log2(#channels in Data Array); #chans must be power of 2; see Note 4
    channel_no = 1  # We have 2 channels so the log2(2) = 1

    # Word 2 Bits 23-0: Data Frame length (including header) in units of 8 bytes with a maximum length of 2^27 bytes
    data_frame_length = 262148  # 262148 for n_fft = 128 and n_gates = 8192 data frames are of ~ 2MB

    # Forming the word from values
    if vdif_version > 7:
        raise ValueError('VDIF version is wrong (too high)! ')
    if channel_no > 31:
        raise ValueError('Number of channels got the wrong (too high) value! ')
    if data_frame_length > 8388607:
        raise ValueError('Data frame length got the wrong (too high) value! ')
    vdif_version = vdif_version << 29
    channel_no = channel_no << 24
    word = vdif_version | channel_no | data_frame_length
    word_bytearray = word_to_bytearray(word)
    header_bytearray += word_bytearray

    # ------------------------------------------------------------------------------------------------------------------

    # Word 3 Bit 31 - Data type
    data_type_bit = 1  # We have complex, if real, data_type_bit = 0
    # Each complex sample consists of two sample components, designated ‘I’ (In-phase) and ‘Q’ (Quadrature),
    # each containing the same number of bits

    # Word 3 Bits 30-26:  # bits/sample-1 (32 bits/sample max); see Note 7
    # If the data type is ‘complex’, this parameter is set according to the #bits in each complex-sample component
    # (i.e. half the total # bits per complex sample).
    bits_per_sample = 7  # 8 bits actually

    # Word 3 Bits 25-16: Thread ID (0 to 1023)
    thread_id = 0  # There will be 2 threads for 2 channels of the data, but by default we put here thread_id = 0

    # Word 3 Bits 15-0: Station ID; see Note 8 (standard globally assigned 2-character ASCII ID)
    station_id = 380  # Dummy number! Ask the right one!!!

    # Forming the word from values
    if data_type_bit > 1:
        raise ValueError('Data type is wrong (too high)! ')
    if bits_per_sample > 31:
        raise ValueError('Bits per sample got the wrong (too high) value! ')
    if thread_id > 1023:
        raise ValueError('Thread ID got the wrong (too high) value! ')
    if station_id > 32767:
        raise ValueError('Station ID got the wrong (too high) value! ')
    data_type_bit = data_type_bit << 31
    bits_per_sample = bits_per_sample << 26
    thread_id = thread_id << 16
    word = data_type_bit | bits_per_sample | thread_id | station_id
    word_bytearray = word_to_bytearray(word)
    header_bytearray += word_bytearray

    # ------------------------------------------------------------------------------------------------------------------

    # Words 4-7
    # Extended User Data: Format and interpretation of extended user data is indicated by the value of
    # Extended Data Version (EDV) in Word 4 Bits 31-24; see Note 9
    header_bytearray += bytearray([0] * 16)

    # # Encoding the bytearray to little endian format -> use single encoding of all data before writing to file
    # header_bytearray = big_to_little_endian(header_bytearray)

    return header_bytearray, file_header_param_dict


def rt32wf_to_vdf_data_converter(filepath, verbose):
    """
    Function takes the header and RPR (.adr) data and creates the VDIF file
    """
    vdif_header, adr_header_dict = rt32wf_to_vdf_frame_header(filepath)
    print(' Header: ', vdif_header)
    print(' Header length: ', len(vdif_header), ' bytes \n')
    print(' Seconds from reference epoch: ', adr_header_dict["Seconds from reference epoch"], ' sec. \n')

    # Open destination vdif file to save the results
    vdif_file = open("DATA/test_file.vdif", "wb")

    # Calculate the number of complex data point in the file
    num_of_complex_points = (adr_header_dict["File size in bytes"] - 1024) / (2 * 2)  # 2 ch (Re + Im) of 1 byte
    print(' Number of complex points for both channels:  ', num_of_complex_points)

    samples_per_frame = 1000000  # To have exactly 16 frames per second at 16 MHz sampling rate

    with open(filepath) as adr_file:  # Open data file

        '''
        In a loop we count number of points and correct seconds from reference epoch in header accordingly
        In a loop we count number of frames and save it into headers
        '''

        # Skip data till the next second start

        f_time = adr_header_dict["dt File creation time UT"]
        us_to_skip = 1000000 - int(f_time.microsecond)
        print(' We have to skip: ', us_to_skip, ' us')
        samples_to_skip = us_to_skip * 16
        print(' We have to skip: ', samples_to_skip, ' samples')

        # Skip data before the round second tick (we can use data reading or just jump to correct place in the file)
        # raw_data = np.fromfile(adr_file, dtype=np.int8, count=samples_per_frame * 2 * 2)
        adr_file.seek(1024 + samples_to_skip * 4)  # Jump to 1024 byte in the file to skip header + samples to skip

        # Calculate number of bunches in file to read
        full_file_size = adr_header_dict["File size in bytes"]
        bunch_num = (full_file_size - (1024 + samples_to_skip * 4)) // (samples_per_frame * 4)

        print(' Number of bunches in file: ', bunch_num, '\n\n')

        # adr_header_dict["Seconds from reference epoch"] --- ???

        # The loop of data chunks to read and save to a frame starts here
        for bunch in range(bunch_num):
            print(' * Bunch # ', bunch+1, ' of ', bunch_num, ' started at ', time.strftime("%H:%M:%S"), ' ')

            # Read raw data from file in int8 format
            # raw_data = np.fromfile(adr_file, dtype=np.int8, count=n_fft * n_gates * 2 * 2)  # 2 ch (Re + Im) of 1 byte
            raw_data = np.fromfile(adr_file, dtype=np.int8, count=samples_per_frame * 2 * 2)  # 2 ch (Re + Im) of 1 byte
            if verbose:
                print(' Shape of data read from file:                ', raw_data.shape)

            # Separating real and imaginary data from the raw data
            real_data = raw_data[0: samples_per_frame * 2 * 2: 2]
            imag_data = raw_data[1: samples_per_frame * 2 * 2: 2]
            del raw_data
            if verbose:
                print(' Shape of real data array:                    ', real_data.shape)
                print(' Shape of imag data array:                    ', imag_data.shape, '\n')

            # Separate channels of data for real and imag parts:
            real_2ch_data = np.reshape(real_data, (samples_per_frame, 2))
            imag_2ch_data = np.reshape(imag_data, (samples_per_frame, 2))
            del real_data, imag_data
            if verbose:
                print(' Shape of real data array:                    ', real_2ch_data.shape)
                print(' Shape of imag data array:                    ', imag_2ch_data.shape, '\n')
                print(' Type of imag data array:                     ', imag_2ch_data.dtype, '\n')

            '''
            So now we have an array of real data real_2ch_data of some length with 2 channels
            and imaginary data in imag_2ch_data of same length with 2 channels
            '''

            # Converting int8 to uint8
            if verbose:
                print(' Range of Real data in int8 format:           ', np.min(real_2ch_data), np.max(real_2ch_data))
            real_2ch_data = np.array(real_2ch_data + 128, dtype=np.uint8)
            imag_2ch_data = np.array(imag_2ch_data + 128, dtype=np.uint8)
            if verbose:
                print(' Range of Real data in uint8 format:          ', np.min(real_2ch_data), np.max(real_2ch_data), '\n')

            # Make data bytearray of the extracted data
            data_bytearray_thrd_1 = bytearray([])
            data_bytearray_thrd_2 = bytearray([])

            # The two identical loops should be separated into separate cpu threads
            for i in range(real_2ch_data.shape[0] // 2):
                word_bytearray = int8_to_32_bit_word(real_2ch_data[2 * i,     0], imag_2ch_data[2 * i,     0],
                                                     real_2ch_data[2 * i + 1, 0], imag_2ch_data[2 * i + 1, 0])
                data_bytearray_thrd_1 += word_bytearray

            for i in range(real_2ch_data.shape[0] // 2):
                word_bytearray = int8_to_32_bit_word(real_2ch_data[2 * i,     1], imag_2ch_data[2 * i,     1],
                                                     real_2ch_data[2 * i + 1, 1], imag_2ch_data[2 * i + 1, 1])
                data_bytearray_thrd_2 += word_bytearray

            if verbose:
                print(' Length of data frame body is:                ', len(data_bytearray_thrd_1), ' bytes')
                print(' Length of full data frame is:                ', len(data_bytearray_thrd_1) + 32, ' bytes')
                print(' Length of full data frame is:                ', (len(data_bytearray_thrd_1) + 32) / 8,
                      ' of 8 bytes chunks')

            # # Encoding the bytearray to little endian format -> use single encoding of all data before writing to file
            # data_bytearray_thrd_1 = big_to_little_endian(data_bytearray_thrd_1)
            # data_bytearray_thrd_2 = big_to_little_endian(data_bytearray_thrd_2)

            '''
            Form the correct frame header with correct values of:
            - thread_id for both threads
            - seconds from reference epoch - to count accordingly to   
            - frame no within second 
            '''

            vdif_header_1 = vdif_header.copy()
            vdif_header_2 = vdif_header.copy()

            # thread_id changes only for the second thread header
            vdif_header_2 = change_thread_id_in_header(vdif_header_2, 1)

            # data_frame_no change in thread headers of both channels/threads
            data_frame_no = 1  # Temporary!!!
            vdif_header_1 = change_data_frame_no_in_header(vdif_header_1, data_frame_no)
            vdif_header_2 = change_data_frame_no_in_header(vdif_header_2, data_frame_no)

            # secs_from_ref_epoch change in thread headers of both channels/threads
            secs_from_ref_epoch = 1  # Temporary!!!
            vdif_header_1 = change_secs_from_ref_epoch_in_header(vdif_header_1, secs_from_ref_epoch)
            vdif_header_2 = change_secs_from_ref_epoch_in_header(vdif_header_2, secs_from_ref_epoch)

            # Adding frame headers and frame data for 2 threads in single bytearray and write to the file
            data_bytearray = vdif_header_1 + data_bytearray_thrd_1 + vdif_header_2 + data_bytearray_thrd_2

            # Encoding the whole bytearray to little endian format
            data_bytearray = big_to_little_endian(data_bytearray)

            vdif_file.write(data_bytearray)

    # Closing the result file
    vdif_file.close()

    return


if __name__ == '__main__':
    # rt32wf_to_vdf_frame_header(filepath)
    rt32wf_to_vdf_data_converter(filepath, False)

