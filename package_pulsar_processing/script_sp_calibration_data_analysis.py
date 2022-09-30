software_version = '2022.07.30'
software_name = 'JDS cross-spectra phase calibration data analysis'

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Directory with JDS files to be analyzed
source_directory = '../RA_DATA_ARCHIVE/DSP_cross_spectra_calibration/'
# Directory where DAT and result txt files to be stored (empty string means project directory)
result_directory = source_directory  # ''

do_filtering = True

MaxNsp = 2048                 # Number of spectra to read for one figure
Vmin = -100                   # Lower limit of figure dynamic range
Vmax = -40                    # Upper limit of figure dynamic range
VminNorm = 0                  # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 20                 # Upper limit of figure dynamic range for normalized spectra
VminCorrMag = -150            # Lower limit of figure dynamic range for correlation magnitude spectra
VmaxCorrMag = -30             # Upper limit of figure dynamic range for correlation magnitude spectra
colormap = 'jet'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
custom_dpi = 300              # Resolution of images of dynamic spectra
CorrelationProcess = 1        # Process correlation data or save time?  (1 = process, 0 = save)
longFileSaveAch = 0           # Save data A to long file? (1 = yes, 0 = no)
longFileSaveBch = 0           # Save data B to long file? (1 = yes, 0 = no)
longFileSaveCRI = 1           # Save correlation data (Real and Imaginary) to long file? (1 = yes, 0 = no)
longFileSaveCMP = 0           # Save correlation data (Module and Phase) to long file? (1 = yes, 0 = no)
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
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_ra_data_files_formats.JDS_file_reader import JDS_file_reader
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_processing.filtering import median_filter
# ###############################################################################


