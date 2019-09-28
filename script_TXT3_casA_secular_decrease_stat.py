# Python3
Software_name = 'CasA secular decrease statistics TXT reader'
Software_version = '2019.09.27'
# Script intended to read TXT files with results of Cas A - Syg A fluxes ration and calculate statistics

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
path_to_data =  'CasA secular decrease measurements results_sample test/'
customDPI = 300                     # Resolution of images of dynamic spectra

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
#import os
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib import rc
import time
import matplotlib
matplotlib.rcParams.update({'errorbar.capsize': 3})


#from package_common_modules.text_manipulations import find_between, read_date_time_and_one_value_txt
#from package_plot_formats.plot_formats import OneValueWithTimePlot
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
file_name_list = find_files_only_in_current_folder(path_to_data, 'jds.txt', 1)

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
if int(np.round(np.sum(frequency[:,0]), 1)) != int(np.sum(np.round(np.sum(frequency, axis = 1) / len(file_name_list), 1))):
        print ('   ERROR! Frequencies in files vary a lot!!! \n\n')
        sys.exit('           Program stopped! \n\n')


frequency = np.mean(frequency, axis = 1)
ratio_CRe_mean = np.mean(ratio_CRe, axis = 1)
ratio_CIm_mean = np.mean(ratio_CIm, axis = 1)
ratio_CRe_std = np.std(ratio_CRe, axis = 1)
ratio_CIm_std = np.std(ratio_CIm, axis = 1)


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
#for i in range (len(freq_list_SygA)):
#    ax1.annotate(str(np.round(flux_ratio[i],3)),  xy=(freq_list_SygA[i], flux_ratio[i]+0.1), fontsize = 6, ha='center')
#if file_name_SygA[-3:] == 'jds': ax1.set_xlim([6, 34])
#if file_name_SygA[-3:] == 'adr': ax1.set_xlim([8, 80])
ax1.set_xlim([6, 34])
ax1.set_ylim([0, 2])
ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
ax1.set_xlabel('Frequency, MHz', fontsize=6, fontweight='bold')
ax1.set_ylabel('Flux ratio', fontsize=6, fontweight='bold')
#if file_name_SygA[-3:] == 'jds': plt.xticks([8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32])
#if file_name_SygA[-3:] == 'adr': plt.xticks([10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75])
plt.xticks([8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32])
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
