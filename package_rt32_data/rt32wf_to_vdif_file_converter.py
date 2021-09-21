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


def rt32wf_to_vdf_file_converter(filepath):
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

    print(' Current time:                           ', dt_data_time)
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
    channel_no = 2  # Temporary value!!!

    # Word 2 Bits 23-0: Data Frame length (including header) in units of 8 bytes with a maximum length of 2^27 bytes
    data_frame_length = 16384  # Temporary value!!!

    # Word 3 Bit 31 - Data type
    data_type_bit = 1  # Complex, if Real, data_type_bit = 0
    # Each complex sample consists of two sample components, designated ‘I’ (In-phase) and ‘Q’ (Quadrature),
    # each containing the same number of bits

    # Word 3 Bits 30-26:  # bits/sample-1 (32 bits/sample max); see Note 7
    # If the data type is ‘complex’, this parameter is set according to the #bits in each complex-sample component
    # (i.e. half the total #bits per complex sample).
    bits_per_sample = 2  # Temporary value!!!

    # Word 3 Bits 25-16: Thread ID (0 to 1023)
    thread_id = 0  # Temporary value!!!

    # Word 3 Bits 15-0: Station ID; see Note 8 (standard globally assigned 2-character ASCII ID)

    # Words 4-7
    # Extended User Data: Format and interpretation of extended user data is indicated by the value of
    # Extended Data Version (EDV) in Word 4 Bits 31-24; see Note 9

    return


if __name__ == '__main__':
    rt32wf_to_vdf_file_converter(filepath)


################################################################################

# if __name__ == '__main__':
#
#     print('\n\n\n\n\n\n\n\n   **************************************************************************')
#     print('   *               ', Software_name, ' v.', Software_version, '              *      (c) YeS 2018')
#     print('   ************************************************************************** \n')
#
#     startTime = time.time()
#     currentTime = time.strftime("%H:%M:%S")
#     currentDate = time.strftime("%d.%m.%Y")
#     print('   Today is ', currentDate, ' time is ', currentTime, '\n')
#
#     # *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
#     result_path = 'RESULTS_MARK5_Reader'
#     if not os.path.exists(result_path):
#         os.makedirs(result_path)
#
