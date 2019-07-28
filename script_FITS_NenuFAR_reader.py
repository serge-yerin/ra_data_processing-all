# Python3
Software_version = '2019.04.13'
#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
foldpath = 'DATA/'
filename = '20190407_094300_BST.fits'

VminNorm = 0                # Min value on normalized spectra plot
VmaxNorm = 10               # Max value on normalized spectra plot

colormap = 'jet'            # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
customDPI = 300             # Resolution of images of dynamic spectra
################################################################################
#*******************************************************************************
#                              L I B R A R I E S                               *
#*******************************************************************************
import os
import numpy as np
import time
import pylab
from astropy.io import fits
from astropy.time import Time
import matplotlib.pyplot as plt

from package_ra_data_processing.spectra_normalization import Normalization_dB
from package_plot_formats.plot_formats import plot2D, TwoDynSpectraPlot, TwoOrOneValuePlot #, OneImmedSpecterPlot
from package_ra_data_files_formats.file_header_FITS import FileHeaderReaderFITS

################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************

print ('\n\n\n\n\n\n\n\n   ****************************************************')
print ('   *      FITS data files reader  v.', Software_version,'      *      (c) YeS 2019')
print ('   **************************************************** \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)
print (' ')

newpath = "FITS_Results"
if not os.path.exists(newpath):
    os.makedirs(newpath)

FileHeaderReaderFITS(foldpath, filename)

print ('\n Reading data and plotting figures... \n')

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

num_beamlet = np.zeros((no_digit_beams, ), dtype = int)     # number of beamlets (subbands) per beam
beam_list = np.zeros((no_digit_beams, 768), dtype = int)    # list of subbands
beam_freq = np.zeros((no_digit_beams, 768), dtype = float)  # list of frequencies


# Reading and forming list of freqiencies for all beamlets
for beam in range(0, no_digit_beams):
    num_beamlet[beam] = hdul[4].data.field('nbbeamlet')[beam]
    beam_list[beam, :] = hdul[4].data.field('beamletlist')[beam]
    beam_freq[beam, :] = hdul[4].data.field('freqlist')[beam]

frequency = np.zeros([no_digit_beams, num_beamlet[beam]])
frequency[:,:] = beam_freq[beam, 0:num_beamlet[beam]]
_, FreqPointsNum = frequency.shape


# Reading time line and convert from JD to UTC
time_JD = hdul[7].data.field('jd') # 0
time_line = Time(time_JD, format='jd', scale='utc')
nt = time_line.shape[0]
time_line_str = time_line.iso


# Reading dynamic spectra data
dynamic_spectra = hdul[7].data.field('DATA')
dynamic_spectra = dynamic_spectra[:, :, 0 : FreqPointsNum]

with np.errstate(divide='ignore'):                      # Conversion to dB
    dynamic_spectra = 10*np.log10(dynamic_spectra)

dynamic_spectra1 = dynamic_spectra[:,0,:]
dynamic_spectra2 = dynamic_spectra[:,1,:]
no_of_spectra, pol, freq_num = dynamic_spectra.shape


# ******************************************************************************
# ***                           F I G U R E S                                ***
# ******************************************************************************

# Calculation of min and max values in both channels
Vmin = np.min([np.min(dynamic_spectra1[0, 0:FreqPointsNum]), np.min(dynamic_spectra2[0, 0:FreqPointsNum])])
Vmax = np.max([np.max(dynamic_spectra1[0, 0:FreqPointsNum]), np.max(dynamic_spectra2[0, 0:FreqPointsNum])])

# *** FIGURE Immediate spectra of initial data ***
TwoOrOneValuePlot(2, frequency[0,:],  dynamic_spectra1[0, 0:FreqPointsNum],  dynamic_spectra2[0, 0:FreqPointsNum],
                    Label01, Label02, frequency[0,0], frequency[0, FreqPointsNum-1],
                    Vmin-3, Vmax+3, Vmin-3, Vmax+3, 'Frequency, MHz', 'Intensity, dB', 'Intensity, dB',
                    'Immediate spectrum', 'for file ' + filename + ', Description: ' + df_description,
                    'FITS_Results/' + filename[0:19] + ' ' + str(df_description).replace('"','') + ' Immediate spectrum.png',
                    currentDate, currentTime, Software_version)

# Preparing variables for figure
figID = 0
figMAX = 1
sumDifMode = ''
ReceiverMode = 'Spectra mode'
fig_file_name = 'FITS_Results/' + filename[0:19] + ' ' + str(df_description).replace('"','') + ' Initial dynamic spectrum fig.' + str(figID+1) + '.png'
Suptitle = 'Dynamic spectrum (initial) ' + str(filename)+' - Fig. '+str(figID+1)+' of '+str(figMAX)+'\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz, '+sumDifMode+' Receiver: '+str(df_system_name)+', Place: '+str(df_obs_place)+'\n'+ReceiverMode+', Description: '+str(df_description)

TimeFigureScaleFig = np.empty_like(time_line_str)
TimeScaleFig = np.empty_like(time_line_str)
for i in range (len(time_line_str)):
    TimeFigureScaleFig[i] = time_line_str[i][0:11]
    TimeScaleFig[i] = time_line_str[i][11:23]

# *** FIGURE Initial dynamic spectra channels A and B ***
TwoDynSpectraPlot(dynamic_spectra1.transpose(), dynamic_spectra2.transpose(),
            np.min(dynamic_spectra1), np.max(dynamic_spectra1), np.min(dynamic_spectra2), np.max(dynamic_spectra2),
            Suptitle, 'Intensity, dB', 'Intensity, dB', no_of_spectra,
            TimeFigureScaleFig, TimeScaleFig, frequency[0,:],
            FreqPointsNum, colormap, 'Channel A - '+Label01, 'Channel B - '+Label02,
            fig_file_name, currentDate, currentTime, Software_version, customDPI)


# Normalization of data (extracting the frequency responce of the signal path)
Normalization_dB(dynamic_spectra1, FreqPointsNum, nt)
Normalization_dB(dynamic_spectra2, FreqPointsNum, nt)


# Preparing variables for figure
fig_file_name = 'FITS_Results/' + filename[0:19] + ' ' + str(df_description).replace('"','') + ' Normalized dynamic spectrum fig.' + str(figID+1) + '.png'
Suptitle = 'Dynamic spectrum (normalized) ' + str(filename)+' - Fig. '+str(figID+1)+' of '+str(figMAX)+'\n Initial parameters: dt = '+str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz, '+sumDifMode+' Receiver: '+str(df_system_name)+', Place: '+str(df_obs_place)+'\n'+ReceiverMode+', Description: '+str(df_description)

# *** FIGURE Dynamic spectra channels A and B normalized ***
TwoDynSpectraPlot(dynamic_spectra1.transpose(), dynamic_spectra2.transpose(),
            VminNorm, VmaxNorm, VminNorm, VmaxNorm,
            Suptitle, 'Intensity, dB', 'Intensity, dB', no_of_spectra,
            TimeFigureScaleFig, TimeScaleFig, frequency[0,:],
            FreqPointsNum, colormap, 'Channel A - '+Label01, 'Channel B - '+Label02,
            fig_file_name, currentDate, currentTime, Software_version, customDPI)

hdul.close()

endTime = time.time()    # Time of calculations

print (' The program execution lasted for ', round((endTime - startTime),2), 'seconds')
print(' \n\n')
print ('       * * *    Program NenuFAR FITS reader has finished!    * * *')
print(' \n\n\n')
