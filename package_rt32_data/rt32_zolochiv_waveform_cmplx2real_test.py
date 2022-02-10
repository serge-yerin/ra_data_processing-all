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
        print('Processed waveform data: ', tt0_new.shape, tt0_new.dtype)

        # Calculation of spectra
        fft_new = np.fft.fft(np.transpose(tt0_new))
        print('Shape of fft_new:', fft_new.shape, fft_new.dtype)

        # show_amplitude_spectra(fft_new)
        # show_phase_spectra(fft_new)

        # second_spectra_half = fft_new.copy()
        # second_spectra_half = np.fliplr(second_spectra_half)
        # second_spectra_half = np.conjugate(second_spectra_half)
        # spectra = np.concatenate((second_spectra_half, fft_new), axis=1)

        # second_spectra_half = fft_new.copy()
        # print(second_spectra_half[0, :2], second_spectra_half[0, -2:])
        #
        # second_spectra_half = np.conjugate(second_spectra_half)
        # print(second_spectra_half[0, :2], second_spectra_half[0, -2:])
        #
        # second_spectra_half = np.fliplr(second_spectra_half)
        # print(second_spectra_half[0, :2], second_spectra_half[0, -2:])
        #
        # second_spectra_half = np.roll(second_spectra_half, -1, axis=1)
        # print(second_spectra_half[0, :2], second_spectra_half[0, -2:], ' \n')
        #
        # second_spectra_half[:, -1] = 0
        # print(second_spectra_half[0, :2], second_spectra_half[0, -2:])
        #
        # spectra = np.concatenate((second_spectra_half, fft_new), axis=1)
        # print(spectra[0, :2], spectra[0, -2:])

        second_spectra_half = fft_new.copy()
        # print(second_spectra_half[0, :2], second_spectra_half[0, -2:])

        second_spectra_half = np.conjugate(second_spectra_half)
        print(second_spectra_half[0, :2], second_spectra_half[0, -2:])

        second_spectra_half = np.fliplr(second_spectra_half)
        print(second_spectra_half[0, :2], second_spectra_half[0, -2:])

        # second_spectra_half[:, -1] = 0
        fft_new[:, 0] = 0
        second_spectra_half = np.roll(second_spectra_half, 1, axis=1)
        # print(second_spectra_half[0, :2], second_spectra_half[0, -2:], ' \n')

        spectra = np.concatenate((fft_new, second_spectra_half), axis=1)
        print(spectra[0, :2], spectra[0, -2:])


        # array_0 = [1, -2, 3, -4, 5, -6, 7, -8]
        # sp = np.fft.fft(array_0)
        # array_1 = np.fft.ifft(sp)
        # print('\n\n', array_0)
        # print(array_1)
        # print(sp)
        # sp_sh = np.fft.fftshift(sp)
        # print(sp_sh)
        # sp_sh_inv = np.fft.ifftshift(sp_sh)
        # print(sp_sh_inv)
        # array_3 = np.fft.ifft(sp_sh)
        # print(array_3)
        #
        # sp_om = np.roll(sp, -1)
        # print('\n\n', sp)
        # print(sp_om)
        # array_om = np.fft.ifft(sp_om)
        # print(array_om)

        # show_amplitude_spectra(spectra)
        # show_phase_spectra(spectra)

        # Making IFFT
        wf_data = (np.fft.ifft(spectra))
        print(np.max(np.imag(wf_data)), np.min(np.imag(wf_data)))

        wf_data = np.real(wf_data)
        print('Inverse FFT result:', wf_data.shape, wf_data.dtype)

        # # Reshaping the waveform to single dimension (real)
        # wf_data = np.reshape(wf_data, [2 * fft_length * spectra_num, 1], order='F')
        # wf_data = np.squeeze(wf_data)
        #
        # print('Processed waveform data: ', wf_data.shape, wf_data.dtype)
        # print(np.max(wf_data), np.min(wf_data), np.mean(wf_data))
        # # print(wf_data[:18])

        # Calculation of spectra
        fft_new = np.fft.fft(wf_data)
        print('Shape of fft_new:', fft_new.shape, fft_new.dtype)

        # Cut the spectra of real waveform and double the magnitude
        fft_new = 1.0 * fft_new[:, fft_length:]
        fft_new = np.fft.fftshift(fft_new)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        fft_new = fft_new[:, ::-1]
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print('Shape of fft_new:', fft_new.shape, fft_new.dtype)

        # **************************************************************************************************************
        # tt0_new = np.squeeze(np.reshape(tt0_new, (spectra_num * fft_length, 1)))
        #
        # tt0_len = tt0_new.shape[0]
        # real_data = np.zeros(2 * tt0_len, dtype=np.int8)
        #
        # for i in range(tt0_len-2):
        #     real_data[2 * i] = tt0_new[i].imag
        #     real_data[2 * i + 1] = (tt0_new[i+1].imag + tt0_new[i+2].imag) / 2
        #
        # # real_data = np.reshape(real_data, (fft_length, 2 * spectra_num))
        # real_data = np.reshape(real_data, (2 * fft_length, spectra_num))
        #
        # # Calculation of integrated spectra
        # fft_new = np.fft.fft(np.transpose(real_data))
        # print('Shape of fft_new:', fft_new.shape)
        # **************************************************************************************************************

        # Calculation of integrated spectra
        fft_tt0 = np.fft.fft(np.transpose(tt0))
        print('Shape of fft_tt0:', fft_tt0.shape, fft_new.dtype)

        # print(fft_tt0[:, 0])

        # Remove current leak to the zero harmonic
        fft_tt0[:, 0] = (np.abs(fft_tt0[:, 1]) + np.abs(fft_tt0[:, fft_length - 1])) / 2

        fft_tt0 = np.fft.fftshift(fft_tt0[:, :])

        # show_amplitude_spectra(fft_tt0)
        # show_phase_spectra(fft_tt0)

        # Calculate and show integrated spectra
        integr_spectra_0 = 20 * np.log10(np.sum(np.abs(fft_tt0), axis=0) + 0.01)
        integr_spectra_n = 20 * np.log10(np.sum(np.abs(fft_new), axis=0) + 0.01)

        plt.figure()
        plt.plot(integr_spectra_0, linewidth='0.50')
        plt.plot(integr_spectra_n, linewidth='0.50', color='C3', alpha=0.7)
        plt.show()
        plt.close('all')

        # plt.figure()
        # plt.plot(integr_spectra_0 - integr_spectra_n, linewidth='0.50')
        # plt.show()
        # plt.close('all')


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


