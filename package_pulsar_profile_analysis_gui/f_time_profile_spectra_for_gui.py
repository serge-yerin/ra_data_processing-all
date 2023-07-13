# Python3
software_version = '2023.05.27'
Software_name = 'Pulsar long time profile spectra calculation (whole & chunks)'
# *******************************************************************************
#                     M A N U A L    P A R A M E T E R S                        *
# *******************************************************************************
# Path to initial and results files
common_path = '../../../RA_DATA_ARCHIVE/ADDITIONAL_pulses_profiles/'

# Name of TXT file to be analyzed:
filename = 'B0329+54_DM_26.78_C240122_152201.jds_Data_chA_time_profile.txt'
# filename = 'B0809+74_DM_5.755_P130422_121607.jds_Data_chA_time_profile.txt'
# filename = 'B0950+08_DM_2.972_C250122_214003.jds_Data_chA_time_profile.txt'
# filename = 'B1919+21_DM_12.4449_C040420_020109.jds_Data_chA_time_profile.txt'

pulsar_name = 'B0329+54'
# pulsar_name = 'B0809+74'
# pulsar_name = 'B0950+08'
# pulsar_name = 'B1919+21'

harmonics_to_show = 15  # Figure upper frequency (x-axis) limit in number of pulse harmonics to show

time_resolution = (1 / 66000000) * 16384 * 32    # Data time resolution, s   # 0.007944

profile_pic_min = -0.1         # Minimum limit of profile picture
profile_pic_max = 0.5          # Maximum limit of profile picture
custom_dpi = 300               # Resolution of images of dynamic spectra

# *******************************************************************************

# *******************************************************************************
#                     I M P O R T   L I B R A R I E S                           *
# *******************************************************************************
import os
import sys
import time
import pylab
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from matplotlib import rc
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_common_modules.text_manipulations import read_one_value_txt_file

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************

