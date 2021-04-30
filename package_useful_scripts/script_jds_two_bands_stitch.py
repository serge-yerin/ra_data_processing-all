# Program intended to read and show data from 2DTXT file attach two channeld from JDS file and attach the time scale

# *************************************************************
#                         PARAMETERS                          *
# *************************************************************

filename_1 = 'DATA/C050620_084900.jds_chA_09-35-30 - 09-38-30.txt'
filename_2 = 'DATA/C050620_084900.jds_chB_09-35-30 - 09-38-30.txt'
time_file_name = 'DATA/C050620_084900.jds_chA_09-35-30 - 09-38-30_timeline.txt'

v_min = 0
v_max = 20

colormap = 'Greys'                                          # Possible: 'jet', 'Blues', 'Purples', 'Greys'
customDPI = 200

median_filter_window = 80  # Window of median filter to smooth the average profile

# *************************************************************
#                    IMPORT LIBRARIES                         *
# *************************************************************
import sys
from os import path
import numpy as np
import pylab
import time
import matplotlib.pyplot as plt


# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_plot_formats.plot_formats import OneDynSpectraPlot, OneDynSpectraPlotPhD

# ************************************************************************************
#                             M A I N   P R O G R A M                                *
# ************************************************************************************
print('\n\n\n\n\n\n\n\n   ****************************************************')
print('   *         2DTXT data files reader  v1.0            *      (c) YeS 2019')
print('   **************************************************** \n\n\n')

startTime = time.time()
current_time = time.strftime("%H:%M:%S")
current_date = time.strftime("%d.%m.%Y")
print('  Today is ', current_date, ' time is ', current_time, ' \n')


# ************************************************************************************
#                             R E A D I N G   D A T A                                *
# ************************************************************************************

# Read data from file 1
file = open(filename_1, 'r')
param = []
for line in file:
    num = line.rstrip().split()
    floatnum = [float(i) for i in num]
    param.append(floatnum)
file.close()
array_1 = np.array((param))

# Read data from file 2
file = open(filename_2, 'r')
param = []
for line in file:
    num = line.rstrip().split()
    floatnum = [float(i) for i in num]
    param.append(floatnum)
file.close()
array_2 = np.array((param))

print('  Shape of the array: ', array_1.shape, array_2.shape)

# Reverting the second channel and attach to the first channel
array_2 = np.flipud(array_2)
array = np.vstack((array_1, array_2))

# Arranging frequencies
freq_line = np.linspace(0, 66, num=16384)

# Reading timeline file
time_file = open(time_file_name, 'r')
time_line = []
for line in time_file:
    time_line.append(str(line))
time_file.close()
print('\nTime interval: \nfrom ', time_line[0], 'to  ', time_line[-1])

# Exact string timescales to show on plots
time_scale_fig = np.empty_like(time_line)
for i in range(len(time_line)):
    # time_scale_fig[i] = str(time_line[i][0:11] + '\n' + time_line[i][11:23])
    # time_scale_fig[i] = str(time_line[i][11:23])
    time_scale_fig[i] = str(time_line[i][11:19])

# Make a figure
fig_file_name = 'DATA/Dynamic spectrum cleanned and normalized (joint).png'
OneDynSpectraPlotPhD(array, v_min, v_max, '',
                     'Інтенсивність, дБ', len(time_scale_fig),
                     time_scale_fig, freq_line,
                     len(freq_line), 'Greys', 'Час UTC', fig_file_name,
                     current_date, current_time, '', customDPI)


# fig = plt.figure(figsize=(10.0, 6.0))
# ax1 = fig.add_subplot(111)
# im1 = ax1.imshow(np.flipud(array), aspect='auto', vmin=v_min, vmax=v_max, cmap=colormap,
#                  extent=[0, array.shape[1], 0, array.shape[0]])
# pylab.savefig('Result.png', bbox_inches='tight', dpi=customDPI)
# plt.close('all')
