
import numpy as np
from progress.bar import IncrementalBar

from package_ra_data_files_formats.file_header_JDS import file_header_jds_read
from package_ra_data_files_formats.f_jds_header_new_channels_numbers import jds_header_new_channels_numbers

# *******************************************************************************
#          W A V E F O R M   F L O A T 3 2   T O   S P E C T R A                *
# *******************************************************************************


def convert_wf32_to_dat_with_overlap(fname, no_of_points_for_fft_spectr, no_of_spectra_in_bunch, use_window):
    """
        function converts waveform data in .wf32 format to spectra in .dat format
        : fname : name of .wf32 file with waveform data
        : no_of_points_for_fft : number of points for FFT to provide necessary time-frequency resolution
        : return : file_data_name - name of .dat file with result spectra
    """

    # *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
     clock_freq, df_time_utc, channel, receiver_mode, mode, n_avr, time_resolution, fmin, fmax,
     df, frequency, freq_points_num, data_block_size] = file_header_jds_read(fname, 0, 0)

    freq_points_num = int(no_of_points_for_fft_spectr / 2)

    with open(fname, 'rb') as file:
        file_header = file.read(1024)  # Data file header read

        # Create a binary file with spectra data for long data storage and make file header
        file_data_name = fname[:-5] + '.dat'
        file_data = open(file_data_name, 'wb')

        file_header = jds_header_new_channels_numbers(file_header, 0, freq_points_num,
                                                      fft_size=no_of_points_for_fft_spectr, n_avr=1)

        file_data.write(file_header)
        file_data.close()
        del file_header

        # Calculation of number of blocks and number of spectra in the file
        no_of_bunches_per_file = int((df_filesize - 1024) /
                                     ((no_of_spectra_in_bunch + 0.5) * no_of_points_for_fft_spectr * 4))

        # Real time resolution of averaged spectra
        fine_clock_freq = int(clock_freq / 1000000.0) * 1000000.0
        real_spectra_dt = float(no_of_points_for_fft_spectr / fine_clock_freq)
        real_spectra_df = float((fine_clock_freq / 2) / (no_of_points_for_fft_spectr / 2))

        print(' Number of spectra in bunch:                  ', no_of_spectra_in_bunch)
        print(' Sampling clock frequency:                    ', fine_clock_freq, ' Hz')
        print(' Number of bunches to read in file:           ', no_of_bunches_per_file)
        print(' Time resolution of calculated spectra:       ', round(real_spectra_dt * 1000, 3), ' ms')
        print(' Frequency resolution of calculated spectra:  ', round(real_spectra_df / 1000, 3), ' kHz \n')

        file.seek(1024)  # Jumping to 1024 byte from file beginning

        # *** Creating a new timeline TXT file for results ***
        new_tl_file_name = file_data_name.split('_Data_', 1)[0] + '_Timeline.txt'
        new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
        new_tl_file.close()

        # *** Reading timeline file ***
        old_tl_file_name = fname.split("_Data_", 1)[0] + '_Timeline.wtxt'
        old_tl_file = open(old_tl_file_name, 'r')
        new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name

        # Making the variable for half length of the spectrum for convenience
        half_of_spectrum = int(no_of_points_for_fft_spectr / 2)

        # Making a small buffer vector to store the last half ot spectrum for the next loop step
        buffer = np.zeros(half_of_spectrum)

        bar = IncrementalBar(' Conversion from waveform to spectra: ',
                             max=no_of_bunches_per_file - 1, suffix='%(percent)d%%')
        bar.start()

        for bunch in range(no_of_bunches_per_file - 1):

            # Read time from timeline file for the bunch
            time_scale_bunch = []
            for line in range(no_of_spectra_in_bunch):
                tmp = str(old_tl_file.readline())
                time_scale_bunch.append(tmp)  # append the current value
                time_scale_bunch.append(tmp)  # append once more the same value for timing of fft with overlap
            # Saving time data to new file
            for i in range(len(time_scale_bunch)):
                new_tl_file.write((time_scale_bunch[i][:]) + '')

            # Reading and reshaping data of the bunch
            wf_data = np.fromfile(file, dtype='f4', count=no_of_spectra_in_bunch * no_of_points_for_fft_spectr)

            wf_data = np.concatenate((buffer, wf_data), axis=0)

            # Save new data from the end to the buffer
            buffer = wf_data[-half_of_spectrum:].copy()

            # Selecting the needed sequence of the data and reshaping to rectangular array
            wf_data_1 = np.reshape(wf_data[: -half_of_spectrum].copy(),
                                   [no_of_points_for_fft_spectr, no_of_spectra_in_bunch], order='F')
            wf_data_2 = np.reshape(wf_data[half_of_spectrum:].copy(),
                                   [no_of_points_for_fft_spectr, no_of_spectra_in_bunch], order='F')
            wf_data_1 = np.transpose(wf_data_1)
            wf_data_2 = np.transpose(wf_data_2)
            del wf_data

            # Merging 2 arrays into one rectangular array in the one by one order
            wf_data = np.zeros((2 * no_of_spectra_in_bunch, no_of_points_for_fft_spectr))
            wf_data[0::2, :] = wf_data_1[:, :]
            wf_data[1::2, :] = wf_data_2[:, :]
            del wf_data_1, wf_data_2

            # Apply window to data for FFT
            if use_window:
                window = np.kaiser(no_of_points_for_fft_spectr, 5)
                wf_data[:] = wf_data[:] * window[:]
                del window

            # Preparing empty array for spectra
            spectra = np.zeros_like(wf_data, dtype=np.float64)

            # Calculation of spectra
            spectra[:] = np.power(np.abs(np.fft.fft(wf_data[:])), 2)
            del wf_data

            # Storing only first (left) mirror part of spectra
            spectra = spectra[:, : int(no_of_points_for_fft_spectr / 2)]

            # At 33 MHz clock frequency the specter is upside down, to correct it we use flip up/down
            if int(clock_freq / 1000000) == 33:
                spectra = np.fliplr(spectra)

            # Saving spectra data to dat file
            temp = spectra.copy(order='C')
            file_data = open(file_data_name, 'ab')
            file_data.write(np.float64(temp))
            file_data.close()

            bar.next()

        bar.finish()

    file.close()  # Close the data file
    return file_data_name


