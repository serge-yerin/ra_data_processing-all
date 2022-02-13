# Python3
Software_version = '2022.01.19'
Software_name = 'RT-32 Zolochiv waveform reader and converter to vdif'
# Script intended to read, show and analyze data from MARK5 receiver
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
directory = '../RA_DATA_ARCHIVE/RT-32_Zolochiv_waveform_first_sample/'
filename = 'A210612_075610_rt32_waveform_first_sample.adr'
result_file_name = "n21c2_zo_no0001.vdif"
filepath = directory + filename
result_path = ''
spectra_inversion = False  # Set True if the data were obtained with inverse spectrum

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import os
import sys
import time
import datetime
import numpy as np
from os import path
from datetime import datetime
# from dateutil.relativedelta import *

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# from package_rt32_data.rt32_zolochiv_waveform_reader import rpr_wf_header_reader_dict


def rpr_wf_header_reader_dict(filepath):
    """
    !!! COPY from package_rt32_data.rt32_zolochiv_waveform_reader import rpr_wf_header_reader_dict
    Zolochiv Ukraine RPR receiver waveform data header reader (not finished, just POC)
    """

    param_dict = {}

    with open(filepath, "rb") as file:
        param_dict["File size in bytes"] = os.stat(filepath).st_size  # Size of file

        fheader_tag = file.read(640)
        param_dict["Initial file name"] = fheader_tag[0:32].decode('utf-8').rstrip('\x00')  # original name of the file
        param_dict["File creation local time"] = fheader_tag[32:58].decode('utf-8').rstrip('\x00')  # file creation local time
        # !!! In the real file bytes between 58 and 64 do not decode with utf-8 but has some info
        tmp = fheader_tag[58:64]
        # tmp = int.from_bytes(fheader_tag[58:64], byteorder='big', signed=True)

        param_dict["File creation utc time"] = fheader_tag[64:96].decode('utf-8').rstrip('\x00')
        param_dict["System name"] = fheader_tag[96:128].decode('utf-8').rstrip('\x00')
        param_dict["Observation place"] = fheader_tag[128:256].decode('utf-8').rstrip('\x00')
        param_dict["Observation description"] = fheader_tag[256:512].decode('utf-8').rstrip('\x00')

        # fheader_tag[512:640]  # uint32 processing and service parameters only for compatibility with old formats

        print('\n File to analyse:             ', filepath)
        print(' File size:                   ', round(param_dict["File size in bytes"] / 1024 / 1024, 3), ' Mb (',
              param_dict["File size in bytes"], ' bytes )')
        print(' Initial file name:           ', param_dict["Initial file name"])
        print(' Initial file local time:     ', str(param_dict["File creation local time"])[:-1])
        # print(' Unrecognized data from bytes 58:64: ', tmp)
        print(' Initial file GMT time:       ', param_dict["File creation utc time"])
        print(' Receiver name:               ', param_dict["System name"])  # operator (can be used as name of the system)
        print(' Observation place:           ', param_dict["Observation place"])  # description of the measurements place
        print(' Observation description:     ', param_dict["Observation description"])  # additional measurements description

        adrs_param_tag = file.read(28)
        param_dict["ADR mode"] = int.from_bytes(adrs_param_tag[0:4], byteorder='big', signed=True)
        param_dict["FFT size"] = int.from_bytes(adrs_param_tag[4:8], byteorder='big', signed=True)
        param_dict["Average constant"] = int.from_bytes(adrs_param_tag[8:12], byteorder='big', signed=True)
        param_dict["FFT start line"] = int.from_bytes(adrs_param_tag[12:16], byteorder='big', signed=True)
        param_dict["FFT width"] = int.from_bytes(adrs_param_tag[16:20], byteorder='big', signed=True)
        param_dict["Block size"] = int.from_bytes(adrs_param_tag[20:24], byteorder='big', signed=True)
        param_dict["ADC frequency, Hz"] = int.from_bytes(adrs_param_tag[20:24], byteorder='big', signed=True)

        print('\n Receiver mode:               ', param_dict["ADR mode"])  # ADRS_MODE (0..2)WVF, (3..5)SPC, 6-CRL
        print(' FFT size:                    ', param_dict["FFT size"])  # 2048 ... 32768
        print(' Number of averaged spectra:  ', param_dict["Average constant"])  # 16 ... 1000
        print(' FFT start line:              ', param_dict["FFT start line"])  # 0 ... 7, SLine*1024 first line for spectrum output
        print(' FFT width:                   ', param_dict["FFT width"])  # 2048 ... 32768
        print(' Data block size:             ', param_dict["Block size"])  # bytes, data block size calculated from data processing/output parameters
        print(' Measured ADC frequency:      ', param_dict["ADC frequency, Hz"], ' Hz')  # ADC frequency reported by Astro-Digital-Receiver

        adrs_opt_tag = file.read(36)
        param_dict["Opt size"] = int.from_bytes(adrs_opt_tag[0:4], byteorder='big', signed=True)
        param_dict["Start/stop switch"] = int.from_bytes(adrs_opt_tag[4:8], byteorder='big', signed=True)
        param_dict["Start second"] = int.from_bytes(adrs_opt_tag[8:12], byteorder='big', signed=True)
        param_dict["Stop second"] = int.from_bytes(adrs_opt_tag[12:16], byteorder='big', signed=True)
        param_dict["Test mode"] = int.from_bytes(adrs_opt_tag[16:20], byteorder='big', signed=True)
        param_dict["Norm coeff 1"] = int.from_bytes(adrs_opt_tag[20:24], byteorder='big', signed=True)
        param_dict["Norm coeff 2"] = int.from_bytes(adrs_opt_tag[24:28], byteorder='big', signed=True)
        param_dict["Channel delay"] = int.from_bytes(adrs_opt_tag[28:32], byteorder='big', signed=True)
        df_opt_bit_opt = int.from_bytes(adrs_opt_tag[32:36], byteorder='big', signed=True)

        '''
        ADRS options (data block size and format do not depends on)
        uint32_t  Opt;		// bit 0 - StartBySec: no(0)/yes(1)
                            // bit 1 - CLC: internal(0)/external(1)
                            // bit 2 - FFT Window: Hanning(0)/rectangle(1)
                            // bit 3 - DC removing: No(0)/Yes(1)
                            // bit 4 - averaging(0)/decimation(1)
                            // bit 5 - CH1: On(0)/Off(1)
                            // bit 6 - CH2: On(0)/Off(1)
        '''

        print('\n Size:                        ', param_dict["Opt size"])
        print(' Start / Stop:                ', param_dict["Start/stop switch"])  # StartStop 0/1	(-1 - ignore)
        print(' Start second:                ', param_dict["Start second"])  # abs.time.sec - processing starts
        print(' Stop second:                 ', param_dict["Stop second"])  # abs.time.sec - processing stops
        print(' Test mode:                   ', param_dict["Test mode"])  # Test Mode: 0, 1, 2...
        print(' Norm. coefficient 1-CH:      ', param_dict["Norm coeff 1"])  # Normalization coefficient 1-CH (1 ... 65535)
        print(' Norm. coefficient 2-CH       ', param_dict["Norm coeff 2"])  # Normalization coefficient 2-CH (1 ... 65535)
        print(' Delay:                       ', param_dict["Channel delay"], ' ps')  # Delay in pico-seconds (-1000000000 ... 1000000000)
        print(' Options:                     ', df_opt_bit_opt, '\n\n')

        # print('Fheader tag 1:', fheader_tag[0:32])
        # print('Fheader tag 2:', fheader_tag[32:64])
        # print('F param tag:', adrs_param_tag)
        # print('F opt tag:', adrs_opt_tag)

    return param_dict


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
# def int8_to_32_bit_word(v_int_1, v_int_2, v_int_3, v_int_4):
#     """
#     The function takes 4 uint8 or int8 values and form a 32 bit word
#     (actually can be changed by appropriate array operations)
#     """
#     if 0 > v_int_1 > 256 or 0 > v_int_2 > 256 or 0 > v_int_3 > 256 or 0 > v_int_4 > 256:
#         raise ValueError('\n\n      Error! Invalid value!  \n\n')
#     byte_4 = v_int_4 << 24
#     byte_3 = v_int_3 << 16
#     byte_2 = v_int_2 << 8
#     word = byte_4 | byte_3 | byte_2 | v_int_1
#     word_bytearray = word_to_bytearray(word)
#     return word_bytearray


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
    # We take the date from initial file name, which is odd but solves a lot of problems without changing file header
    reference_epoch = '2020.01.01 00:00:00'  # Epoch # 40

    # Datetime object of the reference epoch
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
    # first_epoch = '2000.01.01 00:00:00'
    # dt_first_epoch = datetime(int(first_epoch[0:4]),
    #                           int(first_epoch[5:7]),
    #                           int(first_epoch[8:10]),
    #                           int(first_epoch[11:13]),
    #                           int(first_epoch[14:16]),
    #                           int(first_epoch[17:19]), 0)
    #
    # epoch_duration = relativedelta(months=+6)
    # dt_reference_epoch = dt_first_epoch + epoch_no * epoch_duration

    # epoch_no = (dt_reference_epoch - dt_first_epoch) / epoch_duration  --- impossible to divide
    # print(' Reference epoch No:                     ', epoch_no)

    # Word 1 Bits 23-0 - Data Frame # within second, starting at zero; must be integral number of Data Frames per second
    frame_no = 0  # Temporary value, will be changed for each frame while frame forming

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
    vdif_version = 0  # Temporary value, do not know if it is correct...

    # Word 2 Bits 28-24: log2(#channels in Data Array); #chans must be power of 2; see Note 4
    channel_no = 1  # We have 2 channels so the log2(2) = 1

    # Word 2 Bits 23-0: Data Frame length (including header) in units of 8 bytes with a maximum length of 2^27 bytes
    data_frame_length = 250004  # 250004 for samples_per_frame = 1 000 000 data frames are of ~ 2MB
    # !!!!

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
    data_type_bit = 0  # We have real, if complex, data_type_bit = 1
    # Each complex sample consists of two sample components, designated ‘I’ (In-phase) and ‘Q’ (Quadrature),
    # each containing the same number of bits

    # Word 3 Bits 30-26:  # bits/sample-1 (32 bits/sample max); see Note 7
    # If the data type is ‘complex’, this parameter is set according to the #bits in each complex-sample component
    # (i.e. half the total # bits per complex sample).
    bits_per_sample = 1  # 2 bits per sample actually

    # Word 3 Bits 25-16: Thread ID (0 to 1023)
    thread_id = 0  # There will be 2 threads for 2 channels of the data, but by default we put here thread_id = 0

    # Word 3 Bits 15-0: Station ID; see Note 8 (standard globally assigned 2-character ASCII ID) - 'zo' for Zolochiv
    station_id = int.from_bytes('zo'.encode(), 'big')  # 31343 = 'zo' in ASCII

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

    return header_bytearray, file_header_param_dict


