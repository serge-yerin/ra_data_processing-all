# !!! Does not work !!!!


# A program to convert ADR files to DAT files
# **************************************************************************

import tkinter as tk
from tkinter import *
import tkinter.filedialog
import os
import sys
from os import path
import struct
import math
import threading
import time
import numpy as np
import datetime
from datetime import datetime, timedelta

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# **************************************************************************

global source_dir_name, result_dir_name, root_window, start_btn, source_btn, result_btn

# Setting of main window     
root_window = Tk()
root_window.title("ADR to DAT converter (YeS 2018)")

# Setting of main frame
mainframe = Frame(root_window, height=250, width=500)
mainframe.pack()

start_btn = Button(mainframe, text="Begin conversion")

# **************************************************************************


def Chose_source_dir(ev):
    global root_window, source_dir_name
    directory = tkinter.filedialog.askdirectory()
    entry_source_dir.delete(0, END)
    entry_source_dir.insert(0, directory)
    source_dir_name = directory
    source_btn.config(relief=RAISED)
    root_window.update_idletasks()


def Chose_result_dir(ev):
    global root_window, source_dir_name
    directory = tkinter.filedialog.askdirectory()
    entry_result_dir.delete(0, END)
    entry_result_dir.insert(0, directory)
    # result_dir_name = directory
    result_btn.config(relief=RAISED)
    root_window.update_idletasks()
   

# *** FPGAtoPC Transforms FPGA array data format to ordinary PC numbers ***    
def FPGAtoPCarray (FPGAdata, NAvr):
    temp_float = np.uint32(FPGAdata)  
    temp = np.int64(FPGAdata)         
    A = np.int64(int('11111111111111111111111111000000', 2)) 
    temp_mantissa = np.int32(np.bitwise_and (temp, A))
    temp_mantissa = np.float32(temp_mantissa)/64
    B = np.uint32(int('00000000000000000000000000111111', 2))   
    temp_exponent = np.uint8(np.bitwise_and (temp_float, B))
    C0 = np.empty_like(temp_mantissa)
    C0 = np.uint64(C0)
    C0[:] = np.uint64(1)
    C1 = np.left_shift(C0, (temp_exponent+8))  # ! It must be "7" or "10" but "8" works for me
    C1 = np.float64(C1)
    PCdata = np.float64(temp_mantissa / C1 / NAvr)
    del A, B, C0, C1, temp_exponent
    return PCdata