# def convert_wf32_to_dat_with_overlap(fname, no_of_points_for_fft_spectr, no_of_spectra_in_bunch, use_window):
#     """
#         function converts waveform data in .wf32 format to spectra in .dat format
#         : fname : name of .wf32 file with waveform data
#         : no_of_points_for_fft : number of points for FFT to provide necessary time-frequency resolution
#         : return : file_data_name - name of .dat file with result spectra
#     """
#
#     # *** Data file header read ***
#     [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
#      clock_freq, df_time_utc, channel, receiver_mode, mode, n_avr, time_resolution, fmin, fmax,
#      df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(fname, 0, 0)
#
#     freq_points_num = int(no_of_points_for_fft_spectr / 2)
#
#     with open(fname, 'rb') as file:
#         # *** Data file header read ***
#         file_header = file.read(1024)
#
#         # *** Creating a binary file with spectra data for long data storage ***
#         file_data_name = fname[:-5] + '.dat'
#         file_data = open(file_data_name, 'wb')
#         file_data.write(file_header)
#         file_data.seek(574)  # FFT size place in header
#         file_data.write(np.int32(no_of_points_for_fft_spectr).tobytes())
#         file_data.seek(624)  # Lb place in header
#         file_data.write(np.int32(0).tobytes())
#         file_data.seek(628)  # Hb place in header
#         file_data.write(np.int32(freq_points_num).tobytes())
#         file_data.seek(632)  # Wb place in header
#         file_data.write(np.int32(freq_points_num).tobytes())
#         file_data.seek(636)
#         file_data.write(np.int32(1).tobytes())  # Seem to work OK
#         file_data.close()
#         del file_header
#
#         # Calculation of number of blocks and number of spectra in the file
#         no_of_bunches_per_file = int((df_filesize - 1024) /
#                                      ((no_of_spectra_in_bunch + 0.5) * no_of_points_for_fft_spectr * 4))
#
#         # Real time resolution of averaged spectra
#         fine_clock_freq = int(clock_freq / 1000000.0) * 1000000.0
#         real_spectra_dt = float(no_of_points_for_fft_spectr / fine_clock_freq)
#         real_spectra_df = float((fine_clock_freq / 2) / (no_of_points_for_fft_spectr / 2))
#
#         print(' Number of spectra in bunch:                  ', no_of_spectra_in_bunch)
#         print(' Sampling clock frequency:                    ', fine_clock_freq, ' Hz')
#         print(' Number of bunches to read in file:           ', no_of_bunches_per_file)
#         print(' Time resolution of calculated spectra:       ', round(real_spectra_dt * 1000, 3), ' ms')
#         print(' Frequency resolution of calculated spectra:  ', round(real_spectra_df / 1000, 3), ' kHz \n')
#         # print('\n  Reading data from file \n')
#
#         file.seek(1024)  # Jumping to 1024 byte from file beginning
#
#         # *** Creating a new timeline TXT file for results ***
#         new_tl_file_name = file_data_name.split('_Data_', 1)[0] + '_Timeline.txt'
#         new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
#         new_tl_file.close()
#
#         # *** Reading timeline file ***
#         old_tl_file_name = fname.split("_Data_", 1)[0] + '_Timeline.wtxt'
#         old_tl_file = open(old_tl_file_name, 'r')
#         new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
#
#         # Making the variable for half length of the spectrum for convenience
#         half_of_spectrum = int(no_of_points_for_fft_spectr / 2)
#
#         # Making a small buffer vector to store the last half ot spectrum for the next loop step
#         buffer = np.zeros(half_of_spectrum)
#
#         bar = IncrementalBar(' Conversion from waveform to spectra: ',
#                              max=no_of_bunches_per_file - 1, suffix='%(percent)d%%')
#         bar.start()
#
#         for bunch in range(no_of_bunches_per_file - 1):
#
#             # print('Bunch # ', bunch, ' of ', no_of_bunches_per_file - 1)
#
#             # Read time from timeline file for the bunch
#             time_scale_bunch = []
#             for line in range(no_of_spectra_in_bunch):
#                 tmp = str(old_tl_file.readline())
#                 time_scale_bunch.append(tmp)  # append the current value
#                 time_scale_bunch.append(tmp)  # append once more the same value for timing of fft with overlap
#             # Saving time data to new file
#             for i in range(len(time_scale_bunch)):
#                 new_tl_file.write((time_scale_bunch[i][:]) + '')
#
#             # Reading and reshaping data of the bunch
#             wf_data = np.fromfile(file, dtype='f4', count=no_of_spectra_in_bunch * no_of_points_for_fft_spectr)
#
#             wf_data = np.concatenate((buffer, wf_data), axis=0)
#
#             # Save new data from the end to the buffer
#             buffer = wf_data[-half_of_spectrum:]
#
#             # Selecting the needed sequence of the data and reshaping to rectangular array
#             wf_data_1 = np.reshape(wf_data[: -half_of_spectrum],
#                                    [no_of_points_for_fft_spectr, no_of_spectra_in_bunch], order='F')
#             wf_data_2 = np.reshape(wf_data[half_of_spectrum:],
#                                    [no_of_points_for_fft_spectr, no_of_spectra_in_bunch], order='F')  # .copy()
#
#             del wf_data
#
#             # Merging 2 arrays into one rectangular array in the one by one order
#             wf_data = np.zeros((no_of_points_for_fft_spectr, 2 * no_of_spectra_in_bunch))
#             wf_data[:, 0::2] = wf_data_1[:, :]
#             wf_data[:, 1::2] = wf_data_2[:, :]
#             del wf_data_1, wf_data_2
#
#             # Apply window to data for FFT
#             if use_window:
#                 window = np.hanning(no_of_points_for_fft_spectr)
#                 for i in range(2 * no_of_spectra_in_bunch):
#                     wf_data[:, i] = wf_data[:, i] * window[:]
#                 # wf_data = np.multiply(np.transpose(wf_data), window)
#                 # wf_data = np.transpose(wf_data)
#                 del window
#
#             # Preparing empty array for spectra
#             spectra = np.zeros_like(wf_data)
#
#             # Calculation of spectra
#             for i in range(2 * no_of_spectra_in_bunch):
#                 spectra[:, i] = np.power(np.abs(np.fft.fft(wf_data[:, i])), 2)
#             del wf_data
#
#             # Storing only first (left) mirror part of spectra
#             spectra = spectra[: int(no_of_points_for_fft_spectr / 2), :]
#
#             # At 33 MHz clock frequency the specter is upside down, to correct it we use flip up/down
#             if int(clock_freq / 1000000) == 33:
#                 spectra = np.flipud(spectra)
#
#             # Saving spectra data to dat file
#             temp = spectra.transpose().copy(order='C')
#             file_data = open(file_data_name, 'ab')
#             file_data.write(np.float64(temp))
#             file_data.close()
#
#             bar.next()
#
#         bar.finish()
#
#     file.close()  # Close the data file
#     return file_data_name


