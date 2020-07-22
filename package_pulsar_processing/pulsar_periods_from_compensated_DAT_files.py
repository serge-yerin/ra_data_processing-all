# Python3
Software_version = '2020.03.19'
Software_name = 'Pulsar DM delay compensated DAT reader'
# Program intended to read and show pulsar data from DAT files (with compensated DM delay)
# Make figures overlap by one pulse!!!

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
common_path = '' # '/media/data/PYTHON/ra_data_processing-all/' #

# Directory of DAT file to be analyzed:
filename = 'Norm_DM_0.972_DM_1.0_DM_1.0_E310120_225419.jds_Data_wfA+B.dat'

pulsar_name = 'B0950+08'
normalize_response = 0            # Normalize (1) or not (0) the frequency response
profile_pic_min = -0.15           # Minimum limit of profile picture
profile_pic_max = 0.55            # Maximum limit of profile picture
spectrum_pic_min = -0.2           # Minimum limit of dynamic spectrum picture
spectrum_pic_max = 3              # Maximum limit of dynamic spectrum picture

periods_per_fig = 3

customDPI = 500                   # Resolution of images of dynamic spectra
colormap = 'Greys'                # Colormap of images of dynamic spectra ('jet' or 'Greys')


#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
import os
import sys
import numpy as np
import time
import pylab
import matplotlib.pyplot as plt
from os import path
from matplotlib import rc
from progress.bar import IncrementalBar

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_ra_data_processing.spectra_normalization import Normalization_dB
################################################################################


# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************

