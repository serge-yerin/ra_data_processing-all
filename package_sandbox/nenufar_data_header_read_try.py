# Python3
Software_version = '2020.05.22'
Software_name = 'NenuFAR tf reader'
# Script intended to read, show and analyze data from MARK5 receiver
#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
directory = 'DATA/'
filename = 'JUPITER_TRACKING_20200510_030440_0.spectra'



#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
# Common functions
import sys
import numpy as np
from os import path
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib import rc
import pylab
import os
import time
from astropy.time import Time


def nenufar_tf_data_header_read(file):
    '''
    First try to read NenuFAR spectra data header
    '''

    # *** Data file header read ***

    sample_index_of_block = np.uint64(int.from_bytes(file.read(8), byteorder='little', signed=False))
    time_stamp = np.uint64(int.from_bytes(file.read(8), byteorder='little', signed=False))
    block_seq_number = np.uint64(int.from_bytes(file.read(8), byteorder='little', signed=False))
    fft_length = np.int32(int.from_bytes(file.read(4), byteorder='little', signed=True))
    intergrated_spectra_num = np.int32(int.from_bytes(file.read(4), byteorder='little', signed=True))
    fft_overlap = np.int32(int.from_bytes(file.read(4), byteorder='little', signed=True))
    apodization = np.int32(int.from_bytes(file.read(4), byteorder='little', signed=True))
    fft_per_beamlet = np.int32(int.from_bytes(file.read(4), byteorder='little', signed=True))
    channels_beamlets_no = np.int32(int.from_bytes(file.read(4), byteorder='little', signed=True))


    frequency_resolution = 0.1953125 / fft_length  # MHz
    time_resolution = fft_length * intergrated_spectra_num * 5.12  # uS

    print('\n   DATA FRAME HEADER:')

    print('   Sample index of block:            ', sample_index_of_block)
    print('   Time stamp:                       ', time_stamp)
    print('   Block sequence number:            ', block_seq_number)
    print('   Length of FFT:                    ', fft_length)
    print('   Number of integrated spectra:     ', intergrated_spectra_num)
    print('   FFT overlapping:                  ', fft_overlap)
    print('   Apodization:                      ', apodization)
    print('   FFTs per beamlet:                 ', fft_per_beamlet)
    print('   Number of beamlets / channels:    ', channels_beamlets_no)

    print('\n   Frequency resolution:             ', frequency_resolution*1000, ' kHz')
    print('   Time resolution:                  ', time_resolution/1000, ' mS')
    print('   Time satmp:                       ',time.strftime("%Y.%m.%d %H:%M:%S", time.gmtime(time_stamp)))  #"%Y %b %d (%a) %H:%M:%S +0000"
    #t = Time(time.gmtime(time_stamp), scale = 'utc')
    dt_object = datetime.fromtimestamp(time_stamp)
    t = Time(dt_object, format = 'datetime', scale='utc')
    print('   Time satmp (jd):                  ', t.jd )

    return fft_length, fft_per_beamlet, channels_beamlets_no

################################################################################

