# Python3
Software_version = '2019.10.26'
# Script intended to read, show and average data from TXT files of
# date-time-value format

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
common_path =  'DATA/' # 'e:/PYTHON/ra_data_processing-all/DAT_Results/'
filename = []

y_auto = 1
Vmin = -500 * 10**(-12)
Vmax =  500 * 10**(-12)

# Add files manually here, or use standard module to find all txt files in common_path
#filename.append(common_path + 'C141019_055118_chB Intensity variation at 10.002 MHz.txt')
#filename.append(common_path + 'A170712_160219_chA Intensity variation at 10.01 MHz.txt')

customDPI = 300                     # Resolution of images of dynamic spectra

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
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

from package_plot_formats.plot_formats import OneValueWithTimePlot
from package_common_modules.text_manipulations import find_between, read_date_time_and_one_value_txt
from package_plot_formats.MultipleValueWithTimePlot import MultipleValueWithTimePlot
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder

################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************
print ('\n\n\n\n\n\n\n\n   ****************************************************')
print ('   *          TXT data files reader  v1.0             *      (c) YeS 2019')
print ('   ****************************************************      \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, '\n')

# *** Creating a folder where all pictures will be stored (if it doesn't exist) ***
newpath = "TXT_Results"
if not os.path.exists(newpath):
    os.makedirs(newpath)

# TXT files to be analyzed: to find all files in directory
filename = find_files_only_in_current_folder(common_path, '.txt', 1)
for i in range(len(filename)):  filename[i] = common_path + filename[i]

#*******************************************************************************
#                          R E A D I N G   D A T A                             *
#*******************************************************************************

# *** Reading files ***
[x_value, y_value] = read_date_time_and_one_value_txt (filename)

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


parent_filename = find_between(filename[0], common_path, ' Intensity')

#*******************************************************************************
#                                F I G U R E S                                 *
#*******************************************************************************

print ('\n\n\n  *** Building images *** \n\n')

# Preparing the timeline
timeline = []
for i in range(len(date_time)):
    timeline.append(str(date_time[i][0:11] + '\n' + date_time[i][11:23]))

# Figure of all data files
FileName = (newpath + '/' + parent_filename + ' 01 - All txt data used.png')
MultipleValueWithTimePlot(timeline, y_value, text_freqs, 0, 1, Vmin, Vmax, 1, y_auto,
                        'UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', 'Intensity, dB',
                        'File: '+parent_filename, '  ', FileName,
                        currentDate, currentTime, Software_version)

# Averaging the curves
average = np.zeros(b)
for i in range (a):
    average[:] = average[:] + y_value[i, :]
average[:] = average[:] / a



# Figure of averaged data
FileName = (newpath + '/' + parent_filename + ' 02 - Averaged data.png')
OneValueWithTimePlot(timeline, average, 'Averaged values', 0, 1, Vmin, Vmax, 1, y_auto,
                        'UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', 'Intensity, dB',
                        'File: '+parent_filename+' at '+ list_text_freqs +' MHz', '  ', FileName,
                        currentDate, currentTime, Software_version)



endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program TXT reader has finished! *** \n\n\n')
