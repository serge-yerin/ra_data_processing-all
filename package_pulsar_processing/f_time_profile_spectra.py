# Python3
software_version = '2023.05.27'
Software_name = 'Pulsar long time profile spectra calculation (whole & chunks)'
# *******************************************************************************
#                     M A N U A L    P A R A M E T E R S                        *
# *******************************************************************************
# Path to initial and results files
common_path = '../../../RA_DATA_ARCHIVE/ADDITIONAL_pulses_profiles/'

# Name of TXT file to be analyzed:
# filename = 'B0329+54_DM_26.78_C240122_152201.jds_Data_chA_time_profile.txt'
# filename = 'B0809+74_DM_5.755_P130422_121607.jds_Data_chA_time_profile.txt'
filename = 'B0950+08_DM_2.972_C250122_214003.jds_Data_chA_time_profile.txt'
# filename = 'B1919+21_DM_12.4449_C040420_020109.jds_Data_chA_time_profile.txt'

# pulsar_name = 'B0329+54'
# pulsar_name = 'B0809+74'
pulsar_name = 'B0950+08'
# pulsar_name = 'B1919+21'

frequency_limit = 40  # Hz - figure upper frequency (x-axis) limit
analyze_parts = True  # To analyze the splitting the whole time series in 2, 4, 8, 16 parts

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
import matplotlib.pyplot as plt
from matplotlib import rc
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_common_modules.text_manipulations import read_one_value_txt_file


