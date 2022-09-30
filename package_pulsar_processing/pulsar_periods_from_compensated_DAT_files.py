# Python3
software_version = '2020.03.19'
software_name = 'Pulsar DM delay compensated DAT reader'
# Program intended to read and show pulsar data from DAT files (with compensated DM delay)
# Make figures overlap by one pulse!!!

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Path to data files
results_path = ''  # '/media/data/PYTHON/ra_data_processing-all/' #

# Directory of DAT file to be analyzed:
dat_file_path = 'Norm_DM_0.972_DM_1.0_DM_1.0_E310120_225419.jds_Data_wfA+B.dat'

pulsar_name = 'B0809+74'  # 'B0950+08'
normalize_response = 0            # Normalize (1) or not (0) the frequency response
profile_pic_min = -0.15           # Minimum limit of profile picture
profile_pic_max = 0.55            # Maximum limit of profile picture
spectrum_pic_min = -0.2           # Minimum limit of dynamic spectrum picture
spectrum_pic_max = 3              # Maximum limit of dynamic spectrum picture

periods_per_fig = 3

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
import matplotlib.ticker as mticker   # <---- Added to suppress warning
from progress.bar import IncrementalBar
import matplotlib
matplotlib.use('agg')

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_ra_data_files_formats.read_file_header_adr import FileHeaderReaderADR
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_ra_data_processing.f_spectra_normalization import normalization_db

# ###############################################################################
# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************


