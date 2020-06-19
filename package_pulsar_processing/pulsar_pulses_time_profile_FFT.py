# Python3
Software_version = '2020.03.15'
Software_name = 'Pulsar long time profile spectrum calculation'
# Program intended to read and fold pulsar data from DAT files to obtain average pulse
# *******************************************************************************
#                     M A N U A L    P A R A M E T E R S                        *
# *******************************************************************************
# Path to initial and results files
common_path = 'RESULTS_pulsar_single_pulses_B0000+00_B0000+00_DM_7.0_E290120_201402.jds_Data_chA.dat/'

# Name of TXT file to be analyzed:
filename = 'B0000+00_DM_7.0_E290120_201402.jds_Data_chA.dat_time_profile.txt'

pulsar_name = 'J0740+6620'

time_resolution = 0.007944     # Data time resolution, s   # 0.007944

spectrum_max = 2000

profile_pic_min = -0.1         # Minimum limit of profile picture
profile_pic_max = 0.5          # Maximum limit of profile picture
customDPI = 300                # Resolution of images of dynamic spectra
colormap = 'Greys'             # Colormap of images of dynamic spectra ('jet' or 'Greys')


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

# ###############################################################################

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************

def pulsar_pulses_time_profile_FFT (common_path, filename, pulsar_name, time_resolution,
                                       profile_pic_min, profile_pic_max, customDPI, colormap):


    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")

    data_filename = common_path + filename


    # ************************************************************************************
    #                             R E A D I N G   D A T A                                *
    # ************************************************************************************

    # Opening TXT file with pulsar observations long time profile
    profile_txt_file = open(data_filename, 'r')
    profile_data = []
    for line in profile_txt_file:
        profile_data.append(np.float(line))
    profile_txt_file.close()

    print ('\n  Number of samples in text file:  ', len(profile_data), ' \n')

    pulsar_ra, pulsar_dec, DM, pulsar_period = catalogue_pulsar(pulsar_name)

    pulsar_frequency = 1 / pulsar_period  # frequency of pulses, Hz
    frequency_resolution = 1 / (time_resolution * len(profile_data)) # frequency resolution, Hz


    profile_spectrum = np.power(np.real(np.fft.fft(profile_data[:])),2)  # calculation of the spectrum
    profile_spectrum = profile_spectrum[0:int(len(profile_spectrum)/2)]  # delete second part of the spectrum

    profile_spectrum[0:100] = 0.0

    frequency_axis = [frequency_resolution * i for i in range(len(profile_spectrum))]


    # Making result picture
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')
    ax1 = fig.add_subplot(211)
    ax1.plot(profile_data, color=u'#1f77b4', linestyle='-', alpha=1.0, linewidth='0.60', label='Pulses time profile')
    ax1.legend(loc='upper right', fontsize=5)
    ax1.grid(b=True, which='both', color='silver', linewidth='0.50', linestyle='-')
    ax1.axis([0, len(profile_data), profile_pic_min, profile_pic_max])
    ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    ax1.set_title('File: ' + filename + '  Pulsar period: '+str(np.round(pulsar_period,3))+' s.', fontsize=5, fontweight='bold')
    ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax2 = fig.add_subplot(212)
    ax2.axvline(x = pulsar_frequency, color = 'C1', linestyle = '-', linewidth = 2.0, alpha=0.5, label='Frequency of pulses')
    ax2.plot(frequency_axis, profile_spectrum, color=u'#1f77b4', linestyle='-', alpha=1.0, linewidth='0.60', label='Time series spectrum')
    ax2.axis([frequency_axis[0], frequency_axis[-1], -np.max(profile_spectrum)*0.05, np.max(profile_spectrum)*1.05])  #
    #ax2.axis([frequency_axis[0], frequency_axis[-1], -10, spectrum_max])
    ax2.legend(loc='upper right', fontsize=5)
    ax2.set_xlabel('Frequency, Hz', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
    fig.subplots_adjust(hspace=0.05, top=0.91)
    fig.suptitle('Single pulses of ' + pulsar_name + ' in time and frequency', fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: ' + Software_version + ', yerin.serge@gmail.com, IRA NASU', fontsize=3,
             transform=plt.gcf().transFigure)
    pylab.savefig(common_path + '/' + filename[0:-4] + ' and its spectrum.png', bbox_inches='tight', dpi=customDPI)
    plt.close('all')

    return



if __name__ == '__main__':

    print ('\n\n\n\n\n\n\n\n   **********************************************************************')
    print ('   *   ', Software_name,' v.',Software_version,'   *      (c) YeS 2020')
    print ('   ********************************************************************** \n\n\n')

    startTime = time.time()
    previousTime = startTime

    pulsar_pulses_time_profile_FFT(common_path, filename, pulsar_name, time_resolution,
                                     profile_pic_min, profile_pic_max, customDPI, colormap)



    endTime = time.time()    # Time of calculations

    print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                    round((endTime - startTime)/60, 2), 'min. ) \n')
    print ('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
