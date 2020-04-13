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

    serversocket.send((b'get prc/dsp/ctl/opt\0'))  # read directory where data are stored
    data = f_read_adr_meassage(serversocket, 0)
    parameters_dict["synchro_start"] = find_between(data, 'SyncStart: ', '\n')
    parameters_dict["external_clock"] = find_between(data, 'Ext.CLC: ', '\n')
    parameters_dict["fft_window"] = find_between(data, 'FFT_Window: ', '\n')
    parameters_dict["sum_diff_mode"] = find_between(data, 'A+B/A-B: ', '\n')

    serversocket.send((b'get prc/dsp/ctl/mdo\0'))  # read directory where data are stored
    data = f_read_adr_meassage(serversocket, 0)
    parameters_dict["operation_mode_num"] = int(find_between(data, 'SUCCESS\n', ' - Mode'))
    if   parameters_dict["operation_mode_num"] == 0: parameters_dict["operation_mode_str"] = 'Waveform ch. A'
    elif parameters_dict["operation_mode_num"] == 1: parameters_dict["operation_mode_str"] = 'Waveform ch. B'
    elif parameters_dict["operation_mode_num"] == 2: parameters_dict["operation_mode_str"] = 'Waveform ch. A & B'
    elif parameters_dict["operation_mode_num"] == 3: parameters_dict["operation_mode_str"] = 'Spectra ch. A'
    elif parameters_dict["operation_mode_num"] == 4: parameters_dict["operation_mode_str"] = 'Spectra ch. B'
    elif parameters_dict["operation_mode_num"] == 5: parameters_dict["operation_mode_str"] = 'Spectra ch. A & B'
    elif parameters_dict["operation_mode_num"] == 6: parameters_dict["operation_mode_str"] = 'Correlation ch. A & B'
    else: parameters_dict["operation_mode_str"] = 'Unknown mode'

    parameters_dict["FFT_size_samples"] = int(find_between(data, '\n', ' - FFT Size'))
    parameters_dict["spectra_averaging"] = int(find_between(data, '\n', ' - Averaging'))
    parameters_dict["start_line_freq"] = int(find_between(data, '\n', ' - Start line'))
    parameters_dict["width_line_freq"] = int(find_between(data, '\n', ' - Width'))
    parameters_dict["clock_frequency"] = int(find_between(data, '\n', ' - ADC CLOCK'))

    '''
    get prc/srv/ctl/srd
    1 - Save on/off  (On/Off)
    1 - Autocreation  (On/Off)
    2000 - Size restriction  (MB)
    2000 - Time restriction  (ms)
    '''

    if print_or_not > 0:
        print('\n * Current ADR parameters:')
        print('\n   File description: \n\n  ', parameters_dict["file_description"], '\n')
        print('   Path to save data:            ', parameters_dict["save_data_path"])
        print('   Observation place:            ', parameters_dict["observation_place"])
        print('   Receiver name:                ', parameters_dict["receiver_name"])

        print('   External 160 MHz clock:       ', parameters_dict["external_clock"])
        print('   Sum/diff mode:                ', parameters_dict["sum_diff_mode"])
        print('   ADR operation mode:           ', parameters_dict["operation_mode_str"])
        print('   FFT samples number:           ', parameters_dict["FFT_size_samples"])
        print('   Number of frequency channels: ', parameters_dict["FFT_size_samples"]/2)
        print('   Sampling frequency:           ', format(parameters_dict["clock_frequency"], ',').replace(',', ' ').replace('.', ','), ' Hz')
        print('   NMumber of spectra averaged:  ', parameters_dict["spectra_averaging"])

    #parameters_dict["start_line_freq"] = int(find_between(data, '\n', ' - Start line'))
    #parameters_dict["width_line_freq"] = int(find_between(data, '\n', ' - Width'))


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
