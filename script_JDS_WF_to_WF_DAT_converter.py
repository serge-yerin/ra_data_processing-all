# Python3
# pip install progress
Software_version = '2020.07.03'
Software_name = 'JDS Waveform coherent dispersion delay removing'
# Program intended to convert data from DSPZ receivers in waveform mode to waveform float 32 files and make coherent dedispersion
# !!! Time is not correct !!!
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************

source_directory = 'DATA/'      # Directory with JDS files to be analyzed
result_directory = ''           # Directory where DAT files to be stored (empty string means project directory)

no_of_bunches_per_file = 16     # Number of bunches to read one file (depends on RAM volume)
no_of_points_for_fft = 16384    # Number of true wf data points for FFT calculation # 8192, 16384, 32768, 65536, 131072 ...
no_of_points_for_fft_dedisp = 16384
typesOfData = ['chA']

# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import sys
import time
import pylab
import numpy as np
from os import path
from progress.bar import IncrementalBar
import matplotlib.pyplot as plt
from matplotlib import rc


# To change system path to main source_directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_common_modules.find_and_check_files_in_current_folder import find_and_check_files_in_current_folder
from package_common_modules.text_manipulations import find_between
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.JDS_waveform_time import JDS_waveform_time
from package_pulsar_processing.pulsar_DM_full_shift_calculation import DM_full_shift_calc
from package_pulsar_processing.pulsar_DM_compensation_with_indices_changes import pulsar_DM_compensation_with_indices_changes
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader


# ###############################################################################
# *******************************************************************************
#      W A V E F O R M   J D S   T O   W A V E F O R M    F L O A T 3 2         *
# *******************************************************************************

def convert_jds_wf_to_wf32(source_directory, result_directory, no_of_bunches_per_file):

    fileList = find_and_check_files_in_current_folder(source_directory, '.jds')
    
    # To print in console the header of first file
    print('\n  First file header parameters: \n')
    
    # *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        clock_freq, df_creation_timeUTC, channel, receiver_mode, Mode, Navr, time_res, fmin, fmax,
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
            tl_file_name = df_filename + '_Timeline.wtxt'
            tl_file = open(tl_file_name, 'w')  # Open and close to delete the file with the same name
            tl_file.close()

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
                timeline_block_str = JDS_waveform_time(wf_data, clock_freq, data_block_size)
                if channel == 2:                    # Two channels mode
                    timeline_block_str = timeline_block_str[0:int(len(timeline_block_str)/2)]  # Cut the timeline of second channel
                for i in range (len(timeline_block_str)):
                    time_scale_bunch.append(df_creation_timeUTC[0:10] + ' ' +timeline_block_str[i])  # [0:12]
    
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
                    wf_data_chA = wf_data[0 : (2 * real_data_block_size * no_of_spectra_in_bunch) : 2]  # A
                    wf_data_chB = wf_data[1 : (2 * real_data_block_size * no_of_spectra_in_bunch) : 2]  # B
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
                with open(tl_file_name, 'a') as tl_file:
                    for i in range(no_of_spectra_in_bunch):
                        tl_file.write((str(time_scale_bunch[i][:])) + ' \n')  # str
    
            bar.finish()
    
        file.close()  # Close the data file
        del file_data_A
        if channel == 2: del file_data_B

    return result_wf32_files


# *******************************************************************************
#        WAVEFORM FLOAT32 TO WAVEFORM FLOAT32 COHERENT DEDISPERSION             *
# *******************************************************************************

