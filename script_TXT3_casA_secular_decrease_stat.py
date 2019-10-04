# Python3
Software_name = 'CasA secular decrease statistics TXT reader'
Software_version = '2019.09.27'
# Script intended to read TXT files with results of Cas A - Syg A fluxes ration and calculate statistics

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
path_to_data =  'CasA secular decrease measurements results GURT/'
customDPI = 300                     # Resolution of images of dynamic spectra

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
import sys
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib import rc
import time
import matplotlib
matplotlib.rcParams.update({'errorbar.capsize': 3})

from package_common_modules.math_linear_regression_least_squares import math_linear_regression_least_squares
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************
print ('\n\n\n\n\n\n\n\n   *********************************************************************')
print ('   *        ', Software_name, '  v.', Software_version,'         *      (c) YeS 2019')
print ('   ********************************************************************* \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)



#*******************************************************************************
#                          R E A D I N G   D A T A                             *
#*******************************************************************************

# Search needed files in the directory and subdirectories

if  path_to_data[-5:-1].upper() == 'UTR2':
    file_name_list = find_files_only_in_current_folder(path_to_data, 'jds.txt', 1)
elif path_to_data[-5:-1].upper() == 'GURT':
    file_name_list = find_files_only_in_current_folder(path_to_data, 'adr.txt', 1)
else:
    print ('   ERROR! The data folder name has no name of the telescope in the end!!! \n\n')
    sys.exit('           Program stopped! \n\n')

frequency = []
ratio_CRe = []
ratio_CIm = []

for file_no in range (len(file_name_list)):

    freq = []
    val_01 = []
    val_02 = []

    TXT_file = open(path_to_data + file_name_list[file_no], "r")
    num_of_steps = 0
    for line in TXT_file:                                   # Loop by all lines in file
        if line.startswith("#"):  # Searching comments
            pass
        else:
            num_of_steps += 1
            words_in_line = line.split()
            freq.append(np.float(words_in_line[0]))
            val_01.append(np.float(words_in_line[1]))
            val_02.append(np.float(words_in_line[2]))
    TXT_file.close()

    frequency = np.append(frequency, freq, axis=0)
    ratio_CRe = np.append(ratio_CRe, val_01, axis=0)
    ratio_CIm = np.append(ratio_CIm, val_02, axis=0)

frequency = np.reshape(frequency, [num_of_steps, len(file_name_list)], order='F')
ratio_CRe = np.reshape(ratio_CRe, [num_of_steps, len(file_name_list)], order='F')
ratio_CIm = np.reshape(ratio_CIm, [num_of_steps, len(file_name_list)], order='F')

# A very complicated way to check if all the colums are the same with certain precision :-)
# We round up the values to 0.1 and check if the average sum of all colums is equal to the sum of first colum elements. Do not repeat that in real life!
#if int(np.round(np.sum(frequency[:,0]), 0)) != int(np.sum(np.round(np.sum(frequency, axis = 1) / len(file_name_list), 1))):
#        print ('   ERROR! Frequencies in files vary a lot!!! \n\n')
#        sys.exit('           Program stopped! \n\n')


frequency = np.mean(frequency, axis = 1)
ratio_CRe_mean = np.mean(ratio_CRe, axis = 1)
ratio_CIm_mean = np.mean(ratio_CIm, axis = 1)
ratio_CRe_std = np.std(ratio_CRe, axis = 1)
ratio_CIm_std = np.std(ratio_CIm, axis = 1)


# Trying to calculate the linear regression for the data in normal values ranges:
if path_to_data[-5:-1].upper() == 'UTR2':
    frequency_regression = [16.0,17.0,18.0,19.0,20.0,21.0,22.0,23.0,24.0,25.0,26.0,27.0,28.0,29.0,30.0,31.0]
    values_regression_CRe = ratio_CRe_mean[4 : -1]
    values_regression_CIm = ratio_CIm_mean[4 : -1]
if path_to_data[-5:-1].upper() == 'GURT':
    frequency_regression = [30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65]
    values_regression_CRe = ratio_CRe_mean[18 : -10]
    values_regression_CIm = ratio_CIm_mean[18 : -10]

predict_CRe, weight_CRe, bias_CRe = math_linear_regression_least_squares(frequency_regression, values_regression_CRe)
predict_CIm, weight_CIm, bias_CIm = math_linear_regression_least_squares(frequency_regression, values_regression_CIm)


#*******************************************************************************
#                                F I G U R E S                                 *
#*******************************************************************************

print ('\n\n\n  *** Building images *** \n\n')


# Making a figure of flux ratio with frequency
#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (10, 5))
fig.suptitle('Flux ratio of Cas A and Syg A with frequency', fontsize = 8, fontweight='bold')
ax1 = fig.add_subplot(111)
ax1.set_title('Statistics calculated from ' + str(len(file_name_list)) + ' files', fontsize = 7)
ax1.errorbar(frequency, ratio_CRe_mean, yerr = ratio_CRe_std, ls='none', color = 'r', fmt='-o', label = 'Real part of correlation')
ax1.errorbar(frequency, ratio_CIm_mean, yerr = ratio_CIm_std, ls='none', color = 'b', fmt='-o', alpha = 0.6, label = 'Imag part of correlation')
ax1.plot(frequency_regression, predict_CRe, color = 'r', linestyle = '--', label = 'Linear regression for real part')
ax1.plot(frequency_regression, predict_CIm, color = 'b', linestyle = '--', label = 'Linear regression for imag part')
if path_to_data[-5:-1].upper() == 'UTR2': x_ann = 7; y_ann = 0.6
if path_to_data[-5:-1].upper() == 'GURT': x_ann = 32; y_ann = 0.3
ax1.annotate('Coefficients of linear regression (f in MHZ):',  xy=(x_ann, y_ann+0.2), fontsize = 8, ha='left')
ax1.annotate('Real : '+str(np.round(weight_CRe,6))+' * f + '+str(np.round(bias_CRe, 6)),  xy=(x_ann, y_ann+0.1), fontsize = 8, ha='left')
ax1.annotate('Imag: '+str(np.round(weight_CIm,6))+' * f + '+str(np.round(bias_CIm, 6)),  xy=(x_ann, y_ann), fontsize = 8, ha='left')
if path_to_data[-5:-1].upper() == 'UTR2': ax1.set_xlim([6, 34])
if path_to_data[-5:-1].upper() == 'GURT': ax1.set_xlim([8, 80])
if path_to_data[-5:-1].upper() == 'UTR2': ax1.set_ylim([0, 2.5])
if path_to_data[-5:-1].upper() == 'GURT': ax1.set_ylim([0, 2.0])
ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
ax1.set_xlabel('Frequency, MHz', fontsize=6, fontweight='bold')
ax1.set_ylabel('Flux ratio', fontsize=6, fontweight='bold')
if path_to_data[-5:-1].upper() == 'UTR2': plt.xticks([8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32])
if path_to_data[-5:-1].upper() == 'GURT': plt.xticks([10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75])
ax1.legend(loc = 'upper left')
fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
fig.text(0.09, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
pylab.savefig(path_to_data + '/Overall statistics.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''



endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program ' + Software_name + ' has finished! *** \n\n\n')
