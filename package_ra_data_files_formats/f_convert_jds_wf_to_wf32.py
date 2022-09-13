import sys
import numpy as np
from progress.bar import IncrementalBar

from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.JDS_waveform_time import jds_waveform_time
from package_common_modules.find_and_check_files_in_current_folder import find_and_check_files_in_current_folder

# *******************************************************************************
#      W A V E F O R M   J D S   T O   W A V E F O R M    F L O A T 3 2         *
# *******************************************************************************


def convert_jds_wf_to_wf32(source_directory, result_directory, no_of_bunches_per_file):
    """
    function converts jds waveform data to wf32 waveform data for further processing (coherent dedispersion) and
    saves txt files with time data
    Input parameters:
        source_directory - directory where initial jds waveform data are stored
        result_directory - directory where new wf32 files will be stored
        no_of_bunches_per_file - number of data bunches per file to process (depends on RAM volume on the PC)
    Output parameters:
        result_wf32_files - list of results files
    """

    file_list = find_and_check_files_in_current_folder(source_directory, '.jds')

    # To print in console the header of first file
    print('\n  First file header parameters: \n')

    # *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
     clock_freq, df_creation_time_utc, channel, receiver_mode, mode, n_avr, time_res, fmin, fmax,
     df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(source_directory + file_list[0], 0, 1)
    if mode > 0:
        sys.exit('  ERROR!!! Data recorded in wrong mode! Waveform mode needed.\n\n    Program stopped!')

    result_wf32_files = []
    # Main loop by files start
    for file_no in range(len(file_list)):   # loop by files

        fname = source_directory + file_list[file_no]

        # Create long data files and copy first data file header to them
        if file_no == 0:

            with open(fname, 'rb') as file:
                # *** Data file header read ***
                file_header = file.read(1024)

            # *** Creating a name for long timeline TXT file ***
            tl_file_name = result_directory + df_filename + '_Timeline.wtxt'
            tl_file = open(tl_file_name, 'w')  # Open and close to delete the file with the same name
            tl_file.close()

            # *** Creating a name for long phase of second TXT file (to be added to timeline) ***
            sp_file_name = result_directory + df_filename + '_Second_phase.xtxt'
            sp_file = open(sp_file_name, 'w')  # Open and close to delete the file with the same name
            sp_file.close()

            # *** Creating a binary file with data for long data storage ***
            file_data_a_name = result_directory + df_filename + '_Data_chA.wf32'
            result_wf32_files.append(file_data_a_name)
            file_data_a = open(file_data_a_name, 'wb')
            file_data_a.write(file_header)
            file_data_a.close()

            if channel == 2:
                file_data_b_name = result_directory + df_filename + '_Data_chB.wf32'
                result_wf32_files.append(file_data_b_name)
                file_data_b = open(file_data_b_name, 'wb')
                file_data_b.write(file_header)
                file_data_b.close()

            del file_header

        # Calculation of number of blocks and number of spectra in the file
        if channel == 0 or channel == 1:    # Single channel mode
            no_of_spectra_in_bunch = int((df_filesize - 1024) / (no_of_bunches_per_file * 2 * data_block_size))
        else:                               # Two channels mode
            no_of_spectra_in_bunch = int((df_filesize - 1024) / (no_of_bunches_per_file * 4 * data_block_size))

        no_of_blocks_in_file = (df_filesize - 1024) / data_block_size

        if file_no == 0:
            print(' Number of blocks in file:               ', no_of_blocks_in_file)
            print(' Number of bunches to read in file:      ', no_of_bunches_per_file)
            print('\n  *** Reading data from file *** \n')

        # *******************************************************************************
        #                           R E A D I N G   D A T A                             *
        # *******************************************************************************

        with open(fname, 'rb') as file:
            file.seek(1024)  # Jumping to 1024 byte from file beginning

            # !!! Fake timing. Real timing to be done!!!
            TimeFigureScaleFig = np.linspace(0, no_of_bunches_per_file, no_of_bunches_per_file + 1)
            for i in range(no_of_bunches_per_file):
                TimeFigureScaleFig[i] = str(TimeFigureScaleFig[i])

            time_scale_bunch = []

            bar = IncrementalBar(' File ' + str(file_no + 1) + ' of ' + str(len(file_list)) + ' reading: ',
                                 max=no_of_bunches_per_file, suffix='%(percent)d%%')

            bar.start()

            for bunch in range(no_of_bunches_per_file):

                # bar.next()

                # Reading and reshaping all data with time data
                if channel == 0 or channel == 1:    # Single channel mode
                    wf_data = np.fromfile(file, dtype='i2', count=no_of_spectra_in_bunch * data_block_size)
                    wf_data = np.reshape(wf_data, [data_block_size, no_of_spectra_in_bunch], order='F')
                if channel == 2:                    # Two channels mode
                    wf_data = np.fromfile(file, dtype='i2', count=2 * no_of_spectra_in_bunch * data_block_size)
                    wf_data = np.reshape(wf_data, [data_block_size, 2 * no_of_spectra_in_bunch], order='F')

                # Timing
                timeline_block_str, phase_of_second = jds_waveform_time(wf_data, clock_freq, data_block_size)
                if channel == 2:                    # Two channels mode
                    # Cut the timeline of second channel
                    timeline_block_str = timeline_block_str[0:int(len(timeline_block_str) / 2)]  
                    phase_of_second = phase_of_second[0:int(len(phase_of_second) / 2)]
                for i in range(len(timeline_block_str)):
                    time_scale_bunch.append(df_creation_time_utc[0:10] + ' ' + timeline_block_str[i])  # [0:12]

                # Deleting the time blocks from waveform data
                real_data_block_size = data_block_size - 4
                wf_data = wf_data[0: real_data_block_size, :]

                # Separation data into channels
                if channel == 0 or channel == 1:  # Single channel mode
                    wf_data_chA = np.reshape(wf_data, [real_data_block_size * no_of_spectra_in_bunch, 1], order='F')
                    del wf_data  # Deleting unnecessary array name just in case

                if channel == 2:  # Two channels mode

                    # Separating the data into two channels
                    wf_data = np.reshape(wf_data, [2 * real_data_block_size * no_of_spectra_in_bunch, 1], order='F')
                    wf_data_chA = wf_data[0: (2 * real_data_block_size * no_of_spectra_in_bunch): 2]  # A
                    wf_data_chB = wf_data[1: (2 * real_data_block_size * no_of_spectra_in_bunch): 2]  # B
                    del wf_data

                # Saving WF data to dat file
                file_data_a = open(file_data_a_name, 'ab')
                file_data_a.write(np.float32(wf_data_chA).transpose().copy(order='C'))
                file_data_a.close()
                if channel == 2:
                    file_data_b = open(file_data_b_name, 'ab')
                    file_data_b.write(np.float32(wf_data_chB).transpose().copy(order='C'))
                    file_data_b.close()

                # Saving time data to long timeline file
                with open(tl_file_name, 'a') as tl_file:
                    for i in range(no_of_spectra_in_bunch):
                        tl_file.write((str(time_scale_bunch[i][:])) + ' \n')  # str

                # Saving time data to long phase of second file (to be processed and added to time)
                with open(sp_file_name, 'a') as sp_file:
                    if bunch == 0:
                        sp_file.write('# ' + str(clock_freq) + '\n')  # str
                        sp_file.write('# ' + str(df_creation_time_utc) + '\n')  # str
                    for i in range(no_of_spectra_in_bunch):
                        sp_file.write((str(phase_of_second[i])) + ' \n')  # str

                bar.next()

            bar.finish()

        file.close()  # Close the data file
        del file_data_a
        if channel == 2:
            del file_data_b

    return result_wf32_files


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':
    
    source_directory = 'DATA/'  # Directory with JDS files to be analyzed
    result_directory = ''  # Directory where DAT files to be stored (empty string means project directory)
    no_of_bunches_per_file = 16  # Number of bunches to read one WF file (depends on RAM)
    
    file_names = convert_jds_wf_to_wf32(source_directory, result_directory, no_of_bunches_per_file)
    
    print('New wf32 files: ', file_names)
