# Python3
Software_version = '2019.05.06'
# Script intended to read, show and analyze data from

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
path_to_data =  'DATA_for_DAT_reader_development/DAT_Results_E280719_225850.jds/'
y_auto = 1
Vmin = -500 * 10**(-12)
Vmax =  500 * 10**(-12)

interferometer_base = 900
amplitude = 0.021 * 10**-8
vertical_offset = -0.002 * 10**-8

customDPI = 300                     # Resolution of images of dynamic spectra

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
c = 2.997 * 10**8

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
print ('\n\n\n\n\n\n\n\n   ****************************************************')
print ('   *          TXT data files reader  v1.0             *      (c) YeS 2016')
print ('   ****************************************************      \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, '\n')


# Finding TXT files in the folder
file_name_list = find_files_only_in_current_folder(path_to_data, '.txt', 1)


for file_no in range (1): #len(file_name_list)

    # *** Reading files ***
    [x_value, y_value] = read_date_time_and_one_value_txt ([path_to_data + file_name_list[file_no]])

    y_value = np.array(y_value)
    a, b = y_value.shape
    date_time = x_value[0][:]

    text_freq = find_between(file_name_list[file_no], 'at ', ' MHz')
    num_freq = np.float(text_freq)
    parent_filename = find_between(path_to_data + file_name_list[0], path_to_data, ' Intensity')

    x_center = int(b/2) # Central point in time axis
    theta = np.linspace(90-15, 90+15, num = b) * np.pi / 180 # Angle of wave coming

    angle_line = np.linspace(0-15, 0+15, num = b) * np.pi / 180
    addition_angle = ((1 - np.cos(angle_line) )**1) * np.sign(angle_line) * (7.5) * np.pi / 180

    theta = theta - addition_angle

    pattern = np.sinc(3*(theta[:] - np.pi/2))

    theory = np.zeros(b)

    if 'CRe' in parent_filename:
        theory[:] = amplitude * np.cos(1 * np.pi * num_freq * 10**6 * interferometer_base * np.cos(theta[:]) / c ) * pattern
    elif 'CIm' in parent_filename:
        theory[:] = amplitude * np.sin(1 * np.pi * num_freq * 10**6 * interferometer_base * np.cos(theta[:]) / c ) * pattern
    else:
        print ('\n          Error detecting type of data! \n')


    #*******************************************************************************
    #                                F I G U R E S                                 *
    #*******************************************************************************


    rc('font', size = 6, weight='bold')
    fig = plt.figure(figsize = (9, 5))
    ax1 = fig.add_subplot(111)
    plt.axvline(x = x_center, linewidth = '0.5' , color = 'r') #, alpha=0.5
    for i in range (a):
        ax1.plot(theory[:], linestyle = '--', linewidth = '1.50', alpha = 0.5, label = 'Theory')
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
        text[i] = str(date_time[i][0:11] + '\n' + date_time[i][11:23])
    ax1.set_xticklabels(text, fontsize = 6, fontweight = 'bold')
    fig.subplots_adjust(top=0.92)
    fig.suptitle('File: ' + parent_filename + ' at ' + str(num_freq) + ' MHz', fontsize = 8, fontweight='bold')
    fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
    fig.text(0.11, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
    pylab.savefig(path_to_data + parent_filename + ' 01 - All txt data used.png', bbox_inches = 'tight', dpi = 160)
    #pylab.show()
    plt.close('all')


    #'''
    fig = plt.figure(figsize = (9, 5))
    fig.suptitle('Additional and control parameters', fontsize = 8, fontweight='bold')
    ax1 = fig.add_subplot(221)
    ax1.set_title('Additional angle', fontsize = 6)
    for i in range (a):
        ax1.plot(addition_angle * 180 / np.pi, linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Difference')
    ax2 = fig.add_subplot(222)
    ax2.set_title('Antenna pattern ', fontsize = 6)
    for i in range (a):
        ax2.plot(pattern, linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Difference')
    ax3 = fig.add_subplot(223)
    ax3.set_title('Diffrence of theory and measurements ', fontsize = 6)
    for i in range (a):
        ax3.plot(y_value[i, :] + vertical_offset - theory, linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Difference')
    ax4 = fig.add_subplot(224)
    ax4.set_title('Spectra', fontsize = 6)
    ax4.plot(np.abs(np.fft.fft(theory)), linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Theory')
    ax4.plot(np.abs(np.fft.fft(y_value[0, :])), linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
    ax4.set_xlim([0, int(len(theory)/2)])
    #ax4.set_xlim([0, 125])
    pylab.savefig(path_to_data + parent_filename + ' 01 - All txt data used_add.png', bbox_inches = 'tight', dpi = 160)
    #pylab.show()
    plt.close('all')
    #'''





endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program TXT reader has finished! *** \n\n\n')
