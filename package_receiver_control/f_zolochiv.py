# Python3
# The script sends one command to run RT-32 observations an keep server connected (each 90 secs sends '\0')
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import sys
from os import path
import socket
import time
from time import gmtime, strftime

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# *******************************************************************************
#                              V A R I A B L E S                                *
# *******************************************************************************

run_file_path = 'rt32_run.txt'

# host = '192.168.14.20'
# port = 1255
# send_command = 'set prc/ccp/ctl/osf 0 { \
#                "calibration_schedule": [], \
#                "channels_switch_mode": "c", \
#                "dec": 1.0265154, \
#                "frequency_corrections_schedule": [], \
#                "frequency_ranges": \
#                {"cfa": 9440,"cfb": 9440,"cfc": 3200,"cfd": 3200,"kfa": 16600,"kfb":16600,"kfc": 3200,"kfd": 3200,"xfa": null,"xfb": null,"xfc": null,"xfd": null}, \
#                "frequency_switching_schedule": [],"name": "TEST", \
#                "operating_mode": "wck", \
#                "ra": 6.1234877, \
#                "start_date": "2020-10-30", \
#                "start_time":"15:45:00", \
#                "stop_date": "2020-10-30", \
#                "stop_time": "16:00:00"}\0'

# *******************************************************************************
#                                F U N C T I O N S                              *
# *******************************************************************************


def read_run_txt_file(filepath):
    '''
    Read txt file with json run command and return host, port and correct command
    filepath - path to txt file
    host - host to connect
    port: - port to connect
    send_command - full command from file
    '''
    send_command = ''
    file = open(filepath, "r")
    for line in file:
        if line.strip().startswith('#'):
            pass
        if line.strip() == '':
            pass
        elif line.strip().startswith('host'):
            host = line.strip().split('=')[-1].replace("'","").replace('"','')
        elif line.strip().startswith('port'):
            port = int(line.strip().split('=')[-1].replace("'","").replace('"',''))
        else:
            send_command += line.strip()

    host = host.strip() + '\0'
    return host, port, send_command


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


# *******************************************************************************
#                           M A I N     P R O G R A M                           *
# *******************************************************************************

# Read the file with run command
host, port, send_command = read_run_txt_file(run_file_path)

print('\n Host: ', host)
print('\n Port: ', port)
print('\n Command: ', send_command)

t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print('\n ', t, 'GMT:  Connecting to the server...')

# Connecting to server
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.connect((host, port))

t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print('\n ', t, 'GMT:  Connected to the server!')

# Sending the main command from file
serversocket.send(send_command.encode())

t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print('\n ', t, 'GMT:  Message sent! Trying to read the reply...')

# Read reply
message = read_output(serversocket)

# Keep connection live with sending /0 each 90 seconds
while True:
    time.sleep(90)
    serversocket.send(b'\0')
    t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print('\n ', t, 'GMT:  Sent command to keep connection')
