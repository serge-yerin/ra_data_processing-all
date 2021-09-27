# Python3
Software_version = '2021.08.28'
Software_name = 'RT-32 Zolochiv waveform reader'
# Script intended to read, show and analyze data from MARK5 receiver
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
directory = '../RA_DATA_ARCHIVE/'
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


def rt32wf_to_vdf_file_header(filepath):
    """

    """
    file_header_param_dict = rpr_wf_header_reader_dict(filepath)

    # Configure Words of VDIF header
    # Word 0 Bits 31-30
    b31 = 0  # Invalid data
    b30 = 0  # Standard 32-byte VDIF Data Frame header

    # Word 0 Bits 29-0 Seconds from reference epoch
    # For now we will use the time of file creation but in general we need to use actual time of each sample
    # There is a problem because UTC file time does not have a date, and the date from local time can vary vs. UTC
    # We take the date from initial file name, which is odd but solves a lot of problems without changing of file header
    reference_epoch = '2020.01.01 00:00:00'

    print(reference_epoch)
    print(file_header_param_dict["File creation utc time"])
    print(file_header_param_dict["File creation local time"])

    dt_reference_epoch = datetime(int(reference_epoch[0:4]),
                                  int(reference_epoch[5:7]),
                                  int(reference_epoch[8:10]),
                                  int(reference_epoch[11:13]),
                                  int(reference_epoch[14:16]),
                                  int(reference_epoch[17:19]), 0)

    dt_data_time = datetime(int('20' + file_header_param_dict["Initial file name"][1:3]),
                            int(file_header_param_dict["Initial file name"][3:5]),
                            int(file_header_param_dict["Initial file name"][5:7]),
                            int(file_header_param_dict["File creation utc time"][0:2]),
                            int(file_header_param_dict["File creation utc time"][3:5]),
                            int(file_header_param_dict["File creation utc time"][6:8]),
                            int(file_header_param_dict["File creation utc time"][9:12]) * 1000)

    seconds_from_epoch = int((dt_data_time - dt_reference_epoch).total_seconds())

    print(' Data time:                              ', dt_data_time)
    print(' Reference epoch:                        ', dt_reference_epoch)
    print(' Number of seconds from reference epoch: ', seconds_from_epoch)

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
    print(' Reference epoch:                        ', dt_reference_epoch)
    # epoch_no = (dt_reference_epoch - dt_first_epoch) / epoch_duration  --- impossible to divide
    # print(' Reference epoch No:                     ', epoch_no)

    # Word 1 Bits 23-0 - Data Frame # within second, starting at zero; must be integral number of Data Frames per second
    frame_no = 0  # Temporary value!!!

    # Word 2 Bits 31-29: VDIF version number; see Note 3
    vdif_version = 0  # Temporary value!!!

    # Word 2 Bits 28-24: log2(#channels in Data Array); #chans must be power of 2; see Note 4
    channel_no = 1  # We have 2 channels so the log2(2) = 1

    # Word 2 Bits 23-0: Data Frame length (including header) in units of 8 bytes with a maximum length of 2^27 bytes
    data_frame_length = 16384  # Temporary value!!!

    # Word 3 Bit 31 - Data type
    data_type_bit = 1  # We have complex, if real, data_type_bit = 0
    # Each complex sample consists of two sample components, designated ‘I’ (In-phase) and ‘Q’ (Quadrature),
    # each containing the same number of bits

    # Word 3 Bits 30-26:  # bits/sample-1 (32 bits/sample max); see Note 7
    # If the data type is ‘complex’, this parameter is set according to the #bits in each complex-sample component
    # (i.e. half the total #bits per complex sample).
    bits_per_sample = 7  # 8 bits actually

    # Word 3 Bits 25-16: Thread ID (0 to 1023)
    thread_id = 0  # Seems to be the only thread, so 0.

    # Word 3 Bits 15-0: Station ID; see Note 8 (standard globally assigned 2-character ASCII ID)

    # Words 4-7
    # Extended User Data: Format and interpretation of extended user data is indicated by the value of
    # Extended Data Version (EDV) in Word 4 Bits 31-24; see Note 9

    vdif_header = bytearray(8 * 4)

    return vdif_header, file_header_param_dict


def rt32wf_to_vdf_data_converter(filepath):
    """
    Function takes the header and RPR (.adr) data and creates the VDIF file
    """
    vdif_header, adr_header_dict = rt32wf_to_vdf_file_header(filepath)
    print('\n Header: ', vdif_header)

    # Calculate the number of complex data point in the file
    num_of_complex_points = (adr_header_dict["File size in bytes"] - 1024) / (2 * 2)  # 2 ch (Re + Im) of 1 byte
    print(' Number of complex points for both channels: ', num_of_complex_points)

    nFFT = 16384
    nGates = 8192

    with open(filepath) as adr_file:  # Open data file
        adr_file.seek(1024)  # Jump to 1024 byte in the file to skip header
        # Read raw data from file in int8 format
        raw_data = np.fromfile(adr_file, dtype=np.int8, count=nFFT * nGates * 2 * 2)  # 2 ch (Re + Im) of 1 byte
        print('Shape of data read from file:', raw_data.shape)

        # Preparing empty matrix for complex data
        # cmplx_data = np.empty(nFFT * nGates * 2, dtype=np.complex8)
        # print('Shape of prepared complex data array:', cmplx_data.shape)

        # Separating real and imaginary data from the raw data
        real_data = raw_data[0: nFFT * nGates * 2 * 2: 2]
        imag_data = raw_data[1: nFFT * nGates * 2 * 2: 2]
        del raw_data
        print('Shape of real data array                  :', real_data.shape)
        print('Shape of imag data array                  :', imag_data.shape)

        # Separate channels of data for real and imag parts:
        real_2ch_data = np.reshape(real_data, (nGates * nFFT, 2))
        imag_2ch_data = np.reshape(imag_data, (nGates * nFFT, 2))
        del real_data, imag_data
        print('Shape of real data array                  :', real_2ch_data.shape)
        print('Shape of imag data array                  :', imag_2ch_data.shape)
        print('Type of imag data array                   :', imag_2ch_data.dtype)


        # rsh_crd = np.reshape(cmplx_data, (nGates, nFFT, 2))
        # del cmplx_data
        # print('Shape of reshaped complex data array (rsh_crd) before transpose:', rsh_crd.shape)
        # rsh_crd = np.transpose(rsh_crd)
        # print('Shape of reshaped complex data array (rsh_crd) after transpose:', rsh_crd.shape)
        #
        # # Separate data of channels
        # tt0 = rsh_crd[0, :, :]
        # tt1 = rsh_crd[1, :, :]
        # print('Shapes of separated channels (tt0, tt1):', tt0.shape, tt1.shape)




    return


if __name__ == '__main__':
    # rt32wf_to_vdf_file_header(filepath)
    rt32wf_to_vdf_data_converter(filepath)

