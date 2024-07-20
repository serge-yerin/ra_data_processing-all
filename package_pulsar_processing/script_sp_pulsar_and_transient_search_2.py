
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
source_directory = '../RA_DATA_RESULTS/Transient_search_DSP_cross_spectra_B0809+74_URAN2_/'
vardmd_file_name = 'Transient_P130422_121607.jds_Data_chA_var_DM_5.255-6.255.vdm'
timeln_file_name = 'Transient_P130422_121607.jds_Data_chA_var_DM_5.255-6.255_Timeline.txt'
result_directory = '../RA_DATA_RESULTS/Transient_search_DSP_cross_spectra_B0809+74_URAN2_/'

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


frequency_resolution = 1 / (time_res * vdm_data.shape[1]) # frequency resolution, Hz


profile_spectrum = np.power(np.real(np.fft.fft(vdm_data[:])), 2)  # calculation of the spectrum
profile_spectrum = profile_spectrum[:, 0 : int(vdm_data.shape[1]/2)]  # delete second part of the spectrum
profile_spectrum = np.log10(profile_spectrum)

#profile_spectrum[0:100] = 0.0

frequency_axis = [frequency_resolution * i for i in range(len(profile_spectrum))]


import matplotlib.pyplot as plt
from matplotlib import rc

# Making result picture
fig = plt.figure(figsize=(9.2, 4.5))
# rc('font', size=5, weight='bold')
ax1 = fig.add_subplot(111)
# ax1.plot(profile_spectrum[0, :], color=u'#1f77b4', linestyle='-', alpha=1.0, linewidth='0.60', label='Pulses time profile')
# ax1.legend(loc='upper right', fontsize=5)
# ax1.grid(b=True, which='both', color='silver', linewidth='0.50', linestyle='-')
# ax1.axis([0, len(profile_data), profile_pic_min, profile_pic_max])
# ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
# ax1.set_title('File: ' + filename + '  Pulsar period: '+str(np.round(pulsar_period,3))+' s.', fontsize=5, fontweight='bold')
# ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
# ax2 = fig.add_subplot(212)

ax1.imshow(profile_spectrum[0:100, 0:500], aspect='auto')
ax1.set_xticklabels(frequency_axis)
ax1.set_yticklabels(dm_vector)

# ax1.axis([frequency_axis[0], frequency_axis[-1], -10, 10])
# ax2.legend(loc='upper right', fontsize=5)
# ax2.set_xlabel('Frequency, Hz', fontsize=6, fontweight='bold')
# ax2.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
# fig.subplots_adjust(hspace=0.05, top=0.91)
# fig.suptitle('Single pulses of ' + pulsar_name + ' in time and frequency', fontsize=7, fontweight='bold')
# fig.text(0.80, 0.04, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=3, transform=plt.gcf().transFigure)
# fig.text(0.09, 0.04, 'Software version: ' + Software_version + ', yerin.serge@gmail.com, IRA NASU', fontsize=3,
#          transform=plt.gcf().transFigure)
# pylab.savefig(common_path + '/' + filename[0:-4] + ' and its spectrum.png', bbox_inches='tight', dpi=customDPI)
plt.show()
plt.close('all')





print('\n\n  * ', str(datetime.datetime.now())[:19], ' * Pipeline finished successfully! \n\n')