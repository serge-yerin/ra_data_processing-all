# Python3

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************

from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
import time

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************
def f_initialize_adr(serversocket, print_or_not, pause = 0.5):
    '''
    Function initializes ADR receiver if it was just turned on
    Input parameters:
        serversocket        - handle of socket to send and receive messages from server
        print_or_not        - to print the parameters to console (1) or not (0)
    Output parameters:

    '''
    time.sleep(pause)

    # DSP Connect button
    serversocket.send((b"set prc/dsp/net/dsa '192.168.10.204:48391'\0"))
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    # DSP Ready (try to use commands instead of restricted one)
    serversocket.send((b"set prc/srv/ctl/adr 3 1\0"))  # To apply the ADR DSP parameters (which is set in the [mdo]
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    serversocket.send((b"set prc/srv/ctl/adr 5 1\0"))  # To apply the ADR DSP settings, which are defined in [set]
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    serversocket.send((b"set prc/srv/ctl/adr 6 1\0"))  # To apply the ADR DSP options, which are defined in [opt]
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)


    # "Data on PC"
    serversocket.send((b"set prc/srv/ctl/adr 7 0\0"))  # stop  DSP
    data = f_read_adr_meassage(serversocket, print_or_not)
    serversocket.send((b"set prc/srv/ctl/adr 2 0\0"))  # stop UDP data processing threads
    data = f_read_adr_meassage(serversocket, print_or_not)
    serversocket.send((b"set prc/dsp/net/udp '192.168.10.60:48396'\0"))  # set UDP target address:port
    data = f_read_adr_meassage(serversocket, print_or_not)
    serversocket.send((b"set prc/dsp/net/wvf '192.168.11.60:48395'\0"))  #
    data = f_read_adr_meassage(serversocket, print_or_not)
    serversocket.send((b"set prc/srv/ctl/adr 3 1\0"))  # apply ADR DSP parameters
    data = f_read_adr_meassage(serversocket, print_or_not)
    serversocket.send((b"set prc/srv/ctl/adr 5 1\0"))  # apply ADR DSP settings
    data = f_read_adr_meassage(serversocket, print_or_not)
    serversocket.send((b"set prc/srv/ctl/adr 2 1\0"))  # start UDP data processing threads
    data = f_read_adr_meassage(serversocket, print_or_not)
    serversocket.send((b"set prc/srv/ctl/adr 7 1\0"))  # start DSP
    data = f_read_adr_meassage(serversocket, print_or_not)

    # Be sure variables are without spaces! Use underscore instead
    receiver_name = 'B_ADRS02'
    observatory_name = 'Volokhiv_Yar_(Kharkiv_region)_Ukraine'

    # Set system name (receiver name):
    serversocket.send(('set prc/srv/ctl/sys ' + receiver_name + '\0').encode())
    data = f_read_adr_meassage(serversocket, print_or_not)

    # Set observatory name (place name):
    serversocket.send(('set prc/srv/ctl/plc ' + observatory_name + '\0').encode())
    data = f_read_adr_meassage(serversocket, print_or_not)

    time.sleep(pause)

    return



################################################################################

if __name__ == '__main__':

    host = '192.168.1.171'
    port = 38386
    control = 1
    delay = 5

    f_initialize_adr(serversocket, 1)

'''
    "set prc/srv/ctl/adr 7 0"; //stop  DSP
    "set prc/srv/ctl/adr 2 0"; //stop UDP data processing threads
    "set prc/dsp/net/udp <a.b.c.d:port>"; //set UDP target address:port
    "set prc/srv/ctl/adr 3 1"; // apply ADR DSP parameters
    "set prc/srv/ctl/adr 5 1"; // apply ADR DSP settings
    "set prc/srv/ctl/adr 2 1"; //start UDP data processing threads
    "set prc/srv/ctl/adr 7 1"; //start DSP

    # Usual sequence when ADRS is just turned on and buttons in ADRS Control software are pressed
    # DSP Connect
    set prc/dsp/net/dsa '192.168.10.204:48391'
    # DSP Ready
    set prc/srv/ctl/adr 4 1   # Do not use! Used only for Official ADR Control Client!
    # DSP Runs
    set prc/srv/ctl/adr 7 1
    # "Data on PC"
    set prc/srv/ctl/adr 7 0
    set prc/srv/ctl/adr 2 0
    set prc/dsp/net/udp '192.168.10.60:48396'
    set prc/dsp/net/wvf '192.168.11.60:48395'
    set prc/srv/ctl/adr 3 1
    set prc/srv/ctl/adr 5 1
    set prc/srv/ctl/adr 2 1
    set prc/srv/ctl/adr 7 1
'''

'''
    # Messages sent by ADR in seen in low-level mode
    serversocket.send((b"set prc/dsp/net/dsa '192.168.10.204:48391'\0"))  #
    data = f_read_adr_meassage(serversocket, print_or_not)
    # SUCCESS 192.168.10.204:48391

    serversocket.send((b'set prc/srv/ctl/adr 4 1\0'))  # Do not use! Used only for Official ADR Control Client!
    data = f_read_adr_meassage(serversocket, print_or_not)
    # SUCCESS DSP parameters apply: Ok!
'''
