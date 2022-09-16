
fname = 'P130422_114422.jds'

file_path = 'RESULTS_cross-correlation_calibration/'
result_path = 'RESULTS_cross-correlation_calibration/'
phase_calibr_txt_file = file_path + 'Calibration_P130422_114347.jds_cross_spectra_phase.txt'

no_of_spectra_in_bunch = 2048

import os
import math
import pylab
import numpy as np
import matplotlib.pyplot as plt

from progress.bar import IncrementalBar

from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.f_jds_header_new_channels_numbers import jds_header_new_channels_numbers

def cross_spectra_phase_calibration(file_path, file_name, result_path, phase_calibr_txt_file, no_of_spectra_in_bunch,
                                    save_complex=True, save_module=True, save_phase=True, log_module=True):
    """
    function reads cross-spectra data (Re and Im) in .dat format (obtained from jds or adr files)
    multiplies complex data by phase calibration data read from txt file.
    Input parameters:
        fname -                         name of file with initial data
        phase_calibr_txt_file -         txt file with phase calibration data
    Output parameters:
        file_data_name -                name of file with calibrated data
    """

    # Rename the data file to make the new data file of the same name as initial one
    re_fname = file_name + '_Data_CRe' + '.dat'
    im_fname = file_name + '_Data_CIm' + '.dat'
    mod_fname = file_name + '_Data_C_m' + '.dat'
    phs_fname = file_name + '_Data_C_p' + '.dat'

    non_calibrated_re_fname = file_path + re_fname[:-4] + '_without_phase_calibration' + '.dat'
    non_calibrated_im_fname = file_path + im_fname[:-4] + '_without_phase_calibration' + '.dat'

    os.rename(file_path + re_fname, non_calibrated_re_fname)
    os.rename(file_path + im_fname, non_calibrated_im_fname)

    calibrated_re_fname = result_path + re_fname
    calibrated_im_fname = result_path + im_fname
    calibrated_mod_fname = result_path + mod_fname
    calibrated_phs_fname = result_path + phs_fname

    print('\n  Phase calibration of cross-spectra data (Re and IM) \n')

    #  *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
     clock_freq, df_creation_time_utc, channel, receiver_mode, mode, n_avr, time_resolution, fmin, fmax,
     df, frequency_list, freq_points_num, data_block_size] = FileHeaderReaderJDS(non_calibrated_re_fname, 0, 0)

    # Read and copy first data file header from initial file to calibrated files
    non_calibr_re_data_file = open(non_calibrated_re_fname, 'rb')
    non_calibr_im_data_file = open(non_calibrated_im_fname, 'rb')
    file_header = non_calibr_re_data_file.read(1024)
    non_calibr_im_data_file.seek(1024)

    # Changing file header to store only real 8188 channels instead of 8192
    ifmin = int(fmin * 1e6 / df)        # Minimal channel number
    ifmax = int(fmax * 1e6 / df) - 4    # Maximal channel number

    file_header = jds_header_new_channels_numbers(file_header, ifmin, ifmax)

    if save_complex:
        # *** Creating a binary file for Real data for long data storage ***
        calibr_re_file_data = open(calibrated_re_fname, 'wb')
        calibr_re_file_data.write(file_header)
        calibr_re_file_data.close()

        # *** Creating a binary file for Imag data for long data storage ***
        calibr_im_file_data = open(calibrated_im_fname, 'wb')
        calibr_im_file_data.write(file_header)
        calibr_im_file_data.close()

    if save_module:
        # *** Creating a binary file for Module data for long data storage ***
        calibr_mod_file_data = open(calibrated_mod_fname, 'wb')
        calibr_mod_file_data.write(file_header)
        calibr_mod_file_data.close()

    if save_phase:
        # *** Creating a binary file for Phase data for long data storage ***
        calibr_phs_file_data = open(calibrated_phs_fname, 'wb')
        calibr_phs_file_data.write(file_header)
        calibr_phs_file_data.close()

    del file_header

    # Read phase calibration txt file
    phase_calibr_file = open(phase_calibr_txt_file, 'r')
    phase_vs_freq = []
    for line in phase_calibr_file:
        phase_vs_freq.append(float(line))
    phase_calibr_file.close()
    phase_vs_freq = np.array(phase_vs_freq)

    fig = plt.figure(figsize=(9, 5))
    ax1 = fig.add_subplot(111)
    ax1.plot(phase_vs_freq, linestyle='-', linewidth='1.20', label='Calibration phase')
    ax1.set_ylim(-3.15, 3.15)
    ax1.set_title('Calibration phase from ' + phase_calibr_txt_file)
    ax1.legend(loc='upper right', fontsize=6)
    ax1.grid(visible=True, which='both', color='silver', linestyle='-')
    ax1.set_xlabel('Frequency points, #', fontsize=6, fontweight='bold')
    ax1.set_ylabel('Phase, rad', fontsize=6, fontweight='bold')
    pylab.savefig(result_path + '00_Calibration_phase.png', bbox_inches='tight', dpi=250)
    plt.close('all')

    # Converting phase to complex numbers (make function and store in separate file)
    complex_phase = np.zeros((len(phase_vs_freq)), dtype=np.complex128)
    for i in range(len(phase_vs_freq)):
        complex_phase[i] = np.cos(phase_vs_freq[i]) + 1j * np.sin(phase_vs_freq[i])  # - ?

    # Calculation the number of spectra in the file and the number of bunches to read and convert
    no_of_spectra_in_file = int((df_filesize - 1024) / (freq_points_num * 8))
    no_of_bunches_in_file = math.ceil(no_of_spectra_in_file / no_of_spectra_in_bunch)
    print('  Number of spectra per file:    ', no_of_spectra_in_file, '')
    print('  Number of spectra in bunch:    ', no_of_spectra_in_bunch)
    print('  Number of batches per file:    ', no_of_bunches_in_file, '')
    print('  Number of frequency points:    ', freq_points_num, '\n')

    bar = IncrementalBar('  Phase calibration of the file: ', max=no_of_bunches_in_file,
                         suffix='%(percent)d%%        ')
    bar.start()

    for bunch in range(no_of_bunches_in_file):

        if bunch == no_of_bunches_in_file-1:
            no_of_spectra_in_bunch = no_of_spectra_in_file - bunch * no_of_spectra_in_bunch
            # print(' Last bunch ', bunch+1, ', spectra in bunch: ', no_of_spectra_in_bunch)

        # Read data from Re and Im files
        data_re = np.fromfile(non_calibr_re_data_file, dtype=np.float64,
                              count=no_of_spectra_in_bunch * freq_points_num)
        data_re = np.reshape(data_re, [freq_points_num, no_of_spectra_in_bunch], order='F')
        data_re = data_re[:-4]  # Delete the last 4 channels where time is stored

        data_im = np.fromfile(non_calibr_im_data_file, dtype=np.float64,
                              count=no_of_spectra_in_bunch * freq_points_num)
        data_im = np.reshape(data_im, [freq_points_num, no_of_spectra_in_bunch], order='F')
        data_im = data_im[:-4]  # Delete the last 4 channels where time is stored

        data_complex = np.array(data_re + 1j * data_im, dtype=np.complex128)
        del data_re, data_im

        # Phase calibration
        for i in range(no_of_spectra_in_bunch):
            data_complex[:, i] = data_complex[:, i] * np.conj(complex_phase[:])

        # Transposed to save into files correctly
        data_complex = np.transpose(data_complex)

        # Saving calibrated data to a file
        if save_complex:
            calibr_re_file_data = open(calibrated_re_fname, 'ab')
            tmp = np.real(data_complex).copy(order='C')
            calibr_re_file_data.write(tmp)
            calibr_re_file_data.close()

            calibr_im_file_data = open(calibrated_im_fname, 'ab')
            tmp = np.imag(data_complex).copy(order='C')
            calibr_im_file_data.write(tmp)
            calibr_im_file_data.close()

        if save_module:

            calibr_mod_file_data = open(calibrated_mod_fname, 'ab')
            if log_module:
                tmp = 10 * np.log10(np.absolute(data_complex)).copy(order='C')
                tmp[np.isinf(tmp)] = -135.5
            else:
                tmp = np.absolute(data_complex).copy(order='C')
            calibr_mod_file_data.write(tmp)
            calibr_mod_file_data.close()

        if save_phase:
            calibr_phs_file_data = open(calibrated_phs_fname, 'ab')
            tmp = np.angle(data_complex).copy(order='C')
            calibr_phs_file_data.write(tmp)
            calibr_phs_file_data.close()

        bar.next()

    bar.finish()
    non_calibr_re_data_file.close()
    non_calibr_im_data_file.close()

    print('\n Calibrated files saved \n')


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    cross_spectra_phase_calibration(file_path, fname, result_path, phase_calibr_txt_file, no_of_spectra_in_bunch,
                                    save_complex=True, save_module=True, save_phase=False, log_module=False)
