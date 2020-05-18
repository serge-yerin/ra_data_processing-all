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

    serversocket.send((b"set prc/dsp/net/dsa '192.168.10.204:48391'\0"))  #
    data = f_read_adr_meassage(serversocket, print_or_not)

    serversocket.send((b'set prc/srv/ctl/adr 4 1\0'))  #
    data = f_read_adr_meassage(serversocket, print_or_not)


    '''
    serversocket.send((b'get prc/srv/ctl/pth\0'))  # read directory where data are stored
    data = f_read_adr_meassage(serversocket, 0)
    parameters_dict["save_data_path"] = find_between(data,'SUCCESS\n','\n')

    serversocket.send((b'get prc/srv/ctl/sys\0'))  # read directory where data are stored
    data =  f_read_adr_meassage(serversocket, 0)
    parameters_dict["receiver_name"] = find_between(data,'SUCCESS\n','\n')

    serversocket.send((b'get prc/srv/ctl/plc\0'))  # read directory where data are stored
    data = f_read_adr_meassage(serversocket, 0)
    parameters_dict["observation_place"] = find_between(data, 'SUCCESS\n', '\n')

    serversocket.send((b'get prc/srv/ctl/dsc\0'))  # read directory where data are stored
    data = f_read_adr_meassage(serversocket, 0)
    parameters_dict["file_description"] = find_between(data, 'SUCCESS\n', '\n')

    serversocket.send((b'get prc/dsp/ctl/opt\0'))  #
    data = f_read_adr_meassage(serversocket, 0)
    parameters_dict["synchro_start"] = find_between(data, 'SyncStart: ', '\n')
    parameters_dict["external_clock"] = find_between(data, 'Ext.CLC: ', '\n')
    parameters_dict["fft_window"] = find_between(data, 'FFT_Window: ', '\n')
    parameters_dict["sum_diff_mode"] = find_between(data, 'A+B/A-B: ', '\n')


    '''
    return

################################################################################

if __name__ == '__main__':

    host = '192.168.1.171'
    port = 38386
    control = 1
    delay = 5

    parameters_dict = f_get_adr_parameters(serversocket, 1)

    '''
    get prc/dsp/ctl/set
    1387701331 - Start Second (sec)
    1387701332 - Stop Second (sec)
    0 - Test mode (index)
    16384 - Norm1 (rel. un.)
    16384 - Norm2 (rel. un.)
    2000 - Delay (ps)

    get prc/dsp/ctl/clc
    0 - UTC second (sec)
    0 - Seconds Tuning (sec)
    160000001 - Measured F_ADC (Hz)
    1 - Synchro state (On/Off)
    1 - Synchro end (On/Off)

    get prc/srv/ctl/adr
    0 - ADRS Status: OFF
    0 - WatchDog Thread: OFF
    0 - Data Thread: OFF
    0 - ADRS Param. Apply: OFF
    1 - New Param. Apply: ON
    0 - Apply DSP settings: OFF
    0 - Apply DSP synchro: OFF
    1 - Start/Stop: ON
    0 - DSP Status Update: OFF
    '''
'''
get prc/srv/ctl/srd
1 - Save on/off  (On/Off)
1 - Autocreation  (On/Off)
2000 - Size restriction  (MB)
2000 - Time restriction  (ms)

get prc/srv/ctl/adr 0
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




    # get prc/dsp/ctl/mdo                     - get values for all sub-parameters from [mdo] group
