# Python3
Software_version = '2020.04.11'
Software_name = 'ADR control script'
# Script controls the ADR radio astronomy receiver
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
source_to_observe = 'Sun'
set_time_automatically = 0
host = '192.168.1.171'
port = 38386
control = 1

# Manual start and stop time ('yyyy-mm-dd hh:mm:ss')
date_time_start = '2020-04-11 23:35:30'
date_time_stop =  '2020-04-11 23:38:00'

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
#import socket
from datetime import datetime
import time
import sys
from os import path
#from threading import *

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
from package_receiver_control.f_connect_to_adr_receiver import f_connect_to_adr_receiver
from package_receiver_control.f_wait_predefined_time_connected import f_wait_predefined_time_connected

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

# Connect to the ADR receiver via socket
serversocket, input_parameters_str = f_connect_to_adr_receiver(host, port, control, 5)

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
'''

# Construct the name of data directory
data_directory_name = date_time_start[0:10].replace('-','.') + '_GURT_' + source_to_observe


# Print the current directory
#serversocket.send(('get prc/srv/ctl/pth\0').encode())    # read directory where data are stored
#data = f_read_adr_meassage(serversocket, 1)

# Prepare directory for data recording
print ('\n * Changing directory to:', data_directory_name)
serversocket.send(('set prc/srv/ctl/pth ' + data_directory_name + '\0').encode())    # set directory to store data
data = f_read_adr_meassage(serversocket, 0)
if data.startswith('SUCCESS'):
    print ('\n   Directory name changed successfully')


# Construct datetime variables to start and stop observations
dt_time_to_start_record = datetime(int(date_time_start[0:4]), int(date_time_start[5:7]), int(date_time_start[8:10]),
                            int(date_time_start[11:13]), int(date_time_start[14:16]), int(date_time_start[17:19]), 0)

dt_time_to_stop_record = datetime(int(date_time_stop[0:4]), int(date_time_stop[5:7]), int(date_time_stop[8:10]),
                            int(date_time_stop[11:13]), int(date_time_stop[14:16]), int(date_time_stop[17:19]), 0)

# Check if the start time is less then stop one!

# Waiting time to start record
print('\n * Waiting time to start recording...')
ok = f_wait_predefined_time_connected(dt_time_to_start_record, serversocket)
if not ok:
    print(' ERROR!')
    pass # !!!!

# Start record
print ('\n * Starting recording...')
serversocket.send('set prc/srv/ctl/srd 0 1\0'.encode())    # start data recording
data = f_read_adr_meassage(serversocket, 0)
if data.startswith('SUCCESS'):
    print ('\n   Recording started successfully')

# Waiting time to stop record
ok = f_wait_predefined_time_connected(dt_time_to_stop_record, serversocket)
if not ok:
    print(' ERROR!')
    pass # !!!!

# Stop record
print ('\n * Stopping recording...')
serversocket.send('set prc/srv/ctl/srd 0 0\0'.encode())    # stop data recording
data = f_read_adr_meassage(serversocket, 0)
if data.startswith('SUCCESS'):
    print ('\n   Recording stopped successfully')


print ('\n           *** Program ', Software_name, ' has finished! *** \n\n\n')


'''
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

get prc/dsp/ctl/mdo                     - get values for all sub-parameters from [mdo] group use the command:

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

