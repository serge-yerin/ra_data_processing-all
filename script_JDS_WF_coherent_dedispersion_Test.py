# !!! Not ready at all !!!
# Python3
# pip install progress
Software_version = '2020.03.29'
Software_name = 'JDS Waveform pulsar coherent dedispersion'
# Program intended to convert data from DSPZ receivers in waveform mode to spectra in DAT files
# !!! Time is not correct !!!
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
source_directory = ''           # Directory where source DAT file is stored (empty string means project directory)
source_file = 'E280120_212713.jds_Data_chA.wdat'      # DAT file with waveform data to be analyzed

result_directory = ''           # Directory where DAT files to be stored (empty string means project directory)
pulsar_name = 'B0000+00'        # 'B0950+08'
no_of_points_for_fft = 16384    # Number of true wf data points for FFT calculation # 8192, 16384, 32768 ...
#no_of_bunches_in_file = 16     # Number of bunches to read one file (depends on RAM volume)

# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import sys
import time
import numpy as np
from os import path

# To change system path to main source_directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_common_modules.check_if_all_files_of_same_size import check_if_all_files_of_same_size
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.check_if_JDS_files_of_equal_parameters import check_if_JDS_files_of_equal_parameters
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.JDS_waveform_time import JDS_waveform_time
from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_pulsar_processing.pulsar_DM_full_shift_calculation import DM_full_shift_calc
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes

# ###############################################################################
# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************
print('\n\n\n\n\n\n\n\n   *****************************************************************')
print('   *   ', Software_name, ' v.', Software_version,'   *      (c) YeS 2020')
print('   ***************************************************************** \n\n\n')

startTime = time.time()
previousTime = startTime
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print('  Today is ', currentDate, ' time is ', currentTime, '\n')

fname = source_directory + source_file

# *** Data file header read ***
[df_filename, df_filesize, df_system_name, df_obs_place, df_description,
    CLCfrq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, time_resolution, fmin, fmax,
    df, frequency, no_of_freq_points, data_block_size] = FileHeaderReaderJDS(fname, 0, 1)


no_of_freq_points = int(no_of_points_for_fft/2)  # Number of frequency points (steps)

# Manually set frequencies for two channels mode
if int(CLCfrq / 1000000) == 33:
    fmin, fmax = 16.5, 33.0
    frequency = np.linspace(fmin, fmax, no_of_freq_points)
else:
    fmin, fmax = 0.0, 33.0
    frequency = np.linspace(fmin, fmax, no_of_freq_points)
# Frequency and time resolution:
df = (fmax - fmin) / no_of_freq_points
time_resolution = (1/CLCfrq) * no_of_points_for_fft

pulsar_ra, pulsar_dec, DM, p_bar = catalogue_pulsar(pulsar_name)

shift_vector = DM_full_shift_calc(no_of_freq_points, fmin, fmax, df / pow(10, 6), time_resolution, DM,'.jds')

max_shift = np.abs(shift_vector[0])

# Calculation of number of blocks and number of spectra in the file
no_of_bunches_in_file = int(np.floor((df_filesize - 1024) / (max_shift * no_of_points_for_fft * 2)))

no_of_spectra_in_bunch = max_shift

# Real time resolution of averaged spectra
fine_CLCfrq = (int(CLCfrq/1000000.0) * 1000000.0)
real_spectra_dt = (1 / fine_CLCfrq) * (no_of_points_for_fft)

print(' Frequency resolution:                   ', df * 1000, ' kHz')
print(' Time resolution:                        ', time_resolution * 1000, ' ms')
print(' Maximal shift is:                       ', max_shift, ' pixels ')
print(' Number of spectra in bunch:             ', no_of_spectra_in_bunch)
print(' Number of frequency channels:           ', int(no_of_points_for_fft/2))
print(' Number of bunches to read in file:      ', no_of_bunches_in_file)
print(' Time resolution of calculated spectra:  ', round(real_spectra_dt*1000, 3), ' ms.')
print('\n  *** Reading data from file *** \n')


