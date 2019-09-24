# Python3
Software_name = 'CasA secular decrease TXT reader'
Software_version = '2019.09.24'
# Script intended to read, show and analyze data from

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files

path_to_data_SygA =  'DATA/DAT_Results_D250719_165520.jds_3C405/'
path_to_data_CasA =  'DATA/DAT_Results_D250719_230437.jds_3C461/'

y_auto = 1
Vmin = -500 * 10**(-12)
Vmax =  500 * 10**(-12)
interferometer_base = 400 #900

customDPI = 300                     # Resolution of images of dynamic spectra

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
c = 2.997 * 10**8

import os
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import ticker as mtick
import time

from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_common_modules.text_manipulations import find_between, read_date_time_and_one_value_txt
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

result_path = 'CasA_decular_decrease' + find_between(path_to_data_SygA, 'Results_', '_3C') + '_' + find_between(path_to_data_CasA, 'Results_', '_3C')
if not os.path.exists(result_path):
    os.makedirs(result_path)

freq_list_CasA = []
freq_list_SygA = []
ampl_list_CasA = []
ampl_list_SygA = []

for source in ['SygA', 'CasA']:

    if source == 'SygA': path_to_data = path_to_data_SygA
    if source == 'CasA': path_to_data = path_to_data_CasA

    # Finding TXT files in the folder
    print('')
    file_name_list = find_files_only_in_current_folder(path_to_data, '.txt', 1)
    #file_name_list.sort()

    for file_no in range (len(file_name_list)):

        # *** Reading files ***
        [x_value, y_value] = read_date_time_and_one_value_txt ([path_to_data + file_name_list[file_no]])

        y_value = np.array(y_value)
        a, b = y_value.shape
        date_time = x_value[0][:]

        text_freq = find_between(file_name_list[file_no], 'at ', ' MHz')
        num_freq = np.float(text_freq)
        if source == 'SygA': freq_list_SygA.append(num_freq)
        if source == 'CasA': freq_list_CasA.append(num_freq)

        parent_filename = find_between(path_to_data + file_name_list[0], path_to_data, ' variation')

        x_center = int(b/2) # Central point in time axis (culmination time usually)

        amplitude = (np.max(y_value[0, :]) + np.abs(np.min(y_value[0, :])))/2



        #*******************************************************************************
        #                                F I G U R E S                                 *
        #*******************************************************************************

        rc('font', size = 6, weight='bold')
        fig = plt.figure(figsize = (9, 5))
        ax1 = fig.add_subplot(111)
        plt.axvline(x = x_center, linewidth = '0.5' , color = 'r') #, alpha=0.5
        for i in range (a):
            #ax1.plot(theory[:], linestyle = '--', linewidth = '1.50', alpha = 0.5, label = 'Theory')
            vertical_offset = - np.mean(y_value[i, :])
            ax1.plot(y_value[i, :] + vertical_offset, linestyle = '-', linewidth = '1.00', label = 'Measured')
        ax1.legend(loc = 'upper right', fontsize = 6)
        ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
        if y_auto == 0: ax1.set_ylim([Vmin, Vmax])
        ax1.set_xlim([0, b-1])
        ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
        ax1.set_title('Base: '+str(interferometer_base) + ' m., amplitude: ' + ('%.4e' % amplitude) + ', vertical offset: ' + ('%.4e' % vertical_offset), fontsize = 6)
        ax1.set_xlabel('UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', fontsize=6, fontweight='bold')
        ax1.xaxis.set_major_locator(mtick.LinearLocator(7))
        #ax1.xaxis.set_minor_locator(mtick.LinearLocator(25))
        text = ax1.get_xticks().tolist()
        for i in range(len(text)):
            k = int(text[i])
            text[i] = str(date_time[k][0:11] + '\n' + date_time[k][11:23])
        ax1.set_xticklabels(text, fontsize = 6, fontweight = 'bold')
        fig.subplots_adjust(top=0.92)
        fig.suptitle('File: ' + parent_filename + ' at ' + str(num_freq) + ' MHz', fontsize = 8, fontweight='bold')
        fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
        fig.text(0.11, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
        pylab.savefig(result_path + '/' + parent_filename + ' interferometric responce at '+ str(num_freq)+' MHz.png', bbox_inches = 'tight', dpi = 160)
        #pylab.show()
        plt.close('all')


        experiment = np.abs(np.fft.fft(y_value[0, :]))
        experiment[0] = np.nan
        ymax = np.max(experiment[1:])
        if source == 'SygA': ampl_list_SygA.append(ymax)
        if source == 'CasA': ampl_list_CasA.append(ymax)

        #'''
        fig = plt.figure(figsize = (12, 5))
        fig.suptitle('Spectra of the interferometric responce', fontsize = 8, fontweight='bold')
        ax1 = fig.add_subplot(121)
        ax1.set_title('Spectra', fontsize = 6)
        ax1.plot(experiment, linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
        ax1.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center') # xy=(xmax, 2 + 0.3)
        ax1.set_xlim([0, int(len(experiment)/10)])
        ax2 = fig.add_subplot(122)
        ax2.set_title('Spectra', fontsize = 6)
        ax2.plot(10 * np.log10(experiment), linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
        ymax = np.max(10 * np.log10(experiment[1:]))
        ax2.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center')
        ax2.set_xlim([0, int(len(experiment)/10)])
        ax2.set_ylim([-100, -50])
        pylab.savefig(result_path + '/' + parent_filename + ' spectra of interferometric responce at '+ str(num_freq)+' MHz.png', bbox_inches = 'tight', dpi = 160)
        plt.close('all')
        #'''


if freq_list_SygA != freq_list_CasA:
    print ('   ERROR! Frequencies of analysis for two sources do not match!!! \n\n')
    sys.exit('           Program stopped! \n\n')

#flux_ratio = np.zeros(len(ampl_list_CasA))
flux_ratio = []
for i in range(len(ampl_list_CasA)):
    flux_ratio.append(ampl_list_CasA[i] / ampl_list_SygA[i])

print('\n Frequency, MHz   Flux ratio')
for i in range (len(freq_list_SygA)):
    print('   ', freq_list_SygA[i], '         ', np.round(flux_ratio[i], 3))    # , ampl_list_SygA[i], ampl_list_CasA[i]

#'''
fig = plt.figure(figsize = (10, 5))
fig.suptitle('Flux ratio with frequency', fontsize = 8, fontweight='bold')
ax1 = fig.add_subplot(111)
ax1.set_title('Ratio of interferometric responces for files:', fontsize = 6)
ax1.plot(freq_list_SygA, flux_ratio, 'ro',  label = 'Measured points')
for i in range (len(freq_list_SygA)):
    ax1.annotate(str(np.round(flux_ratio[i],3)),  xy=(freq_list_SygA[i], flux_ratio[i]+0.1), fontsize = 6, ha='center')
ax1.set_xlim([6, 34])
ax1.set_ylim([0, 2])
ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
ax1.set_xlabel('Frequency, MHz', fontsize=6, fontweight='bold')
ax1.set_ylabel('Flux ratio', fontsize=6, fontweight='bold')
plt.xticks([8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32])
pylab.savefig(result_path + '/' + 'Flux ratio with frequency.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''

endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program TXT reader has finished! *** \n\n\n')
