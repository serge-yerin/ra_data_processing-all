# Python3
Software_version = '2019.07.30'
Software_name = 'ADR multifolder data files reader'
# Script intended to read, show and analyze data from ADR, to save
# data to long DAT files for further processing

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Directory of files to be analyzed:
common_path =  'DATA/'

MaxNim = 8192                 # Number of data chunks for one figure
chunkSkip = 0                 # Number of chunks to skip from data beginning
RFImeanConst = 8              # Constant of RFI mitigation (usually 8)
Vmin = -120                   # Lower limit of figure dynamic range for initial spectra
Vmax = -50                    # Upper limit of figure dynamic range for initial spectra
VminNorm = 0                  # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 10                 # Upper limit of figure dynamic range for normalized spectra
VminCorrMag = -150            # Lower limit of figure dynamic range for correlation magnitude spectra
VmaxCorrMag = -30             # Upper limit of figure dynamic range for correlation magnitude spectra
customDPI = 200               # Resolution of images of dynamic spectra
colormap = 'jet'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
CorrelationProcess = 1        # Process correlation data or save time?  (1 = process, 0 = save)
Sum_Diff_Calculate = 0        # Calculate sum and diff of A & B channels?
longFileSaveAch = 0           # Save data A to long file? (1 = yes, 0 = no)
longFileSaveBch = 0           # Save data B to long file? (1 = yes, 0 = no)
longFileSaveCMP = 0           # Save correlation data (Module and Phase) to long file? (1 = yes, 0 = no)
longFileSaveCRI = 0           # Save correlation data (Real and Imaginary) to long file? (1 = yes, 0 = no)
longFileSaveSSD = 0           # Save sum / diff data to a long file?
DynSpecSaveInitial = 0        # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 1        # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 1       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
SpecterFileSaveSwitch = 0     # Save 1 immediate specter to TXT file? (1 = yes, 0 = no)
ImmediateSpNo = 100           # Number of immediate specter to save to TXT file

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************

import time
from package_common_modules.find_all_files_in_folder_and_subfolders import find_all_files_in_folder_and_subfolders
from package_common_modules.find_unique_strings_in_list import find_unique_strings_in_list
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR, ChunkHeaderReaderADR
from package_ra_data_files_formats.chaeck_if_ADR_files_of_equal_parameters import chaeck_if_ADR_files_of_equal_parameters

################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************

print ('\n\n\n\n\n\n\n\n   **************************************************************')
print ('   *    ', Software_name,'  v.',Software_version,'     *      (c) YeS 2019')
print ('   ************************************************************** \n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, '\n')

#      *** Making a list of folders with ADR files ***

# Search needed files in the directory and subdirectories
file_path_list, file_name_list = find_all_files_in_folder_and_subfolders(common_path, '.adr', 0)

# Making all slashes in paths of the same type
for i in range (len(file_path_list)):
    file_path_list[i] = file_path_list[i].replace('\\','/')

# Taking only paths without
for i in range (len(file_path_list)):
    file_path_list[i] = file_path_list[i][ : -len(file_name_list[i])]

list_of_folder_names = find_unique_strings_in_list(file_path_list)


print('\n  Number of files ADR found: ', len(file_name_list))
print('\n  List of folders to be analyzed: \n')
for i in range (len(list_of_folder_names)):
    print('         ',  i+1 ,') ', list_of_folder_names[i])


# Take only one folder, find all files
num_of_folders = len(list_of_folder_names)
for folder_no in range (num_of_folders):
    file_name_list_current = find_files_only_in_current_folder(list_of_folder_names[folder_no], '.adr', 0)
    print ('\n\n * Folder ', folder_no+1, ' of ', num_of_folders, ', path: ', list_of_folder_names[folder_no])
    for i in range (len(file_name_list_current)):
        print('         ',  i+1 ,') ', file_name_list_current[i])

    # Check if all files in this folder have the same parameters in headers
    equal_or_not = chaeck_if_ADR_files_of_equal_parameters(list_of_folder_names[folder_no], file_name_list_current)







'''
        newpath = "ADR_Results/Service"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        if DynSpecSaveInitial == 1:
            if not os.path.exists('ADR_Results/Initial_spectra'):
                os.makedirs('ADR_Results/Initial_spectra')
        if (DynSpecSaveCleaned == 1 and CorrelationProcess == 1):
            if not os.path.exists('ADR_Results/Correlation_spectra'):
                os.makedirs('ADR_Results/Correlation_spectra')
'''

# In loop take a folder, make a result folder and process the data





'''
# *** Creating a TXT logfile ***
Log_File = open("ADR_Results/Service/Log.txt", "w")

Log_File.write('\n\n    ****************************************************\n' )
Log_File.write('    *     ADR data files reader  v.%s LOG      *      (c) YeS 2018\n' %Software_version )
Log_File.write('    ****************************************************\n\n' )
Log_File.write('  Date of data processing: %s   \n' %currentDate )
Log_File.write('  Time of data processing: %s \n\n' %currentTime )



# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = "ADR_Results/Service"
if not os.path.exists(newpath):
    os.makedirs(newpath)
if DynSpecSaveInitial == 1:
    if not os.path.exists('ADR_Results/Initial_spectra'):
        os.makedirs('ADR_Results/Initial_spectra')
if (DynSpecSaveCleaned == 1 and CorrelationProcess == 1):
    if not os.path.exists('ADR_Results/Correlation_spectra'):
        os.makedirs('ADR_Results/Correlation_spectra')

'''



endTime = time.time()    # Time of calculations
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('    *** Program ', Software_name,' has finished! *** \n\n\n')
