# Python3
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************

from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
from package_common_modules.text_manipulations import find_between

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************
def f_initialize_adr(serversocket, print_or_not):
    '''
    Function initializes ADR receiver if it was just turned on
    Input parameters:
        serversocket        - handle of socket to send and receive messages from server
        print_or_not        - to print the parameters to console (1) or not (0)
    Output parameters:

    "set prc/srv/ctl/adr 7 0"; //stop  DSP
    "set prc/srv/ctl/adr 2 0"; //stop UDP data processing threads
    "set prc/dsp/net/udp <a.b.c.d:port>"; //set UDP target address:port
    "set prc/srv/ctl/adr 3 1"; // apply ADR DSP parameters
    "set prc/srv/ctl/adr 5 1"; // apply ADR DSP settings
    "set prc/srv/ctl/adr 2 1"; //start UDP data processing threads
    "set prc/srv/ctl/adr 7 1"; //start DSP


    set prc/dsp/net/dsa '192.168.10.204:48391'
    SUCCESS
    192.168.10.204:48391

    set prc/srv/ctl/adr 4 1
    SUCCESS
    DSP parameters apply: Ok!
    '''

    # MDO parameters
    serversocket.send((b"set prc/dsp/ctl/mdo 0 5\0"))  # Set operation mode 0-6 (6 - correlation)
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b"set prc/dsp/ctl/mdo 1 16384\0"))  # Set FFT size 2048,4096,8192,16384,32768
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b"set prc/dsp/ctl/mdo 2 1000\0"))  # Set number of averages spectra in range [16 … 32768]
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b"set prc/dsp/ctl/mdo 3 0\0"))  # Start frequency line of the band in 1024-steps. SLINE range [0 … (SFFT-1024)/1024]
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b"set prc/dsp/ctl/mdo 4 16384\0"))  # Width of  frequency band in 1024-steps. WIDTH range [1 … (SFFT-SLINE*1024)/1024]
    data = f_read_adr_meassage(serversocket, print_or_not)

    # OPT parameters
    serversocket.send((b"set prc/dsp/ctl/opt 0 0\0"))  # On/Off the synchro start of ADR data processing by front of the PPS signal.
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b"set prc/dsp/ctl/opt 1 0\0"))  # On/Off the external source of ADC CLC
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b"set prc/dsp/ctl/opt 2 1\0"))  # On/Off the FFT Hanning window
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b"set prc/dsp/ctl/opt 3 0\0"))  # On/Off the “sum-difference” mode A±B
    data = f_read_adr_meassage(serversocket, print_or_not)



    serversocket.send((b"set prc/srv/ctl/adr 3 1\0"))  # To apply the ADR DSP parameters (which is set in the [mdo]
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b"set prc/srv/ctl/adr 5 1\0"))  # To apply the ADR DSP settings, which are defined in [set]
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b"set prc/srv/ctl/adr 6 1\0"))  # To apply the ADR DSP options, which are defined in [opt]
    data = f_read_adr_meassage(serversocket, print_or_not)




    '''
    # Messages sent by ADR in seen in low-level mode
    serversocket.send((b"set prc/dsp/net/dsa '192.168.10.204:48391'\0"))  #
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b'set prc/srv/ctl/adr 4 1\0'))  # Do not use! Used only for Official ADR Control Client!
    data = f_read_adr_meassage(serversocket, print_or_not)
    '''

    '''
    serversocket.send((b'get prc/srv/ctl/pth\0'))  # read directory where data are stored
    data = f_read_adr_meassage(serversocket, 0)
    parameters_dict["save_data_path"] = find_between(data,'SUCCESS\n','\n')

    '''
    return

################################################################################

if __name__ == '__main__':

    host = '192.168.1.171'
    port = 38386
    control = 1
    delay = 5

    parameters_dict = f_initialize_adr(serversocket, 1)

