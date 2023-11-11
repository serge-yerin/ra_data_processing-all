# TODO: add option to delete internal data files
# TODO: calculate the total data loss from cleaning
# TODO: save pics of data with compensated delay applying mask as well
# TODO: make similar pipeline, but starting from cutting into periods and averaging and then delay compensation

# Python3
software_name = 'Pulses Incoherent Averaging Script'
software_version = '2023.11.10'
"""
The main goal to the script is to analyze of (cross)spectra pulsar data to find anomalously intense pulses during 
observation session. It reads the (cross)spectra files, saves dynamic spectra pics of each file and the 
whole observation, than runs the incoherent dispersion delay removing, saves dynamic spectra pics for 
each max DM delay time, and then makes pics of each 3 pulsar periods. 
"""
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Directory of files to be analyzed:
source_directory = '../../RA_DATA_ARCHIVE/DSP_cross_spectra_B0809+74_URAN2'
# Directory where all results will be stored:
result_directory = '../../RA_DATA_RESULTS/'

# 'B0329+54' 'B0809+74' # 'B0950+08' # 'B1133+16' # 'B1604-00' # 'B1919+21' # 'J0242+6256' # 'J2325-0530' # 'J2336-01'
pulsar_name = 'B0809+74'

# Types of data to get (full possible set in the comment below - copy to list the necessary ones)
# data_types = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm', 'A+B', 'A-B']
data_types = ['chA', 'chB', 'A+B']

# Calibration file needed only if cross-spectra are involved, should be in source directory
phase_calibr_txt_file = 'Calibration_P130422_114347.jds_cross_spectra_phase.txt'

periods_per_fig = 1            # Number of periods on averaged (folded) pulse profile
scale_factor = 10              # Scale factor to interpolate data (depends on RAM, use 1, 10, 30)

save_long_dyn_spectra = True   # Save figures of the whole observation spectrogram?
save_n_period_pics = True      # Save n-period pictures?
threshold = 0.25               # Threshold of the strongest pulses (or RFIs)

colormap = 'Greys'             # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
custom_dpi = 300               # Resolution of images of dynamic spectra
DynSpecSaveInitial = 0         # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 0         # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0        # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 0        # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?

# SMD analysis parameters
no_of_dm_steps = 721             # Number of DM steps to plot (361)
dm_var_step = 0.001              # Step of optimal DM finding  (0.002)
frequency_cuts = [18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0]  # UTR-2 16.5 - 33 MHz divided bands of 2 MHz or less

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import os
import sys
import datetime
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_pulsar_processing.pulsar_incoherent_dedispersion import pulsar_incoherent_dedispersion
from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import pulsar_period_dm_compensated_pics
from package_pulsar_processing.pulsar_dm_compensated_dynamic_spectra_folding import pulsar_period_folding
from package_pulsar_processing.script_smd_integrated_pulses_analyzer import smd_integrated_pulses_analyzer
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

if 'A+B' in data_types:
    longFileSaveAch = 1
    longFileSaveBch = 1
    long_file_sum = True
else:
    long_file_sum = False

longFileSaveCMP = 0

if 'C_m' in data_types:
    CorrelationProcess = 1
    long_file_save_im_re = 1
    phase_calibr_txt_file = os.path.join(source_directory, phase_calibr_txt_file)
    assert os.path.isfile(phase_calibr_txt_file), 'There is no calibration file found'
else:
    CorrelationProcess = 0
    long_file_save_im_re = 0

#
#
#
#
print('\n\n\n\n   ***************************************************************************')
print('   *          ', software_name, ' v.', software_version, '            *      (c) YeS 2023')
print('   *************************************************************************** \n')


print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Making  long dynamic spectra file of the initial data')

# Find all files in folder once more:
file_name_list_current = find_files_only_in_current_folder(source_directory, '.jds', 0)

source_directory = os.path.normpath(source_directory)
result_folder_name = source_directory.split(os.sep)[-1]

# Path to intermediate data files and results
if result_directory == '':
    result_directory = os.path.dirname(os.path.realpath(__file__))  # + '/'

result_directory = os.path.normpath(result_directory)
path_to_dat_files = os.path.join(result_directory, pulsar_name + '_' + result_folder_name)

result_path = os.path.join(path_to_dat_files, 'JDS_Results_' + result_folder_name)

for file in range(len(file_name_list_current)):
    file_name_list_current[file] = os.path.join(source_directory, file_name_list_current[file])

# Run JDS/ADR reader for the current folder

done_or_not, dat_file_name, dat_file_list = JDS_file_reader(file_name_list_current, result_path, 2048, 0,
                                                            8, -100, -40, 0, 6, -150, -30,
                                                            colormap, custom_dpi, CorrelationProcess,
                                                            longFileSaveAch, longFileSaveBch,
                                                            long_file_save_im_re, longFileSaveCMP, DynSpecSaveInitial,
                                                            DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned,
                                                            0, 0,
                                                            dat_files_path=path_to_dat_files,
                                                            long_file_save_channels_sum=long_file_sum,
                                                            long_file_save_channels_diff=False, print_or_not=False)

# dat_file_list = ['chA', 'chB', 'A+B']
# dat_file_name = 'E300117_180000.jds'

# Take only channel A, channel B and Cross Spectra amplitude if present
data_types_to_process = []
if 'chA' in dat_file_list and 'chA' in data_types:
    data_types_to_process.append('chA')
if 'chB' in dat_file_list and 'chB' in data_types:
    data_types_to_process.append('chB')