def pulsar_period_DM_compensated_pics(common_path, filename, pulsar_name, normalize_response, profile_pic_min,
                                      profile_pic_max, spectrum_pic_min, spectrum_pic_max, periods_per_fig, customDPI,
                                      colormap):

    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")

    # Creating a folder where all pictures and results will be stored (if it doesn't exist)
    result_path = "RESULTS_pulsar_n_periods_pics_" + filename
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    # Finding pulsar name from file name
    #pulsar_name = find_between(filename, '', '_')

    # Taking pulsar period from catalogue
    pulsar_ra, pulsar_dec, DM, p_bar = catalogue_pulsar(pulsar_name)

    # DAT file to be analyzed:
    filepath = common_path + filename

    # Timeline file to be analyzed:
    #timeline_filepath = common_path + filename[:-13] + '_Timeline.txt'
    timeline_filepath = common_path + filename.split('_Data_')[0] + '_Timeline.txt'

    # Opening DAT datafile
    file = open(filepath, 'rb')

    # Data file header read
    df_filesize = (os.stat(filepath).st_size)                       # Size of file
    df_filepath = file.read(32).decode('utf-8').rstrip('\x00')      # Initial data file name
    file.close()

    if df_filepath[-4:] == '.adr':

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description,
                CLCfrq, df_creation_timeUTC, ReceiverMode, Mode, sumDifMode,
                NAvr, time_resolution, fmin, fmax, df, frequency, FFTsize, SLine,
                Width, BlockSize] = FileHeaderReaderADR(filepath, 0, 1)

        freq_points_num = len(frequency)

    if df_filepath[-4:] == '.jds':     # If data obtained from DSPZ receiver

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description,
                CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr, time_resolution, fmin, fmax,
                df, frequency, freq_points_num, dataBlockSize] = FileHeaderReaderJDS(filepath, 0, 1)

    # ************************************************************************************
    #                             R E A D I N G   D A T A                                *
    # ************************************************************************************

    # Time line file reading
    timeline, dt_timeline = time_line_file_reader(timeline_filepath)

    # Calculation of the dimensions of arrays to read taking into account the pulsar period
    spectra_in_file = int((df_filesize - 1024) / (8 * freq_points_num))    # int(df_filesize - 1024)/(2*4*freq_points_num)
    spectra_to_read = int(np.round((periods_per_fig * p_bar / time_resolution),0))
    num_of_blocks = int(np.floor(spectra_in_file / spectra_to_read))

    print(' Pulsar period:                           ', p_bar, 's.')
    print(' Time resolution:                         ', time_resolution, 's.')
    print(' Number of spectra to read in', periods_per_fig, 'periods:  ', spectra_to_read, ' ')
    print(' Number of spectra in file:               ', spectra_in_file, ' ')
    print(' Number of', periods_per_fig,'periods blocks in file:      ', num_of_blocks, '\n')

    # Data reading and making figures
    print('\n\n  *** Data reading and making figures *** \n\n')

    data_file = open(filepath, 'rb')
    data_file.seek(1024, os.SEEK_SET)  # Jumping to 1024+number of spectra to skip byte from file beginning

    bar = IncrementalBar(' Making sum of two signals: ', max=num_of_blocks,
                         suffix='%(percent)d%%')

    for block in range(num_of_blocks+1):   # Main loop by blocks of data

        bar.next()

        # currentTime = time.strftime("%H:%M:%S")
        # print(' * Data block # ', block + 1, ' of ', num_of_blocks + 1, '  started at: ', currentTime)

        # Reading the last block which is less then 3 periods
        if block == num_of_blocks:
            spectra_to_read = spectra_in_file - num_of_blocks * spectra_to_read

        # Reading and preparing block of data (3 periods)
        data = np.fromfile(data_file, dtype=np.float64, count = spectra_to_read * len(frequency))
        data = np.reshape(data, [len(frequency), spectra_to_read], order='F')
        data = 10*np.log10(data)
        if normalize_response > 0:
            Normalization_dB(data.transpose(), len(frequency), spectra_to_read)

        # Preparing single averaged data profile for figure
        profile = data.mean(axis=0)[:]
        profile = profile - np.mean(profile)
        data = data - np.mean(data)

        # Time line
        fig_time_scale = timeline[block * spectra_to_read : (block+1) * spectra_to_read]

        # Making result picture
        fig = plt.figure(figsize = (9.2, 4.5))
        rc('font', size=5, weight='bold')
        ax1 = fig.add_subplot(211)
        ax1.plot(profile, color =u'#1f77b4', linestyle = '-', alpha=1.0, linewidth = '0.60', label = '3 pulses time profile')
        ax1.legend(loc = 'upper right', fontsize = 5)
        ax1.grid(b = True, which = 'both', color = 'silver', linewidth = '0.50', linestyle = '-')
        ax1.axis([0, len(profile), profile_pic_min, profile_pic_max])
        ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax1.set_title('File: '+ filename + '  Description: ' + df_description + '  Resolution: '+
                      str(np.round(df/1000, 3))+' kHz and '+str(np.round(time_resolution*1000,3))+' ms.',
                      fontsize = 5, fontweight='bold')
        ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        ax2 = fig.add_subplot(212)
        ax2.imshow(np.flipud(data), aspect='auto', cmap=colormap, vmin = spectrum_pic_min, vmax = spectrum_pic_max, extent=[0,len(profile),frequency[0],frequency[-1]])
        ax2.set_xlabel('Time UTC (at the lowest frequency), HH:MM:SS.ms', fontsize=6, fontweight='bold')
        ax2.set_ylabel('Frequency, MHz', fontsize=6, fontweight='bold')
        text = ax2.get_xticks().tolist()
        for i in range(len(text)-1):
            k = int(text[i])
            text[i] = fig_time_scale[k][11:23]
        ax2.set_xticklabels(text, fontsize = 5, fontweight = 'bold')
        fig.subplots_adjust(hspace=0.05, top=0.91)
        fig.suptitle('Single pulses of '+pulsar_name+' (DM: '+str(DM)+r' $\mathrm{pc \cdot cm^{-3}}$'+', Period: '+
                     str(p_bar) + ' s.), fig. ' + str(block + 1) + ' of ' + str(num_of_blocks+1),
                     fontsize = 7, fontweight='bold')
        fig.text(0.80, 0.04, 'Processed '+currentDate+ ' at '+currentTime, fontsize=3, transform=plt.gcf().transFigure)
        fig.text(0.09, 0.04, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=3, transform=plt.gcf().transFigure)
        pylab.savefig(result_path + '/'+ filename + ' fig. ' +str(block+1)+ ' - Combined picture.png', bbox_inches = 'tight', dpi = customDPI)
        plt.close('all')

    bar.finish()
    data_file.close()



