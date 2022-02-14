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


def show_amplitude_spectra(array):
    # integr_spectra_n = 20 * np.log10(np.sum(np.abs(np.fft.fftshift(fft_new[:, :])), axis=0) + 0.01)
    integr_spectra_n = 20 * np.log10(np.sum(np.abs((array[:, :])), axis=0) + 0.01)
    plt.figure()
    plt.plot(integr_spectra_n, linewidth='0.50', color='C3', alpha=0.7)
    plt.show()
    plt.close('all')
    return


def show_phase_spectra(array):
    integr_spectra_phase = np.angle(np.sum(array, axis=0))
    plt.figure()
    plt.plot(integr_spectra_phase, linewidth='0.50', color='C3', alpha=0.7)
    plt.show()
    plt.close('all')
    return


def rpr_wf_data_reader(filepath):
    """
    RT-32 Zolochiv Ukraine RPR receiver waveform data reader (not finished, just POC)
    """

    fft_length = 16384
    spectra_num = 8  # 8192  4096  # 2048  # 256

    with open(filepath) as f:  # Open data file
        f.seek(1024)  # Jump to 1024 byte in the file to skip the header
        # Read raw data from file in int8 format
        rdd = np.fromfile(f, dtype=np.int8, count=fft_length * spectra_num * 2 * 2)

        # Preparing empty matrix for complex data
        crd = np.empty(fft_length * spectra_num * 2, dtype=np.complex64)

        # Separating real and imaginary data from the raw data
        crd.real = rdd[0: fft_length * spectra_num * 2 * 2: 2]
        crd.imag = rdd[1: fft_length * spectra_num * 2 * 2: 2]
        del rdd

        # Reshaping complex data to separate data of channels
        rsh_crd = np.reshape(crd, (spectra_num, fft_length, 2))
        del crd
        rsh_crd = np.transpose(rsh_crd)

        # Separate data of channels
        tt0 = rsh_crd[0, :, :]
        # print('Shapes of separated channels (tt0, tt1):', tt0.shape, tt1.shape)

        # **************************************************************************************************************
        tt0_new = tt0.copy()
        print('Initial (complex) waveform data: ', tt0_new.shape, tt0_new.dtype)

        # Calculation of spectra
        fft_new = np.fft.fft(np.transpose(tt0_new))
        print('Shape of fft_new:', fft_new.shape, fft_new.dtype)

        # show_amplitude_spectra(fft_new)
        # show_phase_spectra(fft_new)

        # Preparing the array of zeros to concatenate with the spectra
        second_spectra_half = np.zeros_like(fft_new)

        # Concatenating second half of spectra with zeros
        spectra = np.concatenate((2 * fft_new, second_spectra_half), axis=1)

        # Making Inverse FFT
        wf_data = (np.fft.ifft(spectra))
        print(np.max(np.imag(wf_data)), np.min(np.imag(wf_data)))

        # We take only real part of the obtained waveform
        wf_data = np.real(wf_data)
        # wf_data = np.array(wf_data, dtype=np.int16)

        wf_data = np.clip(wf_data, -128, 127)
        wf_data = np.array(wf_data, dtype=np.int8)

        print('Inverse FFT result:', wf_data.shape, wf_data.dtype)
        print(np.max(wf_data), np.min(wf_data), np.mean(wf_data))

        # # Reshaping the waveform to single dimension (real)
        # wf_data_tmp = np.reshape(wf_data, [2 * fft_length * spectra_num, 1], order='F')
        # wf_data_tmp = np.squeeze(wf_data_tmp)
        # print('Processed waveform data: ', wf_data_tmp.shape, wf_data_tmp.dtype)
        # print(np.max(wf_data_tmp), np.min(wf_data_tmp), np.mean(wf_data_tmp))
        # print(wf_data_tmp[:18])

        # Calculation of spectra
        fft_new = np.fft.fft(wf_data)
        print('Shape of fft_new:', fft_new.shape, fft_new.dtype)

        # Cut the spectra of real waveform and double the magnitude
        fft_new = fft_new[:, :fft_length]
        fft_new = np.fft.fftshift(fft_new)

        # **************************************************************************************************************

        # Calculation of integrated spectra of initial (complex signal)
        fft_tt0 = np.fft.fft(np.transpose(tt0))

        # Remove current leak to the zero harmonic in spectra of initial (complex) signal
        fft_tt0[:, 0] = (np.abs(fft_tt0[:, 1]) + np.abs(fft_tt0[:, fft_length - 1])) / 2

        # Shifting spectra to show
        fft_tt0 = np.fft.fftshift(fft_tt0[:, :])

        # Calculate and show integrated spectra
        integr_spectra_0 = 20 * np.log10(np.sum(np.abs(fft_tt0), axis=0) + 0.01)
        integr_spectra_n = 20 * np.log10(np.sum(np.abs(fft_new), axis=0) + 0.01)

        plt.figure()
        plt.plot(integr_spectra_0, linewidth='0.50')
        plt.plot(integr_spectra_n, linewidth='0.50', color='C3', alpha=0.7)
        plt.show()
        plt.close('all')


