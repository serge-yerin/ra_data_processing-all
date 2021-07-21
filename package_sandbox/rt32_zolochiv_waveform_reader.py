# Python3
Software_version = '2021.07.21'
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
import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('TkAgg')


# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


def rt32_data_reader(folderpath, filepath):
    """
    RT-32 waveform data reader - first iteration of data format
    """
    filepath = folderpath + filepath

    nFFT = 64 * 256 * 1  # 16384 fop2
    n_spectra = 8192  # 4096  # 2048  # 256

    # Calculate n_spectra from file size
    # df_filesize = os.stat(filepath).st_size         # Size of the file
    # print(' File size:                     ', round(df_filesize/1024/1024, 3), ' Mb (', df_filesize, ' bytes )')
    # n_spectra = (df_filesize - 5120) / (4 * nFFT)
    # print('Calculated n_spectra = ', n_spectra) 

    with open(filepath) as f:  # Open data file
        f.seek(5120)  # Jump to 5120 byte in the file
        # Read raw data from file in int8 format
        rdd = np.fromfile(f, dtype=np.int8, count=nFFT * n_spectra * 2 * 2)  # need numpy v1.17 for "offset=5120" ...
        print('Shape of data read from file:', rdd.shape)

        # Preparing empty matrix for complex data
        crd = np.empty(nFFT * n_spectra * 2, dtype=np.complex64)
        print('Shape of prepared complex data array:', crd.shape)

        # Separating real and imaginary data from the raw data
        crd.real = rdd[0: nFFT * n_spectra * 2 * 2: 2]
        crd.imag = rdd[1: nFFT * n_spectra * 2 * 2: 2]
        del rdd

        # Reshaping complex data to separate data of channels
        rsh_crd = np.reshape(crd, (n_spectra, nFFT, 2))
        del crd
        print('Shape of reshaped complex data array (rsh_crd) before transpose:', rsh_crd.shape)
        rsh_crd = np.transpose(rsh_crd)
        print('Shape of reshaped complex data array (rsh_crd) after transpose:', rsh_crd.shape)

        # Separate data of channels
        tt0 = rsh_crd[0, :, :]
        tt1 = rsh_crd[1, :, :]
        print('Shapes of separated channels (tt0, tt1):', tt0.shape, tt1.shape)

        # Display real and imaginary data of tt0 separately
        fig, axs = plt.subplots(2)
        axs[0].plot(np.real(tt0[:, 0]), linewidth='0.20', color='C0')
        axs[0].set_xlim([-50, 16500])
        axs[0].set_ylim([-150, 150])
        axs[1].plot(np.imag(tt0[:, 0]), linewidth='0.30', color='C1')
        axs[1].set_xlim([-10, 16400])
        axs[1].set_ylim([-150, 150])
        plt.show()
        plt.close('all')

        # Display spectra of the data in dB
        spectra_tt0 = 20 * np.log10(np.abs((np.fft.fftshift(np.fft.fft(tt0[:, 0])))) + 0.01)
        plt.figure()
        plt.plot(spectra_tt0, linewidth='0.20')
        plt.show()
        plt.close('all')

        # Calculation of integrated spectra
        fft_tt0 = np.fft.fft(np.transpose(tt0))
        print('Shape of fft_tt0:', fft_tt0.shape)
        #
        # Remove current leak to the zero harmonic
        fft_tt0[:, 0] = (np.abs(fft_tt0[:, 1]) + np.abs(fft_tt0[:, nFFT - 1])) / 2
        # print('Shape of fft_tt0[0]:', fft_tt0[0].shape)

        fft_tt1 = np.fft.fft(np.transpose(tt1))
        fft_tt1[:, 0] = (np.abs(fft_tt1[:, 1]) + np.abs(fft_tt1[:, nFFT - 1])) / 2

        # Calculate and show integrated spectra
        integr_spectra_0 = 20 * np.log10(np.sum(np.abs(np.fft.fftshift(fft_tt0)), axis=0) + 0.01)
        integr_spectra_1 = 20 * np.log10(np.sum(np.abs(np.fft.fftshift(fft_tt1)), axis=0) + 0.01)
        plt.figure()
        plt.plot(integr_spectra_0, linewidth='0.50')
        plt.plot(integr_spectra_1, linewidth='0.50')
        plt.show()
        plt.close('all')


if __name__ == '__main__':

    folderpath = 'DATA/'
    filepath = 'A210612_075610.adr'

    rt32_data_reader(folderpath, filepath)

