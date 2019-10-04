# Python3
Software_version = '2019.10.04'  # !!! Not finished !!!
Software_name = 'DAT multifile data reader for CasA study long data'
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
typesOfData = ['CRe', 'CIm']

# List of frequencies to build intensity changes vs. time and save to TXT file:
#freqList_UTR2 = [12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0,21.0,22.0,23.0,24.0,25.0,26.0,27.0,28.0,29.0,30.0,31.0,32.0]
freqList_GURT = [12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0,21.0,22.0,23.0,24.0,25.0,26.0,27.0,28.0,29.0,30.0,31.0,32.0,33.0,34.0,35.0,36.0,37.0,38.0,39.0,40.0,41.0,42.0,43.0,44.0,45.0,46.0,47.0,48.0,49.0,50.0,51.0,52.0,53.0,54.0,55.0,56.0,57.0,58.0,59.0,60.0,61.0,62.0,63.0,64.0,65.0,66.0,67.0,68.0,69.0,70.0,71.0,72.0,73.0,74.0,75.0]


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
AmplitudeReIm = 20 * 10**(-12)  # Color range of Re and Im dynamic spectra
                                 # 10 * 10**(-12) is typical value enough for CasA for interferometer of 2 GURT subarrays
AmplitudeReIm_UTR2 = 20000 * 10**(-12)
AmplitudeReIm_GURT = 20 * 10**(-12)


# Begin and end frequency of dynamic spectrum (MHz)
freqStart = 0.0
freqStop = 10.0

# Begin and end time of dynamic spectrum ('yyyy-mm-dd hh:mm:ss')
#dateTimeStart = '2019-07-19 00:00:00'
#dateTimeStop =  '2019-07-23 04:00:00'


# Begin and end frequency of TXT files to save (MHz)
freqStartTXT = 8.0
freqStopTXT = 80.0

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
print ('\n\n\n\n\n\n\n\n   *************************************************************************')
print ('   *  ', Software_name, ' v.', Software_version,'  *  (c) YeS 2019')
print ('   ************************************************************************* \n\n\n')

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


# Loop by data types selected by user
print('\n Data files found: \n')
dat_files_list = []
for type_of_data in typesOfData:
    name = data_files_name_list[0] + '_Data_' + type_of_data + '.dat'
    print(' - ' + path_to_data + name)
    if os.path.isfile(path_to_data  + name):
        dat_files_list.append(name)


# *** Reading timeline file ***
name = path_to_data + timeline_file_name_list[0]
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


# *** Showing the time limits of file
print ('\n                                Start                         End \n')
print ('   File time limits:   ', dt_timeline[0],' ', dt_timeline[len(timeline)-1], '\n')


# Number of days in the file
dt_period = dt_timeline[0].date() - dt_timeline[-1].date()
no_of_days = int(abs(dt_period.days))


# Find culminations of both sources within timeline of the file and check the 1 hour gap before and after
culm_time_3C405 = []
culm_time_3C461 = []
print('\n * Calculations of culminations time for all days of observations... \n')
for day in range(2):  #(no_of_days+1):
    currentTime = time.strftime("%H:%M:%S")
    print (' Day # ', str(day+1), ' of ', str(no_of_days+1), '   started at: ', currentTime)

    date = str((Time(dt_timeline[0]) + TimeDelta(day * 86400, format = 'sec')))[0:10]
    culm_time = Time(culmination_time_utc('3C405', str(date), 0))
    if (culm_time > Time(dt_timeline[0]) + TimeDelta(3600, format = 'sec')) and (culm_time < Time(dt_timeline[-1]) - TimeDelta(3600, format = 'sec')):
        culm_time_3C405.append(culm_time)
    culm_time = Time(culmination_time_utc('3C461', str(date), 0))
    if (culm_time > Time(dt_timeline[0]) + TimeDelta(3600, format = 'sec')) and (culm_time < Time(dt_timeline[-1]) - TimeDelta(3600, format = 'sec')):
        culm_time_3C461.append(culm_time)

print('\n * Culminations number: '+ str(len(culm_time_3C405)) +' for 3C405 and '+str(len(culm_time_3C461))+' for 3C461 \n')


