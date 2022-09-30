# Python3
Software_version = '2019.08.02'
# ###############################################################################
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import os
import math
import numpy as np
import time
import gc
import datetime
from datetime import datetime, timedelta
import warnings
import matplotlib
matplotlib.use('agg')
warnings.filterwarnings("ignore")

from package_ra_data_files_formats.read_file_header_adr import FileHeaderReaderADR, ChunkHeaderReaderADR
from package_ra_data_files_formats.FPGA_to_PC_array import FPGAtoPCarrayADR
from package_cleaning.simple_channel_clean import simple_channel_clean
from package_plot_formats.plot_formats import TwoOrOneValuePlot, OneDynSpectraPlot, TwoDynSpectraPlot
from package_ra_data_processing.f_spectra_normalization import normalization_db
# ###############################################################################


# *** Search ADR files in the directory ***

def ADR_file_reader(file_list, result_path, MaxNim, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                    VminCorrMag, VmaxCorrMag, custom_dpi, colormap, CorrelationProcess, Sum_Diff_Calculate,
                    longFileSaveAch, longFileSaveBch, longFileSaveCMP, longFileSaveCRI, longFileSaveSSD,
                    DynSpecSaveInitial, DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned,
                    SpectrumFileSaveSwitch, ImmediateSpNo, print_or_not):

    current_date = time.strftime("%d.%m.%Y")

    if not os.path.exists(result_path):
        os.makedirs(result_path)
    if not os.path.exists(result_path + '/Service'):
        os.makedirs(result_path + '/Service')
    if DynSpecSaveInitial == 1:
        if not os.path.exists(result_path + '/Initial_spectra'):
            os.makedirs(result_path + '/Initial_spectra')
    if DynSpecSaveCleaned == 1 and CorrelationProcess == 1:
        if not os.path.exists(result_path + '/Correlation_spectra'):
            os.makedirs(result_path + '/Correlation_spectra')

    for fileNo in range(len(file_list)):   # loop by files

        # *** Opening datafile ***
        fname = ''
        if len(fname) < 1:
            fname = file_list[fileNo]

        # Reading the file header
        [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
                F_ADC, df_creation_utc, ReceiverMode, adr_mode,
                sum_dif_mode, NAvr, time_res, fmin, fmax, df, frequency,
                FFT_Size, SLine, Width, BlockSize] = FileHeaderReaderADR(fname, 0, 0)

        # Reading the chunk header
        [sp_in_file, sp_in_frame, FrameInChunk, ChunksInFile, sizeOfChunk,
                frm_sec, frm_phase] = ChunkHeaderReaderADR(fname, 0, BlockSize, 0)

        freq_points_num = int(Width * 1024)

        # *** Setting the time reference (file beginning) ***
        TimeFirstFramePhase = float(frm_phase)/F_ADC
        TimeFirstFrameFloatSec = frm_sec + TimeFirstFramePhase
        TimeScaleStartTime = datetime(int('20' + df_filename[1:3]), int(df_filename[3:5]), int(df_filename[5:7]),
                                      int(df_creation_utc[0:2]), int(df_creation_utc[3:5]),
                                      int(df_creation_utc[6:8]), int(df_creation_utc[9:12])*1000)

        with open(fname, 'rb') as file:

            # *** Reading indexes of data from index file '*.fft' ***
            indexes = []
            ifname = 'package_ra_data_files_formats/' + str(int(FFT_Size/2)) + '.fft'
            indexfile = open(ifname, 'r')
            num = 0
            for line in indexfile:
                ind = int(line)
                if (ind >= SLine*1024) & (ind < ((SLine+Width)*1024)):
                    indexes.append(ind - SLine*1024)
                num = num + 1
            indexfile.close()

            timeLineSecond = np.zeros(ChunksInFile)  # List of second values from DSP_INF field

            # *** If it is the first file - write the header to long data file ***
            if(longFileSaveAch == 1 or longFileSaveBch == 1 or longFileSaveCRI == 1 or
               longFileSaveCMP == 1 or longFileSaveSSD == 1) and fileNo == 0:
                file.seek(0)
                file_header = file.read(1024)

                # *** Creating a name for long timeline TXT file ***
                tl_file_name = df_filename + '_Timeline.txt'
                tl_file = open(tl_file_name, 'w')  # Open and close to delete the file with the same name
                tl_file.close()

                DAT_file_name = df_filename
                DAT_file_list = []

                # *** Creating a binary file with data for long data storage ***
                if longFileSaveAch == 1 and (adr_mode == 3 or adr_mode == 5 or adr_mode == 6):
                    fileData_A_name = df_filename + '_Data_chA.dat'
                    fileData_A = open(fileData_A_name, 'wb')
                    fileData_A.write(file_header)
                    fileData_A.close()
                    DAT_file_list.append('chA')
                if longFileSaveBch == 1 and (adr_mode == 4 or adr_mode == 5 or adr_mode == 6):
                    fileData_B_name = df_filename + '_Data_chB.dat'
                    fileData_B = open(fileData_B_name, 'wb')
                    fileData_B.write(file_header)
                    fileData_B.close()
                    DAT_file_list.append('chB')
                if CorrelationProcess == 1 and longFileSaveCRI == 1 and adr_mode == 6:
                    fileData_CRe_name = df_filename + '_Data_CRe.dat'
                    fileData_C_Re = open(fileData_CRe_name, 'wb')
                    fileData_C_Re.write(file_header)
                    fileData_C_Re.close()
                    DAT_file_list.append('CRe')
                    fileData_CIm_name = df_filename + '_Data_CIm.dat'
                    fileData_C_Im = open(fileData_CIm_name, 'wb')
                    fileData_C_Im.write(file_header)
                    fileData_C_Im.close()
                    DAT_file_list.append('CIm')
                if CorrelationProcess == 1 and longFileSaveCMP == 1 and adr_mode == 6:
                    fileData_CM_name = df_filename + '_Data_C_m.dat'
                    fileData_C_M = open(fileData_CM_name, 'wb')
                    fileData_C_M.write(file_header)
                    fileData_C_M.close()
                    DAT_file_list.append('C_m')
                    fileData_CP_name = df_filename + '_Data_C_p.dat'
                    fileData_C_P = open(fileData_CP_name, 'wb')
                    fileData_C_P.write(file_header)
                    fileData_C_P.close()
                    DAT_file_list.append('C_p')
                if Sum_Diff_Calculate == 1 and longFileSaveSSD == 1 and (adr_mode == 5 or adr_mode == 6):
                    fileData_Sum_name = df_filename+'_Data_Sum.dat'
                    fileData_Sum = open(fileData_Sum_name, 'wb')
                    fileData_Sum.write(file_header)
                    fileData_Sum.close()
                    fileData_Dif_name = df_filename+'_Data_Dif.dat'
                    fileData_Dif = open(fileData_Dif_name, 'wb')
                    fileData_Dif.write(file_header)
                    fileData_Dif.close()

                del file_header

            # ************************************************************************************
            #                             R E A D I N G   D A T A                                *
            # ************************************************************************************

            file.seek(1024)  # Jumping to 1024 byte from file beginning

            if adr_mode > 2 and adr_mode < 7:           # Spectrum modes
                fig_id = -1
                figMAX = int(math.ceil(ChunksInFile/MaxNim))
                if figMAX < 1:
                    figMAX = 1
                for fig in range(figMAX):
                    fig_id = fig_id + 1
                    current_time = time.strftime("%H:%M:%S")
                    if print_or_not > 0:
                        print('   File # ', str(fileNo+1), ' of ', str(len(file_list)), ', figure # ',
                                                fig_id+1, ' of ', figMAX, '   started at: ', current_time)
                    if (ChunksInFile - MaxNim * fig_id) < MaxNim:
                        Nim = (ChunksInFile - MaxNim * fig_id)
                    else:
                        Nim = MaxNim
                    # SpectrNum = Nim * sp_in_frame * FrameInChunk # Number of spectra in the figure

                    # *** Preparing empty matrices ***
                    if adr_mode == 3 or adr_mode == 5 or adr_mode == 6:
                        Data_Ch_A = np.zeros((Nim * sp_in_frame * FrameInChunk, freq_points_num))
                        Data_Ch_A0 = np.zeros((Nim * sp_in_frame * FrameInChunk, freq_points_num))
                    if adr_mode == 4 or adr_mode == 5 or adr_mode == 6:
                        Data_Ch_B = np.zeros((Nim * sp_in_frame * FrameInChunk, freq_points_num))
                        Data_Ch_B0 = np.zeros((Nim * sp_in_frame * FrameInChunk, freq_points_num))
                    if adr_mode == 6:
                        Data_C_Im = np.zeros((Nim * sp_in_frame * FrameInChunk, freq_points_num))
                        Data_C_Re = np.zeros((Nim * sp_in_frame * FrameInChunk, freq_points_num))
                        Data_C_Im0 = np.zeros((Nim * sp_in_frame * FrameInChunk, freq_points_num))
                        Data_C_Re0 = np.zeros((Nim * sp_in_frame * FrameInChunk, freq_points_num))
                        CorrModule = np.zeros((Nim * sp_in_frame * FrameInChunk, freq_points_num))
                        CorrPhase = np.zeros((Nim * sp_in_frame * FrameInChunk, freq_points_num))

                    TimeScale = []
                    TimeFigureScale = []  # Timelime (new) for each figure
                    TimeFigureStartTime = datetime(2016, 1, 1, 0, 0, 0, 0)

                    # *** DATA READING process ***

                    # Reading and reshaping all data with readers
                    raw = np.fromfile(file, dtype='i4', count=int((Nim * (sizeOfChunk+8))/4))
                    raw = np.reshape(raw, [int((sizeOfChunk+8)/4), Nim], order='F')

                    # Splitting headers from data
                    headers = raw[0:1024, :]
                    data = raw[1024:, :]
                    del raw

                    # Arranging data in right order
                    if adr_mode == 3:
                        data = np.reshape(data, [freq_points_num, Nim*FrameInChunk*sp_in_frame], order='F')
                        Data_Ch_A0 = data[0:freq_points_num:1, :].transpose()
                    if adr_mode == 4:
                        data = np.reshape(data, [freq_points_num, Nim*FrameInChunk*sp_in_frame], order='F')
                        Data_Ch_B0 = data[0:freq_points_num:1, :].transpose()
                    if adr_mode == 5:
                        data = np.reshape(data, [freq_points_num*2, Nim*FrameInChunk*sp_in_frame], order='F')
                        Data_Ch_B0 = data[0:(freq_points_num*2):2, :].transpose()
                        Data_Ch_A0 = data[1:(freq_points_num*2):2, :].transpose()
                    if adr_mode == 6:
                        data = np.reshape(data, [freq_points_num*4, Nim*FrameInChunk*sp_in_frame], order='F')
                        Data_C_Im0 = data[0:(freq_points_num*4):4, :].transpose()
                        Data_C_Re0 = data[1:(freq_points_num*4):4, :].transpose()
                        Data_Ch_B0 = data[2:(freq_points_num*4):4, :].transpose()
                        Data_Ch_A0 = data[3:(freq_points_num*4):4, :].transpose()
                    del data

                    # *** TimeLine calculations ***
                    for i in range(Nim):

                        # *** DSP_INF ***
                        frm_count = headers[3][i]
                        frm_sec = headers[4][i]
                        frm_phase = headers[5][i]

                        # * Absolute time calculation *
                        timeLineSecond[fig_id*MaxNim+i] = frm_sec # to check the linearity of seconds
                        TimeCurrentFramePhase = float(frm_phase)/F_ADC
                        TimeCurrentFrameFloatSec = frm_sec + TimeCurrentFramePhase
                        TimeSecondDiff = TimeCurrentFrameFloatSec - TimeFirstFrameFloatSec
                        TimeAdd = timedelta(0, int(np.fix(TimeSecondDiff)),
                                            int(np.fix((TimeSecondDiff - int(np.fix(TimeSecondDiff)))*1000000)))

                        # Adding of time point to time line is in loop by spectra because
                        # for each spectra in frame there is one time point but it should
                        # appear for all spectra to fit the dimensions of arrays

                        # * Time from figure start calculation *
                        if i == 0:
                            TimeFigureStart = TimeCurrentFrameFloatSec
                        TimeFigureSecondDiff = TimeCurrentFrameFloatSec - TimeFigureStart
                        TimeFigureAdd = timedelta(0, int(np.fix(TimeFigureSecondDiff)),
                                                  int(np.fix((TimeFigureSecondDiff - int(np.fix(TimeFigureSecondDiff)))*1000000)))

                        for iframe in range(0, sp_in_frame):
                            TimeScale.append(str((TimeScaleStartTime + TimeAdd)))  #.time()
                            TimeFigureScale.append(str((TimeFigureStartTime+TimeFigureAdd).time()))

                    # Exact string timescales to show on plots
                    TimeFigureScaleFig = np.empty_like(TimeFigureScale)
                    TimeScaleFig = np.empty_like(TimeScale)
                    for i in range(len(TimeFigureScale)):
                        TimeFigureScaleFig[i] = TimeFigureScale[i][0:11]
                        TimeScaleFig[i] = TimeScale[i][11:23]

                    # *** Performing index changes ***
                    for i in range(0, freq_points_num):
                        n = indexes[i]
                        if adr_mode == 3 or adr_mode == 5 or adr_mode == 6:
                            Data_Ch_A[:, n] = Data_Ch_A0[:, i]
                        if adr_mode == 4 or adr_mode == 5 or adr_mode == 6:
                            Data_Ch_B[:, n] = Data_Ch_B0[:, i]
                        if adr_mode == 6 and CorrelationProcess == 1:
                            Data_C_Im[:, n] = Data_C_Im0[:, i]
                            Data_C_Re[:, n] = Data_C_Re0[:, i]

                    # *** Deleting matrices which were necessary for index changes ***
                    del n

                    if adr_mode == 3 or adr_mode == 5 or adr_mode == 6:
                        del Data_Ch_A0
                    if adr_mode == 4 or adr_mode == 5 or adr_mode == 6:
                        del Data_Ch_B0
                    if adr_mode == 6 and CorrelationProcess == 1:
                        del Data_C_Im0, Data_C_Re0

                    # *** Converting from FPGA to PC float format ***
                    if adr_mode == 3 or adr_mode == 5 or adr_mode == 6:
                        Data_Ch_A = FPGAtoPCarrayADR(Data_Ch_A, NAvr)
                    if adr_mode == 4 or adr_mode == 5 or adr_mode == 6:
                        Data_Ch_B = FPGAtoPCarrayADR(Data_Ch_B, NAvr)
                    if adr_mode == 6 and CorrelationProcess == 1:
                        Data_C_Re = FPGAtoPCarrayADR(Data_C_Re, NAvr)
                        Data_C_Im = FPGAtoPCarrayADR(Data_C_Im, NAvr)

                    # *** Calculating Sum and Difference of A and B channels ***
                    if (adr_mode == 5 or adr_mode == 6) and Sum_Diff_Calculate == 1:
                        Data_Sum = Data_Ch_A + Data_Ch_B
                        Data_Dif = abs(Data_Ch_A - Data_Ch_B)

                    # *** Saving data to a long-term file ***
                    if (adr_mode == 3 or adr_mode == 5 or adr_mode == 6) and longFileSaveAch == 1:
                        fileData_A = open(fileData_A_name, 'ab')
                        fileData_A.write(Data_Ch_A)
                        fileData_A.close()
                    if (adr_mode == 4 or adr_mode == 5 or adr_mode == 6) and longFileSaveBch == 1:
                        fileData_B = open(fileData_B_name, 'ab')
                        fileData_B.write(Data_Ch_B)
                        fileData_B.close()
                    if  adr_mode == 6 and longFileSaveCRI == 1 and CorrelationProcess == 1:
                        fileData_C_Re = open(fileData_CRe_name, 'ab')
                        fileData_C_Re.write(Data_C_Re)
                        fileData_C_Re.close()
                        fileData_C_Im = open(fileData_CIm_name, 'ab')
                        fileData_C_Im.write(Data_C_Im)
                        fileData_C_Im.close()
                    if (adr_mode == 5 or adr_mode == 6) and Sum_Diff_Calculate == 1 and longFileSaveSSD == 1:
                        fileData_Sum = open(fileData_Sum_name, 'ab')
                        fileData_Sum.write(Data_Sum)
                        fileData_Sum.close()
                        fileData_Dif = open(fileData_Dif_name, 'ab')
                        fileData_Dif.write(Data_Dif)
                        fileData_Dif.close()
                        del Data_Sum, Data_Dif

                    if longFileSaveAch == 1 or longFileSaveBch == 1 or longFileSaveCRI == 1 or longFileSaveCMP == 1 or longFileSaveSSD == 1:
                        with open(tl_file_name, 'a') as tl_file:
                            for i in range(sp_in_frame * FrameInChunk * Nim):
                                tl_file.write((TimeScale[i][:]) + ' \n')   # str

                    # *** Converting to logarithmic scale matrices ***
                    if adr_mode == 3 or adr_mode == 5 or adr_mode == 6:
                        with np.errstate(divide='ignore'):
                            Data_Ch_A = 10 * np.log10(Data_Ch_A)
                    if adr_mode == 4 or adr_mode == 5 or adr_mode == 6:
                        with np.errstate(divide='ignore'):
                            Data_Ch_B = 10 * np.log10(Data_Ch_B)
                    if adr_mode == 6 and CorrelationProcess == 1:
                        with np.errstate(divide='ignore'):
                            CorrModule = (Data_C_Re**2 + Data_C_Im**2)**0.5
                            CorrModule = 10 * np.log10(CorrModule)
                            CorrPhase = np.arctan2(Data_C_Im, Data_C_Re)
                        CorrModule[np.isnan(CorrModule)] = 0
                        CorrPhase[np.isnan(CorrPhase)] = 0

                    # *** Writing correlation data to long files ***
                    if adr_mode == 6 and longFileSaveCMP == 1 and CorrelationProcess == 1:
                        fileData_C_M = open(fileData_CM_name, 'ab')
                        fileData_C_M.write(np.float64(CorrModule))
                        fileData_C_M.close()
                        fileData_C_P = open(fileData_CP_name, 'ab')
                        fileData_C_P.write(np.float64(CorrPhase))
                        fileData_C_P.close()

                    # *** Saving immediate spectrum to file ***
                    if SpectrumFileSaveSwitch == 1 and fig_id == 0:
                        SpFile = open(result_path + '/Service/Spectrum_' + df_filename[0:14] + '.txt', 'w')
                        for i in range(freq_points_num-1):
                            if adr_mode == 3:
                                SpFile.write(str('{:10.6f}'.format(frequency[i])) + '  ' +
                                             str('{:16.10f}'.format(Data_Ch_A[ImmediateSpNo][i])) + ' \n')
                            if adr_mode == 4:
                                SpFile.write(str('{:10.6f}'.format(frequency[i])) + '  ' +
                                             str('{:16.10f}'.format(Data_Ch_B[ImmediateSpNo][i])) + ' \n')
                            if adr_mode == 5 or adr_mode == 6:
                                SpFile.write(str('{:10.6f}'.format(frequency[i])) + '  ' +
                                             str('{:16.10f}'.format(Data_Ch_A[ImmediateSpNo][i])) + '  ' +
                                             str('{:16.10f}'.format(Data_Ch_B[ImmediateSpNo][i])) + ' \n')
                        SpFile.close()

                    # *** FIGURE Immediate spectra before cleaning and normalizing ***
                    if fig_id == 0:
                        if adr_mode == 3:
                            Data_1 = Data_Ch_A[0][:]
                            Legend_1 = 'Channel A'
                        if adr_mode == 4:
                            Data_1 = Data_Ch_B[0][:]
                            Legend_1 = 'Channel B'
                        if adr_mode == 3 or adr_mode == 4:
                            no_of_sets = 1
                            Data_2 = []
                            Suptitle = ('Immediate spectrum ' + str(df_filename[0:18]) + ' ' + Legend_1)
                            Title = ('Initial parameters: dt = ' + str(round(time_res*1000, 3)) + ' ms, df = ' +
                                     str(round(df/1000.,3)) + ' kHz' + sum_dif_mode + ', Description: ' +
                                     str(df_description))
                            Filename = (result_path + '/Service/'+df_filename[0:14] + ' ' +
                                        Legend_1 + ' Immediate Spectrum before cleaning and normalizing.png')

                        if adr_mode == 5 or adr_mode == 6:     # Immediate spectrum channels A & B
                            Data_1 = Data_Ch_A[0][:]
                            Data_2 = Data_Ch_B[0][:]
                            Legend_1 = 'Channel A'
                            no_of_sets = 2
                            Suptitle = ('Immediate spectrum '+str(df_filename[0:18]) + ' channels A & B')
                            Title = ('Initial parameters: dt = '+str(round(time_res*1000, 3)) + ' ms, df = ' +
                                     str(round(df/1000., 3)) + ' kHz,' + sum_dif_mode + ' Description: ' +
                                     str(df_description))
                            Filename = (result_path + '/Service/' + df_filename[0:14] +
                                        ' Channels A and B Immediate Spectrum before cleaning and normalizing.png')

                        TwoOrOneValuePlot(no_of_sets, frequency,  Data_1, Data_2, Legend_1, 'Channel B',
                                          frequency[0], frequency[-1], -120, -20, -120, -20, 'Frequency, MHz',
                                          'Intensity, dB', 'Intensity, dB', Suptitle, Title, Filename, current_date,
                                          current_time, Software_version)

                    # *** FIGURE Correlation amplitude and phase immediate spectrum ***
                    if adr_mode == 6 and fig_id == 0 and CorrelationProcess == 1:  # Immediate corr spectrum A & B

                        Suptitle = ('Immediate correlation spectrum ' + str(df_filename[0:18]) + ' channels A & B')
                        Title = ('Initial parameters: dt = ' + str(round(time_res*1000, 3)) + ' ms, df = ' +
                                 str(round(df/1000., 3)) + ' kHz,' + sum_dif_mode + ' Description: ' +
                                 str(df_description))
                        Filename = (result_path + '/Service/' + df_filename[0:14] +
                                    ' Channels A and B Correlation module and phase spectrum.png')

                        TwoOrOneValuePlot(2, frequency,   CorrModule[0][:], CorrPhase[0][:],
                                    'Correlation module', 'Correlation phase', frequency[0], frequency[freq_points_num-1],
                                    -150, -20, -4, 4, 'Frequency, MHz', 'Intensity, dB', 'Phase, rad',
                                    Suptitle, Title, Filename,
                                    current_date, current_time, Software_version)

                    # *** FIGURE Initial dynamic spectrum of 1 channel (A or B) ***
                    if (adr_mode == 3 or adr_mode == 4) and DynSpecSaveInitial == 1:
                        if adr_mode == 3:
                            Data = Data_Ch_A.transpose()
                        if adr_mode == 4:
                            Data = Data_Ch_B.transpose()

                        Suptitle = ('Dynamic spectrum (initial) ' + str(df_filename[0:18]) +
                                    ' - Fig. ' + str(fig_id+1) + ' of ' + str(figMAX) +
                                    '\n Initial parameters: dt = ' + str(round(time_res*1000, 3)) +
                                    ' ms, df = ' + str(round(df/1000., 3)) + ' kHz, ' + sum_dif_mode +
                                    ' Receiver: ' + str(df_system_name) +
                                    ', Place: ' + str(df_obs_place) +
                                    '\n Description: ' + str(df_description))

                        fig_file_name = (result_path + '/Initial_spectra/' + df_filename[0:14] +
                                         ' Initial dynamic spectrum fig.' + str(fig_id+1) + '.png')

                        OneDynSpectraPlot(Data, -120, -30, Suptitle, 'Intensity, dB', Nim * sp_in_frame * FrameInChunk,
                                          TimeScaleFig, frequency, freq_points_num, colormap, 'UTC Time, HH:MM:SS.msec',
                                          fig_file_name, current_date, current_time, Software_version, custom_dpi)

                    # *** FIGURE Initial dynamic spectrum channels A and B ***
                    if (adr_mode == 5 or adr_mode == 6) and DynSpecSaveInitial == 1:

                        fig_file_name = (result_path + '/Initial_spectra/' + df_filename[0:14] +
                                         ' Initial dynamic spectrum fig.' + str(fig_id+1) + '.png')
                        Suptitle = ('Dynamic spectrum (initial) ' + str(df_filename) + ' - Fig. ' +
                                    str(fig_id+1) + ' of ' + str(figMAX) + '\n Initial parameters: dt = ' +
                                    str(round(time_res*1000, 3)) + ' ms, df = ' + str(round(df/1000., 3)) + ' kHz, ' +
                                    sum_dif_mode + ' Receiver: ' + str(df_system_name)+', Place: '+str(df_obs_place) +
                                    '\n' + ReceiverMode + ', Description: ' + str(df_description))

                        TwoDynSpectraPlot(Data_Ch_A.transpose(), Data_Ch_B.transpose(), Vmin, Vmax, Vmin, Vmax,
                                          Suptitle, 'Intensity, dB', 'Intensity, dB', Nim * sp_in_frame * FrameInChunk,
                                          TimeFigureScaleFig, TimeScaleFig, frequency, freq_points_num, colormap,
                                          'Channel A', 'Channel B', fig_file_name, current_date, current_time,
                                          Software_version, custom_dpi)

                    # *** FIGURE Initial correlation spectrum module and phase ***
                    if adr_mode == 6 and CorrSpecSaveInitial == 1 and CorrelationProcess == 1:

                        fig_file_name = (result_path + '/Correlation_spectra/' + df_filename[0:14] +
                                         ' Correlation dynamic spectrum fig.' + str(fig_id+1) + '.png')
                        Suptitle = ('Correlation dynamic spectrum (initial) ' + str(df_filename)+' - Fig. ' +
                                    str(fig_id+1) + ' of ' + str(figMAX) + '\n Initial parameters: dt = ' +
                                    str(round(time_res*1000, 3)) + ' ms, df = ' + str(round(df/1000., 3)) + ' kHz, ' +
                                    sum_dif_mode + ' Receiver: ' + str(df_system_name) + ', Place: ' + str(df_obs_place) +
                                    '\n' + ReceiverMode + ', Description: ' + str(df_description))

                        TwoDynSpectraPlot(CorrModule.transpose(), CorrPhase.transpose(), VminCorrMag, VmaxCorrMag,
                                          -3.15, 3.15, Suptitle, 'Intensity, dB', 'Phase, rad',
                                          Nim * sp_in_frame * FrameInChunk, TimeFigureScaleFig, TimeScaleFig, frequency,
                                          freq_points_num, colormap, 'Correlation module', 'Correlation phase',
                                          fig_file_name, current_date, current_time, Software_version, custom_dpi)

                    # *** Normalizing amplitude-frequency response ***
                    if (adr_mode == 3 or adr_mode == 5 or adr_mode == 6) and DynSpecSaveCleaned == 1:
                        normalization_db(Data_Ch_A, freq_points_num, Nim * sp_in_frame * FrameInChunk)
                    if (adr_mode == 4 or adr_mode == 5 or adr_mode == 6) and DynSpecSaveCleaned == 1:
                        normalization_db(Data_Ch_B, freq_points_num, Nim * sp_in_frame * FrameInChunk)
                    if adr_mode == 6 and CorrelationProcess == 1 and CorrSpecSaveCleaned == 1:
                        normalization_db(CorrModule, freq_points_num, Nim * sp_in_frame * FrameInChunk)

                    # *** Deleting channels with strong RFI ***
                    if (adr_mode == 3 or adr_mode == 5 or adr_mode == 6) and DynSpecSaveCleaned == 1:
                        simple_channel_clean(Data_Ch_A, RFImeanConst)
                    if (adr_mode == 4 or adr_mode == 5 or adr_mode == 6) and DynSpecSaveCleaned == 1:
                        simple_channel_clean(Data_Ch_B, RFImeanConst)
                    if adr_mode == 6 and CorrelationProcess == 1 and CorrSpecSaveCleaned == 1:
                        simple_channel_clean(CorrModule, 2 * RFImeanConst)

                    #   *** Immediate spectra of normalized data ***    (only for first figure in data file)
                    if fig_id == 0 and DynSpecSaveCleaned == 1:
                        if adr_mode == 3:
                            Data_1 = Data_Ch_A[0][:]
                            Legend_1 = 'Channel A'
                        if adr_mode == 4:
                            Data_1 = Data_Ch_B[0][:]
                            Legend_1 = 'Channel B'
                        if adr_mode == 3 or adr_mode == 4:
                            no_of_sets = 1
                            Data_2 = []
                            Suptitle = ('Normalized immediate spectrum ' + str(df_filename[0:18]) + ' ' + Legend_1)
                            Title = ('Initial parameters: dt = ' + str(round(time_res*1000, 3)) + ' ms, df = ' +
                                     str(round(df/1000., 3)) + ' kHz' + sum_dif_mode + ', Description: ' +
                                     str(df_description))
                            Filename = (result_path + '/Service/' + df_filename[0:14] + ' ' +
                                    Legend_1 + ' Immediate Spectrum after cleaning and normalizing.png')

                        if adr_mode == 5 or adr_mode == 6:   # Immediate spectrum channels A & B
                            no_of_sets = 2
                            Data_1 = Data_Ch_A[0][:]
                            Data_2 = Data_Ch_B[0][:]
                            Legend_1 = 'Channel A'
                            Suptitle = ('Normalized immediate spectrum ' + str(df_filename[0:18]) + ' channels A & B')
                            Title = ('Initial parameters: dt = ' + str(round(time_res*1000, 3)) + ' ms, df = ' +
                                     str(round(df/1000.,3)) + ' kHz' + sum_dif_mode + ', Description: ' +
                                     str(df_description))
                            Filename = (result_path + '/Service/' + df_filename[0:14] +
                                        ' Channels A and B Immediate Spectrum after cleaning and normalizing.png')

                        TwoOrOneValuePlot(no_of_sets, frequency,  Data_1,  Data_2, Legend_1, 'Channel B',
                                          frequency[0], frequency[-1], -10, 40, -10, 40, 'Frequency, MHz',
                                          'Intensity, dB', 'Intensity, dB', Suptitle, Title, Filename, current_date,
                                          current_time, Software_version)

                    # *** FIGURE Cleaned and normalized dynamic spectrum of 1 channel A or B
                    if (adr_mode == 3 or adr_mode == 4) and DynSpecSaveCleaned == 1:
                        if adr_mode == 3:
                            Data = Data_Ch_A.transpose()
                        if adr_mode == 4:
                            Data = Data_Ch_B.transpose()

                        Suptitle = ('Dynamic spectrum (normalized) ' + str(df_filename[0:18]) +
                                    ' - Fig. ' + str(fig_id+1) + ' of ' + str(figMAX) +
                                    '\n Initial parameters: dt = ' + str(round(time_res*1000,3)) +
                                    ' ms, df = ' + str(round(df/1000., 3)) + ' kHz, ' + sum_dif_mode +
                                    ' Receiver: ' + str(df_system_name) + ', Place: ' + str(df_obs_place) +
                                    '\n Description: '+str(df_description))

                        fig_file_name = (result_path + '/' + df_filename[0:14] +
                                         ' Dynamic spectrum fig.' + str(fig_id+1) + '.png')

                        OneDynSpectraPlot(Data, VminNorm, VmaxNorm, Suptitle, 'Intensity, dB',
                                          Nim * sp_in_frame * FrameInChunk, TimeScaleFig, frequency, freq_points_num,
                                          colormap, 'UTC Time, HH:MM:SS.msec', fig_file_name, current_date, current_time,
                                          Software_version, custom_dpi)

                    # *** FIGURE Dynamic spectrum channels A and B cleaned and normalized (python 3 new version) ***
                    if (adr_mode == 5 or adr_mode == 6) and DynSpecSaveCleaned == 1:
                        fig_file_name = (result_path + '/' + df_filename[0:14] + ' Dynamic spectrum fig.' +
                                         str(fig_id+1) + '.png')
                        Suptitle = ('Dynamic spectrum (normalized) ' + str(df_filename) + ' - Fig. ' + str(fig_id+1) +
                                    ' of ' + str(figMAX) + '\n Initial parameters: dt = ' + str(round(time_res*1000, 3)) +
                                    ' ms, df = ' + str(round(df/1000., 3)) + ' kHz, ' + sum_dif_mode + ' Receiver: ' +
                                    str(df_system_name) + ', Place: ' + str(df_obs_place) + '\n' + ReceiverMode +
                                    ', Description: ' + str(df_description))

                        TwoDynSpectraPlot(Data_Ch_A.transpose(), Data_Ch_B.transpose(), VminNorm, VmaxNorm, VminNorm,
                                          VmaxNorm, Suptitle, 'Intensity, dB', 'Intensity, dB',
                                          Nim * sp_in_frame * FrameInChunk, TimeFigureScaleFig, TimeScaleFig, frequency,
                                          freq_points_num, colormap, 'Channel A', 'Channel B', fig_file_name,
                                          current_date, current_time, Software_version, custom_dpi)

                    # *** FIGURE Correlation spectrum module and phase cleaned and normalized (python 3 new version) ***
                    if adr_mode == 6 and CorrSpecSaveCleaned == 1 and CorrelationProcess == 1:
                        Suptitle = 'Correlation dynamic spectrum (normalized) ' + str(df_filename) + ' - Fig. ' + \
                                   str(fig_id+1) + ' of ' + str(figMAX) + '\n Initial parameters: dt = ' + \
                                   str(round(time_res*1000, 3)) + ' ms, df = ' + str(round(df/1000., 3)) + ' kHz, ' + \
                                   sum_dif_mode+' Receiver: ' + str(df_system_name) + ', Place: ' + str(df_obs_place) +\
                                   '\n' + ReceiverMode+', Description: ' + str(df_description)
                        fig_file_name = result_path + '/Correlation_spectra/' + df_filename[0:14] + \
                                        ' Correlation dynamic spectrum cleaned fig.' + str(fig_id+1) + '.png'
                        TwoDynSpectraPlot(CorrModule.transpose(), CorrPhase.transpose(), VminNorm, 3*VmaxNorm,
                                          -3.15, 3.15, Suptitle, 'Intensity, dB', 'Phase, rad',
                                          Nim * sp_in_frame * FrameInChunk, TimeFigureScaleFig, TimeScaleFig, frequency,
                                          freq_points_num, colormap, 'Normalized and cleaned correlation module',
                                          'Correlation phase', fig_file_name, current_date, current_time,
                                          Software_version, custom_dpi)

                gc.collect()
            del timeLineSecond
            # print ('\n  Position in file: ', file.tell(), ' File size: ', df_filesize)
            # if (file.tell() == df_filesize): print ('\n  File was read till the end')
            # if (file.tell() < df_filesize):  print ('\n  File was NOT read till the end!!! ERROR')

        # Here we close the data file
    ok = 1
    return ok, DAT_file_name, DAT_file_list


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    result_path = ''
    print_or_not = 1  # Print progress of data processing and figures making (1) or not (0)
    path_to_data = '/media/data/DATA/To_process/2021.05.31_GURT_Sun'
    MaxNim = 1024  # Number of data chunks for one figure
    RFImeanConst = 8  # Constant of RFI mitigation (usually 8)
    Vmin = -120  # Lower limit of figure dynamic range for initial spectra
    Vmax = -50  # Upper limit of figure dynamic range for initial spectra
    VminNorm = 0  # Lower limit of figure dynamic range for normalized spectra
    VmaxNorm = 10  # Upper limit of figure dynamic range for normalized spectra
    VminCorrMag = -150  # Lower limit of figure dynamic range for correlation magnitude spectra
    VmaxCorrMag = -30  # Upper limit of figure dynamic range for correlation magnitude spectra
    custom_dpi = 200  # Resolution of images of dynamic spectra
    colormap = 'jet'  # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
    CorrelationProcess = 1  # Process correlation data or save time?  (1 = process, 0 = save)
    DynSpecSaveInitial = 0  # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
    DynSpecSaveCleaned = 1  # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
    CorrSpecSaveInitial = 0  # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
    CorrSpecSaveCleaned = 1  # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
    SpectrumFileSaveSwitch = 0  # Save 1 immediate spectrum to TXT file? (1 = yes, 0 = no)
    ImmediateSpNo = 1  # Number of immediate spectrum to save to TXT file
    where_save_pics = 1  # Where to save result pictures? (0 - to script folder, 1 - to data folder)

    Sum_Diff_Calculate = 0
    longFileSaveAch = 1
    longFileSaveBch = 1
    longFileSaveCMP = 1
    longFileSaveCRI = 1
    longFileSaveSSD = 0

    done_or_not, DAT_file_name, DAT_file_list = ADR_file_reader(path_to_data, result_path, MaxNim, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
            VminCorrMag, VmaxCorrMag, custom_dpi, colormap, CorrelationProcess, Sum_Diff_Calculate,
            longFileSaveAch, longFileSaveBch, longFileSaveCMP, longFileSaveCRI, longFileSaveSSD,
            DynSpecSaveInitial, DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned,
            SpectrumFileSaveSwitch, ImmediateSpNo, print_or_not)
