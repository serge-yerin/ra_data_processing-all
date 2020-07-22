# Program intended to read and show data from 2DTXT file

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************

filename = 'DATA/Average profile vs DM 2D (initial DM).txt'
filename = 'RESULTS_pulsar_extracted_pulse_Norm_DM_0.972_DM_1.0_DM_1.0_E310120_225419.jds_Data_chA.dat/Norm_DM_0.972_DM_1.0_DM_1.0_E310120_225419.jds_Data_chA.dat - Extracted pulse.txt'
#filename = []

# TXT files to be analyzed:
#filename.append('Average profile vs DM 2D.txt')
#filename.append('e:/Projects/Python/ADRreader/Specter_A160515_161727.txt')
#filename.append('e:/Projects/Python/ADRreader/Specter_A160515_161727.txt')


colormap = 'Greys'               # Possible: 'jet', 'Blues', 'Purples'
customDPI = 200

#Vmin = -110                         # Lower limit of immediate spectrum figure range
#Vmax = -70                          # Upper limit of immediate spectrum figure rnage
#VminNorm = 0                        # Lower limit of normalized dynamic spectrum figure range
#3VmaxNorm = 12                      # Lower Upper of normalized dynamic spectrum figure range (usually = 15)
#customDPI = 300                     # Resolution of images of dynamic spectra

#customFREQ = 0                      # Custom frequency range (1-yes, 0-no)

#*************************************************************


#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************
import os
import struct
import sys
from os import path
import numpy as np
import pylab
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta

from matplotlib.pyplot import plot, draw, show
from matplotlib import rc


# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

#*************************************************************
#                       MAIN PROGRAM                         *
#*************************************************************
print ('\n\n\n\n\n\n\n\n   ****************************************************')
print ('   *         2DTXT data files reader  v1.0            *      (c) YeS 2019')
print ('   **************************************************** \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, ' \n')


#************************************************************************************
#                            R E A D I N G   D A T A                                *
#************************************************************************************



param = np.array((param))

print (param.shape)

#y_value = param[:, 0]
#data2D = param[:, 1:]

#y_central = y_value[int(len(y_value)/2 + 1)]
#print(y_central)

rc('font', size = 8, weight='bold')
fig = plt.figure(1, figsize = (10.0, 6.0))
ax1 = fig.add_subplot(111)
fig.subplots_adjust(left = None, bottom = None, right = None, top = 0.86, wspace = None, hspace = None)
im1 = ax1.imshow(np.flipud(param), aspect = 'auto', vmin = np.min(param), vmax = np.max(param), cmap=colormap) #extent=[0,1,DM_vector[0]-DM,DM_vector[no_of_DM_steps-1]-DM]
ax1.set_title('Pulse profile vs DM in band ' + str(round(30, 3)) + ' - ' + str(round(70,3)) + ' MHz \n File: ' + 'filename', fontweight = 'bold', y=1.025) # , fontsize = 8 , style='italic'
ax2 = ax1.twinx()
ax2.set_ylabel('DM', fontsize = 8, fontweight='bold') #
ax1.set_xlabel('Phase of pulsar period', fontsize = 8, fontweight='bold')
ax1.set_ylabel(r'$\mathrm{\Delta DM}$') # , fontsize=8, fontweight='bold'
ax2.set_ylim(ax1.get_ylim())
fig.colorbar(im1, ax = ax1, pad = 0.08) #
fig.text(0.76, 0.89,'Current SNR \n        '+str(round(20, 3)), fontsize=7, fontweight='bold', transform=plt.gcf().transFigure)
fig.text(0.76, 0.05, ' Current DM  \n'+str(round(15, 4))+r' $\mathrm{pc * cm^{-3}}$', fontsize=7, fontweight='bold', transform=plt.gcf().transFigure)
pylab.savefig('filename' + '_results_08 - SNR vs DM.png', bbox_inches='tight', dpi = customDPI)
plt.close('all')




'''
plt.figure(1, figsize = (10.0, 6.0))
plt.subplots_adjust(left = None, bottom = None, right = None, top = 0.86, wspace = None, hspace = None)
ImA = plt.imshow(data2D, aspect = 'auto', vmin = np.min(param), vmax = 100, extent=[0,1,y_value[0],y_value[len(y_value)-1]], cmap=colormap)
plt.axhline(y = y_central,   color = 'r', linestyle = '-', linewidth = 0.4)
plt.axvline(x = 0.5, color = 'r', linestyle = '-', linewidth = 0.4)
plt.title('Pulse profile vs DM in band', fontsize = 8, fontweight = 'bold', style='italic', y=1.025)
plt.yticks(fontsize=8, fontweight='bold')
plt.xlabel('Phase of pulsar period', fontsize=8, fontweight='bold')
plt.ylabel('deltaDM', fontsize = 8, fontweight='bold')
plt.colorbar()
plt.xticks(fontsize = 8, fontweight = 'bold')
pylab.savefig('SNR vs DM plot.png', bbox_inches='tight', dpi = customDPI)
plt.show()
plt.close('all')
'''
