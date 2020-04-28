#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
# Common functions
import sys
import numpy as np
from os import path
from datetime import datetime
from datetime import timedelta


# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_plot_formats.plot_formats import plot1D

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

    print('\n * Low-level parameters:')
    print('\n   Seconds from epoch begin:  ', seconds_from_epoch_begin, ' s.')
    print('   Invalid data marker:       ', invalid_data_marker)
    print('   Legacy header length:      ', legacy_header_length)
    print('   Data frame number:         ', data_frame_no, ' of ?')
    print('   Number of the epoch:       ', epoch_no, ' (number of half years from 2000-01-01)')
    print('   VDIF version number:       ', vdif_version_no)
    print('   Number of channels:        ', num_of_channels)
    print('   Data frame length:         ', data_frame_length, ' (units of 8 bytes)')
    print('   Data type:                 ', data_type, ' (0 - real, 1 - complex)')
    print('   Bits per sample:           ', bits_per_sample, ' bits')
    print('   Thread ID:                 ', thread_id, ' ')
    print('   Station ID:                ', station_id, ' ')
    print('   Extended data version:     ', extended_data_version, ' ')


    if epoch_no == 40: epoch_start = '2020-01-01 00:00:00'

    dt_epoch_start = datetime(int(epoch_start[0:4]), int(epoch_start[5:7]), int(epoch_start[8:10]),
                                  int(epoch_start[11:13]), int(epoch_start[14:16]),
                                  int(epoch_start[17:19]), 0)

    dt_file_start = dt_epoch_start + timedelta(seconds = int(seconds_from_epoch_begin))

    print('\n * High-level parameters:')
    print('\n   Date and time of first data frame:  ', dt_file_start)

    return data_frame_length, num_of_channels, bits_per_sample

################################################################################

if __name__ == '__main__':

    directory = 'DATA/'
    filename = 'pulsar_ir_no40.m5a'
    fname = directory + filename
    no_of_samples_to_average = 1024000  #64000
    with open(fname, 'rb') as file:

        # Reading first frame header
        data_frame_length, num_of_channels, bits_per_sample = mark_5_data_header_read(file)


        data_bytes_length = data_frame_length * 8 - 32
        samples_in_16_bit_word = int(16 / num_of_channels / bits_per_sample)
        samples_in_frame = int(data_bytes_length/2) / samples_in_16_bit_word
        print('\n   Samples in frame:', samples_in_frame)

        no_of_frames_to_average = int(no_of_samples_to_average / samples_in_frame)
        print('\n   Number of frames to average:', no_of_frames_to_average)

        #raw_data = np.fromfile(file, dtype='i2', count=int(data_bytes_length/2))
        #unpacked_data = np.zeros((int(num_of_channels), int(4 * data_bytes_length / num_of_channels)), dtype=np.uint8)

        file.seek(0)  # Jumping to the file beginning

        profile = []

        for i in range (1200):

            raw_data = np.fromfile(file, dtype='i2', count=int((data_frame_length * 8 / 2) * no_of_frames_to_average))
            raw_data = np.reshape(raw_data, [int(data_frame_length * 8 / 2), no_of_frames_to_average], order='F')
            raw_data = raw_data[16: , :]
            raw_data = np.reshape(raw_data, [int((data_frame_length * 8 / 2)-16) * no_of_frames_to_average], order='F')
            #print(raw_data.shape)


            unpacked_data = np.zeros((int(num_of_channels), int(no_of_frames_to_average * 4 * data_bytes_length / num_of_channels)), dtype=np.uint8)

            unpacked_data[0, :] = raw_data[:] & 3
            unpacked_data[1, :] = np.right_shift(raw_data[:] & 12, 2)
            unpacked_data[2, :] = np.right_shift(raw_data[:] & 48, 4)
            unpacked_data[3, :] = np.right_shift(raw_data[:] & 192, 6)
            unpacked_data[4, :] = np.right_shift(raw_data[:] & 768, 8)
            unpacked_data[5, :] = np.right_shift(raw_data[:] & 3072, 10)
            unpacked_data[6, :] = np.right_shift(raw_data[:] & 12288, 12)
            unpacked_data[7, :] = np.right_shift(raw_data[:] & 49152, 14)

            #del raw_data
            #channel_sum_array = np.sum(unpacked_data, axis = 0)
            sum = np.sum(unpacked_data)
            profile.append(sum)
            #print(channel_sum_array.shape)

        plot1D(profile, 'Fig.1.png', 'Profile', 'Profile', 'xxx', 'xxx', 300)

        # Reading frame header
        data_frame_length, num_of_channels, bits_per_sample = mark_5_data_header_read(file)


'''
Частота оцифровки была 64 МГц. На выходе нужно примерно 1 кГц. Т.е. 
сжать массив данных в 64К раз.
 хотелось бы сделать уплотненный массив, у которого
можно было бы менять параметр сжатия (например, можно взять 8 мс, как на
УТР-2, когда мы меряем пульсары, а для этого нужно сжимать в 512К раз).
Все частотные каналы можно объединить в один (дисперсионное запаздывание
для В1133+16 на 1.4 ГГц будет около 0.5 мс).
'''