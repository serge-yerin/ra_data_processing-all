# Python3
software_name = 'CasA secular decrease test for specter filtering'
software_version = '2019.09.28'
# Script intended to read TXT files with results of Cas A - Syg A fluxes ration and calculate statistics

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Path to data files
path_to_data = 'DATA/TEST/'
file_name = 'A190818_093442_CIm.adr variation at 18.024 MHz.txt'
v_min = -0.2 * 10**-9
v_max =  0.2 * 10**-9
customDPI = 300                     # Resolution of images of dynamic spectra
zero_for_log = 0.0000000000001

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import sys
# import os
from os import path
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib import rc
import time
from matplotlib import ticker as mtick

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_common_modules.text_manipulations import find_between, read_date_time_and_one_value_txt
from package_plot_formats.plot_formats import OneValueWithTimePlot
################################################################################


def spectra_plot(ampl_spectra, max_index, ymax, suptitle, name, path_to_data):
    rc('font', size=6, weight='bold')
    fig = plt.figure(figsize=(12, 5))
    fig.suptitle(suptitle, fontsize=8, fontweight='bold')
    ax1 = fig.add_subplot(121)
    ax1.set_title('Spectra', fontsize=6)
    ax1.plot(ampl_spectra, linestyle='-', linewidth='2.0', alpha=1.0, label='Measurements')
    ax1.scatter(np.linspace(0, len(ampl_spectra)-1, num=len(ampl_spectra)), ampl_spectra, color='r')
    ax1.annotate(str(np.round(ymax, 5)),  xy=(max_index+15, ymax), fontsize=6, ha='center')  # xy=(xmax, 2 + 0.3)
    ax1.set_xlim([0, int(len(ampl_spectra) / 10)])
    ax2 = fig.add_subplot(122)
    ax2.set_title('Spectra', fontsize=6)
    ax2.plot(10 * np.log10(ampl_spectra), linestyle='-', linewidth='2.0', alpha=1.0, label='Measurements')
    ax2.scatter(np.linspace(0, len(ampl_spectra)-1, num=len(ampl_spectra)), 10 * np.log10(ampl_spectra), color='r')
    ax2.annotate(str(np.round(10 * np.log10(ymax), 5)),  xy=(max_index + 15, 10 * np.log10(ymax)), 
                 fontsize=6, ha='center')
    ax2.set_xlim([0, int(len(ampl_spectra)/10)])
    # ax2.set_ylim([-100, -50])
    pylab.savefig(path_to_data + name, bbox_inches='tight', dpi=160)
    plt.close('all')
    return


def response_plot(signal, suptitle, name, path_to_data, v_min, v_max, date_time):
    rc('font', size=6, weight='bold')
    fig = plt.figure(figsize=(9, 5))
    fig.suptitle(suptitle, fontsize=8, fontweight='bold')
    ax1 = fig.add_subplot(111)
    plt.axvline(x=x_center, linewidth='0.5', color='r')  # alpha=0.5
    ax1.plot(signal, linestyle='-', linewidth='1.00', label='Measured')
    # ax1.plot(2 * filtered_signal_im, linestyle = '-', linewidth = '1.00', label = 'Measured')
    ax1.legend(loc='upper right', fontsize=6)
    ax1.grid(b=True, which='both', color='silver', linestyle='-')
    # if y_auto == 0: ax1.set_ylim([v_min, v_max])
    ax1.set_ylim([v_min, v_max])
    ax1.set_xlim([0, b-1])
    ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
    # ax1.set_title('Base: '+str(interferometer_base) + ' m., amplitude: ' + ('%.4e' % amplitude) + 
    # ', vertical offset: ' + ('%.4e' % vertical_offset), fontsize = 6)
    ax1.set_xlabel('UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', fontsize=6, fontweight='bold')
    ax1.xaxis.set_major_locator(mtick.LinearLocator(7))
    # ax1.xaxis.set_minor_locator(mtick.LinearLocator(25))
    text = ax1.get_xticks().tolist()
    for i in range(len(text)):
        k = int(text[i])
        text[i] = str(date_time[k][0:11] + '\n' + date_time[k][11:23])
    ax1.set_xticklabels(text, fontsize=6, fontweight='bold')
    fig.subplots_adjust(top=0.92)
    # fig.suptitle('File: ' + parent_filename + ' at ' + str(num_freq) + ' MHz', fontsize = 8, fontweight='bold')
    # fig.text(0.79, 0.03, 'Processed '+current_date+ ' at '+current_time, fontsize=4, transform=plt.gcf().transFigure)
    # fig.text(0.11, 0.03, 'Software version: '+software_version+', yerin.serge@gmail.com, IRA NASU', 
    # fontsize=4, transform=plt.gcf().transFigure)
    pylab.savefig(path_to_data + name, bbox_inches='tight', dpi=160)
    plt.close('all')


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************
print('\n\n\n\n\n\n\n\n   **********************************************************************************')
print('   *     ', software_name, '  v.', software_version, '         *      (c) YeS 2019')
print('   ********************************************************************************** \n\n\n')

