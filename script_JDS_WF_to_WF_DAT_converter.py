# Python3
# pip install progress
Software_version = '2020.03.29'
Software_name = 'JDS Waveform to DAT Waveform converter'
# Program intended to convert data from DSPZ receivers in waveform mode to waveform in DAT files
# !!! Time is not correct !!!
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************

source_directory = 'DATA/'      # Directory with JDS files to be analyzed
result_directory = ''           # Directory where DAT files to be stored (empty string means project directory)

no_of_bunches_per_file = 16     # Number of bunches to read one file (depends on RAM volume)

# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import sys
import time
import numpy as np
from os import path
from progress.bar import IncrementalBar

# To change system path to main source_directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_common_modules.find_and_check_files_in_current_folder import find_and_check_files_in_current_folder
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.JDS_waveform_time import JDS_waveform_time

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

fileList = find_and_check_files_in_current_folder(source_directory, '.jds')


# To print in console the header of first file
print('\n  First file header parameters: \n')

# *** Data file header read ***
[df_filename, df_filesize, df_system_name, df_obs_place, df_description,
    CLCfrq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
    df, frequency, FreqPointsNum, data_block_size] = FileHeaderReaderJDS(source_directory + fileList[0], 0, 1)


# Main loop by files start
for fileNo in range(len(fileList)):   # loop by files

    fname = source_directory + fileList[fileNo]

    # Create long data files and copy first data file header to them
    if fileNo == 0:
        #'''
        with open(fname, 'rb') as file:
            # *** Data file header read ***
            file_header = file.read(1024)
        
        # *** Creating a name for long timeline TXT file ***
        TLfile_name = df_filename + '_Timeline.wtxt'
        TLfile = open(TLfile_name, 'w')  # Open and close to delete the file with the same name
        TLfile.close()

        # *** Creating a binary file with data for long data storage ***
        file_data_A_name = df_filename + '_Data_chA.wdat'
        file_data_A = open(file_data_A_name, 'wb')
        file_data_A.write(file_header)
        file_data_A.close()

        if Channel == 2:
            file_data_B_name = df_filename + '_Data_chB.wdat'
            file_data_B = open(file_data_B_name, 'wb')
            file_data_B.write(file_header)
            file_data_B.close()

        del file_header
        #'''

    # Calculation of number of blocks and number of spectra in the file
    if Channel == 0 or Channel == 1:    # Single channel mode
        no_of_spectra_in_bunch = int((df_filesize - 1024) / (no_of_bunches_per_file * 2 * data_block_size))
    else:                               # Two channels mode
        no_of_spectra_in_bunch = int((df_filesize - 1024) / (no_of_bunches_per_file * 4 * data_block_size))

    no_of_blocks_in_file = (df_filesize - 1024) / data_block_size

    if fileNo == 0:
        print(' Number of blocks in file:               ', no_of_blocks_in_file)
        print(' Number of bunches to read in file:      ', no_of_bunches_per_file)
        print('\n  *** Reading data from file *** \n')


    # *******************************************************************************
    #                           R E A D I N G   D A T A                             *
    # *******************************************************************************


    with open(fname, 'rb') as file:
        file.seek(1024)  # Jumping to 1024 byte from file beginning

        # !!! Fake timing. Real timing to be done!!!
        TimeFigureScaleFig = np.linspace(0, no_of_bunches_per_file, no_of_bunches_per_file+1)
        for i in range(no_of_bunches_per_file):
            TimeFigureScaleFig[i] = str(TimeFigureScaleFig[i])

        time_scale_bunch = []

        bar = IncrementalBar(' File ' + str(fileNo+1) + ' of ' + str(len(fileList)) + ' reading: ',
                             max=no_of_bunches_per_file, suffix='%(percent)d%%')

        for bunch in range(no_of_bunches_per_file):

            bar.next()

            # Reading and reshaping all data with time data
            if Channel == 0 or Channel == 1:    # Single channel mode
                wf_data = np.fromfile(file, dtype='i2', count = no_of_spectra_in_bunch * data_block_size)
                wf_data = np.reshape(wf_data, [data_block_size, no_of_spectra_in_bunch], order='F')
            if Channel == 2:                    # Two channels mode
                wf_data = np.fromfile(file, dtype='i2', count = 2 * no_of_spectra_in_bunch * data_block_size)
                wf_data = np.reshape(wf_data, [data_block_size, 2 * no_of_spectra_in_bunch], order='F')


            # Timing
            timeline_block_str = JDS_waveform_time(wf_data, CLCfrq, data_block_size)
            if Channel == 2:                    # Two channels mode
                timeline_block_str = timeline_block_str[0:int(len(timeline_block_str)/2)] # Cut the timeline of second channel
            for i in range (len(timeline_block_str)):
                time_scale_bunch.append(df_creation_timeUTC[0:10] + ' ' +timeline_block_str[i])  #  [0:12]

            # Deleting the time blocks from waveform data
            real_data_block_size = data_block_size - 4
            wf_data = wf_data[0 : real_data_block_size, :]

           # Separation data into channels
            if Channel == 0 or Channel == 1:    # Single channel mode
                wf_data_chA = np.reshape(wf_data, [real_data_block_size * no_of_spectra_in_bunch, 1], order='F')
                del wf_data                     # Deleting unnecessary array name just in case

            if Channel == 2:  # Two channels mode

                # Separating the data into two channels
                wf_data = np.reshape(wf_data, [2 * real_data_block_size * no_of_spectra_in_bunch, 1], order='F')
                wf_data_chA = wf_data[0 : (2 * real_data_block_size * no_of_spectra_in_bunch) : 2]  # Separation to channel A
                wf_data_chB = wf_data[1 : (2 * real_data_block_size * no_of_spectra_in_bunch) : 2]  # Separation to channel B
                del wf_data

            # Saving WF data to dat file
            file_data_A = open(file_data_A_name, 'ab')
            file_data_A.write(wf_data_chA.copy(order='C'))
            file_data_A.close()
            if Channel == 2:
                file_data_B = open(file_data_B_name, 'ab')
                file_data_B.write(wf_data_chB.copy(order='C'))
                file_data_B.close()

            # Saving time data to ling timeline file
            with open(TLfile_name, 'a') as TLfile:
                for i in range(no_of_spectra_in_bunch):
                    TLfile.write((str(time_scale_bunch[i][:])) + ' \n')  # str

        bar.finish()

    file.close()  # Close the data file


endTime = time.time()
print ('\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