def plot_time_profile(profile_data, profile_pic_min, profile_pic_max, pulsar_period, filename, common_path,
                      current_date, current_time, software_version, custom_dpi):
    # Making result time profile
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')
    ax1 = fig.add_subplot(111)
    ax1.plot(profile_data, color=u'#1f77b4', linestyle='-', alpha=1.0, linewidth='0.60', label='Pulses time profile')
    ax1.legend(loc='upper right', fontsize=5)
    ax1.grid(visible=True, which='both', color='silver', linewidth='0.50', linestyle='-')
    ax1.axis([0, len(profile_data), profile_pic_min, profile_pic_max])
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title('File: ' + filename + '  Pulsar period: ' + str(np.round(pulsar_period, 3)) + ' s.',
                  fontsize=5, fontweight='bold')
    ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    fig.suptitle('Single pulses of ' + pulsar_name + ' in time', fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: ' + software_version + ', yerin.serge@gmail.com, IRA NASU', fontsize=3,
             transform=plt.gcf().transFigure)
    pylab.savefig(common_path + '/' + filename[0:-4] + ' time profile.png', bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')
    return


def plot_spectra_log_amplitude(frequency_axis, profile_spectrum, pulsar_period, pulsar_frequency, pulsar_harmonics,
                               max_harmonics, spectrum_max, frequency_limit, n_harmonics, common_path, filename, add_text,
                               current_date, current_time, software_version, custom_dpi):
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')
    ax1 = fig.add_subplot(111)
    # Plotting lines where fundamental and other harmonics are expected
    ax1.axvline(x=pulsar_frequency, color='red', linestyle='-', linewidth=2.0, alpha=0.4, label='Frequency of pulses')
    for i in range(n_harmonics):
        ax1.axvline(x=pulsar_harmonics[i], color='C1', linestyle='-', linewidth=2.0, alpha=0.2)
    # Plotting the spectra
    ax1.plot(frequency_axis, profile_spectrum, color=u'#1f77b4',
             linestyle='-', alpha=1.0, linewidth='0.60', label='Time series spectrum')
    # Adding calculated maximal point near harmonics as red dots
    plt.scatter(pulsar_harmonics, max_harmonics, marker='o', color='red', s=3.0)
    ax1.axis([0, frequency_limit, 1, 1.5 * spectrum_max])
    plt.yscale('log')
    ax1.legend(loc='upper right', fontsize=5)
    ax1.set_xlabel('Frequency, Hz', fontsize=6, fontweight='bold')
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title('File: ' + filename + '  Pulsar period: ' + str(np.round(pulsar_period, 3)) + ' s.',
                  fontsize=5, fontweight='bold')
    fig.suptitle('Single pulses of ' + pulsar_name + ' in frequency domain (logarithmic amplitude)' + add_text,
                 fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: ' + software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig(common_path + '/' + filename[0:-4] + ' spectrum logarithmic' + add_text + '.png',
                  bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')
    return


def plot_spectra_lin_amplitude(frequency_axis, profile_spectrum, pulsar_period, pulsar_frequency, pulsar_harmonics,
                               max_harmonics, spectrum_max, frequency_limit, n_harmonics, common_path, filename, add_text,
                               current_date, current_time, software_version, custom_dpi):
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')
    ax1 = fig.add_subplot(111)
    # Plotting lines where fundamental and other harmonics are expected
    ax1.axvline(x=pulsar_frequency, color='red', linestyle='-', linewidth=2.0, alpha=0.4, label='Frequency of pulses')
    for i in range(n_harmonics):
        ax1.axvline(x=pulsar_harmonics[i], color='C1', linestyle='-',
                    linewidth=2.0, alpha=0.2)
    # Plotting the spectra
    ax1.plot(frequency_axis, profile_spectrum, color=u'#1f77b4',
             linestyle='-', alpha=1.0, linewidth='0.60', label='Time series spectrum')
    # Adding calculated maximal point near harmonics as red dots
    plt.scatter(pulsar_harmonics, max_harmonics, marker='o', color='red', s=3.0)
    ax1.axis([0, frequency_limit, 0, 1.1 * spectrum_max])
    ax1.legend(loc='upper right', fontsize=5)
    ax1.set_xlabel('Frequency, Hz', fontsize=6, fontweight='bold')
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title('File: ' + filename + '  Pulsar period: ' + str(np.round(pulsar_period, 3)) + ' s.',
                  fontsize=5, fontweight='bold')
    fig.suptitle('Single pulses of ' + pulsar_name + ' in frequency domain (linear amplitude)' + add_text,
                 fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: ' + software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig(common_path + '/' + filename[0:-4] + ' spectrum linear' + add_text + '.png',
                  bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')
    return

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************


def time_profile_spectra(common_path, filename, pulsar_name, time_resolution, frequency_limit,
                         profile_pic_min, profile_pic_max, analyze_parts, software_version, custom_dpi):

    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")

    data_filename = common_path + filename

    new_folder_name = filename[:-4] + "_analysis"
    if not os.path.exists(common_path + new_folder_name):
        os.makedirs(common_path + new_folder_name)

    # Reading profile data from txt file
    profile_data = read_one_value_txt_file(data_filename)
    print('\n  Number of samples in text file:  ', len(profile_data))

    # Getting pulsar parameters from catalogue
    pulsar_ra, pulsar_dec, source_dm, pulsar_period = catalogue_pulsar(pulsar_name)

    # Data frequency resolution, Hz
    frequency_resolution = 1 / (time_resolution * len(profile_data))

    # Calculate pulsar harmonics frequency
    pulsar_frequency = 1 / pulsar_period  # frequency of pulses, Hz

    freq_points_per_harmonic = np.ceil(pulsar_frequency / frequency_resolution).astype(int)
    n_harmonics = int(np.floor(len(profile_data) / (2 * freq_points_per_harmonic)))

    pulsar_harmonics = pulsar_frequency * np.linspace(1, n_harmonics, num=n_harmonics)
    pulsar_harmonics_points = np.ceil(pulsar_harmonics / frequency_resolution).astype(int)
    max_interval = int(freq_points_per_harmonic / 5)

    print('  Pulsar frequency: ', pulsar_frequency, ' Hz')
    print('  Frequency resolution: ', frequency_resolution, ' s')
    print('  Time resolution: ', time_resolution, ' s')
    print('  Number of points per harmonic: ', freq_points_per_harmonic)
    print('  Number harmonics to highlight: ', n_harmonics)

    # Calculating the spectrum
    profile_spectrum = np.power(np.real(np.fft.fft(profile_data[:])), 2)  # calculation of the spectrum
    profile_spectrum = profile_spectrum[0:int(len(profile_spectrum)/2)]  # delete second part of the spectrum

    # Nulling of lowest harmonics if necessary
    # profile_spectrum[0:100] = 0.0

    frequency_axis = [frequency_resolution * i for i in range(len(profile_spectrum))]

    # Finding the maximal spectrum amplitudes near expected harmonics
    max_harmonics = []
    for i in range(n_harmonics):
        max_harmonics.append(np.max(profile_spectrum[pulsar_harmonics_points[i] - max_interval:
                                                     pulsar_harmonics_points[i] + max_interval]))

    # Calculating the limit o vertical axis of the spectrum plot
    spectrum_max = np.max(max_harmonics)

    # # Making result time profile plot
    plot_time_profile(profile_data, profile_pic_min, profile_pic_max, pulsar_period, filename,
                      common_path + new_folder_name, current_date, current_time, software_version, custom_dpi)

    add_text = ''

    # Plotting figure of result spectrum logarithmic
    # plot_spectra_log_amplitude(frequency_axis, profile_spectrum, pulsar_period, pulsar_frequency, pulsar_harmonics,
    #                            max_harmonics, spectrum_max, frequency_limit, n_harmonics,
    #                            common_path + new_folder_name, filename, add_text, current_date, current_time,
    #                            software_version, custom_dpi)

    # Plotting figure of result spectrum linear
    plot_spectra_lin_amplitude(frequency_axis, profile_spectrum, pulsar_period, pulsar_frequency, pulsar_harmonics,
                               max_harmonics, spectrum_max, frequency_limit, n_harmonics,
                               common_path + new_folder_name, filename, add_text,
                               current_date, current_time, software_version, custom_dpi)

    # Analyze only parts of the time profile
    if analyze_parts:
        print('\n  Processing parts of the full profile:')
        full_data_length = len(profile_data)

        for step in range(4):
            parts_num = 2 ** (step + 1)
            harmonics_amplitudes = np.empty(shape=[parts_num, n_harmonics])

            for part in range(parts_num):
                start = int((full_data_length / parts_num) * part)
                stop = int((full_data_length / parts_num) * (part + 1))
                add_text = ' part ' + str(part+1) + ' of ' + str(parts_num)
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

                # # Making result time profile plot
                plot_time_profile(profile_data, profile_pic_min, profile_pic_max, pulsar_period, filename,
                                  common_path + new_folder_name, current_date, current_time, software_version,
                                  custom_dpi)

                # Plotting figure of result spectrum logarithmic
                # plot_spectra_log_amplitude(frequency_axis, profile_spectrum, pulsar_period, pulsar_frequency,
                #                            pulsar_harmonics, max_harmonics, spectrum_max, frequency_limit,
                #                            n_harmonics, common_path + new_folder_name, filename, add_text,
                #                            current_date, current_time, software_version, custom_dpi)

                # Plotting figure of result spectrum linear
                plot_spectra_lin_amplitude(frequency_axis, profile_spectrum, pulsar_period, pulsar_frequency,
                                           pulsar_harmonics, max_harmonics, spectrum_max, frequency_limit, n_harmonics,
                                           common_path + new_folder_name, filename, add_text, current_date,
                                           current_time, software_version, custom_dpi)

            spectrum_max = np.max(harmonics_amplitudes[:, :])

            fig = plt.figure(figsize=(9.2, 4.5))
            rc('font', size=5, weight='bold')
            ax1 = fig.add_subplot(111)

            # Plotting lines where fundamental and other harmonics are expected
            ax1.axvline(x=pulsar_frequency, color='red', linestyle='-', linewidth=2.0, alpha=0.2)
            for i in range(n_harmonics):
                ax1.axvline(x=pulsar_harmonics[i], color='C1', linestyle='-', linewidth=2.0, alpha=0.1)

            # Adding calculated maximal point near harmonics as red dots
            for i in range(parts_num):
                plt.scatter(pulsar_harmonics, harmonics_amplitudes[i, :], marker='o', s=6.0, label='Part ' + str(i+1))
            ax1.axis([0, frequency_limit, 0, 1.1 * spectrum_max])
            ax1.legend(loc='upper right', fontsize=5)
            ax1.set_xlabel('Frequency, Hz', fontsize=6, fontweight='bold')
            ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
            ax1.set_title('File: ' + filename + '  Pulsar period: ' + str(np.round(pulsar_period, 3)) + ' s.',
                          fontsize=5, fontweight='bold')
            fig.suptitle('Single pulses of ' + pulsar_name + ' in frequency domain (linear amplitude) for ' +
                         str(parts_num) + ' parts', fontsize=7, fontweight='bold')
            fig.text(0.80, 0.04, 'Processed ' + current_date + ' at ' + current_time,
                     fontsize=3, transform=plt.gcf().transFigure)
            fig.text(0.09, 0.04, 'Software version: ' + software_version + ', yerin.serge@gmail.com, IRA NASU',
                     fontsize=3, transform=plt.gcf().transFigure)
            pylab.savefig(common_path + new_folder_name + '/' + filename[0:-4] + ' spectrum for ' +
                          str(parts_num) + ' parts.png', bbox_inches='tight', dpi=custom_dpi)
            plt.close('all')

    return


if __name__ == '__main__':

    print('\n\n\n\n\n\n   *********************************************************************************')
    print('   *   ', Software_name, ' v.', software_version, '   *      (c) YeS 2023')
    print('   ********************************************************************************* \n')

    start_time = time.time()
    previousTime = start_time

    time_profile_spectra(common_path, filename, pulsar_name, time_resolution, frequency_limit,
                         profile_pic_min, profile_pic_max, analyze_parts, software_version, custom_dpi)

    end_time = time.time()    # Time of calculations

    print('\n\n  The program execution lasted for ',
          round((end_time - start_time), 2), 'seconds (', round((end_time - start_time)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
