# Python3
Software_version = '2020.01.03'
Software_name = 'Pulsar data folding'
# Program intended to read and fold pulsar data from DAT files to obtain average pulse

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************
# Path to data files
common_path = 'DATA/'

# Directory of DAT file to be analyzed:
filename = 'E300117_180000.jds_Data_chA.dat'

pulsar_period = 1.292



average_const = 192            # Number of frequency channels to average in result picture
prifile_pic_min = -0.1         # Minimum limit of profile picture
prifile_pic_max = 0.5          # Maximum limit of profile picture

cleaning = 0                   # Apply cleaning to data (1) or skip it (0)
# Parameters of vertical and horizontal lines cleaning
no_of_iterations = 2           # Number of lines cleaning iterations (usually 2-3)
std_lines_clean = 0.8          # Limit in StD of pixels in line to clean
pic_in_line = 3                # Number of pixels in line
# Parameter of pixels cleaning based on StD value estimation
std_pixels_clean = 1.8

SpecFreqRange = 1              # Specify particular frequency range (1) or whole range (0)
# Begin and end frequency of dynamic spectrum (MHz)
freqStart = 20.0
freqStop = 30.0

customDPI = 300                # Resolution of images of dynamic spectra
colormap = 'Greys'             # Colormap of images of dynamic spectra ('jet' or 'Greys')

DM = 5.750   # 'B0809+74'
# DM = 45.325  # 'J0250+5854'
#*************************************************************


#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************
import os
import sys
import time
import pylab
import numpy as np
import matplotlib.pyplot as plt
from os import path


# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_ra_data_processing.spectra_normalization import Normalization_lin
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_pulsar_processing.pulsar_dm_shift_calculation_aver_pulse import pulsar_dm_shift_calculation_aver_pulse
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes
from package_plot_formats.plot_formats import plot1D, plot2Da


def simple_mask_clean(array, RFI_std_const):
    '''
    Simplest cleaning of entire frequency channels polluted with RFI
    '''


    # Making mask array
    mask = np.zeros_like(array, dtype=bool)
    temp_array = np.zeros_like(array)
    temp_array[:,:] = array[:,:]

    for i in range(3):
        # Search for polluted channels in averaged profile
        integr_profile_01 = np.sum(temp_array, axis = 0)
        ip_mean = np.mean(integr_profile_01)
        ip_std = np.std(integr_profile_01)
        polluted_channels = []
        for i in range(len(integr_profile_01)):
            if integr_profile_01[i] > ip_mean + RFI_std_const * ip_std:
                polluted_channels.append(i)

        for i in range(len(polluted_channels)):
            mask[:, polluted_channels[i]] = 1

        integr_profile_02 = np.sum(temp_array, axis = 1)
        ip_mean = np.mean(integr_profile_02)
        ip_std = np.std(integr_profile_02)
        polluted_channels = []
        for i in range(len(integr_profile_02)):
            if integr_profile_02[i] > ip_mean + RFI_std_const * ip_std:
                polluted_channels.append(i)

        for i in range(len(polluted_channels)):
            mask[polluted_channels[i], :] = 1

        # Mask polluted channels in array
        temp_array = np.ma.masked_array(temp_array, mask=mask)


    # Calculate mean of array with masked polluted channels
    ma_mean = np.mean(temp_array)

    # Change the polluted channels to masked array mean value
    array = array * np.abs(mask - 1) + mask * ma_mean

    return array, mask



################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************
print ('\n\n\n\n\n\n\n\n   **************************************************************')
print ('   *    ', Software_name,' v.',Software_version,'     *      (c) YeS 2019')
print ('   ************************************************************** \n\n\n')

startTime = time.time()
previousTime = startTime
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, ' \n')

data_filename = common_path + filename

# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
newpath = "PULSAR_folded_data"
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
    [TimeRes, fmin, fmax, df, frequency_list, FFTsize] = FileHeaderReaderADR(data_filename, 0)

if receiver_type == '.jds':
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
    CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr,
    TimeRes, fmin, fmax, df, frequency_list, FFTsize, dataBlockSize] = FileHeaderReaderJDS(data_filename, 0, 1)


#************************************************************************************
#                            R E A D I N G   D A T A                                *
#************************************************************************************
num_frequencies = len(frequency_list)

# Calculating number of samples per period and number of blocks
samples_per_period = int(np.ceil(pulsar_period / TimeRes))
num_of_blocks = int(np.floor(SpInFile / samples_per_period))

print (' Number of samples per period:  ', samples_per_period, ' \n')
print (' Number of blocks in file:      ', num_of_blocks, ' \n')


if receiver_type == '.jds':
    num_frequencies_initial = len(frequency_list)-4

frequency_list_initial = np.empty_like(frequency_list)
frequency_list_initial[:] = frequency_list[:]

dat_file = open(data_filename, 'rb')
dat_file.seek(1024)                     # Jumping to 1024 byte from file beginning


buffer_array = np.zeros((num_frequencies_initial, samples_per_period))

