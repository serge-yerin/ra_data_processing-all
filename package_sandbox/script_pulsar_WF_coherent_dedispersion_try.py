# Python3
#
#   !!!! NOT FINISHED !!!
#
Software_version = '2020.01.04'
Software_name = 'Coherent dispersion compensation'
# Program intended to read, show and analyze data from DSPZ receivers in waveform mode

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Directory of files to be analyzed:
directory = 'DATA/' # 'DATA/'
pulsar_name = 'B0950+08'

SpecFreqRange = 1              # Specify particular frequency range (1) or whole range (0)
# Begin and end frequency of dynamic spectrum (MHz)
freqStart = 28.0
freqStop = 30.0

average_const = 512            # Number of frequency channels to average in result picture
no_of_batches_in_file = 32      # Number of data batches in file (depends on the RAM volume) more batches for smaller RAM
#VminNorm = 0                   # Lower limit of figure dynamic range for normalized spectra
#VmaxNorm = 5                   # Upper limit of figure dynamic range for normalized spectra
colormap = 'Greys'             # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
customDPI = 300                 # Resolution of images of dynamic spectra


################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
# Common functions
import os
import sys
import numpy as np
import time
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_pulsar_processing.pulsar_DM_full_shift_calculation import DM_full_shift_calc
from package_ra_data_processing.average_some_lines_of_array import average_some_lines_of_array
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.JDS_waveform_time import JDS_waveform_time
from package_ra_data_files_formats.specify_frequency_range import specify_frequency_range
from package_sandbox.f_make_long_spectra_files_from_wf import make_long_spectra_files_from_wf
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes

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

################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************

print ('\n\n\n\n\n\n\n\n   **************************************************************')
print ('   *    ', Software_name,' v.',Software_version,'     *      (c) YeS 2020')
print ('   ************************************************************** \n\n\n')

startTime = time.time()
previousTime = startTime
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, ' \n')


# *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
result_folder = directory + 'TEMP_WF'
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

# *** Search JDS files in the directory ***
fileList = find_files_only_in_current_folder(directory, '.jds', 1)


# Make long data files

#file_data_re_name, file_data_im_name, TLfile_name = make_long_spectra_files_from_wf(directory, fileList, result_folder)


file_data_re_name = 'DATA/TEMP_WF/E220213_201455.jds_Data_WRe.dat'
file_data_im_name = 'DATA/TEMP_WF/E220213_201455.jds_Data_WIm.dat'
TLfile_name = 'DATA/TEMP_WF/E220213_201455.jds_Timeline.txt'

# Compensate DM for both long data files

pulsar_ra, pulsar_dec, DM = catalogue_pulsar(pulsar_name)
print ('\n\n Dispersion measure from catalogue =  ', DM, ' pc / cm3 \n')

data_filename = file_data_re_name


# *** Opening DAT datafile ***
file = open(file_data_re_name, 'rb')

# reading FHEADER
df_filesize = (os.stat(data_filename).st_size)                          # Size of file
df_filename = file.read(32).decode('utf-8').rstrip('\x00')              # Initial data file name
file.close()

receiver_type = df_filename[-4:]

# Reading file header to obtain main parameters of the file

if receiver_type == '.jds':
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
    CLCfrq, df_creation_timeUTC, sp_in_file, ReceiverMode, Mode, Navr,
    TimeRes, fmin, fmax, df, frequency_list, FFTsize, dataBlockSize] = FileHeaderReaderJDS(data_filename, 0, 1)


sp_in_file = int(((df_filesize - 1024)/(len(frequency_list) * 8))) # the second dimension of the array: file size - 1024 bytes

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


    # Dispersion compensation
    data_space = np.zeros((num_frequencies, 2 * max_shift))
    data_space[:, max_shift : ] = data[:,:]
    temp_array = pulsar_DM_compensation_with_indices_changes(data_space, shift_vector)
    del data, data_space


    # Adding the next data block
    buffer_array += temp_array

    # Making and filling the array with fully ready data for plotting and saving to a file
    array_compensated_DM = buffer_array[:, 0 : max_shift]
    #plot_ready_data(array_compensated_DM, frequency_list, num_frequencies, average_const, df_filename, colormap, customDPI, currentDate, currentTime, Software_version)

    # Rolling temp_array to put current data first
    buffer_array = np.roll(buffer_array, - max_shift)
    buffer_array[:, max_shift : ] = 0


dat_file.close()


endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program JDS_WF_reader has finished! *** \n\n\n')