# *******************************************************************************
#          W A V E F O R M   F L O A T 3 2   T O   S P E C T R A                *
# *******************************************************************************


def convert_wf32_to_dat_without_overlap(fname, no_of_points_for_fft_spectr, no_of_spectra_in_bunch):
    """
    Converts waveform data in .wf32 format to spectra in .dat format
    Input parameters:
        fname -                 name of .wf32 file with waveform data
        no_of_points_for_fft -  number of points for FFT to provide necessary time-frequency resolution
    Output parameters:
        file_data_name -        name of .dat file with result spectra
    """

    # *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        clock_freq, df_time_utc, channel, receiver_mode, mode, n_avr, time_resolution, fmin, fmax,
        df, frequency, freq_points_num, data_block_size] = file_header_jds_read(fname, 0, 0)

    freq_points_num = int(no_of_points_for_fft_spectr/2)

    with open(fname, 'rb') as file:
        # Data file header read
        file_header = file.read(1024)

        # Creating a binary file with spectra data for long data storage
        file_data_name = fname[:-5] + '.dat'
        file_data = open(file_data_name, 'wb')

        # Change data header according to new number of channels and other parameters
        file_header = jds_header_new_channels_numbers(file_header, 0, freq_points_num,
                                                      fft_size=no_of_points_for_fft_spectr, n_avr=1)

        file_data.write(file_header)
        file_data.close()
        del file_header

        # Calculation of number of blocks and number of spectra in the file
        no_of_bunches_per_file = int((df_filesize - 1024) / (no_of_spectra_in_bunch * no_of_points_for_fft_spectr * 4))

        # Real time resolution of averaged spectra
        fine_clock_freq = (int(clock_freq / 1000000.0) * 1000000.0)
        real_spectra_dt = float(no_of_points_for_fft_spectr / fine_clock_freq)
        real_spectra_df = float((fine_clock_freq / 2) / (no_of_points_for_fft_spectr / 2))

        print(' Number of spectra in bunch:                  ', no_of_spectra_in_bunch)
        print(' Number of bunches to read in file:           ', no_of_bunches_per_file)
        print(' Time resolution of calculated spectra:       ', round(real_spectra_dt*1000, 3), ' ms')
        print(' Frequency resolution of calculated spectra:  ', round(real_spectra_df/1000, 3), ' kHz')
        print('\n  *** Reading data from file *** \n')

        file.seek(1024)  # Jumping to 1024 byte from file beginning

        # *** Creating a new timeline TXT file for results ***
        new_tl_file_name = file_data_name.split('_Data_', 1)[0] + '_Timeline.txt'
        new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
        new_tl_file.close()

        # *** Reading timeline file ***
        old_tl_file_name = fname.split("_Data_", 1)[0] + '_Timeline.wtxt'
        old_tl_file = open(old_tl_file_name, 'r')
        new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name

        bar = IncrementalBar(' Conversion from waveform to spectra: ',
                             max=no_of_bunches_per_file-1, suffix='%(percent)d%%')

        for bunch in range(no_of_bunches_per_file-1):

            bar.next()

            # Read time from timeline file for the bunch
            time_scale_bunch = []
            for line in range(no_of_spectra_in_bunch):
                time_scale_bunch.append(str(old_tl_file.readline()))
            # Saving time data to new file
            for i in range(len(time_scale_bunch)):
                new_tl_file.write((time_scale_bunch[i][:]) + '')

            # Reading and reshaping data of the bunch
            wf_data = np.fromfile(file, dtype='f4', count=no_of_spectra_in_bunch * no_of_points_for_fft_spectr)
            wf_data = np.reshape(wf_data, [no_of_points_for_fft_spectr, no_of_spectra_in_bunch], order='F')

            #
            #
            #
            #
            #

            # window = np.hamming(no_of_points_for_fft_spectr)
            # window = np.kaiser(no_of_points_for_fft_spectr, 2)
            # for i in range(no_of_spectra_in_bunch):
            #     wf_data[:, i] = wf_data[:, i] * window[:]
            # del window

            #
            #
            #
            #
            #

            # preparing matrices for spectra
            spectra = np.zeros_like(wf_data)

            # Calculation of spectra
            for i in range(no_of_spectra_in_bunch):
                spectra[:, i] = np.power(np.abs(np.fft.fft(wf_data[:, i])), 2)

            # Storing only first (left) mirror part of spectra
            spectra = spectra[: int(no_of_points_for_fft_spectr/2), :]

            # At 33 MHz the specter is usually upside down, to correct it we use flip up/down
            if int(clock_freq/1000000) == 33:
                spectra = np.flipud(spectra)

            # Saving spectra data to dat file
            temp = spectra.transpose().copy(order='C')
            file_data = open(file_data_name, 'ab')
            file_data.write(np.float64(temp))
            file_data.close()

        bar.finish()

    file.close()  # Close the data file
    return file_data_name


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    no_of_points_for_fft_spectr = 16384     # Number of points for FFT on result spectra # 8192 - 131072
    no_of_spectra_in_bunch = 16384          # Number of spectra samples to read while conversion to dat (depends on RAM)
    fname = 'DM_5.755_E280120_205546.jds_Data_chA.wf32'

    # file_names = convert_wf32_to_dat_without_overlap(fname, no_of_points_for_fft_spectr, no_of_spectra_in_bunch)
    file_names = convert_wf32_to_dat_with_overlap(fname, no_of_points_for_fft_spectr, no_of_spectra_in_bunch, True)

    print('New wf32 files: ', file_names)
