import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_processing.f_spectra_normalization import normalization_db
from package_cleaning.f_clean_dirty_lines_for_weak_signal import clean_dirty_lines_for_weak_signal


def dat_rfi_mask_reading(filepath, spectra_to_read_per_bunch):
    """
    Reads dat file and makes a mask for the data in a special .msk file to be used bu further processing
    Needs a path to file and number of spectra ti read in bunch to synchronize bunches with the other
    parts of processing pipeline
    returns the name of the mask file
    """
    # Opening DAT datafile and data file header read
    file = open(filepath, 'rb')
    df_filepath = file.read(32).decode('utf-8').rstrip('\x00')  # Initial data file name
    file.close()

    if df_filepath[-4:] == '.jds':  # If data obtained from DSPZ receiver

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description, clock_frq,
         df_creation_time_utc, sp_in_file, receiver_mode, mode, n_avr, time_resolution, fmin, fmax,
         df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(filepath, 0, 1)
    else:
        sys.exit('Error file format')

    chunks_in_file = int(sp_in_file / spectra_to_read_per_bunch)

    # *** Open data file and read it's header ***
    data_file = open(filepath, 'rb')
    data_file.seek(1024, os.SEEK_SET)  # Jumping to 1024+number of spectra to skip byte from file beginning

    # *** Creating a binary file with data for long data storage ***
    mask_file_name = filepath[:-3] + 'msk'
    mask_file = open(mask_file_name, 'rb')
    mask_file.seek(1024, os.SEEK_SET)  # Jumping to 1024+number of spectra to skip byte from file beginning

    print(' Making mask to clean data...')

    for chunk in range(chunks_in_file):

        # Reading and preparing block of data (3 periods)
        data = np.fromfile(data_file, dtype=np.float64, count=spectra_to_read_per_bunch * len(frequency))
        data = np.reshape(data, [len(frequency), spectra_to_read_per_bunch], order='F')

        with np.errstate(invalid='ignore'):
            data = 10 * np.log10(data)
        data[np.isnan(data)] = -120

        a, b = data.shape
        normalization_db(data.transpose(), a, b)
        data = data - np.mean(data)

        # fig, ax0 = plt.subplots(1, 1, figsize=(8, 4))
        # ax0.imshow(data, vmin=0, vmax=1, cmap='Greys')
        # plt.show()

        # Reading and preparing block of data (3 periods)
        mask = np.fromfile(mask_file, dtype=bool, count=spectra_to_read_per_bunch * len(frequency))
        print(mask.shape)
        mask = np.reshape(mask, [len(frequency), spectra_to_read_per_bunch], order='F')

        cldt = data * np.invert(mask)

        fig, [ax0, ax1, ax2] = plt.subplots(1, 3, figsize=(8, 4))
        ax0.imshow(data, vmin=0, vmax=1, cmap='Greys')
        ax1.imshow(mask, vmin=0, vmax=1, cmap='Greys')
        ax2.imshow(cldt, vmin=0, vmax=1, cmap='Greys')
        plt.show()

    data_file.close()
    mask_file.close()
    return


if __name__ == '__main__':
    filepath = 'P250322_082507.jds_Data_chA.dat'
    dat_rfi_mask_reading(filepath, 2000)
    