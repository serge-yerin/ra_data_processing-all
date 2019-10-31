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
login = 'control'
print ' Host: ', host
print ' Port: ', port
serversocket.connect((host, port))

def ts(str):
    serversocket.send('get prc/dsp/ctl/mdo'.encode())
    data = ''
    data = serversocket.recv(1024).decode()
    print data

ts(str)
 