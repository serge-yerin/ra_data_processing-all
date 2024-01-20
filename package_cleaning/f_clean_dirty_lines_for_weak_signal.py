import os
import sys
import cv2 as cv
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1 import make_axes_locatable
from package_ra_data_files_formats.read_file_header_jds import file_header_jds_read
from package_ra_data_processing.f_spectra_normalization import normalization_db
########################################################################################################################

# Path to DAT file
# path = "e:/python/RA_DATA_RESULTS/B0809+74_DSP_spectra_pulsar_UTR2_B0809+74/"
path = "e:/python/RA_DATA_RESULTS/B0809+74_DSP_cross_spectra_B0809+74_URAN2/"
# DAT file name
# file = "E300117_180000.jds_Data_chA.dat"
file = "P130422_121607.jds_Data_chA.dat"

# Cleaning parameters
delta_sigma = 0.002
n_sigma = 1.5
min_l = 25

# Empirically selected parameters for UTR-2 pulsars:
# delta_sigma = 0.05   # If difference of array StD between 2 iterations is less than delta_sigma - stop iterations
# n_sigma = 2          # Level of RFI to mask as the multiplier of the array StD value
# min_l = 30           # Minimal length of emission line (vertical or horizontal) on spectrum to be assumed as RFI

# More detailed description of parameters you can find byt the link below (in Ukrainian)
# https://docs.google.com/document/d/1DltcB2cZ9KD4d8e0-0H9icxcvYn3ut-BsvUzSfv4qvc/edit?usp=sharing


def clean_dirty_lines_for_weak_signal(array, delta_sigma=0.05, n_sigma=2, min_l=30,
                                      lin_data=True, show_figures=False, print_or_not=True):
    """
    Takes the array, makes log of it if necessary, counts std and in a loop:
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

    if print_or_not:
        print('   Bunch shape:', array.shape,
              ', Min: ', np.round(np.min(array), 5), ', Max: ', np.round(np.max(array), 5),
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

        # Apply as mask to data
        cleaned_array = np.ma.masked_where(new_mask, array)

        # Calculate statistics
        dirty_points = np.sum(new_mask)

        if print_or_not:
            print('   Iteration: {0:2.0f}   StD: {1:10.8f}   Masked: {2:10.0f}'
                  '   pix of {3:10.0f}  or  {4:5.2f} %'.format(counter+1, data_std, dirty_points,
                                                               total_points, dirty_points / total_points * 100))

        if show_figures:

            # Show initial array and cleaned array
            rc('font', size=6, weight='bold')
            fig, [ax0, ax1, ax2] = plt.subplots(1, 3, figsize=(12, 4))
            plt.suptitle('Data chunk before and after RFI masking, iteration #' + str(counter + 1),
                         fontsize=8, fontweight='bold')
            im0 = ax0.imshow(array, vmin=0, vmax=data_std, cmap='Greys')
            ax0.set_xlabel('Time points', fontsize=6, fontweight='bold')
            ax0.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
            ax0.set_title('Before cleaning', fontsize=6, fontweight='bold')
            divider = make_axes_locatable(ax0)
            cax = divider.append_axes("right", size="3%", pad=0.0)
            fig.colorbar(im0, ax=ax0, cax=cax, pad=0.0)

            im1 = ax1.imshow(cleaned_array, vmin=0, vmax=data_std, cmap='Greys')
            ax1.set_xlabel('Time points', fontsize=6, fontweight='bold')
            ax1.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
            ax1.set_title('After cleaning, StD = ' + str(np.round(data_std, 4)), fontsize=6, fontweight='bold')
            divider = make_axes_locatable(ax1)
            cax = divider.append_axes("right", size="3%", pad=0.0)
            fig.colorbar(im1, ax=ax1, cax=cax, pad=0.0)

            im2 = ax2.imshow(new_mask, vmin=0, vmax=1, cmap='Greys')
            ax2.set_xlabel('Time points', fontsize=6, fontweight='bold')
            ax2.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
            ax2.set_title('Calculated mask', fontsize=6, fontweight='bold')
            divider = make_axes_locatable(ax2)
            cax = divider.append_axes("right", size="3%", pad=0.0)
            fig.colorbar(im2, ax=ax2, cax=cax, pad=0.0)

            fig.tight_layout(pad=0.0)
            fig_manager = plt.get_current_fig_manager()
            fig_manager.window.showMaximized()
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
    filepath = os.path.join(path, file)
    file = open(filepath, 'rb')
    df_filepath = file.read(32).decode('utf-8').rstrip('\x00')  # Initial data file name
    file.close()

    if df_filepath[-4:] == '.jds':  # If data obtained from DSPZ receiver

        [df_filepath, df_filesize, df_system_name, df_obs_place, df_description, clock_frq,
         df_creation_time_utc, sp_in_file, receiver_mode, mode, n_avr, time_resolution, fmin, fmax,
         df, frequency, freq_points_num, data_block_size] = file_header_jds_read(filepath, 0, 1)
    else:
        sys.exit('Wrong format')

    data_file = open(filepath, 'rb')
    data_file.seek(1024, os.SEEK_SET)  # Jumping to 1024+number of spectra to skip byte from file beginning

    # Calculating the number of data chunks for chunk length equal to frequency points number
    chunks_in_file = int(sp_in_file / freq_points_num)

    for chunk in range(chunks_in_file):

        print('   Bunch # ' + str(chunk + 1) + ' of ' + str(chunks_in_file))
        # Reading and preparing block of data (3 periods)
        data = np.fromfile(data_file, dtype=np.float64, count=freq_points_num * freq_points_num)
        data = np.reshape(data, [freq_points_num, freq_points_num], order='F')
        data = data[:-4, :]

        # Preparing single averaged data profile for figure
        # profile = data.mean(axis=0)[:]
        # profile = profile - np.mean(profile)
        # data = data - np.mean(data)

        profile_0 = np.mean(data, axis=0)
        profile_1 = np.mean(data, axis=1)

        rc('font', size=6, weight='bold')
        fig, [ax0, ax1] = plt.subplots(1, 2, figsize=(8, 4))
        plt.suptitle('Data average profiles before cleaning and normalizing, chunk #' + str(chunk+1),
                     fontsize=8, fontweight='bold')
        ax0.plot(profile_0)
        ax0.set_xlabel('Time points', fontsize=6, fontweight='bold')
        ax0.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax0.set_title('Integrated time profile', fontsize=6, fontweight='bold')
        ax1.plot(profile_1)
        ax1.set_xlabel('Frequency points', fontsize=6, fontweight='bold')
        ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax1.set_title('Integrated frequency profile', fontsize=6, fontweight='bold')
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()

        data, _, _ = clean_dirty_lines_for_weak_signal(data, delta_sigma=delta_sigma, n_sigma=n_sigma,
                                                       min_l=min_l, lin_data=True, show_figures=True)

        profile_0 = np.mean(data, axis=0)
        profile_1 = np.mean(data, axis=1)

        fig, [ax0, ax1] = plt.subplots(1, 2, figsize=(8, 4))
        plt.suptitle('Data average profiles after cleaning and normalizing, chunk #' + str(chunk+1),
                     fontsize=8, fontweight='bold')
        ax0.plot(profile_0)
        ax0.set_xlabel('Time points', fontsize=6, fontweight='bold')
        ax0.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax0.set_title('Integrated time profile', fontsize=6, fontweight='bold')
        ax1.plot(profile_1)
        ax1.set_xlabel('Frequency points', fontsize=6, fontweight='bold')
        ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax1.set_title('Integrated frequency profile', fontsize=6, fontweight='bold')
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()