start_time = time.time()
current_time = time.strftime("%H:%M:%S")
current_date = time.strftime("%d.%m.%Y")
print('  Today is ', current_date, ' time is ', current_time)


# *******************************************************************************
#                           R E A D I N G   D A T A                             *
# *******************************************************************************
# *** Reading files ***
[x_value, y_value] = read_date_time_and_one_value_txt([path_to_data + file_name])

y_value = np.array(y_value)
a, b = y_value.shape
date_time = x_value[0][:]

x_center = int(b/2)  # Central point in time axis (culmination time usually)
amplitude = (np.max(y_value[0, :]) + np.abs(np.min(y_value[0, :])))/2


# *******************************************************************************
#                                 F I G U R E S                                 *
# *******************************************************************************

print('\n\n\n  *** Building images *** \n\n')

# Initial signal

response_plot(y_value[0, :], 'Interferometric response initial experimental',
              '02 - Interferometric response 01.png', path_to_data, v_min, v_max, date_time)


# Specter of initial signal
experiment_spectra = np.fft.fft(y_value[0, :])
initial_spectra = experiment_spectra
# Making amplitude of zero frequency equal to zero

ampl_spectra = np.abs(experiment_spectra)
ymax = np.max(ampl_spectra)
max_index = np.argmax(ampl_spectra[0:50])

spectra_plot(ampl_spectra, max_index, ymax,
             'Spectra of the initial interferometric response',
             '01 - Spectra of interferometric response 01.png', path_to_data)


# Phase spectra plot
phase_spectra = np.angle(experiment_spectra, deg=True)

rc('font', size=6, weight='bold')
fig = plt.figure(figsize=(12, 5))
fig.suptitle('Phase spectra of the initial interferometric response', fontsize=8, fontweight='bold')
ax1 = fig.add_subplot(111)
ax1.set_title('Spectra', fontsize=6)
ax1.plot(phase_spectra, linestyle='-', linewidth='2.0', alpha=1.0, label='Measurements')
ax1.scatter(np.linspace(0, len(phase_spectra)-1, num=len(phase_spectra)), phase_spectra, color='r')
ax1.annotate(str(np.round(ymax, 5)),  xy=(max_index+15, ymax), fontsize=6, ha='center')  # xy=(xmax, 2 + 0.3)
ax1.set_xlim([0, int(len(ampl_spectra)/1)])
pylab.savefig(path_to_data + '01a - Phase spectra of interferometric response 01.png', bbox_inches='tight', dpi=160)
plt.close('all')


# *******************************************************************************
#               The same signal after FFT and inverse FFT
# *******************************************************************************

filtered_signal_im = np.imag(np.fft.ifft(initial_spectra))
filtered_signal_re = np.real(np.fft.ifft(initial_spectra))

response_plot(1 * filtered_signal_re, 'Interferometric response  after FFT and inverse FFT',
              '02 - Interferometric response 01a.png', path_to_data, v_min, v_max, date_time)


# *******************************************************************************
#               Spectrum of signal without higher frequencies
# *******************************************************************************

experiment_spectra[0] = zero_for_log  # np.nan
experiment_spectra[25:] = zero_for_log
ampl_spectra = np.abs(experiment_spectra)
max_index = np.argmax(ampl_spectra)

spectra_plot(ampl_spectra, max_index, ymax,
             'Spectra of the interferometric response without high frequencies',
             '01 - Spectra of interferometric response 02.png', path_to_data)

# Signal without higher frequencies

