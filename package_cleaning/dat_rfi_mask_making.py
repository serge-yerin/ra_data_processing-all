import os
import numpy as np
import matplotlib.pyplot as plt
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_processing.f_spectra_normalization import normalization_db
from package_cleaning.f_clean_dirty_lines_for_weak_signal import clean_dirty_lines_for_weak_signal
# Files to be analyzed:


def dat_rfi_mask_making(filepath, spectra_to_read_per_bunch):
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

    data_file = open(filepath, 'rb')
    data_file.seek(1024, os.SEEK_SET)  # Jumping to 1024+number of spectra to skip byte from file beginning

    chunks_in_file = int(sp_in_file / spectra_to_read_per_bunch)

    for chunk in range(chunks_in_file):

        # Reading and preparing block of data (3 periods)
        data = np.fromfile(data_file, dtype=np.float64, count=spectra_to_read_per_bunch * len(frequency))
        data = np.reshape(data, [len(frequency), spectra_to_read_per_bunch], order='F')

        mask = clean_dirty_lines_for_weak_signal(data, 2)


if __name__ == '__main__':
    filepath = 'P250322_082507.jds_Data_chA.dat'
    dat_rfi_mask_making(filepath, 4000)
