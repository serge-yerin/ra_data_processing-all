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

from f_spectra_normalization import Normalization_lin
from f_plot_formats import plot1D, plot2Da
from f_pulsar_DM_shift_calculation import DM_shift_calc
from f_file_header_JDS import FileHeaderReaderDSP
from f_file_header_ADR import FileHeaderReaderADR
from f_ra_data_clean import array_clean_by_lines_and_STD   # pulsar_data_clean



# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = 'RFI_mitigation_try'
if not os.path.exists(newpath):
    os.makedirs(newpath)

mean = 0
sigm = 1

no_of_lines = 128
no_of_columns = 256

#theshold_sigm = 3
#min_line_length = 4


array = np.random.normal(mean, sigm, (no_of_lines, no_of_columns))

print('Mean = ', np.mean(array))
print('STD = ', np.std(array),'\n')


array[10:25, 10] = 25.0
array[15:45, 56] = 25.0
array[36, 48:96] = 3.5
array[87, 28:56] = 3.5


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



array = array_clean_by_lines_and_STD(array, 3, 4)



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
