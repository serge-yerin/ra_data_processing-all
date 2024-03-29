# TODO: Correct timeline file making and check correctness of timeline from receiver
# TODO: Add option to delete intermediate data files
# TODO: Add option to process WF data for the full frequency band with 66 MHz clock
# TODO: Correct time resolution for average pulse calculation after last FFT with/without overlap (now correct for "with" case)

# Python3
software_version = '2022.09.11'
software_name = 'JDS Waveform coherent dispersion delay removing'
# Script intended to convert data from DSPZ receivers in waveform mode to waveform float 32 files
# and make coherent dispersion delay removing and save found pulses.
# !!! The coherent dispersion delay removing is not realized properly !!!
# !!! There is a problem with overlapping and window application while FFT after dedispersion !!! 
# You can choose the overlapping/window near line 222 of this script with commenting the function call
# !!! Now works ONLY with 16.5-33.0 MHz data acquired with 33 MHz clock frequency !!!

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Directory with JDS files to be analyzed
source_directory = '../RA_DATA_ARCHIVE/DSP_waveform_33MHz_B0950p08'
# Directory where DAT files and results will be stored
result_directory = '../RA_DATA_RESULTS/'

pulsar_name = 'B0950+08'  # 'B0809+74' # 'B0950+08' # 'B1133+16' # 'J0242+6256'

make_sum = True
dm_step = 1.0
no_of_points_for_fft_spectr = 16384     # Number of points for FFT on result spectra # 8192, 16384, 32768, 65536, 131072
no_of_points_for_fft_dedisp = 16384     # Number of points for FFT on dedispersion # 8192, 16384, 32768, 65536, 131072
no_of_spectra_in_bunch = 16384          # Number of spectra samples to read while conversion to dat (depends on RAM)
no_of_bunches_per_file = 16             # Number of bunches to read one WF file (depends on RAM)
median_filter_window = 80               # Window of median filter to smooth the average profile while normalizing data
calibrate_phase = True                  # Do we need to calibrate phases between two channels? (True/False)

# Phase calibration file (if used, must be in the source_directory near the initial jds files)
phase_calibr_txt_file = 'Calibration_E300120_232956.jds_cross_spectra_phase.txt'

show_av_sp_to_normalize = False         # Pause and display filtered average spectrum to be used for normalization
use_window_for_fft = False              # Use FFT window (to be checked and corrected)

# If only extract pulse from normalized dedispersed dat file, use this True and the name of file, otherwise ignored
only_extract_pulse = False
norm_compensated_dat_file_name = 'Norm_DM_2.972_E310120_225419.jds_Data_wfA+B.dat'

# Parameters for final average spectra folding
scale_factor = 1
spectrum_pic_min = -0.5
spectrum_pic_max = 3
periods_per_fig = 1
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import shutil
import os
import sys
import time
import numpy as np
from os import path
from time import strftime

# To change system path to main source_directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_common_modules.text_manipulations import separate_filename_and_path
from package_ra_data_files_formats.f_convert_jds_wf_to_wf32 import convert_jds_wf_to_wf32
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_ra_data_files_formats.f_convert_wf32_to_dat import convert_wf32_to_dat_with_overlap
from package_ra_data_files_formats.f_convert_wf32_to_dat import convert_wf32_to_dat_without_overlap
from package_ra_data_processing.wf32_two_channel_phase_calibration import wf32_two_channel_phase_calibration
from package_ra_data_processing.sum_signals_of_wf32_files import sum_signals_of_wf32_files
from package_ra_data_processing.f_normalize_dat_file import normalize_dat_file
from package_pulsar_processing.pulsar_dm_compensated_dynamic_spectra_folding import pulsar_period_folding
from package_pulsar_processing.f_cut_needed_time_points_from_txt import cut_needed_time_points_from_dat_to_txt
from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import pulsar_period_dm_compensated_pics
from package_pulsar_processing.f_cut_needed_pulsar_period_from_dat import cut_needed_pulsar_period_from_dat_to_dat
from package_pulsar_processing.pulsar_dm_full_shift_calculation import dm_full_shift_calculate
from package_pulsar_processing.f_coherent_wf_to_wf_dedispersion import coherent_wf_to_wf_dedispersion
# from package_pulsar_processing.f_cut_needed_time_points_from_txt import cut_needed_time_points_from_txt
# from package_pulsar_processing.f_cut_needed_pulsar_period_from_dat import cut_needed_pulsar_period_from_dat

# *******************************************************************************
#                            M A I N    P R O G R A M                           *
# *******************************************************************************