def cut_needed_pulsar_period_from_dat(common_path, filename, pulsar_name, period_number, profile_pic_min,
                                      profile_pic_max, spectrum_pic_min, spectrum_pic_max, periods_per_fig, customDPI,
                                      colormap):

    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")

    # Creating a folder where all pictures and results will be stored (if it doesn't exist)
    result_path = "RESULTS_pulsar_extracted_pulse_" + filename
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    # Taking pulsar period from catalogue
    pulsar_ra, pulsar_dec, DM, p_bar = catalogue_pulsar(pulsar_name)

    # DAT file to be analyzed:
    filepath = common_path + filename

    # Timeline file to be analyzed:
    timeline_filepath = common_path + filename.split('_Data_')[0] + '_Timeline.txt'

    # Opening DAT datafile
    file = open(filepath, 'rb')

    # Data file header read
    df_filesize = os.stat(filepath).st_size                       # Size of file
    df_filepath = file.read(32).decode('utf-8').rstrip('\x00')      # Initial data file name
    file.close()

    if df_filepath[-4:] == '.adr':

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description,
                CLCfrq, df_creation_timeUTC, ReceiverMode, Mode, sumDifMode,
                NAvr, time_resolution, fmin, fmax, df, frequency, FFTsize, SLine,
                Width, BlockSize] = FileHeaderReaderADR(filepath, 0, 0)

        freq_points_num = len(frequency)

    if df_filepath[-4:] == '.jds':     # If data obtained from DSPZ receiver

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description,
                CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr, time_resolution, fmin, fmax,
                df, frequency, freq_points_num, dataBlockSize] = FileHeaderReaderJDS(filepath, 0, 0)

    # ************************************************************************************
    #                             R E A D I N G   D A T A                                *
    # ************************************************************************************

    # Time line file reading
    timeline, dt_timeline = time_line_file_reader(timeline_filepath)

    # Calculation of the dimensions of arrays to read taking into account the pulsar period
    spectra_in_file = int((df_filesize - 1024) / (8 * freq_points_num))    # int(df_filesize - 1024)/(2*4*freq_points_num)
    spectra_to_read = int(np.round((periods_per_fig * p_bar / time_resolution), 0))
    spectra_per_period = int(np.round((p_bar / time_resolution), 0))
    num_of_blocks = int(np.floor(spectra_in_file / spectra_to_read))

    print(' Pulsar name:                             ', pulsar_name, '')
    print(' Pulsar period:                           ', p_bar, 's.')
    print(' Time resolution:                         ', time_resolution, 's.')
    print(' Number of spectra to read in', periods_per_fig, 'periods:  ', spectra_to_read, ' ')
    print(' Number of spectra in file:               ', spectra_in_file, ' ')
    print(' Number of', periods_per_fig, 'periods blocks in file:      ', num_of_blocks, '\n')

    # Data reading and making figures
    print('\n  *** Data reading and making figure *** \n')

    data_file = open(filepath, 'rb')
    # Jumping to 1024+number of spectra to skip bytes from file beginning
    data_file.seek(1024 + (period_number-1) * spectra_per_period * len(frequency) * 8, os.SEEK_SET)

    # Reading and preparing block of data (3 periods)
    data = np.fromfile(data_file, dtype=np.float64, count=spectra_to_read * len(frequency))
    data_file.close()
    data = np.reshape(data, [len(frequency), spectra_to_read], order='F')
    data = 10 * np.log10(data)

    # Preparing single averaged data profile for figure
    profile = data.mean(axis=0)[:]
    profile = profile - np.mean(profile)
    data = data - np.mean(data)

    single_pulse_txt = open(result_path + '/' + filename + ' - Extracted pulse.txt', "w")
    for freq in range(len(frequency) - 1):
        #single_pulse_txt.write(' '.join(format(data[freq, i], "12.7e") for i in range(spectra_to_read)) + ' \n')
        single_pulse_txt.write(' '.join('  {:+12.7E}'.format(data[freq, i]) for i in range(spectra_to_read)) + ' \n')

    single_pulse_txt.close()

    # Time line
    fig_time_scale = timeline[(period_number-1) * spectra_per_period : (period_number - 1 + spectra_to_read) * spectra_per_period]

    # Making result picture
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')
    ax2 = fig.add_subplot(111)
    ax2.set_title('File: ' + filename + '  Description: ' + df_description + '  Resolution: ' +
                  str(np.round(df/1000, 3)) + ' kHz and '+str(np.round(time_resolution*1000, 3))+' ms.',
                  fontsize=5, fontweight='bold')
    ax2.imshow(np.flipud(data), aspect='auto', cmap=colormap, vmin=spectrum_pic_min, vmax=spectrum_pic_max,
               extent=[0, len(profile), frequency[0], frequency[-1]])
    ax2.set_xlabel('Time UTC (at the lowest frequency), HH:MM:SS.ms', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Frequency, MHz', fontsize=6, fontweight='bold')
    text = ax2.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = fig_time_scale[k][11:23]
    ax2.set_xticklabels(text, fontsize = 5, fontweight = 'bold')
    fig.subplots_adjust(hspace=0.05, top=0.91)
    fig.suptitle('Extracted single pulse of '+pulsar_name+' (DM: '+str(DM)+r' $\mathrm{pc \cdot cm^{-3}}$'+', Period: '+
                 str(p_bar) + ' s.)', fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + currentDate + ' at '+currentTime, fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig(result_path + '/' + filename + ' - Extracted pulse.png', bbox_inches='tight', dpi=customDPI)
    plt.close('all')

    return 0


def incoherent_sum_of_single_pulses_spectra(common_path, filename_1, filename_2):
    '''
    Function takes two 2D txt files with matrices and adds the matrices, makes another txt file and a figure
    '''

    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")

    file = open(common_path + filename_1, 'r')
    array_1 = np.array([[float(digit) for digit in line.split()] for line in file])
    file.close()

    file = open(common_path + filename_2, 'r')
    array_2 = np.array([[float(digit) for digit in line.split()] for line in file])
    file.close()

    print('  Shape of first array: ', array_1.shape)
    print('  Shape of second array:', array_2.shape)
    if array_1.shape != array_2.shape:
        sys.exit('\n\n   Error!!! Arrays have different shapes!\n\n      Program stopped!')

    result_array = array_1 + array_2
    print('  Shape of result array:', result_array.shape)
    del array_1, array_2

    single_pulse_txt = open('Incoherent sum of extracted pulses.txt', "w")
    for freq in range(result_array.shape[0] - 1):
        single_pulse_txt.write(' '.join('  {:+12.7E}'.format(result_array[freq, i]) for i in range(result_array.shape[1])) + ' \n')
    single_pulse_txt.close()

    # Making result picture
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')
    ax2 = fig.add_subplot(111)
    ax2.set_title(filename_1 + ' + ' + filename_2, fontsize=5, fontweight='bold')
    ax2.imshow(np.flipud(result_array), aspect='auto', cmap=colormap, vmin=spectrum_pic_min, vmax=spectrum_pic_max)
    ax2.set_xlabel('Time points', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
    fig.subplots_adjust(hspace=0.05, top=0.91)
    fig.suptitle('Sum of two matrices', fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + currentDate + ' at '+currentTime, fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig('Incoherent sum of extracted pulses.png', bbox_inches='tight', dpi=customDPI)
    plt.close('all')

    return 0



def cut_needed_time_points_from_dat(filename, start_point, end_point):

    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")

    file = open(filename, 'r')
    array = np.array([[float(digit) for digit in line.split()] for line in file])
    file.close()

    print('  Shape of the array: ', array.shape)

    result_array = array[:, start_point : end_point]
    del array

    print('  Shape of result array:', result_array.shape)

    single_pulse_txt = open('Incoherent sum of extracted pulses_selected_points.txt', "w")
    for freq in range(result_array.shape[0] - 1):
        single_pulse_txt.write(' '.join('  {:+12.7E}'.format(result_array[freq, i]) for i in range(result_array.shape[1])) + ' \n')
    single_pulse_txt.close()

    # Making result picture
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')
    ax2 = fig.add_subplot(111)
    ax2.set_title('Cut time points: ' + str(start_point) + ' - ' + str(end_point), fontsize=5, fontweight='bold')
    ax2.imshow(np.flipud(result_array), aspect='auto', cmap=colormap, vmin=spectrum_pic_min, vmax=spectrum_pic_max)
    ax2.set_xlabel('Time points', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
    fig.subplots_adjust(hspace=0.05, top=0.91)
    fig.suptitle('Sum of two matrices', fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + currentDate + ' at '+currentTime, fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: '+Software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig('Incoherent sum of extracted pulses_selected_points.png', bbox_inches='tight', dpi=customDPI)
    plt.close('all')

    return 0



# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    print ('\n\n\n\n\n\n\n\n   *****************************************************************')
    print('   *    ', Software_name, ' v.', Software_version,'    *      (c) YeS 2020')
    print('   ***************************************************************** \n\n\n')

    startTime = time.time()
    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")
    print ('  Today is ', currentDate, ' time is ', currentTime, ' \n')

    '''
    pulsar_period_DM_compensated_pics(common_path, filename, pulsar_name, normalize_response, profile_pic_min,
                                      profile_pic_max, spectrum_pic_min, spectrum_pic_max, periods_per_fig, customDPI,
                                      colormap)
    
    
    filename = 'Norm_DM_0.972_DM_1.0_DM_1.0_E310120_225419.jds_Data_chA.dat'
    period_number = 23
    periods_per_fig = 1
    cut_needed_pulsar_period_from_dat(common_path, filename, pulsar_name, period_number, profile_pic_min,
                                      profile_pic_max, spectrum_pic_min, spectrum_pic_max, periods_per_fig, customDPI,
                                      colormap)
    
    
    common_path = 'RESULTS_pulsar_extracted_pulse_Norm_DM_0.972_DM_1.0_DM_1.0_E310120_225419.jds/'
    filename_1 = 'Norm_DM_0.972_DM_1.0_DM_1.0_E310120_225419.jds_Data_chA.dat - Extracted pulse.txt'
    filename_2 = 'Norm_DM_0.972_DM_1.0_DM_1.0_E310120_225419.jds_Data_chB.dat - Extracted pulse.txt'
    incoherent_sum_of_single_pulses_spectra(common_path, filename_1, filename_2)
    '''

    common_path = 'RESULTS_pulsar_extracted_pulse_Norm_DM_0.972_DM_1.0_DM_1.0_E310120_225419.jds/'
    filename = 'Incoherent sum of extracted pulses.txt'
    cut_needed_time_points_from_dat(common_path+filename, 420, 540)


    endTime = time.time()    # Time of calculations

    print('\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                    round((endTime - startTime)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