def data_conversion(source, result):
    global root_window, start_btn, source_btn, result_btn
    label_process.config(text='Conversion in progress...', fg="Dark blue")
    start_btn.config(relief=SUNKEN)
    start_btn.config(state=tk.DISABLED)
    source_btn.config(state=tk.DISABLED)
    result_btn.config(state=tk.DISABLED)
    root_window.update_idletasks()
    
    directory = source 
    result_directory = result + '/' 
    max_chunks_per_image = 128                        # Number of data chunks to read at a time
    longFileA = 1                      # Save data A to long file? (1 = yes, 0 = no)
    longFileB = 1                      # Save data B to long file? (1 = yes, 0 = no)
    longFileC = 1                      # Save correlation data to long file? (1 = yes, 0 = no)
    CorrProcess = 1                    # Process correlation data or save time?  (1 = process, 0 = save)
    
    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")
    
    # *** Creating a TXT logfile ***
    Log_File = open(result_directory + "Log.txt", "w")
    Log_File.write('\n\n    ****************************************************\n')
    Log_File.write('    *          ADR to DAT converter  v2.0 LOG          *      (c) YeS 2018\n')
    Log_File.write('    ****************************************************\n\n')
    Log_File.write('  Date of data processing: %s   \n' % currentDate)
    Log_File.write('  Time of data processing: %s \n\n' % currentTime)
    
    # *** Search ADR files in the directory ***
    fileList = []
    i = 0
    Log_File.write('  Directory: %s \n' %directory )
    Log_File.write('  List of files to be analyzed: \n')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.adr'):
                i = i + 1
                Log_File.write('           '+str(i)+') %s \n' %file )
                fileList.append(str(os.path.join(root, file)))
    Log_File.close()
    
    if len(fileList) < 1:
        label_process.config(text='Error! Check directories.', fg="Red")
        start_btn.config(relief=RAISED)
        start_btn.config(state=tk.ACTIVE)
        source_btn.config(state=tk.ACTIVE)
        result_btn.config(state=tk.ACTIVE)
        Log_File.close()
        return
        
    for file_no in range(len(fileList)):   # loop by files
        Log_File = open(result_directory + "Log.txt", "a")
        Log_File.write('\n\n\n  * File '+str(file_no+1)+' of %s \n' % str(len(fileList)))
        Log_File.write('  * File path: %s \n\n\n' % str(fileList[file_no]))
        
        # *** Opening datafile ***
        fname = ''
        if len(fname) < 1:
            fname = fileList[file_no]
        file = open(fname, 'rb')
       
        # reading FHEADER
        df_filesize = (os.stat(fname).st_size)  # Size of file
        df_filename = file.read(32).decode('utf-8').rstrip('\x00')
        df_creation_timeLOC = file.read(24).decode('utf-8').rstrip('\x00')  # Creation time in local time
        temp = file.read(8)
        df_creation_timeUTC = file.read(32).decode('utf-8').rstrip('\x00')  # Creation time in UTC time
        df_system_name = file.read(32).decode('utf-8').rstrip('\x00')  # System (receiver) name
        df_obs_place = file.read(128).decode('utf-8').rstrip('\x00')  # place of observations
        df_description = file.read(256).decode('utf-8').rstrip('\x00')  # File description

        # reading FHEADER PP ADRS_PAR
        ADRmode = struct.unpack('i', file.read(4))[0]
        FFT_Size = struct.unpack('i', file.read(4))[0]
        NAvr = struct.unpack('i', file.read(4))[0]
        SLine = struct.unpack('i', file.read(4))[0]
        Width = struct.unpack('i', file.read(4))[0]
        BlockSize = struct.unpack('i', file.read(4))[0]
        F_ADC = struct.unpack('i', file.read(4))[0]
    
        # FHEADER PP ADRS_OPT
        SizeOfStructure = struct.unpack('i', file.read(4))[0]   # the size of ADRS_OPT structure
        StartStop = struct.unpack('i', file.read(4))[0]         # starts/stops DSP data processing
        StartSec = struct.unpack('i', file.read(4))[0];         # UTC abs.time.sec - processing starts
        StopSec = struct.unpack('i', file.read(4))[0];          # UTC abs.time.sec - processing stops
        Testmode = struct.unpack('i', file.read(4))[0];         
        NormCoeff1 = struct.unpack('i', file.read(4))[0];       # Normalization coefficient 1-CH: 1 ... 65535 (k = n / 8192), 1 < n < 65536
        NormCoeff2 = struct.unpack('i', file.read(4))[0];       # Normalization coefficient 2-CH: 1 ... 65535 (k = n / 8192), 1 < n < 65536
        Delay = struct.unpack('i', file.read(4))[0];            # Delay in picoseconds	-1000000000 ... 1000000000
        temp = struct.unpack('i', file.read(4))[0];
        ADRSoptions = bin(temp) 
    
        Log_File.write(' Initial data file name:         %s \n' % df_filename)
        Log_File.write(' File size:                      %s Mb \n' % str(df_filesize/1024/1024))
        Log_File.write(' Creation time in local time:    %s \n' % str(df_creation_timeLOC))
        Log_File.write(' Creation time in UTC time:      %s \n' % str(df_creation_timeUTC))
        Log_File.write(' System (receiver) name:         %s \n' % df_system_name)
        Log_File.write(' Place of observations:          %s \n' % df_obs_place)
        Log_File.write(' File description:               %s \n' % df_description)
        Log_File.write(' FFT size:                       %s \n' % FFT_Size)
        Log_File.write(' Averaged spectra:               %s \n' % NAvr)
        Log_File.write(' Clock frequency:                %s MHz \n' % str(F_ADC*10**-6))
        Log_File.close()
        
        # TimeRes = NAvr * (16384. / F_ADC)
        df = F_ADC / FFT_Size                                
        
        file.seek(1024)
        
        # *** DSP_INF reading ***
        temp = file.read(4)         # 
        size_of_chunk = struct.unpack('i', file.read(4))[0]
        frm_size = struct.unpack('i', file.read(4))[0]
        frm_count = struct.unpack('i', file.read(4))[0]
        frm_sec = struct.unpack('i', file.read(4))[0]
        frm_phase = struct.unpack('i', file.read(4))[0]
        AligningDSPINFtag = file.read(4072)
        
        # *** Setting the time reference (file beginning) ***
        TimeFirstFramePhase = float(frm_phase)/F_ADC
        TimeFirstFrameFloatSec = frm_sec + TimeFirstFramePhase
        TimeScaleStartTime = datetime(int('20' + df_filename[1:3]), int(df_filename[3:5]), int(df_filename[5:7]),
                                      int(df_creation_timeUTC[0:2]), int(df_creation_timeUTC[3:5]),
                                      int(df_creation_timeUTC[6:8]), int(df_creation_timeUTC[9:12])*1000)
            
        sp_in_frame = int(frm_size / BlockSize)
        frames_in_chunk = int(size_of_chunk / frm_size)
        chunks_in_file = int((df_filesize - 1024) / (size_of_chunk+8))
        freq_points_num = int(Width * 1024)                # Number of frequency points in specter
        
        indexes = []
        # bundle_dir = sys._MEIPASS
        # ifname = bundle_dir + '\\fft\\' + str(FFT_Size) + '.fft'
        ifname = 'package_ra_data_files_formats/' + str(FFT_Size) + '.fft'
        indexfile = open(ifname, 'r')
        num = 0
        for line in indexfile:
            ind = int(line)
            if (ind >= SLine*1024) & (ind < ((SLine + Width) * 1024)):
                indexes.append(ind - SLine*1024)
            num = num + 1
        indexfile.close()
    
        # *** Frequency calculation (in MHz) ***
        f0 = SLine * 1024 * df
        frequency = np.zeros(freq_points_num)
        for i in range(0, freq_points_num):
            frequency[i] = (f0 + (i * df)) * (10**-6)    
            
        timeLineSecond = np.zeros(chunks_in_file)  # List of second values from DSP_INF field
    
        # *** If it is the first file - write the header to long data file
        if(longFileA == 1 or longFileB == 1 or longFileC == 1) and file_no == 0:
            file.seek(0)
            file_header = file.read(1024)
    
            # *** Creating a name for long timeline TXT file ***
            TLfile_name = result_directory + df_filename + '_Timeline.txt'
            TLfile = open(TLfile_name, 'wb')  # Open and close to delete the file with the same name
            TLfile.close()
    
            # *** Creating a binary file with data for long data storage ***
            if longFileA == 1 and (ADRmode == 3 or ADRmode == 5 or ADRmode == 6): 
                Data_A_name = result_directory+df_filename+'_Data_chA.dat'
                Data_A = open(Data_A_name, 'wb')
                Data_A.write(file_header)
                Data_A.close()
            if longFileB == 1 and (ADRmode == 4 or ADRmode == 5 or ADRmode == 6): 
                Data_B_name = result_directory+df_filename + '_Data_chB.dat'
                Data_B = open(Data_B_name, 'wb')
                Data_B.write(file_header)
                Data_B.close()
            if longFileC == 1 and ADRmode == 6: 
                Data_CRe_name = result_directory+df_filename + '_Data_CRe.dat'
                Data_CRe = open(Data_CRe_name, 'wb')
                Data_CRe.write(file_header)
                Data_CRe.close()
                Data_CIm_name = result_directory+df_filename + '_Data_CIm.dat'
                Data_CIm = open(Data_CIm_name, 'wb')
                Data_CIm.write(file_header)
                Data_CIm.close()
            del file_header
            
        #  * D A T A    R E A D I N G *
        
        file.seek(1024)  # Jumping to 1024 byte from file beginning
        if ADRmode > 2 and ADRmode < 7:           # Specter modes
            figID = -1
            figMAX = int(math.ceil((chunks_in_file)/max_chunks_per_image))+1
            if figMAX < 1: 
                figMAX = 1
            for fig in range(figMAX):
                figID = figID + 1
                if (chunks_in_file - max_chunks_per_image * figID) < max_chunks_per_image:
                    Nim = int(chunks_in_file - max_chunks_per_image * figID)
                else:
                    Nim = max_chunks_per_image
                    
                spectra_num = int(Nim * sp_in_frame * frames_in_chunk)  # Number of spectra in the figure
                
                # *** Preparing empty matrices ***
                if ADRmode == 3 or ADRmode == 5 or ADRmode == 6:
                    FPGAdataRawA = np.zeros((spectra_num, freq_points_num))
                    FPGAdata_ChA = np.zeros((spectra_num, freq_points_num))
                    DSPdata_Ch_A = np.zeros((spectra_num, freq_points_num))
                if ADRmode == 4 or ADRmode == 5 or ADRmode == 6:
                    FPGAdataRawB = np.zeros((spectra_num, freq_points_num))
                    FPGAdata_ChB = np.zeros((spectra_num, freq_points_num))
                    DSPdata_Ch_B = np.zeros((spectra_num, freq_points_num))
                if ADRmode == 6:
                    FPGAdataRawCRe = np.zeros((spectra_num, freq_points_num))
                    FPGAdataRawCIm = np.zeros((spectra_num, freq_points_num))
                    FPGAdata_CIm = np.zeros((spectra_num, freq_points_num))
                    FPGAdata_CRe = np.zeros((spectra_num, freq_points_num))
                    DSPdata_CIm = np.zeros((spectra_num, freq_points_num))
                    DSPdata_CRe = np.zeros((spectra_num, freq_points_num))
                
                TimeScale = []
                TimeFigureScale = []  # Timelime (new) for each figure
                TimeFigureStartTime = datetime(2016, 1, 1, 0, 0, 0, 0)
    
                # Reading and reshaping all data with readers
                raw = np.fromfile(file, dtype='i4', count=int((Nim * (size_of_chunk+8))/4))
                raw = np.reshape(raw, [int((size_of_chunk+8)/4), Nim], order='F')
                
                # Splitting headers from data
                headers = raw[0:1024, :]
                data = raw[1024:, :]
                
                # Arranging data in right order
                if ADRmode == 3:
                    data = np.reshape(data, [freq_points_num, Nim * frames_in_chunk * sp_in_frame], order='F')
                    FPGAdataRawA = data[0:freq_points_num:1, :].transpose()
                if ADRmode == 4:
                    data = np.reshape(data, [freq_points_num, Nim * frames_in_chunk * sp_in_frame], order='F')
                    FPGAdataRawB = data[0:freq_points_num:1, :].transpose()
                if ADRmode == 5:
                    data = np.reshape(data, [freq_points_num * 2, Nim * frames_in_chunk * sp_in_frame], order='F')
                    FPGAdataRawB = data[0:(freq_points_num*2):2, :].transpose()
                    FPGAdataRawA = data[1:(freq_points_num*2):2, :].transpose()
                if (ADRmode == 6):
                    data = np.reshape(data, [freq_points_num * 4, Nim * frames_in_chunk * sp_in_frame], order='F')
                    FPGAdataRawCIm = data[0:(freq_points_num*4):4, :].transpose()
                    FPGAdataRawCRe = data[1:(freq_points_num*4):4, :].transpose()
                    FPGAdataRawB   = data[2:(freq_points_num*4):4, :].transpose()
                    FPGAdataRawA   = data[3:(freq_points_num*4):4, :].transpose()
                
                # *** TimeLine calculations ***
                for i in range(Nim):
    
                    frm_sec = headers[4][i]
                    frm_phase = headers[5][i]
                        
                    # * Abosolute time calculation *
                    timeLineSecond[figID*max_chunks_per_image+i] = frm_sec # to check the linearity of seconds
                    TimeCurrentFramePhase = float(frm_phase)/F_ADC
                    TimeCurrentFrameFloatSec = frm_sec + TimeCurrentFramePhase
                    TimeSecondDiff = TimeCurrentFrameFloatSec - TimeFirstFrameFloatSec
                    TimeAdd = timedelta(0, int(np.fix(TimeSecondDiff)), int(np.fix((TimeSecondDiff - int(np.fix(TimeSecondDiff)))*1000000)))
                    
                    # Adding of time point to time line is in loop by spectra because
                    # for each spectra in frame there is one time point but it should 
                    # appear for all spectra to fit the dimensions of arrays
                    
                    # * Time from figure start calculation *
                    if i == 0:
                        TimeFigureStart = TimeCurrentFrameFloatSec
                    TimeFigureSecondDiff = TimeCurrentFrameFloatSec - TimeFigureStart
                    TimeFigureAdd = timedelta(0, int(np.fix(TimeFigureSecondDiff)), int(np.fix((TimeFigureSecondDiff - int(np.fix(TimeFigureSecondDiff)))*1000000)))
                    
                    for iframe in range(sp_in_frame):
                        TimeScale.append(str((TimeScaleStartTime + TimeAdd)))
                        TimeFigureScale.append(str((TimeFigureStartTime+TimeFigureAdd).time())) 
    
                # *** Performing index changes ***
                for i in range(freq_points_num):
                    n = indexes[i]
                    if ADRmode == 3 or ADRmode == 5 or ADRmode == 6:
                        FPGAdata_ChA[:,n] = FPGAdataRawA[:, i]
                    if ADRmode == 4 or ADRmode == 5 or ADRmode == 6:
                        FPGAdata_ChB[:,n] = FPGAdataRawB[:, i]
                    if ADRmode == 6 and CorrProcess == 1:
                        FPGAdata_CIm[:,n] = FPGAdataRawCIm[:, i]
                        FPGAdata_CRe[:,n] = FPGAdataRawCRe[:, i]
                
                # *** Converting from FPGA to PC float format ***
                if ADRmode == 3 or ADRmode == 5 or ADRmode == 6:
                    DSPdata_Ch_A = FPGAtoPCarray(FPGAdata_ChA, NAvr)
                
                if ADRmode == 4 or ADRmode == 5 or ADRmode == 6:
                    DSPdata_Ch_B = FPGAtoPCarray(FPGAdata_ChB, NAvr)
                
                if ADRmode == 6 and CorrProcess == 1:
                    DSPdata_CRe = FPGAtoPCarray(FPGAdata_CRe, NAvr)
                    DSPdata_CIm = FPGAtoPCarray(FPGAdata_CIm, NAvr)
            
                # *** Saving data to a long-term file ***
                if (ADRmode == 3 or ADRmode == 5 or ADRmode == 6) and longFileA == 1:
                    Data_A = open(Data_A_name, 'ab')
                    Data_A.write(DSPdata_Ch_A)
                    Data_A.close()
                if (ADRmode == 4 or ADRmode == 5 or ADRmode == 6) and longFileB == 1:
                    Data_B = open(Data_B_name, 'ab')
                    Data_B.write(DSPdata_Ch_B)
                    Data_B.close()
                if  ADRmode == 6 and longFileC == 1:
                    Data_CRe = open(Data_CRe_name, 'ab')
                    Data_CRe.write(DSPdata_CRe)
                    Data_CRe.close()
                    Data_CIm = open(Data_CIm_name, 'ab')
                    Data_CIm.write(DSPdata_CIm)
                    Data_CIm.close()
                    
                if longFileA == 1 or longFileB == 1 or longFileC == 1:
                    TLfile = open(TLfile_name, 'ab')
                    for i in range(sp_in_frame * frames_in_chunk * Nim):
                        TLfile.write(str(TimeScale[i][:])+' \n')
                    TLfile.close
            
        del timeLineSecond
        file.close()
        Log_File = open(result_directory + "Log.txt", "a")
        Log_File.write('\n  DONE \n')
        Log_File.close()
    Log_File.close()
    
    label_process.config(text=str('Conversion completed!'), fg = "Blue")
    start_btn.config(relief=RAISED)
    start_btn.config(state=tk.ACTIVE)
    source_btn.config(state=tk.ACTIVE)
    result_btn.config(state=tk.ACTIVE)

