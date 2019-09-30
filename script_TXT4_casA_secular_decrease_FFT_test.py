# Python3
Software_name = 'CasA secular decrease test for specter filtering'
Software_version = '2019.09.28'
# Script intended to read TXT files with results of Cas A - Syg A fluxes ration and calculate statistics

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
path_to_data =  'DATA/TEST/'
file_name = 'D280719_183754_CIm.jds variation at 24.005 MHz.txt'
Vmin = -14 * 10**-9
Vmax =  14 * 10**-9
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
from matplotlib import ticker as mtick

from package_common_modules.text_manipulations import find_between, read_date_time_and_one_value_txt
from package_plot_formats.plot_formats import OneValueWithTimePlot
#from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
################################################################################

def spectra_plot(ampl_spectra, max_index, ymax, suptitle, name, path_to_data):
    rc('font', size = 6, weight='bold')
    fig = plt.figure(figsize = (12, 5))
    fig.suptitle(suptitle, fontsize = 8, fontweight='bold')
    ax1 = fig.add_subplot(121)
    ax1.set_title('Spectra', fontsize = 6)
    ax1.plot(ampl_spectra, linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
    ax1.scatter(np.linspace(0, len(ampl_spectra)-1, num = len(ampl_spectra)), ampl_spectra, color = 'r')
    ax1.annotate(str(np.round(ymax,5)),  xy=(max_index+15, ymax), fontsize = 6, ha='center') # xy=(xmax, 2 + 0.3)
    ax1.set_xlim([0, int(len(ampl_spectra)/10)])
    ax2 = fig.add_subplot(122)
    ax2.set_title('Spectra', fontsize = 6)
    ax2.plot(10 * np.log10(ampl_spectra), linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
    ax2.scatter(np.linspace(0, len(ampl_spectra)-1, num = len(ampl_spectra)), 10 * np.log10(ampl_spectra), color = 'r')
    ax2.annotate(str(np.round(10 * np.log10(ymax),5)),  xy=(max_index+15, 10 * np.log10(ymax)), fontsize = 6, ha='center')
    ax2.set_xlim([0, int(len(ampl_spectra)/10)])
    #ax2.set_ylim([-100, -50])
    pylab.savefig(path_to_data + name, bbox_inches = 'tight', dpi = 160)
    plt.close('all')
    return




def responce_plot(signal, suptitle, name, path_to_data, Vmin, Vmax, date_time):
    rc('font', size = 6, weight='bold')
    fig = plt.figure(figsize = (9, 5))
    fig.suptitle(suptitle, fontsize = 8, fontweight='bold')
    ax1 = fig.add_subplot(111)
    plt.axvline(x = x_center, linewidth = '0.5' , color = 'r') #, alpha=0.5
    ax1.plot(signal, linestyle = '-', linewidth = '1.00', label = 'Measured')
    #ax1.plot(2 * filtered_signal_im, linestyle = '-', linewidth = '1.00', label = 'Measured')
    ax1.legend(loc = 'upper right', fontsize = 6)
    ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
    #if y_auto == 0: ax1.set_ylim([Vmin, Vmax])
    ax1.set_ylim([Vmin, Vmax])
    ax1.set_xlim([0, b-1])
    ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
    #ax1.set_title('Base: '+str(interferometer_base) + ' m., amplitude: ' + ('%.4e' % amplitude) + ', vertical offset: ' + ('%.4e' % vertical_offset), fontsize = 6)
    ax1.set_xlabel('UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', fontsize=6, fontweight='bold')
    ax1.xaxis.set_major_locator(mtick.LinearLocator(7))
    #ax1.xaxis.set_minor_locator(mtick.LinearLocator(25))
    text = ax1.get_xticks().tolist()
    for i in range(len(text)):
        k = int(text[i])
        text[i] = str(date_time[k][0:11] + '\n' + date_time[k][11:23])
    ax1.set_xticklabels(text, fontsize = 6, fontweight = 'bold')
    fig.subplots_adjust(top=0.92)
    #fig.suptitle('File: ' + parent_filename + ' at ' + str(num_freq) + ' MHz', fontsize = 8, fontweight='bold')
    #fig.text(0.79, 0.03, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
    #fig.text(0.11, 0.03, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
    pylab.savefig(path_to_data + name, bbox_inches = 'tight', dpi = 160)
    plt.close('all')









#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************
print ('\n\n\n\n\n\n\n\n   **********************************************************************************')
print ('   *     ', Software_name, '  v.', Software_version,'         *      (c) YeS 2019')
print ('   ********************************************************************************** \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)



#*******************************************************************************
#                          R E A D I N G   D A T A                             *
#*******************************************************************************


# *** Reading files ***
[x_value, y_value] = read_date_time_and_one_value_txt ([path_to_data + file_name])

y_value = np.array(y_value)
a, b = y_value.shape
date_time = x_value[0][:]

x_center = int(b/2) # Central point in time axis (culmination time usually)
amplitude = (np.max(y_value[0, :]) + np.abs(np.min(y_value[0, :])))/2



#*******************************************************************************
#                                F I G U R E S                                 *
#*******************************************************************************

print ('\n\n\n  *** Building images *** \n\n')

# Initial signal

responce_plot(y_value[0, :], 'Interferometric responce initial experimental',
            '02 - Interferometric responce 01.png', path_to_data, Vmin, Vmax, date_time)


# Specter of initial signal
experiment_spectra = np.fft.fft(y_value[0, :])

# Making mplitude of zero frequency eqal to zero
experiment_spectra[0] = 0.000000001 #np.nan
ampl_spectra = np.abs(experiment_spectra)
ymax = np.max(ampl_spectra)
max_index = np.argmax(ampl_spectra[0:50])

spectra_plot(ampl_spectra, max_index, ymax,
            'Spectra of the initial interferometric responce',
            '01 - Spectra of interferometric responce 01.png', path_to_data)


#*******************************************************************************
# Specter of signal without higher frequencies

experiment_spectra[50:] = 0.000000001
ampl_spectra = np.abs(experiment_spectra)
max_index = np.argmax(ampl_spectra)

spectra_plot(ampl_spectra, max_index, ymax,
            'Spectra of the interferometric responce without high frequencies',
            '01 - Spectra of interferometric responce 02.png', path_to_data)

# Signal without higher frequencies

filtered_signal_im = np.imag(np.fft.ifft(experiment_spectra))
filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))

responce_plot(2 * filtered_signal_re, 'Interferometric responce without high frequencies',
            '02 - Interferometric responce 02.png', path_to_data, Vmin, Vmax, date_time)

#*******************************************************************************
# Signal without higher frequencies and filtered to 9 harmonics


if   max_index <= 4:
    experiment_spectra[max_index + 5 : ] = 0.000000001
else:
    experiment_spectra[max_index + 5 : ] = 0.000000001
    experiment_spectra[ : max_index - 4] = 0.000000001

ampl_spectra = np.abs(experiment_spectra)
max_index = np.argmax(ampl_spectra)
ymax = ampl_spectra[max_index]

spectra_plot(ampl_spectra, max_index, ymax,
            'Spectra of the interferometric responce 9 harmonics',
            '01 - Spectra of interferometric responce 03.png', path_to_data)


filtered_signal_im = np.imag(np.fft.ifft(experiment_spectra))
filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))


