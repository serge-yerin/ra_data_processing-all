# Python3
Software_version = '2021.08.28'
Software_name = 'RT-32 Zolochiv waveform reader'
# Script intended to read, show and analyze data from MARK5 receiver
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
directory = '../RA_DATA_ARCHIVE/RT-32_Zolochiv_waveform_first_sample/'
filename = 'A210612_075610_rt32_waveform_first_sample.adr'
filepath = directory + filename
result_path = ''

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import sys
import numpy as np
from os import path
# import matplotlib.pyplot as plt
from matplotlib import pylab as plt
import os
import matplotlib
matplotlib.use('TkAgg')

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


def rpr_wf_data_reader(filepath):
    """
    RT-32 Zolochiv Ukraine RPR receiver waveform data reader (not finished, just POC)
    """

    nFFT = 64 * 256 * 1  # 16384 fop2
    # nGates = 4 * 64 * 1  # 256
    nGates = 256  # 8192  4096  # 2048  # 256
    # Calculate nGates from file size
    # df_filesize = os.stat(filepath).st_size         # Size of the file
    # print(' File size:                     ', round(df_filesize/1024/1024, 3), ' Mb (', df_filesize, ' bytes )')
    # nGates = (df_filesize - 5120) / (4 * nFFT)
    # print('Calculated nGates = ', nGates)

    with open(filepath) as f:  # Open data file
        f.seek(1024)  # Jump to 1024 byte in the file to skip the header
        # Read raw data from file in int8 format
        rdd = np.fromfile(f, dtype=np.int8, count=nFFT * nGates * 2 * 2)  # need numpy v1.17 for "offset=5120" ...
        print('Shape of data read from file:', rdd.shape)

        # Preparing empty matrix for complex data
        crd = np.empty(nFFT * nGates * 2, dtype=np.complex64)
        print('Shape of prepared complex data array:', crd.shape)

        # Separating real and imaginary data from the raw data
        crd.real = rdd[0: nFFT * nGates * 2 * 2: 2]
        crd.imag = rdd[1: nFFT * nGates * 2 * 2: 2]
        del rdd

        # Reshaping complex data to separate data of channels
        rsh_crd = np.reshape(crd, (nGates, nFFT, 2))
        del crd
        print('Shape of reshaped complex data array (rsh_crd) before transpose:', rsh_crd.shape)
        rsh_crd = np.transpose(rsh_crd)
        print('Shape of reshaped complex data array (rsh_crd) after transpose:', rsh_crd.shape)

        # Separate data of channels
        tt0 = rsh_crd[0, :, :]
        tt1 = rsh_crd[1, :, :]
        print('Shapes of separated channels (tt0, tt1):', tt0.shape, tt1.shape)

        # # Display real and imaginary data of tt0 separately
        # fig, axs = plt.subplots(2)
        # axs[0].plot(np.real(tt0[:, 0]), linewidth='0.20', color='C0')
        # axs[0].set_xlim([-50, 16500])
        # axs[0].set_ylim([-150, 150])
        # axs[1].plot(np.imag(tt0[:, 0]), linewidth='0.30', color='C1')
        # axs[1].set_xlim([-10, 16400])
        # axs[1].set_ylim([-150, 150])
        # plt.show()
        # plt.close('all')

        # # Display spectra of the data in dB
        # spectra_tt0 = 20 * np.log10(np.abs((np.fft.fftshift(np.fft.fft(tt0[:, 0])))) + 0.01)
        # plt.figure()
        # plt.plot(spectra_tt0, linewidth='0.20')
        # plt.show()
        # plt.close('all')

        # **************************************************************************************************************
        tt0_new = tt0.copy()
        tt0_new = np.squeeze(np.reshape(tt0_new, (nGates * nFFT, 1)))

        tt0_len = tt0_new.shape[0]
        print(tt0_new.shape, 'QQQ')
        real_data = np.zeros(2 * tt0_len, dtype=np.int8)
        print(np.arctan(tt0_new[0].imag / tt0_new[0].real))
        for i in range(tt0_len):
            real_data[2 * i] = np.sqrt(tt0_new[i].real ** 2 + tt0_new[i].imag ** 2) * \
                               np.cos(2 * np.pi * i + np.angle(tt0_new[i]))  # tt0_new[i].imag / tt0_new[i].real)
            real_data[2 * i + 1] = real_data[2 * i]

        # real_data = np.reshape(real_data, (nFFT, 2 * nGates))
        real_data = np.reshape(real_data, (2 * nFFT, nGates))
        # Calculation of integrated spectra
        fft_new = np.fft.fft(np.transpose(real_data))
        # **************************************************************************************************************

        # Calculation of integrated spectra
        fft_tt0 = np.fft.fft(np.transpose(tt0))
        print('Shape of fft_tt0:', fft_tt0.shape)
        print('Shape of fft_new:', fft_new.shape)
        #
        # Remove current leak to the zero harmonic
        fft_tt0[:, 0] = (np.abs(fft_tt0[:, 1]) + np.abs(fft_tt0[:, nFFT - 1])) / 2
        # print('Shape of fft_tt0[0]:', fft_tt0[0].shape)

        fft_tt1 = np.fft.fft(np.transpose(tt1))
        fft_tt1[:, 0] = (np.abs(fft_tt1[:, 1]) + np.abs(fft_tt1[:, nFFT - 1])) / 2

        # Calculate and show integrated spectra
        # integr_spectra_0 = 20 * np.log10(np.sum(np.abs(np.fft.fftshift(fft_tt0)), axis=0) + 0.01)
        # integr_spectra_1 = 20 * np.log10(np.sum(np.abs(np.fft.fftshift(fft_tt1)), axis=0) + 0.01)
        integr_spectra_0 = 20 * np.log10(np.sum(np.abs(fft_tt0), axis=0) + 0.01)
        integr_spectra_1 = 20 * np.log10(np.sum(np.abs(fft_tt1), axis=0) + 0.01)
        # integr_spectra_new = 20 * np.log10(np.sum(np.abs(fft_new), axis=0) + 0.01)
        integr_spectra_new = 20 * np.log10(np.sum(np.abs(fft_new[:, nFFT:]), axis=0) + 10.01)
        plt.figure()
        plt.plot(integr_spectra_0, linewidth='0.50')
        plt.plot(integr_spectra_1, linewidth='0.50')
        plt.plot(integr_spectra_new, linewidth='0.50')
        plt.show()
        plt.close('all')

        # plt.figure()
        # plt.plot(20 * np.log10(np.sum(np.abs(np.fft.fftshift(fft_tt1)), axis=1) + 0.01), linewidth='0.20')
        # plt.show()
        # plt.close('all')


if __name__ == '__main__':
    rpr_wf_data_reader(filepath)