filtered_signal_im = np.imag(np.fft.ifft(experiment_spectra))
filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))

response_plot(2 * filtered_signal_re, 'Interferometric response without high frequencies',
              '02 - Interferometric response 02.png', path_to_data, v_min, v_max, date_time)


# *******************************************************************************
#        Signal without higher frequencies and filtered to 9 harmonics
# *******************************************************************************

if   max_index <= 4:
    experiment_spectra[max_index + 5:] = zero_for_log
else:
    experiment_spectra[max_index + 5:] = zero_for_log
    experiment_spectra[: max_index - 4] = zero_for_log

ampl_spectra = np.abs(experiment_spectra)
max_index = np.argmax(ampl_spectra)
ymax = ampl_spectra[max_index]

spectra_plot(ampl_spectra, max_index, ymax,
             'Spectra of the interferometric response 9 harmonics',
             '01 - Spectra of interferometric response 03.png', path_to_data)


filtered_signal_im = np.imag(np.fft.ifft(experiment_spectra))
filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))


response_plot(2 * filtered_signal_re, 'Interferometric response only 9 harmonics',
              '02 - Interferometric response 03.png', path_to_data, v_min, v_max, date_time)


# *******************************************************************************
#         Signal without higher frequencies and filtered to 7 harmonics
# ******************************************************************************* 

if   max_index <= 3:
    experiment_spectra[max_index + 4:] = zero_for_log
else:
    experiment_spectra[max_index + 4:] = zero_for_log
    experiment_spectra[: max_index - 3] = zero_for_log

ampl_spectra = np.abs(experiment_spectra)
max_index = np.argmax(ampl_spectra)
ymax = ampl_spectra[max_index]


spectra_plot(ampl_spectra, max_index, ymax,
             'Spectra of the interferometric response 7 harmonics',
             '01 - Spectra of interferometric response 04.png', path_to_data)


filtered_signal_im = np.imag(np.fft.ifft(experiment_spectra))
filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))

response_plot(2 * filtered_signal_re, 'Interferometric response only 7 harmonics',
              '02 - Interferometric response 04.png', path_to_data, v_min, v_max, date_time)


# *******************************************************************************
#        Signal without higher frequencies and filtered to 5 harmonics
# *******************************************************************************

if   max_index <= 2:
    experiment_spectra[max_index + 3:] = zero_for_log
else:
    experiment_spectra[max_index + 3:] = zero_for_log
    experiment_spectra[: max_index - 2] = zero_for_log

ampl_spectra = np.abs(experiment_spectra)
max_index = np.argmax(ampl_spectra)
ymax = ampl_spectra[max_index]


spectra_plot(ampl_spectra, max_index, ymax,
             'Spectra of the interferometric response 5 harmonics',
             '01 - Spectra of interferometric response 05.png', path_to_data)


filtered_signal_im = np.imag(np.fft.ifft(experiment_spectra))
filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))
signal_5_harmonics = 2 * filtered_signal_re

response_plot(2 * filtered_signal_re, 'Interferometric response only 5 harmonics',
              '02 - Interferometric response 05.png', path_to_data, v_min, v_max, date_time)

re_max = 2 * np.max(np.abs(filtered_signal_re))

rc('font', size=6, weight='bold')
fig = plt.figure(figsize=(9, 5))
fig.suptitle('Interferometric response only 5 harmonics', fontsize=8, fontweight='bold')
ax1 = fig.add_subplot(111)
plt.axvline(x=x_center, linewidth='0.5', color='r')  # alpha=0.5
plt.axhline(y=re_max, linewidth='1.5', color='r')  # alpha=0.5
plt.axhline(y=-re_max, linewidth='1.5', color='r')  # alpha=0.5
ax1.plot(2 * filtered_signal_re, linestyle='-', linewidth='1.00', label='Filtered')
ax1.plot(y_value[0, :], linestyle='-', linewidth='1.00', label='Measured')
ax1.legend(loc='upper right', fontsize=6)
ax1.grid(b=True, which='both', color='silver', linestyle='-')
ax1.set_ylim([v_min, v_max])
ax1.set_xlim([0, b-1])
ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
ax1.set_xlabel('UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', fontsize=6, fontweight='bold')
ax1.xaxis.set_major_locator(mtick.LinearLocator(7))
text = ax1.get_xticks().tolist()
for i in range(len(text)):
    k = int(text[i])
    text[i] = str(date_time[k][0:11] + '\n' + date_time[k][11:23])
