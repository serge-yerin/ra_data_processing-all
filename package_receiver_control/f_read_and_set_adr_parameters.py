# Python3

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************

from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
import time
import sys

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************

def f_read_adr_parameters_from_csv_file(parameters_file):
    '''
    Function reads ADR receiver parameters from csv (txt) file and return a dictionary with parameters
    Input parameters:
        parameters_file         - path to parameters file (txt or csv)
    Output parameters:
        parameters_dict         - dictionary with ADR receiver parameters
    '''
    parameters_dict = {}
    file = open(parameters_file, "r")
    for line in file:
        if line.strip().startswith('#'):
            pass
        else:
            line = line.strip().replace(' ', '').split(',')
            parameters_dict["operation_mode_num"] = line[0]
            parameters_dict["FFT_size_samples"] = line[1]
            parameters_dict["spectra_averaging"] = line[2]
            parameters_dict["start_line_freq"] = line[3]
            parameters_dict["width_line_freq"] = line[4]
            parameters_dict["clock_source"] = line[5]
            parameters_dict["sum_diff_mode_num"] = line[6]
            parameters_dict["chan_diff_delay"] = line[7]

    return parameters_dict


def f_read_adr_parameters_from_txt_file(parameters_file):
    '''
    Function reads ADR receiver parameters from csv (txt) file and return a dictionary with parameters
    Input parameters:
        parameters_file         - path to parameters file (txt or csv)
    Output parameters:
        parameters_dict         - dictionary with ADR receiver parameters
    '''
    parameters_dict = {}
    file = open(parameters_file, "r")
    for line in file:
        if line.strip().startswith('#') or line.strip().startswith('Parameter'):
            pass
        else:
            line = line.strip().replace(' ', '').split(',')
            if line[0] == 'ADR_mode':         parameters_dict["operation_mode_num"] = line[1]
            if line[0] == 'FFT_size':         parameters_dict["FFT_size_samples"] = line[1]
            if line[0] == 'Averaged_spectra': parameters_dict["spectra_averaging"] = line[1]
            if line[0] == 'Start_freq_line':  parameters_dict["start_line_freq"] = line[1]
            if line[0] == 'Width_freq_lines': parameters_dict["width_line_freq"] = line[1]
            if line[0] == 'CLC_source':       parameters_dict["clock_source"] = line[1]
            if line[0] == 'Sum_diff_mode':    parameters_dict["sum_diff_mode_num"] = line[1]
            if line[0] == 'Dif_delay':        parameters_dict["chan_diff_delay"] = line[1]

    return parameters_dict


def f_check_adr_parameters_correctness(parameters_dict):
    '''
    Checks dictionary with ADR parameters to set for correct values
    '''

    if int(parameters_dict["operation_mode_num"]) not in (0, 1, 2, 3, 4, 5, 6):
        print('\n  Error!!! Operation mode is wrong!\n')
        sys.exit('  Program stopped!')

    if int(parameters_dict["FFT_size_samples"]) not in (2048, 4096, 8192, 16384, 32768):
        print('\n  Error!!! FFT size is wrong!\n')
        sys.exit('  Program stopped!')

    if (int(parameters_dict["spectra_averaging"]) < 16 or int(parameters_dict["spectra_averaging"]) > 32768):
        print('\n  Error!!! Spectra averaging number is wrong!\n')
        sys.exit('  Program stopped!')

    if int(parameters_dict["start_line_freq"]) not in (0, 1, 2, 3, 4, 5, 6, 7, 8):   # 0 … (SFFT-1024)/1024
        print('\n  Error!!! Start frequency line is wrong!\n')
        sys.exit('  Program stopped!')

    if int(parameters_dict["width_line_freq"]) not in (0, 1, 2, 3, 4, 5, 6, 7, 8):
        print('\n  Error!!! Frequency width line is wrong!\n')
        sys.exit('  Program stopped!')

    if int(parameters_dict["width_line_freq"]) > ((int(parameters_dict["FFT_size_samples"]) - int(parameters_dict["start_line_freq"]) * 1024) / 2048): #1 … (SFFT-SLINE*1024)/1024
        print('\n  Error!!! Frequency width is bigger than FFT size allows!\n')
        sys.exit('  Program stopped!')

    if int(parameters_dict["clock_source"]) not in (0, 1):
        print('\n  Error!!! Clock source is wrong!\n')
        sys.exit('  Program stopped!')

    if int(parameters_dict["sum_diff_mode_num"]) not in (0, 1):
        print('\n  Error!!! Sum-diff mode is wrong!\n')
        sys.exit('  Program stopped!')

    '''
    if (int(parameters_dict["chan_diff_delay"]) < 0 or int(parameters_dict["chan_diff_dalay"]) > 1024):
        print('\n  Error!!! Channel difference delay is wrong!\n')
        sys.exit('  Program stopped!')
    '''
    print('\n   ADR parameters from file are correct!\n')

    return parameters_dict


