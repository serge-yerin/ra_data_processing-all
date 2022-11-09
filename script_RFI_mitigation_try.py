# Python3
#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************
import os
import struct
import sys
import math
import numpy as np
import pylab
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta
from matplotlib import rc

from package_ra_data_processing.f_spectra_normalization import normalization_lin
from package_plot_formats.plot_formats import make_1d_plot, plot2Da
from package_cleaning.clean_lines_of_pixels import clean_lines_of_pixels
from package_cleaning.array_clean_by_STD_value import array_clean_by_STD_value
from package_ra_data_processing.average_some_lines_of_array import average_some_lines_of_array
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes



startTime = time.time()
previousTime = startTime
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, ' \n')

# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = 'RFI_mitigation_try'
if not os.path.exists(newpath):
    os.makedirs(newpath)

mean = 0
sigm = 1

no_of_lines = 8192 #128
no_of_columns = 16384 #256

#theshold_sigm = 3
#min_line_length = 4


array = np.random.normal(mean, sigm, (no_of_lines, no_of_columns))

print('Mean = ', np.mean(array))
print('STD = ', np.std(array),'\n')


array[10:25, 10] = 3.5
array[15:124, 56] = 3.5
array[36, 48:96] = 3.5
array[87, 28:56] = 3.5
array[127, 38:96] = 3.5
array[10:90, 250] = 3.5
array[91:126, 33] = -3.5
array[10:90, 240] = -3.5
array[40:44, 120] = 3.5
array[42, 118:124] = 3.5

'''
plt.figure(1, figsize=(10.0, 6.0))
plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
ImA = plt.imshow(array, aspect='auto', vmin=-4, vmax=4, cmap='Greys')
plt.title('Full log initial data', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
plt.ylabel('One dimension', fontsize = 10, fontweight='bold')
plt.xlabel('Second dimensions', fontsize = 10, fontweight='bold')
plt.colorbar()
plt.yticks(fontsize = 8, fontweight = 'bold')
plt.xticks(fontsize = 8, fontweight = 'bold')
pylab.savefig(newpath+'/01 - RFIed array.png', bbox_inches='tight', dpi = 300)
plt.close('all')
'''

# array, cleaned_pixels_num = array_clean_by_lines_and_STD(array, 3, 3, 4)
array, mask, cleaned_pixels_num = clean_lines_of_pixels(array, 3, 3, 4)

nowTime = time.time() #                            '
print ('\n  * Preparation took:                    ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

shift = np.full(no_of_lines, 500)
array = DM_compensation_with_indices_changes(array, shift)

nowTime = time.time() #                            '
print ('\n  * Method with indices changes took:    ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime

array = np.roll(array, 500)

nowTime = time.time() #                            '
print ('\n  * NUMPY roll took:                     ', round((nowTime - previousTime), 2), 'seconds ')
previousTime = nowTime


'''
plt.figure(1, figsize=(10.0, 6.0))
plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
ImA = plt.imshow(mask, aspect='auto', vmin=0, vmax=1, cmap='Greys')
plt.title('Full log initial data', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
plt.ylabel('One dimension', fontsize = 10, fontweight='bold')
plt.xlabel('Second dimensions', fontsize = 10, fontweight='bold')
plt.colorbar()
plt.yticks(fontsize = 8, fontweight = 'bold')
plt.xticks(fontsize = 8, fontweight = 'bold')
pylab.savefig(newpath+'/00_10 - mask after all iterations.png', bbox_inches='tight', dpi = 300)
plt.close('all')


plt.figure(1, figsize=(10.0, 6.0))
plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
ImA = plt.imshow(array, aspect='auto', vmin=-4, vmax=4, cmap='Greys')
plt.title('Full log initial data', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
plt.ylabel('One dimension', fontsize = 10, fontweight='bold')
plt.xlabel('Second dimensions', fontsize = 10, fontweight='bold')
plt.colorbar()
plt.yticks(fontsize = 8, fontweight = 'bold')
plt.xticks(fontsize = 8, fontweight = 'bold')
pylab.savefig(newpath+'/02 - Cleaned array.png', bbox_inches='tight', dpi = 300)
plt.close('all')
'''
