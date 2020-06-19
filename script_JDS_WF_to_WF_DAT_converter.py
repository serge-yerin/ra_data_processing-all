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
no_of_points_for_fft = 16384    # Number of true wf data points for FFT calculation # 8192, 16384, 32768, 65536, 131072 ...



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

def convert_jds_wf_to_wf32(source_directory, result_directory, no_of_bunches_per_file):

    fileList = find_and_check_files_in_current_folder(source_directory, '.jds')
    
    
    # To print in console the header of first file
    print('\n  First file header parameters: \n')
    
    # *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        CLCfrq, df_creation_timeUTC, channel, receiver_mode, Mode, Navr, time_res, fmin, fmax,
        df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(source_directory + fileList[0], 0, 1)

    result_wf32_files = []
    # Main loop by files start
    for file_no in range(len(fileList)):   # loop by files
    
        fname = source_directory + fileList[file_no]

        # Create long data files and copy first data file header to them
        if file_no == 0:

            with open(fname, 'rb') as file:
                # *** Data file header read ***
                file_header = file.read(1024)
            
            # *** Creating a name for long timeline TXT file ***
            TLfile_name = df_filename + '_Timeline.wtxt'
            TLfile = open(TLfile_name, 'w')  # Open and close to delete the file with the same name
            TLfile.close()

            # *** Creating a binary file with data for long data storage ***
            file_data_A_name = df_filename + '_Data_chA.wf32'
            result_wf32_files.append(file_data_A_name)
            file_data_A = open(file_data_A_name, 'wb')
            file_data_A.write(file_header)
            file_data_A.close()
    
            if channel == 2:
                file_data_B_name = df_filename + '_Data_chB.wf32'
                result_wf32_files.append(file_data_B_name)
                file_data_B = open(file_data_B_name, 'wb')
                file_data_B.write(file_header)
                file_data_B.close()
    
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
            TimeFigureScaleFig = np.linspace(0, no_of_bunches_per_file, no_of_bunches_per_file+1)
            for i in range(no_of_bunches_per_file):
                TimeFigureScaleFig[i] = str(TimeFigureScaleFig[i])
    
            time_scale_bunch = []
    
            bar = IncrementalBar(' File ' + str(file_no+1) + ' of ' + str(len(fileList)) + ' reading: ',
                                 max=no_of_bunches_per_file, suffix='%(percent)d%%')
    
            for bunch in range(no_of_bunches_per_file):
    
                bar.next()
    
                # Reading and reshaping all data with time data
                if channel == 0 or channel == 1:    # Single channel mode
                    wf_data = np.fromfile(file, dtype='i2', count = no_of_spectra_in_bunch * data_block_size)
                    wf_data = np.reshape(wf_data, [data_block_size, no_of_spectra_in_bunch], order='F')
                if channel == 2:                    # Two channels mode
                    wf_data = np.fromfile(file, dtype='i2', count = 2 * no_of_spectra_in_bunch * data_block_size)
                    wf_data = np.reshape(wf_data, [data_block_size, 2 * no_of_spectra_in_bunch], order='F')
    
    
                # Timing
                timeline_block_str = JDS_waveform_time(wf_data, CLCfrq, data_block_size)
                if channel == 2:                    # Two channels mode
                    timeline_block_str = timeline_block_str[0:int(len(timeline_block_str)/2)] # Cut the timeline of second channel
                for i in range (len(timeline_block_str)):
                    time_scale_bunch.append(df_creation_timeUTC[0:10] + ' ' +timeline_block_str[i])  #  [0:12]
    
                # Deleting the time blocks from waveform data
                real_data_block_size = data_block_size - 4
                wf_data = wf_data[0 : real_data_block_size, :]
    
               # Separation data into channels
                if channel == 0 or channel == 1:    # Single channel mode
                    wf_data_chA = np.reshape(wf_data, [real_data_block_size * no_of_spectra_in_bunch, 1], order='F')
                    del wf_data                     # Deleting unnecessary array name just in case
    
                if channel == 2:  # Two channels mode
    
                    # Separating the data into two channels
                    wf_data = np.reshape(wf_data, [2 * real_data_block_size * no_of_spectra_in_bunch, 1], order='F')
                    wf_data_chA = wf_data[0 : (2 * real_data_block_size * no_of_spectra_in_bunch) : 2]  # Separation to channel A
                    wf_data_chB = wf_data[1 : (2 * real_data_block_size * no_of_spectra_in_bunch) : 2]  # Separation to channel B
                    del wf_data
    
                # Saving WF data to dat file
                file_data_A = open(file_data_A_name, 'ab')
                file_data_A.write(np.float32(wf_data_chA).transpose().copy(order='C'))
                file_data_A.close()
                if channel == 2:
                    file_data_B = open(file_data_B_name, 'ab')
                    file_data_B.write(np.float32(wf_data_chB).transpose().copy(order='C'))
                    file_data_B.close()
    
                # Saving time data to ling timeline file
                with open(TLfile_name, 'a') as TLfile:
                    for i in range(no_of_spectra_in_bunch):
                        TLfile.write((str(time_scale_bunch[i][:])) + ' \n')  # str
    
            bar.finish()
    
        file.close()  # Close the data file
    
    return result_wf32_files

# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************