if __name__ == '__main__':

    # To change system path to main directory of the project:
    if __package__ is None:
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    print('\n\n\n\n\n\n\n\n   **************************************************************************')
    print('   *               ', Software_name, ' v.', Software_version, '              *      (c) YeS 2020')
    print('   ************************************************************************** \n')

    startTime = time.time()
    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")
    print('   Today is ', currentDate, ' time is ', currentTime, '\n')
    '''
    # *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
    result_path = 'RESULTS_MARK5_Reader'
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    '''
    filepath = directory + filename

    file_size = os.stat(filepath).st_size  # Size of file
    print('\n   File size:                    ', round(file_size / 1024 / 1024, 3), ' Mb (', file_size, ' bytes )')

    with open(filepath, 'rb') as file:

        # Reading first frame header
        print('\n *  First data frame header info:')
        fft_length, fft_per_beamlet, channels_beamlets_no = nenufar_tf_data_header_read(file)
        ######################################################
        '''
        file.seek(0)  # Jumping to the file beginning

        block_header_length = 48 # bytes
        beamlet_header_length = 12 # bytes
        data_beamlet_length = 2 * fft_length * fft_per_beamlet * 4
        block_length = block_header_length + channels_beamlets_no * (beamlet_header_length + data_beamlet_length)

        n = 2
        raw_data = np.fromfile(file, dtype='f4', count=int(n * block_length))

        raw_data = np.reshape(raw_data, [block_length, n], order='F')
        block_headers = raw_data[:12, :]
        raw_data = raw_data[12:, :]
        raw_data = np.reshape(raw_data, [(block_length - 12) * n], order='F')



        '''
        ######################################################
        for beamlet in range(channels_beamlets_no):  # channels_beamlets_no

            lane_index = np.int32(int.from_bytes(file.read(4), byteorder='little', signed=True))
            beam_index = np.int32(int.from_bytes(file.read(4), byteorder='little', signed=True))
            beamlet_index = np.int32(int.from_bytes(file.read(4), byteorder='little', signed=True))

            print('\n   Lane index:                       ', lane_index)
            print('   Beam index:                       ', beam_index)
            print('   Beamlet index:                    ', beamlet_index)

            raw_data = np.fromfile(file, dtype='i4', count=int(4 * fft_length * fft_per_beamlet))

            #raw_data = np.reshape(raw_data, [fft_per_beamlet, fft_length], order='F')


        fft_length, fft_per_beamlet, channels_beamlets_no = nenufar_tf_data_header_read(file)

        '''
        # PLOTS
        Title = 'File: , recorded on , samples averaged: '
        rc('font', size=8, weight='bold')
        fig = plt.figure(1, figsize=(12.0, 5.0))
        ax1 = fig.add_subplot(111)
        fig.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
        ax1.plot(raw_data[:,0], label='First spectrum')
        #ax1.set_xlim([0, points_in_bunch])
        #ax1.set_ylim([y_min_sum, y_max_sum])
        ax1.set_title('Title', fontsize=10, fontweight='bold', y=1.025)
        ax1.legend(loc='upper right', fontsize=8)
        ax1.set_ylabel('Amplitude, AU', fontsize=10, fontweight='bold')
        ax1.set_xlabel('Freq, ', fontsize=10, fontweight='bold')
        #fig.text(0.78, -0.07, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=5,
        #         transform=plt.gcf().transFigure)
        #fig.text(0.1, -0.07, 'Software version: ' + Software_version + ' yerin.serge@gmail.com, IRA NASU', fontsize=5,
        #         transform=plt.gcf().transFigure)
        pylab.savefig('NenuFAR_first_specrum.png', bbox_inches='tight', dpi=300)
        plt.close('all')
        '''








        '''
        frames_in_file = file_size / (data_frame_length * 8)
        print('\n   Frames in file:                     ', frames_in_file)

        data_bytes_length = data_frame_length * 8 - 32
        samples_in_16_bit_word = int(16 / num_of_channels / bits_per_sample)
        samples_in_frame = int(data_bytes_length/2) / samples_in_16_bit_word
        print('   Samples in frame:                   ', samples_in_frame)
        print('   Samples in file:                    ', samples_in_frame * frames_in_file)
        print('   Points in bunch:                    ', points_in_bunch)

        no_of_frames_to_average = int(no_of_samples_to_average / samples_in_frame)
        print('   Frames in bunch:                    ', points_in_bunch * no_of_frames_to_average)
        print('   Number of frames to average:        ', no_of_frames_to_average)

        no_of_bunches = int(frames_in_file / (points_in_bunch * no_of_frames_to_average))
        print('   Bunches in file:                    ', no_of_bunches)
        no_of_bunches = int(no_of_bunches)
        print('   Bunches in file (integer):          ', no_of_bunches, '\n')


        # making long DAT file to store average data
        if save_aver_data > 0:
            file.seek(0)  # Jumping to the file beginning
            file_header = file.read(32)
            dat_file_name = filename.replace('.','_') + '.dat'
            dat_file = open(dat_file_name, 'wb')
            dat_file.write(file_header)
            dat_file.close()

        #raw_data = np.fromfile(file, dtype='i2', count=int(data_bytes_length/2))
        #unpacked_data = np.zeros((int(num_of_channels), int(4 * data_bytes_length / num_of_channels)), dtype=np.uint8)

        file.seek(0)  # Jumping to the file beginning



        no_of_bunches = no_of_bunches

        for bunch in range(no_of_bunches):
            currentTime = time.strftime("%H:%M:%S")
            print('   Bunch ' + str(bunch+1)+' of '+str(no_of_bunches) + '   started at: ' + currentTime)
            profile = []
            channel_profiles = []
            for i in range (points_in_bunch):  #

                raw_data = np.fromfile(file, dtype='i2', count=int((data_frame_length * 8 / 2) * no_of_frames_to_average))
                raw_data = np.reshape(raw_data, [int(data_frame_length * 8 / 2), no_of_frames_to_average], order='F')
                raw_data = raw_data[16: , :]
                raw_data = np.reshape(raw_data, [int((data_frame_length * 8 / 2)-16) * no_of_frames_to_average], order='F')


                unpacked_data = np.zeros((int(num_of_channels), int(no_of_frames_to_average * 4 * data_bytes_length / num_of_channels)), dtype=np.uint8)

                unpacked_data[0, :] = raw_data[:] & 3
                unpacked_data[1, :] = np.right_shift(raw_data[:] & 12, 2)
                unpacked_data[2, :] = np.right_shift(raw_data[:] & 48, 4)
                unpacked_data[3, :] = np.right_shift(raw_data[:] & 192, 6)
                unpacked_data[4, :] = np.right_shift(raw_data[:] & 768, 8)
                unpacked_data[5, :] = np.right_shift(raw_data[:] & 3072, 10)
                unpacked_data[6, :] = np.right_shift(raw_data[:] & 12288, 12)
                unpacked_data[7, :] = np.right_shift(raw_data[:] & 49152, 14)

                channel_profiles.append(np.sum(unpacked_data, axis = 1))
                profile.append(np.sum(unpacked_data))

            channel_profiles = np.array(channel_profiles)
            profile = np.array(profile, dtype = np.uint32)

            # Store averaged data to long DAT file
            if save_aver_data > 0:
                temp = profile.copy(order='C')
                dat_file = open(dat_file_name, 'ab')
                dat_file.write(temp)
                dat_file.close()

            if save_figures > 0:
                # PLOTS
                Title = 'File: ' + filename + ', recorded on ' + str(dt_file_start) +', samples averaged: ' + str(no_of_samples_to_average)
                # Sum of channels
                rc('font', size=8, weight='bold')
                fig = plt.figure(1, figsize=(12.0, 5.0))
                ax1 = fig.add_subplot(111)
                fig.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
                ax1.plot(profile, label='Sum of channels')
                ax1.set_xlim([0, points_in_bunch])
                ax1.set_ylim([y_min_sum, y_max_sum])
                ax1.set_title(Title, fontsize=10, fontweight='bold', y=1.025)
                ax1.legend(loc='upper right', fontsize=8)
                ax1.set_ylabel('Amplitude, AU', fontsize=10, fontweight='bold')
                ax1.set_xlabel('Averaged samples, #', fontsize=10, fontweight='bold')
                fig.text(0.78, -0.07, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=5,
                         transform=plt.gcf().transFigure)
                fig.text(0.1, -0.07, 'Software version: ' + Software_version + ' yerin.serge@gmail.com, IRA NASU', fontsize=5,
                         transform=plt.gcf().transFigure)
                pylab.savefig(result_path + '/MARK5_sum_of_channels_fig.'+str(bunch+1)+' of '+str(no_of_bunches)+'.png',
                              bbox_inches='tight', dpi=300)
                plt.close('all')

                # Each of channels
                fig = plt.figure(1, figsize=(12.0, 5.0))
                ax1 = fig.add_subplot(111)
                fig.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
                for i in range(num_of_channels):
                    ax1.plot(channel_profiles[:, i], label='Channel '+str(i+1))
                ax1.set_xlim([0, points_in_bunch])
                ax1.set_ylim([y_min_chan, y_max_chan])
                ax1.set_title(Title, fontsize=10, fontweight='bold', y=1.025)
                ax1.legend(loc='upper right', fontsize=8)
                ax1.set_ylabel('Amplitude, AU', fontsize=10, fontweight='bold')
                ax1.set_xlabel('Averaged samples, #', fontsize=10, fontweight='bold')
                fig.text(0.78, -0.07, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=5,
                         transform=plt.gcf().transFigure)
                fig.text(0.1, -0.07, 'Software version: ' + Software_version + ' yerin.serge@gmail.com, IRA NASU', fontsize=5,
                         transform=plt.gcf().transFigure)
                pylab.savefig(result_path + '/MARK5_channels_fig.'+str(bunch+1)+' of '+str(no_of_bunches)+'.png',
                              bbox_inches='tight', dpi=300)
                plt.close('all')


        # Reading frame header
        #data_frame_length, num_of_channels, bits_per_sample, dt_file_start = mark_5_data_header_read(file)
        '''
endTime = time.time()    # Time of calculations

print ('\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n          *** ', Software_name, ' has finished! *** \n\n\n')