def time_profile_spectra_gui(common_path, filename, pulsar_name, time_resolution, harmonics_to_show,
                             software_version, custom_dpi):

    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")

    # Data frequency resolution, Hz
    frequency_resolution = 1 / (time_resolution * len(profile_data))

    # Calculating the spectrum
    profile_spectrum = np.power(np.real(np.fft.fft(profile_data[:])), 2)  # calculation of the spectrum
    profile_spectrum = profile_spectrum[0:int(len(profile_spectrum)/2)]  # delete second part of the spectrum

    frequency_axis = [frequency_resolution * i for i in range(len(profile_spectrum))]


    # Creating the firs plot with the entire data on the figure
    rc('font', size=5, weight='bold')
    fig, axs = plt.subplots(nrows=4, ncols=4, figsize=(18, 9))
    # axs[0, 0].axvline(x=pulsar_frequency, color='red', linestyle='-', linewidth=2.0,
    #                   alpha=0.4, label='Frequency of pulses')
    # for i in range(n_harmonics):
    #     axs[0, 0].axvline(x=pulsar_harmonics[i], color='C1', linestyle='-', linewidth=2.0, alpha=0.2)
    # Plotting the spectra
    axs[0, 0].plot(frequency_axis, profile_spectrum, color=u'#1f77b4',
             linestyle='-', alpha=1.0, linewidth='0.60', label='Time series spectrum')
    # Adding calculated maximal point near harmonics as red dots
    axs[0, 0].axis([0, frequency_limit, 0, 1.1 * spectrum_max])
    axs[0, 0].legend(loc='upper right', fontsize=5)
    axs[0, 0].set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    axs[0, 0].set_title('Full data length', fontsize=5, fontweight='bold')

    # Analyze only parts of the time profile
    # Creating indexes for plots positioning on the big result figure
    v_ind = [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    h_ind = [1, 2, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    index = 0

    full_data_length = len(profile_data)

    for step in range(3):  # 4
        parts_num = 2 ** (step + 1)

        for part in range(parts_num):

            start = int((full_data_length / parts_num) * part)
            stop = int((full_data_length / parts_num) * (part + 1))
            add_text = ' Part ' + str(part+1) + ' of ' + str(parts_num)
            new_profile_data = profile_data[start:stop]

            # Data frequency resolution, Hz
            frequency_resolution = 1 / (time_resolution * len(new_profile_data))

            # Calculating the spectrum
            profile_spectrum = np.power(np.real(np.fft.fft(new_profile_data[:])), 2)  # calculation of the spectrum
            profile_spectrum = profile_spectrum[0:int(len(profile_spectrum) / 2)]  # delete second part

            frequency_axis = [frequency_resolution * i for i in range(len(profile_spectrum))]

            # Adding the plots for parts of data to the big result picture
            # axs[v_ind[index], h_ind[index]].axvline(x=pulsar_frequency, color='red', linestyle='-', linewidth=2.0,
            #                                         alpha=0.4, label='Frequency of pulses')
            # for i in range(n_harmonics):
            #     axs[v_ind[index], h_ind[index]].axvline(x=pulsar_harmonics[i], color='C1', linestyle='-',
            #                                             linewidth=2.0, alpha=0.2)
            # Plotting the spectra
            axs[v_ind[index], h_ind[index]].plot(frequency_axis, profile_spectrum, color=u'#1f77b4',
                                                 linestyle='-', alpha=1.0, linewidth='0.60',
                                                 label='Time series spectrum')
            axs[v_ind[index], h_ind[index]].axis([0, frequency_limit, 0, 1.1 * spectrum_max])
            axs[v_ind[index], h_ind[index]].legend(loc='upper right', fontsize=5)
            if v_ind[index] == 3:
                axs[v_ind[index], h_ind[index]].set_xlabel('Frequency, Hz', fontsize=6, fontweight='bold')
            if h_ind[index] == 0:
                axs[v_ind[index], h_ind[index]].set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
            axs[v_ind[index], h_ind[index]].set_title(add_text, fontsize=5, fontweight='bold')
            index += 1

    # Finishing and saving the big results figure with 15 plots
    axs[0, 3].axis('off')
    fig.subplots_adjust(hspace=0.25, top=0.945)
    fig.suptitle('Single pulses of ' + pulsar_name + ' in frequency domain from file: ' + filename,
                 fontsize=8, fontweight='bold')
    fig.text(0.82, 0.06, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.11, 0.06, 'Software version: ' + software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=5, transform=plt.gcf().transFigure)
    pylab.savefig(common_path + new_folder_name + '/' + filename[0:-4] + ' big picture up to 8 parts.png',
                  bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')
















    #
    #
    # Plotting dividing the data to 16 parts in a separate big figure
    #
    #

    # Creating indexes for plots positioning on the big result figure
    step = 3
    parts_num = 2 ** (step + 1)
    harmonics_amplitudes = np.empty(shape=[parts_num, n_harmonics])

    v_ind = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    h_ind = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    index = 0

    # Creating the first plot with the entire data on the figure
    rc('font', size=5, weight='bold')
    fig, axs = plt.subplots(nrows=4, ncols=4, figsize=(18, 9))

    for part in range(parts_num):

        start = int((full_data_length / parts_num) * part)
        stop = int((full_data_length / parts_num) * (part + 1))
        add_text = ' Part ' + str(part+1) + ' of ' + str(parts_num)
        print('    Processing' + add_text)
        new_profile_data = profile_data[start:stop]

        # Data frequency resolution, Hz
        frequency_resolution = 1 / (time_resolution * len(new_profile_data))

        # Calculate pulsar harmonics frequency
        pulsar_harmonics_points = np.ceil(pulsar_harmonics / frequency_resolution).astype(int)
        freq_points_per_harmonic = np.ceil(pulsar_frequency / frequency_resolution).astype(int)
        max_interval = int(freq_points_per_harmonic / 5)

        # Calculating the spectrum
        profile_spectrum = np.power(np.real(np.fft.fft(new_profile_data[:])), 2)  # calculation of the spectrum
        profile_spectrum = profile_spectrum[0:int(len(profile_spectrum) / 2)]  # delete second part

        frequency_axis = [frequency_resolution * i for i in range(len(profile_spectrum))]

        # Finding the maximal spectrum amplitudes near expected harmonics
        max_harmonics = []
        for i in range(n_harmonics):
            max_harmonics.append(np.max(profile_spectrum[pulsar_harmonics_points[i] - max_interval:
                                                         pulsar_harmonics_points[i] + max_interval]))

        # Adding new maximal harmonics raw to array for the step
        harmonics_amplitudes[part] = max_harmonics

        # Calculating the limit o vertical axis of the spectrum plot
        spectrum_max = np.max(max_harmonics)

        # Adding the plots for parts of data to the big result picture
        axs[v_ind[index], h_ind[index]].axvline(x=pulsar_frequency, color='red', linestyle='-', linewidth=2.0,
                                                alpha=0.4, label='Frequency of pulses')
        for i in range(n_harmonics):
            axs[v_ind[index], h_ind[index]].axvline(x=pulsar_harmonics[i], color='C1', linestyle='-',
                                                    linewidth=2.0, alpha=0.2)
        # Plotting the spectra
        axs[v_ind[index], h_ind[index]].plot(frequency_axis, profile_spectrum, color=u'#1f77b4',
                                             linestyle='-', alpha=1.0, linewidth='0.60',
                                             label='Time series spectrum')
        # Adding calculated maximal point near harmonics as red dots
        axs[v_ind[index], h_ind[index]].scatter(pulsar_harmonics, max_harmonics, marker='o', color='red', s=6.0,
                                                label='Harmonics amplitudes')
        axs[v_ind[index], h_ind[index]].axis([0, frequency_limit, 0, 1.1 * spectrum_max])
        axs[v_ind[index], h_ind[index]].legend(loc='upper right', fontsize=5)
        if v_ind[index] == 3:
            axs[v_ind[index], h_ind[index]].set_xlabel('Frequency, Hz', fontsize=6, fontweight='bold')
        if h_ind[index] == 0:
            axs[v_ind[index], h_ind[index]].set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        axs[v_ind[index], h_ind[index]].set_title(add_text, fontsize=5, fontweight='bold')
        index += 1

    # Finishing and saving the big results figure with 15 plots
    fig.subplots_adjust(hspace=0.25, top=0.945)
    fig.suptitle('Single pulses of ' + pulsar_name + ' in frequency domain in 16 parts from file: ' + filename,
                 fontsize=8, fontweight='bold')
    fig.text(0.82, 0.06, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.11, 0.06, 'Software version: ' + software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=5, transform=plt.gcf().transFigure)
    pylab.savefig(common_path + new_folder_name + '/' + filename[0:-4] + ' big picture 16 parts.png',
                  bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')

    return


if __name__ == '__main__':

    print('\n\n\n\n\n\n   *********************************************************************************')
    print('   *   ', Software_name, ' v.', software_version, '   *      (c) YeS 2023')
    print('   ********************************************************************************* \n')

    start_time = time.time()
    previousTime = start_time

    time_profile_spectra(common_path, filename, pulsar_name, time_resolution, harmonics_to_show,
                         profile_pic_min, profile_pic_max, software_version, custom_dpi)

    end_time = time.time()    # Time of calculations

    print('\n\n  The program execution lasted for ',
          round((end_time - start_time), 2), 'seconds (', round((end_time - start_time)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
