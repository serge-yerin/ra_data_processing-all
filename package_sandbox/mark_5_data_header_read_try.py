# Python3
Software_version = '2020.05.01'
Software_name = 'MARK5 reader'
# Script intended to read, show and analyze data from MARK5 receiver
#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
directory = 'DATA/'
filename = 'pul_b1133+16_ir_no0048.m5a'
no_of_samples_to_average = 512000  # 64000
points_in_bunch = 1280
y_min_sum = 6180000   #6170000
y_max_sum = 6195000   #6185000
y_min_chan = 766000   # 765000
y_max_chan = 783000   # 781000
save_aver_data = 1
save_figures = 1
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


# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


def mark_5_data_header_read(file):
    '''
    First try to read Mark 5 data header
    '''

    A = np.uint32(int('00111111111111111111111111111111', 2))
    B = np.uint32(int('10000000000000000000000000000000', 2))
    C = np.uint32(int('01000000000000000000000000000000', 2))
    D = np.uint32(int('00000000111111111111111111111111', 2))
    E = np.uint32(int('00111111000000000000000000000000', 2))
    F = np.uint32(int('11100000000000000000000000000000', 2))
    G = np.uint32(int('00011111000000000000000000000000', 2))
    H = np.uint32(int('01111100000000000000000000000000', 2))
    I = np.uint32(int('00000011111111110000000000000000', 2))
    J = np.uint32(int('00000000000000001111111111111111', 2))
    K = np.uint32(int('11111111000000000000000000000000', 2))

    # *** Data file header read ***
    file_header = file.read(32)
    # Word 0
    word_0 = np.uint32(int.from_bytes(file_header[0:4], byteorder='little', signed=False))
    seconds_from_epoch_begin = np.uint32(np.bitwise_and(word_0, A))
    invalid_data_marker = np.uint32(np.bitwise_and(word_0, B))
    legacy_header_length = np.uint32(np.bitwise_and(word_0, C))
    # Word 1
    word_1 = np.uint32(int.from_bytes(file_header[4:8], byteorder='little', signed=False))
    data_frame_no = np.uint32(np.bitwise_and(word_1, D))
    epoch_no = np.uint32(np.right_shift(np.bitwise_and(word_1, E), 24))
    # Word 2
    word_2 = np.uint32(int.from_bytes(file_header[8:12], byteorder='little', signed=False))
    vdif_version_no = np.uint32(np.right_shift(np.bitwise_and(word_2, F), 29))
    log_channel_no = np.uint32(np.right_shift(np.bitwise_and(word_2, G), 24))
    data_frame_length = np.uint32(np.bitwise_and(word_2, D))

    # Word 3
    word_3 = np.uint32(int.from_bytes(file_header[12:16], byteorder='little', signed=False))
    data_type = np.uint32(np.right_shift(np.bitwise_and(word_3, B), 31))
    bits_per_sample = 1 + np.uint32(np.right_shift(np.bitwise_and(word_3, H), 26))
    thread_id = np.uint32(np.right_shift(np.bitwise_and(word_3, I), 16))
    station_id = np.uint32(np.right_shift(np.bitwise_and(word_3, J), 0))

    # Word 4
    word_4 = np.uint32(int.from_bytes(file_header[16:20], byteorder='little', signed=False))
    extended_data_version = np.uint32(np.right_shift(np.bitwise_and(word_4, K), 24))

    num_of_channels = np.power(2, log_channel_no)

    print('\n   DATA FRAME HEADER:')
    print('   Seconds from epoch begin:           ', seconds_from_epoch_begin, ' s.')
    print('   Invalid data marker:                ', invalid_data_marker)
    print('   Legacy header length:               ', legacy_header_length)
    print('   Data frame number:                  ', data_frame_no, ' of ?')
    print('   Number of the epoch:                ', epoch_no, ' (number of half years from 2000-01-01)')
    print('   VDIF version number:                ', vdif_version_no)
    print('   Number of channels:                 ', num_of_channels)
    print('   Data frame length:                  ', data_frame_length, ' (units of 8 bytes)')
    print('   Data type:                          ', data_type, ' (0 - real, 1 - complex)')
    print('   Bits per sample:                    ', bits_per_sample, ' bits')
    print('   Thread ID:                          ', thread_id, ' ')
    print('   Station ID:                         ', station_id, ' ')
    print('   Extended data version:              ', extended_data_version, ' ')

    if epoch_no == 39: epoch_start = '2019-06-01 00:00:00'
    if epoch_no == 40: epoch_start = '2020-01-01 00:00:00'
    if epoch_no == 41: epoch_start = '2020-06-01 00:00:00'

    dt_epoch_start = datetime(int(epoch_start[0:4]), int(epoch_start[5:7]), int(epoch_start[8:10]),
                                  int(epoch_start[11:13]), int(epoch_start[14:16]),
                                  int(epoch_start[17:19]), 0)

    dt_file_start = dt_epoch_start + timedelta(seconds = int(seconds_from_epoch_begin))

    print('   Date and time of first data frame:  ', dt_file_start)

    return data_frame_length, num_of_channels, bits_per_sample, dt_file_start

################################################################################

if __name__ == '__main__':

    print('\n\n\n\n\n\n\n\n   **************************************************************************')
    print('   *               ', Software_name, ' v.', Software_version, '              *      (c) YeS 2018')
    print('   ************************************************************************** \n')

    startTime = time.time()
    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")
    print('   Today is ', currentDate, ' time is ', currentTime, '\n')

    # *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
    result_path = 'RESULTS_MARK5_Reader'
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    filepath = directory + filename

    file_size = (os.stat(filepath).st_size)  # Size of file
    print('\n   File size:                    ', round(file_size / 1024 / 1024, 3), ' Mb (', file_size, ' bytes )')

    with open(filepath, 'rb') as file:

        # Reading first frame header
        print('\n *  First data frame header info:')
        data_frame_length, num_of_channels, bits_per_sample, dt_file_start = mark_5_data_header_read(file)

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

endTime = time.time()    # Time of calculations

print ('\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n          *** ', Software_name, ' has finished! *** \n\n\n')



'''
Частота оцифровки была 64 МГц. На выходе нужно примерно 1 кГц. Т.е.
сжать массив данных в 64К раз.
 хотелось бы сделать уплотненный массив, у которого
можно было бы менять параметр сжатия (например, можно взять 8 мс, как на
УТР-2, когда мы меряем пульсары, а для этого нужно сжимать в 512К раз).
Все частотные каналы можно объединить в один (дисперсионное запаздывание
для В1133+16 на 1.4 ГГц будет около 0.5 мс).
'''
