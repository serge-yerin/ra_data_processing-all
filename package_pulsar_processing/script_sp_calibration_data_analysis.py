software_version = '2022.07.30'
software_name = 'JDS cross-spectra phase calibration data analysis'

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************

source_directory = '../RA_DATA_ARCHIVE/DSP_cross_spectra_calibration/'  # Directory with JDS files to be analyzed
result_directory = ''                   # Directory where DAT files to be stored (empty string means project directory)

MaxNsp = 2048                 # Number of spectra to read for one figure
spSkip = 0                    # Number of chunks to skip from data beginning
RFImeanConst = 8              # Constant of RFI mitigation (usually 8)
Vmin = -100                   # Lower limit of figure dynamic range
Vmax = -40                    # Upper limit of figure dynamic range
VminNorm = 0                  # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 20                 # Upper limit of figure dynamic range for normalized spectra
VminCorrMag = -150            # Lower limit of figure dynamic range for correlation magnitude spectra
VmaxCorrMag = -30             # Upper limit of figure dynamic range for correlation magnitude spectra
colormap = 'jet'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
customDPI = 300               # Resolution of images of dynamic spectra
CorrelationProcess = 1        # Process correlation data or save time?  (1 = process, 0 = save)
longFileSaveAch = 0           # Save data A to long file? (1 = yes, 0 = no)
longFileSaveBch = 0           # Save data B to long file? (1 = yes, 0 = no)
longFileSaveCRI = 1           # Save correlation data (Real and Imaginary) to long file? (1 = yes, 0 = no)
longFileSaveCMP = 0           # Save correlation data (Module and Phase) to long file? (1 = yes, 0 = no)
DynSpecSaveInitial = 0        # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 0        # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 0       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
SpecterFileSaveSwitch = 0     # Save 1 immediate specter to TXT file? (1 = yes, 0 = no)
ImmediateSpNo = 0             # Number of immediate specter to save to TXT file
where_save_pics = 1           # Where to save result pictures? (0 - to script folder, 1 - to data folder)


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
from package_ra_data_files_formats.JDS_file_reader import JDS_file_reader
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder

# ###############################################################################


def obtain_calibr_matrix_for_2_channel_sp_calibration(path_to_calibr_data):
    """
    The function reads 2-channel cross-spectra calibration files (UTR-2/URAN noise generator calibration with a set of
    attenuators) and provides a phase difference txt file for cross-spectra observations calibration
    """

    # Prepare a folder for results
    result_path = 'RESULTS_cross-sp_calibr_' + path_to_calibr_data.split('/')[-2] + '/'
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    # Find all files in the calibration folder
    file_list = find_files_only_in_current_folder(path_to_calibr_data, '.jds', 1)

    # Prepare empty lists
    labels = []
    cross_sp_ampl = []
    cross_sp_angl = []
    init_file_names = []

    # Main loop by files start
    for file_no in range(len(file_list)):  # loop by files

        fname = path_to_calibr_data + file_list[file_no]

        # *** Data file header read ***
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
         clock_freq, df_creation_time_utx, channel, receiver_mode, mode, n_avr, time_res, fmin, fmax,
         df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(fname, 0, 0)

        labels.append(df_system_name + ' ' + df_description.replace('_', ' '))
        init_file_names.append(df_filename)

        print('\n  Processing file: ', df_description.replace('_', ' '),
              ',  # ', file_no+1, ' of ', len(file_list), '\n')

        # Run ADR reader for the current folder
        # done, dat_file_name, dat_file_list = JDS_file_reader([path_to_calibr_data + file_list[file_no]],
        #                                                             result_path, MaxNsp, spSkip,
        #                                                             RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
        #                                                             VminCorrMag, VmaxCorrMag, colormap, customDPI,
        #                                                             CorrelationProcess, longFileSaveAch, longFileSaveBch,
        #                                                             longFileSaveCRI, longFileSaveCMP, DynSpecSaveInitial,
        #                                                             DynSpecSaveCleaned, CorrSpecSaveInitial,
        #                                                             CorrSpecSaveCleaned, SpecterFileSaveSwitch,
        #                                                             ImmediateSpNo, dat_files_path=result_path,
        #                                                             print_or_not=0)

    def read_dat_file_for_carlibration(file_name, num_of_spectra, freq_points_num):
        file = open(file_name, 'rb')
        file.seek(1024)
        data = np.fromfile(file, dtype=np.float64, count=num_of_spectra * freq_points_num)
        data = np.reshape(data, [freq_points_num, num_of_spectra], order='F')
        data = data[:-4]
        data[np.isnan(data)] = 0
        return data

    # Processing pairs of files to find the phase difference
    for pair in range(len(file_list)):

        re_file_name = result_path + init_file_names[pair] + '_Data_CRe.dat'
        file_size = os.stat(re_file_name).st_size
        num_of_spectra = int((file_size - 1024) / (8 * freq_points_num))
        re_data = read_dat_file_for_carlibration(re_file_name, num_of_spectra, freq_points_num)
        print(re_file_name)

        im_file_name = result_path + init_file_names[pair] + '_Data_CIm.dat'
        im_data = read_dat_file_for_carlibration(im_file_name, num_of_spectra, freq_points_num)

        cross_sp_phase = np.arctan2(im_data, re_data)
        # cross_sp_phase = corr_phase[:, 0]
        cross_sp_phase = np.mean(cross_sp_phase, axis=1)
        cross_sp_angl.append(cross_sp_phase)

        cross_sp_module = 10 * np.log10((re_data ** 2 + im_data ** 2) ** 0.5)
        # cross_sp_module = corr_phase[:, 0]
        cross_sp_module = np.mean(cross_sp_module, axis=1)
        cross_sp_ampl.append(cross_sp_module)

    fig, axs = plt.subplots(1, 1)
    for i in range(len(file_list)):
        axs.plot(cross_sp_angl[i])
    axs.set_ylim(-3.15, 3.15)
    pylab.savefig('Cross-spectra phase'+'.png', bbox_inches='tight', dpi=160)

    fig, axs = plt.subplots(1, 1)
    for i in range(len(file_list)):
        axs.plot(cross_sp_ampl[i])
    # axs.set_ylim(-3.15, 3.15)
    pylab.savefig('Cross-spectra magnitude'+'.png', bbox_inches='tight', dpi=160)


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

    end_time = time.time()
    print('\n\n  The program execution lasted for ', round((end_time - start_time), 2), 'seconds (',
                                                     round((end_time - start_time)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', software_name, ' has finished! *** \n\n\n')
