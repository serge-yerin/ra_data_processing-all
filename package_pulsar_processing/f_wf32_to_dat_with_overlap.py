# Python3

# Make and test function which converts WF32 to DAT with overlap of wf data
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
pulsar_name = 'B0809+74'  # 'B0950+08'

no_of_points_for_fft_spectr = 16384     # Number of points for FFT on result spectra # 8192, 16384, 32768, 65536, 131072
no_of_spectra_in_bunch = 2048           # Number of spectra samples to read while conversion to dat (depends on RAM)
source_directory = 'DATA/'              # Directory with JDS files to be analyzed
result_directory = ''                   # Directory where DAT files to be stored (empty string means project directory)

# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import sys
import numpy as np
from os import path
from progress.bar import IncrementalBar

# To change system path to main source_directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
# ###############################################################################


# *******************************************************************************
#          W A V E F O R M   F L O A T 3 2   T O   S P E C T R A                *
# *******************************************************************************

def convert_wf32_to_dat(fname, no_of_points_for_fft_spectr, no_of_spectra_in_bunch):
    '''
    function converts waveform data in .wf32 format to spectra in .dat format
    Input parameters:
        fname -                 name of .wf32 file with waveform data
        no_of_points_for_fft -  number of points for FFT to provide necessary time-frequency resolution
    Output parameters:
        file_data_name -        name of .dat file with result spectra
    '''

    # *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        clock_freq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, time_resolution, fmin, fmax,
        df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(fname, 0, 0)

    freq_points_num = int(no_of_points_for_fft_spectr/2)

    with open(fname, 'rb') as file:
        # *** Data file header read ***
        file_header = file.read(1024)

        # *** Creating a binary file with spectra data for long data storage ***
        file_data_name = fname[:-5] + '.dat'
        file_data = open(file_data_name, 'wb')
        file_data.write(file_header)
        file_data.seek(574)  # FFT size place in header
        file_data.write(np.int32(no_of_points_for_fft_spectr).tobytes())
        file_data.seek(624)  # Lb place in header
        file_data.write(np.int32(0).tobytes())
        file_data.seek(628)  # Hb place in header
        file_data.write(np.int32(freq_points_num).tobytes())
        file_data.seek(632)  # Wb place in header
        file_data.write(np.int32(freq_points_num).tobytes())
        file_data.seek(636)  # Navr place in header <------------------------------------------------------------------- change this
        file_data.write(np.int32(1).tobytes()) # !!! Check for correctness !!!
        file_data.close()
        del file_header

        # Calculation of number of blocks and number of spectra in the file
        # no_of_bunches_per_file = int((df_filesize - 1024) / (no_of_spectra_in_bunch * no_of_points_for_fft_spectr * 4))
        no_of_bunches_per_file = int((df_filesize - 1024) /
                                     (no_of_spectra_in_bunch * (no_of_points_for_fft_spectr/2 - 1) * 4))

        # Real time resolution of averaged spectra
        fine_clock_freq = (int(clock_freq / 1000000.0) * 1000000.0)
        real_spectra_dt = float(no_of_points_for_fft_spectr / fine_clock_freq)
        real_spectra_df = float((fine_clock_freq / 2) / (no_of_points_for_fft_spectr / 2 ))

        print(' Number of spectra in bunch:                  ', no_of_spectra_in_bunch)
        print(' Number of bunches to read in file:           ', no_of_bunches_per_file)
        print(' Time resolution of calculated spectra:       ', round(real_spectra_dt*1000, 3), ' ms')
        print(' Frequency resolution of calculated spectra:  ', round(real_spectra_df/1000, 3), ' kHz')
        print('\n  *** Reading data from file *** \n')

        file.seek(1024)  # Jumping to 1024 byte from file beginning

        for bunch in range(no_of_bunches_per_file-1):

            # Reading and reshaping data of the bunch
            wf_data = np.fromfile(file, dtype='f4', count = no_of_spectra_in_bunch * no_of_points_for_fft_spectr)
            wf_data = np.reshape(wf_data, [no_of_points_for_fft_spectr, no_of_spectra_in_bunch], order='F')

            # preparing matrices for spectra
            spectra = np.zeros_like(wf_data)

            # Calculation of spectra
            for i in range(no_of_spectra_in_bunch):
                spectra[:, i] = np.power(np.abs(np.fft.fft(wf_data[:, i])), 2)

            # Storing only first (left) mirror part of spectra
            spectra = spectra[: int(no_of_points_for_fft_spectr/2), :]

            # At 33 MHz the specter is usually upside down, to correct it we use flip up/down
            if int(clock_freq/1000000) == 33:
                spectra = np.flipud(spectra)

            # Saving spectra data to dat file
            temp = spectra.transpose().copy(order='C')
            file_data = open(file_data_name, 'ab')
            file_data.write(np.float64(temp))
            file_data.close()

    file.close()  # Close the data file
    return file_data_name


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    file_name = 'E310120_204449.jds_Data_chA.wf32'

    file_name = convert_wf32_to_dat(file_name, no_of_points_for_fft_spectr, no_of_spectra_in_bunch)
    print('\n Result DAT file: ', file_name, '\n')

