# Python3
Software_version = '2019.07.23' # !!!!!!!   NOT FINISHED   !!!!!!!
# Program intended to read and show individual pulses of pulsars from DAT files

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************
# Path to data files
common_path = 'DATA/'

# Directory of DAT file to be analyzed:
filename = 'E300117_180000.jds_Data_chA.dat'

Cleaning = 0                   # Apply cleaning to data (1) or skip it (0)
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
print (' \n\n\n\n\n\n\n\n')
print ('   *****************************************************************')
print ('   *    Pulsar single pulses processing pipeline v.', Software_version,'    *      (c) YeS 2019')
print ('   ***************************************************************** \n\n\n')

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


for j in range(1):  # Main loop by           of data to analyze

    # *** Opening DAT datafile ***

    file = open(data_filename, 'rb')

    # reading FHEADER
    df_filesize = (os.stat(data_filename).st_size)                          # Size of file
    df_filename = file.read(32).decode('utf-8').rstrip('\x00')              # Initial data file name
    file.close()

    receiver_type = df_filename[-4:]

    # Reading file header to obtain main parameters of the file
    if receiver_type == '.adr':
        [TimeRes, fmin, fmax, df, frequency_list, FFTsize] = FileHeaderReaderADR(data_filename, 0)
    if receiver_type == '.jds':
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr,
        TimeRes, fmin, fmax, df, frequency_list, FFTsize, dataBlockSize] = FileHeaderReaderDSP(data_filename, 0, 1)


    #************************************************************************************
    #                            R E A D I N G   D A T A                                *
    #************************************************************************************
    if receiver_type == '.jds':
        num_frequencies = len(frequency_list)-4

    shift_vector = DM_shift_calc(len(frequency_list), fmin, fmax, df / pow(10,6), TimeRes, DM, receiver_type)

    #plot1D(shift_vector, newpath+'/01 - Shift parameter.png', 'Shift parameter', 'Shift parameter', 'Shift parameter', 'Frequency channel number', customDPI)

    max_shift = np.abs(shift_vector[0])
    print (' Maximal shift is:              ', max_shift, ' pixels \n')

    num_spectra = 2 * max_shift

    buffer_array = np.zeros((num_frequencies, 4 * max_shift))


    dat_file = open(data_filename, 'rb')
    dat_file.seek(1024)                     # Jumping to 1024 byte from file beginning

    # Calculate the number of blocks in file
    numOfBlocks = 4
    for block in range (numOfBlocks):

        print ('\n * Data block # ', block + 1, '\n ****************************************************************** \n')

        if receiver_type == '.jds':
            data = np.fromfile(dat_file, dtype=np.float64, count = (num_frequencies+4) * num_spectra)
            data = np.reshape(data, [(num_frequencies+4), num_spectra], order='F')
            data = data[ : num_frequencies, :] # To delete the last channels of DSP spectra data where exact time is stored


        nowTime = time.time()
        print ('  * Preparation of data took:            ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime


        # Normalization of data
        Normalization_lin(data, num_frequencies, num_spectra)

        '''
        # Log data to examine it in a plot
        data_log = np.empty((num_frequencies, num_spectra), float)

        with np.errstate(invalid='ignore'):
            data_log[:,:] = 10 * np.log10(data[:,:])
        data_log[np.isnan(data_log)] = 0

        plot2Da(data_log, newpath+'/02'+ ' fig. ' +str(block+1)+' - Full log initial data.png', frequency_list, np.min(data_log), np.max(data_log), colormap, 'Full log initial data', customDPI)
        del data_log
        '''

        if Cleaning > 0:

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
            pylab.savefig(newpath+'/00_10'+ ' fig. ' +str(block+1)+'- Result mask after lines cleaning.png', bbox_inches='tight', dpi = 300)
            plt.close('all')

            # Cleaning remaining 1 pixel splashes of RFI
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
            pylab.savefig(newpath+'/00_11'+ ' fig. ' +str(block+1)+' - Mask after fine STD cleaning.png', bbox_inches='tight', dpi = 300)
            plt.close('all')

            nowTime = time.time()
            print ('\n  * Normalization and cleaning took:     ', round((nowTime - previousTime), 2), 'seconds ')
            previousTime = nowTime



        # Averaging and logging data
        data_log = np.empty((num_frequencies, num_spectra), float)
        with np.errstate(invalid='ignore'):
            data_log[:,:] = 10 * np.log10(data[:,:])
        data_log[np.isnan(data_log)] = 0
        del data




        plot2Da(data_log, newpath+'/03 '+ ' fig. ' +str(block+1)+'- Full log cleaned data.png', frequency_list, np.min(data_log), np.max(data_log), colormap, 'Full log initial data', customDPI)

        plot1D(data_log[:,1], newpath+'/04a '+ ' fig. ' +str(block+1)+'- Cleaned data single specter.png', 'Label', 'Initial data specter', 'Frequency, MHz', 'Amplitude, AU', customDPI)
        plot1D(data_log[1,:], newpath+'/04b '+ ' fig. ' +str(block+1)+'- Cleaned data single channel.png', 'Label', 'Initial data channel', 'Time, spectra counts', 'Amplitude, AU', customDPI)


        nowTime = time.time() #                            '
        print ('\n  * Time before dispersion compensation: ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime


        # Creation of big array for correct dispersion compensation and adding the next data block
        temp_array = np.zeros((num_frequencies, 4 * max_shift))
        temp_array[:, 4 * max_shift - num_spectra : 4 * max_shift] = data_log[:,:]
        del data_log
        temp_array = DM_compensation_with_indices_changes(temp_array, shift_vector[0: num_frequencies])

        nowTime = time.time() #                            '
        print ('\n  * Dispersion compensation took:        ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime


        plot2Da(temp_array, newpath+'/05 '+ ' fig. ' +str(block+1)+'- DM compensated data.png', frequency_list, np.min(temp_array), np.max(temp_array), colormap, 'DM compensated data', customDPI)

        # Rolling temp_array to put current data first
        if block == 0:
            #temp_array[:] = np.roll(temp_array[:], - num_spectra)
            temp_array = DM_compensation_with_indices_changes(temp_array, np.full(num_frequencies, - num_spectra) )
            temp_array[:, 3 * max_shift : ] = 0
            buffer_array += temp_array
        else:
            temp_array = DM_compensation_with_indices_changes(temp_array, np.full(num_frequencies, - max_shift) )
            buffer_array += temp_array
            #buffer_array[:] = np.roll(buffer_array[:], - max_shift)



        plot2Da(temp_array, newpath+'/06'+ ' fig. ' +str(block+1)+' - DM compensated data.png', frequency_list, np.min(temp_array), np.max(temp_array), colormap, 'Shifted compensated full data', customDPI)

        nowTime = time.time() #                            '
        print ('\n  * Data rolling took:                   ', round((nowTime - previousTime), 2), 'seconds ')
        previousTime = nowTime


        # Making and filling the array with fully ready data for plotting and saving to a file
        if block == 0:
            array_compensated_DM = np.zeros((num_frequencies, max_shift), float)
            array_compensated_DM = buffer_array[:, 0 : max_shift]
            buffer_array = DM_compensation_with_indices_changes(buffer_array, np.full(num_frequencies, - max_shift) )
            buffer_array[:, 3 * max_shift : ] = 0
        else:
            array_compensated_DM = np.zeros((num_frequencies, num_spectra), float)
            array_compensated_DM = buffer_array[:, 0 : num_spectra]
            buffer_array = DM_compensation_with_indices_changes(buffer_array, np.full(num_frequencies, - num_spectra) )
            buffer_array[:, max_shift : ] = 0

        #del temp_array

        plot2Da(array_compensated_DM, newpath+'/07' + ' fig. ' +str(block+1)+'- Only full ready data.png', frequency_list, np.min(array_compensated_DM), np.max(array_compensated_DM), colormap, 'Only full ready data', customDPI)

        spectrum = array_compensated_DM.mean(axis=1)[:]
        profile = array_compensated_DM.mean(axis=0)[:]
        profile = profile - np.mean(profile)

        plot1D(spectrum, newpath+'/08' + ' fig. ' +str(block+1)+' - Averaged spectrum.png', 'Label', 'Averaged spectrum', 'x_label', 'y_label', customDPI)
        #plot1D(profile,  newpath+'/09 - Temporal profile of pulses.png', 'Label', 'Temporal profile of pulses', 'x_label', 'y_label', customDPI)


        # Averaging of the array with pulses for picture
        averaged_array  = average_some_lines_of_array(array_compensated_DM, int(num_frequencies/192))

        # Plotting picture

        fig = plt.figure(figsize = (9, 6))
        ax1 = fig.add_subplot(211)
        ax1.plot(profile, color =u'#1f77b4', linestyle = '-', alpha=1.0, linewidth = '1.00', label = 'Pulses time profile')
        ax1.legend(loc = 'upper right', fontsize = 6)
        ax1.grid(b = True, which = 'both', color = 'silver', linestyle = '-')
        ax1.axis([0, len(profile), -0.1, 0.5])
        ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax1.set_title('Data from file: '+ filename + ', description: ' + df_description, fontsize = 6)
        ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        ax2 = fig.add_subplot(212)
        ax2.imshow(np.flipud(averaged_array), aspect='auto', cmap='Greys', extent=[0,len(profile),frequency_list[0],frequency_list[num_frequencies-1]]) # vmin=-4, vmax=4,
        ax2.set_xlabel('Time, counts', fontsize=6, fontweight='bold')
        ax2.set_ylabel('Frequency, MHz', fontsize=6, fontweight='bold')
        fig.subplots_adjust(hspace=0.05, top=0.92)
        fig.suptitle('Single pulses of pulsar, fig. ' + str(block+1), fontsize = 8, fontweight='bold')
        fig.text(0.77, 0.06, 'Processed '+currentDate+ ' at '+currentTime, fontsize=4, transform=plt.gcf().transFigure)
        fig.text(0.09, 0.06, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=4, transform=plt.gcf().transFigure)
        pylab.savefig(newpath + '/'+ filename + ' fig. ' +str(block+1)+ ' - Combined picture.png', bbox_inches = 'tight', dpi = 300)
        plt.close('all')

dat_file.close()
endTime = time.time()    # Time of calculations


for i in range (0,2) : print (' ')
#print ('   The program execution lasted for ', round((endTime - startTime),3), 'seconds')
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')

for i in range (0,2) : print (' ')
print ('                 *** Program PULSAR_single_pulse_reader has finished! ***')
for i in range (0,3) : print (' ')
