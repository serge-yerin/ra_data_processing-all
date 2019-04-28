# Python3
Software_version = '2018.02.27'
# Program intended to read and show data from DAT files

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************
# Path to data files
common_path = 'DATA/'          # 'e:/PYTHON/ra_data_processing-all/'

# Directory of DAT file to be analyzed:
filename = common_path + 'A170712_160219.adr_Data_chA.dat'

# Types of data to get
#typesOfData = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm', 'A+B', 'A-B'] # !-!
typesOfData = ['chA', 'chB']

# List of frequencies to build intensity changes vs. time and save to TXT file:
#freqList = [10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,75.0]
freqList = [9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]

StartStopSwitch = 0            # Read the whole file (0) or specified time limits (1)
SpecFreqRange = 0              # Specify particular frequency range (1) or whole range (0)
VminMan = -120                 # Manual lower limit of immediate spectrum figure color range
VmaxMan = -10                  # Manual upper limit of immediate spectrum figure color range
VminNormMan = 0                # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
VmaxNormMan = 10               # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
RFImeanConst = 6               # Constant of RFI mitigation (usually = 8)
customDPI = 300                # Resolution of images of dynamic spectra
colormap = 'jet'               # Colormap of images of dynamic spectra ('jet' or 'Greys')
ColorBarSwitch = 1             # Add colorbar to dynamic spectrum picture? (1 = yes, 0 = no)
ChannelSaveTXT = 0             # Save intensities at specified frequencies to TXT file
ChannelSavePNG = 0             # Save intensities at specified frequencies to PNG file
ListOrAllFreq = 0              # Take all frequencies of a list to save TXT and PNG? 1-All, 0-List
AmplitudeReIm = 2000 * 10**(-12) # Colour range of Re and Im dynamic spectra
                               # 10 * 10**(-12) is typical value enough for CasA for interferometer of 2 GURT subarrays

# Begin and end frequency of dynamic spectrum (MHz)
freqStart = 8.0
freqStop = 33.0

# Begin and end time of dynamic spectrum ('yyyy-mm-dd hh:mm:ss')
dateTimeStart = '2019-03-20 11:00:00'
dateTimeStop =  '2019-03-20 12:30:00'

# Begin and end frequency of TXT files to save (MHz)
freqStartTXT = 8.0
freqStopTXT = 33.0



#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************
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
from f_file_header_JDS import FileHeaderReaderDSP
from f_file_header_ADR import FileHeaderReaderADR
from f_plot_formats import OneImmedSpecterPlot, OneDynSpectraPlot
from f_spectra_normalization import Normalization_dB
from f_ra_data_clean import simple_channel_clean



