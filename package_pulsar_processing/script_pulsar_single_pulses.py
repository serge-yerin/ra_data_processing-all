# Python3
Software_version = '2020.03.14'
Software_name = 'Pulsar single pulses processing pipeline'
# Program intended to read and show individual pulses of pulsars from DAT files
# *******************************************************************************
#                     M A N U A L    P A R A M E T E R S                        *
# *******************************************************************************
# Path to data files
common_path = ''

# Directory of DAT file to be analyzed:
filename = 'E280120_212713.jds_Data_chA.dat' # 'E220213_201439.jds_Data_chA.dat'

pulsar_name = 'B0809+74' # 'B0950+08'

average_const = 512            # Number of frequency channels to appear in result picture
profile_pic_min = -0.15        # Minimum limit of profile picture
profile_pic_max = 0.55         # Maximum limit of profile picture

cleaning_Iana = 0
cleaning = 0                   # Apply cleaning to data (1) or skip it (0)
# Parameters of vertical and horizontal lines cleaning
no_of_iterations = 2           # Number of lines cleaning iterations (usually 2-3)
std_lines_clean = 1            # Limit in StD of pixels in line to clean
pic_in_line = 10               # Number of pixels in line
std_pixels_clean = 2.8         # Parameter of pixels cleaning based on StD value estimation

SpecFreqRange = 0              # Specify particular frequency range (1) or whole range (0)
freqStart = 20.0               # Lower frequency of dynamic spectrum (MHz)
freqStop = 30.0                # Higher frequency of dynamic spectrum (MHz)

save_profile_txt = 1           # Save profile data to TXT file?
save_compensated_data = 1      # Save data with compensated DM to DAT file?
customDPI = 300                # Resolution of images of dynamic spectra
colormap = 'Greys'             # Colormap of images of dynamic spectra ('jet' or 'Greys')
# *******************************************************************************

# *******************************************************************************
#                     I M P O R T   L I B R A R I E S                           *
# *******************************************************************************
import os
import sys
import time
import pylab
import numpy as np
import matplotlib.pyplot as plt
from os import path
from matplotlib import rc

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_ra_data_processing.spectra_normalization import Normalization_lin
from package_ra_data_processing.average_some_lines_of_array import average_some_lines_of_array
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
from package_ra_data_files_formats.specify_frequency_range import specify_frequency_range
from package_pulsar_processing.pulsar_DM_full_shift_calculation import DM_full_shift_calc
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes
from package_pulsar_processing.pulsar_pulses_time_profile_FFT import pulsar_pulses_time_profile_FFT
from package_cleaning.clean_lines_of_pixels import clean_lines_of_pixels
from package_cleaning.array_clean_by_STD_value import array_clean_by_STD_value
from package_cleaning.survey_cleaning import survey_cleaning
from package_astronomy.catalogue_pulsar import catalogue_pulsar


# *******************************************************************************
#                              F U N C T I O N S                                *
# *******************************************************************************


