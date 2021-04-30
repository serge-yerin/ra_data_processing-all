# Program intended to read and show data from 2DTXT file

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************

filename = 'A200604_105919.adr_12-26-30 - 12-27-10.txt'
colormap = 'jet'                                          # Possible: 'jet', 'Blues', 'Purples', 'Greys'
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
from matplotlib.gridspec import GridSpec
from package_ra_data_processing.filtering import median_filter

from matplotlib.pyplot import plot, draw, show
from matplotlib import rc

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# ************************************************************************************
#                             M A I N   P R O G R A M                                *
# ************************************************************************************
print('\n\n\n\n\n\n\n\n   ****************************************************')
print('   *         2DTXT data files reader  v1.0            *      (c) YeS 2019')
print('   **************************************************** \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print('  Today is ', currentDate, ' time is ', currentTime, ' \n')


# ************************************************************************************
#                             R E A D I N G   D A T A                                *
# ************************************************************************************

file = open(filename, 'r')
param = []
for line in file:
    num = line.rstrip().split()
    floatnum = [float(i) for i in num]
    param.append(floatnum)
file.close()
param = np.array((param))
print ('  Shape of the array: ', param.shape)

data = np.max(param, axis=1)
median_data = median_filter(data, median_filter_window)

fig = plt.figure(figsize=(10.0, 6.0))
ax1 = fig.add_subplot(111)
ax1.plot(data, linewidth='0.80')
ax1.plot(median_data, linewidth='0.80')
pylab.savefig('Result.png', bbox_inches='tight', dpi = customDPI)
plt.close('all')



# v_min = 0
# v_max = 15
#
# # Making result figure
# fig = plt.figure(figsize=(10.0, 6.0))
# # gs = GridSpec(10, 19, figure=fig)
# gs = GridSpec(5, 12, figure=fig)
# rc('font', size=5, weight='bold')
#
# ax1 = fig.add_subplot(gs[0:4, 2:10])
# ax1.set_title('Main data', fontsize=5, fontweight='bold')
# im1 = ax1.imshow(np.flipud(param), aspect='auto', vmin=v_min, vmax=v_max, cmap=colormap,
#                  extent=[0, param.shape[1], 0, param.shape[0]])
# ax1.xaxis.tick_top()
#
# ax2 = fig.add_subplot(gs[0:4, 0])
# ax2.set_title('Colorbar', fontsize=5, fontweight='bold')
# fig.colorbar(im1, cax = ax2, aspect=50)
#
# ax3 = fig.add_subplot(gs[0:4, 1])
# ax3.axis('off')
#
# # ax4 = fig.add_subplot(gs[0:4, 10:13])
# # ax4.plot(np.min(param, axis=1), np.linspace(0, len(param), len(param)), linewidth='0.80')
# # ax4.set_ylim(ymin=0, ymax=param.shape[0])
# # ax4.yaxis.tick_right()
#
# ax5 = fig.add_subplot(gs[0:4, 10:13])
# ax5.plot(np.mean(param, axis=1), np.linspace(0, len(param), len(param)), linewidth='0.80')
# ax5.set_ylim(ymin=0, ymax=param.shape[0])
# ax5.yaxis.tick_right()
#
# # ax6 = fig.add_subplot(gs[0:4, 13:16])
# # ax6.plot(np.max(param, axis=1), np.linspace(0, len(param), len(param)), linewidth='0.80')
# # ax6.set_ylim(ymin=0, ymax=param.shape[0])
# # ax6.yaxis.tick_right()
#
# # ax7 = fig.add_subplot(gs[4:6, 2:10])
# # ax7.plot(np.min(param, axis=0), linewidth='0.80')
# # ax7.set_xlim(xmin=0, xmax=param.shape[1])
#
# ax8 = fig.add_subplot(gs[4:6, 2:10])
# ax8.plot(np.mean(param, axis=0), linewidth='0.80')
# ax8.set_xlim(xmin=0, xmax=param.shape[1])
#
# # ax9 = fig.add_subplot(gs[6:8, 2:10])
# # ax9.plot(np.max(param, axis=0), linewidth='0.80')
# # ax9.set_xlim(xmin=0, xmax=param.shape[1])
#
# fig.subplots_adjust(hspace=0.00, wspace=0.00, top=0.9)
# fig.suptitle('Data from file: ' + filename, fontsize=7, fontweight='bold')
#
# pylab.savefig(filename + '.png', bbox_inches='tight', dpi = customDPI)
# plt.close('all')
