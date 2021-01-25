import os
import sys
import numpy as np
from progress.bar import IncrementalBar

# *******************************************************************************
#      C O H E R E N T   S U M   O F   W A V E F O R M    F L O A T 3 2         *
# *******************************************************************************


def sum_signals_of_wf32_files(file_name_1, file_name_2, no_of_spectra_in_bunch):
    """
    Function that takes two wf32 files and makes sum of signals from these files in output wf32 file
    """

    if 'chA' in file_name_1 and 'chB' in file_name_2:
        result_file_name = file_name_1.replace('chA', 'wfA+B')
    elif 'chB' in file_name_1 and 'chA' in file_name_2:
        result_file_name = file_name_1.replace('chB', 'wfA+B')
    else:
        result_file_name = file_name_1[:-4] + '_sum_' + file_name_2

    df_filesize_1 = os.stat(file_name_1).st_size                         # Size of file
    df_filesize_2 = os.stat(file_name_2).st_size                         # Size of file
    if df_filesize_1 != df_filesize_2:
        print('  Size of file 1:    ', df_filesize_1, '\n  Size of file 2:', df_filesize_2)
        sys.exit('   ERROR!!! Files have different sizes!')

    # Calculation of the dimensions of arrays to read
    ny = int((df_filesize_1 - 1024) / 4)   # number of samples to read: file size - 1024 bytes
    num_of_blocks = int(ny // (no_of_spectra_in_bunch * 10000))

    file_1 = open(file_name_1, 'rb')
    file_2 = open(file_name_2, 'rb')
    out_file = open(result_file_name, 'wb')

    file_header = file_1.read(1024)
    out_file.write(file_header)
    del file_header
    file_1.seek(1024)
    file_2.seek(1024)

    bar = IncrementalBar(' Making sum of two signals: ', max=num_of_blocks - 1,
                         suffix='%(percent)d%%')

    for block in range(num_of_blocks):

        bar.next()

        if block == (num_of_blocks - 1):
            samples_num_in_bunch = ny - (num_of_blocks - 1) * no_of_spectra_in_bunch * 10000
        else:
            samples_num_in_bunch = no_of_spectra_in_bunch * 10000

        data_1 = np.fromfile(file_1, dtype=np.float32, count=samples_num_in_bunch)
        data_2 = np.fromfile(file_2, dtype=np.float32, count=samples_num_in_bunch)
        data = data_1 + data_2
        out_file.write(np.float32(data).transpose().copy(order='C'))

    bar.finish()
    file_1.close()
    file_2.close()
    out_file.close()

    # Time line file copying

    # Making copy of timeline file with needed name and extension
    initial_timeline_name = file_name_1.split('_Data')[0] + '_Timeline.wtxt'
    result_timeline_name = result_file_name + '_Timeline.wtxt'

    # Creating a new timeline TXT file for results
    new_tl_file = open(result_timeline_name, 'w')  # Open and close to delete the file with the same name
    new_tl_file.close()

    # Reading timeline file
    old_tl_file = open(initial_timeline_name, 'r')
    new_tl_file = open(result_timeline_name, 'w')

    # Read time from timeline file
    time_scale_bunch = old_tl_file.readlines()

    # Saving time data to new file
    for i in range(len(time_scale_bunch)):
        new_tl_file.write((time_scale_bunch[i][:]) + '')

    old_tl_file.close()
    new_tl_file.close()

    return result_file_name


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':
    no_of_spectra_in_bunch = 16384  # Number of spectra samples to read while conversion to dat (depends on RAM)
    file_name_1 = 'E280120_205546.jds_Data_chA.wf32'
    file_name_2 = 'E280120_205546.jds_Data_chB.wf32'

    file_name = sum_signals_of_wf32_files(file_name_1, file_name_2, no_of_spectra_in_bunch)

    print('Names of files: ', file_name)
