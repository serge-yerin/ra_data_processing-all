'''
'''
#import struct
import os
#import math
import numpy as np
#import datetime
import time
import pylab
from astropy.io import fits
from astropy.time import Time
import matplotlib.pyplot as plt

from f_spectra_normalization import Normalization_dB
from f_plot_formats import plot2D, TwoDynSpectraPlot, TwoImmedSpectraPlot #, OneImmedSpecterPlot


################################################################################

def FileHeaderReaderFITS(foldpath, filename):
    '''
    Reads info from FITS (.fits) data file header and returns needed parameters to the main script
    Input parameters:

    Output parameters:

    '''

    #*************************************************************
    #                       MAIN PROGRAM                         *
    #*************************************************************
    # Python3
    Software_version = '2019.04.08'

    for i in range(8): print (' ')
    print ('   ****************************************************')
    print ('   *      FITS data files reader  v.',Software_version,'      *      (c) YeS 2019')
    print ('   ****************************************************')
    for i in range(3): print (' ')


    startTime = time.time()
    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")
    print ('  Today is ', currentDate, ' time is ', currentTime)
    print (' ')

    newpath = "FITS_Results"
    if not os.path.exists(newpath):
        os.makedirs(newpath)



    file = open(foldpath + filename, 'rb')
    hdul = fits.open(foldpath + filename)
    #hdul.info()
    print ('  File: ', filename)
    
    
    num_of_groups = 8
    num_of_fields = np.zeros(num_of_groups, dtype = 'int')
    num_of_column = np.zeros(num_of_groups, dtype = 'int')
    for i in range (num_of_groups):
        num_of_fields[i] = int(hdul.info(0)[i][4])
 
    for group in range (1, num_of_groups):
        num_of_column[group] = int(len(hdul[group].columns))
        
    
    
    
    print('\n * Header # 0   PRIMARY \n')
    for i in range (len(hdul[0].header)):
        print (' %2i' % i, ' %50s: ' % hdul[0].header.comments[i], hdul[0].header[i])
        
        
    
    for group in range (1, num_of_groups):
        print ('\n ********************************************************************************** \n')
        print(' * Header # ', group,'   ', hdul.info(0)[group][1],'\n')
        for i in range (num_of_column[group]):
            
            hdr = hdul[0].header
            cols = hdul[1].columns
            data = hdul[1].data
            
            
            if hdul[group].data.field(i).shape == (1,):  
                temp_string = hdul[group].data.field(i)[0]
            else:
                temp_string = 'Data dimensions = ' + str(hdul[group].data.field(i).shape)
            print (' %2i' % i, ' %15s' % hdul[group].columns.names[i], ' %10s ' % hdul[group].columns.units[i], temp_string)
            
            #hdul[group].data.field(i)
            #print (' * %2i' % i, ' %50s: ' % hdul[group].header.comments[i], hdul[group].header[i])
            # print(repr(hdul[group].header)) - representation as it is in file
            # print(list(hdul[group].header.keys())) - prints all keywords in header
    
    print ('\n ********************************************************************************** \n')
    print ('\n Plotting figures... \n\n\n')
    
    
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
    
    
    for beam in range(0, no_digit_beams):
        num_beamlet[beam] = hdul[4].data.field('nbbeamlet')[beam]
        beam_list[beam, :] = hdul[4].data.field('beamletlist')[beam]
        beam_freq[beam, :] = hdul[4].data.field('freqlist')[beam]
    
    
        frequency = np.zeros([no_digit_beams, num_beamlet[beam]])
        frequency[:,:] = beam_freq[beam, 0:num_beamlet[beam]]

        _, FreqPointsNum = frequency.shape

 
    dynamic_spectra = hdul[7].data.field(1)
    dynamic_spectra = dynamic_spectra[:, :, 0 : FreqPointsNum]

    time_JD = hdul[7].data.field(0)
    time_line = Time(time_JD, format='jd', scale='utc')
    nt = time_line.shape[0]
    time_line_str = time_line.iso


    with np.errstate(divide='ignore'):
        dynamic_spectra = 10*np.log10(dynamic_spectra)

    dynamic_spectra1 = dynamic_spectra[:,0,:]
    dynamic_spectra2 = dynamic_spectra[:,1,:]
    Nim, pol, freq_num = dynamic_spectra.shape
    
    
    # ***    F I G U R E S   ***

    Vmin = np.min([np.min(dynamic_spectra1[0, 0:FreqPointsNum]), np.min(dynamic_spectra2[0, 0:FreqPointsNum])])
    Vmax = np.max([np.max(dynamic_spectra1[0, 0:FreqPointsNum]), np.max(dynamic_spectra2[0, 0:FreqPointsNum])])

    TwoImmedSpectraPlot(frequency[0,:], dynamic_spectra1[0, 0:FreqPointsNum], dynamic_spectra2[0, 0:FreqPointsNum],
                        Label01, Label02,
                        frequency[0,0], frequency[0, FreqPointsNum-1], Vmin-3, Vmax+3,
                        'Frequency, MHz', 'Intensity, dB',
                        'Immediate spectrum', 'for file ' + filename + ', Description: ' + df_description,
                        'FITS_Results/' + filename + '_Immediate spectrum.png',
                        currentDate, currentTime, Software_version)

    figID = 0
    figMAX = 1
    sumDifMode = ''
    SpInFrame = 1
    FrameInChunk = 1
    ReceiverMode = 'Spectra mode'
    TimeFigureScale = time_line_str
    TimeScale = time_line_str


