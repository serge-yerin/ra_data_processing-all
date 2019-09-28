# Python3
Software_name = 'CasA secular decrease test for specter filtering'
Software_version = '2019.09.28'
# Script intended to read TXT files with results of Cas A - Syg A fluxes ration and calculate statistics

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
path_to_data =  'DATA/TEST/'
file_name = 'E260719_230322_CIm.jds variation at 28.005 MHz.txt'
Vmin = -10 * 10**-9
Vmax =  10 * 10**-9
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

#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (9, 5))
ax1 = fig.add_subplot(111)
plt.axvline(x = x_center, linewidth = '0.5' , color = 'r') #, alpha=0.5
ax1.plot(y_value[0, :], linestyle = '-', linewidth = '1.00', label = 'Measured')
ax1.legend(loc = 'upper right', fontsize = 6)
ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
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
pylab.savefig(path_to_data + '02 - Interferometric responce 01.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''

spectra = np.fft.fft(y_value[0, :])
ampl_spectra = np.abs(spectra)
ampl_spectra[0] = np.nan


ymax = np.max(ampl_spectra[1:])

#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (12, 5))
fig.suptitle('Spectra of the interferometric responce', fontsize = 8, fontweight='bold')
ax1 = fig.add_subplot(121)
ax1.set_title('Spectra', fontsize = 6)
ax1.plot(ampl_spectra, linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
ax1.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center') # xy=(xmax, 2 + 0.3)
ax1.set_xlim([0, int(len(ampl_spectra)/10)])
ax2 = fig.add_subplot(122)
ax2.set_title('Spectra', fontsize = 6)
ax2.plot(10 * np.log10(ampl_spectra), linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
ymax = np.max(10 * np.log10(ampl_spectra[1:]))
ax2.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center')
ax2.set_xlim([0, int(len(ampl_spectra)/10)])
ax2.set_ylim([-100, -50])
pylab.savefig(path_to_data + '01 - Spectra of interferometric responce 01.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''



#spectra[50:] = 0.000000001
spectra[40:] = 0.000000001

ampl_spectra = np.abs(spectra)


#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (12, 5))
fig.suptitle('Spectra of the interferometric responce', fontsize = 8, fontweight='bold')
ax1 = fig.add_subplot(121)
ax1.set_title('Spectra', fontsize = 6)
ax1.plot(ampl_spectra, linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
#ax1.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center') # xy=(xmax, 2 + 0.3)
ax1.set_xlim([0, int(len(ampl_spectra)/10)])
ax2 = fig.add_subplot(122)
ax2.set_title('Spectra', fontsize = 6)
ax2.plot(10 * np.log10(ampl_spectra), linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
#ymax = np.max(10 * np.log10(ampl_spectra[1:]))
#ax2.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center')
ax2.set_xlim([0, int(len(ampl_spectra)/10)])
#ax2.set_ylim([-100, -50])
pylab.savefig(path_to_data + '01 - Spectra of interferometric responce 02.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''


filtered_signal_im = np.imag(np.fft.ifft(spectra))
filtered_signal_re = np.real(np.fft.ifft(spectra))



#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (9, 5))
ax1 = fig.add_subplot(111)
plt.axvline(x = x_center, linewidth = '0.5' , color = 'r') #, alpha=0.5
ax1.plot(2 * filtered_signal_re, linestyle = '-', linewidth = '1.00', label = 'Measured')
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
pylab.savefig(path_to_data + '02 - Interferometric responce 02.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''

# *************************************************************
spectra[40:] = 0.000000001
#spectra[1:24] = 0.000000001
spectra[1:15] = 0.000000001
ampl_spectra = np.abs(spectra)


#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (12, 5))
fig.suptitle('Spectra of the interferometric responce', fontsize = 8, fontweight='bold')
ax1 = fig.add_subplot(121)
ax1.set_title('Spectra', fontsize = 6)
ax1.plot(ampl_spectra, linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
#ax1.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center') # xy=(xmax, 2 + 0.3)
ax1.set_xlim([0, int(len(ampl_spectra)/10)])
ax2 = fig.add_subplot(122)
ax2.set_title('Spectra', fontsize = 6)
ax2.plot(10 * np.log10(ampl_spectra), linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
#ymax = np.max(10 * np.log10(ampl_spectra[1:]))
#ax2.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center')
ax2.set_xlim([0, int(len(ampl_spectra)/10)])
#ax2.set_ylim([-100, -50])
pylab.savefig(path_to_data + '01 - Spectra of interferometric responce 03.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''


filtered_signal_im = np.imag(np.fft.ifft(spectra))
filtered_signal_re = np.real(np.fft.ifft(spectra))



#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (9, 5))
ax1 = fig.add_subplot(111)
plt.axvline(x = x_center, linewidth = '0.5' , color = 'r') #, alpha=0.5
ax1.plot(2 * filtered_signal_re, linestyle = '-', linewidth = '1.00', label = 'Measured')
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
pylab.savefig(path_to_data + '02 - Interferometric responce 03.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''


# *************************************************************
#spectra[37:] = 0.000000001
#spectra[1:30] = 0.000000001
spectra[26:] = 0.000000001
spectra[1:19] = 0.000000001
ampl_spectra = np.abs(spectra)


#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (12, 5))
fig.suptitle('Spectra of the interferometric responce', fontsize = 8, fontweight='bold')
ax1 = fig.add_subplot(121)
ax1.set_title('Spectra', fontsize = 6)
ax1.plot(ampl_spectra, linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
#ax1.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center') # xy=(xmax, 2 + 0.3)
ax1.set_xlim([0, int(len(ampl_spectra)/10)])
ax2 = fig.add_subplot(122)
ax2.set_title('Spectra', fontsize = 6)
ax2.plot(10 * np.log10(ampl_spectra), linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
#ymax = np.max(10 * np.log10(ampl_spectra[1:]))
#ax2.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center')
ax2.set_xlim([0, int(len(ampl_spectra)/10)])
#ax2.set_ylim([-100, -50])
pylab.savefig(path_to_data + '01 - Spectra of interferometric responce 04.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''


filtered_signal_im = np.imag(np.fft.ifft(spectra))
filtered_signal_re = np.real(np.fft.ifft(spectra))



#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (9, 5))
ax1 = fig.add_subplot(111)
plt.axvline(x = x_center, linewidth = '0.5' , color = 'r') #, alpha=0.5
ax1.plot(2 * filtered_signal_re, linestyle = '-', linewidth = '1.00', label = 'Measured')
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
pylab.savefig(path_to_data + '02 - Interferometric responce 04.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''



#


filtered_signal_im = np.imag(np.fft.ifft(spectra))
filtered_signal_re = np.real(np.fft.ifft(spectra))
# *************************************************************
#spectra[35:] = 0.000000001
#spectra[1:31] = 0.000000001
spectra[24:] = 0.000000001
spectra[1:20] = 0.000000001
ampl_spectra = np.abs(spectra)


#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (12, 5))
fig.suptitle('Spectra of the interferometric responce', fontsize = 8, fontweight='bold')
ax1 = fig.add_subplot(121)
ax1.set_title('Spectra', fontsize = 6)
ax1.plot(ampl_spectra, linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
#ax1.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center') # xy=(xmax, 2 + 0.3)
ax1.set_xlim([0, int(len(ampl_spectra)/10)])
ax2 = fig.add_subplot(122)
ax2.set_title('Spectra', fontsize = 6)
ax2.plot(10 * np.log10(ampl_spectra), linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
#ymax = np.max(10 * np.log10(ampl_spectra[1:]))
#ax2.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center')
ax2.set_xlim([0, int(len(ampl_spectra)/10)])
#ax2.set_ylim([-100, -50])
pylab.savefig(path_to_data + '01 - Spectra of interferometric responce 04.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''


filtered_signal_im = np.imag(np.fft.ifft(spectra))
filtered_signal_re = np.real(np.fft.ifft(spectra))



#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (9, 5))
ax1 = fig.add_subplot(111)
plt.axvline(x = x_center, linewidth = '0.5' , color = 'r') #, alpha=0.5
ax1.plot(2 * filtered_signal_re, linestyle = '-', linewidth = '1.00', label = 'Measured')
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
pylab.savefig(path_to_data + '02 - Interferometric responce 04.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''







# *************************************************************
#spectra[33:] = 0.000000001
#spectra[1:32] = 0.000000001
spectra[23:] = 0.000000001
spectra[1:21] = 0.000000001
ampl_spectra = np.abs(spectra)


#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (12, 5))
fig.suptitle('Spectra of the interferometric responce', fontsize = 8, fontweight='bold')
ax1 = fig.add_subplot(121)
ax1.set_title('Spectra', fontsize = 6)
ax1.plot(ampl_spectra, linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
#ax1.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center') # xy=(xmax, 2 + 0.3)
ax1.set_xlim([0, int(len(ampl_spectra)/10)])
ax2 = fig.add_subplot(122)
ax2.set_title('Spectra', fontsize = 6)
ax2.plot(10 * np.log10(ampl_spectra), linestyle = '-', linewidth = '2.0', alpha = 1.0, label = 'Measurements')
#ymax = np.max(10 * np.log10(ampl_spectra[1:]))
#ax2.annotate(str(ymax),  xy=(50, ymax), fontsize = 6, ha='center')
ax2.set_xlim([0, int(len(ampl_spectra)/10)])
#ax2.set_ylim([-100, -50])
pylab.savefig(path_to_data + '01 - Spectra of interferometric responce 05.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''


filtered_signal_im = np.imag(np.fft.ifft(spectra))
filtered_signal_re = np.real(np.fft.ifft(spectra))



#'''
rc('font', size = 6, weight='bold')
fig = plt.figure(figsize = (9, 5))
ax1 = fig.add_subplot(111)
plt.axvline(x = x_center, linewidth = '0.5' , color = 'r') #, alpha=0.5
ax1.plot(2 * filtered_signal_re, linestyle = '-', linewidth = '1.00', label = 'Measured')
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
pylab.savefig(path_to_data + '02 - Interferometric responce 05.png', bbox_inches = 'tight', dpi = 160)
plt.close('all')
#'''










endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program ' + Software_name + ' has finished! *** \n\n\n')
