# Python3
Software_version = '2020.06.24'
"""
The main goal to the script is to analyze of waveform pulsar data to find anomalously intense pulses during observation
session. It reads the waveform files, converts data into spectra (making zero points used for time stamps),
saves dynamic spectra pics of each wf file and the whole observation, than runs the incoherent dispersion delay 
removing, saves dynamic spectra pics for each max DM delay time, and then makes pics of each 3 pulsar periods. 
User can analyze the pics and decide if there are pulses worth processing and the time of the pulse receiving to
run the "script_wf_pulsar_coherent_dispersion_delay_removing.py" for selected files only. 
"""
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Directory of files to be analyzed:
source_directory = '../RA_DATA_ARCHIVE/DSP_waveform_33MHz_B0950p08/'

# Result folder (intermediate data is also stored here, so make sure there is plenty of disk space here)
result_directory = '../RA_DATA_RESULTS/' 

pulsar_name = 'B0950+08'  # 'B0809+74' # 'B1133+16' # 'B1604-00' # 'B1919+21' # 'J0242+6256'

no_of_spectra_to_average = 16   # Number of spectra to average for dynamic spectra (16 - 7.9 ms)
process_channel_b = False       # Process channel B or save time
save_strongest = True           # Save strongest images to additional separate folder?
threshold = 0.25                # Threshold of the strongest pulses (or RFIs)
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import os
import sys
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from script_JDS_WF_reader import jds_wf_simple_reader
from package_pulsar_processing.pulsar_incoherent_dedispersion import pulsar_incoherent_dedispersion
from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import pulsar_period_dm_compensated_pics
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
# ###############################################################################

# Prepare all folder paths to read data, to store intermediate data and results
source_directory = os.path.normpath(source_directory)
result_directory = os.path.normpath(result_directory)

result_folder_name = source_directory.split(os.sep)[-1]
path_to_dat_files = os.path.join(result_directory, pulsar_name + '_' + result_folder_name + '_incoherent_search')

# Conversion from data files to spectra data in long '.dat' format
print('\n\n  * Conversion from waveform to spectra... \n\n')
results_files_list = jds_wf_simple_reader(source_directory, no_of_spectra_to_average, 0, 0, 8, 'Greys', 
                                          300, 1, 0, 1, result_path=path_to_dat_files)

# Making a dynamic spectra of the whole data bunch to examine the data quality
print('\n\n  * Making dynamic spectra of the initial data... \n\n')

types_of_data = ['chA']

if len(results_files_list) > 1 and process_channel_b:
    types_of_data.append('chB')
else:
    results_files_list = [results_files_list[0]]

for i in range(len(results_files_list)):
    results_files_list[i] = results_files_list[i].split(os.sep)[-1]

result_folder_name = source_directory.split(os.sep)[-1] + '_initial'

ok = DAT_file_reader(path_to_dat_files, results_files_list[0][:-13], types_of_data, 
                     path_to_dat_files, result_folder_name, 0, 0, 0, -120, -10, 0, 6, 6,
                     300, 'jet', 0, 0, 0, 20 * 10**(-12), 16.5, 33.0, '', '', 16.5, 33.0, [], 0)

#
#
# results_files_list = ['E080219_200543.jds_Data_chA.dat']
#
#

# Incoherent dispersion delay removal in the whole data
print('\n\n  *  Dispersion delay removing... \n\n')
dedispersed_data_file_list = []
for i in range(len(results_files_list)):
    
    # # Old function call left just in case
    # dedispersed_data_file_name = pulsar_incoherent_dedispersion('', 
    #                                                             results_files_list[i], 
    #                                                             pulsar_name,
    #                                                             512, 
    #                                                             -0.15, 0.55, 
    #                                                             0, 0, 0, 
    #                                                             1, 10, 
    #                                                             2.8, 0, 0.0,
    #                                                             16.5, 1, 1, 300, 'Greys')
    
    dedispersed_data_file_name = pulsar_incoherent_dedispersion(path_to_dat_files,  results_files_list[i],  pulsar_name,
                                                                512,  -0.15, 0.55,  False, 0.0, 0.0, 
                                                                True, True,  300, 'Greys', 
                                                                result_path=path_to_dat_files, save_pics=True, 
                                                                use_mask_file=False, make_fourier=False, 
                                                                print_or_not=True)
    
    dedispersed_data_file_list.append(dedispersed_data_file_name)


# Making figures of dynamic spectra and intergrated profile for each 3 pulsar periods
print('\n\n  *  Making figures of 3 pulsar periods... \n\n')
for dedispersed_data_file_name in dedispersed_data_file_list:
    pulsar_period_dm_compensated_pics(path_to_dat_files, dedispersed_data_file_name, pulsar_name,
                                      0, -0.15, 0.55, -0.2, 3, 3, 500, 'Greys', save_strongest, threshold)

#
#
# dedispersed_data_file_list = ['B0809+74_DM_5.75066_E280120_205409.jds_Data_chA.dat']
#
#

# Making a dynamic spectra of the whole data bunch after dispersioon delay removal to examine the data quality
result_folder_name = source_directory.split(os.sep)[-1] + '_dedispersed'

print('\n\n  * Making dynamic spectra of the dedispersed data... \n\n')

for i in range(len(dedispersed_data_file_list)):
    dedispersed_data_file_list[i] = dedispersed_data_file_list[i].split(os.sep)[-1]

ok = DAT_file_reader(path_to_dat_files, dedispersed_data_file_list[0][:-13], 
                     types_of_data, path_to_dat_files, result_folder_name, 0, 0, 0, -120, -10,
                     0, 6, 6, 300, 'jet', 0, 0, 0, 20 * 10**(-12), 16.5, 33.0, '', '', 16.5, 33.0, [], 0)

print('\n\n  *  Pipeline finished successfully! \n\n')
