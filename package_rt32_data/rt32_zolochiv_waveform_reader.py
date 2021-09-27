# Python3
Software_version = '2021.08.28'
Software_name = 'RT-32 Zolochiv waveform reader'
# Script intended to read, show and analyze data from MARK5 receiver
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
directory = '../RA_DATA_ARCHIVE/'
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


def rpr_wf_header_reader(filepath):
    """
    !!! DEPRECATED !!! Use rpr_wf_header_reader_dict insted!
    Zolochiv Ukraine RPR receiver waveform data header reader (not finished, just POC)
    """
    with open(filepath, "rb") as file:
        df_file_size = os.stat(filepath).st_size  # Size of file

        fheader_tag = file.read(640)
        df_file_name = fheader_tag[0:32].decode('utf-8').rstrip('\x00')  # original name of the file
        df_file_loc_time = fheader_tag[32:58].decode('utf-8').rstrip('\x00')  # original name of the file
        # !!! In the real file bytes between 58 and 64 do not decode with utf-8 but has some info
        tmp = fheader_tag[58:64]
        # tmp = int.from_bytes(fheader_tag[58:64], byteorder='big', signed=True)

        df_file_gmt_time = fheader_tag[64:96].decode('utf-8').rstrip('\x00')  # time of the file creation
        df_file_sys_name = fheader_tag[96:128].decode('utf-8').rstrip('\x00')  # time of the file creation
        df_file_obs_place = fheader_tag[128:256].decode('utf-8').rstrip('\x00')  # time of the file creation
        df_file_obs_descr = fheader_tag[256:512].decode('utf-8').rstrip('\x00')  # time of the file creation

        # fheader_tag[512:640]  # uint32 processing and service parameters only for compatibility with old formats

        print('\n File to analyse:             ', filepath)
        print(' File size:                   ', round(df_file_size / 1024 / 1024, 3), ' Mb (', df_file_size, ' bytes )')
        print(' Initial file name:           ', df_file_name)
        print(' Initial file local time:     ', str(df_file_loc_time)[:-1])
        # print(' Unrecognized data from bytes 58:64: ', tmp)
        print(' Initial file GMT time:       ', df_file_gmt_time)
        print(' Receiver name:               ', df_file_sys_name)  # operator (can be used as name of the system)
        print(' Observation place:           ', df_file_obs_place)  # description of the measurements place
        print(' Observation description:     ', df_file_obs_descr)  # additional measurements description

        adrs_param_tag = file.read(28)
        df_adrs_mode = int.from_bytes(adrs_param_tag[0:4], byteorder='big', signed=True)
        df_fft_size = int.from_bytes(adrs_param_tag[4:8], byteorder='big', signed=True)
        df_aver_const = int.from_bytes(adrs_param_tag[8:12], byteorder='big', signed=True)
        df_fft_start_line = int.from_bytes(adrs_param_tag[12:16], byteorder='big', signed=True)
        df_fft_width = int.from_bytes(adrs_param_tag[16:20], byteorder='big', signed=True)
        df_block_size = int.from_bytes(adrs_param_tag[20:24], byteorder='big', signed=True)
        df_adc_freq = int.from_bytes(adrs_param_tag[20:24], byteorder='big', signed=True)

        print('\n Receiver mode:               ', df_adrs_mode)  # ADRS_MODE (0..2)WVF, (3..5)SPC, 6-CRL
        print(' FFT size:                    ', df_fft_size)  # 2048 ... 32768
        print(' Number of averaged spectra:  ', df_aver_const)  # 16 ... 1000
        print(' FFT start line:              ', df_fft_start_line)  # 0 ... 7, SLine*1024 first line for spectrum output
        print(' FFT width:                   ', df_fft_width)  # 2048 ... 32768
        print(' Data block size:             ', df_block_size)  # bytes, data block size calculated from data processing/output parameters
        print(' Measured ADC frequency:      ', df_adc_freq, ' Hz')  # ADC frequency reported by Astro-Digital-Receiver

        adrs_opt_tag = file.read(36)
        df_opt_size = int.from_bytes(adrs_opt_tag[0:4], byteorder='big', signed=True)
        df_opt_start_stop = int.from_bytes(adrs_opt_tag[4:8], byteorder='big', signed=True)
        df_opt_start_sec = int.from_bytes(adrs_opt_tag[8:12], byteorder='big', signed=True)
        df_opt_stop_sec = int.from_bytes(adrs_opt_tag[12:16], byteorder='big', signed=True)
        df_opt_test_mode = int.from_bytes(adrs_opt_tag[16:20], byteorder='big', signed=True)
        df_opt_norm_1 = int.from_bytes(adrs_opt_tag[20:24], byteorder='big', signed=True)
        df_opt_norm_2 = int.from_bytes(adrs_opt_tag[24:28], byteorder='big', signed=True)
        df_opt_delay = int.from_bytes(adrs_opt_tag[28:32], byteorder='big', signed=True)
        df_opt_bit_opt = int.from_bytes(adrs_opt_tag[32:36], byteorder='big', signed=True)

        '''
        ADRS options (data block size and format do not depends on)
        uint32_t  Opt;		// bit 0 - StartBySec: no(0)/yes(1)
                            // bit 1 - CLC: internal(0)/external(1)
                            // bit 2 - FFT Window: Hanning(0)/rectangle(1)
                            // bit 3 - DC removing: No(0)/Yes(1)
                            // bit 4 - averaging(0)/decimation(1)
                            // bit 5 - CH1: On(0)/Off(1)
                            // bit 6 - CH2: On(0)/Off(1)
        '''

        print('\n Size:                        ', df_opt_size)
        print(' Start / Stop:                ', df_opt_start_stop)  # StartStop 0/1	(-1 - ignore)
        print(' Start second:                ', df_opt_start_sec)  # abs.time.sec - processing starts
        print(' Stop second:                 ', df_opt_stop_sec)  # abs.time.sec - processing stops
        print(' Test mode:                   ', df_opt_test_mode)  # Test Mode: 0, 1, 2...
        print(' Norm. coefficient 1-CH:      ', df_opt_norm_1)  # Normalization coefficient 1-CH (1 ... 65535)
        print(' Norm. coefficient 2-CH       ', df_opt_norm_2)  # Normalization coefficient 2-CH (1 ... 65535)
        print(' Delay:                       ', df_opt_delay, ' ps')  # Delay in pico-seconds (-1000000000 ... 1000000000)
        print(' Options:                     ', df_opt_bit_opt)

        # print('Fheader tag 1:', fheader_tag[0:32])
        # print('Fheader tag 2:', fheader_tag[32:64])
        # print('F param tag:', adrs_param_tag)
        # print('F opt tag:', adrs_opt_tag)

    return


