# Python3
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import socket
import time

# *******************************************************************************
#                              V A R I A B L E S                                *
# *******************************************************************************
host = '192.168.14.20'
port = 1255
send_command = 'set prc/ccp/ctl/osf 0 { \
               "calibration_schedule": [], \
               "channels_switch_mode": "c", \
               "dec": 1.0265154, \
               "frequency_corrections_schedule": [], \
               "frequency_ranges": \
               {"cfa": 9440,"cfb": 9440,"cfc": 3200,"cfd": 3200,"kfa": 16600,"kfb":16600,"kfc": 3200,"kfd": 3200,"xfa": null,"xfb": null,"xfc": null,"xfd": null}, \
               "frequency_switching_schedule": [],"name": "TEST", \
               "operating_mode": "wck", \
               "ra": 6.1234877, \
               "start_date": "2020-10-28", \
               "start_time":"16:16:00", \
               "stop_date": "2020-10-28", \
               "stop_time": "16:21:00"}\0'

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************

def read_relay_output(serversocket):
    byte = b'a'
    message = bytearray([])
    byte = serversocket.recv(8)
    message.extend(byte)
    message = bytes(message).decode()
    print('\n Reply: ', message)
    return message



print('\n * Connecting to the server...')

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.connect((host, port))

print('\n * Connected to the server!')

serversocket.send(send_command.encode())

print('\n * Message sent! Trying to read the reply...')

message = read_relay_output(serversocket)

while True:
    time.sleep(90)
    serversocket.send(b'\0')
    print(' Sent 0')


