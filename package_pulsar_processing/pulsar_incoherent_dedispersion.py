# Python3
software_version = '2022.06.08'
software_name = 'Pulsar single pulses processing pipeline'
# Program intended to read and show individual pulses of pulsars from DAT files
# *******************************************************************************
#                     M A N U A L    P A R A M E T E R S                        *
# *******************************************************************************
# Path to data files
common_path = ''

# DAT file to be analyzed:
filename = 'E300117_180000.jds_Data_chA.dat'  # 'E220213_201439.jds_Data_chA.dat'

pulsar_name = 'B0809+74'  # 'B1919+21' #'B0809+74' #'B1133+16' #  'B1604-00' 'B0950+08'

average_const = 512            # Number of frequency channels to appear in result picture
profile_pic_min = -0.15        # Minimum limit of profile picture
profile_pic_max = 0.55         # Maximum limit of profile picture

SpecFreqRange = 0              # Specify particular frequency range (1) or whole range (0)
freqStart = 2.0                # Lower frequency of dynamic spectrum (MHz)
freqStop = 8.0                 # Higher frequency of dynamic spectrum (MHz)

save_profile_txt = True        # Save profile data to TXT file?
save_compensated_data = True      # Save data with compensated DM to DAT file?
custom_dpi = 300                # Resolution of images of dynamic spectra
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
import matplotlib.ticker as mticker   # <---- Added to suppress warning
from os import path
from matplotlib import rc
import matplotlib
matplotlib.use('agg')

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_ra_data_processing.f_spectra_normalization import normalization_lin
from package_ra_data_processing.average_some_lines_of_array import average_some_lines_of_array
from package_ra_data_files_formats.read_file_header_adr import file_header_adr_read
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
from package_ra_data_files_formats.specify_frequency_range import specify_frequency_range
from package_ra_data_files_formats.f_jds_header_new_channels_numbers import jds_header_new_channels_numbers
from package_pulsar_processing.pulsar_DM_full_shift_calculation import DM_full_shift_calc
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes
from package_pulsar_processing.pulsar_pulses_time_profile_FFT import pulsar_pulses_time_profile_FFT
from package_astronomy.catalogue_pulsar import catalogue_pulsar


# *******************************************************************************
#                              F U N C T I O N S                                *
# *******************************************************************************


