# Python3
Software_version = '2019.12.14'
# Program intended to read and show individual pulses of pulsars from DAT files

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************
# Path to data files
common_path = ''

# Directory of DAT file to be analyzed:
#filename = 'E300117_180000.jds_Data_chA.dat'
filename = 'E220213_201455.jds_Data_chA.dat'

pulsar_name = 'B0950+08'

average_const = 512            # Number of frequency channels to average in result picture
prifile_pic_min = -0.1         # Minimum limit of profile picture
prifile_pic_max = 0.5          # Maximum limit of profile picture

cleaning = 0                   # Apply cleaning to data (1) or skip it (0)
# Parameters of vertical and horizontal lines cleaning
no_of_iterations = 2           # Number of lines cleaning iterations (usually 2-3)
std_lines_clean = 1            # Limit in StD of pixels in line to clean
pic_in_line = 10               # Number of pixels in line
# Parameter of pixels cleaning based on StD value estimation
std_pixels_clean = 2.8

SpecFreqRange = 1              # Specify particular frequency range (1) or whole range (0)
# Begin and end frequency of dynamic spectrum (MHz)
freqStart = 20.0
freqStop = 30.0

customDPI = 300                # Resolution of images of dynamic spectra
colormap = 'Greys'             # Colormap of images of dynamic spectra ('jet' or 'Greys')


#*************************************************************


#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************
import os
import sys
import math
import time
import pylab
import struct
import numpy as np
import matplotlib.pyplot as plt
from os import path
from matplotlib import rc
from datetime import datetime, timedelta

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_ra_data_processing.spectra_normalization import Normalization_lin
from package_ra_data_processing.average_some_lines_of_array import average_some_lines_of_array
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.specify_frequency_range import specify_frequency_range
from package_pulsar_processing.pulsar_DM_full_shift_calculation import DM_full_shift_calc
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes
from package_cleaning.clean_lines_of_pixels import clean_lines_of_pixels
from package_cleaning.array_clean_by_STD_value import array_clean_by_STD_value
from package_plot_formats.plot_formats import plot1D, plot2Da
from package_astronomy.catalogue_pulsar import catalogue_pulsar


def plot_ready_data(array_compensated_DM, frequency_list, num_frequencies, average_const, filename, colormap, customDPI, currentDate, currentTime, Software_version):
    #plot2Da(array_compensated_DM, newpath+'/07' + ' fig. ' +str(block+1)+' - Only full ready data.png', frequency_list, np.min(array_compensated_DM), np.max(array_compensated_DM), colormap, 'Only full ready data', customDPI)

    profile = array_compensated_DM.mean(axis=0)[:]
    profile = profile - np.mean(profile)

    # Averaging of the array with pulses for picture
    averaged_array  = average_some_lines_of_array(array_compensated_DM, int(num_frequencies/average_const))
    #del array_compensated_DM

    # Making result picture
    fig = plt.figure(figsize = (9, 6))
    ax1 = fig.add_subplot(211)
    ax1.plot(profile, color =u'#1f77b4', linestyle = '-', alpha=1.0, linewidth = '1.00', label = 'Pulses time profile')
    ax1.legend(loc = 'upper right', fontsize = 6)
    ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
    ax1.axis([0, len(profile), prifile_pic_min, prifile_pic_max])
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title('Data from file: '+ filename + ', description: ' + df_description, fontsize = 6)
    ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax2 = fig.add_subplot(212)
    ax2.imshow(np.flipud(averaged_array), aspect='auto', cmap=colormap, extent=[0,len(profile),frequency_list[0],frequency_list[num_frequencies-1]])
    ax2.set_xlabel('Time, counts', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Frequency, MHz', fontsize=6, fontweight='bold')
    fig.subplots_adjust(hspace=0.05, top=0.92)
    fig.suptitle('Single pulses of pulsar, fig. ' + str(block+1), fontsize = 8, fontweight='bold')
    fig.text(0.77, 0.06, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.06, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
    pylab.savefig(newpath + '/'+ filename + ' fig. ' +str(block+1)+ ' - Combined picture.png', bbox_inches = 'tight', dpi = customDPI)
    plt.close('all')




#*************************************************************
#                       MAIN PROGRAM                         *
#*************************************************************
print(' \n\n\n\n\n\n\n\n')
print('   *****************************************************************')
print('   *    Pulsar single pulses processing pipeline v.', Software_version,'    *      (c) YeS 2019')
print('   ***************************************************************** \n\n\n')

startTime = time.time()
previousTime = startTime
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, ' \n')

rc('font', size = 6, weight='bold')
data_filename = common_path + filename

# Name of Timeline file to be analyzed:
#timeLineFileName = common_path + data_filename[-31:-13] +'_Timeline.txt'

# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = "PULSAR_single_pulses"
if not os.path.exists(newpath):
    os.makedirs(newpath)


# *** Opening DAT datafile ***
file = open(data_filename, 'rb')

# reading FHEADER
df_filesize = (os.stat(data_filename).st_size)                          # Size of file
df_filename = file.read(32).decode('utf-8').rstrip('\x00')              # Initial data file name
file.close()

receiver_type = df_filename[-4:]

# Reading file header to obtain main parameters of the file
if receiver_type == '.adr':
    [TimeRes, fmin, fmax, df, frequency_list, FFTsize] = FileHeaderReaderADR(data_filename, 0, 1)

if receiver_type == '.jds':
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
    CLCfrq, df_creation_timeUTC, sp_in_file, ReceiverMode, Mode, Navr,
    TimeRes, fmin, fmax, df, frequency_list, FFTsize, dataBlockSize] = FileHeaderReaderJDS(data_filename, 0, 1)

