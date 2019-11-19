# Python3
Software_version = '2019.05.08'
# Program intended to read and show data from DAT files

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
common_path = '' # '/media/data/PYTHON/ra_data_processing-all/' #

# Directory of DAT file to be analyzed:
filename = common_path + 'A170328_060429.adr_Data_chA.dat'

# Types of data to get (full possible set in the comment below - copy to code necessary)
#typesOfData = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm', 'A+B', 'A-B']
typesOfData = ['chA']

# List of frequencies to build intensity changes vs. time and save to TXT file:
#freqList = [10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,75.0]
freqList = [9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
#freqList = [4.0,5.0,6.0,7.0,8.0,8.05,8.1,8.15,8.5,9.0]

averOrMin = 0                    # Use average value (0) per data block or minimum value (1)
StartStopSwitch = 0              # Read the whole file (0) or specified time limits (1)
SpecFreqRange = 0                # Specify particular frequency range (1) or whole range (0)
VminMan = -120                   # Manual lower limit of immediate spectrum figure color range
VmaxMan = -10                    # Manual upper limit of immediate spectrum figure color range
VminNormMan = 0                  # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
VmaxNormMan = 7                 # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
RFImeanConst = 6                 # Constant of RFI mitigation (usually = 8)
customDPI = 300                  # Resolution of images of dynamic spectra
colormap = 'jet'                 # Colormap of images of dynamic spectra ('jet' or 'Greys')
ChannelSaveTXT = 0               # Save intensities at specified frequencies to TXT file
ChannelSavePNG = 0               # Save intensities at specified frequencies to PNG file
ListOrAllFreq = 0                # Take all frequencies of a list to save TXT and PNG? 1-All, 0-List
AmplitudeReIm = 20 * 10**(-12) # Colour range of Re and Im dynamic spectra
                                 # 10 * 10**(-12) is typical value enough for CasA for interferometer of 2 GURT subarrays

# Begin and end frequency of dynamic spectrum (MHz)
freqStart = 0.0
freqStop = 10.0

# Begin and end time of dynamic spectrum ('yyyy-mm-dd hh:mm:ss')
dateTimeStart = '2019-09-05 15:34:05'
dateTimeStop =  '2019-09-06 00:57:41'

# Begin and end frequency of TXT files to save (MHz)
freqStartTXT = 0.0
freqStopTXT = 33.0

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
import os
import struct
import sys
import numpy as np
import pylab
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta
from matplotlib import rc

# My functions
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR
from package_plot_formats.plot_formats import OneDynSpectraPlot, OneDynSpectraPlotPhD, TwoOrOneValuePlot,  OneValueWithTimePlot
from package_ra_data_processing.spectra_normalization import Normalization_dB
from package_cleaning.simple_channel_clean import simple_channel_clean

################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************
print ('\n\n\n\n\n\n\n\n   ****************************************************')
print ('   * DAT time data files processing  v.', Software_version,'   *      (c) YeS 2018')
print ('   **************************************************** \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)
print (' ')

# Directory of Timeline file to be analyzed:
timeLineFileName = common_path + filename[-31:-13] +'_Timeline.txt'

for j in range(len(typesOfData)):  # Main loop by types of data to analyze

    # Current name of DAT file to be analyzed dependent on data type:
    temp = list(filename)
    temp[-7:-4] = typesOfData[j]
    filename = "".join(temp)


    if (typesOfData[j] == 'A+B' or typesOfData[j] == 'A-B'):
        temp = list(filename)
        temp[-7:-4] = 'chA'
        filename01 = "".join(temp)
        temp[-7:-4] = 'chB'
        filename02 = "".join(temp)
        filename = filename01

    # Print the type of data to be analyzed
    print ('\n\n   Processing data type: ', typesOfData[j])
    print ('\n   Processing file: ', filename, ' \n')


    #*************************************************************
    #         WHAT TO PLOT AND CORRESPONDING PARAMETERS          *
    #*************************************************************

    YaxName = 'Intensity, dB'
    Label = 'Intensity'
    nameAdd = ''
    fileNameAdd = ''
    fileNameAddNorm = ''
    fileNameAddSpectr = ''
    Vmin = VminMan              # Switch once more to initial manual settings after changes in previous loop
    Vmax = VmaxMan
    VminNorm = VminNormMan
    VmaxNorm = VmaxNormMan

    if typesOfData[j] == 'chA':
        nameAdd = ' channel A'
        fileNameAdd = ''
        fileNameAddNorm = '001_'
        fileNameAddSpectr = '008_'

    if typesOfData[j] == 'chB':
        nameAdd = ' channel B'
        fileNameAdd = ''
        fileNameAddNorm = '001_'
        fileNameAddSpectr = '008_'

    if typesOfData[j] == 'C_m':
        nameAdd = ' correlation module'
        Vmin = -160
        VmaxNorm = 2 * VmaxNormMan
        fileNameAdd = ''
        fileNameAddNorm = '004_'
        fileNameAddSpectr = '011_'

    if typesOfData[j] == 'C_p':
        nameAdd = ' correlation phase'
        YaxName = 'Phase, rad'
        Label = 'Phase'
        Vmin = -3.5
        Vmax = 3.5
        fileNameAdd = '005_'
        fileNameAddSpectr = '012_'

    if typesOfData[j] == 'CRe':
        nameAdd = ' correlation RE part'
        YaxName = 'Amplitude'
        fileNameAdd = '006_'
        fileNameAddSpectr = '013_'

    if typesOfData[j] == 'CIm':
        nameAdd = ' correlation IM part'
        YaxName = 'Amplitude'
        fileNameAdd = '007_'
        fileNameAddSpectr = '014_'

    if typesOfData[j] == 'A+B':
        nameAdd = ' sum A + B'
        fileNameAddNorm = '003_'
        fileNameAddSpectr = '009_'

    if typesOfData[j] == 'A-B':
        nameAdd = ' difference |A - B|'
        Vmin = Vmin - 20
        Vmax = Vmax - 20
        fileNameAdd = ''
        fileNameAddNorm = '002_'
        fileNameAddSpectr = '010_'

    #*********************************************************************************


    # *** Creating a folder where all pictures and results will be stored (if it doen't exist) ***
    newpath = "DAT_Results"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # *** Opening DAT datafile ***

    file = open(filename, 'rb')

    # *** Data file header read ***
    df_filesize = (os.stat(filename).st_size)                       # Size of file
    df_filename = file.read(32).decode('utf-8').rstrip('\x00')      # Initial data file name
    file.close()

    if df_filename[-4:] == '.adr':

        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
                CLCfrq, df_creation_timeUTC, ReceiverMode, Mode, sumDifMode,
                NAvr, TimeRes, fmin, fmax, df, frequency, FFTsize, SLine,
                Width, BlockSize] = FileHeaderReaderADR(filename, 0, 1)

        FreqPointsNum = len(frequency)

    if df_filename[-4:] == '.jds':     # If data obrained from DSPZ receiver

        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
                CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
                df, frequency, FreqPointsNum, dataBlockSize] = FileHeaderReaderJDS(filename, 0, 1)

        sumDifMode = ''

    #************************************************************************************
    #                            R E A D I N G   D A T A                                *
    #************************************************************************************

    # *** Reading timeline file ***
    TLfile = open(timeLineFileName, 'r')
    timeline = []
    for line in TLfile:
        timeline.append(str(line))
    TLfile.close()


    if StartStopSwitch == 1:  # If we read only specified time limits of files

        # *** Converting text to ".datetime" format ***
        dt_timeline = []
        for i in range (len(timeline)):  # converting text to ".datetime" format

            # Check is the uS field is empty. If so it means it is equal to '000000'
            uSecond = timeline[i][20:26]
            if len(uSecond) < 2: uSecond = '000000'

            dt_timeline.append(datetime(int(timeline[i][0:4]), int(timeline[i][5:7]), int(timeline[i][8:10]), int(timeline[i][11:13]), int(timeline[i][14:16]), int(timeline[i][17:19]), int(uSecond)))

        dt_dateTimeStart = datetime(int(dateTimeStart[0:4]), int(dateTimeStart[5:7]), int(dateTimeStart[8:10]), int(dateTimeStart[11:13]), int(dateTimeStart[14:16]), int(dateTimeStart[17:19]), 0)
        dt_dateTimeStop = datetime(int(dateTimeStop[0:4]), int(dateTimeStop[5:7]), int(dateTimeStop[8:10]), int(dateTimeStop[11:13]), int(dateTimeStop[14:16]), int(dateTimeStop[17:19]), 0)

        # *** Showing the time limits of file and time limits of chosen part
        print ('\n\n                               Start                         End \n')
        print ('  File time limits:   ', dt_timeline[0],' ', dt_timeline[len(timeline)-1], '\n')
        print ('  Chosen time limits: ', dt_dateTimeStart, '        ', dt_dateTimeStop, '\n')

        # Verifying that chosen time limits are inside file and are correct
        if (dt_timeline[len(timeline)-1]>=dt_dateTimeStart>dt_timeline[0])and(dt_timeline[len(timeline)-1]>dt_dateTimeStop>=dt_timeline[0])and(dt_dateTimeStop>dt_dateTimeStart):
            print ('  Time is chosen correctly! \n\n')
        else:
            print ('  ERROR! Time is chosen out of file limits!!! \n\n')
            sys.exit('         Program stopped')

        # Finding the closest spectra to the chosen time limits
        A = []
        B = []
        for i in range (len(timeline)):
            dt_diff_start = dt_timeline[i] - dt_dateTimeStart
            dt_diff_stop  = dt_timeline[i] - dt_dateTimeStop
            A.append(abs(divmod(dt_diff_start.total_seconds(), 60)[0]*60 + divmod(dt_diff_start.total_seconds(), 60)[1]))
            B.append(abs(divmod(dt_diff_stop.total_seconds(), 60)[0]*60 + divmod(dt_diff_stop.total_seconds(), 60)[1]))

        istart = A.index(min(A))
        istop = B.index(min(B))
        print ('\n Start specter number is:          ', istart)
        print ('\n Stop specter number is:           ', istop)
        print ('\n Total number of spectra to read:  ', istop - istart)


    # *** Calculation of the dimensions of arrays to read ***

    nx = len(frequency)                  # the first dimension of the array
    if StartStopSwitch == 1:             # If we read only specified time limits of files
        ny = int(istop - istart)         # the second dimension of the array: number of spectra to read
    else:
        ny = int(((df_filesize-1024)/(nx*8))) # the second dimension of the array: file size - 1024 bytes
        istart = 0
        istop = len(timeline)

    print (' ')
    print (' Number of frequency channels:     ', nx, '\n')
    print (' Number of spectra:                ', ny, '\n')
    print (' Recomended spectra number for averaging is:  ', int(ny/1024))
    # averageConst = raw_input('\n Enter number of spectra to be averaged:       ')

    #if (len(averageConst) < 1 or int(averageConst) < 1):
    #    averageConst = 1
    #else:
    #    averageConst = int(averageConst)
    averageConst = int(ny/1024)
    if int(averageConst) < 1: averageConst = 1



    # *** Data reading and averaging ***

    print ('\n\n\n  *** Data reading and averaging *** \n\n')

    file1 = open(filename, 'rb')
    if (typesOfData[j] == 'A+B' or typesOfData[j] == 'A-B'): file2 = open(filename02, 'rb')

    file1.seek(1024+istart*8*nx, os.SEEK_SET)        # Jumping to 1024+number of spectra to skip byte from file beginning
    if (typesOfData[j] == 'A+B' or typesOfData[j] == 'A-B'): file2.seek(1024+istart*8*nx, os.SEEK_SET)        # Jumping to 1024+number of spectra to skip byte from file beginning

    array = np.empty((nx, 0), float)
    numOfBlocks = int(ny/averageConst)
    for block in range (numOfBlocks):

        data1 = np.fromfile(file1, dtype=np.float64, count = nx * averageConst)
        if (typesOfData[j] == 'A+B' or typesOfData[j] == 'A-B'): data2 = np.fromfile(file2, dtype=np.float64, count = nx * averageConst)

        if (typesOfData[j] == 'A+B' or typesOfData[j] == 'A-B'):
            if typesOfData[j] == 'A+B': data = data1 + data2
            if typesOfData[j] == 'A-B': data = data1 - data2
        else:
            data = data1

        del data1
        if (typesOfData[j] == 'A+B' or typesOfData[j] == 'A-B'): del data2

        data = np.reshape(data, [nx, averageConst], order='F')

        dataApp = np.empty((nx, 1), float)

        if (typesOfData[j] == 'chA' or typesOfData[j]== 'chB'  or typesOfData[j] == 'A+B'):
        # If analyzing intensity - average and log data
            if averOrMin == 0:
                with np.errstate(invalid='ignore'):
                    dataApp[:,0] = 10*np.log10(data.mean(axis=1)[:])
            elif averOrMin == 1:
                with np.errstate(invalid='ignore'):
                    dataApp[:,0] = 10*np.log10(np.amin(data, axis=1)[:])
            else:
                print('\n\n Error!!! Wrong value of parameters!')
            array = np.append(array, dataApp, axis=1)
            array[np.isnan(array)] = -120

        if (typesOfData[j] == 'A-B'):
        # If analyzing intensity - average and log absolute values of data
            with np.errstate(invalid='ignore'):
                dataApp[:,0] = 10*np.log10(np.abs(data.mean(axis=1)[:]))
            array = np.append(array, dataApp, axis=1)
            array[np.isnan(array)] = -120

        if (typesOfData[j] == 'C_p'  or typesOfData[j] == 'CRe' or typesOfData[j] == 'CIm'): # If analyzing phase/Re/Im - no logarythming needed
        # If analyzing phase of Re/Im we do not log data, only averaging
            dataApp[:,0] = (data.mean(axis=1)[:])
            array = np.append(array, dataApp, axis=1)
            array[np.isnan(array)] = 0

        if typesOfData[j] == 'C_m':
            dataApp[:,0] = (data.mean(axis=1)[:])
            array = np.append(array, dataApp, axis=1)
            #array[np.isinf(array)] = -120

        del dataApp, data

    file1.close()
    if (typesOfData[j] == 'A+B' or typesOfData[j] == 'A-B'): file2.close()


    print ('\n Array shape is now             ', array.shape)

    # *** Cutting timeline to time limits ***
    dateTimeNew = timeline[istart:istop:averageConst]
    del dateTimeNew[numOfBlocks:]
    print ('\n TimeLine length is now:        ', len(dateTimeNew))


