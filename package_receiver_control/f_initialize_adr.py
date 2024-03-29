# Python3

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************

import sys, time
from os import path
from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
from package_receiver_control.f_connect_to_adr_receiver import f_connect_to_adr_receiver


# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************

def f_initialize_adr(serversocket, receiver_ip, print_or_not, pause = 0.1):
    """
    Function initializes ADR receiver if it was just turned on
    Input parameters:
        serversocket        - handle of socket to send and receive messages from server
        print_or_not        - to print the parameters to console (1) or not (0)
    Output parameters:

    """
    # Be sure variables are without spaces! Use underscore instead

    observatory_name = 'GURT_Volokhiv_Yar_(Kharkiv_region)_Ukraine'

    receiver_name = 'Test'
    if receiver_ip[-3:] == '171':
        receiver_name = 'A_ADRS01'
        udp_port = '48395'
        wvf_port = '48396'
    if receiver_ip[-3:] == '172':
        receiver_name = 'B_ADRS02'
        udp_port = '48396'
        wvf_port = '48395'

    time.sleep(pause)

    print('\n  Receiver initialization...')

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
    #serversocket.send((b"set prc/dsp/net/udp '192.168.10.60:48395'\0"))  # set UDP target address:port (192.168.10.60:48395 on ADR 1) 6
    serversocket.send(("set prc/dsp/net/udp '192.168.10.60:" + udp_port + "'\0").encode())
    #serversocket.send((b"set prc/dsp/net/udp '192.168.10.60:'" + udp_port + "\0"))  # set UDP target address:port (192.168.10.60:48395 on ADR 1) 6
    data = f_read_adr_meassage(serversocket, print_or_not)
    #serversocket.send((b"set prc/dsp/net/wvf '192.168.11.60:48396'\0"))  # (192.168.11.60:48396 on ADR 1) 5
    serversocket.send(("set prc/dsp/net/wvf '192.168.11.60:" + wvf_port + "'\0").encode())
    #serversocket.send((b"set prc/dsp/net/wvf '192.168.11.60:48396'\0"))  # (192.168.11.60:48396 on ADR 1) 5
    data = f_read_adr_meassage(serversocket, print_or_not)
    serversocket.send((b"set prc/srv/ctl/adr 3 1\0"))  # apply ADR DSP parameters
    data = f_read_adr_meassage(serversocket, print_or_not)
    serversocket.send((b"set prc/srv/ctl/adr 5 1\0"))  # apply ADR DSP settings
    data = f_read_adr_meassage(serversocket, print_or_not)
    serversocket.send((b"set prc/srv/ctl/adr 2 1\0"))  # start UDP data processing threads
    data = f_read_adr_meassage(serversocket, print_or_not)
    serversocket.send((b"set prc/srv/ctl/adr 7 1\0"))  # start DSP
    data = f_read_adr_meassage(serversocket, print_or_not)

    # Set system name (receiver name):
    serversocket.send(('set prc/srv/ctl/sys ' + receiver_name + '\0').encode())
    data = f_read_adr_meassage(serversocket, print_or_not)

    # Set observatory name (place name):
    serversocket.send(('set prc/srv/ctl/plc ' + observatory_name + '\0').encode())
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b"set prc/srv/ctl/srd 1 1\0"))  # Files auto create ON
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b"set prc/srv/ctl/srd 2 2048\0"))  # Data file size 2048 MB
    data = f_read_adr_meassage(serversocket, print_or_not)

    time.sleep(pause)

    return


################################################################################

if __name__ == '__main__':

    # To change system path to main directory of the project:
    if __package__ is None:
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    port = 38386
    receiver_ip = '192.168.1.171'

    # Connect to the ADR receiver via socket
    serversocket, input_parameters_str = f_connect_to_adr_receiver(receiver_ip, port, 1, 1)  # 1 - control, 1 - delay in sec

    f_initialize_adr(serversocket, receiver_ip, 1, pause=0.5)

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
