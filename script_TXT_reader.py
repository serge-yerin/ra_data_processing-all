# Python3
Software_version = '2019.05.06'
# Script intended to read, show and analyze data from

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
common_path = 'd:/PYTHON/ra_data_processing-all/DATA/'          # 'DATA/'
filename = []

# TXT files to be analyzed:
filename.append(common_path + 'A170712_160219_chA Intensity variation at 9.014 MHz.txt')
filename.append(common_path + 'A170712_160219_chA Intensity variation at 10.01 MHz.txt')
filename.append(common_path + 'A170712_160219_chA Intensity variation at 11.006 MHz.txt')
filename.append(common_path + 'A170712_160219_chA Intensity variation at 12.012 MHz.txt')
#filename.append(common_path + 'A170712_160219_chA Intensity variation at 13.008 MHz.txt')
#filename.append(common_path + 'A170712_160219_chA Intensity variation at 14.014 MHz.txt')
#filename.append(common_path + 'A170712_160219_chA Intensity variation at 15.01 MHz.txt')

customDPI = 300                     # Resolution of images of dynamic spectra

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
import os
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib import rc
import time
from f_text_manipulations import find_between, read_date_time_and_one_value_txt
from f_plot_formats import OneValueWithTimePlot
################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************
print ('\n\n\n\n\n\n\n\n   ****************************************************')
print ('   *          TXT data files reader  v1.0             *      (c) YeS 2016')
print ('   ****************************************************      \n\n\n')

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

# *** Reading files ***
[x_value, y_value] = read_date_time_and_one_value_txt (filename)

y_value = np.array(y_value)
a, b = y_value.shape
date_time = x_value[0][:]

text_freqs = []
for i in range (len(filename)):
    text_freqs.append(find_between(filename[i], 'at ', '.txt'))

#*******************************************************************************
#                                F I G U R E S                                 *
#*******************************************************************************

print ('\n\n\n  *** Building images *** \n\n')


rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (9, 5))
ax1 = fig.add_subplot(111)
for i in range (a):
    ax1.plot(y_value[i, :], linestyle = '-', linewidth = '1.00', label = text_freqs[i])
ax1.legend(loc = 'upper right', fontsize = 6)
ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
#ax1.axis([xmin, xmax, ymin_1, ymax_1])
ax1.set_ylabel('Intensity, dB', fontsize=6, fontweight='bold')
ax1.set_title('Title', fontsize = 6)
ax1.set_xlabel('UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', fontsize=6, fontweight='bold')
text = ax1.get_xticks().tolist()
for i in range(len(text)-1):
    k = int(text[i])
    text[i] = str(date_time[i][0:11] + '\n' + date_time[i][11:23])
ax1.set_xticklabels(text, fontsize = 6, fontweight = 'bold')
fig.subplots_adjust(top=0.92)
fig.suptitle('Suptitle', fontsize = 8, fontweight='bold')
fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
fig.text(0.11, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
pylab.savefig(newpath + '/01 - All txt data.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')


# Averaging the curves
average = np.zeros(b)
for i in range (a):
    average[:] = average[:] + y_value[i, :]
average[:] = average[:] / a



# Figure of averaged data
timeline = []
for i in range(len(date_time)):
    timeline.append(str(date_time[i][0:11] + '\n' + date_time[i][11:23]))

FileName = newpath + '/02 - Averaged data.png'
OneValueWithTimePlot(timeline, average, 'Averaged values', 0, 1, 0, 1, 0,
                        'UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', 'Intensity, dB',
                        'Suptitle', 'Title', FileName,
                        currentDate, currentTime, Software_version)



endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program TXT reader has finished! *** \n\n\n')
