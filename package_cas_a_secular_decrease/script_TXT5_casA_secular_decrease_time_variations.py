# Python3
Software_name = 'CasA secular decrease TXT time variations'
Software_version = '2020.01.08'
# Script intended to read, show and analyze data from

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files

path_to_data =    'DATA/Frequency responces processed GURT/'

y_auto = 1
Vmin = -100 * 10**(-12)
Vmax =  100 * 10**(-12)
#interferometer_base = 400 #900
zero_for_log = 0.0000000000001
customDPI = 300                     # Resolution of images of dynamic spectra

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
c = 2.997 * 10**8

import os
from os import path
import sys
import numpy as np
import pandas as pd
import pylab
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import ticker as mtick
import time

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_common_modules.text_manipulations import find_between, read_date_time_and_one_value_txt
from package_common_modules.find_subfolders_in_folder import find_subfolders_in_folder
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
print ('  Today is ', currentDate, ' time is ', currentTime, '\n')


# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
path_to_results = 'RESULTS CasA decrease GURT absolute amplitudes/'
if not os.path.exists(path_to_results):
    os.makedirs(path_to_results)

# Preparing empty pandas data frame
data_frame = pd.DataFrame(columns=['Date', 'Frequencies, MHz', 'Amplitude CasA Re', 'Amplitude CasA Im', 'Amplitude SygA Re', 'Amplitude SygA Im'])

# Searching of the directories with needed data in predefined directory
folder_list =  find_subfolders_in_folder(path_to_data, 0)

# Excluding the folders that are in subfolders of current folder
temp_subfolder_list = []
for i in range(len(folder_list)):
    temp = folder_list[i]
    if ('/' not in temp.replace(path_to_data,'')) and ('\\' not in temp.replace(path_to_data,'')):
        temp_subfolder_list.append(folder_list[i])

# The logic of the next folder selection is stupid. Sorry for that.
# It is inherited from other script

