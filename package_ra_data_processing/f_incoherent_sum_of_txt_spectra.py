import time
import sys
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib import rc


def incoherent_sum_of_txt_spectra(common_path, filename_1, filename_2):
    """
    Function takes two 2D txt files with matrices and adds the matrices, makes another txt file and a figure
    """
    software_version = '2021.01.27'

    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d.%m.%Y")

    file = open(common_path + filename_1, 'r')
    array_1 = np.array([[float(digit) for digit in line.split()] for line in file])
    file.close()

    file = open(common_path + filename_2, 'r')
    array_2 = np.array([[float(digit) for digit in line.split()] for line in file])
    file.close()

    print('  Shape of first array: ', array_1.shape)
    print('  Shape of second array:', array_2.shape)
    if array_1.shape != array_2.shape:
        sys.exit('\n\n   Error!!! Arrays have different shapes!\n\n      Program stopped!')

    result_array = array_1 + array_2
    print('  Shape of result array:', result_array.shape)
    del array_1, array_2

    single_pulse_txt = open('Incoherent sum of extracted pulses.txt', "w")
    for freq in range(result_array.shape[0] - 1):
        single_pulse_txt.write(' '.join('  {:+12.7E}'.format(result_array[freq, i]) for i in range(result_array.shape[1])) + ' \n')
    single_pulse_txt.close()

    # Making result picture
    fig = plt.figure(figsize=(9.2, 4.5))
    rc('font', size=5, weight='bold')
    ax2 = fig.add_subplot(111)
    ax2.set_title(filename_1 + ' + ' + filename_2, fontsize=5, fontweight='bold')
    ax2.imshow(np.flipud(result_array), aspect='auto', cmap=colormap, vmin=spectrum_pic_min, vmax=spectrum_pic_max)
    ax2.set_xlabel('Time points', fontsize=6, fontweight='bold')
    ax2.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
    fig.subplots_adjust(hspace=0.05, top=0.91)
    fig.suptitle('Sum of two matrices', fontsize=7, fontweight='bold')
    fig.text(0.80, 0.04, 'Processed ' + current_date + ' at '+current_time, fontsize=3, transform=plt.gcf().transFigure)
    fig.text(0.09, 0.04, 'Software version: ' + software_version + ', yerin.serge@gmail.com, IRA NASU',
             fontsize=3, transform=plt.gcf().transFigure)
    pylab.savefig('Incoherent sum of extracted pulses.png', bbox_inches='tight', dpi=customDPI)
    plt.close('all')

    return 0


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':
    
    common_path = 'DATA/'      # Directory with JDS files to be analyzed
    filename_1 = 'file_1.txt'  # Text file of 2D dynamic spectra
    filename_2 = 'file_2.txt'  # Text file of 2D dynamic spectra

    incoherent_sum_of_txt_spectra(common_path, filename_1, filename_2)
