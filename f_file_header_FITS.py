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
from f_plot_formats import plot2D, TwoDynSpectraPlot #, OneImmedSpecterPlot, TwoImmedSpectraPlot,


################################################################################

def FileHeaderReaderFITS(filepath):
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



    file = open(filepath, 'rb')
    hdul = fits.open(filepath)
    #hdul.info()

    # Header 0
    hdr = hdul[0].header

    print(' \n')
    print(' Length of header = ', len(hdr), '\n')
    for i in range (len(hdr)):
        print (' %2i' % i, ' %50s: ' % hdr.comments[i], hdr[i])

    df_system_name = hdr[17]
    df_obs_place = hdr[16]
    print(' \n')

    # print(repr(hdr)) - representation as it is in file
    # print(list(hdr.keys())) - prints all keywords in header

    '''
    hdr1 = hdul[1].header
    print(' \n')
    print(' Length of header = ', len(hdr1), '\n')
    for i in range (len(hdr1)):
        print (' %2i' % i, ' %50s: ' % hdr1.comments[i], hdr1[i])
    '''

    # Header 1
    cols = hdul[1].columns
    data = hdul[1].data
    #cols.info()
    #print(data.shape)
    #print(data.dtype.name)
    for i in range (17):
        print('   * ', cols.names[i], '   ', cols.units[i])
        #print(data.field(i))

    frequency_list = data.field(1)

    print(' \n')

    # Header 2
    cols = hdul[2].columns
    data = hdul[2].data
    for i in range (16):
        print('   * %15s' % cols.names[i], ' %5s ' % cols.units[i], ' %40s ' % data.field(i))



    df_description = cols.units[0]


    print(' \n')

    cols = hdul[3].columns
    data = hdul[3].data
    for i in range (4):
        print('   * %15s' % cols.names[i], ' %5s ' % cols.units[i], ' %40s ' % data.field(i))



    print(' \n')

    cols = hdul[4].columns
    data = hdul[4].data
    for i in range (4):
        print('   * %15s' % cols.names[i], ' %5s ' % cols.units[i], ' %40s ' % data.field(i))


    print(' \n')

    cols = hdul[5].columns
    data = hdul[5].data
    for i in range (4):
        print('   * ', cols.names[i], '   ', cols.units[i])
        #print(data.field(i))

    print(' \n')

    cols = hdul[6].columns
    data = hdul[6].data
    for i in range (4):
        print('   * ', cols.names[i], '   ', cols.units[i])
        #print(data.field(i))

    print(' \n')

    cols = hdul[7].columns
    data = hdul[7].data
    for i in range (2):
        print('   * ', cols.names[i], '   ', cols.units[i])
        #print(data.field(i))
    print(' \n')


    FreqPointsNum = 412
    dynamic_spectra = data.field(1)
    dynamic_spectra = dynamic_spectra[:, :, 0:FreqPointsNum]

    time_JD = data.field(0)
    time_line = Time(time_JD, format='jd', scale='utc')
    nt = time_line.shape[0]
    time_line_str = time_line.iso


    with np.errstate(divide='ignore'):
        dynamic_spectra = 10*np.log10(dynamic_spectra)

    dynamic_spectra1 = dynamic_spectra[:,0,:]
    dynamic_spectra2 = dynamic_spectra[:,1,:]
    Nim, pol, freq_num = dynamic_spectra.shape
    print('   * Shape of dynamic spectra matrix: ', dynamic_spectra.shape)
    print('   * Shape of frequency list:         ', frequency_list.shape)
    print('   * Shape of time line:              ', nt)


    # ***    F I G U R E S   ***


    plt.figure(1, figsize=(10.0, 6.0))
    plt.subplots_adjust(left=None, bottom=0, right=None, top=0.86, wspace=None, hspace=None)
    plt.plot(dynamic_spectra1[0, 0:FreqPointsNum])
    plt.plot(dynamic_spectra2[0, 0:FreqPointsNum])
    pylab.savefig('FITS_Results/Immediate spectrum.png', bbox_inches='tight', dpi = 300)
    plt.close('all')



    Vmin = 65
    Vmax = 110
    figID = 0
    figMAX = 1
    TimeRes = 1
    df = 0
    sumDifMode = ''
    df_filename = filepath
    SpInFrame = 1
    FrameInChunk = 1
    ReceiverMode = 'Spectra mode'
    TimeFigureScale = time_line_str
    TimeScale = time_line_str
    SpectrNum = Nim
    frequency = np.linspace(0,FreqPointsNum,FreqPointsNum+1)
    colormap = 'jet'
    df_filename = 'filename______'


# *** FIGURE Initial dynamic spectrum channels A and B (python 3 new version) ***

    TwoDynSpectraPlot(np.flipud(dynamic_spectra1), np.flipud(dynamic_spectra2),
        Vmin, Vmax, Vmin, Vmax,
        'Dynamic spectrum (initial) ',
        figID, figMAX, TimeRes, df, sumDifMode, df_system_name, df_obs_place,
        df_filename, df_description, 'Intensity, dB', 'Intensity, dB', Nim,
        SpInFrame, FrameInChunk, ReceiverMode, TimeFigureScale, TimeScale,
        SpectrNum, frequency, FreqPointsNum, colormap,
        'Channel A', 'Channel B',
        'FITS_Results/',
        ' Initial dynamic spectrum fig.',
        currentDate, currentTime, Software_version, 300)



    Normalization_dB(dynamic_spectra1, FreqPointsNum, nt)
    Normalization_dB(dynamic_spectra2, FreqPointsNum, nt)


    # *** FIGURE Dynamic spectrum channels A and B cleaned and normalized (python 3 new version) ***
    VminNorm = 0
    VmaxNorm = 12



    TwoDynSpectraPlot(np.flipud(dynamic_spectra1), np.flipud(dynamic_spectra2),
        VminNorm, VmaxNorm, VminNorm, VmaxNorm,
        'Dynamic spectrum (normalized) ',
        figID, figMAX, TimeRes, df, sumDifMode, df_system_name, df_obs_place,
        df_filename, df_description, 'Intensity, dB', 'Intensity, dB', Nim,
        SpInFrame, FrameInChunk, ReceiverMode, TimeFigureScale, TimeScale,
        SpectrNum, frequency, FreqPointsNum, colormap,
        'Channel A', 'Channel B',
        'FITS_Results/',
        ' Dynamic spectrum fig.',
        currentDate, currentTime, Software_version, 300)



    print(' \n\n\n')

    hdul.close()




    #return df_filename, df_filesize, df_system_name, df_obs_place, df_description, F_ADC, df_creation_timeUTC, ReceiverMode, ADRmode, sumDifMode, NAvr, TimeRes, frequency[0], frequency[FreqPointsNum-1], df, frequency, FFT_Size, SLine, Width, BlockSize


################################################################################

if __name__ == '__main__':

    filename = 'DATA/20190329_102000_BST.fits'

    print('\n\n * Parameters of the file: ')

    FileHeaderReaderFITS(filename)