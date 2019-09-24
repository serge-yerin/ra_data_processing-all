# Python3
Software_version = '2019.08.29'  # !!! Not finished !!!
Software_name = 'DAT multifile data reader for CasA study'
# Program intended to read and show data from DAT files
import os
#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
path_to_data = 'DATA/'  # '/media/data/PYTHON/ra_data_processing-all/'

# Path to intermediate data files and results
path_to_results = os.path.dirname(os.path.realpath(__file__)) + '/'  # 'd:/PYTHON/ra_data_processing-all/' # 'DATA/'

# Types of data to get
#typesOfData = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm', 'A+B', 'A-B'] # !-!
typesOfData = ['CRe', 'CIm']

# List of frequencies to build intensity changes vs. time and save to TXT file:
#freqList = [10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,75.0]
#freqList = [9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
freqList = [12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0]

averOrMin = 0                    # Use average value (0) per data block or minimum value (1)
StartStopSwitch = 1              # Read the whole file (0) or specified time limits (1)
AutoStartStop = 1                # 1 - calculte depending on source in comment, 0 - use manual values
AutoSourceSwitch = 1             # 1 - find sourcs in comment, 0 - use manually set source
SpecFreqRange = 0                # Specify particular frequency range (1) or whole range (0)
VminMan = -120                   # Manual lower limit of immediate spectrum figure color range
VmaxMan = -10                    # Manual upper limit of immediate spectrum figure color range
VminNormMan = 0                  # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
VmaxNormMan = 18                 # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
RFImeanConst = 6                 # Constant of RFI mitigation (usually = 8)
customDPI = 300                  # Resolution of images of dynamic spectra
colormap = 'jet'                 # Colormap of images of dynamic spectra ('jet' or 'Greys')
ChannelSaveTXT = 1               # Save intensities at specified frequencies to TXT file
ChannelSavePNG = 1               # Save intensities at specified frequencies to PNG file
ListOrAllFreq = 0                # Take all frequencies of a list to save TXT and PNG? 1-All, 0-List
AmplitudeReIm = 20000 * 10**(-12) # Color range of Re and Im dynamic spectra
                                 # 10 * 10**(-12) is typical value enough for CasA for interferometer of 2 GURT subarrays

# Begin and end frequency of dynamic spectrum (MHz)
freqStart = 0.0
freqStop = 10.0

# Begin and end time of dynamic spectrum ('yyyy-mm-dd hh:mm:ss')
dateTimeStart = '2019-07-19 00:00:00'
dateTimeStop =  '2019-07-23 04:00:00'

# Source to calculate culmination time (if AutoSourceSwitch = 0)
source = '3C405'

# Begin and end frequency of TXT files to save (MHz)
freqStartTXT = 0.0
freqStopTXT = 33.0

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
import numpy as np
import time
import sys
from datetime import datetime, timedelta
from astropy.time import Time, TimeDelta

# My functions
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.ADR_file_reader import ADR_file_reader
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS
from package_astronomy.culmination_time_utc import culmination_time_utc

################################################################################