def convert_wf32_to_dat(fname, result_directory, no_of_points_for_fft):

    # *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        CLCfrq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
        df, frequency, freq_points_num, data_block_size] = FileHeaderReaderJDS(fname, 0, 0)

     # !!! Make automatic calculations of time and frequency resolutions for waveform mode!!!

    # Manually set frequencies for one channel mode

    freq_points_num = int(no_of_points_for_fft/2)

    # Create long data files and copy first data file header to them

    with open(fname, 'rb') as file:
        # *** Data file header read ***
        file_header = file.read(1024)

        # *** Creating a name for long timeline TXT file ***
        TLfile_name = df_filename + '_Timeline.txt'
        TLfile = open(TLfile_name, 'w')  # Open and close to delete the file with the same name
        TLfile.close()

        # *** Creating a binary file with data for long data storage ***
        file_data_name = df_filename + '_Data_chA.dat'                          # !!!! #
        file_data = open(file_data_name, 'wb')
        file_data.write(file_header)
        file_data.seek(574)  # FFT size place in header
        file_data.write(np.int32(no_of_points_for_fft).tobytes())
        file_data.seek(624)  # Lb place in header
        file_data.write(np.int32(0).tobytes())
        file_data.seek(628)  # Hb place in header
        file_data.write(np.int32(freq_points_num).tobytes())
        file_data.seek(632)  # Wb place in header
        file_data.write(np.int32(freq_points_num).tobytes())
        file_data.seek(636)  # Navr place in header
        file_data.write(np.int32(1).tobytes()) # !!! Check for correctness !!!
        file_data.close()

        del file_header
        #'''

    # Calculation of number of blocks and number of spectra in the file

        no_of_spectra_in_bunch = 256

        no_of_bunches_per_file = int((df_filesize - 1024) / (no_of_spectra_in_bunch * 4))

        fine_CLCfrq = (int(CLCfrq/1000000.0) * 1000000.0)

        # Real time resolution of averaged spectra
        real_spectra_dt = float(no_of_points_for_fft / fine_CLCfrq)
        real_spectra_df = float((fine_CLCfrq / 2) / (no_of_points_for_fft / 2 ))

        print(' Number of spectra in bunch:                  ', no_of_spectra_in_bunch)
        print(' Number of bunches to read in file:           ', no_of_bunches_per_file)
        print(' Time resolution of calculated spectra:       ', round(real_spectra_dt*1000, 3), ' ms')
        print(' Frequency resolution of calculated spectra:  ', round(real_spectra_df/1000, 3), ' kHz')
        print('\n  *** Reading data from file *** \n')

        file.seek(1024)  # Jumping to 1024 byte from file beginning

        # *** DATA READING process ***

        # !!! Fake timing. Real timing to be done!!!
        #TimeFigureScaleFig = np.linspace(0, no_of_bunches_per_file, no_of_bunches_per_file+1)
        #for i in range(no_of_bunches_per_file):
        #    TimeFigureScaleFig[i] = str(TimeFigureScaleFig[i])

        time_scale_bunch = []

        for bunch in range(no_of_bunches_per_file):

            #print(' Bunch # ', bunch+1)

            # Reading and reshaping all data with time data

            wf_data = np.fromfile(file, dtype='f4', count = no_of_spectra_in_bunch * no_of_points_for_fft)
            wf_data = np.reshape(wf_data, [no_of_points_for_fft, no_of_spectra_in_bunch], order='F')

            # preparing matrices for spectra
            spectra_chA = np.zeros_like(wf_data)

            #no_of_spectra_to_compute = int(np.floor(len(wf_data) / no_of_points_for_fft))

            # Calculation of spectra
            #for i in range(no_of_spectra_to_compute):
            for i in range(no_of_spectra_in_bunch):
                spectra_chA[:, i] = np.power(np.abs(np.fft.fft(wf_data[:, i])), 2)

            # Storing only first (left) mirror part of spectra
            spectra_chA = spectra_chA[: int(no_of_points_for_fft/2), :]

            # At 33 MHz the specter is usually upside down, to correct it we use flip up/down
            if int(CLCfrq/1000000) == 33:
                spectra_chA = np.flipud(spectra_chA)

            '''
            '''
            # Saving spectra data to dat file
            temp = spectra_chA.transpose().copy(order='C')
            file_data = open(file_data_name, 'ab')
            file_data.write(np.float64(temp))
            file_data.close()

            # Saving time data to ling timeline file
            #with open(TLfile_name, 'a') as TLfile:
            #    for i in range(no_of_spectra_in_bunch):
            #        TLfile.write((str(time_scale_bunch[i][:])) + ' \n')  # str

    file.close()  # Close the data file





################################################################################

if __name__ == '__main__':

    print('\n\n\n\n\n\n\n\n   *****************************************************************')
    print('   *   ', Software_name, ' v.', Software_version,'   *      (c) YeS 2020')
    print('   ***************************************************************** \n\n\n')
    
    startTime = time.time()
    previousTime = startTime
    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")
    print('  Today is ', currentDate, ' time is ', currentTime, '\n')



    #result_wf32_files = convert_jds_wf_to_wf32(source_directory, result_directory, no_of_bunches_per_file)
    
    #print(result_wf32_files)

    fname = 'E310120_204449.jds_Data_chA.wf32'
    convert_wf32_to_dat(fname, result_directory, no_of_points_for_fft)
    
    
    endTime = time.time()
    print ('\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                    round((endTime - startTime)/60, 2), 'min. ) \n')
    print ('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