sp_in_file = int(((df_filesize - 1024)/(len(frequency_list) * 8))) # the second dimension of the array: file size - 1024 bytes

pulsar_ra, pulsar_dec, DM = catalogue_pulsar(pulsar_name)
#************************************************************************************
#                            R E A D I N G   D A T A                                *
#************************************************************************************
#num_frequencies = len(frequency_list)

# if SpecFreqRange == 1 and (frequency_list[0]<=freqStart<=frequency_list[-1]) and (frequency_list[0]<=freqStop<=frequency_list[-1]) and (freqStart<freqStop):
if SpecFreqRange == 1:
    A = []
    B = []
    for i in range (len(frequency_list)):
        A.append(abs(frequency_list[i] - freqStart))
        B.append(abs(frequency_list[i] - freqStop))
    ifmin = A.index(min(A))
    ifmax = B.index(min(B))
    shift_vector = DM_full_shift_calc(ifmax - ifmin, frequency_list[ifmin], frequency_list[ifmax], df / pow(10,6), TimeRes, DM, receiver_type)
    print (' Number of frequency channels:  ', ifmax - ifmin)
else:
    shift_vector = DM_full_shift_calc(len(frequency_list), fmin, fmax, df / pow(10, 6), TimeRes, DM, receiver_type)
    print (' Number of frequency channels:  ', len(frequency_list)-4)

max_shift = np.abs(shift_vector[0])

if SpecFreqRange == 1:
    buffer_array = np.zeros((ifmax - ifmin, 2 * max_shift))
else:
    buffer_array = np.zeros((len(frequency_list) - 4, 2 * max_shift))

#plot1D(shift_vector, newpath+'/01 - Shift parameter.png', 'Shift parameter', 'Shift parameter', 'Shift parameter', 'Frequency channel number', customDPI)

num_of_blocks = int(sp_in_file / (1 * max_shift))

print (' Number of spectra in file:     ', sp_in_file, ' ')
print (' Maximal shift is:              ', max_shift, ' pixels ')
print (' Number of blocks in file:      ', num_of_blocks, ' \n')


if receiver_type == '.jds':
    num_frequencies_initial = len(frequency_list)-4

frequency_list_initial = np.empty_like(frequency_list)
frequency_list_initial[:] = frequency_list[:]

dat_file = open(data_filename, 'rb')
dat_file.seek(1024)                     # Jumping to 1024 byte from file beginning


