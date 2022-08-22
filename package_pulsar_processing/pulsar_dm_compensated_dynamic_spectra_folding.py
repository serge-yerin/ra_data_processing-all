Software_version = '2022.05.10'
Software_name = 'Pulsar dynamic spectra folding'
# Program intended to integrate (fold) average pulse profile from DAT files of pulsar data (with compensated DM delay)

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
# Path to folder with the data file
common_path = ''  # Empty string means the project directory

# File name of DAT file to be analyzed:
filename = 'B0809+74_DM_5.755_E300117_180000.jds_Data_chA.dat'

pulsar_name = 'B0809+74'  # 'J2325-0530' # 'B0950+08'

use_mask_file = True
periods_per_fig = 1               # Periods of pulsar to show in the figure
spectra_to_read = 500             # Spectra to read in one bunch (depends on RAM)

spectrum_pic_min = -0.5           # Minimum limit of dynamic spectrum picture
spectrum_pic_max = 3              # Maximum limit of dynamic spectrum picture

scale_factor = 10                 # Scale factor to interpolate data (depends on RAM, use 1, 10, 30)
custom_dpi = 500                  # Resolution of images of dynamic spectra
colormap = 'Greys'                # Colormap of images of dynamic spectra ('jet' or 'Greys')

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import os
import sys
import numpy as np
import numpy.ma as ma
import time
import pylab
import matplotlib.pyplot as plt
from os import path
from matplotlib import rc
from progress.bar import IncrementalBar
import matplotlib

matplotlib.use('TkAgg')

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_ra_data_processing.f_spectra_normalization import normalization_db
# ###############################################################################


def save_integrated_pulse_to_file(array, file_header, pulsar_period, samples_per_period, file_name):
    """
    Saving .smd file with integrated pulsar pulse in a format by V. V. Zakharenko (IDL)
    """
    integrated_pulse_file = open(file_name, 'wb')
    array = np.array(array, dtype=np.float32)
    integrated_pulse_file.write(np.float64(pulsar_period))
    integrated_pulse_file.write(np.int32(samples_per_period))
    integrated_pulse_file.write(np.transpose(array).copy(order='C'))
    integrated_pulse_file.write(file_header)
    integrated_pulse_file.close()
    return 0


