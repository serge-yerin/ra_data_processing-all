software_version = '2022.07.30'
software_name = 'JDS cross-spectra phase calibration data analysis'

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************

source_directory = '../RA_DATA_ARCHIVE/DSP_cross_spectra_calibration/'  # Directory with JDS files to be analyzed
result_directory = ''                   # Directory where DAT files to be stored (empty string means project directory)

# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import os
import sys
import time
import pylab
from scipy import ndimage
import numpy as np
from os import path
from progress.bar import IncrementalBar
from matplotlib import rc
import matplotlib.pyplot as plt

# To change system path to main source_directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_common_modules.find_and_check_files_in_current_folder import find_and_check_files_in_current_folder
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS


# ###############################################################################


def obtain_calibr_matrix_for_2_channel_sp_calibration(path_to_calibr_data):
    """
    The function reads 2-channel cross-spectra calibration files (UTR-2/URAN noise generator calibration with a set of
    attenuators) and provides a phase difference txt file for cross-spectra observations calibration
    """

    file_list = find_and_check_files_in_current_folder(path_to_calibr_data, '.jds')

    result_path = 'RESULTS_cross-spectra_calibration/'
    if not os.path.exists(result_path):
        os.makedirs(result_path)


# ###############################################################################
# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    print('\n\n\n\n\n\n\n\n   ********************************************************************')
    print('   * ', software_name, ' v.', software_version, ' *      (c) YeS 2020')
    print('   ******************************************************************** \n\n\n')

    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")
    print('  Today is ', current_date, ' time is ', current_time, '\n')

    obtain_calibr_matrix_for_2_channel_sp_calibration(source_directory)

    endTime = time.time()
    print('\n\n  The program execution lasted for ', round((endTime - start_time), 2), 'seconds (',
                                                     round((endTime - start_time)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', software_name, ' has finished! *** \n\n\n')
