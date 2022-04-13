# TODO:  https://www.geeksforgeeks.org/how-to-resample-numpy-array-representing-an-image/

Software_version = '2022.04.11'
Software_name = 'Pulsar dynamic spectra folding'
# Program intended to read and show pulsar data from DAT files (with compensated DM delay)

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Path to data files
common_path = ''  # '/media/data/PYTHON/ra_data_processing-all/' #

# Directory of DAT file to be analyzed:
filename = 'B0809+74_DM_5.755_E300117_180000.jds_Data_chA.dat'

pulsar_name = 'B0809+74'  # 'J2325-0530' # 'B0950+08'
normalize_response = 0            # Normalize (1) or not (0) the frequency response
profile_pic_min = -0.1            # Minimum limit of profile picture
profile_pic_max = 1.20            # Maximum limit of profile picture
spectrum_pic_min = -0.5           # Minimum limit of dynamic spectrum picture
spectrum_pic_max = 3              # Maximum limit of dynamic spectrum picture

periods_per_fig = 1
integrated_pulses = 30  # 230 / 3
roll_count = 8000

scale_factor = 100
customDPI = 500                   # Resolution of images of dynamic spectra
colormap = 'Greys'                # Colormap of images of dynamic spectra ('jet' or 'Greys')

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import os
import sys
import numpy as np
import time
import pylab
import matplotlib.pyplot as plt
from os import path
from matplotlib import rc
import matplotlib
matplotlib.use('agg')
import matplotlib.ticker as mticker   # <---- Added to suppress warning

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_ra_data_processing.spectra_normalization import Normalization_dB

# ###############################################################################
# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************


