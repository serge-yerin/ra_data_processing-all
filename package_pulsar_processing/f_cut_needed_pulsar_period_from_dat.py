
import os
import sys
import numpy as np
import time
import pylab
import matplotlib.pyplot as plt
from os import path
from matplotlib import rc


# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader


def cut_needed_pulsar_period_from_dat(common_path, filename, pulsar_name, period_number, profile_pic_min,
                                      profile_pic_max, spectrum_pic_min, spectrum_pic_max, periods_per_fig, customDPI,
                                      colormap):
    """
    Function to find and cut the selected pulsar period (by its number) from the DAT files
    """
    
    software_version = '2021.01.25'

    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")

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
    df_filepath = file.read(32).decode('utf-8').rstrip('\x00')    # Initial data file name
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
    spectra_in_file = int((df_filesize - 1024) / (8 * freq_points_num))  # int(df_filesize - 1024)/(2*4*freq_points_num)
    spectra_to_read = int(np.round((periods_per_fig * p_bar / time_resolution), 0))
    spectra_per_period = int(np.round((p_bar / time_resolution), 0))
    num_of_blocks = int(np.floor(spectra_in_file / spectra_to_read))

    print('\n   Pulsar name:                             ', pulsar_name, '')
    print('   Pulsar period:                           ', p_bar, 's.')
    print('   Time resolution:                         ', time_resolution, 's.')
    print('   Number of spectra to read in', periods_per_fig, 'periods:  ', spectra_to_read, ' ')
    print('   Number of spectra in file:               ', spectra_in_file, ' ')
    print('   Number of', periods_per_fig, 'periods blocks in file:      ', num_of_blocks, '\n')

    # Data reading and making figures
    print('\n   Data reading and making figure...')

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
        single_pulse_txt.write(' '.join('  {:+12.7E}'.format(data[freq, i]) for i in range(spectra_to_read)) + ' \n')

    single_pulse_txt.close()

    # Time line
    fig_time_scale = timeline[(period_number-1) *
                              spectra_per_period: (period_number - 1 + spectra_to_read) * spectra_per_period]

    # Making result picture
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')
    ax2 = fig.add_subplot(111)
    ax2.set_title('File: ' + filename + '  Description: ' + df_description + '  Resolution: ' +
                  str(np.round(df/1000, 3)) + ' kHz and '+str(np.round(time_resolution*1000, 3))+' ms.',
                  fontsize=5, fontweight='bold')
    ax2.imshow(np.flipud(data), aspect='auto', cmap=colormap, vmin=spectrum_pic_min, vmax=spectrum_pic_max,
               extent=[0, len(profile), frequency[0] + 16.5, frequency[-1] + 16.5])   # <----------- added line
    ax2.set_xlabel('Time UTC (at the lowest frequency), HH:MM:SS.ms', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Frequency, MHz', fontsize=6, fontweight='bold')
    text = ax2.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = fig_time_scale[k][11:23]
    ax2.set_xticklabels(text, fontsize=5, fontweight='bold')
    fig.subplots_adjust(hspace=0.05, top=0.91)
    fig.suptitle('Extracted single pulse of ' + pulsar_name + ' (DM: ' + str(DM) + r' $\mathrm{pc \cdot cm^{-3}}$' +
                 ', Period: ' + str(p_bar) + ' s.)', fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + current_date + ' at '+current_time, fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: '+software_version+', yerin.serge@gmail.com, IRA NASU',
             fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig(result_path + '/' + filename + ' - Extracted pulse.png', bbox_inches='tight', dpi=customDPI)
    plt.close('all')

    # Copy data file header to a small file to save info on observations in the result directory

    # Read data file header
    with open(filepath, 'rb') as file:
        file_header = file.read(1024)

    # Create a small binary file with header
    file_data = open(result_path + '/' + filename, 'wb')
    file_data.write(file_header)
    file_data.close()
    del file_header

    return result_path, filename + ' - Extracted pulse.txt', filename + ' - Extracted pulse.png'


'''

# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':
    
    
    
    cut_needed_pulsar_period_from_dat(common_path, filename, pulsar_name, period_number, profile_pic_min,
                                      profile_pic_max, spectrum_pic_min, spectrum_pic_max, periods_per_fig, customDPI,
                                      colormap)
'''