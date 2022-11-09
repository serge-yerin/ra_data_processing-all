

import pylab
import numpy as np
import matplotlib.pyplot as plt
from progress.bar import IncrementalBar

from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_pulsar_processing.pulsar_dm_full_shift_calculation import dm_full_shift_calculate
from package_pulsar_processing.pulsar_dm_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes


# *******************************************************************************
#        WAVEFORM FLOAT32 TO WAVEFORM FLOAT32 COHERENT DEDISPERSION             *
# *******************************************************************************


def coherent_wf_to_wf_dedispersion(pulsar_dm, file_path, no_of_points_for_fft_dedisp):
    """
    function reads waveform data in wf32 format, makes FFT, cuts the symmetrical half of the spectra and shifts the
    lines of complex data to provide coherent dedispersion. Then a symmetrcal part of spectra are made and joined
    to the shifted one, inverse FFT as applied and data are stored in waveform wf32 format
    Input parameters:
        pulsar_dm -                            dispersion measure to compensate
        file_path -                     path and name of file with initial wf32 data
        no_of_points_for_fft_dedisp -   number of waveform data points to use for FFT
    Output parameters:
        file_data_name -                name of file with processed data
    """

    #  *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
     clock_freq, df_creation_time_utc, channel, receiver_mode, mode, n_avr, time_resolution, fmin, fmax,
     df, frequency_list, freq_points_num, data_block_size] = file_header_jds_read(file_path, 0, 0)

    # Manually set frequencies for one channel mode
    freq_points_num = int(no_of_points_for_fft_dedisp / 2)

    # Manually set frequencies for 33 MHz clock frequency
    if int(clock_freq / 1000000) == 33:
        fmin = 16.5
        fmax = 33.0
        df = 16500000 / freq_points_num

    # Create long data files and copy first data file header to them

    fname = file_path.split('/')[-1]
    fpath = '/'.join(file_path.split('/')[:-1]) + '/'

    with open(file_path, 'rb') as file:
        # *** Data file header read ***
        file_header = file.read(1024)

        # Removing old DM from file name and updating it to current value
        if fname.startswith('DM_'):
            prev_dm_str = fname.split('_')[1]
            prev_dm = np.float32(prev_dm_str)
            new_dm = prev_dm + pulsar_dm
            n = len('DM_' + prev_dm_str + '_')
            file_data_name = 'DM_' + str(np.round(new_dm, 6)) + '_' + fname[n:]
        else:
            file_data_name = 'DM_' + str(np.round(pulsar_dm, 6)) + '_' + fname

        # *** Creating a binary file with data for long data storage ***
        file_data = open(fpath + file_data_name, 'wb')
        file_data.write(file_header)
        file_data.close()
        del file_header

        # *** Creating a new timeline TXT file for results ***
        new_tl_file_name = file_data_name.split("_Data_ch", 1)[0] + '_Timeline.wtxt'
        new_tl_file = open(fpath + new_tl_file_name, 'w')  # Open and close to delete the file with the same name
        new_tl_file.close()

        # Calculation of the time shifts
        shift_vector = dm_full_shift_calculate(freq_points_num, fmin, fmax, df / pow(10, 6),
                                               time_resolution, pulsar_dm, 'jds')
        max_shift = np.abs(shift_vector[0])

        # Preparing buffer array
        buffer_array = np.zeros((freq_points_num, 2 * max_shift), dtype='complex64')

        print(' Maximal shift is:                            ', max_shift, ' pixels ')
        print(' Dispersion measure:                          ', pulsar_dm, ' pc / cm3 ')

        # Calculation of number of blocks and number of spectra in the file
        no_of_spectra_in_bunch = max_shift.copy()
        no_of_bunches_per_file = int(np.ceil((df_filesize - 1024)
                                             / (no_of_spectra_in_bunch * no_of_points_for_fft_dedisp * 4)))

        # Real time resolution of spectra
        fine_clock_freq = (int(clock_freq / 1000000.0) * 1000000.0)
        real_spectra_dt = float(no_of_points_for_fft_dedisp / fine_clock_freq)
        real_spectra_df = float((fine_clock_freq / 2) / (no_of_points_for_fft_dedisp / 2))

        print(' Number of spectra in bunch:                  ', no_of_spectra_in_bunch)
        print(' Number of bunches to read in file:           ', no_of_bunches_per_file)
        print(' Time resolution of calculated spectra:       ', round(real_spectra_dt * 1000, 3), ' ms')
        print(' Frequency resolution of calculated spectra:  ', round(real_spectra_df / 1000, 3), ' kHz \n')

        # !!! Fake timing. Real timing to be done!!!
        # *** Reading timeline file ***
        old_tl_file_name = fname.split("_Data_ch", 1)[0] + '_Timeline.wtxt'
        old_tl_file = open(fpath + old_tl_file_name, 'r')
        new_tl_file = open(fpath + new_tl_file_name, 'w')  # Open and close to delete the file with the same name

        file.seek(1024)  # Jumping to 1024 byte from file beginning

        bar = IncrementalBar(' Coherent dispersion delay removing: ', max=no_of_bunches_per_file,
                             suffix='%(percent)d%%')
        bar.start()

        # for bunch in range(no_of_bunches_per_file - 1):
        for bunch in range(no_of_bunches_per_file):

            # Trying to read all the file, not only integer number of bunches
            if bunch >= no_of_bunches_per_file - 1:

                # Make sure all the variables are int, otherwise we can get overflow
                df_filesize = int(df_filesize)
                no_of_points_for_fft_dedisp = int(no_of_points_for_fft_dedisp)
                bunch = int(bunch)
                max_shift = int(max_shift)
                no_of_spectra_in_bunch = int(((df_filesize - 1024) -
                                              bunch * max_shift * no_of_points_for_fft_dedisp * 4) //
                                             (no_of_points_for_fft_dedisp * 4))

                # print('\n  Bunch No ', str(bunch+1), ' of ', no_of_bunches_per_file, ' bunches')
                # print('\n  Number of spectra in the last bunch is: ', no_of_spectra_in_bunch)
                # print('\n  Maximal shift is:                       ', max_shift)
            # Read time from timeline file for the bunch
            time_scale_bunch = []
            for line in range(no_of_spectra_in_bunch):
                time_scale_bunch.append(str(old_tl_file.readline()))

            # Reading and reshaping all data with time data
            wf_data = np.fromfile(file, dtype='f4', count=no_of_spectra_in_bunch * no_of_points_for_fft_dedisp)

            '''
            fig = plt.figure(figsize=(9, 5))
            ax1 = fig.add_subplot(111)
            ax1.plot(wf_data, linestyle='-', linewidth='1.00', label='Initial waveform')
            ax1.legend(loc='upper right', fontsize=6)
            ax1.grid(b=True, which='both', color='silver', linestyle='-')
            ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
            pylab.savefig('00_Initial_waveform_' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
            plt.close('all')
            '''

            wf_data = np.reshape(wf_data, [no_of_points_for_fft_dedisp, no_of_spectra_in_bunch], order='F')

            # preparing matrices for spectra
            spectra = np.zeros((no_of_points_for_fft_dedisp, no_of_spectra_in_bunch), dtype='complex64')

            # Calculation of spectra
            for i in range(no_of_spectra_in_bunch):
                spectra[:, i] = np.fft.fft(wf_data[:, i])
            del wf_data

            '''
            fig = plt.figure(figsize=(9, 5))
            ax1 = fig.add_subplot(111)
            ax1.plot(10 * np.log10(np.power(np.abs(spectra[:, 0]), 2)), linestyle='-', linewidth='1.00',
                     label='Initial spectra before cut')
            ax1.legend(loc='upper right', fontsize=6)
            ax1.grid(b=True, which='both', color='silver', linestyle='-')
            ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
            pylab.savefig('00a_Initial_doubled_imm_spectra' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
            plt.close('all')
            '''

            # Cut half of the spectra
            spectra = spectra[int(no_of_points_for_fft_dedisp / 2):, :]

            ''' # making figures
            fig = plt.figure(figsize=(9, 5))
            ax1 = fig.add_subplot(111)
            ax1.imshow(np.flipud(10*np.log10(np.power(np.abs(spectra), 2))), aspect='auto', cmap='jet')
            ax1.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
            ax1.set_xlabel('Time points', fontsize=6, fontweight='bold')
            pylab.savefig('01_Initial_spectra_' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
            plt.close('all')

            fig = plt.figure(figsize=(9, 5))
            ax1 = fig.add_subplot(111)
            ax1.plot(10*np.log10(np.power(np.abs(spectra[:, 0]), 2)), linestyle='-', linewidth='1.00', label='Initial waveform')
            ax1.legend(loc='upper right', fontsize=6)
            ax1.grid(b=True, which='both', color='silver', linestyle='-')
            ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
            pylab.savefig('02_Initial_imm_spectra' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
            plt.close('all')
            '''

            #  Dispersion delay removing
            data_space = np.zeros((freq_points_num, 2 * max_shift), dtype='complex64')

            # if it is the last bunch - use only available data
            if bunch >= no_of_bunches_per_file - 1:
                data_space[:, max_shift:max_shift + no_of_spectra_in_bunch] = spectra[:, :]
            else:
                data_space[:, max_shift:] = spectra[:, :]

            data_space = pulsar_DM_compensation_with_indices_changes(data_space, shift_vector)
            del spectra

            # Adding the next data block
            buffer_array += data_space

            # Making and filling the array with fully ready data for plotting and saving to a file
            if bunch >= no_of_bunches_per_file - 1:
                array_compensated_dm = buffer_array[:, 0: no_of_spectra_in_bunch]
            else:
                array_compensated_dm = buffer_array[:, 0: max_shift]

            if bunch > 0:

                # Saving time data to a new file
                for i in range(len(time_scale_bunch)):
                    new_tl_file.write((time_scale_bunch[i][:]) + '')

                # Saving data with compensated DM
                spectra = array_compensated_dm  # .copy()

                '''
                # making figures
                fig = plt.figure(figsize=(9, 5))
                ax1 = fig.add_subplot(111)
                ax1.imshow(np.flipud(10*np.log10(np.power(np.abs(spectra), 2))), aspect='auto', cmap='jet')
                ax1.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
                ax1.set_xlabel('Time points', fontsize=6, fontweight='bold')
                pylab.savefig('03_Compensated_spectra_' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
                plt.close('all')

                fig = plt.figure(figsize=(9, 5))
                ax1 = fig.add_subplot(111)
                ax1.plot(10*np.log10(np.power(np.abs(spectra[:,0]), 2)), linestyle='-', linewidth='1.00', label='Initial waveform')
                ax1.legend(loc='upper right', fontsize=6)
                ax1.grid(b=True, which='both', color='silver', linestyle='-')
                ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
                pylab.savefig('04_Compensated_imm_spectra' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
                plt.close('all')
                '''

                wf_data = np.zeros((no_of_points_for_fft_dedisp, no_of_spectra_in_bunch))

                # Add lost half of the spectra

                second_spectra_half = spectra.copy()
                second_spectra_half = np.flipud(second_spectra_half)
                spectra = np.concatenate((second_spectra_half, spectra), axis=0)  # Changed places!!!

                '''
                fig = plt.figure(figsize=(9, 5))
                ax1 = fig.add_subplot(111)
                ax1.plot(10*np.log10(np.power(np.abs(spectra[:,0]), 2)), linestyle='-', linewidth='1.00', label='Initial waveform')
                ax1.legend(loc='upper right', fontsize=6)
                ax1.grid(b=True, which='both', color='silver', linestyle='-')
                ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
                pylab.savefig('05_Compensated_doubled_imm_spectra' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
                plt.close('all')
                '''

                # Making IFFT
                for i in range(no_of_spectra_in_bunch):
                    wf_data[:, i] = np.real(np.fft.ifft(spectra[:, i]))
                del spectra

                # Reshaping the waveform to single dimension (real)
                wf_data = np.reshape(wf_data, [no_of_points_for_fft_dedisp * no_of_spectra_in_bunch, 1], order='F')

                ''' # making figures
                fig = plt.figure(figsize=(9, 5))
                ax1 = fig.add_subplot(111)
                ax1.plot(wf_data, linestyle='-', linewidth='1.00', label='Initial waveform')
                ax1.legend(loc='upper right', fontsize=6)
                ax1.grid(b=True, which='both', color='silver', linestyle='-')
                ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
                pylab.savefig('06_Compensated_waveform_' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
                plt.close('all')
                '''

                # Saving waveform data to wf32 file
                file_data = open(fpath + file_data_name, 'ab')
                file_data.write(np.float32(wf_data).transpose().copy(order='C'))
                file_data.close()

                # !!! Saving time data to timeline file !!!

            # Rolling temp_array to put current data first
            buffer_array = np.roll(buffer_array, - max_shift)
            buffer_array[:, max_shift:] = 0

            bar.next()

        bar.finish()
        old_tl_file.close()
        new_tl_file.close()

    return fpath + file_data_name


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':
    # pulsar_dm = 5.075
    pulsar_dm = 1.0
    no_of_points_for_fft_dedisp = 16384  # Number of points for FFT on dedispersion # 8192, 16384, 32768, 65536, 131072
    # path_to_file = 'E280120_205546.jds_Data_chA.wf32'
    path_to_file = 'e:/python/B0950+08_DSP_waveform_B0950p08_high_band/E310120_225419.jds_Data_wfA+B.wf32'

    file_name = coherent_wf_to_wf_dedispersion(pulsar_dm, path_to_file, no_of_points_for_fft_dedisp)

    print('Names of files: ', file_name)
