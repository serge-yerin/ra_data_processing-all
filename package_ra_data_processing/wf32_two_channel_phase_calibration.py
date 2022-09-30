import os
import math
import pylab
import numpy as np
from progress.bar import IncrementalBar
import matplotlib.pyplot as plt

from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read


# *******************************************************************************
#             W A V E F O R M    P H A S E   C A L I B R A T I O N              *
# *******************************************************************************


def wf32_two_channel_phase_calibration(fname, no_of_points_for_fft_dedisp,
                                       no_of_spectra_in_bunch, phase_calibr_txt_file):
    """
    function reads waveform data in wf32 format, makes FFT, cuts the symmetrical half of the spectra and
    multiplies complex data by phase calibration data read from txt file. Then a symmetrical part of spectra
    are made and joined to the shifted one, inverse FFT as applied and data are stored in waveform wf32 format
    Input parameters:
        fname -                         name of file with initial wf32 data
        no_of_points_for_fft_dedisp -   number of waveform data points to use for FFT
        phase_calibr_txt_file -         txt file with phase calibration data
    Output parameters:
        file_data_name -                name of file with calibrated data
    """

    # Rename the data file to make the new data file of the same name as initial one
    non_calibrated_fname = fname[:-5] + '_without_phase_calibration' + '.wf32'
    calibrated_fname = fname
    print('\n  Phase calibration of one channel \n')
    print('  Old filename of initial file:  ', calibrated_fname)
    print('  New filename of initial file:  ', non_calibrated_fname)

    os.rename(calibrated_fname, non_calibrated_fname)

    #  *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
     clock_freq, df_creation_time_utc, channel, receiver_mode, mode, n_avr, time_resolution, fmin, fmax,
     df, frequency_list, freq_points_num, data_block_size] = file_header_jds_read(non_calibrated_fname, 0, 0)

    # Read phase calibration txt file
    phase_calibr_file = open(phase_calibr_txt_file, 'r')
    phase_vs_freq = []
    for line in phase_calibr_file:
        phase_vs_freq.append(np.float(line))
    phase_calibr_file.close()

    # Path of the initial file
    path = '/'.join(fname.split('/')[:-1]) + '/'

    fig = plt.figure(figsize=(9, 5))
    ax1 = fig.add_subplot(111)
    ax1.plot(phase_vs_freq, linestyle='-', linewidth='1.00', label='Phase to add')
    ax1.legend(loc='upper right', fontsize=6)
    ax1.grid(b=True, which='both', color='silver', linestyle='-')
    ax1.set_ylabel('Phase, a.u.', fontsize=6, fontweight='bold')
    pylab.savefig(path + '00_Phase to add.png', bbox_inches='tight', dpi=160)
    plt.close('all')

    # Converting phase to complex numbers
    cmplx_phase = np.zeros((len(phase_vs_freq)), dtype=np.complex)
    for i in range(len(phase_vs_freq)):
        cmplx_phase[i] = np.cos(phase_vs_freq[i]) + 1j * np.sin(phase_vs_freq[i])

    # Create long data files and copy first data file header to them
    non_calibr_file_data = open(non_calibrated_fname, 'rb')
    file_header = non_calibr_file_data.read(1024)

    # *** Creating a binary file with data for long data storage ***
    calibr_file_data = open(calibrated_fname, 'wb')
    calibr_file_data.write(file_header)
    calibr_file_data.close()
    del file_header

    # Calculation of number of blocks and number of spectra in the file
    no_of_spectra_per_file = int((df_filesize - 1024) / (no_of_points_for_fft_dedisp * 4))
    no_of_bunches_per_file = math.ceil(no_of_spectra_per_file / no_of_spectra_in_bunch)
    print('  Number of spectra in bunch:    ', no_of_spectra_in_bunch)
    print('  Number of batches per file:    ', no_of_bunches_per_file, '')
    print('  Number of spectra per file:    ', no_of_spectra_per_file, '\n')

    non_calibr_file_data.seek(1024)  # Jumping to 1024 byte from file beginning

    bar = IncrementalBar(' Phase calibration of the file: ', max=no_of_bunches_per_file - 1,
                         suffix='%(percent)d%%')

    for bunch in range(no_of_bunches_per_file):

        if bunch < no_of_bunches_per_file-1:
            pass
        else:
            no_of_spectra_in_bunch = no_of_spectra_per_file - bunch * no_of_spectra_in_bunch
            # print(' Last bunch ', bunch, ', spectra in bunch: ', no_of_spectra_in_bunch)

        bar.next()

        # Reading and reshaping all data with time data
        wf_data = np.fromfile(non_calibr_file_data, dtype='f4',
                              count=no_of_spectra_in_bunch * no_of_points_for_fft_dedisp)

        wf_data = np.reshape(wf_data, [no_of_points_for_fft_dedisp, no_of_spectra_in_bunch], order='F')

        # preparing matrices for spectra
        spectra = np.zeros((no_of_points_for_fft_dedisp, no_of_spectra_in_bunch), dtype='complex64')

        # Calculation of spectra
        for i in range(no_of_spectra_in_bunch):
            spectra[:, i] = np.fft.fft(wf_data[:, i])
        del wf_data

        # Add phase to the data (multiply by complex number)
        for i in range(no_of_spectra_in_bunch):
            spectra[:, i] = spectra[:, i] * cmplx_phase[:]

        # Preparing array for new waveform
        wf_data = np.zeros((no_of_points_for_fft_dedisp, no_of_spectra_in_bunch))

        # Making IFFT
        for i in range(no_of_spectra_in_bunch):
            wf_data[:, i] = np.real(np.fft.ifft(spectra[:, i]))
        del spectra

        # Reshaping the waveform to single dimension (real)
        wf_data = np.reshape(wf_data, [no_of_points_for_fft_dedisp * no_of_spectra_in_bunch, 1], order='F')

        # Saving waveform data to wf32 file
        calibr_file_data = open(calibrated_fname, 'ab')
        calibr_file_data.write(np.float32(wf_data).transpose().copy(order='C'))
        calibr_file_data.close()

    bar.finish()

    return


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':
    phase_calibr_txt_file = 'Calibration_E300120_232956.jds_cross_spectra_phase.txt'
    no_of_spectra_in_bunch = 16384  # Number of spectra samples to read while conversion to dat (depends on RAM)
    no_of_points_for_fft_dedisp = 16384  # Number of points for FFT on dedispersion # 8192, 16384, 32768, 65536, 131072
    fname = 'E280120_205546.jds_Data_chA.wf32'

    wf32_two_channel_phase_calibration(fname, no_of_points_for_fft_dedisp, no_of_spectra_in_bunch, phase_calibr_txt_file)