if __name__ == '__main__':

    print('\n\n\n\n\n\n\n\n   ********************************************************************')
    print('   * ', software_name, ' v.', software_version, ' *      (c) YeS 2020')
    print('   ******************************************************************** \n\n')
    
    start_time = time.time()
    print('  Today is ', time.strftime("%d.%m.%Y"), ' time is ', time.strftime("%H:%M:%S"), '\n\n')

    # Take pulsar parameters from catalogue
    pulsar_ra, pulsar_dec, pulsar_dm, p_bar = catalogue_pulsar(pulsar_name)

    # Calculation of the maximal time shift for dispersion delay removing
    shift_vector = dm_full_shift_calculate(8192, 16.5, 33.0, 2014 / pow(10, 6), 0.000496, pulsar_dm, 'jds')
    max_shift = np.abs(shift_vector[0])
    print('  * Pulsar ', pulsar_name)
    print('                   Barycentric period: ', p_bar, 's.')
    print('                   Dispersion measure:  {} pc・cm\u00b3'.format(pulsar_dm))
    print('    Maximal shift of dynamic spectrum: ', max_shift, ' points')
    print('                                  or : ', np.round(max_shift * 16384/33000000, 1), ' seconds')  # nfft/f_cl
    print('                                  or :  ~', int(np.ceil((max_shift * 16384/33000000) / 16)),
          ' files in 2 ch 33 MHz mode\n\n')


    # Preparing result directory
    source_directory = os.path.normpath(source_directory)
    result_directory = os.path.normpath(result_directory)

    result_folder_name = source_directory.split(os.sep)[-1]

    # Path to intermediate data files and results
    if result_directory == '':
        result_directory = os.path.dirname(os.path.realpath(__file__))  # + '/'

    result_directory = os.path.join(result_directory, pulsar_name + '_' + result_folder_name + '_coherent_dedispersion')
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    # Reading initial jds file list to save the list of files in the result folder
    file_list = find_files_only_in_current_folder(source_directory, '.jds', 0)

    #
    #
    # Start commenting lines here!
    #
    #
    # '''

    if not only_extract_pulse:
        t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
        print('\n\n', t, 'Converting waveform from JDS to WF32 format. \n\n')

        initial_wf32_files = convert_jds_wf_to_wf32(source_directory, result_directory, no_of_bunches_per_file)
        print('\n  List of WF32 files:')
        for i in range(len(initial_wf32_files)):
            print('   - ', initial_wf32_files[i])

        #
        #
        # Do not forget to comment variables below!!!
        # initial_wf32_files = ['E261015_035419.jds_Data_chA.wf32']
        #
        #

        if len(initial_wf32_files) > 1 and calibrate_phase:
            t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
            print('\n\n', t, 'Making phase calibration of wf32 file... \n')
            phase_calibr_txt_file = os.path.join(source_directory, phase_calibr_txt_file)
            wf32_two_channel_phase_calibration(initial_wf32_files[1], no_of_points_for_fft_dedisp,
                                               no_of_spectra_in_bunch, phase_calibr_txt_file)

        #
        #
        # Do not forget to comment variables below!!!
        # initial_wf32_files = ['E150221_231756.jds_Data_chA.wf32', 'E150221_231756.jds_Data_chB.wf32']
        #
        #

        if len(initial_wf32_files) > 1 and make_sum:
            t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
            print('\n\n', t, 'Making sum of two WF32 files. \n')
            file_name = sum_signals_of_wf32_files(initial_wf32_files[0], initial_wf32_files[1], no_of_spectra_in_bunch)
            print('\n  Sum file:', file_name, '\n')
            typesOfData = ['wfA+B']
        else:
            file_name = initial_wf32_files[0]  # [0] or [1]
            typesOfData = ['chA']  # ['chA'] or ['chB']

        #
        #
        # Do not forget to comment variables below!!!
        # file_name = os.path.join(result_directory, 'E240621_113029.jds_Data_wfA+B.wf32')
        # typesOfData = ['wfA+B']
        #
        #

        print('\n\n  * Making coherent dispersion delay removing. \n')
        for i in range(int(pulsar_dm // dm_step)):  #
            t = strftime("%Y-%m-%d %H:%M:%S")
            print('\n Step ', i+1, ' of ', int((pulsar_dm // dm_step) + 1), ' started at: ', t, '\n')
            file_name = coherent_wf_to_wf_dedispersion(dm_step, file_name, no_of_points_for_fft_dedisp)
        t = strftime("%Y-%m-%d %H:%M:%S")
        print('\n Last step of ', np.round(pulsar_dm % dm_step, 6), ' pc/cm3 started at: ', t, '\n')
        file_name = coherent_wf_to_wf_dedispersion(pulsar_dm % dm_step, file_name, no_of_points_for_fft_dedisp)
        print('\n List of WF32 files with removed dispersion delay: ', file_name, '\n')

        #
        #
        # Do not forget to comment variables below!!!
        # file_name = 'DM_5.755_E261015_035419.jds_Data_chA.wf32'  # 'DM_5.752_E150221_203739.jds_Data_wfA+B.wf32'
        # typesOfData = ['chA']  # ['wfA+B']
        #
        #

        # Correction of file names for further processing with timeline files (made for wfA+B case)
        if typesOfData == ['wfA+B']:
            current_tl_fname = file_name + '_Timeline.wtxt'
            correct_tl_fname = file_name.split('.jds')[0] + '.jds_Timeline.wtxt'
            shutil.copyfile(current_tl_fname, correct_tl_fname)
            print('  Current time line file name:', current_tl_fname)
            print('  Correct time line file name:', correct_tl_fname)

        #
        #
        # Do not forget to comment variables below!!!
        # file_name = 'DM_2.972_E310120_225419.jds_Data_wfA+B.wf32'
        # typesOfData = ['wfA+B']
        #
        #

        t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
        print('\n\n', t, 'Making DAT files spectra of dedispersed wf32 data. \n')

        file_name = convert_wf32_to_dat_without_overlap(file_name, no_of_points_for_fft_spectr,
                                                        no_of_spectra_in_bunch)
        # file_name = convert_wf32_to_dat_with_overlap(file_name, no_of_points_for_fft_spectr,
                                                    #  int(no_of_spectra_in_bunch/2), use_window_for_fft)

        print('\n Dedispersed DAT file: ', file_name, '\n')

        #
        #
        # file_name = os.path.join(result_directory, 'DM_5.755_E240621_113029.jds_Data_wfA+B.dat')
        # typesOfData = ['wfA+B']
        #
        #

        t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
        print('\n\n', t, 'Making normalization of the dedispersed spectra data. \n')

        file_name = file_name.split(os.sep)[-1]
        output_file_name = normalize_dat_file(result_directory, file_name, no_of_spectra_in_bunch,
                                              median_filter_window, show_av_sp_to_normalize)

        print('\n File names after normalizing: ', output_file_name)

        t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
        print('\n\n', t, 'Making figures of 3 pulsar periods. \n\n')

        pulsar_period_dm_compensated_pics(result_directory, output_file_name, pulsar_name,
                                          0, -0.15, 0.55, -0.2, 3.0, 3, 500, 'Greys', False, 0.25)

        #
        #
        #
        #
        #

        t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
        print('\n\n', t, 'Pulsar folding. \n\n')

        # Separate file path from file name
        [data_directory, output_file_name] = os.path.split(output_file_name)

        # Make an average pulse profile and pulse evolution plot
        pulsar_period_folding(data_directory, output_file_name, result_directory, pulsar_name, scale_factor,
                              spectrum_pic_min, spectrum_pic_max, periods_per_fig, 500, 'Greys',
                              use_mask_file=False, save_pulse_evolution=True)

        #
        #
        # output_file_name = 'Norm_DM_2.972_E310120_225419.jds_Data_wfA+B.dat'
        # typesOfData = ['wfA+B']
        #
        #

        # t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
        # print('\n\n', t, 'Making dynamic spectra figures of the dedispersed data... \n')
        #
        # result_folder_name = source_directory.split('/')[-2] + '_dedispersed'
        # file_name = output_file_name.split('_Data_', 1)[0]  # + '.dat'
        # ok = DAT_file_reader('', file_name, typesOfData, '', result_folder_name, 0, 0, 0, -120, -10, 0, 6, 6,
        #                      300, 'jet', 0, 0, 0, 20 * 10 ** (-12), 16.5, 33.0, '', '', 16.5, 33.0, [], 0)

    else:
        output_file_name = norm_compensated_dat_file_name

    t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
    print('\n\n', t, 'Cutting the data of found pulse period from whole data... ')
    print('\n\n  Examine 3 pulses pics and enter the number of period to cut:')

    #  Manual input of the pulsar period where pulse is found
    period_number = int(input('\n    Enter the number of period where the pulse is:  '))
    periods_per_fig = int(input('\n    Enter the length of wanted data in periods:     '))

    [_, output_file_name] = os.path.split(output_file_name)
    path, dat_fname, png_fname = cut_needed_pulsar_period_from_dat_to_dat(result_directory, output_file_name,
                                                                          pulsar_name, period_number, -0.15, 0.55,
                                                                          -0.2, 3.0, periods_per_fig, 500, 'Greys')

    #
    #
    #
    # path = 'RESULTS_pulsar_extracted_pulse_Norm_DM_2.972_E310120_225419.jds_Data_wfA+B.dat'
    # dat_fname = 'Single_pulse_Norm_DM_2.972_E310120_225419.jds_Data_wfA+B.dat'
    # period_number = 45
    #
    #
    #
    
    t = time.strftime(" %Y-%m-%d %H:%M:%S : ")
    print('\n\n', t, 'Cutting the data of pulse from pulsar period data... \n')
    start_point, end_point = cut_needed_time_points_from_dat_to_txt(path, dat_fname)

    #
    #
    #
    #
    #

    # Save initial jds files list to a txt file
    jds_files_txt = open(os.path.join(path, 'Initial data files used.txt'), "w")
    jds_files_txt.write('Period # ' + str(period_number) + ', points: ' + str(start_point) + ' - ' +
                        str(end_point) + ' of ' + str(len(file_list)) + ' data files: \n')
    for item in range(len(file_list)):
        jds_files_txt.write(file_list[item] + ' \n')
    jds_files_txt.close()

    #
    #
    #
    #
    #

    end_time = time.time()
    print('\n\n  The program execution lasted for ',
          round((end_time - start_time), 2), 'seconds (', round((end_time - start_time)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', software_name, ' has finished! *** \n\n\n')