def coherent_wf_to_wf_dedispersion(DM, fname, no_of_points_for_fft_dedisp):

    #  *** Data file header read ***
    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
        clock_freq, df_creation_timeUTC, Channel, ReceiverMode, Mode, Navr, time_resolution, fmin, fmax,
        df, frequency_list, freq_points_num, data_block_size] = FileHeaderReaderJDS(fname, 0, 0)

    # Manually set frequencies for one channel mode
    freq_points_num = int(no_of_points_for_fft_dedisp/2)

    # Manually set frequencies for 33 MHz clock frequency
    if int(clock_freq / 1000000) == 33:
        fmin = 16.5
        fmax = 33.0
        df = 16500000 / freq_points_num

    # Create long data files and copy first data file header to them

    with open(fname, 'rb') as file:
        # *** Data file header read ***
        file_header = file.read(1024)

        # *** Creating a binary file with data for long data storage ***
        file_data_name = 'DM_' + str(DM) + '_' + fname
        file_data = open(file_data_name, 'wb')
        file_data.write(file_header)
        file_data.close()
        del file_header

        # *** Creating a new timeline TXT file ***
        new_tl_file_name = file_data_name.split("_Data_ch", 1)[0] + '_Timeline.txt'
        new_tl_file = open(new_tl_file_name, 'w')  # Open and close to delete the file with the same name
        new_tl_file.close()

        # Calculation of the time shifts
        shift_vector = DM_full_shift_calc(freq_points_num, fmin, fmax, df / pow(10, 6), time_resolution, DM, 'jds')
        max_shift = np.abs(shift_vector[0])

        # Preparing buffer array
        buffer_array = np.zeros((freq_points_num, 2 * max_shift), dtype='complex')

        print(' Maximal shift is:              ', max_shift, ' pixels ')
        print(' Dispersion measure:            ', DM, ' pc / cm3 \n')

        # Calculation of number of blocks and number of spectra in the file
        no_of_spectra_in_bunch = max_shift
        no_of_bunches_per_file = int((df_filesize - 1024) / (no_of_spectra_in_bunch * no_of_points_for_fft_dedisp * 4))

        # Real time resolution of spectra
        fine_clock_freq = (int(clock_freq / 1000000.0) * 1000000.0)
        real_spectra_dt = float(no_of_points_for_fft / fine_clock_freq)
        real_spectra_df = float((fine_clock_freq / 2) / (no_of_points_for_fft / 2))

        print(' Number of spectra in bunch:                  ', no_of_spectra_in_bunch)
        print(' Number of bunches to read in file:           ', no_of_bunches_per_file)
        print(' Time resolution of calculated spectra:       ', round(real_spectra_dt*1000, 3), ' ms')
        print(' Frequency resolution of calculated spectra:  ', round(real_spectra_df/1000, 3), ' kHz')
        print('\n  *** Reading data from file *** \n')

        # !!! Fake timing. Real timing to be done!!!
        #  time_scale_bunch = []

        file.seek(1024)  # Jumping to 1024 byte from file beginning

        bar = IncrementalBar(' Coherent dispersion delay removing: ', max=no_of_bunches_per_file-1, suffix='%(percent)d%%')

        for bunch in range(no_of_bunches_per_file-1):

            bar.next()

            #print('  Dispersion delay removing bunch #', bunch+1, ' of ', no_of_bunches_per_file-1)

            # Reading and reshaping all data with time data
            wf_data = np.fromfile(file, dtype='f4', count = no_of_spectra_in_bunch * no_of_points_for_fft_dedisp)
            
            '''
            fig = plt.figure(figsize=(9, 5))
            ax1 = fig.add_subplot(111)
            ax1.plot(wf_data, linestyle='-', linewidth='1.00', label='Initial waveform')
            ax1.legend(loc='upper right', fontsize=6)
            ax1.grid(b=True, which='both', color='silver', linestyle='-')
            ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
            pylab.savefig('00_Initial_waveform_' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
            plt.close('all')
            '''
            
            wf_data = np.reshape(wf_data, [no_of_points_for_fft_dedisp, no_of_spectra_in_bunch], order='F')

            # preparing matrices for spectra
            spectra = np.zeros((no_of_points_for_fft_dedisp, max_shift), dtype='complex')

            # Calculation of spectra
            for i in range(no_of_spectra_in_bunch):
                spectra[:, i] = np.fft.fft(wf_data[:, i])
            del wf_data

            '''
            fig = plt.figure(figsize=(9, 5))
            ax1 = fig.add_subplot(111)
            ax1.plot(10 * np.log10(np.power(np.abs(spectra[:, 0]), 2)), linestyle='-', linewidth='1.00',
                     label='Initial spectra before cut')
            ax1.legend(loc='upper right', fontsize=6)
            ax1.grid(b=True, which='both', color='silver', linestyle='-')
            ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
            pylab.savefig('00a_Initial_doubled_imm_spectra' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
            plt.close('all')
            '''
            
            # Cut half of the spectra
            spectra = spectra[int(no_of_points_for_fft_dedisp/2):, :]

            ''' # making figures
            fig = plt.figure(figsize=(9, 5))
            ax1 = fig.add_subplot(111)
            ax1.imshow(np.flipud(10*np.log10(np.power(np.abs(spectra), 2))), aspect='auto', cmap='jet')
            ax1.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
            ax1.set_xlabel('Time points', fontsize=6, fontweight='bold')
            pylab.savefig('01_Initial_spectra_' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
            plt.close('all')

            fig = plt.figure(figsize=(9, 5))
            ax1 = fig.add_subplot(111)
            ax1.plot(10*np.log10(np.power(np.abs(spectra[:, 0]), 2)), linestyle='-', linewidth='1.00', label='Initial waveform')
            ax1.legend(loc='upper right', fontsize=6)
            ax1.grid(b=True, which='both', color='silver', linestyle='-')
            ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
            pylab.savefig('02_Initial_imm_spectra' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
            plt.close('all')
            '''
            
            #  Dispersion delay removing
            data_space = np.zeros((freq_points_num, 2 * max_shift), dtype='complex')
            data_space[:, max_shift:] = spectra[:, :]
            data_space = pulsar_DM_compensation_with_indices_changes(data_space, shift_vector)
            del spectra

            # Adding the next data block
            buffer_array += data_space

            # Making and filling the array with fully ready data for plotting and saving to a file
            array_compensated_DM = buffer_array[:, 0: max_shift]

            if bunch > 0:
                # Saving data with compensated DM
                spectra = array_compensated_DM.copy()

                '''
                # making figures
                fig = plt.figure(figsize=(9, 5))
                ax1 = fig.add_subplot(111)
                ax1.imshow(np.flipud(10*np.log10(np.power(np.abs(spectra), 2))), aspect='auto', cmap='jet')
                ax1.set_ylabel('Frequency points', fontsize=6, fontweight='bold')
                ax1.set_xlabel('Time points', fontsize=6, fontweight='bold')
                pylab.savefig('03_Compensated_spectra_' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
                plt.close('all')

                fig = plt.figure(figsize=(9, 5))
                ax1 = fig.add_subplot(111)
                ax1.plot(10*np.log10(np.power(np.abs(spectra[:,0]), 2)), linestyle='-', linewidth='1.00', label='Initial waveform')
                ax1.legend(loc='upper right', fontsize=6)
                ax1.grid(b=True, which='both', color='silver', linestyle='-')
                ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
                pylab.savefig('04_Compensated_imm_spectra' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
                plt.close('all')
                '''

                wf_data = np.zeros((no_of_points_for_fft_dedisp, no_of_spectra_in_bunch))

                # Add lost half of the spectra

                second_spectra_half = spectra.copy()
                second_spectra_half = np.flipud(second_spectra_half)
                spectra = np.concatenate((second_spectra_half, spectra), axis=0)  # Changed places!!!

                '''
                fig = plt.figure(figsize=(9, 5))
                ax1 = fig.add_subplot(111)
                ax1.plot(10*np.log10(np.power(np.abs(spectra[:,0]), 2)), linestyle='-', linewidth='1.00', label='Initial waveform')
                ax1.legend(loc='upper right', fontsize=6)
                ax1.grid(b=True, which='both', color='silver', linestyle='-')
                ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
                pylab.savefig('05_Compensated_doubled_imm_spectra' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
                plt.close('all')
                '''

                # Making IFFT
                for i in range(no_of_spectra_in_bunch):
                    wf_data[:, i] = np.real(np.fft.ifft(spectra[:, i]))
                del spectra

                # Reshaping the waveform to single dimension (real)
                wf_data = np.reshape(wf_data, [no_of_points_for_fft_dedisp * no_of_spectra_in_bunch, 1], order='F')

                ''' # making figures
                fig = plt.figure(figsize=(9, 5))
                ax1 = fig.add_subplot(111)
                ax1.plot(wf_data, linestyle='-', linewidth='1.00', label='Initial waveform')
                ax1.legend(loc='upper right', fontsize=6)
                ax1.grid(b=True, which='both', color='silver', linestyle='-')
                ax1.set_ylabel('Intensity, a.u.', fontsize=6, fontweight='bold')
                pylab.savefig('06_Compensated_waveform_' + str(bunch) + '.png', bbox_inches='tight', dpi=160)
                plt.close('all')
                '''
                
                # Saving waveform data to wf32 file
                file_data = open(file_data_name, 'ab')
                file_data.write(np.float32(wf_data).transpose().copy(order='C'))  # C
                file_data.close()

                # !!! Saving time data to timeline file !!!

            # Rolling temp_array to put current data first
            buffer_array = np.roll(buffer_array, - max_shift)
            buffer_array[:, max_shift:] = 0

        bar.finish()

    return file_data_name