if 'A+B' in dat_file_list and 'A+B' in data_types:
    data_types_to_process.append('A+B')
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

    ok = DAT_file_reader(path_to_dat_files, dat_file_name, data_types_to_process, path_to_dat_files, result_folder_name,
                         0, 0, 0, -120, -10, 0, 6, 6, 300, 'jet', 0, 0, 0, 20 * 10**(-12), 16.5, 33.0, '', '',
                         16.5, 33.0, [], 0)

#
#
#
# dat_file_name = 'P130422_121607.jds'
# data_types_to_process = ['C_m']
#
#

# RFI mask making
print('\n\n * ', str(datetime.datetime.now())[:19], ' * Making mask to clean data \n')

for i in range(len(data_types_to_process)):
    if data_types_to_process[i] == 'chA' or data_types_to_process[i] == 'chB' or data_types_to_process[i] == 'A+B':
        delta_sigma = 0.05
        n_sigma = 2
        min_l = 30
    elif data_types_to_process[i] == 'C_m':
        delta_sigma = 0.1
        n_sigma = 5
        min_l = 30
    else:
        sys.exit('            Type error!')
    file_name = os.path.join(path_to_dat_files, dat_file_name + '_Data_' + data_types_to_process[i] + '.dat')
    dat_rfi_mask_making(file_name, 1024, lin_data=True,
                        delta_sigma=delta_sigma, n_sigma=n_sigma, min_l=min_l)


#
#
# data_types_to_process = ['chA', 'chB']
# path_to_dat_files = '../B1919+21_DSP_spectra_pulsar_UTR2_B1919+21/'
# dat_file_name = 'C250122_070501.jds'
#
#

# Dispersion delay removing
print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Dispersion delay removing... \n\n')

dedispersed_data_file_list = []
for i in range(len(data_types_to_process)):

    amp_min = -0.15
    amp_max = 0.55
    dedispersed_data_file_name = pulsar_incoherent_dedispersion(path_to_dat_files, dat_file_name + '_Data_' +
                                                                data_types_to_process[i] + '.dat', pulsar_name, 512,
                                                                amp_min, amp_max, 0, 0.0, 16.5, 1, 1, 300, 'Greys',
                                                                use_mask_file=True, result_path=path_to_dat_files)

    dedispersed_data_file_list.append(dedispersed_data_file_name)

#
#
#
# dedispersed_data_file_list = ['B0809+74_DM_5.755_E300117_180000.jds_Data_chA.dat']
# data_types_to_process = ['chA']
#
#

# Making N periods pics
if save_n_period_pics:

    print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Making figures of 3 pulsar periods... \n\n')

    for dedispersed_data_file_name in dedispersed_data_file_list:
        # Setting  ranges of integrated signal
        amp_min = -0.15
        amp_max = 0.55
        dyn_sp_min = -0.2
        dyn_sp_max = 3

        pulsar_period_dm_compensated_pics(path_to_dat_files, dedispersed_data_file_name, pulsar_name, 0,
                                          amp_min, amp_max, dyn_sp_min, dyn_sp_max, 3, 500, 'Greys',
                                          True, threshold, use_mask_file=True)

#
#
# dedispersed_data_file_list = ['B0809+74_DM_5.75066_E280120_205409.jds_Data_chA.dat']
#
#

if save_long_dyn_spectra:

    # Making another long dynamic spectra
    result_folder_name = source_directory.split(os.sep)[-1] + '_dedispersed'

    print('\n\n  * ', str(datetime.datetime.now())[:19],
          ' * Making dynamic spectra of the data with compensated dispersion delay... \n\n')

    ok = DAT_file_reader('', dedispersed_data_file_list[0][:-13], data_types_to_process,
                         path_to_dat_files, result_folder_name, 0, 0, 0,
                         -120, -10, 0, 6, 6, 300, 'jet',
                         0, 0, 0, 20 * 10**(-12), 16.5, 33.0,
                         '', '', 16.5, 33.0, [], 0)


#
#
#
# dedispersed_data_file_list = ['B0809+74_DM_5.755_P130422_115005.jds_Data_chA.dat',
#                               'B0809+74_DM_5.755_P130422_115005.jds_Data_chB.dat']
# path_to_dat_files = 'g:/python/B0809+74_2022.04.13_URAN2_B0809+74/'
#
#


# Averaging the pulse
print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Making averaged (folded) pulse profile... \n\n')

smp_file_name_list = []
for dedispersed_data_file_name in dedispersed_data_file_list:
    file_name = dedispersed_data_file_name.split(os.sep)[-1]
    smp_file_name = pulsar_period_folding(path_to_dat_files, file_name,
                                          path_to_dat_files, pulsar_name,
                                          scale_factor, -0.5, 3, periods_per_fig,
                                          custom_dpi, colormap, use_mask_file=True, save_pulse_evolution=True)
    smp_file_name_list.append(smp_file_name)


# SMP files analysis
print('\n\n  * ', str(datetime.datetime.now())[:19], ' * SMP file analysis... \n\n')

for smp_file_name in smp_file_name_list:
    smd_integrated_pulses_analyzer(path_to_dat_files, path_to_dat_files, smp_file_name, pulsar_name, scale_factor,
                                   True, True, no_of_dm_steps, dm_var_step,
                                   1, 1.0, 1, 128,
                                   8, True, 0,
                                   frequency_cuts, colormap, custom_dpi, 16.5, 33.0)


print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Pipeline finished successfully! \n\n')