def rt32wf_to_vdf_data_converter(filepath, verbose, fft_length, spectra_num):
    """
    Function takes the header and RPR (.adr) data and creates the VDIF file
    """
    vdif_header, adr_header_dict = rt32wf_to_vdf_frame_header(filepath)
    print(' Header: ', vdif_header)
    print(' Header length: ', len(vdif_header), ' bytes \n')
    print(' Seconds from reference epoch: ', adr_header_dict["Seconds from reference epoch"], ' sec. \n')

    '''
         the file(s) should be named according to this pattern:
                <experiment>_<station>_<scan>
        So for your station, participating in the 2nd C-band NME in 2021, the file names would look like this:
                n21c2_zo_no0001
        assuming "Zo" will be the two-letter station code assigned to Zolochiv.
        The scan numbers correspond to the scan labels in the VEX file that your station 
        participates in and records data for.
    '''

    # Open destination vdif file to save the results
    # vdif_file = open("DATA/" + adr_header_dict["Initial file name"][:-4] + ".vdif", "wb")
    vdif_file = open(result_file_name, "wb")

    # Calculate the number of complex data point in the file
    num_of_complex_points = (adr_header_dict["File size in bytes"] - 1024) / (2 * 2)  # 2 ch (Re + Im) of 1 byte
    print(' Number of complex points for both channels:  ', num_of_complex_points)

    samples_per_frame = 1000000  # To have exactly 16 frames per second at 16 MHz sampling rate

    with open(filepath) as adr_file:  # Open data file

        # Skip data till the next second starts
        f_time = adr_header_dict["dt File creation time UT"]
        us_to_skip = 1000000 - int(f_time.microsecond)
        print(' We have to skip: ', us_to_skip, ' us')
        samples_to_skip = us_to_skip * 16
        print(' We have to skip: ', samples_to_skip, ' samples')

        # Skip data before the round second tick (we can use data reading or just jump to correct place in the file)
        # raw_data = np.fromfile(adr_file, dtype=np.int8, count=samples_per_frame * 2 * 2)
        adr_file.seek(1024 + samples_to_skip * 4)  # Jump to 1024 byte in the file to skip header + samples to skip

        # Calculate number of bunches in file to read
        bunch_num = (adr_header_dict["File size in bytes"] - (1024 + samples_to_skip * 4)) // (samples_per_frame * 4)

        print(' Number of bunches in file: ', bunch_num, '\n\n')

        # The next second after the one shown in file header
        second_counter = adr_header_dict["Seconds from reference epoch"] + 1
        frame_counter = 0

        # The loop of data chunks to read and save to a frame starts here
        for bunch in range(bunch_num):
            print(' * Bunch # ', bunch+1, ' of ', bunch_num, ' started at ', time.strftime("%H:%M:%S"), ' ')

            # We have 16 frames per second, so each 16 frames we set counter of frames/second to 0 and add a second
            if frame_counter >= 16:
                frame_counter = 0
                second_counter += 1
                # print(' Frame counter:', frame_counter, ', second from epoch:', second_counter, '\n')

            # Read raw data from file in int8 format
            raw_data = np.fromfile(adr_file, dtype=np.int8, count=samples_per_frame * 2 * 2)  # 2 ch (Re + Im) of 1 byte
            if verbose:
                print(' Shape of data read from file:                ', raw_data.shape)

            # Preparing empty matrix for complex data
            cmplx_data = np.empty(fft_length * spectra_num * 2, dtype=np.complex64)

            # Separating real and imaginary data from the raw data
            cmplx_data.real = raw_data[0: samples_per_frame * 2 * 2: 2]
            cmplx_data.imag = raw_data[1: samples_per_frame * 2 * 2: 2]
            del raw_data
            if verbose:
                print(' Shape of complex data array:                    ', cmplx_data.shape)

            # # Reshaping complex data to separate data of channels
            # rsh_crd = np.reshape(crd, (nGates, nFFT, 2))
            # del crd
            # print('Shape of reshaped complex data array (rsh_crd) before transpose:', rsh_crd.shape)
            # rsh_crd = np.transpose(rsh_crd)
            # print('Shape of reshaped complex data array (rsh_crd) after transpose:', rsh_crd.shape)
            #
            # # Separate data of channels
            # tt0 = rsh_crd[0, :, :]
            # tt1 = rsh_crd[1, :, :]
            # print('Shapes of separated channels (tt0, tt1):', tt0.shape, tt1.shape)

            input()




            # Separate channels of data for real and imag parts:
            real_2ch_data = np.reshape(real_data, (samples_per_frame, 2))
            imag_2ch_data = np.reshape(imag_data, (samples_per_frame, 2))
            del real_data, imag_data
            if verbose:
                print(' Shape of real data array:                    ', real_2ch_data.shape)
                print(' Shape of imag data array:                    ', imag_2ch_data.shape, '\n')
                print(' Type of imag data array:                     ', imag_2ch_data.dtype, '\n')

            '''
            now we have an array of real data real_2ch_data of some length with 2 channels
            and imaginary data in imag_2ch_data of same length with 2 channels
            '''

            # # Converting int8 to uint8
            # if verbose:
            #     print(' Range of Real data in int8 format:           ', np.min(real_2ch_data), np.max(real_2ch_data))
            # real_2ch_data = np.array(real_2ch_data + 128, dtype=np.uint8)
            # imag_2ch_data = np.array(imag_2ch_data + 128, dtype=np.uint8)
            # if verbose:
            #     print(' Range of Real data in uint8 format:          ', np.min(real_2ch_data), np.max(real_2ch_data),
            #           '\n')

            # # Make data bytearray of the extracted data
            # data_bytearray_thrd_1 = bytearray([])
            # data_bytearray_thrd_2 = bytearray([])
            #
            # # The two identical loops (and further operations) should be separated into separate cpu threads
            # # or better replaced by making bytes directly of uint8 arrays for this particular case of 8 bits data.
            # for i in range(real_2ch_data.shape[0] // 2):
            #     word_bytearray = int8_to_32_bit_word(real_2ch_data[2 * i,     0], imag_2ch_data[2 * i,     0],
            #                                          real_2ch_data[2 * i + 1, 0], imag_2ch_data[2 * i + 1, 0])
            #     data_bytearray_thrd_1 += word_bytearray
            #
            # for i in range(real_2ch_data.shape[0] // 2):
            #     word_bytearray = int8_to_32_bit_word(real_2ch_data[2 * i,     1], imag_2ch_data[2 * i,     1],
            #                                          real_2ch_data[2 * i + 1, 1], imag_2ch_data[2 * i + 1, 1])
            #     data_bytearray_thrd_2 += word_bytearray

            # # Preparing arrays to fill with data correctly
            # data_0 = np.zeros((2 * real_2ch_data.shape[0]), dtype=np.uint8)
            # data_1 = np.zeros((2 * real_2ch_data.shape[0]), dtype=np.uint8)
            #
            # # Forming the 32-bit words (it's better to check order of data_0 first index, but it works like first try)
            # data_0[3::4] = real_2ch_data[0::2, 0]
            # data_0[2::4] = imag_2ch_data[0::2, 0]
            # data_0[1::4] = real_2ch_data[1::2, 0]
            # data_0[0::4] = imag_2ch_data[1::2, 0]
            # data_1[3::4] = real_2ch_data[0::2, 1]
            # data_1[2::4] = imag_2ch_data[0::2, 1]
            # data_1[1::4] = real_2ch_data[1::2, 1]
            # data_1[0::4] = imag_2ch_data[1::2, 1]

            # # Converting to bytes
            # data_0_bytes = data_0.tobytes(order='F')  # order='C'
            # data_1_bytes = data_1.tobytes(order='F')  # order='C'



            # Make two copies of basic headers for changing them according to current numbers
            vdif_header_1 = vdif_header.copy()
            vdif_header_2 = vdif_header.copy()

            # thread_id changes only for the second thread header
            vdif_header_2 = change_thread_id_in_header(vdif_header_2, 1)

            # data_frame_no change in thread headers of both channels/threads
            vdif_header_1 = change_data_frame_no_in_header(vdif_header_1, frame_counter)
            vdif_header_2 = change_data_frame_no_in_header(vdif_header_2, frame_counter)

            # secs_from_ref_epoch change in thread headers of both channels/threads
            vdif_header_1 = change_secs_from_ref_epoch_in_header(vdif_header_1, second_counter)
            vdif_header_2 = change_secs_from_ref_epoch_in_header(vdif_header_2, second_counter)

            # Adding frame headers and frame data for 2 threads in single bytearray and write to the file
            data_bytearray = vdif_header_1 + data_0_bytes + vdif_header_2 + data_1_bytes
            # print(' Length of one full frame: ', len(data_bytearray)/2, ' bytes')

            # Encoding the whole bytearray to little endian format
            data_bytearray = big_to_little_endian(data_bytearray)

            # Write data of 2 frames to a file
            vdif_file.write(data_bytearray)

            # Increment counter
            frame_counter += 1

    # Closing the result file
    vdif_file.close()

    return


if __name__ == '__main__':
    # rt32wf_to_vdf_frame_header(filepath)
    rt32wf_to_vdf_data_converter(filepath, True, 16384, 2048)

