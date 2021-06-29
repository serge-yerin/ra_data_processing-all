
import sys
import numpy as np
import time
import pylab
import matplotlib.pyplot as plt
from os import path
from matplotlib import rc
from matplotlib.gridspec import GridSpec


# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


spectrum_pic_min = -0.2           # Minimum limit of dynamic spectrum picture
spectrum_pic_max = 3              # Maximum limit of dynamic spectrum picture
customDPI = 500                   # Resolution of images of dynamic spectra
colormap = 'Greys'                # Colormap of images of dynamic spectra ('jet' or 'Greys')


def cut_needed_time_points_from_txt(path, filename):
    import matplotlib
    matplotlib.use('TkAgg')

    """
    Function to cut the part of pulsar period data with the pulse from one txt file to the new smalled one
    User is asked to specify the start and stop point of the selected pulse period.
    Returns the start and stop point numbers, the data and image are saved to HDD
    """
    software_version = '2021.01.25'
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")

    file = open(path + '/' + filename, 'r')
    array = np.array([[float(digit) for digit in line.split()] for line in file])
    file.close()

    print('  Shape of the array: ', array.shape)

    # Show the pulse profile to select the start and end points of the cut
    fig = plt.figure(figsize=(16.0, 9.0))
    ax1 = fig.add_subplot(111)
    ax1.plot(np.mean(array, axis=0), linewidth='0.50')
    ax1.set_xlim(xmin=0, xmax=array.shape[1])
    ax1.tick_params(axis='both', which='major', labelsize=10)
    ax1.set_xlabel('Time points to select', fontsize=8, fontweight='bold')
    ax1.set_ylabel('Amplitude, a.u.', fontsize=8, fontweight='bold')
    plt.show()

    # Enter the points from the keyboard
    start_point = int(input('\n  Begin from point: '))
    end_point = int(input('  End at point: '))

    result_array = array[:, start_point: end_point]
    del array

    print('  Shape of result array:', result_array.shape)

    # Save cut data to the new txt file
    single_pulse_txt = open(path + '/Extracted pulse (selected_points).txt', "w")
    for freq in range(result_array.shape[0] - 1):
        single_pulse_txt.write(' '.join('  {:+12.7E}'.format(result_array[freq, i]) \
                                        for i in range(result_array.shape[1])) + ' \n')
    single_pulse_txt.close()

    # Making result figure
    fig = plt.figure(figsize=(8.0, 6.0))
    gs = GridSpec(3, 4, figure=fig)
    rc('font', size=5, weight='bold')
    ax1 = fig.add_subplot(gs[0:2, 0])
    ax1.set_title('Cut time points: ' + str(start_point) + ' - ' + str(end_point), fontsize=5, fontweight='bold')
    ax1.imshow(np.flipud(result_array), aspect='auto', cmap=colormap, vmin=spectrum_pic_min, vmax=spectrum_pic_max,
               extent=[0, result_array.shape[1], 16.5, 33.0])
    ax1.xaxis.set_ticklabels([])
    ax1.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
    ax2 = fig.add_subplot(gs[2, 0])
    ax2.plot(np.mean(result_array, axis=0), linewidth='0.50')
    ax2.set_xlim(xmin=0, xmax=result_array.shape[1])
    ax2.set_xlabel('Time points', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Amplitude, a.u.', fontsize=6, fontweight='bold')
    ax3 = fig.add_subplot(gs[0:2, 1:2])
    ax3.plot(np.mean(result_array, axis=1), np.linspace(0, len(result_array), len(result_array)), linewidth='0.50')
    ax3.axvline(x=0, linewidth=1, color='C1')
    ax3.set_ylim(ymin=0, ymax=result_array.shape[0])
    ax3.set_yticks([])
    ax3.set_xlabel('Amplitude, a.u.', fontsize=6, fontweight='bold')
    ax3.yaxis.set_ticklabels([])
    ax3.set_title('Frequency mean profile', fontsize=5, fontweight='bold')
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.axis('off')

    # Make an averaged profile of the pulse
    aver_num = 64
    freq_profile_aver = np.mean(result_array, axis=1)
    tmp = np.append(freq_profile_aver, 0)
    tmp = np.mean(tmp.reshape(-1, aver_num), axis=1)

    ax5 = fig.add_subplot(gs[0:2, 2:3])
    ax5.plot(tmp, np.linspace(0, len(tmp), len(tmp)), linewidth='0.50')
    ax5.axvline(x=0, linewidth=1, color='C1')
    ax5.set_ylim(ymin=0, ymax=tmp.shape[0])
    ax5.set_yticks([])
    ax5.set_xlabel('Amplitude, a.u.', fontsize=6, fontweight='bold')
    ax5.yaxis.set_ticklabels([])
    ax5.set_title(str(aver_num) + ' times averaged profile', fontsize=5, fontweight='bold')
    ax6 = fig.add_subplot(gs[2, 2])
    ax6.axis('off')
    ax6.text(0.5, 0.5, 'Pulsar:', ha='center', va='center')  # , color=text_color # <----------- added line

    # Make a maximum profile of the pulse
    freq_profile_max = np.max(result_array, axis=1)
    tmp_mean = np.mean(freq_profile_max)

    ax7 = fig.add_subplot(gs[0:2, 3:4])
    ax7.plot(freq_profile_max, np.linspace(0, len(freq_profile_max), len(freq_profile_max)), linewidth='0.50')
    ax7.axvline(x=tmp_mean, linewidth=1, color='C1')
    ax7.set_ylim(ymin=0, ymax=freq_profile_max.shape[0])
    ax7.set_yticks([])
    ax7.set_xlabel('Amplitude, a.u.', fontsize=6, fontweight='bold')
    ax7.yaxis.set_ticklabels([])
    ax7.set_title('Frequency max profile', fontsize=5, fontweight='bold')
    ax8 = fig.add_subplot(gs[2, 3])
    ax8.axis('off')

    fig.subplots_adjust(hspace=0.00, wspace=0.00, top=0.93)
    fig.suptitle('Result pulse cut for further processing', fontsize=7, fontweight='bold')
    fig.text(0.80, 0.05, 'Processed ' + current_date + ' at ' + current_time,
             fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.05, 'Software version: '+software_version+', yerin.serge@gmail.com, IRA NASU',
             fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig(path + '/Extracted pulse (selected_points).png', bbox_inches='tight', dpi=customDPI)
    plt.close('all')

    # # Making Fourier transform of the profiles
    #
    # aver_profile_sp = np.abs(np.fft.fft(freq_profile_aver)[int(len(freq_profile_aver)/2):])
    # max_profile_sp = np.abs(np.fft.fft(freq_profile_max)[int(len(freq_profile_max)/2):])
    #
    # # Making figure of profiles Fourier analysis
    # fig = plt.figure(figsize=(8.0, 6.0))
    # ax1 = fig.add_subplot(211)
    # ax1.plot(aver_profile_sp, linewidth='0.50')
    # ax1.set_title('Spectrum of average profile', fontsize=5, fontweight='bold')
    # ax1.set_ylabel('Amplitude, a.u.', fontsize=6, fontweight='bold')
    # ax2 = fig.add_subplot(212)
    # ax2.plot(max_profile_sp, linewidth='0.50')
    # ax2.set_title('Spectrum of maximal profile', fontsize=5, fontweight='bold')
    # ax2.set_ylabel('Amplitude, a.u.', fontsize=6, fontweight='bold')
    # pylab.savefig(path + '/Fourier analysis of pulse frequency profiles.png', bbox_inches='tight', dpi=customDPI)
    # plt.close('all')

    return start_point, end_point


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    common_path = 'RESULTS_pulsar_extracted_pulse_Norm_DM_5.755_E261015_035419.jds_Data_wfA+B.dat'
    filename = 'Norm_DM_5.755_E261015_035419.jds_Data_wfA+B.dat - Extracted pulse.txt'
    cut_needed_time_points_from_txt(common_path, filename)