responce_plot(2 * filtered_signal_re, 'Interferometric responce only 9 harmonics',
            '02 - Interferometric responce 03.png', path_to_data, Vmin, Vmax, date_time)


#*******************************************************************************
# Signal without higher frequencies and filtered to 7 harmonics

if   max_index <= 3:
    experiment_spectra[max_index + 4:] = 0.000000001
else:
    experiment_spectra[max_index + 4 : ] = 0.000000001
    experiment_spectra[ : max_index - 3] = 0.000000001

ampl_spectra = np.abs(experiment_spectra)
max_index = np.argmax(ampl_spectra)
ymax = ampl_spectra[max_index]


spectra_plot(ampl_spectra, max_index, ymax,
            'Spectra of the interferometric responce 7 harmonics',
            '01 - Spectra of interferometric responce 04.png', path_to_data)


filtered_signal_im = np.imag(np.fft.ifft(experiment_spectra))
filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))

responce_plot(2 * filtered_signal_re, 'Interferometric responce only 7 harmonics',
            '02 - Interferometric responce 04.png', path_to_data, Vmin, Vmax, date_time)


#*******************************************************************************
# Signal without higher frequencies and filtered to 5 harmonics

if   max_index <= 2:
    experiment_spectra[max_index + 3 :] = 0.000000001
else:
    experiment_spectra[max_index + 3 : ] = 0.000000001
    experiment_spectra[ : max_index - 2] = 0.000000001

ampl_spectra = np.abs(experiment_spectra)
max_index = np.argmax(ampl_spectra)
ymax = ampl_spectra[max_index]


spectra_plot(ampl_spectra, max_index, ymax,
            'Spectra of the interferometric responce 5 harmonics',
            '01 - Spectra of interferometric responce 05.png', path_to_data)


filtered_signal_im = np.imag(np.fft.ifft(experiment_spectra))
filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))

responce_plot(2 * filtered_signal_re, 'Interferometric responce only 5 harmonics',
            '02 - Interferometric responce 05.png', path_to_data, Vmin, Vmax, date_time)

#*******************************************************************************
# Signal without higher frequencies and filtered to 3 harmonics

if   max_index <= 1:
    experiment_spectra[max_index + 2:] = 0.000000001
else:
    experiment_spectra[max_index + 2 : ] = 0.000000001
    experiment_spectra[ : max_index - 1] = 0.000000001

ampl_spectra = np.abs(experiment_spectra)
max_index = np.argmax(ampl_spectra)
ymax = ampl_spectra[max_index]


spectra_plot(ampl_spectra, max_index, ymax,
            'Spectra of the interferometric responce 3 harmonics',
            '01 - Spectra of interferometric responce 06.png', path_to_data)


filtered_signal_im = np.imag(np.fft.ifft(experiment_spectra))
filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))

responce_plot(2 * filtered_signal_re, 'Interferometric responce only 3 harmonics',
            '02 - Interferometric responce 06.png', path_to_data, Vmin, Vmax, date_time)

#*******************************************************************************
# Signal without higher frequencies and filtered to only 1 harmonic

experiment_spectra[max_index + 1 : ] = 0.000000001
experiment_spectra[0 : max_index] = 0.000000001

ampl_spectra = np.abs(experiment_spectra)
max_index = np.argmax(ampl_spectra)
ymax = ampl_spectra[max_index]


spectra_plot(ampl_spectra, max_index, ymax,
            'Spectra of the interferometric responce 1 harmonic',
            '01 - Spectra of interferometric responce 07.png', path_to_data)


filtered_signal_im = np.imag(np.fft.ifft(experiment_spectra))
filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))

responce_plot(2 * filtered_signal_re, 'Interferometric responce only 1 harmonic',
            '02 - Interferometric responce 07.png', path_to_data, Vmin, Vmax, date_time)





endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program ' + Software_name + ' has finished! *** \n\n\n')
