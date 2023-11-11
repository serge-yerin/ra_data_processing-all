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
observation_description = 'Test_observations'  # (do not use spaces, use underscores instead)

# Manual start and stop time ('yyyy-mm-dd hh:mm:ss')
date_time_start = '2020-05-21 16:25:00'
date_time_stop =  '2020-05-21 16:27:00'

dir_data_on_server = '/media/data/DATA/To_process/'  # data folder on server, please do not change!

# ADR PARAMETERS


# Rarely changes parameters:
port = 38386                    # Port of the receiver to connect (always 38386)
telegram_chat_id = '927534685'  # Telegram chat ID to send messages  - '927534685' - YeS
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
from datetime import datetime
from os import path
import time
import sys

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
from package_ra_data_files_formats.f_adr_file_read import adr_file_reader
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

# Check if the receiver is initialized, if it is not - initialize it
serversocket.send((b"set prc/srv/ctl/adr 3 1\0"))
data = f_read_adr_meassage(serversocket, 1)

if ('Failed!' in data or 'Stopped' in data):

    serversocket.send((b"set prc/dsp/net/dsa '192.168.10.204:48391'\0"))
    data = f_read_adr_meassage(serversocket, 1)
    serversocket.send((b"set prc/srv/ctl/adr 3 1\0"))
    data = f_read_adr_meassage(serversocket, 1)

'''
# Initialize ADR and set ADR parameters
f_initialize_adr(serversocket, receiver_ip, 1)

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


# Set observation description:
serversocket.send(('set prc/srv/ctl/dsc ' + observation_description + '\0').encode())
data = f_read_adr_meassage(serversocket, 0)


# Requesting and printing current ADR parameters
parameters_dict = f_get_adr_parameters(serversocket, 1)

#'''
print ('\n\n           *** Program ', Software_name, ' has finished! *** \n\n\n')

