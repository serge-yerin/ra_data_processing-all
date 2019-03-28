# Program intended to read and show data from DAT (ADR) file

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************

filename = []

# TXT files to be analyzed:
filename.append('d:/__Temp/Specter_B181114_200104.txt')
#filename.append('e:/Projects/Python/ADRreader/Specter_A160515_161727.txt')
#filename.append('e:/Projects/Python/ADRreader/Specter_A160515_161727.txt')

Vmin = -110                         # Lower limit of immediate spectrum figure range
Vmax = -70                          # Upper limit of immediate spectrum figure rnage
VminNorm = 0                        # Lower limit of normalized dynamic spectrum figure range
VmaxNorm = 12                       # Lower Upper of normalized dynamic spectrum figure range (usually = 15)
customDPI = 300                     # Resolution of images of dynamic spectra

customFREQ = 0                      # Custom frequency range (1-yes, 0-no)
# Begin and end frequency of dynamic spectrum (MHz)
freqStart = 0
freqStop =  80
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
print ('   *          TXT data files reader  v1.0             *      (c) YeS 2016')
print ('   ****************************************************')
for i in range(3): print (' ')


startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)
print (' ')


# *** Creating a folder where all pictures will be stored (if it doen't exist) ***
newpath = "TXT_Results" 
if not os.path.exists(newpath):
    os.makedirs(newpath)

   
    
#************************************************************************************
#                            R E A D I N G   D A T A                                *
#************************************************************************************

# *** Reading specter file ***
par1 = []
par2 = []
freq = []

for file in range (len(filename)):
    file = open(filename[file], 'r')
    param1 = []
    param2 = []
    frequency = []
    for line in file:
        num = line.rstrip().split()
        floatnum = [float(i) for i in num]
        frequency.append(floatnum[0])
        param1.append(floatnum[1])
        param2.append(floatnum[2])
    file.close()

    freq.append(frequency)
    par1.append(param1)
    par2.append(param2)

    

#************************************************************************************
#                                  F I G U R E S
#************************************************************************************
for i in range (3) : print (' ')
print ('  *** Building images ***')
for i in range (2) : print (' ')
            
#            0       1         2          3           4         5       6         7        8          9          10          11
#           Red     Blue    orange     violet     Dark Blue LightBlue Yellow  DarkGreen  Green   YellowGreen    Wine        Pink
Colors = [[1,0,0],[0,0,1],[1,0.3,0],[0.35,0,0.5],[0,0,0.45], [0,1,1], [1,1,0],[0,0.5,0],[0,1,0], [0.6,0.8,0], [0.2,0,0], [0.8,0,0.4]]


# Plot ranges
if customFREQ == 1:
    frMAX = freqStop
    frMIN = freqStart 
else:
    frMAX = max(max(freq))
    frMIN = min(min(freq))                    

# Start main plot
plt.figure()

# Add curve
plt.plot(freq[0][:], par1[0][:], color = Colors[0], linestyle = '-', linewidth = '1.00', label = 'Channel A')
plt.plot(freq[0][:], par2[0][:], color = Colors[1], linestyle = '-', linewidth = '1.00', label = 'Channel B')
#plt.plot(freq[0][:], par2[0][:], color = Colors[2], linestyle = '-', linewidth = '1.00', label = 'Channel A')

# Other parameters of plot
plt.axis([frMIN,  frMAX, Vmin, Vmax])
plt.xlabel('Frequency, MHz')
plt.ylabel('Amplitude, dB')
plt.suptitle('Immediate spectrum', fontsize=12, fontweight='bold')
plt.title(' ', fontsize=8)
plt.grid(b = True, which = 'both', color = '0.00',linestyle = '--')
plt.legend(loc = 'upper right', fontsize = 10)
pylab.savefig('TXT_Results/Spectrum.png', bbox_inches='tight', dpi = 160)
plt.show()
plt.close()                    
                    



# Data processing for additional plot
array = np.zeros(len(par1[0][:]))
print (' l = ', len(array))
a = par1[0][:]
b = par2[0][:]
for i in range(len(a)):
    array[i] =  b[i] - a[i]




# Start additional plot
plt.figure()

# Add curve
plt.plot(freq[0][:], array[:], color = Colors[1], linestyle = '-', linewidth = '1.00', label = 'Channel A')

# Other parameters of plot
plt.axis([frMIN,  frMAX, -8, 8])
plt.xlabel('Frequency, MHz')
plt.ylabel('Amplitude, dB')
plt.suptitle('Immediate spectrum', fontsize=12, fontweight='bold')
plt.title(' ', fontsize=8)
plt.grid(b = True, which = 'both', color = '0.00',linestyle = '--')
plt.legend(loc = 'upper right', fontsize = 10)
pylab.savefig('TXT_Results/Spectrum difference.png', bbox_inches='tight', dpi = 160)
plt.show()
plt.close()       








                    
               
               
endTime = time.time()    # Time of calculations      
      
        
for i in range (0,2) : print (' ')
print ('   The program execution lasted for ', (endTime - startTime), 'seconds')
for i in range (0,2) : print (' ')
print ('                 *** Program has finished! ***')
for i in range (0,3) : print (' ')