def pulsar_period_dm_compensated_pics(results_path, dat_file_path, pulsar_name, normalize_response, profile_pic_min,
                                      profile_pic_max, spectrum_pic_min, spectrum_pic_max, periods_per_fig, customDPI,
                                      colormap, save_strongest, threshold, use_mask_file=False):

    a_current_time = time.strftime("%H:%M:%S")
    a_current_date = time.strftime("%d.%m.%Y")

    # Creating a folder where all pictures and results will be stored (if it doesn't exist)
    dat_file_name = dat_file_path.split('/')[-1]
    result_path = results_path + "Pulsar_n_periods_" + dat_file_name[:-4]
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    if save_strongest:
        best_result_path = result_path + '/Strongest_pulses'
        if not os.path.exists(best_result_path):
            os.makedirs(best_result_path)

    # Taking pulsar period from catalogue
    pulsar_ra, pulsar_dec, DM, p_bar = catalogue_pulsar(pulsar_name)

    # Timeline file to be analyzed:
    # timeline_filepath = results_path + dat_file_name.split('_Data_')[0] + '_Timeline.txt'
    timeline_filepath = dat_file_path.split('_Data_')[0] + '_Timeline.txt'

    # Opening DAT datafile
    file = open(dat_file_path, 'rb')

    if use_mask_file:
        mask_file = open(dat_file_path[:-3] + 'msk', 'rb')
        mask_file.seek(1024)  # Jumping to 1024 byte from file beginning

    # Data file header read
    df_filesize = os.stat(dat_file_path).st_size                         # Size of file
    df_filepath = file.read(32).decode('utf-8').rstrip('\x00')      # Initial data file name
    file.close()

    if df_filepath[-4:] == '.adr':

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description,
                clock_frq, df_creation_time_utc, receiver_mode, mode, sum_diff_mode,
                n_avr, time_resolution, fmin, fmax, df, frequency, fft_size, sline,
                width, block_size] = FileHeaderReaderADR(dat_file_path, 0, 0)

        freq_points_num = len(frequency)

    if df_filepath[-4:] == '.jds':     # If data obtained from DSPZ receiver

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description, clock_frq,
         df_creation_time_utc, sp_in_file, receiver_mode, mode, n_avr, time_resolution, fmin, fmax,
         df, frequency, freq_points_num, data_block_size] = file_header_jds_read(dat_file_path, 0, 1)

    # ************************************************************************************
    #                             R E A D I N G   D A T A                                *
    # ************************************************************************************

    # Time line file reading
    timeline, dt_timeline = time_line_file_reader(timeline_filepath)

    # Calculation of the dimensions of arrays to read taking into account the pulsar period
    spectra_in_file = int((df_filesize - 1024) / (8 * freq_points_num))  # int(df_filesize - 1024)/(2*4*freq_points_num)
    spectra_to_read = int(np.round((periods_per_fig * p_bar / time_resolution), 0))
    num_of_blocks = int(np.floor(spectra_in_file / spectra_to_read))

    print('   Pulsar period:                           ', p_bar, 's.')
    print('   Time resolution:                         ', time_resolution, 's.')
    print('   Number of spectra to read in', periods_per_fig, 'periods:  ', spectra_to_read, ' ')
    print('   Number of spectra in file:               ', spectra_in_file, ' ')
    print('   Number of', periods_per_fig, 'periods blocks in file:      ', num_of_blocks, '\n')

    # Data reading and making figures
    print('\n\n  *** Data reading and making figures *** \n\n')

    data_file = open(dat_file_path, 'rb')
    data_file.seek(1024, os.SEEK_SET)  # Jumping to 1024+number of spectra to skip byte from file beginning

    bar = IncrementalBar('   Making pictures of n periods: ', max=num_of_blocks, suffix='%(percent)d%%')
    bar.start()

    for block in range(num_of_blocks+1):   # Main loop by blocks of data

        # Reading the last block which is less than 3 periods
        if block == num_of_blocks:
            spectra_to_read = spectra_in_file - num_of_blocks * spectra_to_read

        # Reading and preparing block of data (3 periods)
        data = np.fromfile(data_file, dtype=np.float64, count=spectra_to_read * len(frequency))
        data = np.reshape(data, [len(frequency), spectra_to_read], order='F')

        with np.errstate(divide='ignore'):
            data = 10 * np.log10(data)
        data[data == np.nan] = -135.5
        data[data == -np.inf] = -135.5

        if normalize_response > 0:
            normalization_db(data.transpose(), len(frequency), spectra_to_read)

        # Apply masking if needed
        if use_mask_file:
            # Read mask from file
            mask = np.fromfile(mask_file, dtype=bool, count=spectra_to_read * len(frequency))
            mask = np.reshape(mask, [len(frequency), spectra_to_read], order='F')
            # Apply as mask to data copy and calculate mean value without noise
            masked_data_raw = np.ma.masked_where(mask, data)
            data_raw_mean = np.mean(masked_data_raw)
            del masked_data_raw

            # Apply as mask to data (change masked data with mean values of data outside mask)
            data = data * np.invert(mask)
            data = data + mask * data_raw_mean
            add_text = ' (masked)'
        else:
            add_text = ''

        # Preparing single averaged data profile for figure
        profile = data.mean(axis=0)[:]
        profile = profile - np.mean(profile)
        data = data - np.mean(data)

        # Timeline
        fig_time_scale = timeline[block * spectra_to_read: (block+1) * spectra_to_read]

        # Making result picture
        fig = plt.figure(figsize=(9.2, 4.5))
        rc('font', size=5, weight='bold')
        ax1 = fig.add_subplot(211)
        ax1.plot(profile, color=u'#1f77b4', linestyle='-', alpha=1.0, linewidth='0.60', label='3 pulses time profile')
        ax1.legend(loc='upper right', fontsize=5)
        ax1.grid(visible=True, which='both', color='silver', linewidth='0.50', linestyle='-')
        ax1.axis([0, len(profile), profile_pic_min, profile_pic_max])
        ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax1.set_title('File: ' + dat_file_name + '  Description: ' + df_description + '  Resolution: ' +
                      str(np.round(df/1000, 3)) + ' kHz and ' + str(np.round(time_resolution*1000, 3)) + ' ms' +
                      add_text, fontsize=5, fontweight='bold')
        ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        ax2 = fig.add_subplot(212)
        ax2.imshow(np.flipud(data), aspect='auto', cmap=colormap, vmin=spectrum_pic_min, vmax=spectrum_pic_max,
                   extent=[0, len(profile), frequency[0], frequency[-1]])
        ax2.set_xlabel('Time UTC (at the lowest frequency), HH:MM:SS.ms', fontsize=6, fontweight='bold')
        ax2.set_ylabel('Frequency, MHz', fontsize=6, fontweight='bold')
        text = ax2.get_xticks().tolist()
        for i in range(len(text)-1):
            k = int(text[i])
            text[i] = fig_time_scale[k][11:23]

        ticks_loc = ax2.get_xticks().tolist()                           # <---- Added to suppress warning
        ax2.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))         # <---- Added to suppress warning

        ax2.set_xticklabels(text, fontsize=5, fontweight='bold')
        fig.subplots_adjust(hspace=0.05, top=0.91)
        fig.suptitle('Single pulses of ' + pulsar_name + ' (DM: ' + str(DM) + r' $\mathrm{pc \cdot cm^{-3}}$' +
                     ', Period: ' + str(p_bar) + ' s.), fig. ' + str(block + 1) + ' of ' + str(num_of_blocks+1),
                     fontsize=7, fontweight='bold')
        fig.text(0.80, 0.04, 'Processed ' + a_current_date + ' at ' + a_current_time,
                 fontsize=3, transform=plt.gcf().transFigure)
        fig.text(0.09, 0.04, 'Software version: ' + software_version+', yerin.serge@gmail.com, IRA NASU',
                 fontsize=3, transform=plt.gcf().transFigure)
        pylab.savefig(result_path + '/' + dat_file_name[:-4] + ' fig. ' + str(block+1) + '.png',
                      bbox_inches='tight', dpi=customDPI)

        # If the profile has points above threshold save picture also into separate folder
        if save_strongest and np.max(profile) > threshold:
            pylab.savefig(best_result_path + '/' + dat_file_name[:-4] + ' fig. ' + str(block + 1) +
                          ' - Combined picture.png',
                          bbox_inches='tight', dpi=customDPI)
        plt.close('all')

        bar.next()

    bar.finish()
    data_file.close()
    if use_mask_file:
        mask_file.close()


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    pulsar_period_dm_compensated_pics(results_path, dat_file_path, pulsar_name, normalize_response, profile_pic_min,
                                      profile_pic_max, spectrum_pic_min, spectrum_pic_max, periods_per_fig, customDPI,
                                      colormap, True, 0.25, use_mask_file=True)