ax1.set_xticklabels(text, fontsize=6, fontweight='bold')
fig.subplots_adjust(top=0.92)
pylab.savefig(path_to_data + '02 - Interferometric response 05a.png', bbox_inches='tight', dpi=160)
plt.close('all')


# *******************************************************************************
#         Signal without higher frequencies and filtered to 3 harmonics
# *******************************************************************************

if   max_index <= 1:
    experiment_spectra[max_index + 2:] = zero_for_log
else:
    experiment_spectra[max_index + 2:] = zero_for_log
    experiment_spectra[: max_index - 1] = zero_for_log

ampl_spectra = np.abs(experiment_spectra)
max_index = np.argmax(ampl_spectra)
ymax = ampl_spectra[max_index]


spectra_plot(ampl_spectra, max_index, ymax,
             'Spectra of the interferometric response 3 harmonics',
             '01 - Spectra of interferometric response 06.png', path_to_data)


filtered_signal_im = np.imag(np.fft.ifft(experiment_spectra))
filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))

response_plot(2 * filtered_signal_re, 'Interferometric response only 3 harmonics',
              '02 - Interferometric response 06.png', path_to_data, v_min, v_max, date_time)


# *******************************************************************************
#       Signal without higher frequencies and filtered to only 1 harmonic
# *******************************************************************************

experiment_spectra[max_index + 1:] = zero_for_log
experiment_spectra[0: max_index] = zero_for_log

ampl_spectra = np.abs(experiment_spectra)
max_index = np.argmax(ampl_spectra)
ymax = ampl_spectra[max_index]


spectra_plot(ampl_spectra, max_index, ymax,
             'Spectra of the interferometric response 1 harmonic',
             '01 - Spectra of interferometric response 07.png', path_to_data)


filtered_signal_im = np.imag(np.fft.ifft(experiment_spectra))
filtered_signal_re = np.real(np.fft.ifft(experiment_spectra))

response_plot(2 * filtered_signal_re, 'Interferometric response only 1 harmonic',
              '02 - Interferometric response 07.png', path_to_data, v_min, v_max, date_time)


# *******************************************************************************
#                     Signal without lower frequencies
# *******************************************************************************

spectra = np.fft.fft(y_value[0, :])
spectra[0: 25] = zero_for_log
spectra[-25:] = zero_for_log
ampl_spectra = np.abs(spectra)


rc('font', size=6, weight='bold')
fig = plt.figure(figsize=(12, 5))
fig.suptitle('Spectra of the higher frequencies only', fontsize=8, fontweight='bold')
ax1 = fig.add_subplot(121)
ax1.set_title('Spectra', fontsize=6)
ax1.plot(ampl_spectra, linestyle='-', linewidth='2.0', alpha=1.0, label='Measurements')
ax1.scatter(np.linspace(0, len(ampl_spectra)-1, num=len(ampl_spectra)), ampl_spectra, color='r')
# ax1.annotate(str(np.round(ymax,5)), xy=(max_index+15, ymax), fontsize = 6, ha='center') # xy=(xmax, 2 + 0.3)
ax1.set_xlim([0, int(len(ampl_spectra)/2)])
ax2 = fig.add_subplot(122)
ax2.set_title('Spectra', fontsize=6)
ax2.plot(10 * np.log10(ampl_spectra), linestyle='-', linewidth='2.0', alpha=1.0, label='Measurements')
ax2.scatter(np.linspace(0, len(ampl_spectra)-1, num=len(ampl_spectra)), 10 * np.log10(ampl_spectra), color='r')
# ax2.annotate(str(np.round(10 * np.log10(ymax),5)),  xy=(max_index+15, 10 * np.log10(ymax)), fontsize = 6, ha='center')
ax2.set_xlim([0, int(len(ampl_spectra)/2)])
# ax2.set_ylim([-100, -50])
pylab.savefig(path_to_data + '01 - Spectra of interferometric response 08.png', bbox_inches='tight', dpi=160)
plt.close('all')


signal_re = np.real(np.fft.ifft(spectra))