#*******************************************************************************
#                                F I G U R E S                                 *
#*******************************************************************************
    print ('\n\n\n  *** Building images *** \n\n')

    # Exact string timescales to show on plots
    TimeScaleFig = np.empty_like(dateTimeNew)
    for i in range (len(dateTimeNew)):
        TimeScaleFig[i] = str(dateTimeNew[i][0:11]+'\n'+dateTimeNew[i][11:23])

    # Limits of figures for common case or for Re/Im parts to show the interferometric picture
    if typesOfData[j]== 'CRe' or typesOfData[j] == 'CIm':
        Vmin = 0 - AmplitudeReIm
        Vmax = 0 + AmplitudeReIm


    # *** Immediate spectrum ***

    Suptitle = ('Immediate spectrum ' + str(df_filename[0:18]) + ' ' + nameAdd)
    Title = ('Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+str(round(df/1000,3))+' kHz '+sumDifMode+
    'Processing: Averaging '+str(averageConst)+' spectra ('+str(round(averageConst*TimeRes,3))+' sec.)')

    TwoOrOneValuePlot(1, frequency, array[:,[1]], [],
                'Spectrum', ' ', frequency[0], frequency[FreqPointsNum-1],
                Vmin, Vmax, Vmin, Vmax, 'Frequency, MHz', YaxName, ' ',
                Suptitle, Title,
                'DAT_Results/' + fileNameAddSpectr + df_filename[0:14]+'_'+typesOfData[j]+' Immediate Spectrum.png',
                currentDate, currentTime, Software_version)


    # *** Decide to use only list of frequencies or all frequencies in range
    if ListOrAllFreq == 0:
        freqList = np.array(freqList)
    if ListOrAllFreq == 1:
        freqList = np.array(frequency)


    # *** Finding frequency most close to specified by user ***
    for fc in range(len(freqList)):
        if (freqList[fc] > freqStartTXT) and (freqList[fc] < freqStopTXT):
            newFreq = np.array(frequency)
            newFreq = np.absolute(newFreq - freqList[fc])
            index = np.argmin(newFreq)+1
            tempArr1 = np.arange(0,len(dateTimeNew),1)

            if ChannelSavePNG == 1 or typesOfData[j]== 'CRe' or typesOfData[j] == 'CIm':
                if typesOfData[j]== 'CRe' or typesOfData[j] == 'CIm':
                    Vmin = 0 - AmplitudeReIm
                    Vmax = 0 + AmplitudeReIm



                # *** Plotting intensity changes at particular frequency ***
                timeline = []
                for i in range(len(dateTimeNew)):
                    timeline.append(str(dateTimeNew[i][0:11] + '\n' + dateTimeNew[i][11:23]))

                Suptitle = 'Intensity variation '+str(df_filename[0:18])+' '+nameAdd
                Title = ('Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+
                            str(round(df/1000,3))+' kHz, Frequency = '+str(round(frequency[index],3))+
                            ' MHz '+sumDifMode+' Processing: Averaging '+str(averageConst)+
                            ' spectra ('+str(round(averageConst*TimeRes,3))+' sec.)')

                FileName = ('DAT_Results/'+df_filename[0:14]+'_'+typesOfData[j]+
                            ' Intensity variation at '+str(round(frequency[index],3))+'.png')

                OneValueWithTimePlot(timeline, array[[index],:].transpose(), Label,
                                        0, len(dateTimeNew), Vmin, Vmax, 0, 0,
                                        'UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', YaxName,
                                        Suptitle, Title, FileName,
                                        currentDate, currentTime, Software_version)


            # *** Saving value changes at particular frequency to TXT file ***
            if ChannelSaveTXT == 1:
                SingleChannelData = open('DAT_Results/'+df_filename[0:14]+'_'+filename[-7:-4:]+' Intensity variation at '+str(round(frequency[index],3))+' MHz.txt', "w")
                for i in range(len(dateTimeNew)):
                    SingleChannelData.write(str(dateTimeNew[i]).rstrip()+'   '+str(array.transpose()[i, index])+' \n' )
                SingleChannelData.close()


    # *** Cutting the array inside frequency range specified by user ***
    if SpecFreqRange == 1 and (frequency[0]<=freqStart<=frequency[FreqPointsNum-1]) and (frequency[0]<=freqStop<=frequency[FreqPointsNum-1]) and (freqStart<freqStop):
        print ('\n You have chosen the frequency range', freqStart, '-', freqStop, 'MHz')
        A = []
        B = []
        for i in range (len(frequency)):
            A.append(abs(frequency[i] - freqStart))
            B.append(abs(frequency[i] - freqStop))
        ifmin = A.index(min(A))
        ifmax = B.index(min(B))
        array = array[ifmin:ifmax, :]
        print ('\n New data array shape is: ', array.shape)
        freqLine = frequency[ifmin:ifmax]
    else:
        freqLine = frequency


    # Limits of figures for common case or for Re/Im parts to show the interferometric picture
    Vmin = np.min(array)
    Vmax = np.max(array)
    if typesOfData[j]== 'CRe' or typesOfData[j] == 'CIm':
        Vmin = 0 - AmplitudeReIm
        Vmax = 0 + AmplitudeReIm


    # *** Dynamic spectrum of initial signal***

    Suptitle = ('Dynamic spectrum starting from file '+str(df_filename[0:18])+
                ' '+nameAdd+'\n Initial parameters: dt = '+str(round(TimeRes,3))+
                ' Sec, df = '+str(round(df/1000,3))+' kHz, '+sumDifMode+
                ' Processing: Averaging '+str(averageConst)+' spectra ('+str(round(averageConst*TimeRes,3))+
                ' sec.)\n'+' Receiver: '+str(df_system_name)+
                ', Place: '+str(df_obs_place) +', Description: '+str(df_description))
    fig_file_name = ('DAT_Results/' +fileNameAdd+ df_filename[0:14]+'_'+typesOfData[j]+' Dynamic spectrum.png')

    OneDynSpectraPlot(array, Vmin, Vmax, Suptitle,
                    'Intensity, dB', len(dateTimeNew),
                    TimeScaleFig, freqLine,
                    len(freqLine), colormap, 'UTC Date and time, YYYY-MM-DD HH:MM:SS.msec', fig_file_name,
                    currentDate, currentTime, Software_version, customDPI)


    if (typesOfData[j] != 'C_p' and typesOfData[j] != 'CRe' and typesOfData[j] != 'CIm'):

        # *** Normalization and cleaning of dynamic spectra ***
        Normalization_dB(array.transpose(), len(freqLine), len(dateTimeNew))
        simple_channel_clean(array.transpose(), RFImeanConst)


        # *** Dynamic spectra of cleaned and normalized signal ***

        Suptitle = ('Dynamic spectrum cleaned and normalized starting from file '+str(df_filename[0:18])+
                    ' '+nameAdd+'\n Initial parameters: dt = '+str(round(TimeRes,3))+
                    ' Sec, df = '+str(round(df/1000,3))+' kHz, '+sumDifMode+
                    ' Processing: Averaging '+str(averageConst)+' spectra ('+str(round(averageConst*TimeRes,3))+
                    ' sec.)\n'+' Receiver: '+str(df_system_name)+
                    ', Place: '+str(df_obs_place) +', Description: '+str(df_description))
        fig_file_name = ('DAT_Results/' +fileNameAddNorm+ df_filename[0:14]+'_'+typesOfData[j]+
                        ' Dynamic spectrum cleanned and normalized'+'.png')
        '''
        OneDynSpectraPlot(array, VminNorm, VmaxNorm, Suptitle,
                        'Intensity, dB', len(dateTimeNew),
                        TimeScaleFig, freqLine,
                        len(freqLine), colormap, 'UTC Date and time, YYYY-MM-DD HH:MM:SS.msec', fig_file_name,
                        currentDate, currentTime, Software_version, customDPI)
        '''
        # Figure in PhD thesis format
        fig_file_name = ('DAT_Results/' +fileNameAddNorm+ df_filename[0:14]+'_'+typesOfData[j]+
                        ' Dynamic spectrum cleanned and normalized_PhD'+'.png')
        OneDynSpectraPlotPhD(array, VminNorm, VmaxNorm, Suptitle,
                        'Інтенсивність, дБ', len(dateTimeNew),
                        TimeScaleFig, freqLine,
                        len(freqLine), colormap, 'Дата та час UTC', fig_file_name,
                        currentDate, currentTime, Software_version, customDPI)

        '''
        # *** TEMPLATE FOR JOURNLS Dynamic spectra of cleaned and normalized signal ***
        plt.figure(2, figsize=(16.0, 7.0))
        ImA = plt.imshow(np.flipud(array), aspect='auto', extent=[0,len(dateTimeNew),freqLine[0],freqLine[len(freqLine)-1]], vmin=VminNorm, vmax=VmaxNorm, cmap=colormap) #
        plt.ylabel('Frequency, MHz', fontsize=12, fontweight='bold')
        #plt.suptitle('Dynamic spectrum cleaned and normalized starting from file '+str(df_filename[0:18])+' '+nameAdd+
        #            '\n Initial parameters: dt = '+str(round(TimeRes,3))+
        #            ' Sec, df = '+str(round(df/1000,3))+' kHz, '+sumDifMode+
        #            ' Processing: Averaging '+str(averageConst)+' spectra ('+str(round(averageConst*TimeRes,3))+' sec.)\n'+
        #            ' Receiver: '+str(df_system_name)+
        #            ', Place: '+str(df_obs_place) +
        #            ', Description: '+str(df_description),
        #            fontsize=10, fontweight='bold', x = 0.46, y = 0.96)
        plt.yticks(fontsize=12, fontweight='bold')
        rc('font', weight='bold')
        cbar = plt.colorbar(ImA, pad=0.005)
        cbar.set_label('Intensity, dB', fontsize=12, fontweight='bold')
        cbar.ax.tick_params(labelsize=12)
        ax1 = plt.figure(2).add_subplot(1,1,1)
        a = ax1.get_xticks().tolist()
        for i in range(len(a)-1):   #a-1
            k = int(a[i])
            #a[i] = str(dateTimeNew[k][0:11]+'\n'+dateTimeNew[k][11:23])
            a[i] = str(dateTimeNew[k][11:19])
        ax1.set_xticklabels(a)
        plt.xticks(fontsize=12, fontweight='bold')
        plt.xlabel('UTC time, HH:MM:SS', fontsize=12, fontweight='bold')
        #plt.text(0.72, 0.04,'Processed '+currentDate+ ' at '+currentTime, fontsize=6, transform=plt.gcf().transFigure)
        pylab.savefig('DAT_Results/' + fileNameAddNorm + df_filename[0:14]+'_'+typesOfData[j]+' Dynamic spectrum cleanned and normalized'+'.png', bbox_inches='tight', dpi = customDPI)
        #pylab.savefig('DAT_Results/' +fileNameAddNorm+ df_filename[0:14]+'_'+typesOfData[j]+ ' Dynamic spectrum cleanned and normalized'+'.eps', bbox_inches='tight', dpi = customDPI)
                                                                             #filename[-7:-4:]
        plt.close('all')
        '''


endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program DAT_reader has finished! *** \n\n\n')
