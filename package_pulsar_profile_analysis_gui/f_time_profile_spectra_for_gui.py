import os
import sys
import time
import pylab
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


def time_profile_spectra_for_gui_1_8(profile_data, time_resolution, harmonics_to_show, frequency_limit,
                                     common_path, filename, software_version, custom_dpi):

    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")

    # Data frequency resolution, Hz
    frequency_resolution = 1 / (time_resolution * len(profile_data))

    # Calculating the spectrum
    profile_spectrum = np.power(np.real(np.fft.fft(profile_data[:])), 2)  # calculation of the spectrum
    profile_spectrum = profile_spectrum[0:int(len(profile_spectrum)/2)]  # delete second part of the spectrum

    frequency_axis = [frequency_resolution * i for i in range(len(profile_spectrum))]

    # Calculating the limit of vertical axis of the spectrum plot
    spectrum_max = np.max(profile_spectrum)

    # Creating the firs plot with the entire data on the figure
    rc('font', size=5, weight='bold')
    fig, axs = plt.subplots(nrows=4, ncols=4, figsize=(18, 9))
    if harmonics_to_show is not None:
        for i in range(len(harmonics_to_show)):
            axs[0, 0].axvline(x=harmonics_to_show[i], color='C1', linestyle='-', linewidth=2.0, alpha=0.2)
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

    for step in range(3):
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

            # Calculating the limit of vertical axis of the spectrum plot
            spectrum_max = np.max(profile_spectrum)

            # Adding the plots for parts of data to the big result picture
            if harmonics_to_show is not None:
                for i in range(len(harmonics_to_show)):
                    axs[v_ind[index], h_ind[index]].axvline(x=harmonics_to_show[i], color='C1', linestyle='-',
                                                            linewidth=2.0, alpha=0.2)
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
    fig.suptitle('Time profile in frequency domain from file: ' + filename,
                 fontsize=8, fontweight='bold')
    fig.text(0.82, 0.06, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.11, 0.06, 'Software version: ' + software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=5, transform=plt.gcf().transFigure)
    pylab.savefig(os.path.join(common_path, filename[0:-4] + ' big picture up to 8 parts.png'),
                  bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')

    return


def time_profile_spectra_for_gui_16(profile_data, time_resolution, harmonics_to_show, frequency_limit,
                                     common_path, filename, software_version, custom_dpi):

    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")
    full_data_length = len(profile_data)

    step = 3
    parts_num = 2 ** (step + 1)
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
        new_profile_data = profile_data[start:stop]

        # Data frequency resolution, Hz
        frequency_resolution = 1 / (time_resolution * len(new_profile_data))

        # Calculating the spectrum
        profile_spectrum = np.power(np.real(np.fft.fft(new_profile_data[:])), 2)  # calculation of the spectrum
        profile_spectrum = profile_spectrum[0:int(len(profile_spectrum) / 2)]  # delete second part

        spectrum_max = np.max(profile_spectrum)
        frequency_axis = [frequency_resolution * i for i in range(len(profile_spectrum))]

        # Adding the plots for parts of data to the big result picture
        if harmonics_to_show is not None:
            for i in range(len(harmonics_to_show)):
                axs[v_ind[index], h_ind[index]].axvline(x=harmonics_to_show[i], color='C1', linestyle='-',
                                                        linewidth=2.0, alpha=0.2)
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
    fig.subplots_adjust(hspace=0.25, top=0.945)
    fig.suptitle('Time profile in frequency domain (16 parts) from file: ' + filename,
                 fontsize=8, fontweight='bold')
    fig.text(0.82, 0.06, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=5, transform=plt.gcf().transFigure)
    fig.text(0.11, 0.06, 'Software version: ' + software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=5, transform=plt.gcf().transFigure)
    pylab.savefig(os.path.join(common_path, filename[0:-4] + ' big picture 16 parts.png'),
                  bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')

    return