def test_int8_to_2bit_words_conversion():
    # test_array = np.array(([int('11000000', 2), int('10000000', 2), int('11000000', 2), int('11000000', 2)],
    #                        [int('11000000', 2), int('11000000', 2), int('00000000', 2), int('11000000', 2)],
    #                        [int('11000000', 2), int('11000000', 2), int('11000000', 2), int('01000000', 2)]),
    #                       dtype=np.uint8)

    test_array = np.array(([192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192],
                           [192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192],
                           [192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192]),
                          dtype=np.uint8)
    # Separation of the 2 bits to group them into 32-bit word
    a0, a1, a2, a3 = int('11000000', 2), int('11000000', 2), int('11000000', 2), int('11000000', 2)
    t0, t1, t2, t3 = test_array[:, 0] & a0, test_array[:, 1] & a1, test_array[:, 2] & a2, test_array[:, 3] & a3
    print(t0, t1, t2, t3)
    byte_0 = t0 | t1 >> 2 | t2 >> 4 | t3 >> 6
    t0, t1, t2, t3 = test_array[:, 4] & a0, test_array[:, 5] & a1, test_array[:, 6] & a2, test_array[:, 7] & a3
    byte_1 = t0 | t1 >> 2 | t2 >> 4 | t3 >> 6
    t0, t1, t2, t3 = test_array[:, 8] & a0, test_array[:, 9] & a1, test_array[:, 10] & a2, test_array[:, 11] & a3
    byte_2 = t0 | t1 >> 2 | t2 >> 4 | t3 >> 6
    t0, t1, t2, t3 = test_array[:, 12] & a0, test_array[:, 13] & a1, test_array[:, 14] & a2, test_array[:, 15] & a3
    byte_3 = t0 | t1 >> 2 | t2 >> 4 | t3 >> 6

    print(byte_0)
    # for i in range(len(byte_0)):
    #     print(bin(byte_0[i]))

    # word_32_bit = byte_0 | byte_1 | byte_2 | byte_3
    byte_0 = np.uint32(byte_0)
    byte_1 = np.uint32(byte_1)
    byte_2 = np.uint32(byte_2)
    byte_3 = np.uint32(byte_3)

    word_32_bit = (byte_0 << 24) | (byte_1 << 16) | (byte_2 << 8) | byte_3

    print(word_32_bit)
    print(bin(word_32_bit[0]))
    # print(byte_0)
    # print(byte_0 << 2)
    # print(bin(word_32_bit))

    # test_array = np.array((1, 2, 3, 4, 5, 6))
    # print(test_array)
    # test_array = np.reshape(test_array, (2, 3))
    # print(test_array)
    # print(test_array[1, 2])
    # test_array = np.reshape(test_array, (1, 6))
    # print(test_array)

    return


if __name__ == '__main__':
    rpr_wf_data_reader(filepath)
    # test_int8_to_2bit_words_conversion()


