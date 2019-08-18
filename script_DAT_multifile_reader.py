# Python3
Software_version = '2019.08.14'  # !!! Not finished !!!
Software_name = 'DAT multifile data reader'
# Program intended to read and show data from DAT files
import os
#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
path_to_data = 'DATA_for_DAT_reader_development/'  # '/media/data/PYTHON/ra_data_processing-all/'

# Path to intermediate data files and results
path_to_results = os.path.dirname(os.path.realpath(__file__)) + '/'  # 'd:/PYTHON/ra_data_processing-all/' # 'DATA/'

# Types of data to get
typesOfData = ['chA', 'chB', 'C_m', 'C_p', 'CRe', 'CIm', 'A+B', 'A-B'] # !-!
#typesOfData = ['CRe', 'CIm']

# List of frequencies to build intensity changes vs. time and save to TXT file:
#freqList = [10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,75.0]
#freqList = [9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
freqList = [4.0,5.0,6.0,7.0,8.0,8.05,8.1,8.15,8.5,9.0]

averOrMin = 0                    # Use average value (0) per data block or minimum value (1)
StartStopSwitch = 0              # Read the whole file (0) or specified time limits (1)
SpecFreqRange = 0                # Specify particular frequency range (1) or whole range (0)
VminMan = -120                   # Manual lower limit of immediate spectrum figure color range
VmaxMan = -10                    # Manual upper limit of immediate spectrum figure color range
VminNormMan = 0                  # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
VmaxNormMan = 18                 # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
RFImeanConst = 6                 # Constant of RFI mitigation (usually = 8)
customDPI = 300                  # Resolution of images of dynamic spectra
colormap = 'jet'                 # Colormap of images of dynamic spectra ('jet' or 'Greys')
ChannelSaveTXT = 0               # Save intensities at specified frequencies to TXT file
ChannelSavePNG = 0               # Save intensities at specified frequencies to PNG file
ListOrAllFreq = 0                # Take all frequencies of a list to save TXT and PNG? 1-All, 0-List
AmplitudeReIm = 200000 * 10**(-12) # Color range of Re and Im dynamic spectra
                                 # 10 * 10**(-12) is typical value enough for CasA for interferometer of 2 GURT subarrays

# Begin and end frequency of dynamic spectrum (MHz)
freqStart = 0.0
freqStop = 10.0

# Begin and end time of dynamic spectrum ('yyyy-mm-dd hh:mm:ss')
dateTimeStart = '2019-07-19 00:00:00'
dateTimeStop =  '2019-07-23 04:00:00'

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
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.file_header_ADR import FileHeaderReaderADR
from package_ra_data_files_formats.file_header_JDS import FileHeaderReaderJDS

################################################################################

#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************
print ('\n\n\n\n\n\n\n\n   ****************************************************')
print ('   *   ', Software_name, '  v.', Software_version,'    *      (c) YeS 2019')
print ('   **************************************************** \n\n\n')

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

print(' * Number of datasets found: ', len(timeline_file_name_list), '\n')

# Loop by data types selected by user
for file_no in range (len(data_files_name_list)):
    print('   Dataset No: ', file_no + 1, ' of ', len(timeline_file_name_list), '\n')
    dat_types_list = []
    for type_of_data in range(len(typesOfData)):
            name = data_files_name_list[file_no] + '_Data_' + typesOfData[type_of_data] + '.dat'
            if os.path.isfile(path_to_data + name):
                dat_types_list.append(typesOfData[type_of_data])


    done_or_not = DAT_file_reader(path_to_data, data_files_name_list[file_no], dat_types_list, data_files_name_list[file_no] , averOrMin,
                        StartStopSwitch, SpecFreqRange, VminMan, VmaxMan, VminNormMan, VmaxNormMan,
                        RFImeanConst, customDPI, colormap, ChannelSaveTXT, ChannelSavePNG, ListOrAllFreq,
                        AmplitudeReIm, freqStart, freqStop, dateTimeStart, dateTimeStop, freqStartTXT,
                        freqStopTXT, freqList, 0)




endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program ', Software_name, ' has finished! *** \n\n\n')