#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************
print ('\n\n\n\n\n\n\n\n   *********************************************************************')
print ('   *    ', Software_name, '  v.', Software_version,'     *      (c) YeS 2019')
print ('   ********************************************************************* \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('   Today is ', currentDate, ' time is ', currentTime, '\n')


# Search needed files in the directory and subdirectories
file_name_list = find_files_only_in_current_folder(path_to_data, '.txt', 0)

# Find timeline files from TXT files
timeline_file_name_list = []
for i in range (len(file_name_list)):
    if file_name_list[i].endswith('_Timeline.txt'):
        timeline_file_name_list.append(file_name_list[i])

# Find original data file name from timeline file name
data_files_name_list = []
for i in range (len(timeline_file_name_list)):
    data_files_name_list.append(timeline_file_name_list[i][-31:-13])


# Checking and printing


# Loop by data types selected by user
for type_of_data in typesOfData:
    dat_files_list = []
    for i in range (len(data_files_name_list)):
        name = data_files_name_list[i] + '_Data_' + type_of_data + '.dat'
        if os.path.isfile(path_to_data  + name):
            dat_files_list.append(name)

    # Loop by DAT files
    for file_no in range (len(dat_files_list)):

        #  *** Find if the file is CasA of SygA ***
        file = open(path_to_data + dat_files_list[file_no], 'rb')

        # Check is it the file of ADR or JDS data
        df_filename = file.read(32).decode('utf-8').rstrip('\x00')      # Initial data file name
        file.close()

        if df_filename[-4:] == '.adr':

            [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
                    CLCfrq, df_creation_timeUTC, ReceiverMode, Mode, sumDifMode,
                    NAvr, TimeRes, fmin, fmax, df, frequency, FFTsize, SLine,
                    Width, BlockSize] = FileHeaderReaderADR(dat_files_list[file_no], 0, 0)

        if df_filename[-4:] == '.jds':     # If data obrained from DSPZ receiver

            [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
                    CLCfrq, df_creation_timeUTC, SpInFile, ReceiverMode, Mode, Navr, TimeRes, fmin, fmax,
                    df, frequency, FreqPointsNum, dataBlockSize] = FileHeaderReaderJDS(path_to_data + dat_files_list[file_no], 0, 0)

        if AutoSourceSwitch == 1:
            if ('3c461' in df_description.lower()) or ('cas' in df_description.lower()):
                source = '3C461'
            elif '3c405' in df_description.lower() or 'cyg' in df_description.lower():
                source = '3C405'
            else:
                print('  Source not detected !!!')
                source  = str(input(' * Enter source name like 3C405 or 3C461:    '))

        print('\n\n * File:            ', dat_files_list[file_no])
        if AutoSourceSwitch == 1: print('   Detected source: ', source, '\n   Description:     ', df_description)
        if AutoSourceSwitch == 0: print('   Manual source:   ', source, '\n   Description:     ', df_description)


        # Take the date of the file and find the culmination time of the source

        if AutoStartStop == 1:
            if df_filename[-4:] == '.jds':
                date = '20'+df_filename[5:7]+'-'+df_filename[3:5]+'-'+df_filename[1:3]
            if df_filename[-4:] == '.adr':
                date = '20'+df_filename[1:3]+'-'+df_filename[3:5]+'-'+df_filename[5:7]

            culm_time = culmination_time_utc(source, date, 0)

            culm_time = Time(culm_time)
            start_time = culm_time - TimeDelta(3600, format = 'sec')
            end_time  = culm_time + TimeDelta(3600, format = 'sec')


        # *** Reading timeline file ***
        name = path_to_data + data_files_name_list[file_no] + '_Timeline.txt'
        TLfile = open(name, 'r')
        timeline = []
        for line in TLfile:
            timeline.append(str(line))
        TLfile.close()

        # *** Converting text to ".datetime" format ***
        dt_timeline = []
        for i in range (len(timeline)):  # converting text to ".datetime" format

            # Check is the uS field is empty. If so it means it is equal to '000000'
            uSecond = timeline[i][20:26]
            if len(uSecond) < 2: uSecond = '000000'

            dt_timeline.append(datetime(int(timeline[i][0:4]), int(timeline[i][5:7]), int(timeline[i][8:10]), int(timeline[i][11:13]), int(timeline[i][14:16]), int(timeline[i][17:19]), int(uSecond)))


        if AutoStartStop == 0: # If switch is off - use manually set time and date
            start_time = datetime(int(dateTimeStart[0:4]), int(dateTimeStart[5:7]), int(dateTimeStart[8:10]), int(dateTimeStart[11:13]), int(dateTimeStart[14:16]), int(dateTimeStart[17:19]), 0)
            end_time = datetime(int(dateTimeStop[0:4]), int(dateTimeStop[5:7]), int(dateTimeStop[8:10]), int(dateTimeStop[11:13]), int(dateTimeStop[14:16]), int(dateTimeStop[17:19]), 0)

        # *** Showing the time limits of file and time limits of chosen part
        print ('\n                                Start                         End \n')
        print ('   File time limits:   ', dt_timeline[0],' ', dt_timeline[len(timeline)-1], '\n')
        print ('   Chosen time limits: ', start_time, '    ', end_time, '\n')

        # Verifying that chosen time limits are inside file and are correct
        if (dt_timeline[len(timeline)-1]>=start_time>dt_timeline[0]) and (dt_timeline[len(timeline)-1]>end_time>=dt_timeline[0]) and (end_time>start_time):
            print ('   Time is chosen correctly! \n\n')
        elif(dt_timeline[len(timeline)-1] >= start_time + TimeDelta(86400, format = 'sec') > dt_timeline[0]) and (dt_timeline[len(timeline)-1] > end_time + TimeDelta(86400, format = 'sec') >= dt_timeline[0]) and (end_time>start_time):
            start_time = start_time + TimeDelta(86400, format = 'sec')
            end_time = end_time + TimeDelta(86400, format = 'sec')
            print ('   Time is chosen correctly but adjusted for 1 day ahead! \n')
        else:
            print ('   ERROR! Culmination time is calculated chosen out of file limits!!! \n\n')
            sys.exit('           Program stopped! \n\n')

        #DAT_result_path = 'DAT_Results_' + data_files_name_list[file_no]
        if AutoStartStop == 1:
            dateTimeStart = str(start_time)[0:19]
            dateTimeStop = str(end_time)[0:19]


        done_or_not = DAT_file_reader(path_to_data, data_files_name_list[file_no], [type_of_data], data_files_name_list[file_no]+'_'+source,
                                averOrMin, StartStopSwitch, SpecFreqRange, VminMan, VmaxMan, VminNormMan, VmaxNormMan,
                                RFImeanConst, customDPI, colormap, ChannelSaveTXT, ChannelSavePNG, ListOrAllFreq,
                                AmplitudeReIm, freqStart, freqStop, dateTimeStart, dateTimeStop, freqStartTXT,
                                freqStopTXT, freqList, 0)
















endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program ', Software_name, ' has finished! *** \n\n\n')
