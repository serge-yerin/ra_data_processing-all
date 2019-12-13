# Python3
Software_version = '2019.08.03'


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
from os import path
from datetime import datetime, timedelta
from matplotlib import rc
import warnings
warnings.filterwarnings("ignore")

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# My functions
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR
from package_plot_formats.plot_formats import OneDynSpectraPlot, TwoOrOneValuePlot,  OneValueWithTimePlot
from package_ra_data_processing.spectra_normalization import Normalization_dB
from package_cleaning.simple_channel_clean import simple_channel_clean
################################################################################
#*******************************************************************************
#                         M A I N    F U N C T I O N                           *
#*******************************************************************************

def DAT_file_reader(common_path, DAT_file_name, typesOfData, DAT_result_path, averOrMin, StartStopSwitch, SpecFreqRange, VminMan, VmaxMan,
                    VminNormMan, VmaxNormMan, RFImeanConst, customDPI, colormap,
                    ChannelSaveTXT, ChannelSavePNG, ListOrAllFreq, AmplitudeReIm,
                    freqStart, freqStop, dateTimeStart, dateTimeStop, freqStartTXT,
                    freqStopTXT, freqList, print_or_not):

    startTime = time.time()
    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")

    # Files to be analyzed:
    filename = common_path + DAT_file_name + '_Data_chA.dat'
    timeLineFileName = common_path + DAT_file_name +'_Timeline.txt'

    for j in range(len(typesOfData)):  # Main loop by types of data to analyze

        # Current name of DAT file to be analyzed dependent on data type:
        temp = list(filename)
        temp[-7:-4] = typesOfData[j]
        filename = "".join(temp)
        temp = list( DAT_file_name + '_Data_chA.dat')
        temp[-7:-4] = typesOfData[j]
        only_file_name = "".join(temp)


        if (typesOfData[j] == 'A+B' or typesOfData[j] == 'A-B'):
            temp = list(filename)
            temp[-7:-4] = 'chA'
            filename01 = "".join(temp)
            temp[-7:-4] = 'chB'
            filename02 = "".join(temp)
            filename = filename01

        # Print the type of data to be analyzed
        if print_or_not == 1: print ('\n\n   Processing data type: ', typesOfData[j], '\n')
        currentTime = time.strftime("%H:%M:%S")
        print ('   Processing file: ', only_file_name, '   started at: ', currentTime)
        if print_or_not == 1: print('\n')


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
        if averOrMin == 0: reducing_type = 'Averaging '
        if averOrMin == 1: reducing_type = 'Least of '

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
        newpath = common_path + 'DAT_Results_' + DAT_result_path
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
                    Width, BlockSize] = FileHeaderReaderADR(filename, 0, 0)

            FreqPointsNum = len(frequency)

        if df_filename[-4:] == '.jds':     # If data obrained from DSPZ receiver

            [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
                    CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
                    df, frequency, FreqPointsNum, dataBlockSize] = FileHeaderReaderJDS(filename, 0, 0)

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
            if print_or_not == 1: print ('\n\n                               Start                         End \n')
            if print_or_not == 1: print ('  File time limits:   ', dt_timeline[0],' ', dt_timeline[len(timeline)-1], '\n')
            if print_or_not == 1: print ('  Chosen time limits: ', dt_dateTimeStart, '        ', dt_dateTimeStop, '\n')

            # Verifying that chosen time limits are inside file and are correct
            if (dt_timeline[len(timeline)-1]>=dt_dateTimeStart>dt_timeline[0])and(dt_timeline[len(timeline)-1]>dt_dateTimeStop>=dt_timeline[0])and(dt_dateTimeStop>dt_dateTimeStart):
                if print_or_not == 1:  print ('  Time is chosen correctly! \n\n')
            else:
                print ('  ERROR! Time is chosen out of file limits!!! \n\n')
                sys.exit('           Program stopped')

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
            if print_or_not == 1: print ('\n Start specter number is:          ', istart)
            if print_or_not == 1: print ('\n Stop specter number is:           ', istop)
            if print_or_not == 1: print ('\n Total number of spectra to read:  ', istop - istart)


        # *** Calculation of the dimensions of arrays to read ***
        nx = len(frequency)                  # the first dimension of the array
        if StartStopSwitch == 1:             # If we read only specified time limits of files
            ny = int(istop - istart)         # the second dimension of the array: number of spectra to read
        else:
            ny = int(((df_filesize-1024)/(nx*8))) # the second dimension of the array: file size - 1024 bytes
            istart = 0
            istop = len(timeline)

        if print_or_not == 1: print (' ')
        if print_or_not == 1: print (' Number of frequency channels:     ', nx, '\n')
        if print_or_not == 1: print (' Number of spectra:                ', ny, '\n')
        if print_or_not == 1: print (' Recomended spectra number for averaging is:  ', int(ny/1024))
        # averageConst = raw_input('\n Enter number of spectra to be averaged:       ')

        #if (len(averageConst) < 1 or int(averageConst) < 1):
        #    averageConst = 1
        #else:
        #    averageConst = int(averageConst)
        averageConst = int(ny/1024)
        if int(averageConst) < 1: averageConst = 1


        # *** Data reading and averaging ***
        if print_or_not == 1: print ('\n\n\n  *** Data reading and averaging *** \n\n')

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


        if print_or_not == 1: print ('\n Array shape is now             ', array.shape)

        # *** Cutting timeline to time limits ***
        dateTimeNew = timeline[istart:istop:averageConst]
        del dateTimeNew[numOfBlocks:]
        if print_or_not == 1: print ('\n TimeLine length is now:        ', len(dateTimeNew))


    #*******************************************************************************
    #                                F I G U R E S                                 *
    #*******************************************************************************
        if print_or_not == 1: print ('\n\n\n  *** Building images *** \n\n')

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
        'Processing: ' + reducing_type + str(averageConst)+' spectra ('+str(round(averageConst*TimeRes,3))+' sec.)')

        TwoOrOneValuePlot(1, frequency, array[:,[1]], [],
                    'Spectrum', ' ', frequency[0], frequency[FreqPointsNum-1],
                    Vmin, Vmax, Vmin, Vmax, 'Frequency, MHz', YaxName, ' ',
                    Suptitle, Title,
                    newpath + '/' + fileNameAddSpectr + df_filename[0:14]+'_'+typesOfData[j]+' Immediate Spectrum.png',
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
                                ' MHz '+sumDifMode+' Processing: ' + reducing_type + str(averageConst)+
                                ' spectra ('+str(round(averageConst*TimeRes,3))+' sec.)')

                    FileName = (newpath + '/' + df_filename[0:14] + '_' + typesOfData[j]+ df_filename[-4:]+
                                ' variation at '+str(round(frequency[index],3))+' MHz.png')

                    OneValueWithTimePlot(timeline, array[[index],:].transpose(), Label,
                                            0, len(dateTimeNew), Vmin, Vmax, 0, 0,
                                            'UTC Date and time, YYYY-MM-DD HH:MM:SS.ms', YaxName,
                                            Suptitle, Title, FileName,
                                            currentDate, currentTime, Software_version)


                # *** Saving value changes at particular frequency to TXT file ***
                if ChannelSaveTXT == 1:
                    SingleChannelData = open(newpath + '/' + df_filename[0:14]+'_'+filename[-7:-4:]+ df_filename[-4:]+' variation at '+str(round(frequency[index],3))+' MHz.txt', "w")
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
                    ' Processing: ' + reducing_type + str(averageConst)+' spectra ('+str(round(averageConst*TimeRes,3))+
                    ' sec.)\n'+' Receiver: '+str(df_system_name)+
                    ', Place: '+str(df_obs_place) +', Description: '+str(df_description))
        fig_file_name = (newpath + '/' + fileNameAdd + df_filename[0:14]+'_'+typesOfData[j]+' Dynamic spectrum.png')

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
                        ' Processing: ' + reducing_type + str(averageConst)+' spectra ('+str(round(averageConst*TimeRes,3))+
                        ' sec.)\n'+' Receiver: '+str(df_system_name)+
                        ', Place: '+str(df_obs_place) +', Description: '+str(df_description))
            fig_file_name = (newpath + '/' + fileNameAddNorm + df_filename[0:14] + '_'+typesOfData[j]+
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
            #            ' Processing: ' + reducing_type + str(averageConst)+' spectra ('+str(round(averageConst*TimeRes,3))+' sec.)\n'+
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

    ok = 1
    return ok


#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************

if __name__ == '__main__':

    common_path = 'DATA/'
    result_path = ''

    ok = DAT_file_reader(common_path, DAT_file_name, typesOfData, averOrMin, StartStopSwitch, SpecFreqRange, VminMan, VmaxMan,
                        VminNormMan, VmaxNormMan, RFImeanConst, customDPI, colormap,
                        ChannelSaveTXT, ChannelSavePNG, ListOrAllFreq, AmplitudeReIm,
                        freqStart, freqStop, dateTimeStart,dateTimeStop, freqStartTXT,
                        freqStopTXT, freqList)