def obtain_calibr_matrix_for_2_channel_sp_calibration(path_to_calibr_data, result_directory):
    """
    The function reads 2-channel cross-spectra calibration files (UTR-2/URAN noise generator calibration with a set of
    attenuators) and provides a phase difference txt file for cross-spectra observations calibration
    """

    # Prepare a folder for results
    result_path = result_directory + 'RESULTS_cross-sp_calibr_' + path_to_calibr_data.split('/')[-2] + '/'
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
         df, frequency, freq_points_num, data_block_size] = file_header_jds_read(fname, 0, 0)

        labels.append(df_system_name + ' ' + df_description.replace('_', ' '))
        init_file_names.append(df_filename)

        print('\n  Processing file: ', df_description.replace('_', ' '),
              ',  # ', file_no+1, ' of ', len(file_list), '\n')

        # Run JDS reader for the current folder
        done, dat_file_name, dat_file_types = JDS_file_reader([path_to_calibr_data + file_list[file_no]],
                                                              result_path, MaxNsp, 0,
                                                              20, Vmin, Vmax, VminNorm, VmaxNorm,
                                                              VminCorrMag, VmaxCorrMag, colormap, custom_dpi,
                                                              CorrelationProcess, longFileSaveAch, longFileSaveBch,
                                                              longFileSaveCRI, longFileSaveCMP, 0,
                                                              0, 0, 0, 0, 0, dat_files_path=result_path,
                                                              print_or_not=0)

    def read_dat_file_for_calibration(file_name, num_of_spectra, freq_points_num):
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
        re_data = read_dat_file_for_calibration(re_file_name, num_of_spectra, freq_points_num)
        print(re_file_name)

        im_file_name = result_path + init_file_names[pair] + '_Data_CIm.dat'
        im_data = read_dat_file_for_calibration(im_file_name, num_of_spectra, freq_points_num)

        cross_sp_phase = np.arctan2(im_data, re_data)
        # cross_sp_phase = corr_phase[:, 0]
        cross_sp_phase = np.mean(cross_sp_phase, axis=1)
        if do_filtering:
            cross_sp_phase = median_filter(cross_sp_phase, 30)
        cross_sp_angl.append(cross_sp_phase)

        cross_sp_module = 10 * np.log10((re_data ** 2 + im_data ** 2) ** 0.5)
        # cross_sp_module = corr_phase[:, 0]
        cross_sp_module = np.mean(cross_sp_module, axis=1)
        if do_filtering:
            cross_sp_module = median_filter(cross_sp_module, 30)
        cross_sp_ampl.append(cross_sp_module)

    # Figures of initial and averaged spectra for each file
    for i in range(len(file_list)):
        rc('font', size=10, weight='bold')
        fig = plt.figure(figsize=(18, 10))
        fig.suptitle('Calibration matrix of waveform signals correlation for ' + file_list[i] +
                     ' (' + labels[i] + ')', fontsize=12, fontweight='bold')
        ax1 = fig.add_subplot(211)
        ax1.set_title('Files: ' + init_file_names[0] + ' - ' + init_file_names[-1], fontsize=12)
        ax1.plot(cross_sp_ampl[i], linestyle='-', linewidth='1.30', label='Cross spectra amplitude')
        ax1.legend(loc='upper right', fontsize=10)
        ax1.set(xlim=(0, freq_points_num-4))
        ax1.set_ylim(-120, -60)
        ax1.set_ylabel('Amplitude, A.U.', fontsize=10, fontweight='bold')
        ax2 = fig.add_subplot(212)
        ax2.plot(cross_sp_angl[i], linestyle='-', linewidth='1.30', label='Cross spectra phase')
        ax2.set(xlim=(0, freq_points_num-4))
        ax2.set_ylim(-3.15, 3.15)
        ax2.set_xlabel('Frequency channels, #', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Phase, rad', fontsize=10, fontweight='bold')
        ax2.legend(loc='upper right', fontsize=10)
        fig.subplots_adjust(hspace=0.07, top=0.94)
        pylab.savefig(result_path + 'Signal_cross-spectra_' + init_file_names[i] + '.png', bbox_inches='tight', dpi=160)
        plt.close('all')

    # Plot cross spectra matrix
    rc('font', size=10, weight='bold')
    fig = plt.figure(figsize=(18, 10))
    fig.suptitle('Cross spectra calibration matrix', fontsize=12, fontweight='bold')
    ax1 = fig.add_subplot(211)
    ax1.set_title('Files: ' + init_file_names[0] + ' - ' + init_file_names[-1], fontsize=12)
    for i in range(len(cross_sp_ampl)):
        ax1.plot(cross_sp_ampl[i], linestyle='-', linewidth='1.30', label=labels[i]+' '+init_file_names[i])
    ax1.legend(loc='upper right', fontsize=10)
    ax1.set(xlim=(0, freq_points_num-4))
    ax1.set_ylim(-120, -60)
    ax1.set_ylabel('Amplitude, A.U.', fontsize=10, fontweight='bold')
    ax2 = fig.add_subplot(212)
    for i in range(len(cross_sp_angl)):
        ax2.plot(cross_sp_angl[i], linestyle='-', linewidth='1.30', label=labels[i])
    ax2.set(xlim=(0, freq_points_num-4))
    ax2.set_ylim(-3.15, 3.15)
    ax2.set_xlabel('Frequency channels, #', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Phase, rad', fontsize=10, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=10)
    fig.subplots_adjust(hspace=0.07, top=0.94)
    pylab.savefig(result_path + 'Cross_spectra_calibration_matrix.png', bbox_inches='tight', dpi=160)
    plt.close('all')

    # Save phase matrix to txt files
    for i in range(len(file_list)):
        phase_txt_file = open(result_path + 'Calibration_' + init_file_names[i] + '_cross_spectra_phase.txt', "w")
        for freq in range(freq_points_num-4):
            phase_txt_file.write(''.join(' {:+12.7E}'.format(cross_sp_angl[i][freq])) + ' \n')
        phase_txt_file.close()


# ###############################################################################
# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    print('\n\n\n\n\n\n\n\n   **********************************************************************')
    print('   * ', software_name, ' v.', software_version, ' *      (c) YeS 2022')
    print('   ********************************************************************** \n\n\n')

    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")
    print('  Today is ', current_date, ' time is ', current_time, '\n')

    obtain_calibr_matrix_for_2_channel_sp_calibration(source_directory, result_directory)

    end_time = time.time()
    print('\n\n  The program execution lasted for ', round((end_time - start_time), 2), 'seconds (',
                                                     round((end_time - start_time)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', software_name, ' has finished! *** \n\n\n')