# *******************************************************************************
#          W A V E F O R M   F L O A T 3 2   T O   S P E C T R A                *
# *******************************************************************************

def convert_wf32_to_dat(fname, no_of_points_for_fft):
    '''
    function converts waverform data in .wf32 format to spectra in .dat format
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

    freq_points_num = int(no_of_points_for_fft/2)

    with open(fname, 'rb') as file:
        # *** Data file header read ***
        file_header = file.read(1024)

        # *** Creating a binary file with data for long data storage ***
        file_data_name = fname[:-5] + '.dat'
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

        # *** Creating a name for long timeline TXT file ***
        tl_file_name = file_data_name + '_Timeline.txt'
        tl_file = open(tl_file_name, 'w')  # Open and close to delete the file with the same name
        tl_file.close()

        # Calculation of number of blocks and number of spectra in the file
        no_of_spectra_in_bunch = 512
        no_of_bunches_per_file = int((df_filesize - 1024) / (no_of_spectra_in_bunch * no_of_points_for_fft * 4))

        # Real time resolution of averaged spectra
        fine_clock_freq = (int(clock_freq / 1000000.0) * 1000000.0)
        real_spectra_dt = float(no_of_points_for_fft / fine_clock_freq)
        real_spectra_df = float((fine_clock_freq / 2) / (no_of_points_for_fft / 2 ))

        print(' Number of spectra in bunch:                  ', no_of_spectra_in_bunch)
        print(' Number of bunches to read in file:           ', no_of_bunches_per_file)
        print(' Time resolution of calculated spectra:       ', round(real_spectra_dt*1000, 3), ' ms')
        print(' Frequency resolution of calculated spectra:  ', round(real_spectra_df/1000, 3), ' kHz')
        print('\n  *** Reading data from file *** \n')

        file.seek(1024)  # Jumping to 1024 byte from file beginning

        # !!! Fake timing. Real timing to be done!!!
        #TimeFigureScaleFig = np.linspace(0, no_of_bunches_per_file, no_of_bunches_per_file+1)
        #for i in range(no_of_bunches_per_file):
        #    TimeFigureScaleFig[i] = str(TimeFigureScaleFig[i])

        time_scale_bunch = []

        bar = IncrementalBar(' Conversion from waveform to spectra: ', max=no_of_bunches_per_file-1, suffix='%(percent)d%%')

        for bunch in range(no_of_bunches_per_file-1):

            bar.next()

            #print(' Making spectra bunch # ', bunch+1, ' of ', no_of_bunches_per_file-1)

            # Reading and reshaping all data with time data

            wf_data = np.fromfile(file, dtype='f4', count = no_of_spectra_in_bunch * no_of_points_for_fft)
            wf_data = np.reshape(wf_data, [no_of_points_for_fft, no_of_spectra_in_bunch], order='F')

            # preparing matrices for spectra
            spectra = np.zeros_like(wf_data)

            # Calculation of spectra
            for i in range(no_of_spectra_in_bunch):
                spectra[:, i] = np.power(np.abs(np.fft.fft(wf_data[:, i])), 2)

            # Storing only first (left) mirror part of spectra
            spectra = spectra[: int(no_of_points_for_fft/2), :]

            # At 33 MHz the specter is usually upside down, to correct it we use flip up/down
            if int(clock_freq/1000000) == 33:
                spectra = np.flipud(spectra)

            # Saving spectra data to dat file
            temp = spectra.transpose().copy(order='C')
            file_data = open(file_data_name, 'ab')
            file_data.write(np.float64(temp))
            file_data.close()

            # Saving time data to ling timeline file
            #with open(tl_file_name, 'a') as tl_file:
            #    for i in range(no_of_spectra_in_bunch):
            #        tl_file.write((str(time_scale_bunch[i][:])) + ' \n')  # str

        bar.finish()

    file.close()  # Close the data file
    return file_data_name


################################################################################
# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    print('\n\n\n\n\n\n\n\n   ********************************************************************')
    print('   * ', Software_name, ' v.', Software_version, ' *      (c) YeS 2020')
    print('   ******************************************************************** \n\n\n')
    
    startTime = time.time()
    previousTime = startTime
    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")
    print('  Today is ', currentDate, ' time is ', currentTime, '\n')

    dedispersed_wf32_files = []
    dedispersed_dat_files = []

    print('\n\n  * Converting waveform from JDS to WF32 format... \n\n')

    initial_wf32_files = convert_jds_wf_to_wf32(source_directory, result_directory, no_of_bunches_per_file)
    print('\n List of WF32 files: ', initial_wf32_files, '\n')

    # result_wf32_files = ['E280120_205409.jds_Data_chA.wf32']
    print('\n\n  * Making coherent dispersion delay removing... \n\n')
    file_name = coherent_wf_to_wf_dedispersion(0.3, initial_wf32_files[0], no_of_points_for_fft_dedisp)
    dedispersed_wf32_files.append(file_name)
    print('\n List of dedispersed WF32 files: ', initial_wf32_files, '\n')

    # dedispersed_wf32_files = ['DM_0.3_E280120_205409.jds_Data_chA.wf32']
    print('\n\n  * Making DAT files spectra of dedispersed wf32 data... \n\n')
    file_name = convert_wf32_to_dat(dedispersed_wf32_files[0], no_of_points_for_fft)
    dedispersed_dat_files.append(file_name)
    print('\n List of dedispersed DAT files: ', dedispersed_dat_files, '\n')

    print('\n\n  * Making dynamic spectra figures of the dedispersed data... \n\n')
    result_folder_name = source_directory.split('/')[-2] + '_dedispersed'
    #dedispersed_dat_files = ['DM_0.3_E280120_205409.jds']
    file_name = dedispersed_dat_files[0].replace('_Data_chA.dat', '')
    ok = DAT_file_reader('', file_name, typesOfData, '', result_folder_name,
                         0, 0, 0, -120, -10, 0, 6, 6, 300, 'jet', 0, 0, 0, 20 * 10 ** (-12),
                         16.5, 33.0, '', '', 16.5, 33.0, [], 0)

    endTime = time.time()
    print ('\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                    round((endTime - startTime)/60, 2), 'min. ) \n')
    print ('\n\n                 *** ', Software_name, ' has finished! *** \n\n\n')
