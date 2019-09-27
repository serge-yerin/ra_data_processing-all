# Python3
Software_name = 'CasA secular decrease TXT reader'
Software_version = '2019.09.25'
# Script intended to read, show and analyze data from

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files

#path_to_data_SygA =  'DATA/DAT_Results_D250719_165520.jds_3C405/'
#path_to_data_CasA =  'DATA/DAT_Results_D250719_230437.jds_3C461/'

path_to_data_SygA =  'DATA/DAT_Results_D280719_183754.jds_3C405/'
path_to_data_CasA =  'DATA/DAT_Results_D280719_225845.jds_3C461/'


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

file_name_SygA = find_between(path_to_data_SygA, 'Results_', '_3C')
file_name_CasA = find_between(path_to_data_CasA, 'Results_', '_3C')

#result_path = 'CasA_secular_decrease_' + file_name_SygA + '_' + file_name_CasA
result_path = 'CasA secular decrease measurements results'
if not os.path.exists(result_path):
    os.makedirs(result_path)

freq_list_CasA_CRe = []
freq_list_SygA_CRe = []
ampl_list_CasA_CRe = []
ampl_list_SygA_CRe = []
freq_list_CasA_CIm = []
freq_list_SygA_CIm = []
ampl_list_CasA_CIm = []
ampl_list_SygA_CIm = []

file_text = []

for source in ['SygA', 'CasA']:

    if source == 'SygA': path_to_data = path_to_data_SygA
    if source == 'CasA': path_to_data = path_to_data_CasA


    # Finding TXT files with interferometric responces in the folder
    print('')
    file_name_list = find_files_only_in_current_folder(path_to_data, '.txt', 1)


    # Reading description of the observation from INFO file
    info_txt_file = find_files_only_in_current_folder(path_to_data, '.info', 0)
    TXT_file = open(path_to_data + info_txt_file[0], "r")
    for line in TXT_file:                # Loop by all lines in file
        file_text.append(line)
        if line.startswith(" Description:"):  # Searching comments
            words_in_line = line.split()
            if source == 'SygA': description_SygA = words_in_line[1]    # reading description of data file
            if source == 'CasA': description_CasA = words_in_line[1]    # reading description of data file
    TXT_file.close()

    # Loop by found TXT files in the folder
    for file_no in range (len(file_name_list)):

        data_type = find_between(file_name_list[file_no], '_', '.jds')[-3:]


        # *** Reading files ***
        [x_value, y_value] = read_date_time_and_one_value_txt ([path_to_data + file_name_list[file_no]])

        y_value = np.array(y_value)
        a, b = y_value.shape
        date_time = x_value[0][:]

        text_freq = find_between(file_name_list[file_no], 'at ', ' MHz')
        num_freq = np.float(text_freq)
        if data_type == 'CIm' and source == 'SygA': freq_list_SygA_CIm.append(num_freq)
        if data_type == 'CRe' and source == 'SygA': freq_list_SygA_CRe.append(num_freq)
        if data_type == 'CIm' and source == 'CasA': freq_list_CasA_CIm.append(num_freq)
        if data_type == 'CRe' and source == 'CasA': freq_list_CasA_CRe.append(num_freq)

        parent_filename = find_between(path_to_data + file_name_list[0], path_to_data, ' variation')

        x_center = int(b/2) # Central point in time axis (culmination time usually)

        amplitude = (np.max(y_value[0, :]) + np.abs(np.min(y_value[0, :])))/2



        #*******************************************************************************
        #                                F I G U R E S                                 *
        #*******************************************************************************
        '''
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

        '''
        experiment = np.abs(np.fft.fft(y_value[0, :]))
        experiment[0] = np.nan
        ymax = np.max(experiment[1:])
        if data_type == 'CIm' and source == 'SygA': ampl_list_SygA_CIm.append(ymax)
        if data_type == 'CRe' and source == 'SygA': ampl_list_SygA_CRe.append(ymax)
        if data_type == 'CIm' and source == 'CasA': ampl_list_CasA_CIm.append(ymax)
        if data_type == 'CRe' and source == 'CasA': ampl_list_CasA_CRe.append(ymax)

        #'''
        rc('font', size = 6, weight='bold')
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
        if source == 'SygA': path = path_to_data_SygA
        if source == 'CasA': path = path_to_data_CasA
        pylab.savefig(path + parent_filename + ' spectra of interferometric responce at '+ str(num_freq)+' MHz.png', bbox_inches = 'tight', dpi = 160)
        plt.close('all')
        #'''


