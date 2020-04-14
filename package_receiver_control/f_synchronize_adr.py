# Python 3

from pexpect import pxssh
import time
from datetime import datetime
from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage

#*************************************************************
#                       MAIN FUNCTION                        *
#*************************************************************
def f_synchronize_adr(serversocket):
    '''
    Function reads a message from ADR radio astronomy receiver
    Input parameters:
        print_or_not   - to print (1) or not (0) the message to terminal
    Output parameters:
        message        - string message
    '''
    # Update synchronization of PC and ADR
    print('\n * ADR synchronization with Server and ADR PC')
    # os.system('sntp -P no -r 192.168.1.150')
    # print('\n   ADR PC synchronized with the GURT server')
    # time.sleep(1)

    s = pxssh.pxssh()
    if not s.login('192.168.1.171', 'root', 'ghbtvybr'):
        print("   SSH session failed on login.")
        print(str(s))
    else:
        print("   SSH session login successful!")
        s.sendline('sntp -P no -r 192.168.1.150')
        s.prompt()  # match the prompt
        print('  Answer: ', s.before)  # print everything before the prompt.
        s.logout()

    time.sleep(1)

    now = datetime.now()
    seconds_since_midnight = int((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
    serversocket.send(
        ('set prc/dsp/ctl/clc 0 ' + str(seconds_since_midnight) + '\0').encode())  # set directory to store data
    data = f_read_adr_meassage(serversocket, 0)
    if data.startswith('SUCCESS'):
        print('\n   UTC absolute second set')
    else:
        print('\n   ERROR! UTC absolute second was not set!')

    time.sleep(1)

    serversocket.send(b'set prc/dsp/ctl/clc 1 0\0')  # set directory to store data
    data = f_read_adr_meassage(serversocket, 0)
    if data.startswith('SUCCESS'):
        print('\n   UTC absolute second tuned')

################################################################################

if __name__ == '__main__':


    f_synchronize_adr(serversocket)