# **************************************************************************
#                       M A I N   P R O G R A M                            *
# **************************************************************************


# Show dynamic processing information 
label_process = Label(mainframe, fg="dark blue")
label_process.config(font=("Arial", 16))
label_process.place(x=20, y=170, width=450, height=30)

# Initial directories manes
source_dir_name = 'Not chosen'
result_dir_name = 'Not chosen'
#source_dir_name = 'E:/Scaner'
#result_dir_name = 'C:/Users/User/Desktop'
#source_dir_name = 'E:/Radioastronomical data/Different files'
#result_dir_name = 'E:/Radioastronomical data/Different files'

# Labels "Path" before text entry fields
label_path_in  = Label(mainframe, text="  Path:")
label_path_out = Label(mainframe, text="  Path:")
label_copyright = Label(mainframe, text="v.2018.01.25 (c) IRA NASU   Serge Yerin (YeS)   e-mail: yerin.serge@gmail.com")
label_copyright.config(font=("Arial", 8), fg="dark blue")

# Text entry fields to show directories paths
entry_source_dir = Entry(mainframe)
entry_source_dir.insert(END, source_dir_name)
entry_result_dir = Entry(mainframe)
entry_result_dir.insert(END, result_dir_name)

# Buttons for directories choosing
source_btn = Button(mainframe, text="Source directory")
result_btn = Button(mainframe, text="Result directory")

