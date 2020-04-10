# Program intended to read and show data from DAT (ADR) file

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************
#*************************************************************

#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************
import socket
from threading import *

#*************************************************************
#                       MAIN PROGRAM                         *
#*************************************************************

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.1.171'
port = 38386
login = 'view' #'control'
print (' Host: ', host)
print (' Port: ', port)
serversocket.connect((host, port))

def ts(str):
    ####serversocket.send('get prc/dsp/ctl/mdo'.encode())
    serversocket.send('ADRSCTRL'.encode())
    ctrl = 0
    register_cc_msg = bytearray([108,0,0,0])
    register_cc_msg.extend(b'YeS\0                                                            ')  # Name 64 bytes
    register_cc_msg.extend('adrs\0                           '.encode())                          # Password 32 bytes
    register_cc_msg.extend([0, 0, 0, 0])                                                         # Priv 4 bytes
    register_cc_msg.extend([ctrl, 0, 0, 0])                                                      # CTRL 4 bytes
    register_cc_msg = bytes(register_cc_msg)
    print(' Length: ', len(register_cc_msg))
    #print(' Sent message: ', register_cc_msg)

    serversocket.send(register_cc_msg)

    data = serversocket.recv(200).decode()
    print (' Received message: ', data)

    serversocket.send('get prc/dsp/ctl/mdo'.encode())
    data = serversocket.recv(1024).decode()
    print (' Received message: ', data)

ts(str)