if freq_list_SygA_CRe != freq_list_CasA_CRe:
    print ('   ERROR! Frequencies of analysis for two sources do not match!!! \n\n')
    sys.exit('           Program stopped! \n\n')



# Calculating the flux ratio
flux_ratio_CRe = []
flux_ratio_CIm = []
for i in range(len(ampl_list_CasA_CRe)):
    flux_ratio_CIm.append(ampl_list_CasA_CIm[i] / ampl_list_SygA_CIm[i])
    flux_ratio_CRe.append(ampl_list_CasA_CRe[i] / ampl_list_SygA_CRe[i])

# Printing to terminal the calculated ratios
print('\n Frequency, MHz  |  Flux ratio Re  |  Flux ratio Im')
for i in range (len(freq_list_SygA_CRe)):
    print('   ', freq_list_SygA_CRe[i], '          ', ''.join(format(np.round(flux_ratio_CRe[i], 5), "8.5f")), '        ', ''.join(format(np.round(flux_ratio_CIm[i], 5), "8.5f")))

# Making string of observations start date
date_of_experiment = '20' + file_name_SygA[5:7] + '.' + file_name_SygA[3:5] + '.' + file_name_SygA[1:3]


# Making a figure of flux ratio with frequency
#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (10, 5))
fig.suptitle('Flux ratio of Cas A and Syg A with frequency', fontsize = 8, fontweight='bold')
ax1 = fig.add_subplot(111)
ax1.set_title('Ratio of interferometric responces for files: ' + file_name_SygA + ' and ' + file_name_CasA + '\n Syg A description: '+ description_SygA + ', Cas A description: '+ description_CasA, fontsize = 7)
ax1.plot(freq_list_SygA_CRe, flux_ratio_CRe, 'ro',  label = 'Real part of correlation')
ax1.plot(freq_list_SygA_CIm, flux_ratio_CIm, 'bo', alpha = 0.7, label = 'Imag part of correlation')
#for i in range (len(freq_list_SygA)):
#    ax1.annotate(str(np.round(flux_ratio[i],3)),  xy=(freq_list_SygA[i], flux_ratio[i]+0.1), fontsize = 6, ha='center')
if file_name_SygA[-3:] == 'jds': ax1.set_xlim([6, 34])
if file_name_SygA[-3:] == 'adr': ax1.set_xlim([8, 80])
ax1.set_ylim([0, 2])
ax1.legend(loc = 'upper left')
ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
ax1.set_xlabel('Frequency, MHz', fontsize=6, fontweight='bold')
ax1.set_ylabel('Flux ratio', fontsize=6, fontweight='bold')
if file_name_SygA[-3:] == 'jds': plt.xticks([8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32])
if file_name_SygA[-3:] == 'adr': plt.xticks([10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75])
fig.text(0.09, 0.95, date_of_experiment, fontsize = 8, fontweight='bold', transform=plt.gcf().transFigure)
fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
fig.text(0.09, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
pylab.savefig(result_path + '/' + date_of_experiment + ' Flux ratio with frequency for files '+file_name_SygA+'_'+file_name_CasA+'.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''

# Saving data on flux ratio to TXT file
TXT_file = open(result_path + '/' + date_of_experiment + ' Flux ratio with frequency for files '+file_name_SygA+'_'+file_name_CasA+'.txt', "w")
TXT_file.write('#  Ratio of interferometric responces of Cas A and Syg A with frequency \n#\n')
for i in range (len(file_text)):
    TXT_file.write('# ' + file_text[i])
TXT_file.write('# \n# Frequency, MHz | Flux ratio Re | Flux ratio Im \n')
for i in range(len(freq_list_SygA_CRe)):
    TXT_file.write('     ' + str(freq_list_SygA_CRe[i]) + '          ' +''.join(format(np.round(flux_ratio_CRe[i], 5), "8.5f")) + '        ' + ''.join(format(np.round(flux_ratio_CIm[i], 5), "8.5f")) + '\n')
TXT_file.close()



endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program ' + Software_name + ' has finished! *** \n\n\n')