def f_set_adr_parameters(serversocket, parameters_dict, print_or_not, pause = 0.5):
    '''
    Function sets ADR receiver parameters
    Input parameters:
        serversocket        - handle of socket to send and receive messages from server
        print_or_not        - to print the parameters to console (1) or not (0)
    Output parameters:
    '''

    # MDO parameters
    serversocket.send(('set prc/dsp/ctl/mdo 0 ' + str(parameters_dict["operation_mode_num"]) + '\0').encode())  # Set operation mode 0-6 (6 - correlation)
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    serversocket.send(('set prc/dsp/ctl/mdo 1 ' + str(parameters_dict["FFT_size_samples"]) + '\0').encode())  # Set FFT size 2048,4096,8192,16384,32768
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    serversocket.send(('set prc/dsp/ctl/mdo 2 ' + str(parameters_dict["spectra_averaging"]) + '\0').encode())  # Set number of averaged spectra in range [16 … 32768]
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    serversocket.send(('set prc/dsp/ctl/mdo 3 ' + str(parameters_dict["start_line_freq"]) + '\0').encode())  # Start frequency line of the band in 1024-steps. SLINE range [0 … (SFFT-1024)/1024]
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    serversocket.send(('set prc/dsp/ctl/mdo 4 ' + str(parameters_dict["width_line_freq"]) + '\0').encode())  # Width of frequency band in 1024-steps. WIDTH range [1 … (SFFT-SLINE*1024)/1024]
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    serversocket.send((b"set prc/srv/ctl/adr 3 1\0"))  # To apply the ADR DSP parameters (which is set in the [mdo]
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)



    # OPT parameters
    serversocket.send((b"set prc/dsp/ctl/opt 0 0\0"))  # On/Off the synchro start of ADR data processing by front of the PPS signal.
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    serversocket.send(('set prc/dsp/ctl/opt 1 ' + str(parameters_dict["clock_source"]) + '\0').encode())  # On/Off the external source of ADC CLC
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    serversocket.send((b"set prc/dsp/ctl/opt 2 1\0"))  # On/Off the FFT Hanning window
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    serversocket.send(('set prc/dsp/ctl/opt 3 ' + str(parameters_dict["sum_diff_mode_num"]) + '\0').encode())  # On/Off the “sum-difference” mode A±B
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    serversocket.send((b"set prc/srv/ctl/adr 6 1\0"))  # To apply the ADR DSP options, which are defined in [opt]
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)


    # SET parameters
    serversocket.send(('set prc/dsp/ctl/set 5 ' + str(parameters_dict["chan_diff_delay"]) + '\0').encode())  # Differential delay (DDEL) between CH-A and CH-B ADC sampling (CLC front) in picoseconds
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    serversocket.send((b"set prc/srv/ctl/adr 5 1\0"))  # To apply the ADR DSP settings, which are defined in [set]
    data = f_read_adr_meassage(serversocket, print_or_not)
    time.sleep(pause)

    return


################################################################################

if __name__ == '__main__':

    parameters_file = 'service_data/Param_full_band_0.1s_4096_spectra.txt'

    parameters_dict = f_read_adr_parameters_from_txt_file(parameters_file)
    parameters_dict = f_check_adr_parameters_correctness(parameters_dict)

    #f_set_adr_parameters_from_file(serversocket, parameters_dict, print_or_not, pause = 0.5):

    for y in parameters_dict:
        print (y, ' : ', parameters_dict[y])
