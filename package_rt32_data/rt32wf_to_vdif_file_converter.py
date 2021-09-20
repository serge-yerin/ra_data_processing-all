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
matplotlib.use('TkAgg')

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_rt32_data.rt32_zolochiv_waveform_reader import rpr_wf_header_reader_dict


def rt32wf_to_vdf_file_converter(filepath):
    """

    """
    file_header_param_dict = rpr_wf_header_reader_dict(filepath)

    # Configure Word 0 of VDIF header
    b31 = 0  # Invalid data
    b30 = 0  # Standard 32-byte VDIF Data Frame header

    # Seconds from reference epoch
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

    seconds_from_epoch = (dt_data_time - dt_reference_epoch).total_seconds()

    print(dt_data_time)
    print(dt_reference_epoch)
    print(seconds_from_epoch)

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