# Taking the pairs of folders and process them with standard script
for subfolder in range(len(temp_subfolder_list)//2): #
    only_subfolder_list = []
    only_subfolder_list.append(temp_subfolder_list[2*subfolder])
    only_subfolder_list.append(temp_subfolder_list[2*subfolder+1])

    # Finding the folder that ends with needed source names
    # !!! There should be only one subfolder with this source name !!!

    for i in range(len(only_subfolder_list)):
        if only_subfolder_list[i].endswith('3C405'):
            path_to_data_SygA = only_subfolder_list[i]+'/'
        if only_subfolder_list[i].endswith('3C461'):
            path_to_data_CasA = only_subfolder_list[i]+'/'


    # Finding the initial data files names in the folder names
    file_name_SygA = find_between(path_to_data_SygA, 'Results_', '_3C')
    file_name_CasA = find_between(path_to_data_CasA, 'Results_', '_3C')

    '''
    if   '.jds' in path_to_data_SygA and '.jds' in path_to_data_CasA:
        result_path = 'CasA secular decrease UTR2 time variations'
    elif '.adr' in path_to_data_SygA and '.adr' in path_to_data_CasA:
        result_path = 'CasA secular decrease GURT time variations'
    else:
        print ('   ERROR! Cannot find the correct file extension in folder name!!! \n\n')
        sys.exit('           Program stopped! \n\n')

    if not os.path.exists(result_path):
        os.makedirs(result_path)
    '''

    freq_list_CasA_CRe = []
    freq_list_SygA_CRe = []
    ampl_list_CasA_CRe = []
    ampl_list_SygA_CRe = []
    freq_list_CasA_CIm = []
    freq_list_SygA_CIm = []
    ampl_list_CasA_CIm = []
    ampl_list_SygA_CIm = []

    file_text = []
    date_of_experiment_spectra = ''

    for source in ['SygA', 'CasA']:

        if source == 'SygA': path_to_data = path_to_data_SygA
        if source == 'CasA': path_to_data = path_to_data_CasA


        # Finding TXT files with interferometric responces in the folder

        file_name_list = find_files_only_in_current_folder(path_to_data, '.txt', 0)


        # Reading description of the observation from INFO file
        info_txt_file = find_files_only_in_current_folder(path_to_data, '.info', 0)
        TXT_file = open(path_to_data + info_txt_file[0], "r")
        for line in TXT_file:                # Loop by all lines in file
            file_text.append(line)
            if line.startswith(" Description:"):  # Searching comments
                words_in_line = line.split()
                if source == 'SygA': description_SygA = words_in_line[1]    # reading description of data file
                if source == 'CasA': description_CasA = words_in_line[1]    # reading description of data file
            if line.startswith(" Culmination"):  # Searching comments
                words_in_line = line.split()
                if source == 'SygA':
                    date_of_experiment_spectra = words_in_line[2]
        TXT_file.close()

        # Loop by found TXT files in the folder
        for file_no in range (len(file_name_list)):

            if '.jds' in file_name_list[file_no]:
                data_type = find_between(file_name_list[file_no], '_', '.jds')[-3:]
            if '.adr' in file_name_list[file_no]:
                data_type = find_between(file_name_list[file_no], '_', '.adr')[-3:]

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


            # Specter of initial signal
            experiment_spectra = np.fft.fft(y_value[0, :])
            ampl_spectra = np.abs(experiment_spectra)
            ymax = np.max(ampl_spectra)
            max_index = np.argmax(ampl_spectra[0:50])


            # Filtering of data
            if   max_index <= 2:
                experiment_spectra[max_index + 3 :] = zero_for_log
            else:
                experiment_spectra[max_index + 3 : ] = zero_for_log
                experiment_spectra[ : max_index - 2] = zero_for_log

            # Making inverse FFT to obtain the cleaned response
            filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))

            # Finding the maximal absolute value of the response
            ymax = 2 * np.max(np.abs(filtered_signal_re))

            if data_type == 'CIm' and source == 'SygA': ampl_list_SygA_CIm.append(ymax)
            if data_type == 'CRe' and source == 'SygA': ampl_list_SygA_CRe.append(ymax)
            if data_type == 'CIm' and source == 'CasA': ampl_list_CasA_CIm.append(ymax)
            if data_type == 'CRe' and source == 'CasA': ampl_list_CasA_CRe.append(ymax)

    if freq_list_SygA_CRe != freq_list_CasA_CRe:
        print ('   ERROR! Frequencies of analysis for two sources do not match!!! \n\n')
        sys.exit('           Program stopped! \n\n')

    # Making string of observations start date
    if date_of_experiment_spectra == '':
        #print(' No')
        if '.jds' in file_name_list[file_no]:
            date_of_experiment_spectra = '20' + file_name_SygA[5:7] + '.' + file_name_SygA[3:5] + '.' + file_name_SygA[1:3]
        if '.adr' in file_name_list[file_no]:
            date_of_experiment_spectra = '20' + file_name_SygA[1:3] + '.' + file_name_SygA[3:5] + '.' + file_name_SygA[5:7]

    date_of_experiment_spectra = date_of_experiment_spectra.replace('-','.')

    # adding new line to data frame
    data_frame.loc[subfolder] = [date_of_experiment_spectra, freq_list_SygA_CRe, ampl_list_CasA_CRe, ampl_list_CasA_CIm, ampl_list_SygA_CRe, ampl_list_SygA_CIm]
    print('  Date processed: ', date_of_experiment_spectra)

    # print(data_frame.keys())
    # print(*data_frame['Frequencies, MHz'])
    # print('Index =', (data_frame['Frequencies, MHz'].tolist())[0][0])
    # print('Index =', (data_frame['Frequencies, MHz'].tolist())[0][1])

# print('Data: ', np.array(data_frame['Amplitude CasA Re'].tolist()).transpose()[3][:])
# print('Dates:', (data_frame['Date'].tolist())[:])
# print('Label:', np.array(data_frame['Frequencies, MHz'].tolist()).transpose()[3][0])

freq_num = len(data_frame['Frequencies, MHz'].tolist()[0][:])
print('\n  Number of frequencies:', freq_num)

