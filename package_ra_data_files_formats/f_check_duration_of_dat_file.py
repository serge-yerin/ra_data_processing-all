
from datetime import datetime
from package_ra_data_files_formats.time_line_file_reader import time_line_file_reader
import os

def check_duration_of_dat_file(path_to_dat_file, dat_file_name):
    """
    Reading timeline file and store data in lists of text and datetime data formats
    """

    tl_file_name = dat_file_name.split('_Data_')[0]
    tl_file_name += '_Timeline.txt'
    try:
        timeline, dt_timeline = time_line_file_reader(os.path.join(path_to_dat_file, tl_file_name))
        duration = dt_timeline[-1] - dt_timeline[0]
    except FileNotFoundError:
        duration = ''
        dt_timeline = ['', '']
    return dt_timeline[0], dt_timeline[-1], duration


if __name__ == '__main__':

    path = 'e:/RA_DATA_RESULTS/B0809+74_DSP_cross_spectra_B0809+74_URAN2/'
    fname = 'B0809+74_DM_5.755_P130422_121607.jds_Data_chA.dat'

    print('\n\n File: ', fname)

    start, stop, dur = check_duration_of_dat_file(path, fname)

    print(' Time duration: ', dur)
