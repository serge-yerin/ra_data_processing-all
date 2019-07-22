# Python3
Software_version = '2019.03.27' # !!!!!!!   NOT FINISHED   !!!!!!!
# Program intended to read and show individual pulses of pulsars from DAT files

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************
# Path to data files
common_path = 'DATA/'

# Directory of DAT file to be analyzed:
filename = common_path + 'E300117_180000.jds_Data_chA.dat'


StartStopSwitch = 1            # Read the whole file (0) or specified time limits (1)
SpecFreqRange = 0              # Specify particular frequency range (1) or whole range (0)
VminMan = -110                 # Manual lower limit of immediate spectrum figure color range
VmaxMan = -60                  # Manual upper limit of immediate spectrum figure color range
VminNormMan = 0                # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
VmaxNormMan = 15               # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
RFImeanConst = 6               # Constant of RFI mitigation (usually = 8)
customDPI = 300                # Resolution of images of dynamic spectra
colormap = 'Greys'             # Colormap of images of dynamic spectra ('jet' or 'Greys')
ColorBarSwitch = 1             # Add colorbar to dynamic spectrum picture? (1 = yes, 0 = no)
ChannelSaveTXT = 0             # Save intensities at specified frequencies to TXT file
ChannelSavePNG = 0             # Save intensities at specified frequencies to PNG file
ListOrAllFreq = 0              # Take all frequencies of a list to save TXT and PNG? 1-All, 0-List
AmplitudeReIm = 3 * 10**(-12) # Colur range of Re and Im dynamic spectra
                               # 10 * 10**(-12) is typical value enough for CasA for interferometer of 2 GURT subarrays

# Begin and end frequency of dynamic spectrum (MHz)
freqStart = 0.0
freqStop =  80.0

# Begin and end time of dynamic spectrum ('yyyy-mm-dd hh:mm:ss')
dateTimeStart = '2017-04-18 09:34:00'
dateTimeStop =  '2017-04-18 09:35:20'

# Begin and end frequency of TXT files to save (MHz)
freqStartTXT = 0.0
freqStopTXT = 80.0

DM = 5.750   #PSRname='B0809+74'

#*************************************************************


#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************
import os
import struct
import sys
import math
import numpy as np
import pylab
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta
from matplotlib import rc

from f_spectra_normalization import Normalization_lin
from f_plot_formats import plot1D, plot2Da
from f_pulsar_DM_shift_calculation import DM_shift_calc
from f_file_header_JDS import FileHeaderReaderDSP
from f_file_header_ADR import FileHeaderReaderADR
from f_ra_data_clean import array_clean_by_STD_value, clean_lines_of_pixels
from f_data_manipulations import average_some_lines_of_array, DM_compensation_with_indices_changes


#*************************************************************
#                       MAIN PROGRAM                         *
#*************************************************************
for i in range(8): print (' ')
print ('   ****************************************************')
print ('   *    Pulsar processing pipeline v.', Software_version,'     *      (c) YeS 2019')
print ('   ****************************************************')
for i in range(3): print (' ')


startTime = time.time()
previousTime = startTime
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)
print (' ')

# Name of Timeline file to be analyzed:
#timeLineFileName = common_path + filename[-31:-13] +'_Timeline.txt'

# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = "PULSAR_single_pulses"
if not os.path.exists(newpath):
    os.makedirs(newpath)


