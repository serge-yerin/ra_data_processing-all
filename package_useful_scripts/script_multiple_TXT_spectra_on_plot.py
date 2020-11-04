# Python3
Software_version = '2019.05.06'
# Script intended to read, show and analyze data from

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
common_path =  '' #'DATA/' # 'e:/PYTHON/ra_data_processing-all/DAT_Results/'
file_name_list = []
plot_name_list = []

y_auto = 0
Vmin = -120
Vmax =  -30


# TXT files to be analyzed:
file_name_list.append(common_path + 'Specter_B201102_235517_sky.txt')
file_name_list.append(common_path + 'Specter_B201102_235702_open.txt')
file_name_list.append(common_path + 'Specter_B201102_235829_short.txt')


plot_name_list.append('Noise generator at antenna amplifier input')
plot_name_list.append('Noise generator at antenna amplifier output')
plot_name_list.append('Noise generator at last amplifier with filter input')


customDPI = 400                     # Resolution of images of dynamic spectra

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

from package_common_modules.text_manipulations import read_frequency_and_two_values_txt
from package_common_modules.text_manipulations import read_date_time_and_one_value_txt
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

#*******************************************************************************
#                          R E A D I N G   D A T A                             *
#*******************************************************************************
number_of_files = len(file_name_list)

# *** Reading files ***
for i in range (number_of_files):
    #[x_value, y1_value, y2_value] = read_frequency_and_two_values_txt ([sky_file])
    [x_value, y1_value] = read_date_time_and_one_value_txt ([file_name_list[i]])
    if i == 0:
        freq_num = len(x_value[0])
        frequencies = np.zeros((number_of_files, freq_num))
        responce = np.zeros((number_of_files, freq_num))
    frequencies[i] = x_value[0]
    responce[i] = y1_value[0]



#*******************************************************************************
#                                F I G U R E S                                 *
#*******************************************************************************

print ('\n\n\n  *** Building images *** \n\n')


rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (9, 5))
ax1 = fig.add_subplot(111)
for i in range (number_of_files):
    ax1.plot(frequencies[i], responce[i], label=plot_name_list[i])
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



endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program TXT reader has finished! *** \n\n\n')
