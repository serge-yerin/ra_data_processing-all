
# Python3
software_version = '2022.07.05'
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
source_directory = '../RA_DATA_ARCHIVE/DSP_spectra_pulsar_UTR2_B0809+74/'
result_directory = '../'

central_dm = 5.755
dm_range = 0.5
dm_step = 0.1

# Types of data to get (full possible set in the comment below - copy to code necessary)
# data_types = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm', 'A+B', 'A-B', 'chAdt', 'chBdt']
data_types = ['chA']

# periods_per_fig = 1           # Number of periods on averaged (folded) pulse profile
# scale_factor = 10             # Scale factor to interpolate data (depends on RAM, use 1, 10, 30)
#
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
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_pulsar_processing.pulsar_incoherent_dedispersion import pulsar_incoherent_dedispersion
from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import pulsar_period_dm_compensated_pics
from package_pulsar_processing.pulsar_dm_compensated_dynamic_spectra_folding import pulsar_period_folding
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_ra_data_files_formats.JDS_file_reader import JDS_file_reader
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_cleaning.dat_rfi_mask_making import dat_rfi_mask_making
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

if 'C_m' in data_types:
    longFileSaveCMP = 1
    CorrelationProcess = 1
else:
    longFileSaveCMP = 0
    CorrelationProcess = 0


# '''
#
#
#
#

print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Making dynamic spectra of the initial data')

# Find all files in folder once more:
file_name_list_current = find_files_only_in_current_folder(source_directory, '.jds', 0)

result_folder_name = source_directory.split('/')[-2]

# Path to intermediate data files and results
if result_directory == '':
    result_directory = os.path.dirname(os.path.realpath(__file__))  # + '/'

path_to_dat_files = result_directory + '/Transient_search_DM=' + pulsar_name + '_' + result_folder_name + '/'

result_path = path_to_dat_files + 'JDS_Results_' + result_folder_name

for file in range(len(file_name_list_current)):
    file_name_list_current[file] = source_directory + file_name_list_current[file]

# Run JDS/ADR reader for the current folder

done_or_not, DAT_file_name, DAT_file_list = JDS_file_reader(file_name_list_current, result_path, 2048, 0,
                                                            8, -100, -40, 0, 6, -150, -30, colormap, custom_dpi,
                                                            CorrelationProcess, longFileSaveAch, longFileSaveBch,
                                                            longFileSaveCRI, longFileSaveCMP, DynSpecSaveInitial,
                                                            DynSpecSaveCleaned, CorrSpecSaveInitial,
                                                            CorrSpecSaveCleaned, 0, 0, dat_files_path=path_to_dat_files)

# Take only channel A, channel B and Cross Spectra amplitude if present
data_types_to_process = []
if 'chA' in DAT_file_list and 'chA' in data_types:
    data_types_to_process.append('chA')
if 'chB' in DAT_file_list and 'chB' in data_types:
    data_types_to_process.append('chB')
if 'C_m' in DAT_file_list and 'C_m' in data_types:
    data_types_to_process.append('C_m')


print('\n * ', str(datetime.datetime.now())[:19], ' * DAT reader analyzes file: \n',
      DAT_file_name, ', of types:', data_types_to_process, '\n')

result_folder_name = source_directory.split('/')[-2] + '_initial'

ok = DAT_file_reader(path_to_dat_files, DAT_file_name, data_types_to_process, path_to_dat_files, result_folder_name,
                     0, 0, 0, -120, -10, 0, 6, 6, 300, 'jet', 0, 0, 0, 20 * 10**(-12), 16.5, 33.0, '', '',
                     16.5, 33.0, [], 0)
# '''
#
#
# DAT_file_name = 'E300117_180000.jds'
# data_types_to_process = ['chA']
#
#

# RFI mask making
print('\n\n * ', str(datetime.datetime.now())[:19], ' * Making mask to clean data \n')

for i in range(len(data_types_to_process)):
    dat_rfi_mask_making(path_to_dat_files + DAT_file_name + '_Data_' + data_types_to_process[i] + '.dat', 4000)

#
#
#
#
#
#

# Dispersion delay removing
print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Dispersion delay removing... \n\n')



dedispersed_data_file_list = []
for i in range(len(data_types_to_process)):
    # Setting different ranges of integrated signal for cross spectra amplitude and simple spectra
    if data_types_to_process[i] == 'C_m':
        amp_min = -0.05
        amp_max = 0.15
    else:
        amp_min = -0.15
        amp_max = 0.55

    dedispersed_data_file_name = pulsar_incoherent_dedispersion(path_to_dat_files, DAT_file_name + '_Data_' +
                                                                data_types_to_process[i] + '.dat', pulsar_name, 512,
                                                                amp_min, amp_max, 0, 0.0, 16.5, 1, 1, 300, 'Greys',
                                                                use_mask_file=True, result_path=path_to_dat_files)

    dedispersed_data_file_list.append(dedispersed_data_file_name)

# '''
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
        # Setting different ranges of integrated signal for cross spectra amplitude and simple spectra
        if '_Data_C_m' in dedispersed_data_file_name:
            amp_min = -0.01
            amp_max = 0.02
            dyn_sp_min = -0.02
            dyn_sp_max = 0.3

        else:
            amp_min = -0.15
            amp_max = 0.55
            dyn_sp_min = -0.2
            dyn_sp_max = 3

        pulsar_period_dm_compensated_pics(path_to_dat_files, dedispersed_data_file_name, pulsar_name, 0,
                                          amp_min, amp_max, dyn_sp_min, dyn_sp_max, 3, 500, 'Greys',
                                          save_strongest, threshold)

#
#
# dedispersed_data_file_list = ['B0809+74_DM_5.75066_E280120_205409.jds_Data_chA.dat']
#
#

# Making another long dynamic spectra
result_folder_name = source_directory.split('/')[-2] + '_dedispersed'
print('\n\n  * ', str(datetime.datetime.now())[:19],
      ' * Making dynamic spectra of the data with compensated dispersion delay... \n\n')

ok = DAT_file_reader(path_to_dat_files, dedispersed_data_file_list[0][:-13], data_types_to_process, path_to_dat_files,
                     result_folder_name, 0, 0, 0, -120, -10, 0, 6, 6, 300, 'jet', 0, 0, 0, 20 * 10**(-12),
                     16.5, 33.0, '', '', 16.5, 33.0, [], 0)

#
#
#
#
#

# Averaging the pulse
print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Making averaged (folded) pulse profile... \n\n')

for dedispersed_data_file_name in dedispersed_data_file_list:
    pulsar_period_folding(path_to_dat_files, dedispersed_data_file_name, pulsar_name, scale_factor, -0.5, 3,
                          periods_per_fig, custom_dpi, colormap, use_mask_file=True)

print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Pipeline finished successfully! \n\n')