# Assigning directory choosing dialogs to buttons
source_btn.bind("<Button-1>",  Chose_source_dir)
result_btn.bind("<Button-1>",  Chose_result_dir)

# Button for conversion starting
start_btn = Button(mainframe, text = "Start conversion", command = lambda: threading.Thread(target = data_conversion(entry_source_dir.get(), entry_result_dir.get())).start())
#start_btn.bind("<Button-1>",  lambda: threading.Thread(target = data_conversion(entry_source_dir.get(), entry_result_dir.get())).start())

#start_btn = Button(mainframe, text = "Start conversion", command = t.start()) 

#start_btn = Button(mainframe, text = "Start conversion", command = lambda: start_conversion(entry_source_dir.get(), entry_result_dir.get())) 

# *** Placing of elements on the window frame ***
source_btn.place(x = 20, y = 20, width = 100, height = 30)
result_btn.place(x = 20, y = 60, width = 100, height = 30)

start_btn.place(x = 170, y = 120, width = 150, height = 30)

label_path_in.place (x = 140, y = 20, width = 30, height = 30)
label_path_out.place(x = 140, y = 60, width = 30, height = 30)
label_copyright.place(x = 100, y = 230, width = 400, height = 20)

entry_source_dir.place(x = 180, y = 20, width = 290, height = 30)
entry_result_dir.place(x = 180, y = 60, width = 290, height = 30)

root_window.mainloop()  # Main loop
    