def plot_integrated_profile_and_spectra(profile, averaged_array, frequency_list, num_frequencies, fig_time_scale,
                                        newpath, filename, pulsar_name, pulsar_dm, freq_resolution, time_resolution,
                                        max_time_shift, fig_no, fig_num, block, profile_pic_min, profile_pic_max,
                                        df_description, colormap, custom_dpi, a_current_date, a_current_time,
                                        software_version):

    # Making result picture
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')
    ax1 = fig.add_subplot(211)
    ax1.plot(profile, color=u'#1f77b4', linestyle='-', alpha=1.0, linewidth='0.60', label='Pulses time profile')
    ax1.legend(loc='upper right', fontsize=5)
    ax1.grid(visible=True, which='both', color='silver', linewidth='0.50', linestyle='-')
    ax1.axis([0, len(profile), profile_pic_min, profile_pic_max])
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title('File: ' + filename + '  Description: ' + df_description + '  Averaging: ' +
                  str(np.round(freq_resolution, 3)) + ' kHz and ' + str(np.round(time_resolution*1000, 3)) +
                  ' ms.  Max. shift: ' + str(np.round(max_time_shift, 3)) + ' s.', fontsize=5, fontweight='bold')
    ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax2 = fig.add_subplot(212)
    ax2.imshow(np.flipud(averaged_array), vmin=0, vmax=5, aspect='auto', cmap=colormap,
               extent=[0, len(profile), frequency_list[0], frequency_list[num_frequencies-1]])
    ax2.set_xlabel('Time UTC (at the lowest frequency), HH:MM:SS.ms', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Frequency, MHz', fontsize=6, fontweight='bold')
    text = ax2.get_xticks().tolist()
    for i in range(len(text)-1):
        k = int(text[i])
        text[i] = fig_time_scale[k]

    ticks_loc = ax2.get_xticks().tolist()                              # <---- Added to suppress warning
    ax2.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))       # <---- Added to suppress warning

    ax2.set_xticklabels(text, fontsize=5, fontweight='bold')
    fig.subplots_adjust(hspace=0.05, top=0.91)  # top=0.92
    fig.suptitle('Single pulses of ' + pulsar_name+' (DM = ' + str(pulsar_dm) + r' $\mathrm{pc \cdot cm^{-3}}$' +
                 '), fig. ' + str(fig_no) + ' of ' + str(fig_num), fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + a_current_date + ' at ' + a_current_time,
             fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: ' + software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=3,
             transform=plt.gcf().transFigure)
    pylab.savefig(newpath + '/' + filename + ' fig. ' + str(block) + ' - Combined picture.png',
                  bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')


def pulsar_incoherent_dedispersion(common_path, filename, pulsar_name, average_const, profile_pic_min, profile_pic_max,
                                   SpecFreqRange, freqStart, freqStop, save_profile_txt, save_compensated_data,
                                   custom_dpi, colormap, use_mask_file=False, save_pics=True, transient_dm=0,
                                   result_path='', make_fourier=False):

    """
    Makes incoherent compensation of time delays in each frequency channel with its shift
    It assumes we obtain raw dat files from ADR or JDS readers where for JDS the last channels are not deleted
    """

    a_previous_time = time.time()
    a_current_time = time.strftime("%H:%M:%S")
    a_current_date = time.strftime("%d.%m.%Y")

    rc('font', size=6, weight='bold')
    data_filepath = common_path + filename

    # *** Creating a folder where all pictures and results will be stored (if it doesn't exist) ***
    newpath = result_path + 'RESULTS_pulsar_single_pulses_' + pulsar_name + '_' + filename[:-4]
    if save_pics:
        if not os.path.exists(newpath):
            os.makedirs(newpath)

    # Path to timeline file to be analyzed:
    time_line_file_name = common_path + filename[-31:-13] + '_Timeline.txt'

    # *** Opening DAT datafile to check the initial file type ***
    file = open(data_filepath, 'rb')
    df_filename = file.read(32).decode('utf-8').rstrip('\x00')            # Initial data file name
    file.close()

    receiver_type = df_filename[-4:]

    # Reading file header to obtain main parameters of the file
    if receiver_type == '.adr':
        [time_res, fmin, fmax, df, frequency_list, fft_size, clc_freq, mode] = file_header_adr_read(data_filepath, 0, 1)

    elif receiver_type == '.jds':
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description, clc_freq, df_creation_time_utc, 
            sp_in_file, receiver_mode, mode, n_avr, time_res, fmin, fmax, df, frequency_list, fft_size,
            data_block_size] = file_header_jds_read(data_filepath, 0, 1)
    else:
        sys.exit(' Error! Unknown data type!')

    # Manually set frequencies for two channels mode
    if int(clc_freq / 1000000) == 33:
        # fft_size = 8192
        fmin = 16.5
        fmax = 33.0
        frequency_list = np.linspace(fmin, fmax, fft_size)

    # Number of spectra in the file   #   file size - 1024 bytes of header
    dat_sp_in_file = int(((df_filesize - 1024) / (len(frequency_list) * 8)))

    # Obtain pulsar parameters from catalogue
    if 'Transient' in pulsar_name:
        pulsar_dm = transient_dm
    else:
        pulsar_ra, pulsar_dec, pulsar_dm, p_bar = catalogue_pulsar(pulsar_name)

    if save_profile_txt > 0:
        # *** Creating a name for long timeline TXT file ***
        profile_file_name = common_path + pulsar_name + '_DM_' + str(pulsar_dm) + '_' + \
                            filename[:-4] + '_time_profile.txt'
        profile_txt_file = open(profile_file_name, 'w')  # Open and close to delete the file with the same name
        profile_txt_file.close()

    # ************************************************************************************
    #                             R E A D I N G   D A T A                                *
    # ************************************************************************************

    # Timeline file reading
    timeline, dt_timeline = time_line_file_reader(time_line_file_name)

    # Selecting the frequency range of data to be analyzed
    if SpecFreqRange == 1:
        A = []
        B = []
        for i in range(len(frequency_list)):
            A.append(abs(frequency_list[i] - freqStart))
            B.append(abs(frequency_list[i] - freqStop))
        ifmin = A.index(min(A))
        ifmax = B.index(min(B))
        shift_vector = DM_full_shift_calc(ifmax - ifmin, frequency_list[ifmin], frequency_list[ifmax], df / pow(10, 6),
                                          time_res, pulsar_dm, receiver_type)
        print(' Number of frequency channels:  ', ifmax - ifmin)

    else:
        shift_vector = DM_full_shift_calc(len(frequency_list) - 4, fmin, fmax, df / pow(10, 6),
                                          time_res, pulsar_dm, receiver_type)
        print(' Number of frequency channels:  ', len(frequency_list) - 4)
        ifmin = int(fmin * 1e6 / df)
        ifmax = int(fmax * 1e6 / df) - 4

    if save_compensated_data > 0:
        with open(data_filepath, 'rb') as file:
            file_header = file.read(1024)  # Data file header read

        # Change number of frequency channels in the header
        file_header = jds_header_new_channels_numbers(file_header, ifmin, ifmax)

        # *** Creating a binary file with data for long data storage ***
        new_data_file_name = common_path + pulsar_name + '_DM_' + str(pulsar_dm) + '_' + filename
        new_data_file = open(new_data_file_name, 'wb')
        new_data_file.write(file_header)
        new_data_file.close()

        if use_mask_file:
            new_mask_file_name = common_path + pulsar_name + '_DM_' + str(pulsar_dm) + '_' + filename[:-3] + 'msk'
            new_mask_file = open(new_mask_file_name, 'wb')
            new_mask_file.write(file_header)
            new_mask_file.close()

        # *** Creating a name for long timeline TXT file ***
        data_filename = data_filepath.split('/')[-1]
        new_tl_file_name = common_path + pulsar_name + '_DM_' + str(pulsar_dm) + '_' + \
                           data_filename[:-13] + '_Timeline.txt'
        new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
        new_tl_file.close()
        del file_header

    max_shift = np.abs(shift_vector[0])

    buffer_array = np.zeros((ifmax - ifmin, 2 * max_shift))
    if use_mask_file:
        buffer_msk_array = np.zeros((ifmax - ifmin, 2 * max_shift), dtype=bool)

    num_of_blocks = int(dat_sp_in_file / max_shift)

    print(' Number of spectra in file:     ', dat_sp_in_file)
    print(' Maximal shift is:              ', max_shift, ' pixels ')
    print(' Number of blocks in file:      ', num_of_blocks)
    print(' Pulsar name:                   ', pulsar_name)
    print(' Dispersion measure:            ', pulsar_dm, ' pc / cm3 \n')

    if receiver_type == '.jds':
        num_frequencies_initial = len(frequency_list) - 4

    frequency_list_initial = np.empty_like(frequency_list)
    frequency_list_initial[:] = frequency_list[:]

    dat_file = open(data_filepath, 'rb')
    dat_file.seek(1024)                     # Jumping to 1024 byte from file beginning

    if use_mask_file:
        msk_file = open(data_filepath[:-3] + 'msk', 'rb')
        msk_file.seek(1024)  # Jumping to 1024 byte from file beginning

    for block in range(num_of_blocks):   # main loop by number of blocks in file

        print('\n * Data block # ', block + 1, ' of ', num_of_blocks,
              '\n ******************************************************************')

        # Timeline arrangements:
        fig_time_scale = []
        fig_date_time_scale = []
        for i in range(block * max_shift, (block+1) * max_shift):  # Shows the time of pulse end (at lowest frequency)
            fig_time_scale.append(timeline[i][11:23])
            fig_date_time_scale.append(timeline[i][:])
        print(' Time: ', fig_time_scale[0], ' - ', fig_time_scale[-1], ', number of points: ', len(fig_time_scale))

        # Data block reading
        if receiver_type == '.jds':
            data = np.fromfile(dat_file, dtype=np.float64, count=(num_frequencies_initial + 4) * max_shift)   # 2
            data = np.reshape(data, [(num_frequencies_initial + 4), max_shift], order='F')  # 2
            data = data[:num_frequencies_initial, :]  # To delete the last channels of DSP data where time is stored

        if use_mask_file:
            mask = np.fromfile(msk_file, dtype=bool, count=(num_frequencies_initial + 4) * max_shift)
            mask = np.reshape(mask, [(num_frequencies_initial + 4), max_shift], order='F')
            mask = mask[:num_frequencies_initial, :]

        # Cutting the array in predefined frequency range
        if SpecFreqRange == 1:
            data, frequency_list, fi_start, fi_stop = specify_frequency_range(data, frequency_list_initial,
                                                                              freqStart, freqStop)
            num_frequencies = len(frequency_list)
        else:
            num_frequencies = num_frequencies_initial  # + 4

        # Normalization of data
        normalization_lin(data, num_frequencies, 1 * max_shift)

        now_time = time.time()
        print('\n  *** Preparation of data took:              ', round((now_time - a_previous_time), 2), 'seconds ')
        a_previous_time = now_time

        # Dispersion delay removing
        data_space = np.zeros((num_frequencies, 2 * max_shift))
        data_space[:, max_shift:] = data[:, :]
        temp_array = pulsar_DM_compensation_with_indices_changes(data_space, shift_vector)
        del data, data_space

        if use_mask_file:
            mask_space = np.zeros((num_frequencies, 2 * max_shift), dtype=bool)
            mask_space[:, max_shift:] = mask[:, :]
            temp_mask_array = pulsar_DM_compensation_with_indices_changes(mask_space, shift_vector)
            temp_mask_array = np.array(temp_mask_array, dtype=bool)

        now_time = time.time()
        print('\n  *** Dispersion delay removing took:        ', round((now_time - a_previous_time), 2), 'seconds ')
        a_previous_time = now_time

        # Adding the next data block
        buffer_array += temp_array
        if use_mask_file:
            buffer_msk_array += temp_mask_array

        # Making and filling the array with fully ready data for plotting and saving to a file
        array_compensated_pulsar_dm = buffer_array[:, 0: max_shift]
        if use_mask_file:
            mask_compensated_pulsar_dm = buffer_msk_array[:, 0: max_shift]

        if block > 0:
            # Saving data with compensated pulsar_dm to DAT file
            if save_compensated_data > 0 and block > 0:
                temp_to_write = np.transpose(array_compensated_pulsar_dm).copy(order='C')
                new_data_file = open(new_data_file_name, 'ab')
                new_data_file.write(temp_to_write)
                new_data_file.close()
                del temp_to_write

                if use_mask_file:
                    temp_to_write = np.transpose(mask_compensated_pulsar_dm).copy(order='C')
                    new_mask_file = open(new_mask_file_name, 'ab')
                    new_mask_file.write(temp_to_write)
                    new_mask_file.close()
                    del temp_to_write

                # Saving time data to ling timeline file
                with open(new_tl_file_name, 'a') as new_tl_file:
                    for i in range(max_shift):
                        new_tl_file.write((fig_date_time_scale[i][:]))  # str

            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # Logging the data
            with np.errstate(divide='ignore'):
                array_compensated_pulsar_dm[:, :] = 10 * np.log10(array_compensated_pulsar_dm[:, :])
            array_compensated_pulsar_dm[array_compensated_pulsar_dm == -np.inf] = 0
            array_compensated_pulsar_dm[array_compensated_pulsar_dm == np.nan] = 0
            array_compensated_pulsar_dm[np.isinf(array_compensated_pulsar_dm)] = 0

            # Normalizing log data
            array_compensated_pulsar_dm = array_compensated_pulsar_dm - np.mean(array_compensated_pulsar_dm)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            masked_data_raw = np.ma.masked_where(mask_compensated_pulsar_dm, array_compensated_pulsar_dm)
            data_raw_mean = np.mean(masked_data_raw)
            del masked_data_raw

            # Apply as mask to data (change masked data with mean values of data outside mask)
            array_compensated_pulsar_dm = array_compensated_pulsar_dm * np.invert(mask_compensated_pulsar_dm)
            array_compensated_pulsar_dm = array_compensated_pulsar_dm + mask_compensated_pulsar_dm * data_raw_mean

            # Preparing single averaged data profile for figure
            profile = array_compensated_pulsar_dm.mean(axis=0)[:]
            profile = profile - np.mean(profile)

            # Save full profile to TXT file
            if save_profile_txt > 0:
                profile_txt_file = open(profile_file_name, 'a')
                for i in range(len(profile)):
                    profile_txt_file.write(str(profile[i]) + ' \n')
                profile_txt_file.close()

            if save_pics:
                # Averaging of the array with pulses for figure
                averaged_array = average_some_lines_of_array(array_compensated_pulsar_dm, int(num_frequencies/average_const))
                freq_resolution = (df * int(num_frequencies/average_const)) / 1000.
                max_time_shift = max_shift * time_res

                averaged_array = averaged_array - np.mean(averaged_array)

                plot_integrated_profile_and_spectra(profile, averaged_array, frequency_list, num_frequencies,
                                                    fig_time_scale, newpath, filename, pulsar_name, pulsar_dm,
                                                    freq_resolution, time_res, max_time_shift, block, num_of_blocks-1,
                                                    block, profile_pic_min, profile_pic_max, df_description, colormap,
                                                    custom_dpi, a_current_date, a_current_time, software_version)

        # Rolling temp_array to put current data first
        buffer_array = np.roll(buffer_array, - max_shift)
        buffer_array[:, max_shift:] = 0
        if use_mask_file:
            buffer_msk_array = np.roll(buffer_msk_array, - max_shift)
            buffer_msk_array[:, max_shift:] = 0

    dat_file.close()

    # Fourier analysis of the obtained time profile of pulses
    if save_profile_txt and make_fourier:
        print('\n\n  *** Making Fourier transform of the time profile...')
        pulsar_pulses_time_profile_FFT(newpath + '/', filename + '_time_profile.txt', pulsar_name, time_res,
                                       profile_pic_min, profile_pic_max, custom_dpi, colormap)
    if not save_compensated_data:
        new_data_file_name = ''
    return new_data_file_name


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    print(' \n\n\n\n\n\n\n\n')
    print('   *****************************************************************')
    print('   *   ', software_name, ' v.', software_version, '   *      (c) YeS 2020')
    print('   ***************************************************************** \n\n\n')

    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")
    print('  Today is ', current_date, ' time is ', current_time, ' \n')

    data_file_name = pulsar_incoherent_dedispersion(common_path, filename, pulsar_name, average_const,
                                        profile_pic_min, profile_pic_max,
                                        SpecFreqRange, freqStart, freqStop, save_profile_txt,
                                        save_compensated_data, custom_dpi, colormap, use_mask_file=True)

    print('  Dedispersed data stored in:', data_file_name)

    end_time = time.time()    # Time of calculations

    print('\n\n  The program execution lasted for ', round((end_time - start_time), 2), 'seconds (',
                                                     round((end_time - start_time)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', software_name, ' has finished! *** \n\n\n')
