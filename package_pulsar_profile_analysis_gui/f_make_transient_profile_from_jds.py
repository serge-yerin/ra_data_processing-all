import os
import sys
import numpy as np
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_ra_data_files_formats.f_jds_file_read import jds_file_reader
from package_cleaning.dat_rfi_mask_making import dat_rfi_mask_making
from package_pulsar_processing.pulsar_incoherent_dedispersion import pulsar_incoherent_dedispersion


def make_transient_profile_from_jds(source_directory, file_name_list_current, result_directory, source_dm):

    # data_types = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm', 'A+B', 'A-B', 'chAdt', 'chBdt']
    data_types = ['chA']

    colormap = 'Greys'  # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
    custom_dpi = 300  # Resolution of images of dynamic spectra
    DynSpecSaveInitial = 0  # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
    DynSpecSaveCleaned = 0  # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
    CorrSpecSaveInitial = 0  # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
    CorrSpecSaveCleaned = 0  # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?

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
    CorrelationProcess = 0
    long_file_save_im_re = 0

    # result_folder_name = source_directory.split('/')[-2]
    result_folder_name = source_directory.split(os.sep)[-1]
    # path_to_dat_files = result_directory + '/' + 'Transient_search_' + result_folder_name + '/'
    path_to_dat_files = os.path.join(result_directory, 'Transient_search_' + result_folder_name)
    # result_path = path_to_dat_files + 'JDS_Results_' + result_folder_name
    result_path = os.path.join(path_to_dat_files, 'JDS_Results_' + result_folder_name)

    for file in range(len(file_name_list_current)):
        file_name_list_current[file] = source_directory + file_name_list_current[file]

    # Run JDS/ADR reader for the current folder
    done_or_not, dat_file_name, dat_file_list = jds_file_reader(file_name_list_current, result_path, 2048, 0,
                                                                8, -100, -40, 0, 6, -150, -30, colormap, custom_dpi,
                                                                CorrelationProcess, longFileSaveAch, longFileSaveBch,
                                                                long_file_save_im_re, longFileSaveCMP,
                                                                DynSpecSaveInitial,
                                                                DynSpecSaveCleaned, CorrSpecSaveInitial,
                                                                CorrSpecSaveCleaned, 0, 0,
                                                                dat_files_path=path_to_dat_files,
                                                                print_verbose=0)

    # Take only channel A, channel B and Cross Spectra amplitude if present
    data_types_to_process = []
    if 'chA' in dat_file_list and 'chA' in data_types:
        data_types_to_process.append('chA')
    if 'chB' in dat_file_list and 'chB' in data_types:
        data_types_to_process.append('chB')
    if 'CRe' in dat_file_list and 'C_m' in data_types:
        data_types_to_process.append('C_m')

    # RFI mask making
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

        dat_rfi_mask_making(path_to_dat_files + dat_file_name + '_Data_' + data_types_to_process[i] + '.dat',
                            1024, lin_data=True, delta_sigma=delta_sigma, n_sigma=n_sigma, min_l=min_l,
                            print_or_not=False)

    dedispersed_data_file_name = pulsar_incoherent_dedispersion(path_to_dat_files, dat_file_name + '_Data_' +
                                                                data_types_to_process[0] + '.dat', 'Transient', 512,
                                                                -0.15,  0.55, False, 16.5, 33.0, True, False, 300,
                                                                'Greys', use_mask_file=True, save_pics=False,
                                                                source_dm=source_dm,
                                                                result_path=path_to_dat_files, print_or_not=False)

    
    # data_filepath = path_to_dat_files + dat_file_name + '_Data_' + data_types_to_process[0] + '.dat'
    data_filepath = os.path.join(path_to_dat_files, dat_file_name + '_Data_' + data_types_to_process[0] + '.dat')
    
    # data_filename = data_filepath.split('/')[-1]
    data_filename = data_filepath.split(os.sep)[-1]

    # profile_txt_file_path = path_to_dat_files + 'Transient_DM_' + str(np.round(source_dm, 6)) + '_' + \
        # data_filename[:-4] + '_time_profile.txt'
    profile_txt_file_path = os.path.join(path_to_dat_files + 'Transient_DM_' + 
                                         str(np.round(source_dm, 6)) + '_' + data_filename[:-4] + '_time_profile.txt')

    # profile_txt_file_path = profile_txt_file_path.replace('//', '/')

    # common_path = '../../../RA_DATA_ARCHIVE/ADDITIONAL_pulses_profiles/'
    # filename = 'B0329+54_DM_26.78_C240122_152201.jds_Data_chA_time_profile.txt'
    # profile_txt_file_path = common_path + filename

    return profile_txt_file_path


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':
    source_directory = 'E:/RA_DATA_ARCHIVE/DSP_spectra_pulsar_UTR2_B0809+74/'
    file_name_list_current = ['E300117_180000.jds', 'E300117_180841.jds']
    result_directory = 'E:/'
    source_dm = 5.755

    a = make_transient_profile_from_jds(source_directory, file_name_list_current, result_directory, source_dm)