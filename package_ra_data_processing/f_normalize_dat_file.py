
import os
import pylab
import numpy as np
import matplotlib.pyplot as plt
from progress.bar import IncrementalBar

from package_ra_data_processing.filtering import median_filter
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR


# *******************************************************************************
#         N O R M A L I Z A T I O N   O F   D A T   S P E C T R A               *
# *******************************************************************************


def normalize_dat_file(directory, filename, no_of_spectra_in_bunch, median_filter_window, show_aver_spectra):
    """
    function calculates the average spectrum in DAT file and normalizes all spectra in file to average spectra
    Input parameters:
        directory - name of directory with initial dat file
        filename - name of initial dat file
    Output parameters:
        output_file_name -  name of result normalized .dat file
    """

    print('\n   Preparations and calculation of the average spectrum to normalize...')

    output_file_name = directory + 'Norm_' + filename
    filename = directory + filename

    # Opening DAT datafile
    file = open(filename, 'rb')

    # *** Data file header read ***
    df_filesize = os.stat(filename).st_size                         # Size of file
    df_filename = file.read(32).decode('utf-8').rstrip('\x00')      # Initial data file name
    file.close()

    if df_filename[-4:] == '.adr':

        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
                CLCfrq, df_creation_timeUTC, ReceiverMode, Mode, sumDifMode,
                NAvr, TimeRes, fmin, fmax, df, frequency, FFTsize, SLine,
                Width, BlockSize] = FileHeaderReaderADR(filename, 0, 0)

    if df_filename[-4:] == '.jds':     # If data obrained from DSPZ receiver

        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
        df, frequency, FreqPointsNum, dataBlockSize] = FileHeaderReaderJDS(filename, 0, 0)

    # Calculation of the dimensions of arrays to read
    nx = len(frequency)                           # the first dimension of the array
    ny = int(((df_filesize - 1024) / (nx * 8)))   # the second dimension of the array: file size - 1024 bytes

    # Number of data blocks to read from file
    num_of_blocks = int(ny // no_of_spectra_in_bunch)

    # Read data from file by blocks and average it
    file = open(filename, 'rb')
    file.seek(1024)
    average_array = np.empty((nx, 0), float)
    for block in range(num_of_blocks):
        if block == (num_of_blocks-1):
            spectra_num_in_bunch = ny - (num_of_blocks-1) * no_of_spectra_in_bunch
        else:
            spectra_num_in_bunch = no_of_spectra_in_bunch

        data = np.fromfile(file, dtype=np.float64, count=nx * spectra_num_in_bunch)
        data = np.reshape(data, [nx, spectra_num_in_bunch], order='F')
        tmp = np.empty((nx, 1), float)
        tmp[:, 0] = data.mean(axis=1)[:]
        average_array = np.append(average_array, tmp, axis=1)  #

    # Average average spectra of all data blocks
    average_profile = average_array.mean(axis=1)

    # Make a figure of average spectrum (profile)
    fig = plt.figure(figsize=(9, 5))
    ax1 = fig.add_subplot(111)
    ax1.plot(10 * np.log10(average_profile), linestyle='-', linewidth='1.00', label='Average spectra')
    ax1.legend(loc='upper right', fontsize=6)
    ax1.grid(b=True, which='both', color='silver', linestyle='-')
    ax1.set_xlabel('Frequency points, num.', fontsize=6, fontweight='bold')
    ax1.set_ylabel('Intensity, dB', fontsize=6, fontweight='bold')
    pylab.savefig('Averaged_spectra_'+filename[:-4]+'_before_filtering.png', bbox_inches='tight', dpi=160)
    plt.close('all')

    # Apply median filter to average profile
    average_profile = median_filter(average_profile, median_filter_window)

    # Make a figure of filtered average spectrum (profile)
    fig = plt.figure(figsize=(9, 5))
    ax1 = fig.add_subplot(111)
    ax1.plot(10 * np.log10(average_profile), linestyle='-', linewidth='1.00', label='Average spectra')
    ax1.legend(loc='upper right', fontsize=6)
    ax1.grid(b=True, which='both', color='silver', linestyle='-')
    ax1.set_xlabel('Frequency points, num.', fontsize=6, fontweight='bold')
    ax1.set_ylabel('Intensity, dB', fontsize=6, fontweight='bold')
    pylab.savefig('Averaged_spectra_'+filename[:-4]+'_after_filtering.png', bbox_inches='tight', dpi=160)
    if show_aver_spectra:
        print('\n   Close the figure window to continue processing!!!\n')
        plt.show()
    plt.close('all')

    # Normalization
    print('   Spectra normalization...')
    file.seek(0)
    file_header = file.read(1024)
    normalized_file = open(output_file_name, 'wb')
    normalized_file.write(file_header)
    del file_header

    bar = IncrementalBar(' Normalizing of the DAT file: ', max=num_of_blocks, suffix='%(percent)d%%')
    bar.start()

    for block in range(num_of_blocks):

        if block == (num_of_blocks - 1):
            spectra_num_in_bunch = ny - (num_of_blocks - 1) * no_of_spectra_in_bunch
        else:
            spectra_num_in_bunch = no_of_spectra_in_bunch

        data = np.fromfile(file, dtype=np.float64, count=nx * spectra_num_in_bunch)
        data = np.reshape(data, [nx, spectra_num_in_bunch], order='F')
        for j in range(spectra_num_in_bunch):
            data[:, j] = data[:, j] / average_profile[:]
        temp = data.transpose().copy(order='C')
        normalized_file.write(np.float64(temp))

        bar.next()

    file.close()
    normalized_file.close()
    bar.finish()

    # *** Creating a new timeline TXT file for results ***
    new_tl_file_name = output_file_name.split('_Data_', 1)[0] + '_Timeline.txt'
    new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
    new_tl_file.close()

    # *** Reading timeline file ***
    old_tl_file_name = filename.split('_Data_', 1)[0] + '_Timeline.txt'
    old_tl_file = open(old_tl_file_name, 'r')
    new_tl_file = open(new_tl_file_name, 'w')

    # Read time from timeline file
    time_scale_bunch = old_tl_file.readlines()

    # Saving time data to new file
    for j in range(len(time_scale_bunch)):
        new_tl_file.write((time_scale_bunch[j][:]) + '')

    old_tl_file.close()
    new_tl_file.close()

    return output_file_name


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':
    no_of_spectra_in_bunch = 16384  # Number of spectra samples to read while conversion to dat (depends on RAM)
    median_filter_window = 80  # Window of median filter to smooth the average profile
    directory = ''
    filename = 'E280120_205546.jds_Data_chA.dat'

    file_name = normalize_dat_file(directory, filename, no_of_spectra_in_bunch, median_filter_window)

    print('Names of files: ', file_name)