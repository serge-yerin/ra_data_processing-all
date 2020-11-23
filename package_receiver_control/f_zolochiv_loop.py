# Python3
# The script sends one command to run RT-32 observations an keep server connected (each 90 secs sends '\0')
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import sys
import time
import json
import socket
from os import path
from datetime import datetime
from time import gmtime, strftime

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# *******************************************************************************
#                              V A R I A B L E S                                *
# *******************************************************************************
run_file_path = 'rt32_run.json'
host = '192.168.14.20'
port = 1255

# *******************************************************************************
#                                F U N C T I O N S                              *
# *******************************************************************************
def read_output(serversocket):
    '''
    Reads the reply of the server to any command till the null-termination
    '''
    byte = b'a'
    message = bytearray([])
    byte = serversocket.recv(8)
    message.extend(byte)
    message = bytes(message).decode()
    print('\n Reply: ', message)
    return message

def print_obs_parameters(data):
    print('\n\n Observation parameters: \n')

    print(' Channels switch mode:          ', data['channels_switch_mode'])
    print(' Operating mode:                ', data['operating_mode'])
    print(' Observation name:              ', data['name'])
    print(' Source declination:            ', data['dec'])
    print(' Source right ascension:        ', data['ra'])
    print(' Date and time of start:        ', data['start_date'], ' ', data['start_time'])
    print(' Date and time of stop:         ', data['stop_date'], ' ', data['stop_time'])
    print(' Calibration schedule:          ', data['calibration_schedule'])
    print(' Frequency switching schedule:  ', data['frequency_switching_schedule'])
    print('\n Frequency ranges: ')
    print(' CFA:                           ', data['frequency_ranges']['cfa'])
    print(' CFB:                           ', data['frequency_ranges']['cfb'])
    print(' CFC:                           ', data['frequency_ranges']['cfc'])
    print(' CFD:                           ', data['frequency_ranges']['cfd'])
    print(' KFA:                           ', data['frequency_ranges']['kfa'])
    print(' KFB:                           ', data['frequency_ranges']['kfb'])
    print(' KFC:                           ', data['frequency_ranges']['kfc'])
    print(' KFD:                           ', data['frequency_ranges']['kfd'])
    print(' XFA:                           ', data['frequency_ranges']['xfa'])
    print(' XFB:                           ', data['frequency_ranges']['xfb'])
    print(' XFC:                           ', data['frequency_ranges']['xfc'])
    print(' XFD:                           ', data['frequency_ranges']['xfd'])


# *******************************************************************************
#                           M A I N     P R O G R A M                           *
# *******************************************************************************

check_files = True

#while check_files:
    # Read the file with run command

    #host, port, send_command = read_run_txt_file(run_file_path)

with open(run_file_path, "r") as read_file:
    data_json = json.load(read_file)

print_obs_parameters(data_json)


dt_time_to_start_record = datetime(int(data_json['start_date'][0:4]), int(data_json['start_date'][5:7]),
                                   int(data_json['start_date'][8:10]),
                                   int(data_json['start_time'][0:2]), int(data_json['start_time'][3:5]),
                                   int(data_json['start_time'][6:8]), 0)

dt_time_to_stop_record = datetime(int(data_json['stop_date'][0:4]), int(data_json['stop_date'][5:7]),
                                   int(data_json['stop_date'][8:10]),
                                   int(data_json['stop_time'][0:2]), int(data_json['stop_time'][3:5]),
                                   int(data_json['stop_time'][6:8]), 0)


print(dt_time_to_start_record)
print(dt_time_to_stop_record)

# Check the correctness of start and stop time
if (dt_time_to_start_record < dt_time_to_stop_record) and (dt_time_to_start_record > datetime.now()):
    print('\n   Time limits:')
    print('   Recording start time: ', dt_time_to_start_record)
    print('   Recording stop time:  ', dt_time_to_stop_record, '\n')
else:
    sys.exit('\n\n * ERROR! Time limits are wrong!!! \n\n')


print('   The record will start in: ', dt_time_to_start_record - datetime.now())

# Convert the data to string
json_string = json.dumps(data_json)

# Prepare command to send
send_command = 'set prc/ccp/ctl/osf 0 ' + json_string + '\0'



# print('\n Host: ', host)
# print('\n Port: ', port)
# print('\n Command: ', send_command)
#
# t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
# print('\n ', t, 'GMT:  Connecting to the server...')
#
# # Connecting to server
# serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serversocket.connect((host, port))
#
# t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
# print('\n ', t, 'GMT:  Connected to the server!')
#
# # Sending the main command from file
# serversocket.send(send_command.encode())
#
# t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
# print('\n ', t, 'GMT:  Message sent! Trying to read the reply...')
#
# # Read reply
# message = read_output(serversocket)
#
# # Keep connection live with sending /0 each 90 seconds
# while True:
#     time.sleep(90)
#     serversocket.send(b'\0')
#     t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#     print('\n ', t, 'GMT:  Sent command to keep connection')
