# Python3
# Errors found while analyzing data from the receiver
# 1 - wrong FFT size value (zero instead of )
# 2 - something wrong is with second of the day and phase of the second

Software_version = '2019.05.09'
# Program intended to read, show and analyze data from DSPZ receivers
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
# Common functions
import os
import math
import numpy as np
import time
import gc
import datetime
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pylab

# My functions
from package_plot_formats.plot_formats import TwoDynSpectraPlot, TwoOrOneValuePlot
from package_ra_data_processing.f_spectra_normalization import normalization_db
from package_ra_data_files_formats.read_file_header_njds import file_header_njds_read
from package_ra_data_files_formats.FPGA_to_PC_array import FPGAtoPCarrayJDS
from package_cleaning.simple_channel_clean import simple_channel_clean

# *******************************************************************************
#                         M A I N    F U N C T I O N                            *
# *******************************************************************************


# *********************************************************************************

# *** Opening datafile ***
fname = 'e:/RA_DATA_ARCHIVE/NJDS_cross_spectra_new_DSP_receiver/A230620_134825.jds'
# fname = 'e:/RA_DATA_ARCHIVE/DSP_cross_spectra_B0809+74_URAN2/P130422_121607.jds'
corr_process = True

# *** Data file header read ***
[df_filename, df_filesize, df_system_name, df_obs_place, df_description,
    clc_freq, df_creation_time_utc, sp_in_file, receiver_mode, mode, n_avr, time_resol, fmin, fmax,
    df, frequency, freq_points_num, data_block_size] = file_header_njds_read(fname, 0, 1)


with open(fname, 'rb') as file:
    file.seek(1024)  # Jumping to 1024 byte from file beginning

    if 0 < mode < 3:           # Spectra modes
        n_sp = 1
        if mode == 2:
            raw = np.fromfile(file, dtype='u4', count=(4 * n_sp * freq_points_num))

            raw = np.reshape(raw, [4 * freq_points_num, n_sp], order='F')

            data_cha = raw[0:(freq_points_num*4):4, :].transpose()
            data_chb = raw[1:(freq_points_num*4):4, :].transpose()
            data_cre = raw[2:(freq_points_num*4):4, :].transpose()
            data_cim = raw[3:(freq_points_num*4):4, :].transpose()

            del raw

            # *** Single out timing from data ***
            # counter_a2 = np.uint64(data_cha[:, -1])
            # counter_b2 = np.uint64(data_chb[:, -1])
            # counter_a1 = np.uint64(data_cha[:, -2])
            # counter_b1 = np.uint64(data_chb[:, -2])

            # *** Converting from FPGA to PC float format ***
            # if mode == 1 or mode == 2:
            #     data_cha = FPGAtoPCarrayJDS(data_cha, n_avr)
                # data_chb = FPGAtoPCarrayJDS(data_chb, n_avr)
            # if mode == 2 and corr_process == 1:
                # data_cre = FPGAtoPCarrayJDS(data_cre, n_avr)
                # data_cim = FPGAtoPCarrayJDS(data_cim, n_avr)

            # *** Converting to logarithmic scale matrices ***
            # if mode == 1 or mode == 2:
            #     with np.errstate(invalid='ignore'):
            #         data_cha = 10 * np.log10(data_cha)
            #         # data_chb = 10 * np.log10(data_chb)
                # data_cha[np.isnan(data_cha)] = -120
                # data_chb[np.isnan(data_chb)] = -120
            # if mode == 2 and corr_process == 1:
            #     with np.errstate(invalid='ignore', divide='ignore'):
                    # corr_module = 10 * np.log10((data_cre ** 2 + data_cim ** 2) ** 0.5)
                    # corr_phase = np.arctan2(data_cim, data_cre)
                # corr_phase[np.isnan(corr_phase)] = 0
                # corr_module[np.isinf(corr_module)] = -135.5

print(data_cha.shape)

plt.figure(1)
plt.subplot(221)
plt.plot(data_cha[0])
plt.subplot(222)
plt.plot(data_chb[0])
plt.subplot(223)
plt.plot(data_cre[0])
plt.subplot(224)
plt.plot(data_cim[0])

plt.show()
# pylab.savefig('result.png', bbox_inches='tight', dpi=250)
plt.close('all')


# *******************************************************************************
#                                   F I G U R E S                               *
# *******************************************************************************


file.close()  # Here we close the data file



