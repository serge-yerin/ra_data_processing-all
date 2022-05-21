# Python3
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

# My functions
from package_plot_formats.plot_formats import TwoDynSpectraPlot, TwoOrOneValuePlot
from package_ra_data_processing.f_spectra_normalization import normalization_db
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_ra_data_files_formats.FPGA_to_PC_array import FPGAtoPCarrayJDS
from package_cleaning.simple_channel_clean import simple_channel_clean

################################################################################
#*******************************************************************************
#                        M A I N    F U N C T I O N                            *
#*******************************************************************************

def JDS_file_reader(fileList, result_path, MaxNsp, spSkip, RFImeanConst,
                Vmin, Vmax, VminNorm, VmaxNorm, VminCorrMag, VmaxCorrMag,
                colormap, customDPI, CorrelationProcess, longFileSaveAch,
                longFileSaveBch, longFileSaveCRI, longFileSaveCMP,
                DynSpecSaveInitial, DynSpecSaveCleaned, CorrSpecSaveInitial,
                CorrSpecSaveCleaned, SpecterFileSaveSwitch, ImmediateSpNo):
    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")

    # *** Creating a folder where all pictures and results will be stored (if it doesn't exist) ***
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    if not os.path.exists(result_path + '/Service'):
        os.makedirs(result_path + '/Service')
    if DynSpecSaveInitial == 1:
        if not os.path.exists(result_path + '/Initial_spectra'):
            os.makedirs(result_path + '/Initial_spectra')
    if (DynSpecSaveCleaned == 1 and CorrelationProcess == 1):
        if not os.path.exists(result_path + '/Correlation_spectra'):
            os.makedirs(result_path + '/Correlation_spectra')



    # Main loop
    for fileNo in range (len(fileList)):   # loop by files
        print ('\n\n  *  File ',  str(fileNo+1), ' of', str(len(fileList)))
        print ('  *  File path: ', str(fileList[fileNo]))

    #*********************************************************************************

        # *** Opening datafile ***
        fname = ''
        if len(fname) < 1 : fname = fileList[fileNo]

        # *** Data file header read ***
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
            CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
            df, frequency, FreqPointsNum, dataBlockSize] = FileHeaderReaderJDS(fname, 0, 0)

        # Initial time line settings
        TimeScaleStartDate = datetime(int(df_creation_timeUTC[0:4]), int(df_creation_timeUTC[5:7]), int(df_creation_timeUTC[8:10]), 0, 0, 0, 0)

        timeLineMS = np.zeros(int(SpInFile)) # List of ms values from ends of spectra


        # *** Creating a name for long timeline TXT file ***
        if fileNo == 0 and (longFileSaveAch == 1 or longFileSaveBch == 1 or longFileSaveCRI == 1 or longFileSaveCMP == 1):
            TLfile_name = df_filename + '_Timeline.txt'
            TLfile = open(TLfile_name, 'wb')  # Open and close to delete the file with the same name
            TLfile.close()

        with open(fname, 'rb') as file:

            # *** If it is the first file - write the header to long data file
            if((longFileSaveAch == 1 or longFileSaveBch == 1 or longFileSaveCRI == 1 or longFileSaveCMP == 1) and fileNo == 0):
                file.seek(0)
                file_header = file.read(1024)

                DAT_file_name = df_filename
                DAT_file_list = []

                # *** Creating a binary file with data for long data storage ***
                if((Mode == 1 or Mode == 2) and longFileSaveAch == 1):
                    Data_A_name = df_filename+'_Data_chA.dat'
                    Data_AFile = open(Data_A_name, 'wb')
                    Data_AFile.write(file_header)
                    Data_AFile.close()
                    DAT_file_list.append('chA')
                if(longFileSaveBch == 1 and (Mode == 1 or Mode == 2)):
                    Data_B_name = df_filename+'_Data_chB.dat'
                    Data_BFile = open(Data_B_name, 'wb')
                    Data_BFile.write(file_header)
                    Data_BFile.close()
                    DAT_file_list.append('chB')
                if(longFileSaveCRI == 1 and CorrelationProcess == 1 and Mode == 2):
                    Data_CRe_name = df_filename+'_Data_CRe.dat'
                    Data_CReFile = open(Data_CRe_name, 'wb')
                    Data_CReFile.write(file_header)
                    Data_CReFile.close()
                    DAT_file_list.append('CRe')
                    Data_CIm_name = df_filename+'_Data_CIm.dat'
                    Data_CImFile = open(Data_CIm_name, 'wb')
                    Data_CImFile.write(file_header)
                    Data_CImFile.close()
                    DAT_file_list.append('CIm')
                if(longFileSaveCMP == 1 and CorrelationProcess == 1 and Mode == 2):
                    Data_Cm_name = df_filename+'_Data_C_m.dat'
                    Data_CmFile = open(Data_Cm_name, 'wb')
                    Data_CmFile.write(file_header)
                    Data_CmFile.close()
                    DAT_file_list.append('C_m')
                    Data_Cp_name = df_filename+'_Data_C_p.dat'
                    Data_CpFile = open(Data_Cp_name, 'wb')
                    Data_CpFile.write(file_header)
                    Data_CpFile.close()
                    DAT_file_list.append('C_p')

                del file_header


    #*******************************************************************************
    #                         R E A D I N G   D A T A                              *
    #*******************************************************************************

            file.seek(1024)  # Jumping to 1024 byte from file beginning
            if Mode == 0:
                print('\n\n  Data in waveform mode, use appropriate program!!! \n\n\n')

            if Mode > 0 and Mode < 3:           # Spectra modes
                figID = -1
                figMAX = int(math.ceil((SpInFile - spSkip)/MaxNsp))
                if figMAX < 1: figMAX = 1
                for fig in range (figMAX):
                    Time1 = time.time()               # Timing
                    figID = figID + 1
                    currentTime = time.strftime("%H:%M:%S")
                    print (' File # ', str(fileNo+1), ' of ', str(len(fileList)), ', figure # ', figID+1, ' of ', figMAX, '   started at: ', currentTime)
                    if (SpInFile - spSkip - MaxNsp * figID) < MaxNsp:
                        Nsp = int(SpInFile - spSkip - MaxNsp * figID)
                    else:
                        Nsp = MaxNsp


                    # *** Preparing empty matrices ***
                    if Mode == 1 or Mode == 2:
                        Data_ChA = np.zeros((Nsp, FreqPointsNum))

                    if Mode == 1 or Mode == 2:
                        Data_ChB = np.zeros((Nsp, FreqPointsNum))

                    if Mode == 2:
                        Data_CRe = np.zeros((Nsp, FreqPointsNum))
                        Data_CIm = np.zeros((Nsp, FreqPointsNum))
                        CorrModule = np.zeros((Nsp, FreqPointsNum))
                        CorrPhase = np.zeros((Nsp, FreqPointsNum))

                    # *** Reading and reshaping all data for figure ***
                    if Mode == 1:
                        raw = np.fromfile(file, dtype='u4', count = (2 * Nsp * FreqPointsNum))
                        raw = np.reshape(raw, [2*FreqPointsNum, Nsp], order='F')
                        Data_ChA = raw[0:(FreqPointsNum*2):2, :].transpose()
                        Data_ChB = raw[1:(FreqPointsNum*2):2, :].transpose()

                    if Mode == 2:
                        raw = np.fromfile(file, dtype='u4', count = (4 * Nsp * FreqPointsNum))
                        raw = np.reshape(raw, [4*FreqPointsNum, Nsp], order='F')
                        Data_ChA = raw[0:(FreqPointsNum*4):4, :].transpose()
                        Data_ChB = raw[1:(FreqPointsNum*4):4, :].transpose()
                        Data_CRe = raw[2:(FreqPointsNum*4):4, :].transpose()
                        Data_CIm = raw[3:(FreqPointsNum*4):4, :].transpose()

                    del raw

                    # *** Single out timing from data ***
                    counterA2 = np.uint64(Data_ChA[:,-1])
                    counterB2 = np.uint64(Data_ChB[:,-1])
                    counterA1 = np.uint64(Data_ChA[:,-2])
                    counterB1 = np.uint64(Data_ChB[:,-2])

                    A = np.uint64(int('01111111111111111111111111111111', 2))
                    msCount = np.uint32(np.bitwise_and (counterB2, A))        # number of ms since record started
                    ftCount = np.uint32(np.bitwise_and (counterA2, A))        # number of specter since record started

                    A = np.uint64(int('00000111111111111111111111111111', 2))
                    phaOfSec = np.uint32(np.bitwise_and (counterA1, A))        # phase of second for the spectr
                    A = np.uint64(int('00000000000000011111111111111111', 2))
                    secOfDay = np.uint32(np.bitwise_and (counterB1, A))        # second of the day for the specter



                    # *** Time line arranging ***

                    # Preparing/cleaning matrices for time scales
                    TimeScale = []              # New for each file
                    TimeFigureScale = []        # Timelime (new) for each figure (Nsp)
                    # Calculations
                    FigStartTime = timedelta(0, int(secOfDay[0]), int(1000000*phaOfSec[0]/CLCfrq))
                    for i in range (Nsp):
                        TimeAdd = timedelta(0, int(secOfDay[i]), int(1000000*phaOfSec[i]/CLCfrq))
                        TimeScale.append(str(str(TimeScaleStartDate + TimeAdd)))
                        TimeFigureScale.append(str((TimeAdd - FigStartTime)))

                    TimeFigureScaleFig = np.empty_like(TimeFigureScale)
                    TimeScaleFig = np.empty_like(TimeScale)
                    for i in range (len(TimeFigureScale)):
                        TimeFigureScaleFig[i] = TimeFigureScale[i][0:11]
                        TimeScaleFig[i] = TimeScale[i][11:23]


                    # *** Converting from FPGA to PC float format ***
                    if Mode == 1 or Mode == 2:
                        Data_ChA = FPGAtoPCarrayJDS(Data_ChA, Navr)
                        Data_ChB = FPGAtoPCarrayJDS(Data_ChB, Navr)
                    if (Mode == 2 and CorrelationProcess == 1):
                        Data_CRe = FPGAtoPCarrayJDS(Data_CRe, Navr)
                        Data_CIm = FPGAtoPCarrayJDS(Data_CIm, Navr)


                    '''
                    # *** Absolute correlation specter plot ***
                    if Mode == 2 and figID == 0:   #  Immediate correlation spectrum channels A & B
                        TwoImmedSpectraPlot(frequency, Data_CRe[1][:], Data_CIm[1][:], 'Channel A', 'Channel B',
                                            frequency[0], frequency[FreqPointsNum-1], -0.001, 0.001,
                                            'Frequency, MHz', 'Amplitude, dB',
                                            'Immediate spectrum '+str(df_filename[0:18])+ ' channels A & B',
                                            'Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+str(round(df/1000,3))+' kHz',
                                            'JDS_Results/Service/'+df_filename[0:14]+' Correlation Spectrum Re and Im before log.png')
                    '''



                    # *** Saving data to a long-term file ***
                    if (Mode == 1 or Mode == 2) and longFileSaveAch == 1:
                        Data_AFile = open(Data_A_name, 'ab')
                        Data_AFile.write(Data_ChA)
                        Data_AFile.close()
                    if (Mode == 1 or Mode == 2) and longFileSaveBch == 1:
                        Data_BFile = open(Data_B_name, 'ab')
                        Data_BFile.write(Data_ChB)
                        Data_BFile.close()
                    if  Mode == 2 and longFileSaveCRI == 1 and CorrelationProcess == 1:
                        Data_CReFile = open(Data_CRe_name, 'ab')
                        Data_CReFile.write(np.float64(Data_CRe))
                        Data_CReFile.close()
                        Data_CImFile = open(Data_CIm_name, 'ab')
                        Data_CImFile.write(np.float64(Data_CIm))
                        Data_CImFile.close()

                    if(longFileSaveAch == 1 or longFileSaveBch == 1 or longFileSaveCRI == 1 or longFileSaveCMP == 1):
                        with open(TLfile_name, 'a') as TLfile:
                            for i in range(Nsp):
                                TLfile.write((TimeScale[i][:]+' \n'))  #str.encode



                    # *** Converting to logarythmic scale matrices ***
                    if (Mode == 1 or Mode == 2):
                        with np.errstate(invalid='ignore'):
                            Data_ChA = 10*np.log10(Data_ChA)
                            Data_ChB = 10*np.log10(Data_ChB)
                        Data_ChA[np.isnan(Data_ChA)] = -120
                        Data_ChB[np.isnan(Data_ChB)] = -120
                    if (Mode == 2 and CorrelationProcess == 1):
                        with np.errstate(invalid='ignore', divide='ignore'):
                            CorrModule = 10*np.log10(((Data_CRe)**2 + (Data_CIm)**2)**(0.5))
                            CorrPhase = np.arctan2(Data_CIm, Data_CRe)
                        CorrPhase[np.isnan(CorrPhase)] = 0
                        CorrModule[np.isinf(CorrModule)] = -135.5

                    # *** Saving correlation data to a long-term module and phase files ***
                    if (Mode == 2 and CorrelationProcess == 1 and longFileSaveCMP == 1):
                        Data_CmFile = open(Data_Cm_name, 'ab')
                        Data_CmFile.write(np.float64(CorrModule))
                        Data_CmFile.close()
                        Data_CpFile = open(Data_Cp_name, 'ab')
                        Data_CpFile.write(np.float64(CorrPhase))
                        Data_CpFile.close()


                    # *** Saving immediate spectrum to file ***
                    if(SpecterFileSaveSwitch == 1 and figID == 0):
                        SpFile = open(result_path + '/Service/' +'Specter_'+df_filename[0:14]+'.txt', 'w')
                        for i in range(FreqPointsNum-1):
                            if Mode == 1:
                                SpFile.write(str('{:10.6f}'.format(frequency[i]))+'  '+str('{:16.10f}'.format(Data_ChA[ImmediateSpNo][i]))+'  '+str('{:16.10f}'.format(Data_ChB[ImmediateSpNo][i]))+' \n')
                            if Mode == 2:
                                SpFile.write(str(frequency[i])+'  '+str(Data_ChA[ImmediateSpNo][i])+'  '+str(Data_ChB[ImmediateSpNo][i])+'  '+str(Data_CRe[ImmediateSpNo][i])+'  '+str(Data_CIm[ImmediateSpNo][i])+' \n')

                        SpFile.close()




    #*******************************************************************************
    #                                  F I G U R E S                               *
    #*******************************************************************************

                    # *** Plotting immediate spectra before cleaning and normalizing ***
                    if (Mode == 1 or Mode == 2) and figID == 0:

                        Suptitle = ('Immediate spectrum '+str(df_filename[0:18])+ ' channels A & B')
                        Title = ('Place: '+str(df_obs_place)+', Receiver: '+str(df_system_name)+
                                '. Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+
                                str(round(df/1000,3))+' kHz '+'Description: '+str(df_description))
                        Filename = (result_path + '/Service/' + df_filename[0:14] +
                                    ' Channels A and B Immediate Spectrum before cleaning and normalizing.png')

                        TwoOrOneValuePlot(2, frequency,  Data_ChA[0][:], Data_ChB[0][:],
                                        'Channel A', 'Channel B', frequency[0], frequency[FreqPointsNum-1],
                                        -120, -20, -120, -20, 'Frequency, MHz', 'Intensity, dB', 'Intensity, dB',
                                        Suptitle, Title, Filename,
                                        currentDate, currentTime, Software_version)

                    if Mode == 2 and CorrelationProcess == 1 and figID == 0:

                        Suptitle = ('Immediate correlation spectrum '+str(df_filename[0:18])+ ' channels A & B')
                        Title = ('Place: '+str(df_obs_place)+', Receiver: '+str(df_system_name)+
                                    '. Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+
                                    str(round(df/1000,3))+' kHz '+'Description: '+str(df_description))
                        Filename = (result_path + '/Service/' + df_filename[0:14] +
                                    ' Channels A and B Correlation Immedaiate Spectrum before cleaning and normalizing.png')

                        TwoOrOneValuePlot(2, frequency,  CorrModule[0][:], CorrPhase[0][:],
                                        'Correlation module', 'Correlation phase', frequency[0], frequency[FreqPointsNum-1],
                                        VminCorrMag, VmaxCorrMag, -4, 4, 'Frequency, MHz', 'Amplitude, dB', 'Phase, deg',
                                        Suptitle, Title, Filename,
                                        currentDate, currentTime, Software_version)


                    # *** FIGURE Initial dynamic spectrum channels A and B ***
                    if (Mode == 1 or Mode == 2) and DynSpecSaveInitial == 1:

                        Suptitle = ('Dynamic spectrum (initial) ' + str(df_filename)+' - Fig. '+
                                    str(figID+1)+' of '+str(figMAX)+'\n Initial parameters: dt = '+
                                    str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+
                                    ' kHz, Receiver: '+str(df_system_name)+', Place: '+str(df_obs_place)+
                                    '\n'+ReceiverMode+', Description: '+str(df_description))

                        fig_file_name = (result_path + '/Initial_spectra/' + df_filename[0:14] +
                                        ' Initial dynamic spectrum fig.' + str(figID+1) + '.png')

                        TwoDynSpectraPlot(Data_ChA.transpose(), Data_ChB.transpose(), Vmin, Vmax, Vmin, Vmax, Suptitle,
                                                'Intensity, dB', 'Intensity, dB', Nsp,
                                                TimeFigureScaleFig, TimeScaleFig, frequency,
                                                FreqPointsNum, colormap, 'Channel A', 'Channel B', fig_file_name,
                                                currentDate, currentTime, Software_version, customDPI)


                    # *** FIGURE Initial correlation spectrum Module and Phase (python 3 new version) ***
                    if (Mode == 2 and CorrSpecSaveInitial == 1 and CorrelationProcess == 1):

                        Suptitle = ('Correlation dynamic spectrum (initial) ' + str(df_filename)+
                                    ' - Fig. '+str(figID+1)+' of '+str(figMAX)+'\n Initial parameters: dt = '+
                                    str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz, Receiver: '+
                                    str(df_system_name)+', Place: '+str(df_obs_place)+'\n'+ReceiverMode+
                                    ', Description: '+str(df_description))

                        fig_file_name = (result_path + '/Correlation_spectra/' + df_filename[0:14] +
                                        ' Correlation dynamic spectrum fig.' + str(figID+1) + '.png')

                        TwoDynSpectraPlot(CorrModule.transpose(), CorrPhase.transpose(), VminCorrMag, VmaxCorrMag, -3.15, 3.15, Suptitle,
                                                'Intensity, dB', 'Phase, rad', Nsp,
                                                TimeFigureScaleFig, TimeScaleFig, frequency,
                                                FreqPointsNum, colormap, 'Correlation module', 'Correlation phase',
                                                fig_file_name, currentDate, currentTime, Software_version, customDPI)


                    # *** Normalizing amplitude-frequency responce ***
                    if Mode == 1 or Mode == 2:
                        normalization_db(Data_ChA, FreqPointsNum, Nsp)
                        normalization_db(Data_ChB, FreqPointsNum, Nsp)
                    if Mode == 2 and CorrelationProcess == 1 and CorrSpecSaveCleaned == 1:
                        normalization_db(CorrModule, FreqPointsNum, Nsp)


                    # *** Deleting cahnnels with strong RFI ***
                    if Mode == 1 or Mode == 2:
                        simple_channel_clean(Data_ChA, RFImeanConst)
                        simple_channel_clean(Data_ChB, RFImeanConst)
                    if Mode == 2 and CorrelationProcess == 1 and CorrSpecSaveCleaned == 1:
                        simple_channel_clean(CorrModule, 2 * RFImeanConst)



                    #   *** Immediate spectra ***    (only for first figure in data file)
                    if (Mode == 1 or Mode == 2) and figID == 0:   # Immediate spectrum channels A & B

                        Suptitle = ('Cleaned and normalized immediate spectrum '+str(df_filename[0:18])+ ' channels A & B')
                        Title = ('Place: '+str(df_obs_place)+', Receiver: '+str(df_system_name)+
                                '. Initial parameters: dt = '+str(round(TimeRes,3))+' Sec, df = '+
                                str(round(df/1000,3))+' kHz '+'Description: '+str(df_description))
                        Filename = (result_path + '/Service/'+df_filename[0:14]+
                                    ' Channels A and B Immediate Spectrum after cleaning and normalizing.png')

                        TwoOrOneValuePlot(2, frequency,  Data_ChA[1][:], Data_ChB[1][:],
                                        'Channel A', 'Channel B', frequency[0], frequency[FreqPointsNum-1],
                                        VminNorm-5, VmaxNorm, VminNorm-5, VmaxNorm, 'Frequency, MHz', 'Intensity, dB', 'Intensity, dB',
                                        Suptitle, Title, Filename, currentDate, currentTime, Software_version)


                    # *** FIGURE Normalized dynamic spectrum channels A and B ***
                    if (Mode == 1 or Mode == 2) and DynSpecSaveCleaned == 1:

                        Suptitle = ('Dynamic spectrum (normalized) ' + str(df_filename)+' - Fig. '+
                                    str(figID+1)+' of '+str(figMAX)+'\n Initial parameters: dt = '+
                                    str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+
                                    ' kHz, Receiver: '+str(df_system_name)+', Place: '+str(df_obs_place)+
                                    '\n'+ReceiverMode+', Description: '+str(df_description))

                        fig_file_name = (result_path + '/' + df_filename[0:14] + ' Dynamic spectra fig.' +
                                            str(figID+1) + '.png')

                        TwoDynSpectraPlot(Data_ChA.transpose(), Data_ChB.transpose(), VminNorm, VmaxNorm, VminNorm, VmaxNorm, Suptitle,
                                                'Intensity, dB', 'Intensity, dB', Nsp,
                                                TimeFigureScaleFig, TimeScaleFig, frequency,
                                                FreqPointsNum, colormap, 'Channel A', 'Channel B', fig_file_name,
                                                currentDate, currentTime, Software_version, customDPI)


                    # *** FIGURE Normalized correlation spectrum Module and Phase ***
                    if (Mode == 2 and CorrSpecSaveCleaned == 1 and CorrelationProcess == 1):

                        Suptitle = ('Correlation dynamic spectrum (normalized) ' + str(df_filename)+
                                    ' - Fig. '+str(figID+1)+' of '+str(figMAX)+'\n Initial parameters: dt = '+
                                    str(round(TimeRes*1000,3))+' ms, df = '+str(round(df/1000.,3))+' kHz, Receiver: '+
                                    str(df_system_name)+', Place: '+str(df_obs_place)+'\n'+ReceiverMode+
                                    ', Description: '+str(df_description))

                        fig_file_name = (result_path + '/Correlation_spectra/' + df_filename[0:14] +
                                        ' Correlation dynamic spectra cleaned fig.' + str(figID+1) + '.png')
                        TwoDynSpectraPlot(CorrModule.transpose(), CorrPhase.transpose(), 2*VminNorm, 2*VmaxNorm, -3.15, 3.15, Suptitle,
                                                'Intensity, dB', 'Phase, rad', Nsp,
                                                TimeFigureScaleFig, TimeScaleFig, frequency,
                                                FreqPointsNum, colormap, 'Normalized correlation module', 'Correlation phase',
                                                fig_file_name, currentDate, currentTime, Software_version, customDPI)



                '''
                # Check of second counter data for linearity
                OneImmedSpecterPlot(list(range(ChunksInFile)), timeLineSecond, 'timeLineSecond',
                                    0, ChunksInFile, 0, 2000,
                                    'Time, sec', 'Second counter, sec',
                                    'Second counter',
                                    ' ',
                                    'ADR_Results/Service/' + df_filename[0:14] + ' Second counter fig.' + str(figID+1) + '.png')

                '''

                gc.collect()

            #print ('\n  Position in file: ', file.tell(), ' File size: ', df_filesize)
            #if (file.tell() == df_filesize): print ('\n  File was read till the end \n')
            if (file.tell() < df_filesize):
                print ('    The difference is ', (df_filesize - file.tell()), ' bytes')
                print ('\n  File was NOT read till the end!!! ERROR')

        file.close()  #Here we close the data file

    ok = 1
    return ok, DAT_file_name, DAT_file_list

#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************

if __name__ == '__main__':

    fileList = 'DATA/'
    result_path = ''

    done_or_not, DAT_file_name, DAT_file_list = JDS_file_reader(directory, result_path, MaxNim, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
            VminCorrMag, VmaxCorrMag, customDPI, colormap, CorrelationProcess, Sum_Diff_Calculate,
            longFileSaveAch, longFileSaveBch, longFileSaveCMP, longFileSaveCRI, longFileSaveSSD,
            DynSpecSaveInitial, DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned,
            SpecterFileSaveSwitch, ImmediateSpNo)
