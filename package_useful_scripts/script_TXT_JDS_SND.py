# Python3
Software_version = '2019.05.06'
# Script intended to read, show and analyze data from

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Path to data files
common_path = ''   #'DATA/' # 'e:/PYTHON/ra_data_processing-all/DAT_Results/'
filename = []

y_auto = 0
Vmin = -120
Vmax = -30
median_window = 50

subband_number = 1  # 1 or 2 if the record was obtained in two JDS channels with band splitting
# channel_number = 1 # 0 or 1 relevant if subband number == 1, else == 0

# TXT files to be analyzed:
sky_file = common_path + 'Spectrum_B210215_223216_sky.txt'
# off_file = common_path + 'Specter_C141019_215835.txt'
open_file = common_path + 'Spectrum_B210215_223904_open.txt'
short_file = common_path + 'Spectrum_B210215_224259_short.txt'

customDPI = 400                     # Resolution of images of dynamic spectra

# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import os
import sys
from os import path
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib import rc
import time

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_common_modules.text_manipulations import read_frequency_and_two_values_txt
from package_common_modules.text_manipulations import read_date_time_and_one_value_txt
from package_ra_data_processing.filtering import median_filter

# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************
print('\n\n\n\n\n\n\n\n   ****************************************************')
print('   *          TXT data files reader  v1.0             *      (c) YeS 2019')
print('   ****************************************************      \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, '\n')


# *** Creating a folder where all pictures will be stored (if it doesn't exist) ***
newpath = "TXT_Results"
if not os.path.exists(newpath):
    os.makedirs(newpath)



#*******************************************************************************
#                          R E A D I N G   D A T A                             *
#*******************************************************************************
# SND (in dB) of Moon dipole of plastic for h=183.7
theoretical_f = np.linspace(1, 50, 50)
theoretical_snd =  [-20.83, -16.18, -6.811,  -1.488, 1.941, 4.356, 6.149, 7.526, 8.621, 9.519, 10.28, 10.93, 11.51,
                    12.02, 12.49, 12.92, 13.3, 13.65, 13.95, 14.21, 14.42, 14.56, 14.64, 14.64, 14.56, 14.4, 14.16,
                    13.84, 13.46, 13.03, 12.59, 12.21, 12.01, 12.22, 13.01, 13.83, 13.56, 12.44, 11.21, 10.12, 9.164,
                    8.318, 7.553, 6.85, 6.201, 5.603, 5.055, 4.565, 4.142, 3.799]



# *** Reading files ***
#[x_value, y1_value, y2_value] = read_frequency_and_two_values_txt ([sky_file])
[x_value, y1_value] = read_date_time_and_one_value_txt ([sky_file])

freq_num = len(x_value[0])
frequencies = np.zeros(subband_number * freq_num)
sky_responce = np.zeros(subband_number * freq_num)

for i in range(freq_num):
    frequencies[i] = x_value[0][i]
    # frequencies[i + freq_num] = x_value[0][i] + 33.0

for i in range(freq_num):
    sky_responce[i] = y1_value[0][i]
    # sky_responce[i + freq_num] = y2_value[0][freq_num - i - 1]

    # sky_responce[i] = y2_value[0][i]


# [x_value, y1_value, y2_value] = read_frequency_and_two_values_txt ([off_file])
#
# off_responce = np.zeros(2 * freq_num)
# for i in range(freq_num):
#     off_responce[i] = y1_value[0][i]
#     off_responce[i + freq_num] = y2_value[0][freq_num - i - 1]

# [x_value, y1_value, y2_value] = read_frequency_and_two_values_txt ([open_file])
[x_value, y1_value] = read_date_time_and_one_value_txt ([open_file])

open_responce = np.zeros(subband_number * freq_num)
for i in range(freq_num):
    open_responce[i] = y1_value[0][i]
    # open_responce[i + freq_num] = y2_value[0][freq_num - i - 1]

    # open_responce[i] = y2_value[0][i]

# [x_value, y1_value, y2_value] = read_frequency_and_two_values_txt ([short_file])
[x_value, y1_value] = read_date_time_and_one_value_txt ([short_file])

short_responce = np.zeros(subband_number * freq_num)
for i in range(freq_num):
    short_responce[i] = y1_value[0][i]
    # short_responce[i + freq_num] = y2_value[0][freq_num - i - 1]

    # short_responce[i] = y2_value[0][i]

# *******************************************************************************
#                                 F I G U R E S                                 *
# *******************************************************************************


print('\n\n\n  *** Building images *** \n\n')


rc('font', size=6, weight='bold')
fig = plt.figure(figsize=(9, 5))
ax1 = fig.add_subplot(111)
ax1.plot(frequencies, sky_responce, color = 'C0', label = 'Sky')
# ax1.plot(frequencies, off_responce, color = 'C1', label = 'Power OFF')
ax1.plot(frequencies, open_responce, color = 'C2', label = 'Open circuit (XX)')
ax1.plot(frequencies, short_responce, color = 'C3', label = 'Short circuit (KZ)')
ax1.legend(loc = 'upper right', fontsize = 6)
ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
if y_auto == 0: ax1.set_ylim([Vmin, Vmax])
ax1.set_ylabel('Intensity, dB', fontsize=6, fontweight='bold')
ax1.set_title('   ', fontsize = 6)
ax1.set_xlabel('Frequency, MHz', fontsize=6, fontweight='bold')
fig.subplots_adjust(top=0.92)
fig.suptitle('File: ', fontsize = 8, fontweight='bold')
fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
fig.text(0.11, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
pylab.savefig(newpath + '/' + ' 01 - All txt data used.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')


snd_open = sky_responce - open_responce
snd_short = sky_responce - short_responce

rc('font', size=6, weight='bold')
fig = plt.figure(figsize=(9, 5))
ax1 = fig.add_subplot(111)
#ax1.plot(frequencies, sky_responce - off_responce, color = 'C1', label = 'Sky - Power OFF')
ax1.plot(frequencies, snd_open, color='C0', alpha = 0.8, label='SND for sky - open circuit')
ax1.plot(frequencies, snd_short, color='C1', alpha = 0.8, label='SND for sky - short circuit')
ax1.plot(theoretical_f, theoretical_snd, 'o', markersize = 3.0, color='C3', label='Calculated SND')
ax1.legend(loc='upper right', fontsize=6)
ax1.grid(b=True, which='both', color='silver', linestyle='-')
ax1.set_ylim([-21, 60])
ax1.set_xlim([0, 60])
ax1.set_ylabel('DND, dB', fontsize=6, fontweight='bold')
ax1.set_title('   ', fontsize = 6)
ax1.set_xlabel('Frequency, MHz', fontsize=6, fontweight='bold')
fig.subplots_adjust(top=0.92)
fig.suptitle('File: ', fontsize = 8, fontweight='bold')
fig.text(0.79, 0.03, 'Processed '+currentDate + ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
fig.text(0.11, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4,
         transform=plt.gcf().transFigure)
pylab.savefig(newpath + '/' + ' 02 - Differences.png', bbox_inches='tight', dpi = 160)
plt.close('all')

snd_open = median_filter(snd_open, median_window)
snd_short = median_filter(snd_short, median_window)

rc('font', size=6, weight='bold')
fig = plt.figure(figsize=(9, 5))
ax1 = fig.add_subplot(111)
#ax1.plot(frequencies, sky_responce - off_responce, color = 'C1', label = 'Sky - Power OFF')
ax1.plot(frequencies, snd_open, color='C0', alpha = 0.8, label='SND for sky - open circuit')
ax1.plot(frequencies, snd_short, color='C1', alpha = 0.8, label='SND for sky - short circuit')
ax1.plot(theoretical_f, theoretical_snd, 'o', markersize = 3.0, color='C3', label='Calculated SND')
ax1.legend(loc='upper right', fontsize=6)
ax1.grid(b=True, which='both', color='silver', linestyle='-')
ax1.set_ylim([-21, 50])
ax1.set_xlim([0, 60])
ax1.set_ylabel('SND, dB', fontsize=6, fontweight='bold')
ax1.set_title('   ', fontsize = 6)
ax1.set_xlabel('Frequency, MHz', fontsize=6, fontweight='bold')
fig.subplots_adjust(top=0.92)
fig.suptitle('File: ', fontsize = 8, fontweight='bold')
fig.text(0.79, 0.03, 'Processed '+currentDate + ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
fig.text(0.11, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4,
         transform=plt.gcf().transFigure)
pylab.savefig(newpath + '/' + ' 03 - Differences filtered.png', bbox_inches='tight', dpi = 160)
plt.close('all')














'''

y_value = np.array(y_value)
a, b = y_value.shape
date_time = x_value[0][:]

text_freqs = []
for i in range (len(filename)):
    text_freqs.append(find_between(filename[i], 'at ', '.txt'))

list_text_freqs = ''
for i in range (len(filename)):
    list_text_freqs = list_text_freqs + find_between(filename[i], 'at ', ' MHz')
    if i < len(filename) - 1: list_text_freqs = list_text_freqs + ', '

print (list_text_freqs)

parent_filename = find_between(filename[0], common_path, ' Intensity')



# Averaging the curves
average = np.zeros(b)
for i in range (a):
    average[:] = average[:] + y_value[i, :]
average[:] = average[:] / a



# Figure of averaged data
timeline = []
for i in range(len(date_time)):
    timeline.append(str(date_time[i][0:11] + '\n' + date_time[i][11:23]))

FileName = (newpath + '/' + parent_filename + ' 02 - Averaged data.png')
OneValueWithTimePlot(timeline, average, 'Averaged values', 0, 1, Vmin, Vmax, 1, y_auto,
                        'UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', 'Intensity, dB',
                        'File: '+parent_filename+' at '+ list_text_freqs +' MHz', '  ', FileName,
                        currentDate, currentTime, Software_version)
'''


endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program TXT reader has finished! *** \n\n\n')
