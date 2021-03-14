# Python3
# pip install progress
Software_version = '2021.01.25'
Software_name = 'JDS Waveform coherent dispersion delay removing'
# Script intended to convert data from DSPZ receivers in waveform mode to waveform float 32 files
# and make coherent dispersion delay removing and saving found pulses
# !!! Time possibly is not correct !!!
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
pulsar_name = 'B0809+74'  # 'B0809+74' 'B0950+08' 'B1133+16'

make_sum = True
dm_step = 1.0
no_of_points_for_fft_spectr = 16384     # Number of points for FFT on result spectra # 8192, 16384, 32768, 65536, 131072
no_of_points_for_fft_dedisp = 16384     # Number of points for FFT on dedispersion # 8192, 16384, 32768, 65536, 131072
no_of_spectra_in_bunch = 16384          # Number of spectra samples to read while conversion to dat (depends on RAM)
no_of_bunches_per_file = 16             # Number of bunches to read one WF file (depends on RAM)
source_directory = 'DATA/'              # Directory with JDS files to be analyzed
result_directory = ''                   # Directory where DAT files to be stored (empty string means project directory)
calibrate_phase = True                  # Do we need to calibrate phases between two channels? (True/False)
median_filter_window = 80               # Window of median filter to smooth the average profile

phase_calibr_txt_file = 'DATA/Calibration_E261015_044242.jds_cross_spectra_phase.txt'

show_av_sp_to_normalize = False         # Pause and display filtered average spectrum to be used for normalization
use_window_for_fft = False              # Use FFT window (not finished)

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import shutil
import sys
import time
import numpy as np
from os import path
from time import gmtime, strftime

# To change system path to main source_directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import pulsar_period_DM_compensated_pics
from package_pulsar_processing.f_cut_needed_pulsar_period_from_dat import cut_needed_pulsar_period_from_dat
from package_pulsar_processing.pulsar_DM_full_shift_calculation import DM_full_shift_calc
from package_pulsar_processing.f_coherent_wf_to_wf_dedispersion import coherent_wf_to_wf_dedispersion
from package_pulsar_processing.f_cut_needed_time_points_from_txt import cut_needed_time_points_from_txt
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_ra_data_files_formats.f_convert_jds_wf_to_wf32 import convert_jds_wf_to_wf32
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_ra_data_files_formats.f_convert_wf32_to_dat import convert_wf32_to_dat_with_overlap
from package_ra_data_files_formats.f_convert_wf32_to_dat import convert_wf32_to_dat_without_overlap

from package_ra_data_processing.wf32_two_channel_phase_calibration import wf32_two_channel_phase_calibration
from package_ra_data_processing.sum_signals_of_wf32_files import sum_signals_of_wf32_files
from package_ra_data_processing.f_normalize_dat_file import normalize_dat_file


# *******************************************************************************
#                            M A I N    P R O G R A M                           *
# *******************************************************************************