for block in range (num_of_blocks):   #      main loop by number of blocks in file

    #print ('\n * Data block # ', block + 1, ' of ', num_of_blocks,'\n ******************************************************************')

    # Data block reading
    if receiver_type == '.jds':
        data = np.fromfile(dat_file, dtype=np.float64, count = (num_frequencies_initial+4) * samples_per_period)
        data = np.reshape(data, [(num_frequencies_initial+4), samples_per_period], order='F')
        data = data[ : num_frequencies_initial, :] # To delete the last channels of DSP spectra data where exact time is stored

    frequency_list[:] = frequency_list_initial[:-4]

    # Normalization of data
    Normalization_lin(data, num_frequencies_initial, samples_per_period)

    data, mask = simple_mask_clean(data, 3.0)
    #data, mask = simple_mask_clean(data, 0.3)
    #plot2Da(mask, newpath + '/fig. 3 - mask of data.png', frequency_list, 0, 1, colormap,'averaged data', customDPI)

    # Adding the next data block
    buffer_array += data

# Logging the data
with np.errstate(invalid='ignore'):
    buffer_array[:,:] = 10 * np.log10(buffer_array[:,:])
buffer_array[np.isnan(buffer_array)] = 0

# Normalizing log data
buffer_array = buffer_array - np.mean(buffer_array)

profile_0 = np.sum(buffer_array, axis = 0)
profile_1 = np.sum(buffer_array, axis = 1)

plt.figure(1, figsize=(10.0, 6.0))
plt.subplots_adjust(left=None, bottom=None, right=None, top=0.86, wspace=None, hspace=0.3)
plt.subplot(2, 1, 1)
plt.title('Data integrated over time and over frequency \n File: ', fontsize=10,
          fontweight='bold', style='italic', y=1.025)
plt.plot(profile_0)
plt.xlabel('Samples in time', fontsize=8, fontweight='bold')
plt.ylabel('Dummy values', fontsize=8, fontweight='bold')
plt.xticks(fontsize=6, fontweight='bold')
plt.yticks(fontsize=6, fontweight='bold')
plt.subplot(2, 1, 2)
plt.plot(profile_1)
plt.xlabel('Frequency points', fontsize=8, fontweight='bold')
plt.ylabel('Dummy values', fontsize=8, fontweight='bold')
plt.xticks(fontsize=6, fontweight='bold')
plt.yticks(fontsize=6, fontweight='bold')
pylab.savefig(newpath + '/02 data integrated over time and over frequency.png',
              bbox_inches='tight', dpi=250)
plt.close('all')

plot2Da(buffer_array, newpath+'/fig. 1 - averaged data.png', frequency_list, -3, 2, colormap, 'averaged data', customDPI)


shift_vector = pulsar_dm_shift_calculation_aver_pulse(len(frequency_list), fmin, fmax, df / pow(10,6), TimeRes, DM, pulsar_period)

# Dispersion compensation
buffer_array = pulsar_DM_compensation_with_indices_changes(buffer_array, shift_vector)

plot2Da(buffer_array, newpath+'/fig. 1 - dedispersed averaged data.png', frequency_list, -3, 2, colormap, 'averaged data', customDPI)

AverageChannelNumber = 128
reduced_matrix = np.array([[0.0 for col in range(samples_per_period)] for row in range(int(len(frequency_list)/AverageChannelNumber))])
for i in range (int(len(frequency_list) / AverageChannelNumber)):
    for j in range (samples_per_period):
        reduced_matrix[i, j] = sum(buffer_array[i*AverageChannelNumber : (i+1)*AverageChannelNumber, j])

plot2Da(reduced_matrix, newpath+'/fig. 2 - twice averaged data.png', frequency_list, -3, 2, colormap, 'averaged data', customDPI)


profile_0 = np.sum(buffer_array, axis = 0)
profile_1 = np.sum(buffer_array, axis = 1)

plt.figure(1, figsize=(10.0, 6.0))
plt.subplots_adjust(left=None, bottom=None, right=None, top=0.86, wspace=None, hspace=0.3)
plt.subplot(2, 1, 1)
plt.title('Data integrated over time and over frequency \n File: ', fontsize=10,
          fontweight='bold', style='italic', y=1.025)
plt.plot(profile_0)
plt.xlabel('Samples in time', fontsize=8, fontweight='bold')
plt.ylabel('Dummy values', fontsize=8, fontweight='bold')
plt.xticks(fontsize=6, fontweight='bold')
plt.yticks(fontsize=6, fontweight='bold')
plt.subplot(2, 1, 2)
plt.plot(profile_1)
plt.xlabel('Frequency points', fontsize=8, fontweight='bold')
plt.ylabel('Dummy values', fontsize=8, fontweight='bold')
plt.xticks(fontsize=6, fontweight='bold')
plt.yticks(fontsize=6, fontweight='bold')
pylab.savefig(newpath + '/03 dedispersed data integrated over time and over frequency.png',
              bbox_inches='tight', dpi=250)
plt.close('all')

dat_file.close()
endTime = time.time()    # Time of calculations


print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n\n                 *** Program PULSAR_single_pulse_reader has finished! *** \n\n\n')
