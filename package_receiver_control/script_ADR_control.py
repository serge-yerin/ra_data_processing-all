# Python3
Software_version = '2020.04.19'
Software_name = 'ADR control script'
# Script controls the ADR radio astronomy receiver
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
source_to_observe = 'Sun'       # Name of source to observe (used for folder name construction)
receiver_ip = '10.0.12.172'     # Receiver IP address in local network '192.168.1.171'
time_server = '10.0.12.57'      # '192.168.1.150'
copy_data = 1                   # Copy data from receiver?
process_data = 1                # Process data copied from receiver?

# Manual start and stop time ('yyyy-mm-dd hh:mm:ss')
date_time_start = '2020-05-20 15:59:00'
date_time_stop =  '2020-05-20 16:00:00'

dir_data_on_server = '/media/data/DATA/To_process/'  # data folder on server, please do not change!

# PROCESSING PARAMETERS
MaxNim = 1024                 # Number of data chunks for one figure
RFImeanConst = 8              # Constant of RFI mitigation (usually 8)
Vmin = -120                   # Lower limit of figure dynamic range for initial spectra
Vmax = -50                    # Upper limit of figure dynamic range for initial spectra
VminNorm = 0                  # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 10                 # Upper limit of figure dynamic range for normalized spectra
VminCorrMag = -150            # Lower limit of figure dynamic range for correlation magnitude spectra
VmaxCorrMag = -30             # Upper limit of figure dynamic range for correlation magnitude spectra
customDPI = 200               # Resolution of images of dynamic spectra
colormap = 'jet'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
CorrelationProcess = 0        # Process correlation data or save time?  (1 = process, 0 = save)
DynSpecSaveInitial = 0        # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 1        # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 0       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
SpecterFileSaveSwitch = 1     # Save 1 immediate specter to TXT file? (1 = yes, 0 = no)
ImmediateSpNo = 1             # Number of immediate specter to save to TXT file
where_save_pics = 0           # Where to save result pictures? (0 - to script folder, 1 - to data folder)

averOrMin = 0                    # Use average value (0) per data block or minimum value (1)
VminMan = -120                   # Manual lower limit of immediate spectrum figure color range
VmaxMan = -10                    # Manual upper limit of immediate spectrum figure color range
VminNormMan = 0                  # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
VmaxNormMan = 12                 # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
AmplitudeReIm = 1 * 10**(-12)    # Color range of Re and Im dynamic spectra
                                 # 10 * 10**(-12) is typical value enough for CasA for interferometer of 2 GURT subarrays

# Rarely changes parameters:
port = 38386                    # Port of the receiver to connect (always 38386)
telegram_chat_id = '927534685'  # Telegram chat ID to send messages  - '927534685' - YeS
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
from datetime import datetime
from pexpect import pxssh
from os import path
import time
import sys
import os

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
from package_receiver_control.f_connect_to_adr_receiver import f_connect_to_adr_receiver
from package_receiver_control.f_wait_predefined_time_connected import f_wait_predefined_time_connected
from package_receiver_control.f_get_adr_parameters import f_get_adr_parameters
from package_receiver_control.f_synchronize_adr import f_synchronize_adr
from package_receiver_control.f_initialize_adr import f_initialize_adr
from package_receiver_control.f_set_adr_parameters import f_set_adr_parameters
from package_receiver_control.f_copy_data_from_adr import f_copy_data_from_adr
from package_common_modules.find_and_check_files_in_current_folder import find_and_check_files_in_current_folder
from package_common_modules.telegram_bot_sendtext import telegram_bot_sendtext
from package_ra_data_files_formats.ADR_file_reader import ADR_file_reader
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader

# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************
print ('\n\n\n\n\n\n\n\n   *********************************************************************')
print ('   *              ', Software_name, '  v.', Software_version,'                 *      (c) YeS 2020')
print ('   ********************************************************************* \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('   Today is ', currentDate, ' time is ', currentTime, '\n')

# process only copied from receiver data
if process_data > 0: copy_data = 1

# Connect to the ADR receiver via socket
serversocket, input_parameters_str = f_connect_to_adr_receiver(receiver_ip, port, 1, 1)  # 1 - control, 1 - delay in sec

# Initialize ADR and set ADR parameters
f_initialize_adr(serversocket, 1)

# Set initial ADR parameters
f_set_adr_parameters(serversocket, 1)

# Update synchronization of PC and ADR
f_synchronize_adr(serversocket, receiver_ip, time_server)

# Construct the name of data directory
data_directory_name = date_time_start[0:10].replace('-','.') + '_GURT_' + source_to_observe

# Prepare directory for data recording
serversocket.send(('set prc/srv/ctl/pth ' + data_directory_name + '\0').encode())    # set directory to store data
data = f_read_adr_meassage(serversocket, 0)
if data.startswith('SUCCESS'):
    print ('\n * Directory name changed to: ', data_directory_name)

# Requesting and printing current ADR parameters
parameters_dict = f_get_adr_parameters(serversocket, 1)

# Construct datetime variables to start and stop observations
dt_time_to_start_record = datetime(int(date_time_start[0:4]), int(date_time_start[5:7]), int(date_time_start[8:10]),
                            int(date_time_start[11:13]), int(date_time_start[14:16]), int(date_time_start[17:19]), 0)

dt_time_to_stop_record = datetime(int(date_time_stop[0:4]), int(date_time_stop[5:7]), int(date_time_stop[8:10]),
                            int(date_time_stop[11:13]), int(date_time_stop[14:16]), int(date_time_stop[17:19]), 0)

# Check the correctness of start and stop time
if (dt_time_to_start_record < dt_time_to_stop_record) and (dt_time_to_start_record > datetime.now()):
    print('\n   ******************************************\n   Recording start time: ', date_time_start)
    print('\n   Recording stop time:  ', date_time_stop,'\n   ******************************************')
else:
    sys.exit('\n\n * ERROR! Time limits are wrong!!! \n\n')


# Waiting time to start record
print('\n * Waiting time to synchronize and start recording...')
ok = f_wait_predefined_time_connected(dt_time_to_start_record, serversocket, 1, receiver_ip, time_server)

# Start record
serversocket.send('set prc/srv/ctl/srd 0 1\0'.encode())    # start data recording
data = f_read_adr_meassage(serversocket, 0)
if data.startswith('SUCCESS'):
    print ('\n * Recording started')

# Waiting time to stop record
ok = f_wait_predefined_time_connected(dt_time_to_stop_record, serversocket, 0, receiver_ip, time_server)

# Stop record
serversocket.send('set prc/srv/ctl/srd 0 0\0'.encode())    # stop data recording
data = f_read_adr_meassage(serversocket, 0)
if data.startswith('SUCCESS'):
    print ('\n * Recording stopped')


# Sending message to Telegram
message = 'GURT ' + data_directory_name.replace('_',' ') + ' observations completed!\nStart time: '\
            +date_time_start + '\nStop time: '+date_time_stop + \
            '\nReceiver: '+ parameters_dict["receiver_name"].replace('_',' ') + \
            '\nDescription: ' + parameters_dict["file_description"].replace('_',' ') + \
            '\nMode: ' + parameters_dict["operation_mode_str"] + \
            '\nTime resolution: ' + str(round(parameters_dict["time_resolution"], 3)) + ' s.' + \
            '\nFrequency resolution: ' + str(round(parameters_dict["frequency_resolution"] / 1000, 3)) + ' kHz.' + \
            '\nFrequency range: ' + str(round(parameters_dict["lowest_frequency"] / 1000000, 3)) + ' - ' + \
            str(round(parameters_dict["highest_frequency"] / 1000000, 3)) + ' MHz'
if process_data > 0:
    message = message + '\nData will be copied to GURT server and processed.'
try:
    test = telegram_bot_sendtext(telegram_chat_id, message)
except:
    pass


# Data copying and processing

if copy_data > 0:
    time.sleep(1)
    ok = f_copy_data_from_adr(receiver_ip, data_directory_name, dir_data_on_server, 0)

if process_data > 0:

    time.sleep(1)

    # Processing data with ADR reader and DAT reader

    # Find all files in folder once more:
    file_name_list_current = find_and_check_files_in_current_folder(dir_data_on_server + data_directory_name + '/', '.adr')
    file_name_list_current.sort()

    print('\n\n * ADR reader analyses data... \n')

    # Making a name of folder for storing the result figures and txt files
    result_path = dir_data_on_server + data_directory_name + '/' + 'ADR_Results_' + data_directory_name

    for file in range(len(file_name_list_current)):
        file_name_list_current[file] = dir_data_on_server + data_directory_name + '/' + file_name_list_current[file]

    # Run ADR reader for the current folder
    ok, DAT_file_name, DAT_file_list = ADR_file_reader(file_name_list_current, result_path, MaxNim,
                                                                RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                                                                VminCorrMag, VmaxCorrMag, customDPI, colormap,
                                                                CorrelationProcess, 0, 1, 1, 1, 1, 0,
                                                                DynSpecSaveInitial, DynSpecSaveCleaned, CorrSpecSaveInitial,
                                                                CorrSpecSaveCleaned,
                                                                SpecterFileSaveSwitch, ImmediateSpNo, 0)

    print('\n * DAT reader analyzes file:', DAT_file_name, ', of types:', DAT_file_list, '\n')

    result_path = dir_data_on_server + data_directory_name + '/'

    # Run DAT reader for the results of current folder
    ok = DAT_file_reader('' , DAT_file_name, DAT_file_list, result_path, data_directory_name,
                                  averOrMin, 0, 0, VminMan, VmaxMan, VminNormMan, VmaxNormMan,
                                  RFImeanConst, customDPI, colormap, 0, 0, 0, AmplitudeReIm, 0, 0, '', '', 0, 0, [], 0)

    # Sending message to Telegram
    message = 'Data of '+ data_directory_name.replace('_',' ') + ' observations ('+ parameters_dict["receiver_name"].replace('_',' ') +' receiver) were copied and processed.'
    try:
        test = telegram_bot_sendtext(telegram_chat_id, message)
    except:
        pass

print ('\n\n           *** Program ', Software_name, ' has finished! *** \n\n\n')


'''
*** Possible workflow ***
Read the source to observe
Read number of hours before and after culmination
Calculate culmination time
Calculate the time of start and stop of observations (or set manually)
Find the number of days to observe
In a loop:
    Make a folder to observe for the date and source
    Wait predefined time and check connection every minute
    Start observations on predefined time
    Wait predefined time and check connection every minute
    Stop observations on predefined time 


Connection terminates if control client has no any activity in 120 seconds

set prc/srv/ctl/srd 0 1     - to switch on the data recording
set prc/srv/ctl/srd 0 0     - to switch off the data recording

set prc/srv/ctl/srd 1 1     - to switch on the file autocreation option
set prc/srv/ctl/srd 1 0     - to switch off the file autocreation option

set prc/srv/ctl/srd 2 <FSIZE>   - defines the file size restriction to be set to FSIZE MB (FSIZE = -1 means no restrictions)

set prc/srv/ctl/pth <directory_name>    - set directory to store data
get prc/srv/ctl/pth

set prc/srv/ctl/sys <system_name>       - set the system (receiver) name
get prc/srv/ctl/sys                     - get the system (receiver) name

set prc/srv/ctl/plc <place_text>        - set text string defining the observation place
get prc/srv/ctl/plc                     - get text string defining the observation place

set prc/srv/ctl/adr 6 <0/1>             - To apply the ADR DSP options, defined in [opt]

get prc/dsp/ctl/opt                     - get values for all sub-parameters from [opt] group

set prc/dsp/ctl/opt 1 <0/1>             - On/Off the external source of ADC CLC.
get prc/dsp/ctl/opt 1

set prc/dsp/ctl/opt 3 <0/1>             - On/Off the “sum-difference” mode A±B, instead of A/B mode on CH-A and CH-B outputs.
get prc/dsp/ctl/opt 3

set prc/srv/ctl/adr 5 <0/1>             - to apply the ADR DSP settings, defined in [set]

set prc/dsp/ctl/set 5 <DDEL>            - Differential delay (DDEL) between CH-A and CH-B ADC sampling (CLC front) in picoseconds.
get prc/dsp/ctl/set 5

set prc/srv/ctl/adr 3 <0/1>             - to apply the ADR DSP parameters which is set in the [mdo]

get prc/dsp/ctl/mdo                     - get values for all sub-parameters from [mdo] group

set prc/dsp/ctl/mdo 0 <index>           - set ADR operation mode:
get prc/dsp/ctl/mdo 0

set prc/dsp/ctl/mdo 1 <SFFT>            - set SFFT from list: 2048,4096,8192,16384,32768
get prc/dsp/ctl/mdo 1

set prc/dsp/ctl/mdo 2 <NAVR>            - set number of averaged spectra, NAVR, in range: [16 … 32768]
get prc/dsp/ctl/mdo 2

set prc/dsp/ctl/mdo 3 <SLINE>           - set starting frequency line of frequency band in 1024-steps. SLINE in range [0 … (SFFT-1024)/1024]
get prc/dsp/ctl/mdo 3

set prc/dsp/ctl/mdo 4 <WIDTH>           - set width of frequency band in 1024-steps. WIDTH in range [1 … (SFFT-SLINE*1024)/1024].
get prc/dsp/ctl/mdo 4
'''

