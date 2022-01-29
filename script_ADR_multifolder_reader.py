# Python3
software_version = '2020.01.11'
software_name = 'ADR multifolder data files reader'
# Script intended to read, show and analyze data from ADR, to save
# data to long DAT files and analyze them
import os
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Path to directory with files to be analyzed:
path_to_data = '../RA_DATA_ARCHIVE/ADR_GURT_typical_Sun_data_J_burst/'  # 'h:/To_process/'

print_or_not = 0              # Print progress of data processing and figures making (1) or not (0)
MaxNim = 1024                 # Number of data chunks for one figure
RFImeanConst = 8              # Constant of RFI mitigation (usually 8)
Vmin = -120                   # Lower limit of figure dynamic range for initial spectra
Vmax = -50                    # Upper limit of figure dynamic range for initial spectra
VminNorm = 0                  # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 10                 # Upper limit of figure dynamic range for normalized spectra
VminCorrMag = -150            # Lower limit of figure dynamic range for correlation magnitude spectra
VmaxCorrMag = -30             # Upper limit of figure dynamic range for correlation magnitude spectra
custom_dpi = 200               # Resolution of images of dynamic spectra
colormap = 'jet'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
CorrelationProcess = 1        # Process correlation data or save time?  (1 = process, 0 = save)
DynSpecSaveInitial = 0        # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 1        # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 1       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
SpectrumFileSaveSwitch = 0    # Save 1 immediate spectrum to TXT file? (1 = yes, 0 = no)
ImmediateSpNo = 0             # Number of immediate spectrum to save to TXT file
where_save_pics = 1           # Where to save result pictures? (0 - to script folder, 1 - to data folder)

averOrMin = 0                    # Use average value (0) per data block or minimum value (1)
VminMan = -120                   # Manual lower limit of immediate spectrum figure color range
VmaxMan = -10                    # Manual upper limit of immediate spectrum figure color range
VminNormMan = 0                  # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
VmaxNormMan = 12                 # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
AmplitudeReIm = 1 * 10**(-12)    # Color range of Re and Im dynamic spectra
                                 # 10 * 10**(-12) is typical value for CasA for interferometer of 2 GURT subarrays

# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************

import time
import sys
import numpy as np
from package_common_modules.find_all_files_in_folder_and_subfolders import find_all_files_in_folder_and_subfolders
from package_common_modules.find_unique_strings_in_list import find_unique_strings_in_list
from package_common_modules.check_if_all_files_of_same_size import check_if_all_files_of_same_size
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.check_if_ADR_files_of_equal_parameters import check_if_ADR_files_of_equal_parameters
from package_ra_data_files_formats.ADR_file_reader import ADR_file_reader
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader

# ###############################################################################
# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************

print('\n\n\n\n\n   **************************************************************')
print('   *    ', software_name, '  v.', software_version, '     *      (c) YeS 2019')
print('   ************************************************************** \n\n')

start_time = time.time()
current_time = time.strftime("%H:%M:%S")
current_date = time.strftime("%d.%m.%Y")
print('  Today is ', current_date, ' time is ', current_time, '\n')

# Path to intermediate data files (DAT)
path_to_DAT_files = os.path.dirname(os.path.realpath(__file__)) + '/'  # 'd:/PYTHON/ra_data_processing-all/' # 'DATA/'


#      *** Making a list of folders with ADR files ***
# Search needed files in the directory and subdirectories
file_path_list, file_name_list = find_all_files_in_folder_and_subfolders(path_to_data, '.adr', 0)

# Making all slashes in paths of the same type
for i in range(len(file_path_list)):
    file_path_list[i] = file_path_list[i].replace('\\', '/')

# Taking only paths without
for i in range(len(file_path_list)):
    file_path_list[i] = file_path_list[i][: -len(file_name_list[i])]

list_of_folder_names = find_unique_strings_in_list(file_path_list)


print('\n  Number of ADR files found: ', len(file_name_list))
print('\n  List of folders to be analyzed: \n')
for i in range(len(list_of_folder_names)):
    print('         ',  i+1, ') ', list_of_folder_names[i])