rc('font', size=6, weight='bold')
fig = plt.figure(figsize=(9, 5))
fig.suptitle('Interferometric response of high frequencies', fontsize=8, fontweight='bold')
ax1 = fig.add_subplot(111)
plt.axvline(x=x_center, linewidth='0.5', color='r')  # alpha=0.5
ax1.plot(2 * signal_re, linestyle='-', linewidth='1.00', label='Filtered')
# ax1.plot(y_value[0, :], linestyle = '-', linewidth = '1.00', label = 'Measured')
ax1.legend(loc='upper right', fontsize=6)
ax1.grid(b=True, which='both', color='silver', linestyle='-')
ax1.set_ylim([v_min, v_max])
ax1.set_xlim([0, b-1])
ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
ax1.set_xlabel('UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', fontsize=6, fontweight='bold')
ax1.xaxis.set_major_locator(mtick.LinearLocator(7))
text = ax1.get_xticks().tolist()
for i in range(len(text)):
    k = int(text[i])
    text[i] = str(date_time[k][0:11] + '\n' + date_time[k][11:23])
ax1.set_xticklabels(text, fontsize=6, fontweight='bold')
fig.subplots_adjust(top=0.92)
pylab.savefig(path_to_data + '02 - Interferometric response 08.png', bbox_inches='tight', dpi=160)
plt.close('all')

rc('font', size=6, weight='bold')
fig = plt.figure(figsize=(9, 5))
fig.suptitle('Interferometric response of high frequencies vs. initial signal', fontsize=8, fontweight='bold')
ax1 = fig.add_subplot(111)
plt.axvline(x=x_center, linewidth='0.5', color='r')  # alpha=0.5
ax1.plot(2 * signal_re, linestyle='-', linewidth='1.00', label='Filtered')
ax1.plot(y_value[0, :], linestyle='-', linewidth='1.00', label='Measured')
ax1.legend(loc='upper right', fontsize=6)
ax1.grid(b=True, which='both', color='silver', linestyle='-')
ax1.set_ylim([v_min, v_max])
ax1.set_xlim([0, b-1])
ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
ax1.set_xlabel('UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', fontsize=6, fontweight='bold')
ax1.xaxis.set_major_locator(mtick.LinearLocator(7))
text = ax1.get_xticks().tolist()
for i in range(len(text)):
    k = int(text[i])
    text[i] = str(date_time[k][0:11] + '\n' + date_time[k][11:23])
ax1.set_xticklabels(text, fontsize=6, fontweight='bold')
fig.subplots_adjust(top=0.92)
pylab.savefig(path_to_data + '02 - Interferometric response 09.png', bbox_inches='tight', dpi=160)
plt.close('all')


rc('font', size=6, weight='bold')
fig = plt.figure(figsize=(9, 5))
fig.suptitle('Interferometric response of high frequencies vs. 5 harmonics', fontsize=8, fontweight='bold')
ax1 = fig.add_subplot(111)
plt.axvline(x=x_center, linewidth='0.5', color='r')  # alpha=0.5
ax1.plot(2 * signal_re, linestyle='-', linewidth='1.00', label='Filtered high')
ax1.plot(signal_5_harmonics, linestyle='-', linewidth='1.00', label='Filtered 5 harmonics')
ax1.legend(loc='upper right', fontsize=6)
ax1.grid(b=True, which='both', color='silver', linestyle='-')
ax1.set_ylim([v_min, v_max])
ax1.set_xlim([0, b-1])
ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
ax1.set_xlabel('UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', fontsize=6, fontweight='bold')
ax1.xaxis.set_major_locator(mtick.LinearLocator(7))
text = ax1.get_xticks().tolist()
for i in range(len(text)):
    k = int(text[i])
    text[i] = str(date_time[k][0:11] + '\n' + date_time[k][11:23])
ax1.set_xticklabels(text, fontsize=6, fontweight='bold')
fig.subplots_adjust(top=0.92)
pylab.savefig(path_to_data + '02 - Interferometric response 10.png', bbox_inches='tight', dpi=160)
plt.close('all')


end_time = time.time()
print('\n\n\n  The program execution lasted for ', round((end_time - start_time), 2), 'seconds (',
                                                   round((end_time - start_time)/60, 2), 'min. ) \n')
print('\n           *** Program ' + software_name + ' has finished! *** \n\n\n')
