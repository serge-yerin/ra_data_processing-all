# Python3
Software_version = '2021.06.28'
Software_name = 'RT-32 Zolochiv waveform reader'
# Script intended to read, show and analyze data from MARK5 receiver
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
directory = 'DATA/'
filename = 'A210612_075610.adr'
result_path = ''

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import sys
import numpy as np
from os import path
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib import rc
import pylab
import os
import time
import matplotlib
matplotlib.use('TkAgg')


# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


def mark_5_data_header_read():
    """
    RT-32 waveform data reader ?
    """

    nGates = 4 * 64 * 1
    nFFT = 64 * 256 * 1

    # inX = np.linspace(0, nFFT * nGates - 1)
    even = np.arange(1, nFFT * nGates * 2 * 2+1, 2)
    odd = np.arange(0, nFFT * nGates * 2 * 2, 2)

    print(even)
    print(odd)

    i = 0
    # rsh_crd = np.zeros(2, nFFT, nGates)
    # tt = []
    # wind = np.hamming(nFFT)
    # for i in range(1):
    file = open(directory + filename, 'r')
    file.seek(5120 + (1 - 1) * 1327244)   # FFTD block 320 gates
    data = np.fromfile(file, dtype='i', count=int(nFFT * nGates * 2 * 2))
    print(data)
    print(data.shape)
    # data = file.read(nFFT * nGates * 2 * 2, 'int8')
    file.close()
    data_re = data[odd]
    data_im = data[even]
    print('Re shape', data_re.shape)
    del data
    cmplx_data = data_re + 1j * data_im  # np.complex(,)
    rsh_crd = np.reshape(cmplx_data, [2, nFFT, nGates])

    # tt0 = np.zeros((nFFT, nGates))
    tt1 = np.zeros((nFFT, nGates))

    # tt0[:, :] = rsh_crd[1, :, :] - 0.0 * np.sum(rsh_crd[1, :, :], 2) / nFFT
    # tt1[:, :] = rsh_crd[2, :, :] - 0.0 * np.sum(rsh_crd[2, :, :], 2) / nFFT

    # tt0[:, :] = rsh_crd[0, :, :] / nFFT
    tt1[:, :] = rsh_crd[1, :, :] / nFFT

    fig = plt.figure(1, figsize=(12.0, 5.0))
    ax1 = fig.add_subplot(111)
    ax1.plot(np.real(tt1[0, 0:200]), label='Real')
    ax1.plot(np.real(tt1[1, 0:200]), label='Real')
    # ax1.plot(np.imag(tt1), label='Imag')
    # pylab.savefig(result_path + 'RT-32_waveform_fig.' + str(1) + ' of ' + str(1) + '.png',
    #               bbox_inches='tight', dpi=200)
    plt.show()
    plt.close('all')


if __name__ == '__main__':
    mark_5_data_header_read()


################################################################################

# if __name__ == '__main__':
#
#     print('\n\n\n\n\n\n\n\n   **************************************************************************')
#     print('   *               ', Software_name, ' v.', Software_version, '              *      (c) YeS 2018')
#     print('   ************************************************************************** \n')
#
#     startTime = time.time()
#     currentTime = time.strftime("%H:%M:%S")
#     currentDate = time.strftime("%d.%m.%Y")
#     print('   Today is ', currentDate, ' time is ', currentTime, '\n')
#
#     # *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
#     result_path = 'RESULTS_MARK5_Reader'
#     if not os.path.exists(result_path):
#         os.makedirs(result_path)
#
#     filepath = directory + filename
#
#     file_size = (os.stat(filepath).st_size)  # Size of file
#     print('\n   File size:                    ', round(file_size / 1024 / 1024, 3), ' Mb (', file_size, ' bytes )')
#
#     with open(filepath, 'rb') as file:
#
#