# Python3
Software_version = '2020.01.07'
Software_name = 'JDS multifolder data files reader'
# Script intended to read, show and analyze data from ADR, to save
# data to long DAT files for further processing
import os
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Path to directory with files to be analyzed:
# path_to_data = 'DATA/'  # 'h:/To process/'
path_to_data = '/media/gurt/GURT_2021.12/3C461-3C405/'  # 'h:/To process/'

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
longFileSaveAch = 1           # Save data A to long file? (1 = yes, 0 = no)
longFileSaveBch = 1           # Save data B to long file? (1 = yes, 0 = no)
longFileSaveCRI = 1           # Save correlation data (Real and Imaginary) to long file? (1 = yes, 0 = no)
longFileSaveCMP = 1           # Save correlation data (Module and Phase) to long file? (1 = yes, 0 = no)
DynSpecSaveInitial = 0        # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 1        # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 1       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
SpecterFileSaveSwitch = 0     # Save 1 immediate specter to TXT file? (1 = yes, 0 = no)
ImmediateSpNo = 0             # Number of immediate specter to save to TXT file
where_save_pics = 1           # Where to save result pictures? (0 - to script folder, 1 - to data folder)

averOrMin = 0                     # Use average value (0) per data block or minimum value (1)
VminMan = -120                    # Manual lower limit of immediate spectrum figure color range
VmaxMan = -10                     # Manual upper limit of immediate spectrum figure color range
VminNormMan = 0                   # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
VmaxNormMan = 20                  # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
AmplitudeReIm = 20000 * 10**(-12) # Colour range of Re and Im dynamic spectra
                                  # 10 * 10**(-12) is typical value enough for CasA for interferometer of 2 GURT subarrays

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
from package_ra_data_files_formats.check_if_JDS_files_of_equal_parameters import check_if_JDS_files_of_equal_parameters
from package_ra_data_files_formats.JDS_file_reader import JDS_file_reader
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader

# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************

print('\n\n\n\n\n\n   **************************************************************')
print('   *    ', Software_name,'  v.',Software_version,'     *      (c) YeS 2019')
print('   ************************************************************** \n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print('  Today is ', currentDate, ' time is ', currentTime, '\n')

# Path to intermediate data files and results
path_to_DAT_files = os.path.dirname(os.path.realpath(__file__)) + '/'  # 'DATA/'

#      *** Making a list of folders with ADR files ***

# Search needed files in the directory and subdirectories
file_path_list, file_name_list = find_all_files_in_folder_and_subfolders(path_to_data, '.jds', 0)

# Making all slashes in paths of the same type
for i in range (len(file_path_list)):
    file_path_list[i] = file_path_list[i].replace('\\', '/')

# Taking only paths without file names
for i in range (len(file_path_list)):
    file_path_list[i] = file_path_list[i][: -len(file_name_list[i])]

# Take only unique paths
list_of_folder_names = find_unique_strings_in_list(file_path_list)


print('  Total number of JDS files found: ', len(file_name_list))
print('\n  List of folders to be analyzed: \n')
for i in range(len(list_of_folder_names)):
    print('         ',  i+1, ') ', list_of_folder_names[i])


# Take only one folder, find all files
num_of_folders = len(list_of_folder_names)
same_or_not = np.zeros(num_of_folders)
equal_or_not = np.zeros(num_of_folders)
for folder_no in range (num_of_folders):
    file_name_list_current = find_files_only_in_current_folder(list_of_folder_names[folder_no], '.jds', 0)
    print('\n\n\n * Folder ', folder_no+1, ' of ', num_of_folders, ', path: ', list_of_folder_names[folder_no],
          '\n **********************************************************')
    for i in range(len(file_name_list_current)):
        print('         ',  i+1, ') ', file_name_list_current[i])
    print('')

    # Check if all files (except the last) have same size
    same_or_not[folder_no] = check_if_all_files_of_same_size(list_of_folder_names[folder_no], file_name_list_current, 1)

    # Check if all files in this folder have the same parameters in headers
    equal_or_not[folder_no] = check_if_JDS_files_of_equal_parameters(list_of_folder_names[folder_no], file_name_list_current)

if int(np.sum((equal_or_not[:])) == num_of_folders) and (int(np.sum(same_or_not[:])) == num_of_folders):
    print('\n\n\n        :-)  All folders seem to be ready for reading and processing!  :-) \n\n\n')
else:
    print('\n\n\n ************************************************************************************* ',
          '\n *                                                                                   *')
    print(' *   Seems files in folders are different check the errors and restart the script!   *')
    print(' *                                                                                   *  ',
          '\n ************************************************************************************* \n\n\n')


decision = int(input('* Enter "1" to process all folders, or "0" to stop the script:     '))
if decision != 1:
    sys.exit('\n\n\n              ***  Program stopped! *** \n\n\n')


print('\n\n\n   **************************************************************')
print('   *               D A T A   P R O C E S S I N G                *')
print('   **************************************************************')


# In loop take a folder, make a result folder and process the data
for folder_no in range (num_of_folders):

    # Find all files in folder once more:
    file_name_list_current = find_files_only_in_current_folder(list_of_folder_names[folder_no], '.jds', 0)

    print ('\n\n * Folder ', folder_no+1, ' of ', num_of_folders, ', path: ', list_of_folder_names[folder_no])

    # Making a name of folder for storing the result figures and txt files
    # result_path = 'JDS_Results_'+list_of_folder_names[folder_no].split('/')[-2]
    result_folder_name = list_of_folder_names[folder_no].split('/')[-2]
    if where_save_pics == 0:
        result_path = path_to_DAT_files + 'JDS_Results_' + result_folder_name
    else:
        result_path = list_of_folder_names[folder_no] + 'JDS_Results_' + result_folder_name

    for file in range (len(file_name_list_current)):
        file_name_list_current[file] = list_of_folder_names[folder_no] + file_name_list_current[file]

    # Run ADR reader for the current folder
    done_or_not, DAT_file_name, DAT_file_list = JDS_file_reader(file_name_list_current, result_path,
                    MaxNsp, spSkip, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                    VminCorrMag, VmaxCorrMag, colormap, customDPI,
                    CorrelationProcess, longFileSaveAch,
                    longFileSaveBch, longFileSaveCRI, longFileSaveCMP,
                    DynSpecSaveInitial, DynSpecSaveCleaned, CorrSpecSaveInitial,
                    CorrSpecSaveCleaned, SpecterFileSaveSwitch, ImmediateSpNo)

    print('\n * DAT reader analyzes file:', DAT_file_name, ', of types:', DAT_file_list, '\n')

    # DAT_result_path = list_of_folder_names[folder_no].replace('/','_').replace(':','')[:-1]
    # DAT_result_path = list_of_folder_names[folder_no].split('/')[-2]

    # Making path to folder with result pictures
    if where_save_pics == 0:
        DAT_result_path = path_to_DAT_files
    else:
        DAT_result_path = list_of_folder_names[folder_no]

    # Run DAT reader for the resuls of current folder
    done_or_not = DAT_file_reader(path_to_DAT_files, DAT_file_name, DAT_file_list, DAT_result_path, result_folder_name,
                                  averOrMin, 0, 0, VminMan, VmaxMan, VminNormMan, VmaxNormMan,
                                  RFImeanConst, customDPI, colormap, 0, 0, 0, AmplitudeReIm, 0, 0, '', '', 0, 0, [], 0)


endTime = time.time()    # Time of calculations
print('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print('    *** Program ', Software_name, ' has finished! *** \n\n\n')
