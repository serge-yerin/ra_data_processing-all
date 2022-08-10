
phase_calibr_txt_file = 'Calibration_E300120_232956.jds_cross_spectra_phase.txt'
fname = 'E280120_205546.jds'
file_path = ''
result_path = ''


import os
import pylab
import numpy as np
import matplotlib.pyplot as plt

from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS


def cross_spectra_phase_calibration(file_path, file_name, result_path, phase_calibr_txt_file, save_complex=True,
                                    save_module=True):
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

    non_calibrated_re_fname = file_path + re_fname[:-4] + '_without_phase_calibration' + '.dat'
    non_calibrated_im_fname = file_path + im_fname[:-4] + '_without_phase_calibration' + '.dat'

    os.rename(re_fname, non_calibrated_re_fname)
    os.rename(im_fname, non_calibrated_im_fname)

    calibrated_re_fname = result_path + re_fname
    calibrated_im_fname = result_path + im_fname
    calibrated_mod_fname = result_path + mod_fname

    print('\n  Phase calibration of cross-spectra data (Re and IM) \n')

    # #  *** Data file header read ***
    # [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
    #  clock_freq, df_creation_time_utc, channel, receiver_mode, mode, n_avr, time_resolution, fmin, fmax,
    #  df, frequency_list, freq_points_num, data_block_size] = FileHeaderReaderJDS(non_calibrated_fname, 0, 0)

    # Read and copy first data file header from initial file to calibrated files
    non_calibr_file_data = open(non_calibrated_re_fname, 'rb')
    file_header = non_calibr_file_data.read(1024)

    if save_complex:
        # *** Creating a binary file for Real data for long data storage ***
        calibr_file_data = open(calibrated_re_fname, 'wb')
        calibr_file_data.write(file_header)
        calibr_file_data.close()

        # *** Creating a binary file for Imag data for long data storage ***
        calibr_file_data = open(calibrated_im_fname, 'wb')
        calibr_file_data.write(file_header)
        calibr_file_data.close()

    if save_module:
        # *** Creating a binary file for Module data for long data storage ***
        calibr_file_data = open(calibrated_mod_fname, 'wb')
        calibr_file_data.write(file_header)
        calibr_file_data.close()

    del file_header

    # Read phase calibration txt file
    phase_calibr_file = open(phase_calibr_txt_file, 'r')
    phase_vs_freq = []
    for line in phase_calibr_file:
        phase_vs_freq.append(np.float(line))
    phase_calibr_file.close()

    fig = plt.figure(figsize=(9, 5))
    ax1 = fig.add_subplot(111)
    ax1.plot(phase_vs_freq, linestyle='-', linewidth='1.00', label='Phase to add')
    ax1.legend(loc='upper right', fontsize=6)
    ax1.grid(b=True, which='both', color='silver', linestyle='-')
    ax1.set_ylabel('Phase, a.u.', fontsize=6, fontweight='bold')
    pylab.savefig('00_Phase to add.png', bbox_inches='tight', dpi=160)
    plt.close('all')

    # Converting phase to complex numbers (make function and store in separate file)
    cmplx_phase = np.zeros((len(phase_vs_freq)), dtype=np.complex)
    for i in range(len(phase_vs_freq)):
        cmplx_phase[i] = np.cos(phase_vs_freq[i]) + 1j * np.sin(phase_vs_freq[i])





# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    cross_spectra_phase_calibration(file_path, fname, result_path, phase_calibr_txt_file)
