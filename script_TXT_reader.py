# Python3
Software_version = '2019.05.06'
# Script intended to read, show and analyze data from

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
common_path = 'd:/PYTHON/ra_data_processing-all/'          # 'DATA/'
filename = []

# TXT files to be analyzed:
filename.append(common_path + '-141119_165243_chA Intensity variation at 10.01.txt')
filename.append(common_path + '-141119_165243_chA Intensity variation at 11.006.txt')
filename.append(common_path + '-141119_165243_chA Intensity variation at 12.012.txt')


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
from f_plot_formats import TwoOrOneValuePlot

################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************
for i in range(8): print (' ')
print ('   ****************************************************')
print ('   *          TXT data files reader  v1.0             *      (c) YeS 2016')
print ('   ****************************************************')
for i in range(3): print (' ')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, '\n')

# *** Creating a folder where all pictures will be stored (if it doen't exist) ***
newpath = "TXT_Results"
if not os.path.exists(newpath):
    os.makedirs(newpath)

#*******************************************************************************
#                          R E A D I N G   D A T A                             *
#*******************************************************************************

# *** Reading files ***
x_value = []
y_value = []

for file in range (len(filename)):
    file = open(filename[file], 'r')
    x_val = []
    y_val = []
    for line in file:
        words = line.rstrip().split()
        x_val.append(words[0] + ' ' + words[1])
        y_val.append(float(words[2]))
    file.close()

    x_value.append(x_val)
    y_value.append(y_val)

y_value = np.array(y_value)
a, b = y_value.shape

#*******************************************************************************
#                                F I G U R E S                                 *
#*******************************************************************************

print ('\n\n\n  *** Building images *** \n\n')


rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (9, 5))
ax1 = fig.add_subplot(111)
for i in range (a):
    ax1.plot(y_value[i, :], linestyle = '-', linewidth = '1.00', label = 'Label')
ax1.legend(loc = 'upper right', fontsize = 6)
ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
#ax1.axis([xmin, xmax, ymin_1, ymax_1])
ax1.set_ylabel('Y label', fontsize=6, fontweight='bold')
ax1.set_title('Title', fontsize = 6)
ax1.set_xlabel('X label', fontsize=6, fontweight='bold')
fig.subplots_adjust(top=0.9)
fig.suptitle('Suptitle', fontsize = 8, fontweight='bold')
fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
fig.text(0.11, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
pylab.savefig(newpath + '/Plot 01.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')

# Averaging the curves
average = np.zeros(b)
for i in range (a):
    average[:] = average[:] + y_value[i, :]
average[:] = average[:] / a


rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (9, 5))
ax1 = fig.add_subplot(111)
ax1.plot(average, linestyle = '-', linewidth = '1.00', label = 'Label')
ax1.legend(loc = 'upper right', fontsize = 6)
ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
#ax1.axis([xmin, xmax, ymin_1, ymax_1])
ax1.set_ylabel('Y label', fontsize=6, fontweight='bold')
ax1.set_title('Title', fontsize = 6)
ax1.set_xlabel('X label', fontsize=6, fontweight='bold')
fig.subplots_adjust(top=0.9)
fig.suptitle('Suptitle', fontsize = 8, fontweight='bold')
fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
fig.text(0.11, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
pylab.savefig(newpath + '/Plot 02.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')



endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program TXT reader has finished! *** \n\n\n')
