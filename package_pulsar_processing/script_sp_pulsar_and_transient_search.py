
# Python3
software_version = '2022.09.30'
software_name = 'Transient Search Script'
"""
The main goal to the script is to analyze of (cross)spectra transient or pulsar data to find anomalously intense 
pulses during observation session. It reads the (cross)spectra files, saves dynamic spectra pics of each file and the 
whole observation, than runs the incoherent dispersion delay removing for a rage of DM values, saves dynamic 
spectra pics for each max DM delay time. 
"""
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Directory of files to be analyzed:
source_directory = '../../RA_DATA_ARCHIVE/DSP_spectra_pulsar_UTR2_B0950+08/'
result_directory = '../../RA_DATA_RESULTS'

central_dm = 2.972
dm_range = 0.2
dm_points = 11
batch_factor = 20

# Types of data to get (full possible set in the comment below - copy to code necessary)
# data_types = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm', 'A+B', 'A-B', 'chAdt', 'chBdt']
data_types = ['chA']

# Calibration file needed only if cross-spectra are involved
phase_calibr_txt_file = source_directory + 'Calibration_P130422_114347.jds_cross_spectra_phase.txt'

# periods_per_fig = 1           # Number of periods on averaged (folded) pulse profile
# scale_factor = 10             # Scale factor to interpolate data (depends on RAM, use 1, 10, 30)

save_long_dyn_spectra = False   # Save figures of the whole observation spectrogram?
# save_n_period_pics = False    # Save n-period pictures?
# save_strongest = True         # Save strongest images to additional separate folder?
# threshold = 0.25              # Threshold of the strongest pulses (or RFIs)

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
import os
import sys
import datetime
import numpy as np
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_pulsar_processing.pulsar_incoherent_dedispersion import pulsar_incoherent_dedispersion
from package_pulsar_processing.incoherent_dedispersion import incoherent_dedispersion
from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import pulsar_period_dm_compensated_pics
from package_pulsar_processing.pulsar_dm_compensated_dynamic_spectra_folding import pulsar_period_folding
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_ra_data_files_formats.JDS_file_reader import JDS_file_reader
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_cleaning.dat_rfi_mask_making import dat_rfi_mask_making
from package_ra_data_processing.f_cross_spectra_phase_calibration import cross_spectra_phase_calibration
# ###############################################################################

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

#
#
#
#
print('\n\n\n\n   ***************************************************************************')
print('   *               ', software_name, ' v.', software_version, '                  *      (c) YeS 2022')
print('   *************************************************************************** \n')

dm_vector = np.linspace(central_dm - dm_range, central_dm + dm_range, num=dm_points)
print('  DM varies in range from', dm_vector[0], 'to', dm_vector[-1], ', number of points:', dm_points)
print(dm_vector)
print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Making dynamic spectra of the initial data')

# # Find all files in folder once more:
# file_name_list_current = find_files_only_in_current_folder(source_directory, '.jds', 0)

result_folder_name = source_directory.split('/')[-2]

# Path to intermediate data files and results
if result_directory == '':
    result_directory = os.path.dirname(os.path.realpath(__file__))  # + '/'
#
path_to_dat_files = result_directory + '/' + 'Transient_search_' + result_folder_name + '/'