def plot_ready_data(profile, averaged_array, frequency_list, num_frequencies, fig_time_scale, filename,
                    pulsar_name, DM, freq_resolution, time_resolution, max_time_shift, fig_no, fig_num,
                    profile_pic_min, profile_pic_max, df_description, colormap, customDPI, currentDate,
                    currentTime, Software_version):

    # Making result picture
    fig = plt.figure(figsize = (9.2, 4.5))
    rc('font', size=5, weight='bold')
    ax1 = fig.add_subplot(211)
    ax1.plot(profile, color =u'#1f77b4', linestyle = '-', alpha=1.0, linewidth = '0.60', label = 'Pulses time profile')
    ax1.legend(loc = 'upper right', fontsize = 5)
    ax1.grid(b = True, which = 'both', color = 'silver', linewidth = '0.50', linestyle = '-')
    ax1.axis([0, len(profile), profile_pic_min, profile_pic_max])
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title('File: '+ filename + '  Description: ' + df_description + '  Averaging: '+
                  str(np.round(freq_resolution, 3))+' kHz and '+str(np.round(time_resolution*1000,3))+
                  ' ms.  Max. shift: '+ str(np.round(max_time_shift,3))+' s.', fontsize = 5, fontweight='bold')
    ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax2 = fig.add_subplot(212)
    ax2.imshow(np.flipud(averaged_array), aspect='auto', cmap=colormap, extent=[0,len(profile),frequency_list[0],frequency_list[num_frequencies-1]])
    ax2.set_xlabel('Time UTC (at the lowest frequency), HH:MM:SS.ms', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Frequency, MHz', fontsize=6, fontweight='bold')
    text = ax2.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = fig_time_scale[k]
    ax2.set_xticklabels(text, fontsize = 5, fontweight = 'bold')
    fig.subplots_adjust(hspace=0.05, top=0.91) # top=0.92
    fig.suptitle('Single pulses of '+pulsar_name+' (DM = '+str(DM)+r' $\mathrm{pc \cdot cm^{-3}}$'+'), fig. ' +
                 str(fig_no) + ' of ' + str(fig_num), fontsize = 7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed '+currentDate+ ' at '+currentTime, fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig(newpath + '/'+ filename + ' fig. ' +str(block)+ ' - Combined picture.png', bbox_inches = 'tight', dpi = customDPI)
    plt.close('all')


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************

print(' \n\n\n\n\n\n\n\n')
print('   *****************************************************************')
print('   *   ', Software_name, ' v.', Software_version,'   *      (c) YeS 2020')
print('   ***************************************************************** \n\n\n')

startTime = time.time()
previousTime = startTime
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, ' \n')

rc('font', size = 6, weight='bold')
data_filename = common_path + filename

# *** Creating a folder where all pictures and results will be stored (if it doesn't exist) ***
newpath = "RESULTS_pulsar_single_pulses"
if not os.path.exists(newpath):
    os.makedirs(newpath)

# Path to timeline file to be analyzed:
time_line_file_name = common_path + filename[-31:-13] +'_Timeline.txt'

if save_profile_txt > 0:
    # *** Creating a name for long timeline TXT file ***
    profile_file_name = newpath + '/' + filename +'_time_profile.txt'
    profile_txt_file = open(profile_file_name, 'w')  # Open and close to delete the file with the same name
    profile_txt_file.close()

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

# Manually set frequencies for two channels mode
if int(CLCfrq/1000000) == 33:
    FFTsize = 8192
    fmin = 16.5
    fmax = 33.0
    frequency_list = np.linspace(fmin, fmax, FFTsize)

sp_in_file = int(((df_filesize - 1024)/(len(frequency_list) * 8))) # the second dimension of the array: file size - 1024 bytes

pulsar_ra, pulsar_dec, DM, p_bar = catalogue_pulsar(pulsar_name)

if save_compensated_data > 0:
    with open(data_filename, 'rb') as file:
        file_header = file.read(1024)  # Data file header read

    # *** Creating a binary file with data for long data storage ***
    new_data_file_name = pulsar_name + '_DM_' + str(DM) + '_' + filename
    new_data_file = open(new_data_file_name, 'wb')
    new_data_file.write(file_header)
    new_data_file.close()

    # *** Creating a name for long timeline TXT file ***
    new_TLfile_name = pulsar_name + '_DM_' + str(DM) + '_' + data_filename[:-13] + '_Timeline.txt'
    new_TLfile = open(new_TLfile_name, 'w')  # Open and close to delete the file with the same name
    new_TLfile.close()

    del file_header

# ************************************************************************************
#                             R E A D I N G   D A T A                                *
# ************************************************************************************

# Time line file reading
timeline, dt_timeline = time_line_file_reader(time_line_file_name)

# Selecting the frequency range of data to be analyzed
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

    # Save to file header the frequency range of new data !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    '''
    file_data_A_name = df_filename + '_Data_chA.dat'
    file_data_A = open(file_data_A_name, 'wb')
    file_data_A.write(file_header)
    file_data_A.seek(636)  # Navr place in header
    file_data_A.write(bytes([np.int32(Navr * no_of_spectra_to_average)]))
    file_data_A.close()
    '''

else:
    shift_vector = DM_full_shift_calc(len(frequency_list)-4, fmin, fmax, df / pow(10, 6), TimeRes, DM, receiver_type)
    print (' Number of frequency channels:  ', len(frequency_list)-4)

max_shift = np.abs(shift_vector[0])

if SpecFreqRange == 1:
    buffer_array = np.zeros((ifmax - ifmin, 2 * max_shift))
else:
    buffer_array = np.zeros((len(frequency_list) - 4, 2 * max_shift))

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

    # Time line arrangements:
    fig_time_scale = []
    for i in range (block * max_shift, (block+1) * max_shift):  # Shows the time of pulse end (at lowest frequency)
        fig_time_scale.append(timeline[i][11:23])
    print(' Time: ', fig_time_scale[0], ' - ', fig_time_scale[-1], ', number of points: ', len(fig_time_scale))


    # Data block reading
    if receiver_type == '.jds':
        data = np.fromfile(dat_file, dtype=np.float64, count = (num_frequencies_initial+4) * 1 * max_shift)   # 2
        data = np.reshape(data, [(num_frequencies_initial+4), 1 * max_shift], order='F')  # 2
        data = data[ : num_frequencies_initial, :] # To delete the last channels of DSP spectra data where exact time is stored


    # Cutting the array in predefined frequency range
    if SpecFreqRange == 1:
        data, frequency_list, fi_start, fi_stop = specify_frequency_range(data, frequency_list_initial, freqStart, freqStop)
        num_frequencies = len(frequency_list)
    else:
        num_frequencies = num_frequencies_initial

    # Normalization of data
    Normalization_lin(data, num_frequencies, 1 * max_shift)

    nowTime = time.time()
    print ('\n  *** Preparation of data took:              ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime

    if cleaning_Iana > 0:
        data = survey_cleaning(data)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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

    '''
    # Logging the data
    with np.errstate(invalid='ignore'):
        data[:,:] = 10 * np.log10(data[:,:])
    data[np.isnan(data)] = 0

    # Normalizing log data
    data = data - np.mean(data)
    '''


    # Dispersion delay compensation
    data_space = np.zeros((num_frequencies, 2 * max_shift))
    data_space[:, max_shift : ] = data[:,:]
    temp_array = pulsar_DM_compensation_with_indices_changes(data_space, shift_vector)
    del data, data_space


    nowTime = time.time()
    print ('\n  *** Dispersion compensation took:          ', round((nowTime - previousTime), 2), 'seconds ')
    previousTime = nowTime

    # Adding the next data block
    buffer_array += temp_array

    # Making and filling the array with fully ready data for plotting and saving to a file
    array_compensated_DM = buffer_array[:, 0 : max_shift]

    if block > 0:
        # Saving data with compensated DM to DAT file
        if save_compensated_data > 0 and block > 0:
            temp = array_compensated_DM.copy(order='C')   # .transpose()
            new_data_file = open(new_data_file_name, 'ab')
            new_data_file.write(temp)
            new_data_file.close()

            # Saving time data to ling timeline file
            with open(new_TLfile_name, 'a') as new_TLfile:
                for i in range(max_shift):
                    new_TLfile.write((fig_time_scale[i][:]) + ' \n')  # str


        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Logging the data
        with np.errstate(divide='ignore'):
            array_compensated_DM[:, :] = 10 * np.log10(array_compensated_DM[:, :])
        array_compensated_DM[array_compensated_DM == -np.inf] = 0

        # Normalizing log data
        array_compensated_DM = array_compensated_DM - np.mean(array_compensated_DM)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Preparing single averaged data profile for figure
        profile = array_compensated_DM.mean(axis=0)[:]
        profile = profile - np.mean(profile)

        # Save full profile to TXT file
        if save_profile_txt > 0:
            profile_txt_file = open(profile_file_name, 'a')
            for i in range(len(profile)):
                profile_txt_file.write(str(profile[i]) + ' \n')
            profile_txt_file.close()

        # Averaging of the array with pulses for figure
        averaged_array  = average_some_lines_of_array(array_compensated_DM, int(num_frequencies/average_const))
        freq_resolution = (df * int(num_frequencies/average_const)) / 1000.
        max_time_shift = max_shift * TimeRes

        plot_ready_data(profile, averaged_array, frequency_list, num_frequencies, fig_time_scale, filename,
                        pulsar_name, DM, freq_resolution, TimeRes, max_time_shift, block, num_of_blocks-1,
                        profile_pic_min, profile_pic_max, df_description, colormap, customDPI, currentDate,
                        currentTime, Software_version)

    # Rolling temp_array to put current data first
    buffer_array = np.roll(buffer_array, - max_shift)
    buffer_array[:, max_shift : ] = 0

dat_file.close()

# Fourier analysis of the obtained time profile of pulses
if save_profile_txt > 0:
    print('\n\n  *** Making Fourier transform of the time profile...')
    pulsar_pulses_time_profile_FFT(newpath+'/', filename +'_time_profile.txt', pulsar_name, TimeRes,
                                   profile_pic_min, profile_pic_max, customDPI, colormap)

endTime = time.time()    # Time of calculations


print ('\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