# In a loop take a two-hour fragments of data and make text files with responces
print('\n * Saving responces for each culmination of 3C405... ')
source = '3C405'
for i in range (len(culm_time_3C405)):
    currentTime = time.strftime("%H:%M:%S")
    print ('\n Culmination '+ str(culm_time_3C405[i]) +' # ', str(i+1), ' of ', str(len(culm_time_3C405)), '       started at: ', currentTime)


    start_time = culm_time_3C405[i] - TimeDelta(3600, format = 'sec')
    end_time  = culm_time_3C405[i] + TimeDelta(3600, format = 'sec')

    dateTimeStart = str(start_time)[0:19]
    dateTimeStop = str(end_time)[0:19]

    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
                CLCfrq, df_creation_timeUTC, ReceiverMode, Mode, sumDifMode,
                NAvr, TimeRes, fmin, fmax, df, frequency, FFTsize, SLine,
                Width, BlockSize] = FileHeaderReaderADR(path_to_data + dat_files_list[0], 0, 0)


    result_folder = data_files_name_list[0]+"_"+str(i+1)+'_of_'+str(len(culm_time_3C405))+'_'+source
    done_or_not = DAT_file_reader(path_to_data, data_files_name_list[0], typesOfData, result_folder,
                                averOrMin, StartStopSwitch, SpecFreqRange, VminMan, VmaxMan, VminNormMan, VmaxNormMan,
                                RFImeanConst, customDPI, colormap, ChannelSaveTXT, ChannelSavePNG, ListOrAllFreq,
                                AmplitudeReIm_GURT, freqStart, freqStop, dateTimeStart, dateTimeStop, freqStartTXT,
                                freqStopTXT, freqList_GURT, 0)

    # Saving TXT file with parameters from file header
    path = path_to_data + 'DAT_Results_' + result_folder + '/'
    TXT_file = open(path + data_files_name_list[0]+'_'+source + '_header.info', "w")
    TXT_file.write(' Observatory:           ' + df_obs_place + '\n')
    TXT_file.write(' Receiver:              ' + df_system_name + '\n')
    TXT_file.write(' Initial filename:      ' + df_filename + '\n')
    TXT_file.write(' Description:           ' + df_description + '\n')
    TXT_file.write(' Source for processing: ' + source + '\n')
    TXT_file.write(' Culmination time:      ' + str(culm_time_3C405[i]) + '\n')
    TXT_file.write(' Receiver mode:         ' + ReceiverMode + '\n')
    TXT_file.write(' Time resolution:       ' + str(np.round(TimeRes, 6)) + ' s \n')
    TXT_file.write(' Frequency range:       ' + str(fmin) + ' - ' + str(fmax)+ ' MHz \n')
    TXT_file.write(' Frequency resolution:  ' + str(np.round(df, )) + ' Hz \n')
    TXT_file.close()


# In a loop take a two-hour fragments of data and make text files with responces
print('\n * Saving responces for each culmination of 3C461... ')
source = '3C461'
for i in range (len(culm_time_3C461)):
    currentTime = time.strftime("%H:%M:%S")
    print ('\n Culmination '+ str(culm_time_3C461[i]) +' # ', str(i+1), ' of ', str(len(culm_time_3C461)), '       started at: ', currentTime)


    start_time = culm_time_3C461[i] - TimeDelta(3600, format = 'sec')
    end_time  = culm_time_3C461[i] + TimeDelta(3600, format = 'sec')

    dateTimeStart = str(start_time)[0:19]
    dateTimeStop = str(end_time)[0:19]

    [df_filename, df_filesize, df_system_name, df_obs_place, df_description,
                CLCfrq, df_creation_timeUTC, ReceiverMode, Mode, sumDifMode,
                NAvr, TimeRes, fmin, fmax, df, frequency, FFTsize, SLine,
                Width, BlockSize] = FileHeaderReaderADR(path_to_data + dat_files_list[0], 0, 0)


    result_folder = data_files_name_list[0]+"_"+str(i+1)+'_of_'+str(len(culm_time_3C461))+'_'+source
    done_or_not = DAT_file_reader(path_to_data, data_files_name_list[0], typesOfData, result_folder,
                                averOrMin, StartStopSwitch, SpecFreqRange, VminMan, VmaxMan, VminNormMan, VmaxNormMan,
                                RFImeanConst, customDPI, colormap, ChannelSaveTXT, ChannelSavePNG, ListOrAllFreq,
                                AmplitudeReIm_GURT, freqStart, freqStop, dateTimeStart, dateTimeStop, freqStartTXT,
                                freqStopTXT, freqList_GURT, 0)

    # Saving TXT file with parameters from file header
    path = path_to_data + 'DAT_Results_' + result_folder + '/'
    TXT_file = open(path + data_files_name_list[0]+'_'+source + '_header.info', "w")
    TXT_file.write(' Observatory:           ' + df_obs_place + '\n')
    TXT_file.write(' Receiver:              ' + df_system_name + '\n')
    TXT_file.write(' Initial filename:      ' + df_filename + '\n')
    TXT_file.write(' Description:           ' + df_description + '\n')
    TXT_file.write(' Source for processing: ' + source + '\n')
    TXT_file.write(' Culmination time:      ' + str(culm_time_3C461[i]) + '\n')
    TXT_file.write(' Receiver mode:         ' + ReceiverMode + '\n')
    TXT_file.write(' Time resolution:       ' + str(np.round(TimeRes, 6)) + ' s \n')
    TXT_file.write(' Frequency range:       ' + str(fmin) + ' - ' + str(fmax)+ ' MHz \n')
    TXT_file.write(' Frequency resolution:  ' + str(np.round(df, )) + ' Hz \n')
    TXT_file.close()



endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program ', Software_name, ' has finished! *** \n\n\n')