# result_path = path_to_dat_files + 'JDS_Results_' + result_folder_name
#
# for file in range(len(file_name_list_current)):
#     file_name_list_current[file] = source_directory + file_name_list_current[file]
#
# # Run JDS/ADR reader for the current folder
#
# done_or_not, dat_file_name, dat_file_list = JDS_file_reader(file_name_list_current, result_path, 2048, 0,
#                                                             8, -100, -40, 0, 6, -150, -30, colormap, custom_dpi,
#                                                             CorrelationProcess, longFileSaveAch, longFileSaveBch,
#                                                             long_file_save_im_re, longFileSaveCMP, DynSpecSaveInitial,
#                                                             DynSpecSaveCleaned, CorrSpecSaveInitial,
#                                                             CorrSpecSaveCleaned, 0, 0, dat_files_path=path_to_dat_files,
#                                                             print_or_not=0)
#
# # dat_file_list = ['chA', 'chB', 'CRe', 'CIm']
# # dat_file_name = 'P130422_121607.jds'
#
#
# # Take only channel A, channel B and Cross Spectra amplitude if present
# data_types_to_process = []
# if 'chA' in dat_file_list and 'chA' in data_types:
#     data_types_to_process.append('chA')
# if 'chB' in dat_file_list and 'chB' in data_types:
#     data_types_to_process.append('chB')
# if 'CRe' in dat_file_list and 'C_m' in data_types:
#     data_types_to_process.append('C_m')
#
#
# # Calibrate phase of cross-correlation data if needed
# if 'C_m' in data_types_to_process:
#
#     print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Calibrating cross-spectra data')
#     cross_spectra_phase_calibration(path_to_dat_files, dat_file_name, path_to_dat_files, phase_calibr_txt_file, 2048,
#                                     save_complex=False, save_module=True, save_phase=True, log_module=False)
#
#
# if save_long_dyn_spectra:
#     print('\n * ', str(datetime.datetime.now())[:19], ' * DAT reader analyzes file: \n',
#           dat_file_name, ', of types:', data_types_to_process, '\n')
#
#     result_folder_name = source_directory.split('/')[-2] + '_initial'
#
#     ok = DAT_file_reader(path_to_dat_files, dat_file_name, data_types_to_process, path_to_dat_files, result_folder_name,
#                          0, 0, 0, -120, -10, 0, 6, 6, 300, 'jet', 0, 0, 0, 20 * 10**(-12), 16.5, 33.0, '', '',
#                          16.5, 33.0, [], 0)

#
#
#
# dat_file_name = 'C250122_214003.jds'
# data_types_to_process = ['chA']
#
#

# # RFI mask making
# print('\n\n * ', str(datetime.datetime.now())[:19], ' * Making mask to clean data \n')
#
# for i in range(len(data_types_to_process)):
#     if data_types_to_process[i] == 'chA' or data_types_to_process[i] == 'chB':
#         delta_sigma = 0.05
#         n_sigma = 2
#         min_l = 30
#     elif data_types_to_process[i] == 'C_m':
#         delta_sigma = 0.1
#         n_sigma = 5
#         min_l = 30
#     else:
#         sys.exit('            Type error!')
#
#     dat_rfi_mask_making(path_to_dat_files + dat_file_name + '_Data_' + data_types_to_process[i] + '.dat',
#                         1024, lin_data=True, delta_sigma=delta_sigma, n_sigma=n_sigma, min_l=min_l)


#
#
data_types_to_process = ['chA']
# path_to_dat_files = '../B1919+21_DSP_spectra_pulsar_UTR2_B1919+21/'
dat_file_name = 'C250122_214003.jds'
#
#

# Dispersion delay removing
print('\n\n  * ', str(datetime.datetime.now())[:19], ' * First dispersion delay removing... \n\n')

amp_min = -0.15
amp_max = 0.55
dedispersed_data_file_list = []

for i in range(len(data_types_to_process)):

    dedispersed_data_file_name = pulsar_incoherent_dedispersion(path_to_dat_files, dat_file_name + '_Data_' +
                                                                data_types_to_process[i] + '.dat', 'Transient', 512,
                                                                amp_min, amp_max, 0, 0.0, 16.5, True, True, 300,
                                                                'Greys', use_mask_file=True, save_pics=False,
                                                                transient_dm=dm_vector[0],
                                                                result_path=path_to_dat_files)

    dedispersed_data_file_list.append(dedispersed_data_file_name)


for k in range(dm_points-2):

    current_add_dm = dm_vector[k + 1] - dm_vector[0]
    print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Dispersion delay removing step ', k+1, ' of ', dm_points-1,
          ' DM: ', np.round(current_add_dm, 6), ' pc / cm3 \n\n')

    dedispersed_data_file_name = incoherent_dedispersion(path_to_dat_files, 'Transient_DM_2.472_' + dat_file_name +
                                                         '_Data_' + data_types_to_process[0] + '.dat', current_add_dm,
                                                         'Transient', batch_factor,
                                                         512, amp_min, amp_max, 0, 0.0, 16.5, True, False, 300, 'Greys',
                                                         start_dm=dm_vector[0], use_mask_file=True,
                                                         result_path=path_to_dat_files)


print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Pipeline finished successfully! \n\n')
