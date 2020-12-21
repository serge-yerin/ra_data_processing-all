# Python 3
import sys
import time
from os import path
from pexpect import pxssh
# from datetime import datetime
from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
from package_receiver_control.f_connect_to_adr_receiver import f_connect_to_adr_receiver

# *************************************************************
#                        MAIN FUNCTION                        *
# *************************************************************


def f_synchronize_adr(serversocket, receiver_ip, time_server):
    '''
    Function reads a message from ADR radio astronomy receiver
    ntp server must be installed on server PC (sudo apt install ntp)
    to start ntp-server on server pc use "sudo /etc/init.d/ntp start" or/and "sudo systemctl restart ntp"
    Input parameters:
        serversocket        - handle of socket to send and receive messages from server
        receiver_ip                - IP address of receiver_ip to connect for sntp synchro from server
        time_server         - IP address of the ntp time server (probably PC where the script runs)
    Output parameters:
    '''
    # Update synchronization of PC and ADR
    print('\n * ADR synchronization with Server and ADR PC')
    
    receiver_file = open('service_data/receiver.txt', 'r')
    rec_user = receiver_file.readline()[:-1]
    password = receiver_file.readline()[:-1]
    receiver_file.close()

    # SSH connection to ADR receiver to send sntp command to synchronize with server
    s = pxssh.pxssh()
    if not s.login(receiver_ip, rec_user, password):
        print('\n   ERROR! SSH session failed on login!')
        print(str(s))
    else:
        print('\n   SSH session login successful')
        s.sendline('sntp -P no -r ' + time_server)
        s.prompt()  # match the prompt
        print('\n   Answer: ', s.before)  # print everything before the prompt.
        s.logout()

    time.sleep(1)

    # now = datetime.now()
    serversocket.send(b'set prc/dsp/ctl/clc 0 1\0')
    data_0 = f_read_adr_meassage(serversocket, 0)
    serversocket.send(b'set prc/srv/ctl/adr 6 1\0')
    data_1 = f_read_adr_meassage(serversocket, 0)
    if data_0.startswith('SUCCESS') and data_1.startswith('SUCCESS'):
        print('\n   UTC absolute second set')
    else:
        print('\n   ERROR! UTC absolute second was not set!')

    time.sleep(3)

    serversocket.send(b'set prc/dsp/ctl/clc 0 0\0')  # tune second
    data_0 = f_read_adr_meassage(serversocket, 0)
    serversocket.send(b'set prc/dsp/ctl/clc 1 0\0')  # tune second
    data_1 = f_read_adr_meassage(serversocket, 0)
    serversocket.send(b'set prc/srv/ctl/adr 6 1\0')
    data_2 = f_read_adr_meassage(serversocket, 0)
    if data_0.startswith('SUCCESS') and data_1.startswith('SUCCESS') and data_2.startswith('SUCCESS'):
        print('\n   UTC absolute second tuned')

# ###############################################################################


if __name__ == '__main__':

    # To change system path to main directory of the project:
    if __package__ is None:
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    port = 38386
    receiver_ip = '192.168.1.172'
    time_server = '192.168.1.150'

    # Connect to the ADR receiver via socket # 1 - control, 1 - delay in sec
    serversocket, input_parameters_str = f_connect_to_adr_receiver(receiver_ip, port, 1, 1)

    f_synchronize_adr(serversocket, receiver_ip, time_server)