def rpr_wf_header_reader_dict(filepath):
    """
    Zolochiv Ukraine RPR receiver waveform data header reader (not finished, just POC)
    """

    param_dict = {}

    with open(filepath, "rb") as file:
        param_dict["File size in bytes"] = os.stat(filepath).st_size  # Size of file

        fheader_tag = file.read(640)
        param_dict["Initial file name"] = fheader_tag[0:32].decode('utf-8').rstrip('\x00')  # original name of the file
        param_dict["File creation local time"] = fheader_tag[32:58].decode('utf-8').rstrip('\x00')  # file creation local time
        # !!! In the real file bytes between 58 and 64 do not decode with utf-8 but has some info
        tmp = fheader_tag[58:64]
        # tmp = int.from_bytes(fheader_tag[58:64], byteorder='big', signed=True)

        param_dict["File creation utc time"] = fheader_tag[64:96].decode('utf-8').rstrip('\x00')
        param_dict["System name"] = fheader_tag[96:128].decode('utf-8').rstrip('\x00')
        param_dict["Observation place"] = fheader_tag[128:256].decode('utf-8').rstrip('\x00')
        param_dict["Observation description"] = fheader_tag[256:512].decode('utf-8').rstrip('\x00')

        # fheader_tag[512:640]  # uint32 processing and service parameters only for compatibility with old formats

        print('\n File to analyse:             ', filepath)
        print(' File size:                   ', round(param_dict["File size in bytes"] / 1024 / 1024, 3), ' Mb (',
              param_dict["File size in bytes"], ' bytes )')
        print(' Initial file name:           ', param_dict["Initial file name"])
        print(' Initial file local time:     ', str(param_dict["File creation local time"])[:-1])
        # print(' Unrecognized data from bytes 58:64: ', tmp)
        print(' Initial file GMT time:       ', param_dict["File creation utc time"])
        print(' Receiver name:               ', param_dict["System name"])  # operator (can be used as name of the system)
        print(' Observation place:           ', param_dict["Observation place"])  # description of the measurements place
        print(' Observation description:     ', param_dict["Observation description"])  # additional measurements description

        adrs_param_tag = file.read(28)
        param_dict["ADR mode"] = int.from_bytes(adrs_param_tag[0:4], byteorder='big', signed=True)
        param_dict["FFT size"] = int.from_bytes(adrs_param_tag[4:8], byteorder='big', signed=True)
        param_dict["Average constant"] = int.from_bytes(adrs_param_tag[8:12], byteorder='big', signed=True)
        param_dict["FFT start line"] = int.from_bytes(adrs_param_tag[12:16], byteorder='big', signed=True)
        param_dict["FFT width"] = int.from_bytes(adrs_param_tag[16:20], byteorder='big', signed=True)
        param_dict["Block size"] = int.from_bytes(adrs_param_tag[20:24], byteorder='big', signed=True)
        param_dict["ADC frequency, Hz"] = int.from_bytes(adrs_param_tag[20:24], byteorder='big', signed=True)

        print('\n Receiver mode:               ', param_dict["ADR mode"])  # ADRS_MODE (0..2)WVF, (3..5)SPC, 6-CRL
        print(' FFT size:                    ', param_dict["FFT size"])  # 2048 ... 32768
        print(' Number of averaged spectra:  ', param_dict["Average constant"])  # 16 ... 1000
        print(' FFT start line:              ', param_dict["FFT start line"])  # 0 ... 7, SLine*1024 first line for spectrum output
        print(' FFT width:                   ', param_dict["FFT width"])  # 2048 ... 32768
        print(' Data block size:             ', param_dict["Block size"])  # bytes, data block size calculated from data processing/output parameters
        print(' Measured ADC frequency:      ', param_dict["ADC frequency, Hz"], ' Hz')  # ADC frequency reported by Astro-Digital-Receiver

        adrs_opt_tag = file.read(36)
        param_dict["Opt size"] = int.from_bytes(adrs_opt_tag[0:4], byteorder='big', signed=True)
        param_dict["Start/stop switch"] = int.from_bytes(adrs_opt_tag[4:8], byteorder='big', signed=True)
        param_dict["Start second"] = int.from_bytes(adrs_opt_tag[8:12], byteorder='big', signed=True)
        param_dict["Stop second"] = int.from_bytes(adrs_opt_tag[12:16], byteorder='big', signed=True)
        param_dict["Test mode"] = int.from_bytes(adrs_opt_tag[16:20], byteorder='big', signed=True)
        param_dict["Norm coeff 1"] = int.from_bytes(adrs_opt_tag[20:24], byteorder='big', signed=True)
        param_dict["Norm coeff 2"] = int.from_bytes(adrs_opt_tag[24:28], byteorder='big', signed=True)
        param_dict["Channel delay"] = int.from_bytes(adrs_opt_tag[28:32], byteorder='big', signed=True)
        df_opt_bit_opt = int.from_bytes(adrs_opt_tag[32:36], byteorder='big', signed=True)

        '''
        ADRS options (data block size and format do not depends on)
        uint32_t  Opt;		// bit 0 - StartBySec: no(0)/yes(1)
                            // bit 1 - CLC: internal(0)/external(1)
                            // bit 2 - FFT Window: Hanning(0)/rectangle(1)
                            // bit 3 - DC removing: No(0)/Yes(1)
                            // bit 4 - averaging(0)/decimation(1)
                            // bit 5 - CH1: On(0)/Off(1)
                            // bit 6 - CH2: On(0)/Off(1)
        '''

        print('\n Size:                        ', param_dict["Opt size"])
        print(' Start / Stop:                ', param_dict["Start/stop switch"])  # StartStop 0/1	(-1 - ignore)
        print(' Start second:                ', param_dict["Start second"])  # abs.time.sec - processing starts
        print(' Stop second:                 ', param_dict["Stop second"])  # abs.time.sec - processing stops
        print(' Test mode:                   ', param_dict["Test mode"])  # Test Mode: 0, 1, 2...
        print(' Norm. coefficient 1-CH:      ', param_dict["Norm coeff 1"])  # Normalization coefficient 1-CH (1 ... 65535)
        print(' Norm. coefficient 2-CH       ', param_dict["Norm coeff 2"])  # Normalization coefficient 2-CH (1 ... 65535)
        print(' Delay:                       ', param_dict["Channel delay"], ' ps')  # Delay in pico-seconds (-1000000000 ... 1000000000)
        print(' Options:                     ', df_opt_bit_opt)

        # print('Fheader tag 1:', fheader_tag[0:32])
        # print('Fheader tag 2:', fheader_tag[32:64])
        # print('F param tag:', adrs_param_tag)
        # print('F opt tag:', adrs_opt_tag)

    return param_dict


def rpr_wf_data_reader(filepath):
    """
    RT-32 Zolochiv Ukraine RPR receiver waveform data reader (not finished, just POC)
    """

    nFFT = 64 * 256 * 1  # 16384 fop2
    # nGates = 4 * 64 * 1  # 256
    nGates = 8192  # 4096  # 2048  # 256
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

        # plt.figure()
        # plt.plot(20 * np.log10(np.sum(np.abs(np.fft.fftshift(fft_tt1)), axis=1) + 0.01), linewidth='0.20')
        # plt.show()
        # plt.close('all')


if __name__ == '__main__':
    rpr_wf_data_reader(filepath)
    # rpr_wf_header_reader(filepath)