# Take only one folder, find all files
num_of_folders = len(list_of_folder_names)
same_or_not = np.zeros(num_of_folders)
equal_or_not = np.zeros(num_of_folders)
for folder_no in range(num_of_folders):
    file_name_list_current = find_files_only_in_current_folder(list_of_folder_names[folder_no], '.adr', 0)
    print('\n\n\n * Folder ', folder_no+1, ' of ', num_of_folders, ', path: ', list_of_folder_names[folder_no],
          '\n **********************************************************')
    for i in range(len(file_name_list_current)):
        print('         ',  i+1, ') ', file_name_list_current[i])
    print(' ')

    # Check if all files (except the last) have same size
    same_or_not[folder_no] = check_if_all_files_of_same_size(list_of_folder_names[folder_no], file_name_list_current, 1)

    # Check if all files in this folder have the same parameters in headers
    equal_or_not[folder_no] = check_if_ADR_files_of_equal_parameters(list_of_folder_names[folder_no],
                                                                     file_name_list_current)

if int(np.sum((equal_or_not[:])) == num_of_folders) and (int(np.sum(same_or_not[:])) == num_of_folders):
    print('\n\n   :-) All folder seem to be ready for reading! :-) \n')
else:
    print('\n\n\n ************************************************************************************* \n ',
          '*                                                                                   *')
    print(' *   Seems files in folders are different check the errors and restart the script!   *')
    print(' *                                                                                   *  \n ',
          '************************************************************************************* \n\n\n')

    decision = int(input('* Enter "1" to process all folders, or "0" to stop the script:     '))
    if decision != 1:
        sys.exit('\n\n\n              ***  Program stopped! *** \n\n\n')


print('\n\n\n   **************************************************************')
print('   *               D A T A   P R O C E S S I N G                *')
print('   **************************************************************')


# In a loop take a folder, make a result folder and process the data
for folder_no in range(num_of_folders):

    # Find all files in folder once more:
    file_name_list_current = find_files_only_in_current_folder(list_of_folder_names[folder_no], '.adr', 0)
    file_name_list_current.sort()

    print('\n\n * Folder ', folder_no+1, ' of ', num_of_folders, ', path: ', list_of_folder_names[folder_no], '\n')

    # Making a name of folder for storing the result figures and txt files
    result_folder_name = list_of_folder_names[folder_no].split('/')[-2]
    if where_save_pics == 0:
        result_path = path_to_DAT_files + 'ADR_Results_' + result_folder_name
    else:
        result_path = list_of_folder_names[folder_no] + 'ADR_Results_' + result_folder_name

    for file in range(len(file_name_list_current)):
        file_name_list_current[file] = list_of_folder_names[folder_no] + file_name_list_current[file]

    # Run ADR reader for the current folder
    done_or_not, DAT_file_name, DAT_file_list = ADR_file_reader(file_name_list_current, result_path, MaxNim,
                                                                RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                                                                VminCorrMag, VmaxCorrMag, custom_dpi, colormap,
                                                                CorrelationProcess, 0, 1, 1, 1, 1, 0,
                                                                DynSpecSaveInitial, DynSpecSaveCleaned,
                                                                CorrSpecSaveInitial, CorrSpecSaveCleaned,
                                                                SpectrumFileSaveSwitch, ImmediateSpNo, print_or_not)

    print('\n * DAT reader analyzes file:', DAT_file_name, ', of types:', DAT_file_list, '\n')

    # Making path to folder with result pictures
    if where_save_pics == 0:
        DAT_result_path = path_to_DAT_files
    else:
        DAT_result_path = list_of_folder_names[folder_no]

    # Run DAT reader for the results of current folder
    done_or_not = DAT_file_reader(path_to_DAT_files, DAT_file_name, DAT_file_list, DAT_result_path, result_folder_name,
                                  averOrMin, 0, 0, VminMan, VmaxMan, VminNormMan, VmaxNormMan,
                                  RFImeanConst, custom_dpi, colormap, 0, 0, 0, AmplitudeReIm, 0, 0, '', '', 0, 0, [], 0)


endTime = time.time()    # Time of calculations
print('\n\n\n  The program execution lasted for ',
      round((endTime - start_time), 2), 'seconds (', round((endTime - start_time)/60, 2), 'min. ) \n')
print('    *** Program ', software_name, ' has finished! *** \n\n\n')
