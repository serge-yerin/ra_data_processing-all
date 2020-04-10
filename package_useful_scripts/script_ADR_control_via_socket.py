# Program intended to read and show data from DAT (ADR) file

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************
data_directory_name = 'test_yes'


#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************
import socket
import time
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
    serversocket.send('ADRSCTRL'.encode())
    ctrl = 1
    register_cc_msg = bytearray([108,0,0,0])
    register_cc_msg.extend(b'YeS\0                                                            ')  # Name 64 bytes
    register_cc_msg.extend('adrs\0                           '.encode())                          # Password 32 bytes
    register_cc_msg.extend([0, 0, 0, 0])                                                         # Priv 4 bytes
    register_cc_msg.extend([ctrl, 0, 0, 0])                                                      # CTRL 4 bytes
    register_cc_msg = bytes(register_cc_msg)
    print(' Length: ', len(register_cc_msg))
    #print(' Sent message: ', register_cc_msg)

    serversocket.send(register_cc_msg)
    data = serversocket.recv(5024).decode()
    print ('\n Received message: ', data)

    #serversocket.send('get prc/dsp/ctl/mdo'.encode())
    #data = serversocket.recv(1024).decode()
    #print (' Received message: ', data)

    time.sleep(5)

    print ('\n\n\n Making directory ')
    #serversocket.send(('set prc/srv/ctl/pth ' + data_directory_name).encode())    # set directory to store data
    serversocket.send(('get prc/srv/ctl/pth').encode())    # set directory to store data

    data = serversocket.recv(6024).decode()
    print ('\n Received message: ', data)


    '''
    time.sleep(5)

    print ('\n\n\n Start ')
    serversocket.send('set prc/srv/ctl/srd 0 1'.encode())    # start data recording
    data = serversocket.recv(3024).decode()
    print ('\n Received message: ', data)

    time.sleep(15)

    print ('\n\n\n Stop ')
    serversocket.send('set prc/srv/ctl/srd 0 0'.encode())    # stop data recording
    data = serversocket.recv(3024).decode()
    print ('\n Received message: ', data)

    time.sleep(15)

    '''

ts(str)

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

get prc/dsp/ctl/opt                     - get values for all sub-parameters from [opt] group

set prc/dsp/ctl/opt 1 <0/1>             - On/Off the external source of ADC CLC.
get prc/dsp/ctl/opt 1

set prc/dsp/ctl/opt 3 <0/1>             - On/Off the “sum-difference” mode A±B, instead of A/B mode on CH-A and CH-B outputs.
get prc/dsp/ctl/opt 3

set prc/dsp/ctl/set 5 <DDEL>            - Differential delay (DDEL) between CH-A and CH-B ADC sampling (CLC front) in picoseconds.
get prc/dsp/ctl/set 5

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


get prc/srv/ctl/adr 0           - get ADRS status (read only)
    ADR Mode: 6
    Flags: 143
    DSP Time: 1387859967
    PC1 Time: 1387859967:893
    PC2 Time: 1387859968:331
    FileSize: 0
    FileTime: 0
    F_ADC: 160000002
    FS_FREE: 1.35e+04
    FS_PERC: 41.6

'''


'''
Name=Processing
Descr=Setup parameters for pre-processing and post-processing of the radar data
Type=2
END_SIBLNXT_CHLDdsp
Name=DSP parameters
Descr=DSP processing parameters
NXT_SIBLNXT_CHLDctl
Name=DSP Control
Descr=DSP data processing parameters
NXT_SIBLNXT_CHLDmdo
Name=Operation Mode
Descr=Receiver Operation Mode
Action=3
Access=0
CntVal=6
iValue0=4
iValMin0=0
iValMax0=6
iName0=Mode
iUnit0=index
iValue1=4096
iValMin1=2048
iValMax1=32768
iName1=FFT Size
iUnit1=samples
iValue2=3815
iValMin2=14
iValMax2=32767
iName2=Averaging
iUnit2=Spectra count
iValue3=0
iValMin3=0
iValMax3=15
iName3=Start line
iUnit3=count
iValue4=2
iValMin4=1
iValMax4=16
iName4=Width
iUnit4=count
iValue5=156250130
iValMin5=10000000
iValMax5=180000000
iName5=ADC CLOCK
iUnit5=Hz
NXT_SIBLopt
Name=Options
Descr=Digital Receiver Options
Action=3
Access=0
CntVal=4
bValue0=0
bName0=SyncStart
bUnit0=On/Off
bValue1=0
bName1=Ext.CLC
'''
