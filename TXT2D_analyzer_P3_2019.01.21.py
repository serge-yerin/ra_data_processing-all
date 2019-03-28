# Program intended to read and show data from 2DTXT file

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************

filename = 'Average profile vs DM 2D.txt'
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
import numpy as np
import pylab
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta



#*************************************************************
#                       MAIN PROGRAM                         *
#*************************************************************
for i in range(8): print (' ')
print ('   ****************************************************')
print ('   *         2DTXT data files reader  v1.0            *      (c) YeS 2019')
print ('   ****************************************************')
for i in range(3): print (' ')


startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)
print (' ')


   
    
#************************************************************************************
#                            R E A D I N G   D A T A                                *
#************************************************************************************

file = open(filename, 'r')
param = []
for line in file:
    num = line.rstrip().split()
    floatnum = [float(i) for i in num]
    param.append(floatnum)
file.close()


param = np.array((param))

y_value = param[:, 0]
data2D = param[:, 1:]

y_central = y_value[int(len(y_value)/2 + 1)]
print(y_central)

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











