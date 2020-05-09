# Python3
Software_version = '2020.05.01'
Software_name = 'MARK5 reader'
# Script intended to read, show and analyze data from MARK5 receiver
#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
directory = 'DATA/'
filename = 'pul_b1133+16_ir_no0048.m5a'

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



# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

def mark_5_data_header_read(file):

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

    filepath = directory + filename

    file_size = (os.stat(filepath).st_size)  # Size of file
    print('\n   File size:                    ', round(file_size / 1024 / 1024, 3), ' Mb (', file_size, ' bytes )')


    with open(filepath, 'rb') as file:


        print('\n *  First data frame header info:')
        data_frame_length, num_of_channels, bits_per_sample, dt_file_start = mark_5_data_header_read(file)

        frames_in_file = file_size / (data_frame_length * 8)
        print('\n   Frames in file:                     ', frames_in_file)

        data_bytes_length = data_frame_length * 8 - 32
        samples_in_16_bit_word = int(16 / num_of_channels / bits_per_sample)
        samples_in_frame = int(data_bytes_length / 2) / samples_in_16_bit_word
        print('   Samples in frame:                   ', samples_in_frame)
        print('   Samples in file:                    ', samples_in_frame * frames_in_file)


        file.seek(0)  # Jumping to the file beginning
        no_of_frames_to_average = 2
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

        # Each of channels
        rc('font', size=6, weight='bold')
        fig = plt.figure(1, figsize=(12.0, 5.0))
        fig.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=0.35)

        ax1 = fig.add_subplot(241)
        ax1.plot(unpacked_data[0, 0:100])
        ax1.set_xlim([-2, 102])
        ax1.set_ylim([0, 3])
        ax1.set_title('Channel 1', fontsize=8, fontweight='bold', y=1.025)
        ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax1.set_xlabel('Samples, #', fontsize=6, fontweight='bold')

        ax2 = fig.add_subplot(242)
        ax2.plot(unpacked_data[1, 0:100])
        ax2.set_xlim([-2, 102])
        ax2.set_ylim([0, 3])
        ax2.set_title('Channel 2', fontsize=8, fontweight='bold', y=1.025)
        ax2.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax2.set_xlabel('Samples, #', fontsize=6, fontweight='bold')

        ax3 = fig.add_subplot(243)
        ax3.plot(unpacked_data[2, 0:100])
        ax3.set_xlim([-2, 102])
        ax3.set_ylim([0, 3])
        ax3.set_title('Channel 3', fontsize=8, fontweight='bold', y=1.025)
        ax3.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax3.set_xlabel('Samples, #', fontsize=6, fontweight='bold')

        ax4 = fig.add_subplot(244)
        ax4.plot(unpacked_data[3, 0:100])
        ax4.set_xlim([-2, 102])
        ax4.set_ylim([0, 3])
        ax4.set_title('Channel 4', fontsize=8, fontweight='bold', y=1.025)
        ax4.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax4.set_xlabel('Samples, #', fontsize=6, fontweight='bold')


        ax5 = fig.add_subplot(245)
        ax5.plot(unpacked_data[4, 0:100])
        ax5.set_xlim([-2, 102])
        ax5.set_ylim([0, 3])
        ax5.set_title('Channel 5', fontsize=8, fontweight='bold', y=1.025)
        ax5.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax5.set_xlabel('Samples, #', fontsize=6, fontweight='bold')

        ax6 = fig.add_subplot(246)
        ax6.plot(unpacked_data[5, 0:100])
        ax6.set_xlim([-2, 102])
        ax6.set_ylim([0, 3])
        ax6.set_title('Channel 6', fontsize=8, fontweight='bold', y=1.025)
        ax6.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax6.set_xlabel('Samples, #', fontsize=6, fontweight='bold')

        ax7 = fig.add_subplot(247)
        ax7.plot(unpacked_data[6, 0:100])
        ax7.set_xlim([-2, 102])
        ax7.set_ylim([0, 3])
        ax7.set_title('Channel 7', fontsize=8, fontweight='bold', y=1.025)
        ax7.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax7.set_xlabel('Samples, #', fontsize=6, fontweight='bold')

        ax8 = fig.add_subplot(248)
        ax8.plot(unpacked_data[7, 0:100])
        ax8.set_xlim([-2, 102])
        ax8.set_ylim([0, 3])
        ax8.set_title('Channel 8', fontsize=8, fontweight='bold', y=1.025)
        ax8.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax8.set_xlabel('Samples, #', fontsize=6, fontweight='bold')

        pylab.savefig('MARK5_verification_channels.png', bbox_inches='tight', dpi=300)
        plt.close('all')