# *** FIGURE Initial dynamic spectrum channels A and B (python 3 new version) ***

    TwoDynSpectraPlot(np.flipud(dynamic_spectra1), np.flipud(dynamic_spectra2),
        np.min(dynamic_spectra1), np.max(dynamic_spectra1), np.min(dynamic_spectra2), np.max(dynamic_spectra2),
        'Dynamic spectrum (initial) ',
        figID, figMAX, TimeRes, df, sumDifMode, df_system_name, df_obs_place,
        filename, df_description, 'Intensity, dB', 'Intensity, dB', Nim,
        SpInFrame, FrameInChunk, ReceiverMode, TimeFigureScale, TimeScale,
        Nim, frequency[0,:], FreqPointsNum, 'jet',
        'Channel A', 'Channel B',
        'FITS_Results/',
        ' Initial dynamic spectrum fig.',
        currentDate, currentTime, Software_version, 300)


    Normalization_dB(dynamic_spectra1, FreqPointsNum, nt)
    Normalization_dB(dynamic_spectra2, FreqPointsNum, nt)


    # *** FIGURE Dynamic spectrum channels A and B cleaned and normalized (python 3 new version) ***
    VminNorm = 0
    VmaxNorm = 15


    TwoDynSpectraPlot(np.flipud(dynamic_spectra1), np.flipud(dynamic_spectra2),
        VminNorm, VmaxNorm, VminNorm, VmaxNorm,
        'Dynamic spectrum (normalized) ',
        figID, figMAX, TimeRes, df, sumDifMode, df_system_name, df_obs_place,
        filename, df_description, 'Intensity, dB', 'Intensity, dB', Nim,
        SpInFrame, FrameInChunk, ReceiverMode, TimeFigureScale, TimeScale,
        Nim, frequency[0,:], FreqPointsNum, 'jet',
        'Channel A', 'Channel B',
        'FITS_Results/',
        ' Normalized dynamic spectrum fig.',
        currentDate, currentTime, Software_version, 300)



    print(' \n\n\n')

    hdul.close()



    #return df_filename, df_filesize, df_system_name, df_obs_place, df_description, F_ADC, df_creation_timeUTC, ReceiverMode, ADRmode, sumDifMode, NAvr, TimeRes, frequency[0], frequency[FreqPointsNum-1], df, frequency, FFT_Size, SLine, Width, BlockSize


################################################################################

if __name__ == '__main__':

    filename = '20190406_002900_BST.fits'
    foldpath = 'DATA/'

    print('\n\n * Parameters of the file: ')

    FileHeaderReaderFITS(foldpath, filename)
