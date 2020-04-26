# Python3
Software_version = '2020.04.26'
Software_name = 'ADR control by schedule'
# Script controls the ADR radio astronomy receiver according to schedule txt file
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
host = '192.168.1.171'          # Receiver IP address in local network
schedule_txt_file = 'Observations.txt'
dir_data_on_server = '/media/data/DATA/To_process/'  # data folder on server, please do not change!

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
from package_common_modules.telegram_bot_sendtext import telegram_bot_sendtext
from package_receiver_control.f_read_schedule_txt_for_adr import f_read_schedule_txt_for_adr
# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************
print ('\n\n\n\n\n\n\n\n   *********************************************************************')
print ('   *           ', Software_name, '  v.', Software_version,'              *      (c) YeS 2020')
print ('   ********************************************************************* \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('   Today is ', currentDate, ' time is ', currentTime, '\n')

# Read schedule
schedule = f_read_schedule_txt_for_adr(schedule_txt_file)

'''
Check correctness and recalculate the parameters to variables sent to ADR receiver
'''


# Connect to the ADR receiver via socket
serversocket, input_parameters_str = f_connect_to_adr_receiver(host, port, 1, 1)  # 1 - control, 1 - delay in sec

# Update synchronization of PC and ADR
f_synchronize_adr(serversocket, host)


for obs_no in range(len(schedule)):

    # Prepare directory for data recording
    data_directory_name = schedule[obs_no][6]
    serversocket.send(('set prc/srv/ctl/pth ' + data_directory_name + '\0').encode())    # set directory to store data
    data = f_read_adr_meassage(serversocket, 0)
    if data.startswith('SUCCESS'):
        print ('\n * Directory name changed to: ', data_directory_name)

    # Requesting and printing current ADR parameters
    parameters_dict = f_get_adr_parameters(serversocket, 1)

    # Construct datetime variables to start and stop observations
    dt_time = schedule[obs_no][0]
    dt_time_to_start_record = datetime(int(dt_time[0:4]), int(dt_time[5:7]), int(dt_time[8:10]),
                                int(dt_time[11:13]), int(dt_time[14:16]), int(dt_time[17:19]), 0)

    dt_time = schedule[obs_no][1]
    dt_time_to_stop_record = datetime(int(dt_time[0:4]), int(dt_time[5:7]), int(dt_time[8:10]),
                                int(dt_time[11:13]), int(dt_time[14:16]), int(dt_time[17:19]), 0)

    # Check the correctness of start and stop time
    if (dt_time_to_start_record < dt_time_to_stop_record) and (dt_time_to_start_record > datetime.now()):
        print('\n   ******************************************\n   Recording start time: ', schedule[obs_no][0])
        print('\n   Recording stop time:  ', schedule[obs_no][1],'\n   ******************************************')
    else:
        sys.exit('\n\n * ERROR! Time limits are wrong!!! \n\n')

    '''
    To apply other parameters set in schedule
    '''

    # Waiting time to start record
    print('\n * Waiting time to synchronize and start recording...')
    ok = f_wait_predefined_time_connected(dt_time_to_start_record, serversocket, 1, host)

    # Start record
    serversocket.send('set prc/srv/ctl/srd 0 1\0'.encode())    # start data recording
    data = f_read_adr_meassage(serversocket, 0)
    if data.startswith('SUCCESS'):
        print ('\n * Recording started')

    # Waiting time to stop record
    ok = f_wait_predefined_time_connected(dt_time_to_stop_record, serversocket)

    # Stop record
    serversocket.send('set prc/srv/ctl/srd 0 0\0'.encode())    # stop data recording
    data = f_read_adr_meassage(serversocket, 0)
    if data.startswith('SUCCESS'):
        print ('\n * Recording stopped')


    # Sending message to Telegram
    message = 'GURT ' + data_directory_name + ' observations completed!\nStart time: '+schedule[obs_no][0]\
              +'\nStop time: '+schedule[obs_no][1]
    try:
        test = telegram_bot_sendtext(telegram_chat_id, message)
    except:
        pass


print ('\n\n           *** Program ', Software_name, ' has finished! *** \n\n\n')

