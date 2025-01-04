# Same as package_pulsar_processing/script_sp_pulsar_and_transient_search.py but optimized to be used in GUI program

import os
import sys
import datetime
import numpy as np
from os import path
from tqdm import tqdm
import multiprocessing 

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_ra_data_files_formats.f_jds_file_read import jds_file_reader
from package_cleaning.dat_rfi_mask_making import dat_rfi_mask_making
from package_pulsar_processing.pulsar_incoherent_dedispersion import pulsar_incoherent_dedispersion

from package_pulsar_processing.pulsar_incoherent_dedispersion import pulsar_incoherent_dedispersion
from package_pulsar_processing.incoherent_dedispersion import incoherent_dedispersion
from package_pulsar_processing.time_profiles_allignment import align_time_profiles, read_and_plot_var_dm_file
from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import pulsar_period_dm_compensated_pics
from package_pulsar_processing.pulsar_dm_compensated_dynamic_spectra_folding import pulsar_period_folding
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_ra_data_files_formats.f_jds_file_read import jds_file_reader
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_cleaning.dat_rfi_mask_making import dat_rfi_mask_making
from package_ra_data_processing.f_cross_spectra_phase_calibration import cross_spectra_phase_calibration


def make_var_dm_file_from_jds(source_directory, file_name_list_current, result_directory, source_dm):
    
    

    central_dm = 22.5
    dm_range = 12.5
    dm_points = 1251

    time_res = (1 / 66000000) * 16384 * 32     # Time resolution, s  (0.007944 s)
    fig_time = 30           # Time on one figure, s
    n_proc = 1              # Number of processes when making dedispersion (less than CPU cores)

    # Types of data to get (full possible set in the comment below - copy to code necessary)
    # data_types = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm', 'A+B', 'A-B', 'chAdt', 'chBdt']
    data_types = ['chA']

    # Calibration file needed only if cross-spectra are involved
    phase_calibr_txt_file = source_directory + 'Calibration_P130422_114347.jds_cross_spectra_phase.txt'

    save_long_dyn_spectra = True   # Save figures of the whole observation spectrogram?

    colormap = 'Greys'            # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
    custom_dpi = 300              # Resolution of images of dynamic spectra
    longFileSaveCRI = 0           # Save correlation data (Real and Imaginary) to long file? (1 = yes, 0 = no)
    DynSpecSaveInitial = 0        # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
    DynSpecSaveCleaned = 0        # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
    CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
    CorrSpecSaveCleaned = 0       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?


    # *******************************************************************************
    #                     I M P O R T    L I B R A R I E S                          *
    # *******************************************************************************

    # Preparations for automatic processing
    if 'chA' in data_types:
        longFileSaveAch = 1
    else:
        longFileSaveAch = 0

    if 'chB' in data_types:
        longFileSaveBch = 1
    else:
        longFileSaveBch = 0

    longFileSaveCMP = 0

    if 'C_m' in data_types:
        CorrelationProcess = 1
        long_file_save_im_re = 1
    else:
        CorrelationProcess = 0
        long_file_save_im_re = 0

 
    source_directory = os.path.normpath(source_directory)
    result_directory = os.path.normpath(result_directory)

    # Making a DM values vector
    dm_vector = np.linspace(central_dm - dm_range, central_dm + dm_range, num=dm_points)

    # Printing to terminal the DM values vector
    print('\n  DM varies in range from', dm_vector[0], 'to', dm_vector[-1], ', number of points:', dm_points, '\n')
    for i in range(int(len(dm_vector)/2)):
        print(" {:>3}   {:<10}    |    {:<10}   {:>3} ".format(i, np.round(dm_vector[i], 6), np.round(dm_vector[-(i+1)], 6), len(dm_vector)-i-1))

    k = int(len(dm_vector)/2)  # Central value
    print(" {:>3}            {:^10}  ".format(k, np.round(dm_vector[k], 6)))

    # Removing possible values less than 2 pc/cm3 from DM vector
    dm_vector = [elem for elem in dm_vector if elem >= 2]

    print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Making long DAT file of the initial data')

    # Find all jds files in folder:
    file_name_list_current = find_files_only_in_current_folder(source_directory, '.jds', 0)

    # Path to intermediate data files and results
    if result_directory == '':
        result_directory = os.path.dirname(os.path.realpath(__file__))

    # Configuring paths to save intermediate and result files
    result_folder_name = source_directory.split(os.sep)[-1]
    path_to_dat_files = os.path.join(result_directory, 'Transient_search_' + result_folder_name)
    jds_result_path = os.path.join(path_to_dat_files, 'JDS_Results_' + result_folder_name)

    for file in range(len(file_name_list_current)):
        file_name_list_current[file] = os.path.join(source_directory, file_name_list_current[file])


    # # Read data file header
    # with open(filepath, 'rb') as file:
    #     file_header = file.read(1024)
    #
    # # Create a small binary file with header
    # file_data = open(jds_result_path + '/' + filename, 'wb')
    # file_data.write(file_header)
    # file_data.close()
    # del file_header


    #"""

    # Run JDS/ADR reader for the current folder

    done_or_not, dat_file_name, dat_file_list = jds_file_reader(file_name_list_current, jds_result_path, 2048, 0,
                                                                8, -100, -40, 0, 6, -150, -30, colormap, custom_dpi,
                                                                CorrelationProcess, longFileSaveAch, longFileSaveBch,
                                                                long_file_save_im_re, longFileSaveCMP, DynSpecSaveInitial,
                                                                DynSpecSaveCleaned, CorrSpecSaveInitial,
                                                                CorrSpecSaveCleaned, 0, 0, dat_files_path=path_to_dat_files,
                                                                print_verbose=0)
    #
    #
    #
    # dat_file_list = ['chA']
    # dat_file_name = 'P130422_121607.jds'
    #
    #
    #

    # Take only channel A, channel B and Cross Spectra amplitude if present
    data_types_to_process = []
    if 'chA' in dat_file_list and 'chA' in data_types:
        data_types_to_process.append('chA')
    if 'chB' in dat_file_list and 'chB' in data_types:
        data_types_to_process.append('chB')
    if 'CRe' in dat_file_list and 'C_m' in data_types:
        data_types_to_process.append('C_m')


    # Calibrate phase of cross-correlation data if needed
    if 'C_m' in data_types_to_process:

        print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Calibrating cross-spectra data')
        cross_spectra_phase_calibration(path_to_dat_files, dat_file_name, path_to_dat_files, phase_calibr_txt_file, 2048,
                                        save_complex=False, save_module=True, save_phase=True, log_module=False)


    if save_long_dyn_spectra:
        print('\n * ', str(datetime.datetime.now())[:19], ' * DAT reader analyzes file: \n',
            dat_file_name, ', of types:', data_types_to_process, '\n')

        result_folder_name = source_directory.split(os.sep)[-1] + '_initial'
        # result_folder_name = os.path.split(source_directory)[-1] + '_initial'

        ok = DAT_file_reader(path_to_dat_files, dat_file_name, data_types_to_process, path_to_dat_files, result_folder_name,
                            0, 0, 0, -120, -10, 0, 6, 6, 300, 'jet', 0, 0, 0, 20 * 10**(-12), 16.5, 33.0, '', '',
                            16.5, 33.0, [], 0)

    #
    #
    #
    # dat_file_name = 'C250122_214003.jds'
    # data_types_to_process = ['chA']
    #
    #
    #

    # RFI mask making
    print('\n\n * ', str(datetime.datetime.now())[:19], ' * Making mask to clean data \n')

    for i in range(len(data_types_to_process)):
        if data_types_to_process[i] == 'chA' or data_types_to_process[i] == 'chB':
            delta_sigma = 0.005  # 0.05
            n_sigma = 1.0  # 2
            min_l = 20  # 30
        elif data_types_to_process[i] == 'C_m':
            delta_sigma = 0.1
            n_sigma = 5
            min_l = 30
        else:
            sys.exit('            Type error!')

        dat_rfi_mask_making(os.path.join(path_to_dat_files, dat_file_name + '_Data_' + data_types_to_process[i] + '.dat'),
                            1024, lin_data=True, delta_sigma=delta_sigma, n_sigma=n_sigma, min_l=min_l)

    #"""

    #
    #
    # data_types_to_process = ['chA']
    # dat_file_name = 'C240122_152201.jds'
    # dm_vector = np.linspace(22.46, 25, num=128)
    # print(dm_vector[0], dm_vector[1], dm_vector[-1])

    #
    #
    #

    # """
    # Dispersion delay removing in a loop for all values in DM vector
    print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Dispersion delay removing... \n')

    amp_min = -0.15
    amp_max = 0.55
    dedispersed_data_file_list = []
    calculated_dm_vector = []

    
    # Running incoherent dedispersion for many DM values in parallel
    args = (path_to_dat_files,  
            dat_file_name + '_Data_' + data_types_to_process[0] + '.dat',  
            'Transient', 512, amp_min, amp_max, False, 
            16.5, 33.0, True, False, 300, 'Greys')

    kwargs = {"use_mask_file": True, 
            "save_pics": False, 
            "result_path": path_to_dat_files, 
            "print_or_not": False}

    pool = multiprocessing.Pool(processes=n_proc) 

    result_async = tqdm([pool.apply_async(pulsar_incoherent_dedispersion, args, {**{"source_dm": dm}, **kwargs}) for dm in dm_vector]) 

    dedispersed_data_file_list = [r.get() for r in result_async]

    #
    #
    #
    # dedispersed_data_file_list = ['Transient_DM_5.255_P130422_121607.jds_Data_chA.dat']
    #
    #
    #
    # """


    print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Aligning profiles in time and saving array to file... \n\n')

    data_file_name, tl_file_name = align_time_profiles(path_to_dat_files, dat_file_name, data_types_to_process[0], central_dm, dm_range, dm_points)

    # Separate file name and path
    data_path, data_file_name = os.path.split(data_file_name)
    data_path, tl_file_name = os.path.split(tl_file_name)

    # Read and plot the file of various DM tine profiles
    read_and_plot_var_dm_file(path_to_dat_files, data_file_name, tl_file_name, path_to_dat_files,
                              time_res, fig_time, print_or_not=True)

    print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Pipeline finished successfully! \n\n')
