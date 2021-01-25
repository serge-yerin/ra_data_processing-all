
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


def cut_needed_time_points_from_txt(filename):
    """
    Function to cut the part of pulsar period data with the pulse ffrom one txt file to the new one
    """
    software_version = '2021.01.25'
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")

    file = open(filename, 'r')
    array = np.array([[float(digit) for digit in line.split()] for line in file])
    file.close()

    print('  Shape of the array: ', array.shape)

    fig = plt.figure(figsize=(12.0, 8.0))
    ax1 = fig.add_subplot(111)
    ax1.plot(np.mean(array, axis=0), linewidth='0.50')
    ax1.set_xlim(xmin=0, xmax=array.shape[1])
    ax1.set_xlabel('Time points to select', fontsize=6, fontweight='bold')
    ax1.set_ylabel('Amplitude, a.u.', fontsize=6, fontweight='bold')
    plt.show()

    start_point = int(input('\n  Begin from point: '))
    end_point = int(input('  End at point: '))

    result_array = array[:, start_point: end_point]
    del array

    print('  Shape of result array:', result_array.shape)

    single_pulse_txt = open('Incoherent sum of extracted pulses_selected_points.txt', "w")
    for freq in range(result_array.shape[0] - 1):
        single_pulse_txt.write(' '.join('  {:+12.7E}'.format(result_array[freq, i]) for i in range(result_array.shape[1])) + ' \n')
    single_pulse_txt.close()

    # Making result picture
    fig = plt.figure(figsize=(4.0, 6.0))
    gs = GridSpec(3, 2, figure=fig)
    rc('font', size=5, weight='bold')
    ax1 = fig.add_subplot(gs[0:2, 0])
    ax1.set_title('Cut time points: ' + str(start_point) + ' - ' + str(end_point), fontsize=5, fontweight='bold')
    ax1.imshow(np.flipud(result_array), aspect='auto', cmap=colormap, vmin=spectrum_pic_min, vmax=spectrum_pic_max)
    ax1.xaxis.set_ticklabels([])
    ax1.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
    ax2 = fig.add_subplot(gs[2, 0])
    ax2.plot(np.mean(result_array, axis=0), linewidth='0.50')
    ax2.set_xlim(xmin=0, xmax=result_array.shape[1])
    ax2.set_xlabel('Time points', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Amplitude, a.u.', fontsize=6, fontweight='bold')
    ax3 = fig.add_subplot(gs[0:2, 1:2])
    ax3.plot(np.mean(result_array, axis=1), np.linspace(0, 8191, 8191), linewidth='0.50')  # transform=rot+base
    ax3.set_ylim(ymin=0, ymax=result_array.shape[0])
    ax3.set_yticks([])
    ax3.set_xlabel('Amplitude, a.u.', fontsize=6, fontweight='bold')
    ax3.yaxis.set_ticklabels([])
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.axis('off')
    fig.subplots_adjust(hspace=0.00, wspace=0.00, top=0.93)
    fig.suptitle('Result pulse cut for further processing', fontsize=7, fontweight='bold')
    fig.text(0.80, 0.05, 'Processed ' + current_date + ' at '+current_time, fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.05, 'Software version: '+software_version+', yerin.serge@gmail.com, IRA NASU', fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig('Incoherent sum of extracted pulses_selected_points.png', bbox_inches='tight', dpi=customDPI)
    plt.close('all')

    return 0


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    common_path = 'RESULTS_pulsar_extracted_pulse_Norm_DM_5.755_E280120_205546.jds_Data_chA.dat/'
    filename = 'Norm_DM_5.755_E280120_205546.jds_Data_chA.dat - Extracted pulse.txt'
    cut_needed_time_points_from_txt(common_path + filename)  # 3550, 3600