for i in range(freq_num):

    x_data = data_frame['Date'].tolist()[:]
    y_data_1 = np.array(data_frame['Amplitude CasA Re'].tolist()).transpose()[i][:]
    y_data_2 = np.array(data_frame['Amplitude CasA Im'].tolist()).transpose()[i][:]
    y_data_3 = np.array(data_frame['Amplitude SygA Re'].tolist()).transpose()[i][:]
    y_data_4 = np.array(data_frame['Amplitude SygA Im'].tolist()).transpose()[i][:]
    data_label = str(np.array(data_frame['Frequencies, MHz'].tolist()).transpose()[i][0]) + ' MHz'

    rc('font', size = 10, weight='bold')
    fig = plt.figure(1, figsize=(16.0, 8.0))
    fig.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)

    ax1 = fig.add_subplot(211)
    ax1.plot(x_data, y_data_1, label = 'Amplitude CasA Re ' + data_label)
    ax1.plot(x_data, y_data_2, label = 'Amplitude CasA Im ' + data_label)
    ax1.scatter(np.linspace(0, len(x_data) - 1, num = len(x_data)), y_data_1, color='b')
    ax1.scatter(np.linspace(0, len(x_data) - 1, num = len(x_data)), y_data_2, color='r')

    ax1.set_title('Cassiopeia A', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    ax1.legend(loc = 'upper right', fontsize = 10)
    #ax1.set_xlabel('Date', fontsize = 10, fontweight='bold')
    ax1.set_ylabel('Interferometric response amplitude', fontsize = 10, fontweight='bold')
    #plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45 )
    ax1.axes.get_xaxis().set_ticks([])

    ax2 = fig.add_subplot(212)
    ax2.plot(x_data, y_data_3, label = 'Amplitude SygA Re ' + data_label)
    ax2.plot(x_data, y_data_4, label = 'Amplitude SygA Im ' + data_label)
    ax2.scatter(np.linspace(0, len(x_data) - 1, num=len(x_data)), y_data_3, color='b')
    ax2.scatter(np.linspace(0, len(x_data) - 1, num=len(x_data)), y_data_4, color='r')

    ax2.set_title('Sygnus A', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    ax2.legend(loc = 'upper right', fontsize = 10)
    ax2.set_xlabel('Date', fontsize = 10, fontweight='bold')
    ax2.set_ylabel('Interferometric response amplitude', fontsize = 10, fontweight='bold')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45 )

    pylab.savefig(path_to_results + 'Absolute amplitudes at ' + data_label + '.png', bbox_inches='tight', dpi = customDPI)
    plt.close('all')


date_num = len(data_frame['Date'].tolist())
print('\n  Number of dates:', date_num)

for i in range(date_num):

    x_data = data_frame['Frequencies, MHz'].tolist()[0][18:]
    y_data_1 = np.array(data_frame['Amplitude CasA Re'].tolist())[i][18:]
    y_data_2 = np.array(data_frame['Amplitude CasA Im'].tolist())[i][18:]
    y_data_3 = np.array(data_frame['Amplitude SygA Re'].tolist())[i][18:]
    y_data_4 = np.array(data_frame['Amplitude SygA Im'].tolist())[i][18:]
    data_label = data_frame['Date'].tolist()[i]

    rc('font', size = 6, weight='bold')
    fig = plt.figure(figsize = (10, 8))
    fig.suptitle('Amplitudes of Cas A interferometric responses with frequency', fontsize = 8, fontweight='bold')
    fig.subplots_adjust(left=None, bottom=0, right=None, top=0.95, wspace=None, hspace=None)
    ax1 = fig.add_subplot(211)
    #ax1.set_title('Statistics calculated from ' + str(len(file_name_list)) + ' files', fontsize = 7)
    ax1.plot(x_data, y_data_1, label = 'Amplitude CasA Re ' + data_label)
    ax1.plot(x_data, y_data_1, 'bo')
    ax1.plot(x_data, y_data_2, label = 'Amplitude CasA Im ' + data_label)
    ax1.plot(x_data, y_data_2, 'ro')
    ax1.set_xlim([28, 80])
    ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
    ax1.set_xlabel('Frequency, MHz', fontsize=6, fontweight='bold')
    ax1.set_ylabel('Amplitude', fontsize=6, fontweight='bold')
    ax1.legend(loc = 'upper right')

    ax2 = fig.add_subplot(212)
    #ax1.set_title('Statistics calculated from ' + str(len(file_name_list)) + ' files', fontsize = 7)
    ax2.plot(x_data, y_data_3, label = 'Amplitude SygA Re ' + data_label)
    ax2.plot(x_data, y_data_3, 'bo')
    ax2.plot(x_data, y_data_4, label = 'Amplitude SygA Im ' + data_label)
    ax2.plot(x_data, y_data_4, 'ro')
    ax2.set_xlim([28, 80])
    ax2.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
    ax2.set_xlabel('Frequency, MHz', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Amplitude', fontsize=6, fontweight='bold')
    ax2.legend(loc = 'upper right')

    #fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
    #fig.text(0.09, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
    pylab.savefig(path_to_results + 'Amplitude vs frequency ' + data_label + '.png', bbox_inches = 'tight', dpi = 160)
    plt.close('all')



endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program ' + Software_name + ' has finished! *** \n\n\n')