for block in range (num_of_blocks):   # main loop by number of blocks in file

    print ('\n * Data block # ', block + 1, ' of ', num_of_blocks,'\n ******************************************************************')

    # Data block reading
    if receiver_type == '.jds':
        data = np.fromfile(dat_file, dtype=np.float64, count = (num_frequencies_initial+4) * 1 * max_shift)   # 2
        data = np.reshape(data, [(num_frequencies_initial+4), 1 * max_shift], order='F')  # 2
        data = data[ : num_frequencies_initial, :] # To delete the last channels of DSP spectra data where exact time is stored


    # Cutting the array in predefined frequency range
    if SpecFreqRange == 1:
        data, frequency_list, fi_start, fi_stop = specify_frequency_range(data, frequency_list_initial, freqStart, freqStop)
        num_frequencies = len(frequency_list)


    # Normalization of data
    Normalization_lin(data, num_frequencies, 1 * max_shift)  # 2

    nowTime = time.time()
    print ('\n  *** Preparation of data took:              ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime


    if cleaning > 0:

        # Cleaning vertical and horizontal lines of RFI
        data, mask, cleaned_pixels_num = clean_lines_of_pixels(data, no_of_iterations, std_lines_clean, pic_in_line)

        plt.figure(1, figsize=(10.0, 6.0))
        plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
        ImA = plt.imshow(mask, aspect='auto', vmin=0, vmax=1, cmap='Greys')
        plt.title('Full log initial data', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
        plt.ylabel('One dimension', fontsize = 10, fontweight='bold')
        plt.xlabel('Second dimensions', fontsize = 10, fontweight='bold')
        plt.colorbar()
        plt.yticks(fontsize = 8, fontweight = 'bold')
        plt.xticks(fontsize = 8, fontweight = 'bold')
        pylab.savefig(newpath+'/00_10'+ ' fig. ' +str(block+1)+' - Result mask after lines cleaning.png', bbox_inches='tight', dpi = 300)
        plt.close('all')

        # Cleaning remaining 1 pixel splashes of RFI
        data, mask, cleaned_pixels_num = array_clean_by_STD_value(data, std_pixels_clean)

        plt.figure(1, figsize=(10.0, 6.0))
        plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
        ImA = plt.imshow(mask, aspect='auto', vmin=0, vmax=1, cmap='Greys')
        plt.title('Full log initial data', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
        plt.ylabel('One dimension', fontsize = 10, fontweight='bold')
        plt.xlabel('Second dimensions', fontsize = 10, fontweight='bold')
        plt.colorbar()
        plt.yticks(fontsize = 8, fontweight = 'bold')
        plt.xticks(fontsize = 8, fontweight = 'bold')
        pylab.savefig(newpath+'/00_11'+ ' fig. ' +str(block+1)+' - Mask after fine STD cleaning.png', bbox_inches='tight', dpi = 300)
        plt.close('all')

        nowTime = time.time()
        print ('\n  *** Normalization and cleaning took:       ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime


    # Logging the data
    with np.errstate(invalid='ignore'):
        data[:,:] = 10 * np.log10(data[:,:])
    data[np.isnan(data)] = 0

    # Normalizing log data
    data = data - np.mean(data)


    nowTime = time.time() #                                '
    print ('\n  *** Time before dispersion compensation:   ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime


    # Dispersion compensation
    data_space = np.zeros((num_frequencies, 2 * max_shift))
    data_space[:, max_shift : ] = data[:,:]
    temp_array = pulsar_DM_compensation_with_indices_changes(data_space, shift_vector)
    del data, data_space


    nowTime = time.time()
    print ('\n  *** Dispersion compensation took:          ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime

    #plot2Da(temp_array, newpath+'/05 '+ ' fig. ' +str(block+1)+' - DM compensated data.png', frequency_list, np.min(temp_array), np.max(temp_array), colormap, 'DM compensated data', customDPI)

    # Adding the next data block
    buffer_array += temp_array

    # Making and filling the array with fully ready data for plotting and saving to a file
    array_compensated_DM = buffer_array[:, 0 : max_shift]
    plot_ready_data(array_compensated_DM, frequency_list, num_frequencies, average_const, filename, colormap, customDPI, currentDate, currentTime, Software_version)

    # Rolling temp_array to put current data first
    buffer_array = np.roll(buffer_array, - max_shift)
    buffer_array[:, max_shift : ] = 0


dat_file.close()
endTime = time.time()    # Time of calculations


print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n\n                 *** Program PULSAR_single_pulse_reader has finished! *** \n\n\n')