for j in range(1):  # Main loop by types of data to analyze


    # *** Opening DAT datafile ***

    file = open(filename, 'rb')

    # reading FHEADER
    df_filesize = (os.stat(filename).st_size)            # Size of file
    df_filename = file.read(32).decode('utf-8').rstrip('\x00')           # Initial data file name
    file.close()

    print(df_filename)

    receiver_type = df_filename[-4:]


    # Reading file header to obtain main parameters of the file
    if receiver_type == '.adr':
        [TimeRes, fmin, fmax, df, frequencyList0, FFTsize] = FileHeaderReaderADR(filename, 0)
    if receiver_type == '.jds':
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr,
        TimeRes, fmin, fmax, df, frequencyList0, FFTsize, dataBlockSize] = FileHeaderReaderDSP(filename, 0, 1)


    #************************************************************************************
    #                            R E A D I N G   D A T A                                *
    #************************************************************************************

    num_frequencies = len(frequencyList0)
    shift_vector = DM_shift_calc(num_frequencies, fmin, fmax, df / pow(10,6), TimeRes, DM, receiver_type)

    #plot1D(shift_vector, newpath+'/01 - Shift parameter.png', 'Shift parameter', 'Shift parameter', 'Shift parameter', 'Frequency channel number', customDPI)

    max_shift = np.abs(shift_vector[0])
    print (' Maximal shift is:              ', max_shift)


    num_spectra = 2 * max_shift


    dat_file = open(filename, 'rb')
    dat_file.seek(1024)               # Jumping to 1024 byte from file beginning


    numOfBlocks = 1
    for block in range (numOfBlocks):

        data = np.fromfile(dat_file, dtype=np.float64, count = num_frequencies * num_spectra)
        data = np.reshape(data, [num_frequencies, num_spectra], order='F')

        # To mask the last channels of DSP where exact time is stored
        '''
        if receiver_type == '.jds':
            mean_data = np.mean(data)
            data[num_frequencies-4 : num_frequencies-1, :] = mean_data
        '''
        num_frequencies = num_frequencies -4
        data = data[ : num_frequencies, :]


        nowTime = time.time()
        print ('\n  * Preparation of data took:            ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime

        #plot2Da(data_log, newpath+'/02 - Full log initial data.png', frequencyList0, np.min(data_log), np.max(data_log), colormap, 'Full log initial data', customDPI)

        # Normalization of data
        Normalization_lin(data, num_frequencies, num_spectra)


        # Log data to examine it in a plot
        data_log = np.empty((num_frequencies, num_spectra), float)

        with np.errstate(invalid='ignore'):
            data_log[:,:] = 10 * np.log10(data[:,:])
        data_log[np.isnan(data_log)] = 0

        plot2Da(data_log, newpath+'/02 - Full log initial data.png', frequencyList0, np.min(data_log), np.max(data_log), colormap, 'Full log initial data', customDPI)
        del data_log



        # Cleaning vertical and horizontal lines of RFI
        data, mask, cleaned_pixels_num = clean_lines_of_pixels(data, 3, 1, 3)

        plt.figure(1, figsize=(10.0, 6.0))
        plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
        ImA = plt.imshow(mask, aspect='auto', vmin=0, vmax=1, cmap='Greys')
        plt.title('Full log initial data', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
        plt.ylabel('One dimension', fontsize = 10, fontweight='bold')
        plt.xlabel('Second dimensions', fontsize = 10, fontweight='bold')
        plt.colorbar()
        plt.yticks(fontsize = 8, fontweight = 'bold')
        plt.xticks(fontsize = 8, fontweight = 'bold')
        pylab.savefig(newpath+'/00_10 - Result mask after lines cleaning.png', bbox_inches='tight', dpi = 300)
        plt.close('all')

        data, mask, cleaned_pixels_num = array_clean_by_STD_value(data, 2.8)


        plt.figure(1, figsize=(10.0, 6.0))
        plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
        ImA = plt.imshow(mask, aspect='auto', vmin=0, vmax=1, cmap='Greys')
        plt.title('Full log initial data', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
        plt.ylabel('One dimension', fontsize = 10, fontweight='bold')
        plt.xlabel('Second dimensions', fontsize = 10, fontweight='bold')
        plt.colorbar()
        plt.yticks(fontsize = 8, fontweight = 'bold')
        plt.xticks(fontsize = 8, fontweight = 'bold')
        pylab.savefig(newpath+'/00_11 - Mask after fine STD cleaning.png', bbox_inches='tight', dpi = 300)
        plt.close('all')

        nowTime = time.time()
        print ('\n  * Normalization and cleaning took:     ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime


        data_log = np.empty((num_frequencies, num_spectra), float)

        # Average and log data
        with np.errstate(invalid='ignore'):
            data_log[:,:] = 10 * np.log10(data[:,:])
        data_log[np.isnan(data_log)] = 0


    del data
    dat_file.close()



    plot2Da(data_log, newpath+'/03 - Full log cleaned data.png', frequencyList0, np.min(data_log), np.max(data_log), colormap, 'Full log initial data', customDPI)


    '''
    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    ImA = plt.imshow(np.flipud(data_log), aspect='auto', vmin=np.min(data_log), vmax=np.max(data_log), cmap=colormap, extent=[0,num_spectra,frequencyList0[0],frequencyList0[len(frequencyList0)-1]])
    plt.title('Full log initial data', fontsize = 10, fontweight = 'bold', style = 'italic', y = 1.025)
    plt.ylabel('Frequency, MHz', fontsize = 10, fontweight='bold')
    plt.xlabel('Time, spectra counts', fontsize = 10, fontweight='bold')
    plt.colorbar()
    plt.yticks(fontsize = 8, fontweight = 'bold')
    plt.xticks(fontsize = 8, fontweight = 'bold')
    pylab.savefig(newpath+'/03 - Full log cleaned data.png', bbox_inches='tight', dpi = customDPI)
    plt.close('all')
    '''
    plot1D(data_log[:,1], newpath+'/04a - Cleaned data single specter.png', 'Label', 'Initial data specter', 'Frequency, MHz', 'Amplitude, AU', customDPI)
    plot1D(data_log[1,:], newpath+'/04b - Cleaned data single channel.png', 'Label', 'Initial data channel', 'Time, spectra counts', 'Amplitude, AU', customDPI)



    temp_array = np.zeros((num_frequencies, 4 * max_shift))

    temp_array[:, 4 * max_shift - num_spectra : 4 * max_shift] = data_log[:,:]
    del data_log

    '''
    for i in range (num_frequencies):
        temp_array[i] = np.roll(temp_array[i], shift_vector[i])
    '''
    temp_array = DM_compensation_with_indices_changes(temp_array, shift_vector[0: num_frequencies])



    plot2Da(temp_array, newpath+'/05 - DM compensated data.png', frequencyList0, np.min(temp_array), np.max(temp_array), colormap, 'DM compensated data', customDPI)

    temp_array[:] = np.roll(temp_array[:], - num_spectra)

    plot2Da(temp_array, newpath+'/06 - DM compensated data.png', frequencyList0, np.min(temp_array), np.max(temp_array), colormap, 'Shifted compensated full data', customDPI)


    array_compensated_DM = np.zeros((num_frequencies, max_shift), float)
    array_compensated_DM[:,:] = temp_array[:, 0 : max_shift]

    del temp_array

    plot2Da(array_compensated_DM, newpath+'/07 - Only full ready data.png', frequencyList0, np.min(array_compensated_DM), np.max(array_compensated_DM), colormap, 'Only full ready data', customDPI)

    spectrum = array_compensated_DM.mean(axis=1)[:]
    profile = array_compensated_DM.mean(axis=0)[:]
    profile = profile - np.mean(profile)

    plot1D(spectrum, newpath+'/08 - Averaged spectrum.png', 'Label', 'Averaged spectrum', 'x_label', 'y_label', customDPI)
    #plot1D(profile,  newpath+'/09 - Temporal profile of pulses.png', 'Label', 'Temporal profile of pulses', 'x_label', 'y_label', customDPI)


    averaged_array  = average_some_lines_of_array(array_compensated_DM, int(num_frequencies/192))

    no_of_lines, no_of_columns = averaged_array.shape
    print(' * Array shape:                               ', no_of_lines,' * ', no_of_columns)


    fig = plt.figure(figsize = (9, 6))
    ax1 = fig.add_subplot(211)
    ax1.plot(profile, color =u'#1f77b4', linestyle = '-', alpha=1.0, linewidth = '1.00', label = 'Pulses time profile')
    ax1.legend(loc = 'upper right', fontsize = 6)
    ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
    ax1.axis([0, len(profile), -0.1, 0.5])
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title('Average profile of pulses in time', fontsize = 6)
    ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax2 = fig.add_subplot(212)
    ax2.imshow(np.flipud(averaged_array), aspect='auto', cmap='Greys') # vmin=-4, vmax=4,
    ax2.set_xlabel('Time, counts', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Frequency, MHz', fontsize=6, fontweight='bold')
    fig.subplots_adjust(hspace=0.05, top=0.94)
    fig.suptitle('SupTitle', fontsize = 8, fontweight='bold')
    fig.text(0.73, 0.06, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.06, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
    pylab.savefig(newpath+'/10 - Combined picture.png', bbox_inches = 'tight', dpi = 300)
    plt.close('all')



endTime = time.time()    # Time of calculations


for i in range (0,2) : print (' ')
#print ('   The program execution lasted for ', round((endTime - startTime),3), 'seconds')
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')

for i in range (0,2) : print (' ')
print ('                 *** Program PULSAR_single_pulse_reader has finished! ***')
for i in range (0,3) : print (' ')
