import sys
import numpy as np
import datetime
import matplotlib.pyplot as plt
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_processing.f_spectra_normalization import normalization_db
from package_cleaning.f_clean_dirty_lines_for_weak_signal import clean_dirty_lines_for_weak_signal


# def dat_rfi_mask_making(filepath, spectra_to_read_per_bunch, lin_data=True, delta_sigma=0.05, n_sigma=2, min_l=30):
def dat_rfi_mask_making(filepath, spectra_to_read_per_bunch, lin_data=True, delta_sigma=0.05, n_sigma=2, min_l=30):
    """
    Reads dat file and makes a mask for the data in a special .msk file to be used by further processing
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

    # Number of spectra in the file for dat file, not jds
    dat_sp_in_file = int((df_filesize - 1024) / (len(frequency) * 8))
    chunks_in_file = int(dat_sp_in_file / spectra_to_read_per_bunch)

    # *** Open data file and read its header ***
    data_file = open(filepath, 'rb')
    file_header = data_file.read(1024)  # Data file header read

    # *** Creating a binary file with data for long data storage ***
    new_data_file_name = filepath[:-3] + 'msk'
    new_data_file = open(new_data_file_name, 'wb')
    new_data_file.write(file_header)
    del file_header
    new_data_file.close()
    print(' Making mask to clean data...')

    for chunk in range(chunks_in_file):

        # Reading and preparing a chunk of data
        data = np.fromfile(data_file, dtype=np.float64, count=spectra_to_read_per_bunch * len(frequency))
        data = np.reshape(data, [len(frequency), spectra_to_read_per_bunch], order='F')

        # Make mask
        print('\n * Chunk', chunk+1, 'of', chunks_in_file, 'time:', str(datetime.datetime.now())[:19])
        cleaned_array, mask, dirty_points = clean_dirty_lines_for_weak_signal(data, delta_sigma=delta_sigma,
                                                                              n_sigma=n_sigma, min_l=min_l,
                                                                              lin_data=lin_data, show_figures=False)

        # Save mask array to the file
        new_data_file = open(new_data_file_name, 'ab')
        mask = np.transpose(mask).copy(order='C')
        new_data_file.write(mask)
        new_data_file.close()
        del mask

    return new_data_file_name


if __name__ == '__main__':
    filepath = 'E300117_180000.jds_Data_chA.dat'
    file_name = dat_rfi_mask_making(filepath, 4000)
    print('Mask file name: ', file_name)
