import os
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from package_ra_data_files_formats.file_header_JDS import file_header_jds_read
from package_ra_data_processing.f_spectra_normalization import normalization_db
import cv2 as cv

# Files to be analyzed:
filepath = 'P250322_082507.jds_Data_chA.dat'


def clean_dirty_lines_for_weak_signal(array, delta_sigma=0.05, n_sigma=2, min_l=30, lin_data=True, show_figures=False):
    """
    Takes the array, makes log of it ib necessary, counts std and in a loop^
    - masks lines of data which exceed std in a row of min_l pixels horizontally and vertically
    - calculates new std with masked noise, if it is less than previous std for more than delta_sigma
      there will be next loop, else - we assume the array is cleaned and return it.
    """
    a, b = array.shape
    total_points = a * b

    if lin_data:
        with np.errstate(divide='ignore'):
            array = 10 * np.log10(array)
        array[np.isnan(array)] = -120
        array[np.isinf(array)] = -135.5
        normalization_db(array.transpose(), a, b)
        array = array - np.mean(array)

    print('   Bunch shape :', array.shape, ', Max: ', np.round(np.max(array), 5), ', Min: ', np.round(np.min(array), 5),
          ', Mean: ', np.round(np.mean(array), 5), ', StD: ', np.round(np.std(array), 2))

    # Set arrays and numbers for the while loop begin and for case when no loop iteration needed
    new_mask = np.zeros_like(array, dtype=bool)
    new_mask[-4:, :] = 1  # set mask for 4 last spectra samples where time is stored
    masked_array = np.ma.masked_where(new_mask, array)
    data_std = np.std(masked_array)
    old_data_std = 2 * data_std
    cleaned_array = array
    dirty_points = 0

    counter = 0
    while old_data_std - data_std > delta_sigma:

        # Find mask for all values greater than n sigma
        masked_array = np.ma.masked_greater(masked_array, n_sigma * data_std)
        mask = ma.getmaskarray(masked_array)

        # Vertical lines mask making
        kernel = np.array(min_l * [1]) / min_l
        mask = np.array(mask, dtype=np.uint8)
        new_vertical_mask = cv.filter2D(mask, -1, kernel)

        # Horizontal lined mask making
        mask = np.transpose(mask)
        new_horizont_mask = cv.filter2D(mask, -1, kernel)
        new_horizont_mask = np.transpose(new_horizont_mask)

        # Converting to bool type to reduce memory
        new_horizont_mask = np.array(new_horizont_mask, dtype=bool)
        new_vertical_mask = np.array(new_vertical_mask, dtype=bool)

        # Concatenating vertical and horizontal masks
        new_mask = np.logical_or(new_horizont_mask, new_vertical_mask)

        # fig, [ax0, ax1, ax2, ax3] = plt.subplots(1, 4, figsize=(8, 4))
        # ax0.imshow(mask, vmin=0, vmax=1, cmap='Greys')
        # ax1.imshow(new_vertical_mask, vmin=0, vmax=1, cmap='Greys')
        # ax2.imshow(new_horizont_mask, vmin=0, vmax=1, cmap='Greys')
        # ax3.imshow(new_mask, vmin=0, vmax=1, cmap='Greys')
        # plt.show()

        # Apply as mask to data
        cleaned_array = np.ma.masked_where(new_mask, array)

        # Calculate statistics
        dirty_points = np.sum(new_mask)
        print('   Iteration:', counter+1, ' StD:', np.round(data_std, 5), ' Masked:', dirty_points,
              'pix of', total_points, 'or', np.round(dirty_points / total_points * 100, 5), '%')

        if show_figures:
            # Show initial array and cleaned array
            fig, [ax0, ax1] = plt.subplots(1, 2, figsize=(8, 4))
            ax0.imshow(array, vmin=0, vmax=1, cmap='Greys')
            ax1.imshow(cleaned_array, vmin=0, vmax=1, cmap='Greys')
            plt.show()

        # Calculate new std and repeat if needed
        old_data_std = data_std
        data_std = np.std(masked_array)

        # Make sure the loop is not infinite
        counter += 1
        if counter > 10:
            break

    return cleaned_array, new_mask, dirty_points


if __name__ == "__main__":

    # Opening DAT datafile and data file header read
    file = open(filepath, 'rb')
    df_filepath = file.read(32).decode('utf-8').rstrip('\x00')  # Initial data file name
    file.close()

    if df_filepath[-4:] == '.jds':  # If data obtained from DSPZ receiver

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description, clock_frq,
         df_creation_time_utc, sp_in_file, receiver_mode, mode, n_avr, time_resolution, fmin, fmax,
         df, frequency, freq_points_num, data_block_size] = file_header_jds_read(filepath, 0, 1)

    data_file = open(filepath, 'rb')
    data_file.seek(1024, os.SEEK_SET)  # Jumping to 1024+number of spectra to skip byte from file beginning

    spectra_to_read = 4000

    for chunk in range(10):

        # Reading and preparing block of data (3 periods)
        data = np.fromfile(data_file, dtype=np.float64, count=spectra_to_read * len(frequency))
        data = np.reshape(data, [len(frequency), spectra_to_read], order='F')
        # data = data[:-4, :]

        # Preparing single averaged data profile for figure
        # profile = data.mean(axis=0)[:]
        # profile = profile - np.mean(profile)
        # data = data - np.mean(data)

        # profile_0 = np.mean(data, axis=0)
        # profile_1 = np.mean(data, axis=1)

        # fig, [ax0, ax1] = plt.subplots(1, 2, figsize=(8, 4))
        # ax0.plot(profile_0)
        # ax1.plot(profile_1)
        # plt.show()

        clean_dirty_lines_for_weak_signal(data, delta_sigma=0.05, n_sigma=2,
                                          min_l=30, lin_data=True, show_figures=True)