# Create long data files and copy first data file header to them
with open(fname, 'rb') as file:
    # *** Data file header read ***
    file_header = file.read(1024)

    # *** Creating a binary file with data for long data storage ***
    file_data_A_name = pulsar_name + '_DM_' + str(DM) + '_' + source_file[:-4] + 'dat'  # df_filename + '_Data_chA.dat'
    file_data_A = open(file_data_A_name, 'wb')
    file_data_A.write(file_header)
    file_data_A.seek(624)  # Lb place in header
    file_data_A.write(np.int32(0).tobytes())
    file_data_A.seek(628)  # Hb place in header
    file_data_A.write(np.int32(no_of_points_for_fft/2).tobytes())
    file_data_A.seek(632)  # Wb place in header
    file_data_A.write(np.int32(no_of_points_for_fft/2).tobytes())
    file_data_A.seek(636)  # Navr place in header
    file_data_A.write(np.int32(no_of_points_for_fft/8192).tobytes())
    file_data_A.close()

    del file_header

# *** Creating a name for long timeline TXT file ***
TLfile_name = pulsar_name + '_DM_' + str(DM) + '_' + source_file[:-4] + '_Timeline.txt'
#TLfile_name = pulsar_name + '_DM_' + str(DM) + '_' + data_filename[:-13] + '_Timeline.txt'
TLfile = open(TLfile_name, 'w')  # Open and close to delete the file with the same name
TLfile.close()

# *******************************************************************************
#                           R E A D I N G   D A T A                             *
# *******************************************************************************

with open(fname, 'rb') as file:
    file.seek(1024)  # Jumping to 1024 byte from file beginning

    # !!! Fake timing. Real timing to be done!!!
    TimeFigureScaleFig = np.linspace(0, no_of_bunches_in_file, no_of_bunches_in_file+1)
    for i in range(no_of_bunches_in_file):
        TimeFigureScaleFig[i] = str(TimeFigureScaleFig[i])

    time_scale_bunch = []

    #bar = IncrementalBar(' File ' + str(fileNo+1) + ' of ' + str(len(fileList)) + ' reading: ',
    #                     max=no_of_bunches_in_file, suffix='%(percent)d%%')

    for bunch in range(no_of_bunches_in_file):
        print('\n  *** Bunch #',bunch+1,' *** \n')
        #bar.next()

        # Reading and reshaping all data with time data
        wf_data = np.fromfile(file, dtype='i2', count = no_of_spectra_in_bunch * no_of_points_for_fft)
        wf_data = np.reshape(wf_data, [no_of_points_for_fft, no_of_spectra_in_bunch], order='F')

        # Scaling of the data - seems to be wrong in absolute value
        wf_data = wf_data / 32768  #  .0

        # preparing matrices for spectra
        spectra_data = np.zeros_like(wf_data)

        print('\n  *** Data read and prepared *** \n')

        # Calculation of spectra
        for i in range(no_of_spectra_in_bunch):
            spectra_data[:, i] = np.power(np.abs(np.fft.fft(wf_data[:, i])),2)
        del wf_data

        print('\n  *** Spectra calculated *** \n')

       # Storing only first (left) mirror part of spectra
        spectra_data = spectra_data[: int(no_of_points_for_fft / 2), :]

        # At 33 MHz the specter is usually upside down, to correct it we use flip up/down
        if int(CLCfrq/1000000) == 33:
            spectra_data = np.flipud(spectra_data)

        # Saving spectra data to dat file
        temp = spectra_data.transpose().copy(order='C')
        file_data_A = open(file_data_A_name, 'ab')
        file_data_A.write(temp)
        file_data_A.close()
        del spectra_data
        print('\n  *** Spectra saved to file *** \n')

        # Saving time data to ling timeline file
        #with open(TLfile_name, 'a') as TLfile:
        #    for i in range(no_of_spectra_in_bunch):
        #        TLfile.write((str(time_scale_bunch[i][:])) + ' \n')  # str


file.close()  # Close the data file


endTime = time.time()
print ('\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
