# Python3
Software_version = '2022.04.05'
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
directory = 'DATA/'

pulsar_name = 'J2325-0530'  # 'B0809+74' # 'B0950+08' # 'B1133+16' # 'B1604-00' # 'B1919+21' # 'J0242+6256' #

process_channel_b = False       # Process channel B or save time
save_strongest = True           # Save strongest images to additional separate folder?
threshold = 0.25                # Threshold of the strongest pulses (or RFIs)

MaxNsp = 2048                 # Number of spectra to read for one figure
Vmin = -100                   # Lower limit of figure dynamic range
Vmax = -40                    # Upper limit of figure dynamic range
VminNorm = 0                  # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 10                 # Upper limit of figure dynamic range for normalized spectra
VminCorrMag = -150            # Lower limit of figure dynamic range for correlation magnitude spectra
VmaxCorrMag = -30             # Upper limit of figure dynamic range for correlation magnitude spectra
colormap = 'jet'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
customDPI = 300               # Resolution of images of dynamic spectra
CorrelationProcess = 1        # Process correlation data or save time?  (1 = process, 0 = save)
longFileSaveAch = 1           # Save data A to long file? (1 = yes, 0 = no)
longFileSaveBch = 1           # Save data B to long file? (1 = yes, 0 = no)
longFileSaveCRI = 0           # Save correlation data (Real and Imaginary) to long file? (1 = yes, 0 = no)
longFileSaveCMP = 1           # Save correlation data (Module and Phase) to long file? (1 = yes, 0 = no)
DynSpecSaveInitial = 0        # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 0        # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 0       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
where_save_pics = 0           # Where to save result pictures? (0 - to script folder, 1 - to data folder)


# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import os
import sys
from os import path

# To change system path to main source_directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_pulsar_processing.script_pulsar_single_pulses import pulsar_incoherent_dedispersion
from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import pulsar_period_DM_compensated_pics
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_ra_data_files_formats.JDS_file_reader import JDS_file_reader
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
# ###############################################################################


print('\n\n  * Making dynamic spectra of the initial data... ')

# Find all files in folder once more:
file_name_list_current = find_files_only_in_current_folder(directory, '.jds', 0)

# Path to intermediate data files and results
path_to_DAT_files = os.path.dirname(os.path.realpath(__file__)) + '/'

result_folder_name = directory.split('/')[-2]
if where_save_pics == 0:
    result_path = path_to_DAT_files + 'JDS_Results_' + result_folder_name
else:
    result_path = directory + 'JDS_Results_' + result_folder_name

for file in range(len(file_name_list_current)):
    file_name_list_current[file] = directory + file_name_list_current[file]

# Run ADR reader for the current folder
done_or_not, DAT_file_name, DAT_file_list = JDS_file_reader(file_name_list_current, result_path, MaxNsp, 0,
                                                            8, Vmin, Vmax, VminNorm, VmaxNorm,
                                                            VminCorrMag, VmaxCorrMag, colormap, customDPI,
                                                            CorrelationProcess, longFileSaveAch, longFileSaveBch,
                                                            longFileSaveCRI, longFileSaveCMP, DynSpecSaveInitial,
                                                            DynSpecSaveCleaned, CorrSpecSaveInitial,
                                                            CorrSpecSaveCleaned, 0, 0)

# Take only channel A, channel B and Cross Spectra amplitude if present
typesOfData = []
if 'chA' in DAT_file_list:
    typesOfData.append('chA')
if 'chB' in DAT_file_list:
    typesOfData.append('chB')
if 'C_m' in DAT_file_list:
    typesOfData.append('C_m')

print('\n * DAT reader analyzes file:', DAT_file_name, ', of types:', typesOfData, '\n')

result_folder_name = directory.split('/')[-2] + '_initial'

ok = DAT_file_reader('', DAT_file_name, typesOfData, '', result_folder_name, 0, 0, 0, -120, -10, 0, 6, 6,
                     300, 'jet', 0, 0, 0, 20 * 10**(-12), 16.5, 33.0, '', '', 16.5, 33.0, [], 0)

#
#
# results_files_list = ['E080219_200543.jds_Data_chA.dat']
#
#

print('\n\n  *  Dispersion delay removing... \n\n')
dedispersed_data_file_list = []
for i in range(len(typesOfData)):
    dedispersed_data_file_name = pulsar_incoherent_dedispersion('', DAT_file_name + '_Data_' + typesOfData[i] + '.dat',
                                                                pulsar_name, 512, -0.15, 0.55, 0, 0, 0, 1, 10, 2.8, 0,
                                                                0.0, 16.5, 1, 1, 300, 'Greys')
    dedispersed_data_file_list.append(dedispersed_data_file_name)

print('\n\n  *  Making figures of 3 pulsar periods... \n\n')
for dedispersed_data_file_name in dedispersed_data_file_list:
    pulsar_period_DM_compensated_pics('', dedispersed_data_file_name, pulsar_name,
                                      0, -0.15, 0.55, -0.2, 3, 3, 500, 'Greys', save_strongest, threshold)

#
#
# dedispersed_data_file_list = ['B0809+74_DM_5.75066_E280120_205409.jds_Data_chA.dat']
#
#

result_folder_name = directory.split('/')[-2] + '_dedispersed'

print('\n\n  * Making dynamic spectra of the dedispersed data... \n\n')

ok = DAT_file_reader('', dedispersed_data_file_list[0][:-13], typesOfData, '', result_folder_name, 0, 0, 0, -120, -10,
                     0, 6, 6, 300, 'jet', 0, 0, 0, 20 * 10**(-12), 16.5, 33.0, '', '', 16.5, 33.0, [], 0)

print('\n\n  *  Pipeline finished successfully! \n\n')