def pulsar_period_folding(common_path, filename, pulsar_name, normalize_response, profile_pic_min, profile_pic_max,
                          spectrum_pic_min, spectrum_pic_max, periods_per_fig, customDPI, colormap):

    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")

    # Taking pulsar period from catalogue
    pulsar_ra, pulsar_dec, DM, p_bar = catalogue_pulsar(pulsar_name)

    # DAT file to be analyzed:
    filepath = common_path + filename

    # Timeline file to be analyzed:
    # timeline_filepath = common_path + filename.split('_Data_')[0] + '_Timeline.txt'

    # Opening DAT datafile
    file = open(filepath, 'rb')

    # Data file header read
    df_filesize = os.stat(filepath).st_size                         # Size of file
    df_filepath = file.read(32).decode('utf-8').rstrip('\x00')      # Initial data file name
    file.close()

    if df_filepath[-4:] == '.adr':

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description, CLCfrq, df_creation_timeUTC,
                ReceiverMode, Mode, sumDifMode,  NAvr, time_resolution, fmin, fmax, df, frequency, FFTsize, SLine,
                Width, BlockSize] = FileHeaderReaderADR(filepath, 0, 0)

        freq_points_num = len(frequency)

    if df_filepath[-4:] == '.jds':     # If data obtained from DSPZ receiver

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description, CLCfrq, df_creation_timeUTC,
                SpInFile, ReceiverMode, Mode, Navr, time_resolution, fmin, fmax, df, frequency, freq_points_num,
                dataBlockSize] = FileHeaderReaderJDS(filepath, 0, 1)

    # ************************************************************************************
    #                             R E A D I N G   D A T A                                *
    # ************************************************************************************

    # Time line file reading
    # timeline, dt_timeline = time_line_file_reader(timeline_filepath)

    # Calculation of the dimensions of arrays to read taking into account the pulsar period
    spectra_in_file = int((df_filesize - 1024) / (8 * freq_points_num))

    data_file = open(filepath, 'rb')
    data_file.seek(1024, os.SEEK_SET)  # Jumping to 1024+number of spectra to skip byte from file beginning

    # Make a buffer for initial time resolution
    # Make a buffer for enhanced time resolution

    # Read some number of spectra
    # Enhance resolution
    # Find how many full pulsar periods it covers
    # Integrate the integer number of periods and delete this data from buffer
    # Repeat

    interp_spectra_in_period = int(np.round((periods_per_fig * p_bar / (time_resolution / scale_factor)), 0))

    data_interp = np.zeros([len(frequency), 0])
    integrated_spectra = np.zeros([len(frequency), interp_spectra_in_period])
    spectra_to_read = 500

    for bunch in range(50):

        data_raw = np.fromfile(data_file, dtype=np.float64, count=spectra_to_read * len(frequency))
        data_raw = np.reshape(data_raw, [len(frequency), spectra_to_read], order='F')
        data_raw = 10 * np.log10(data_raw)
        if normalize_response > 0:
            Normalization_dB(data_raw.transpose(), len(frequency), spectra_to_read)

        # Append the new interpolated (np.kron) data to buffer
        data_interp = np.append(data_interp, np.kron(data_raw, np.ones((1, scale_factor))), axis=1)

        periods_in_bunch = data_interp.shape[1] // interp_spectra_in_period

        for i in range(periods_in_bunch):
            integrated_spectra = integrated_spectra + \
                                 data_interp[:, i * interp_spectra_in_period: (i+1) * interp_spectra_in_period]

        data_interp = data_interp[:, interp_spectra_in_period * periods_in_bunch:]

    block = 3

    # Preparing single averaged data profile for figure
    integrated_spectra = np.roll(integrated_spectra, roll_count, axis=1)
    profile = integrated_spectra.mean(axis=0)[:]
    profile = profile - np.mean(profile)
    profile = profile / np.max(profile)
    data = integrated_spectra - np.mean(integrated_spectra)


    # spectra_to_read = int(np.round((periods_per_fig * p_bar / time_resolution), 0))
    # num_of_blocks = int(np.floor(spectra_in_file / spectra_to_read))
    #
    # print('   Pulsar period:                           ', p_bar, 's.')
    # print('   Time resolution:                         ', time_resolution, 's.')
    # print('   Number of spectra to read in', periods_per_fig, 'periods:  ', spectra_to_read, ' ')
    # print('   Number of spectra in file:               ', spectra_in_file, ' ')
    # print('   Number of', periods_per_fig, 'periods blocks in file:      ', num_of_blocks, '\n')
    #
    # # Data reading and making figures
    # print('\n\n  *** Data reading and making figures *** \n\n')
    #
    # data_file = open(filepath, 'rb')
    # data_file.seek(1024, os.SEEK_SET)  # Jumping to 1024+number of spectra to skip byte from file beginning
    #
    # data_cumulative = np.zeros([len(frequency), spectra_to_read])
    #
    # for block in range(integrated_pulses):   # Main loop by blocks of data
    #
    #     # Reading the last block which is less than n periods
    #     if block == num_of_blocks:
    #         spectra_to_read = spectra_in_file - num_of_blocks * spectra_to_read
    #
    #     # Reading and preparing block of data (n periods)
    #     data = np.fromfile(data_file, dtype=np.float64, count=spectra_to_read * len(frequency))
    #     data = np.reshape(data, [len(frequency), spectra_to_read], order='F')
    #     data = 10 * np.log10(data)
    #     if normalize_response > 0:
    #         Normalization_dB(data.transpose(), len(frequency), spectra_to_read)
    #
    #     data_cumulative += data
    #
    # # Preparing single averaged data profile for figure
    # profile = data_cumulative.mean(axis=0)[:]
    # profile = profile - np.mean(profile)
    # data = data_cumulative - np.mean(data_cumulative)

    # Making result picture
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')

    ax1 = fig.add_subplot(211)
    ax1.plot(profile, color=u'#1f77b4', linestyle='-', alpha=1.0, linewidth='0.60',
             label='Pulses integrated time profile')
    ax1.legend(loc='upper right', fontsize=5)
    ax1.axis([0, len(profile), profile_pic_min, profile_pic_max])
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title('File: ' + filename + '  Description: ' + df_description + '  Resolution: ' +
                  str(np.round(df/1000, 3)) + ' kHz and ' + str(np.round(time_resolution*1000, 3)) + ' ms.',
                  fontsize=5, fontweight='bold')

    # Grid lines parameters
    major_ticks_top = np.linspace(0, len(profile), periods_per_fig+1)
    minor_ticks_top = np.linspace(0, len(profile), (4 * periods_per_fig+1))
    ax1.set_xticks([])
    ax1.yaxis.grid(visible=True, which='major', color='silver', linewidth='0.30', linestyle='--')  # Major y
    ax1.yaxis.grid(visible=True, which='minor', color='silver', linewidth='0.30', linestyle='--')  # Minor all

    ax1up = ax1.twiny()
    ax1up.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax1up.set_xticks(major_ticks_top)
    ax1up.set_xticks(minor_ticks_top, minor=True)

    ax1up.xaxis.grid(visible=True, which='major', color='gray', linewidth='0.50', linestyle='-')  # Major x
    ax1up.xaxis.grid(visible=True, which='minor', color='silver', linewidth='0.30', linestyle='--')  # Minor all

    ax2 = fig.add_subplot(212)
    ax2.imshow(np.flipud(data), aspect='auto', cmap=colormap, vmin=spectrum_pic_min, vmax=spectrum_pic_max,
               extent=[0, periods_per_fig, frequency[0], frequency[-1]])
    ax2.set_xlabel('Pulsar period phase', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Frequency, MHz', fontsize=6, fontweight='bold')

    major_ticks_bottom = np.linspace(0, periods_per_fig, 4 * periods_per_fig+1)
    ax2.set_xticks(major_ticks_bottom)

    fig.subplots_adjust(hspace=0.05, top=0.86)  # 91

    fig.suptitle('Folded average pulses of ' + pulsar_name + ' (DM: ' + str(DM) + r' $\mathrm{pc \cdot cm^{-3}}$' +
                 ', Period: ' + str(p_bar) + ' s.), ' + str(block + 1) + ' integrated pulses ',
                 fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: ' + Software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig(filename + ' - folded pulses.png',
                  bbox_inches='tight', dpi=customDPI)
    plt.close('all')

    data_file.close()

    return


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    pulsar_period_folding(common_path, filename, pulsar_name, normalize_response, profile_pic_min, profile_pic_max,
                          spectrum_pic_min, spectrum_pic_max, periods_per_fig, customDPI, colormap)
