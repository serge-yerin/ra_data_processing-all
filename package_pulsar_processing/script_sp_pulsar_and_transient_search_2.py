
# Python3
software_version = '2024.07.20'
software_name = 'Transient Search Script 2'
"""
"""
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Directory of files to be analyzed:
# source_directory = '../../RA_DATA_ARCHIVE/DSP_spectra_pulsar_UTR2_B0950+08/'
source_directory = '../RA_DATA_RESULTS/Transient_search_DSP_cross_spectra_B0809+74_URAN2/'
vardmd_file_name = 'Transient_P130422_121607.jds_Data_chA_var_DM_5.255-6.255.vdm'
timeln_file_name = 'Transient_P130422_121607.jds_Data_chA_var_DM_5.255-6.255_Timeline.txt'
result_directory = '../RA_DATA_RESULTS/Transient_search_DSP_cross_spectra_B0809+74_URAN2/'

# central_dm = 2.972
central_dm = 5.755
# dm_range = 0.2
dm_range = 0.5
# dm_points = 51  # 41
dm_points = 101  # 41

time_res = 0.007944     # Time resolution, s
fig_time = 30           # Time on one figure, s

colormap = 'Greys'            # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
custom_dpi = 300              # Resolution of images of dynamic spectra



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

# from package_pulsar_processing.pulsar_incoherent_dedispersion import pulsar_incoherent_dedispersion
# from package_pulsar_processing.incoherent_dedispersion import incoherent_dedispersion
from package_pulsar_processing.time_profiles_allignment import read_and_plot_var_dm_file
# from package_pulsar_processing.pulsar_periods_from_compensated_DAT_files import pulsar_period_dm_compensated_pics
# from package_pulsar_processing.pulsar_dm_compensated_dynamic_spectra_folding import pulsar_period_folding
# from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
# from package_ra_data_files_formats.f_jds_file_read import jds_file_reader
# from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
# from package_common_modules.text_manipulations import separate_filename_and_path
# from package_cleaning.dat_rfi_mask_making import dat_rfi_mask_making
# from package_ra_data_processing.f_cross_spectra_phase_calibration import cross_spectra_phase_calibration
# ###############################################################################


print('\n\n\n\n   ***************************************************************************')
print('   *               ', software_name, ' v.', software_version, '                  *      (c) YeS 2024')
print('   *************************************************************************** \n')

# Making a DM values vector
dm_vector = np.linspace(central_dm - dm_range, central_dm + dm_range, num=dm_points)

print('  DM varies in range from', dm_vector[0], 'to', dm_vector[-1], ', number of points:', dm_points)
for i in range(int(len(dm_vector)/2)):
    print(i, '   ', np.round(dm_vector[i], 6), '   ', np.round(dm_vector[-(i+1)], 6))

# Central value
k = int(len(dm_vector)/2)
print(k, '        ', dm_vector[k])

print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Making...')

vdm_data, dm_vector = read_and_plot_var_dm_file(source_directory, vardmd_file_name, timeln_file_name, 
                                                result_directory, time_res, fig_time, 
                                                print_or_not=True, plot_or_not=False)


print(vdm_data.shape)

print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Pipeline finished successfully! \n\n')