if __name__ == '__main__':

    print('\n\n\n\n\n\n\n\n   ********************************************************************')
    print('   * ', Software_name, ' v.', Software_version, ' *      (c) YeS 2020')
    print('   ******************************************************************** \n\n')
    
    start_time = time.time()
    print('  Today is ', time.strftime("%d.%m.%Y"), ' time is ', time.strftime("%H:%M:%S"), '\n\n')

    # Take pulsar parameters from catalogue
    pulsar_ra, pulsar_dec, pulsar_dm, p_bar = catalogue_pulsar(pulsar_name)

    # Calculation of the maximal time shift for dispersion delay removing
    shift_vector = DM_full_shift_calc(8192, 16.5, 33.0, 2014 / pow(10, 6), 0.000496, pulsar_dm, 'jds')
    max_shift = np.abs(shift_vector[0])
    print('  * Maximal shift of dynamic spectrum: ', max_shift, ' points')
    print('                                  or : ', max_shift * 0.000496, ' seconds')

    # Reading initial jds file list to save the list of files in the result folder
    file_list = find_files_only_in_current_folder(source_directory, '.jds', 0)

    print('\n\n  * Converting waveform from JDS to WF32 format... \n\n')

    initial_wf32_files = convert_jds_wf_to_wf32(source_directory, result_directory, no_of_bunches_per_file)
    print('\n List of WF32 files: ', initial_wf32_files, '\n')

    #
    #
    # initial_wf32_files = ['E150221_203844.jds_Data_chA.wf32', 'E150221_203844.jds_Data_chB.wf32']
    #
    #

    if len(initial_wf32_files) > 1 and calibrate_phase:
        print('\n\n  * Making phase calibration of wf32 file... \n')
        wf32_two_channel_phase_calibration(initial_wf32_files[1], no_of_points_for_fft_dedisp, no_of_spectra_in_bunch,
                                           phase_calibr_txt_file)

    #
    #
    # initial_wf32_files = ['E150221_231756.jds_Data_chA.wf32', 'E150221_231756.jds_Data_chB.wf32']
    #
    #

    if len(initial_wf32_files) > 1 and make_sum:
        print('\n\n  * Making sum of two WF32 files... \n')
        file_name = sum_signals_of_wf32_files(initial_wf32_files[0], initial_wf32_files[1], no_of_spectra_in_bunch)
        print('  Sum file:', file_name, '\n')
        typesOfData = ['wfA+B']
    else:
        file_name = initial_wf32_files[0]  # [0] or [1]
        typesOfData = ['chA']  # ['chA'] or ['chB']

    print('\n\n  * Making coherent dispersion delay removing... \n')

    #
    #
    # pulsar_dm = 0.755  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # file_name = 'DM_5.0_E150221_203828.jds_Data_wfA+B.wf32'
    # typesOfData = ['wfA+B']
    #
    #

    for i in range(int(pulsar_dm // dm_step)):  #
        t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print('\n Step ', i+1, ' of ', int((pulsar_dm // dm_step) + 1), ' started at: ', t, '\n')
        file_name = coherent_wf_to_wf_dedispersion(dm_step, file_name, no_of_points_for_fft_dedisp)
    print('\n Last step of ', np.round(pulsar_dm % dm_step, 6), ' pc/cm3 \n')
    file_name = coherent_wf_to_wf_dedispersion(pulsar_dm % dm_step, file_name, no_of_points_for_fft_dedisp)
    print('\n List of WF32 files with removed dispersion delay: ', file_name, '\n')

    #
    #
    # pulsar_dm = 5.755  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # file_name = 'DM_5.752_E150221_203739.jds_Data_wfA+B.wf32'
    # typesOfData = ['wfA+B']
    #
    #

    # Correction of file names for further processing with timeline files (made for wfA+B case)
    current_tl_fname = file_name + '_Timeline.wtxt'
    correct_tl_fname = file_name.split('.jds')[0] + '.jds_Timeline.wtxt'
    shutil.copyfile(current_tl_fname, correct_tl_fname)
    print('  Current time line file name:', current_tl_fname)
    print('  Correct time line file name:', correct_tl_fname)

    t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
    print('\n\n', t, 'Making DAT files spectra of dedispersed wf32 data... \n')

    #
    #
    # file_name = 'DM_5.755_E280120_205546.jds_Data_chA.wf32'
    # typesOfData = ['chA']
    #
    #

    # file_name = convert_wf32_to_dat_without_overlap(file_name, no_of_points_for_fft_spectr, no_of_spectra_in_bunch)
    file_name = convert_wf32_to_dat_with_overlap(file_name, no_of_points_for_fft_spectr,
                                                 no_of_spectra_in_bunch, use_window_for_fft)

    print('\n Dedispersed DAT file: ', file_name, '\n')
    
    #
    #
    # file_name = 'DM_2.972_E150221_213204.jds_Data_wfA+B.dat'
    # typesOfData = ['wfA+B']
    #
    #

    t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
    print('\n\n', t, 'Making normalization of the dedispersed spectra data... \n')

    output_file_name = normalize_dat_file('', file_name, no_of_spectra_in_bunch,
                                          median_filter_window, show_av_sp_to_normalize)

    print(' Files names after normalizing: ', output_file_name)

    t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
    print('\n\n', t, 'Making figures of 3 pulsar periods... \n\n')

    pulsar_period_DM_compensated_pics('', output_file_name, pulsar_name, 0, -0.15, 0.55, -0.2, 3.0, 3, 500,
                                      'Greys', False, 0.25)

    #
    #
    # output_file_name = 'Norm_DM_5.755_E280120_205546.jds_Data_chA.dat'
    # typesOfData = ['chA']
    #
    #

    t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
    print('\n\n', t, 'Making dynamic spectra figures of the dedispersed data... \n')

    result_folder_name = source_directory.split('/')[-2] + '_dedispersed'
    file_name = output_file_name.split('_Data_', 1)[0]  # + '.dat'
    ok = DAT_file_reader('', file_name, typesOfData, '', result_folder_name, 0, 0, 0, -120, -10, 0, 6, 6, 300, 'jet',
                         0, 0, 0, 20 * 10 ** (-12), 16.5, 33.0, '', '', 16.5, 33.0, [], 0)

    #
    #
    # output_file_name = 'Norm_DM_5.755_E261015_035701.jds_Data_wfA+B.dat'
    #
    #

    t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
    print('\n\n', t, 'Cutting the data of found pulse period from whole data... ')
    print('\n\n  Examine 3 pulses pics and enter the number of period to cut:')

    #  Manual input of the pulsar period where pulse is found
    period_number = int(input('\n    Enter the number of period where the pulse is:  '))
    periods_per_fig = int(input('\n    Enter the length of wanted data in periods:     '))

    path, txt_fname, png_fname = cut_needed_pulsar_period_from_dat('', output_file_name, pulsar_name, period_number,
                                                                   -0.15, 0.55, -0.2, 3.0,
                                                                   periods_per_fig, 500, 'Greys')
    #
    #
    #
    #
    #
    
    t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
    print('\n\n', t, 'Cutting the data of pulse from pulsar period data... \n')

    start_point, end_point = cut_needed_time_points_from_txt(path, txt_fname)
    
    # Save initial jds files list to a txt file
    jds_files_txt = open(path + '/Initial data files used.txt', "w")
    jds_files_txt.write('Period # ' + str(period_number) + ', points: ' + str(start_point) + ' - ' +
                        str(end_point) + ' of ' + str(len(file_list)) + ' data files: \n')
    for item in range(len(file_list)):
        jds_files_txt.write(file_list[item] + ' \n')
    jds_files_txt.close()

    end_time = time.time()
    print('\n\n  The program execution lasted for ',
          round((end_time - start_time), 2), 'seconds (', round((end_time - start_time)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
