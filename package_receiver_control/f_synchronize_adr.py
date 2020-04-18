# Python 3
from pexpect import pxssh
import time
from datetime import datetime
from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage

#*************************************************************
#                       MAIN FUNCTION                        *
#*************************************************************
def f_synchronize_adr(serversocket, host):
    '''
    Function reads a message from ADR radio astronomy receiver
    Input parameters:
        serversocket        - handle of socket to send and receive messages from server
        host                - IP address of host to connect for sntp synchro from server
    Output parameters:
    '''
    # Update synchronization of PC and ADR
    print('\n * ADR synchronization with Server and ADR PC')

    # SSH connection to ADR receiver to send sntp command to synchronize with server
    s = pxssh.pxssh()
    if not s.login(host, 'root', 'ghbtvybr'):
        print('\n   ERROR! SSH session failed on login!')
        print(str(s))
    else:
        print('\n   SSH session login successful')
        s.sendline('sntp -P no -r 192.168.1.150')
        s.prompt()  # match the prompt
        print('\n   Answer: ', s.before)  # print everything before the prompt.
        s.logout()

    time.sleep(1)

    now = datetime.now()
    seconds_since_midnight = int((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
    #serversocket.send(('set prc/dsp/ctl/clc 0 ' + str(seconds_since_midnight) + '\0').encode())  # seconds since midnight
    serversocket.send(b'set prc/dsp/ctl/clc 0 1\0')
    serversocket.send(b'set prc/srv/ctl/adr 6 1\0')
    data = f_read_adr_meassage(serversocket, 0)
    if data.startswith('SUCCESS'):
        print('\n   UTC absolute second set')
    else:
        print('\n   ERROR! UTC absolute second was not set!')

    time.sleep(3)

    #serversocket.send(b'set prc/dsp/ctl/clc 1 0\0')  # tune second
    serversocket.send(b'set prc/dsp/ctl/clc 0 0\0')  # tune second
    serversocket.send(b'set prc/dsp/ctl/clc 1 0\0')  # tune second
    serversocket.send(b'set prc/srv/ctl/adr 6 1\0')
    data = f_read_adr_meassage(serversocket, 0)
    if data.startswith('SUCCESS'):
        print('\n   UTC absolute second tuned')

################################################################################

if __name__ == '__main__':

    host = '192.168.1.171'
    f_synchronize_adr(serversocket, host)

