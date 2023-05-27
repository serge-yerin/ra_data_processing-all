# Python3
Software_version = '2023.05.27'
Software_name = 'Pulsar long time profile spectra calculation for various parts of files chunk'
# Program intended to read and fold pulsar data from DAT files to obtain average pulse
# *******************************************************************************
#                     M A N U A L    P A R A M E T E R S                        *
# *******************************************************************************
# Path to initial and results files
# common_path = '../../../RA_DATA_ARCHIVE/DSP_spectra_pulsar_UTR2_B0809+74/'
common_path = '../../../RA_DATA_ARCHIVE/DSP_spectra_pulsar_UTR2_B1919+21/'

# Name of TXT file to be analyzed:
# filename = 'B0809+74_DM_5.755_P130422_121607.jds_Data_chA_time_profile.txt'
filename = 'B1919+21_DM_12.4449_C040420_020109.jds_Data_chA_time_profile.txt'

# pulsar_name = 'B0809+74'
pulsar_name = 'B1919+21'

frequency_limit = 20  # MHz
n_harmonics = 50
max_interval = 20

time_resolution = (1 / 66000000) * 16384 * 32    # Data time resolution, s   # 0.007944

profile_pic_min = -0.1         # Minimum limit of profile picture
profile_pic_max = 0.5          # Maximum limit of profile picture
custom_dpi = 300               # Resolution of images of dynamic spectra

# *******************************************************************************

# *******************************************************************************
#                     I M P O R T   L I B R A R I E S                           *
# *******************************************************************************
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

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************


def time_profile_spectra(common_path, filename, pulsar_name, time_resolution, frequency_limit,
                         profile_pic_min, profile_pic_max, custom_dpi, n_harmonics=50, max_interval=10):

    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")

    data_filename = common_path + filename

    # Opening TXT file with pulsar observations long time profile
    profile_txt_file = open(data_filename, 'r')
    profile_data = []
    for line in profile_txt_file:
        profile_data.append(float(line))
    profile_txt_file.close()

    print('\n  Number of samples in text file:  ', len(profile_data))

    # Getting pulsar parameters from catalogue
    pulsar_ra, pulsar_dec, source_dm, pulsar_period = catalogue_pulsar(pulsar_name)

    # Data frequency resolution, Hz
    frequency_resolution = 1 / (time_resolution * len(profile_data))

    # Calculate pulsar harmonics frequency
    pulsar_frequency = 1 / pulsar_period  # frequency of pulses, Hz
    pulsar_harmonics = pulsar_frequency * np.linspace(1, n_harmonics)
    pulsar_harmonics_points = np.ceil(pulsar_harmonics / frequency_resolution).astype(int)

    print('  Pulsar frequency: ', pulsar_frequency, ' Hz')
    print('  Frequency resolution: ', frequency_resolution, ' s')
    print('  Time resolution: ', time_resolution, ' s')

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
    fig.text(0.09, 0.04, 'Software version: ' + Software_version + ', yerin.serge@gmail.com, IRA NASU', fontsize=3,
             transform=plt.gcf().transFigure)
    pylab.savefig(common_path + '/' + filename[0:-4] + ' time profile.png', bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')

    # *** Plotting figure of result spectrum logarithmic
    
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
    plt.scatter(pulsar_harmonics, max_harmonics, marker='o', color='red', s=0.6)
    ax1.axis([0, frequency_limit, 1, 1.5 * spectrum_max])
    plt.yscale('log')
    ax1.legend(loc='upper right', fontsize=5)
    ax1.set_xlabel('Frequency, Hz', fontsize=6, fontweight='bold')
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title('File: ' + filename + '  Pulsar period: ' + str(np.round(pulsar_period, 3)) + ' s.',
                  fontsize=5, fontweight='bold')
    fig.suptitle('Single pulses of ' + pulsar_name + ' in frequency domain (logarithmic amplitude)',
                 fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: ' + Software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig(common_path + '/' + filename[0:-4] + ' spectrum logarithmic.png', bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')

    # *** Plotting figure of result spectrum linear

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
    plt.scatter(pulsar_harmonics, max_harmonics, marker='o', color='red', s=0.6)
    ax1.axis([0, frequency_limit, -10, 1.1 * spectrum_max])
    ax1.legend(loc='upper right', fontsize=5)
    ax1.set_xlabel('Frequency, Hz', fontsize=6, fontweight='bold')
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title('File: ' + filename + '  Pulsar period: ' + str(np.round(pulsar_period, 3)) + ' s.',
                  fontsize=5, fontweight='bold')
    fig.suptitle('Single pulses of ' + pulsar_name + ' in frequency domain (linear amplitude)',
                 fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: ' + Software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig(common_path + '/' + filename[0:-4] + ' spectrum linear.png', bbox_inches='tight', dpi=custom_dpi)
    plt.close('all')

    return


if __name__ == '__main__':

    print('\n\n\n\n\n\n   **********************************************************************')
    print('   *   ', Software_name, ' v.', Software_version, '   *      (c) YeS 2023')
    print('   ********************************************************************** \n')

    start_time = time.time()
    previousTime = start_time

    time_profile_spectra(common_path, filename, pulsar_name, time_resolution, frequency_limit,
                         profile_pic_min, profile_pic_max, custom_dpi, n_harmonics, max_interval)

    end_time = time.time()    # Time of calculations

    print('\n\n  The program execution lasted for ',
          round((end_time - start_time), 2), 'seconds (', round((end_time - start_time)/60, 2), 'min. ) \n')
    print('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
