# Python3
Software_version = '2021.12.25'
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
foldpath = '../RA_DATA_ARCHIVE/NenuFAR_beamstatistic_file_Jupiter/'
filename = '20210724_015600_BST.fits'

VminNorm = 0                # Min value on normalized spectra plot
VmaxNorm = 10               # Max value on normalized spectra plot

colormap = 'jet'            # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
customDPI = 300             # Resolution of images of dynamic spectra

single_plot_for_digital_beams = True

# *******************************************************************************
#                               L I B R A R I E S                               *
# *******************************************************************************
import os
import numpy as np
import time
from astropy.io import fits
from astropy.time import Time

from package_ra_data_processing.spectra_normalization import Normalization_dB
from package_plot_formats.plot_formats import TwoDynSpectraPlot, TwoOrOneValuePlot  # OneImmedSpecterPlot, plot2D
from package_ra_data_files_formats.file_header_FITS import file_header_reader_fits


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************

print('\n\n\n\n\n\n\n\n   ****************************************************')
print('   *      FITS data files reader  v.', Software_version, '      *      (c) YeS 2019')
print('   **************************************************** \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print('  Today is ', currentDate, ' time is ', currentTime, ' \n')

newpath = "FITS_Results"
if not os.path.exists(newpath):
    os.makedirs(newpath)

file_header_reader_fits(foldpath, filename)

print('\n Reading data and plotting figures... \n')

hdul = fits.open(foldpath + filename)

df_system_name = hdul[0].header[17]
df_obs_place = hdul[0].header[16]
TimeRes = (1 / float(hdul[0].header[14]))
df = 1000 * float(hdul[0].header[13][0:8])

Label01 = hdul[1].data.field(14)[0, 0]
Label02 = hdul[1].data.field(14)[0, 1]

df_description = hdul[2].data.field(0)[0]
no_analog_beams = int(hdul[2].data.field(6)[0])
no_digit_beams = int(hdul[2].data.field(7)[0])

num_beamlet = np.zeros((no_digit_beams, ), dtype=int)     # number of beamlets (subbands) per beam
beam_list = np.zeros((no_digit_beams, 768), dtype=int)    # list of subbands
beam_freq = np.zeros((no_digit_beams, 768), dtype=float)  # list of frequencies


# Reading and forming list of frequencies for all beamlets
for beam in range(0, no_digit_beams):
    num_beamlet[beam] = hdul[4].data.field('nbbeamlet')[beam]
    beam_list[beam, :] = hdul[4].data.field('beamletlist')[beam]
    beam_freq[beam, :] = hdul[4].data.field('freqlist')[beam]

# frequency = np.zeros([no_digit_beams, num_beamlet[beam]])
# frequency[:, :] = beam_freq[beam, 0:num_beamlet[beam]]
# _, freq_points_num = frequency.shape

# If we want to built all beams in a single spectra as they are two subbands of single source observation
if single_plot_for_digital_beams:

    frequency = beam_freq[0, 0: num_beamlet[0]]
    # If there are more than one digital beam - add frequencies from each one
    for beam in range(1, no_digit_beams):
        frequency = np.concatenate((frequency[:], beam_freq[beam, 0: num_beamlet[beam]]))

    freq_points_num = frequency.shape[0]


# Reading time line and convert from JD to UTC
time_JD = hdul[7].data.field('jd')  # 0
time_line = Time(time_JD, format='jd', scale='utc')
nt = time_line.shape[0]
time_line_str = time_line.iso


# Reading dynamic spectra data
dynamic_spectra = hdul[7].data.field('DATA')
dynamic_spectra = dynamic_spectra[:, :, 0: freq_points_num]

with np.errstate(divide='ignore'):                      # Conversion to dB
    dynamic_spectra = 10*np.log10(dynamic_spectra)

dynamic_spectra1 = dynamic_spectra[:, 0, :]
dynamic_spectra2 = dynamic_spectra[:, 1, :]
no_of_spectra, pol, freq_num = dynamic_spectra.shape


# ******************************************************************************
# ***                           F I G U R E S                                ***
# ******************************************************************************

# Calculation of min and max values in both channels
Vmin = np.min([np.min(dynamic_spectra1[0, 0:freq_points_num]), np.min(dynamic_spectra2[0, 0:freq_points_num])])
if Vmin == float('-inf') or Vmin == float('inf'):
    Vmin = -50
Vmax = np.max([np.max(dynamic_spectra1[0, 0:freq_points_num]), np.max(dynamic_spectra2[0, 0:freq_points_num])])
if Vmax == float('-inf') or Vmax == float('inf'):
    Vmax = 250


# *** FIGURE Immediate spectra of initial data ***
TwoOrOneValuePlot(2, frequency[:],  dynamic_spectra1[0, 0:freq_points_num],  dynamic_spectra2[0, 0:freq_points_num],
                  Label01, Label02, frequency[0], frequency[-1],
                  Vmin-3, Vmax+3, Vmin-3, Vmax+3, 'Frequency, MHz', 'Intensity, dB', 'Intensity, dB',
                  'Immediate spectrum', 'for file ' + filename + ', Description: ' + df_description,
                  'FITS_Results/' + filename[0:19] + ' ' + str(df_description).replace('"', '') +
                  ' Immediate spectrum.png', currentDate, currentTime, Software_version)

# Preparing variables for figure
figID = 0
figMAX = 1
sumDifMode = ''
ReceiverMode = 'Spectra mode'
fig_file_name = 'FITS_Results/' + filename[0:19] + ' ' + str(df_description).replace('"', '') + \
                ' Initial dynamic spectrum fig.' + str(figID+1) + '.png'
Suptitle = 'Dynamic spectrum (initial) ' + str(filename)+' - Fig. ' + str(figID+1)+' of ' + \
           str(figMAX) + '\n Initial parameters: dt = '+str(round(TimeRes*1000, 3)) + ' ms, df = ' + \
           str(round(df/1000., 3))+' kHz, ' + sumDifMode + ' Receiver: ' + str(df_system_name) + \
           ', Place: ' + str(df_obs_place) + '\n' + ReceiverMode + ', Description: ' + str(df_description)

TimeFigureScaleFig = np.empty_like(time_line_str)
TimeScaleFig = np.empty_like(time_line_str)
for i in range(len(time_line_str)):
    TimeFigureScaleFig[i] = time_line_str[i][0:11]
    TimeScaleFig[i] = time_line_str[i][11:23]

# *** FIGURE Initial dynamic spectra channels A and B ***
TwoDynSpectraPlot(dynamic_spectra1.transpose(), dynamic_spectra2.transpose(), np.min(dynamic_spectra1),
                  np.max(dynamic_spectra1), np.min(dynamic_spectra2), np.max(dynamic_spectra2), Suptitle,
                  'Intensity, dB', 'Intensity, dB', no_of_spectra, TimeFigureScaleFig, TimeScaleFig, frequency[:],
                  freq_points_num, colormap, 'Channel A - ' + Label01, 'Channel B - ' + Label02, fig_file_name,
                  currentDate, currentTime, Software_version, customDPI)

# Normalization of data (extracting the frequency response of the signal path)
Normalization_dB(dynamic_spectra1, freq_points_num, nt)
Normalization_dB(dynamic_spectra2, freq_points_num, nt)


# Preparing variables for figure
fig_file_name = 'FITS_Results/' + filename[0:19] + ' ' + str(df_description).replace('"', '') + \
                ' Normalized dynamic spectrum fig.' + str(figID+1) + '.png'
Suptitle = 'Dynamic spectrum (normalized) ' + str(filename) + ' - Fig. ' + str(figID+1) + ' of ' + str(figMAX) + \
           '\n Initial parameters: dt = ' + str(round(TimeRes*1000, 3)) + ' ms, df = ' + str(round(df/1000., 3)) + \
           ' kHz, ' + sumDifMode + ' Receiver: ' + str(df_system_name) + ', Place: ' + str(df_obs_place) + \
           '\n' + ReceiverMode + ', Description: ' + str(df_description)

# *** FIGURE Dynamic spectra channels A and B normalized ***
TwoDynSpectraPlot(dynamic_spectra1.transpose(), dynamic_spectra2.transpose(), VminNorm, VmaxNorm, VminNorm, VmaxNorm,
                  Suptitle, 'Intensity, dB', 'Intensity, dB', no_of_spectra, TimeFigureScaleFig, TimeScaleFig,
                  frequency[:], freq_points_num, colormap, 'Channel A - ' + Label01, 'Channel B - ' + Label02,
                  fig_file_name, currentDate, currentTime, Software_version, customDPI)

hdul.close()

endTime = time.time()    # Time of calculations

print(' The program execution lasted for ', round((endTime - startTime), 2), 'seconds')
print('\n\n       * * *    Program NenuFAR FITS reader has finished!    * * *\n\n\n')
