# Python3
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************

from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
from package_common_modules.text_manipulations import find_between

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************
def f_get_adr_parameters(serversocket, print_or_not):
    '''
    Function requests ADR receiver parameters via specified socket and prints them
    Input parameters:
        serversocket        - handle of socket to send and receive messages from server
        print_or_not        - to print the parameters to console (1) or not (0)
    Output parameters:
        parameters_dict     - dictionary with current parameters of ADR receiver
    '''
    parameters_dict = {}

    serversocket.send((b'get prc/srv/ctl/pth\0'))  # read directory where data are stored
    data = f_read_adr_meassage(serversocket, 0)
    parameters_dict["save_data_path"] = find_between(data,'SUCCESS\n',' ')

    serversocket.send((b'get prc/srv/ctl/sys\0'))  # read directory where data are stored
    data =  f_read_adr_meassage(serversocket, 0)
    parameters_dict["receiver_name"] = find_between(data,'SUCCESS\n','\0')

    serversocket.send((b'get prc/srv/ctl/plc\0'))  # read directory where data are stored
    data = f_read_adr_meassage(serversocket, 0)
    parameters_dict["observation_place"] = find_between(data, 'SUCCESS\n', '\0')

    serversocket.send((b'get prc/srv/ctl/dsc\0'))  # read directory where data are stored
    data = f_read_adr_meassage(serversocket, 0)
    parameters_dict["file_description"] = find_between(data, 'SUCCESS\n', '\0')

    '''
    get prc/dsp/ctl/opt                     - get values for all sub-parameters from [opt] group
    1 - SyncStart: ON
    0 - Ext.CLC: OFF
    1 - FFT_Window: ON
    0 - A+B/A-B: OFF

    get prc/srv/ctl/srd
    1 - Save on/off  (On/Off)
    1 - Autocreation  (On/Off)
    2000 - Size restriction  (MB)
    2000 - Time restriction  (ms)

    get prc/dsp/ctl/mdo
    5 - Mode (index)
    2048 - FFT Size (samples)
    700 - Averaging (Spectra count)
    0 - Start line (count)
    1 - Width (count)
    160000005 - ADC CLOCK (Hz)
    '''

    if print_or_not > 0:
        print('\n * Current ADR parameters:')
        print('   File description: \n   ', parameters_dict["file_description"], '\n')
        print('   Path to save data:               ', parameters_dict["save_data_path"])
        print('   Path to save data:               ', parameters_dict["observation_place"])
        print('   Path to save data:               ', parameters_dict["receiver_name"])

    return parameters_dict


################################################################################

if __name__ == '__main__':

    host = '192.168.1.171'
    port = 38386
    control = 1
    delay = 5


    parameters_dict = f_get_adr_parameters(serversocket, 1)



    '''
    get prc/dsp/ctl/opt                     - get values for all sub-parameters from [opt] group
    1 - SyncStart: ON
    0 - Ext.CLC: OFF
    1 - FFT_Window: ON
    0 - A+B/A-B: OFF
    '''
    '''
    get prc/dsp/ctl/set
    1387701331 - Start Second (sec)
    1387701332 - Stop Second (sec)
    0 - Test mode (index)
    16384 - Norm1 (rel. un.)
    16384 - Norm2 (rel. un.)
    2000 - Delay (ps)
    '''

    '''
    get prc/dsp/ctl/clc
    0 - UTC second (sec)
    0 - Seconds Tuning (sec)
    160000001 - Measured F_ADC (Hz)
    1 - Synchro state (On/Off)
    1 - Synchro end (On/Off)
    '''
    '''
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
'''

'''
get prc/dsp/ctl/mdo
5 - Mode (index)
2048 - FFT Size (samples)
700 - Averaging (Spectra count)
0 - Start line (count)
1 - Width (count)
160000005 - ADC CLOCK (Hz)

'''


'''
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