#*************************************************************
#                       MAIN PROGRAM                         *
#*************************************************************
for i in range(8): print (' ')
print ('   ****************************************************')
print ('   * DAT time data files processing  v.', Software_version,'   *      (c) YeS 2018')
print ('   ****************************************************')
for i in range(3): print (' ')


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
    for i in range(2): print (' ')
    print ('   Processing data type: ', typesOfData[j])
    print ('\n   Processing file: ', filename)
    for i in range(1): print (' ')


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

    # reading FHEADER
    df_filesize = (os.stat(filename).st_size)            # Size of file
    df_filename = file.read(32).decode('utf-8').rstrip('\x00')           # Initial data file name

    if df_filename[-4:] == '.adr':

        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
                CLCfrq, df_creation_timeUTC, ReceiverMode, Mode, sumDifMode,
                NAvr, TimeRes, fmin, fmax, df, frequency, FFTsize, SLine,
                Width, BlockSize] = FileHeaderReaderADR(filename, 0)

        FreqPointsNum = len(frequency)

    if df_filename[-4:] == '.jds':     # If data obrained from DSPZ receiver

        # *** Data file header read ***

        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
                CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
                df, frequency, FreqPointsNum, dataBlockSize] = FileHeaderReaderDSP(filename, 0)

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
        print ('\n\n')
        print ('                               Start                         End \n')
        print ('  File time limits:   ', dt_timeline[0],' ', dt_timeline[len(timeline)-1], '\n')
        print ('  Chosen time limits: ', dt_dateTimeStart, '        ', dt_dateTimeStop)
        print ('\n')

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

    for i in range (3) : print (' ')
    print ('  *** Data reading and averaging ***')
    for i in range (2) : print (' ')



    # *** Data reading and averaging ***

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
            with np.errstate(invalid='ignore'):
                dataApp[:,0] = 10*np.log10(data.mean(axis=1)[:])
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


    #************************************************************************************
    #                                  F I G U R E S                                    *
    #************************************************************************************
    for i in range (3) : print (' ')
    print ('  *** Building images ***')
    for i in range (2) : print (' ')

    # Exact string timescales to show on plots
    TimeScaleFig = np.empty_like(dateTimeNew)
    for i in range (len(dateTimeNew)):
        TimeScaleFig[i] = str(dateTimeNew[i][0:11]+'\n'+dateTimeNew[i][11:23])

    # Limits of figures for common case or for Re/Im parts to show the interferometric picture
    if typesOfData[j]== 'CRe' or typesOfData[j] == 'CIm':
        Vmin = 0 - AmplitudeReIm
        Vmax = 0 + AmplitudeReIm


    # *** Immediate spectrum ***
    OneImmedSpecterPlot(frequency, array[:,[1]], 'Spectrum',
                        frequency[0], frequency[FreqPointsNum-1], Vmin, Vmax,
                        'Frequency, MHz', YaxName,
                        'Immediate spectrum '+str(df_filename[0:18])+' '+nameAdd,
                        'Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+str(round(df/1000,3))+' kHz '+sumDifMode+
                        '\n Processing: Averaging '+str(averageConst)+' spectra ('+str(round(averageConst*TimeRes,3))+' sec.)',
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
                plt.figure(0)
                plt.plot(np.arange(0,len(dateTimeNew),1), array[[index],:].transpose(), color = 'b', linestyle = '-', linewidth = '1.00', label = Label)
                plt.axis([0, len(dateTimeNew), Vmin, Vmax])
                plt.xlabel('Date & UTC time, yyyy-mm-dd hh:mm:ss.msec')
                plt.ylabel(YaxName)
                plt.suptitle('Intensity variation '+str(df_filename[0:18])+' '+nameAdd, fontsize=10, fontweight='bold')
                plt.title('Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+str(round(df/1000,3))+' kHz, Frequency = '+str(round(frequency[index],3))+' MHz '+sumDifMode+'\n Processing: Averaging '+str(averageConst)+' spectra ('+str(round(averageConst*TimeRes,3))+' sec.)', fontsize=8)
                plt.grid(b = True, which = 'both', color = '0.00',linestyle = '--')
                plt.legend(loc = 'upper right', fontsize = 10)
                axes = plt.figure(0).add_subplot(1,1,1)
                a = axes.get_xticks().tolist()
                for i in range(len(a)-1):
                    k = int(a[i])
                    a[i] = str(dateTimeNew[k][0:11]+'\n'+dateTimeNew[k][11:23])
                axes.set_xticklabels(a)
                plt.xticks(fontsize=6, fontweight='bold')
                plt.yticks(fontsize=6, fontweight='bold')
                pylab.savefig('DAT_Results/'+df_filename[0:14]+'_'+typesOfData[j]+' Intensity variation at '+str(round(frequency[index],3))+'.png', bbox_inches='tight', dpi = 160)
                # plt.show()                                      #filename[-7:-4:]
                plt.close('all')



            # *** Saving value changes at particular frequency to TXT file ***
            if ChannelSaveTXT == 1:
                SingleChannelData = open('DAT_Results/'+df_filename[0:14]+'_'+filename[-7:-4:]+' Intensity variation at '+str(round(frequency[index],3))+'.txt', "w")
                for i in range(len(dateTimeNew)):
                    SingleChannelData.write(str(dateTimeNew[i]).rstrip()+'   '+str(array.transpose()[i, index])+' \n' )
                SingleChannelData.close()


    # *** Cutting the array inside frequency range specified by user ***
    if SpecFreqRange == 1 and (frequency[0]<freqStart<frequency[FreqPointsNum-1]) and (frequency[0]<freqStop<frequency[FreqPointsNum-1]) and (freqStart<freqStop):
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

        OneDynSpectraPlot(array, VminNorm, VmaxNorm, Suptitle,
                        'Intensity, dB', len(dateTimeNew),
                        TimeScaleFig, freqLine,
                        len(freqLine), colormap, 'UTC Date and time, YYYY-MM-DD HH:MM:SS.msec', fig_file_name,
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
        if (ColorBarSwitch == 1):
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

endTime = time.time()    # Time of calculations


for i in range (0,2) : print (' ')
print ('   The program execution lasted for ', round((endTime - startTime),3), 'seconds')
for i in range (0,2) : print (' ')
print ('                 *** Program DAT_reader has finished! ***')
for i in range (0,3) : print (' ')