def make_figure_of_pulse_profile_and_spectra(profile, data, frequency, profile_pic_min, profile_pic_max,
                                             spectrum_pic_min, spectrum_pic_max,  periods_per_fig,
                                             fig_suptitle, fig_title, pic_filename, current_date, current_time,
                                             custom_dpi, colormap, show=False, save=True):
    """Displays and/or saves picture with integrated profile and dynamic spectrum of average pulse"""
    # Making result picture
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')

    ax1 = fig.add_subplot(211)
    ax1.plot(profile, color=u'#1f77b4', linestyle='-', alpha=1.0, linewidth='0.60',
             label='Pulses integrated time profile')
    ax1.legend(loc='upper right', fontsize=5)
    ax1.axis([0, len(profile), profile_pic_min, profile_pic_max])
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title(fig_title, fontsize=5, fontweight='bold')

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

    fig.subplots_adjust(hspace=0.05, top=0.86)
    fig.suptitle(fig_suptitle, fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: ' + Software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=3, transform=plt.gcf().transFigure)
    if save:
        pylab.savefig(pic_filename, bbox_inches='tight', dpi=custom_dpi)
    if show:
        plt.show()
    plt.close('all')
    return 0


# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************


def pulsar_period_folding(common_path, filename, pulsar_name, scale_factor, spectrum_pic_min, spectrum_pic_max,
                          periods_per_fig, custom_dpi, colormap, use_mask_file=False):

    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")

    # Taking pulsar period from catalogue
    pulsar_ra, pulsar_dec, pulsar_dm, p_bar = catalogue_pulsar(pulsar_name)

    print('\n * Data file name: ', filename)

    # DAT datafile to be analyzed:
    filepath = common_path + filename

    # Timeline file to be analyzed:
    timeline_filepath = common_path + filename.split('_Data_')[0] + '_Timeline.txt'

    # Opening DAT datafile
    file = open(filepath, 'rb')

    # Data file header read
    df_filepath = file.read(32).decode('utf-8').rstrip('\x00')      # Initial data file name
    file.close()

    if df_filepath[-4:] == '.adr':

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description, clock_frq, df_creation_time_utc,
                receiver_mode, mode, sum_diff_mode,  n_avr, time_resolution, fmin, fmax, df, frequency, fft_size, sline,
                width, block_size] = FileHeaderReaderADR(filepath, 0, 0)

        freq_points_num = len(frequency)

    elif df_filepath[-4:] == '.jds':     # If data obtained from DSPZ receiver

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description, clock_frq, df_creation_time_utc,
                sp_in_file, receiver_mode, mode, n_avr, time_resolution, fmin, fmax, df, frequency, freq_points_num,
                block_size] = FileHeaderReaderJDS(filepath, 0, 1)
    else:
        sys.exit(' Error! File type is unknown')

    # ************************************************************************************
    #                             R E A D I N G   D A T A                                *
    # ************************************************************************************

    # Timeline file reading
    timeline, dt_timeline = time_line_file_reader(timeline_filepath)
    del dt_timeline

    # Calculation of the dimensions of arrays to read taking into account the pulsar period
    spectra_in_file = int((df_filesize - 1024) / (8 * freq_points_num))
    bunches_in_file = spectra_in_file // spectra_to_read
    print(' Spectra in file:                    ', spectra_in_file)
    print(' Bunches in file:                    ', bunches_in_file)
    print(' Periods per figure:                 ', periods_per_fig)
    print(' Using mask for cleaning:            ', use_mask_file)

    # Open data file with removed dispersion delay (.dat)
    data_file = open(filepath, 'rb')
    file_header = data_file.read(1024)
    data_file.seek(1024, os.SEEK_SET)  # Jumping to 1024 byte from file beginning to skip header

    if use_mask_file:
        mask_file = open(filepath[:-3] + 'msk', 'rb')
        mask_file.seek(1024)  # Jumping to 1024 byte from file beginning

    # Time resolution of interpolated data
    interp_time_resolution = time_resolution / scale_factor

    interp_spectra_in_profile = int(periods_per_fig * p_bar / interp_time_resolution)
    # Keep in mind that 2 arises here because the time resolution is valid for each second sample, and other samples
    # are obtained with overlap of wf samples to calculate fft

    # Calculation of remainder of the pulsar period when divided by interpolated time resolution
    remainder_of_n_periods = (periods_per_fig * p_bar) - (interp_time_resolution * interp_spectra_in_profile)
    if remainder_of_n_periods < 0:
        sys.exit('Error! Remainder is less then zero! ')

    print(' Scale factor:                       ', scale_factor)
    print(' Spectra in one profile:             ', interp_spectra_in_profile)
    print(' Remainder on n periods (1 profile): ', remainder_of_n_periods, ' s.')
    print(' Interpolated time resolution:       ', interp_time_resolution, ' s.\n')

    # Interpolated data buffer
    data_interp = np.zeros([freq_points_num, 0], dtype=np.float32)
    # Array for result integrated pulse
    integrated_spectra = np.zeros([freq_points_num, interp_spectra_in_profile], dtype=np.float32)

    # Counters:
    profiles_counter = 0  # Absolute profiles counter
    current_time_remainder = 0.0  # Counts time float lag between precise period and time resolution

    bar = IncrementalBar(' Averaging pulsar pulses... ', max=bunches_in_file, suffix='%(percent)d%%     ')
    bar.start()

    for bunch in range(bunches_in_file):

        data_raw = np.fromfile(data_file, dtype=np.float64, count=spectra_to_read * freq_points_num)
        data_raw = np.reshape(data_raw, [freq_points_num, spectra_to_read], order='F')
        with np.errstate(invalid='ignore', divide='ignore'):
            data_raw = 10 * np.log10(data_raw, dtype=np.float32)
        data_raw[np.isinf(data_raw)] = -135.5

        # Apply masking if needed
        if use_mask_file:
            # Read mask from file
            mask = np.fromfile(mask_file, dtype=bool, count=spectra_to_read * freq_points_num)
            mask = np.reshape(mask, [freq_points_num, spectra_to_read], order='F')
            # Apply as mask to data copy and calculate mean value without noise
            masked_data_raw = np.ma.masked_where(mask, data_raw)
            data_raw_mean = np.mean(masked_data_raw)
            del masked_data_raw

            # Apply as mask to data (change masked data with mean values of data outside mask)
            data_raw = data_raw * np.invert(mask)
            data_raw = data_raw + mask * data_raw_mean

        # Append the new interpolated (np.kron) data to buffer
        data_interp = np.append(data_interp, np.kron(data_raw, np.ones((1, scale_factor))), axis=1)
        del data_raw

        profiles_in_bunch = (data_interp.shape[1] - 10) // interp_spectra_in_profile  # -10 to have extra spectra to cut

        for i in range(profiles_in_bunch):
            # If cumulative time reminder exceeds time resolution we cut one spectrum to align time scales
            if current_time_remainder > interp_time_resolution:
                current_time_remainder = current_time_remainder - interp_time_resolution
                data_interp = data_interp[:, 1:]

            # Calculate current reminder
            current_time_remainder += remainder_of_n_periods
            # Integrate dynamic spectra
            integrated_spectra = integrated_spectra + \
                                 data_interp[:, i * interp_spectra_in_profile: (i+1) * interp_spectra_in_profile]

        profiles_counter += profiles_in_bunch

        data_interp = data_interp[:, interp_spectra_in_profile * profiles_in_bunch:]

        bar.next()

    bar.finish()

    data_file.close()
    if use_mask_file:
        mask_file.close()

    print('\n Total number of integrated pulses: ', profiles_counter)

    # Normalizing each frequency channel to have smooth dynamic spectra
    integrated_spectra = np.transpose(integrated_spectra)
    integrated_spectra = normalization_db(integrated_spectra, integrated_spectra.shape[1], integrated_spectra.shape[0])
    integrated_spectra = np.transpose(integrated_spectra)

    # Preparing single averaged data profile for figure
    profile = integrated_spectra.mean(axis=0)[:]
    profile = profile - np.mean(profile)
    profile = profile / np.max(profile)
    data = integrated_spectra - np.mean(integrated_spectra)

    #  Calculation of number of points to roll the pulse to the centre of the plot
    roll_count = int((len(profile) / 2 / periods_per_fig) - np.argmax(profile))
    data = np.roll(data, roll_count, axis=1)
    profile = np.roll(profile, roll_count)

    # Saving data to file
    data_filename = filename.split('/')[-1]
    save_integrated_pulse_to_file(data, file_header, p_bar, data.shape[1], common_path +
                                  'DSPZ_' + data_filename + ' - folded pulses.smp')
    print('\n SMP data file saved. \n')

    # Make a figure of pulses profiles and dynamic spectrum
    fig_title = 'File: ' + data_filename + '   Description: ' + df_description + '   Resolution: ' + \
                str(np.round(df/1000, 3)) + ' kHz and ' + str(np.round(time_resolution*1000, 3)) + ' ms.' + \
                '\n from ' + timeline[0][:19] + ' till ' + timeline[-1][:19] + ' UTC'

    fig_suptitle = 'Folded average pulses of ' + pulsar_name + ' (DM: ' + str(pulsar_dm) + \
                   r' $\mathrm{pc \cdot cm^{-3}}$' + ', Period: ' + str(p_bar) + ' s.), ' + \
                   str(profiles_counter) + ' integrated profiles '

    pic_filename = common_path + filename + ' - folded pulses.png'
    profile_pic_min = -0.25  # Minimum limit of profile picture
    profile_pic_max = 1.20  # Maximum limit of profile picture

    make_figure_of_pulse_profile_and_spectra(profile, data, frequency, profile_pic_min, profile_pic_max,
                                             spectrum_pic_min, spectrum_pic_max, periods_per_fig,
                                             fig_suptitle, fig_title, pic_filename, current_date, current_time,
                                             custom_dpi, colormap, show=True, save=True)

    return 0


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    pulsar_period_folding(common_path, filename, pulsar_name, scale_factor, spectrum_pic_min, spectrum_pic_max,
                          periods_per_fig, custom_dpi, colormap, use_mask_file=use_mask_file)

    print('\n\n       *** Program has finished! ***   \n\n\n')
