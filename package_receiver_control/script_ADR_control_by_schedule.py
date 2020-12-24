# Python3
Software_version = '2020.12.25'
Software_name = 'ADR control by schedule'
# Script controls the ADR radio astronomy receiver according to schedule txt file
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
receiver_ip = '192.168.1.172'     # Receiver IP address in local network '192.168.1.171'
time_server = '192.168.1.150'     # IP of the time server (usually the control PC) '192.168.1.150'

# PROCESSING PARAMETERS
MaxNim = 1024                 # Number of data chunks for one figure
RFImeanConst = 8              # Constant of RFI mitigation (usually 8)
Vmin = -120                   # Lower limit of figure dynamic range for initial spectra
Vmax = -50                    # Upper limit of figure dynamic range for initial spectra
VminNorm = 0                  # Lower limit of figure dynamic range for normalized spectra
VmaxNorm = 10                 # Upper limit of figure dynamic range for normalized spectra
VminCorrMag = -150            # Lower limit of figure dynamic range for correlation magnitude spectra
VmaxCorrMag = -30             # Upper limit of figure dynamic range for correlation magnitude spectra
customDPI = 200               # Resolution of images of dynamic spectra
colormap = 'jet'              # Colormap of images of dynamic spectra ('jet', 'Purples' or 'Greys')
CorrelationProcess = 1        # Process correlation data or save time?  (1 = process, 0 = save)
DynSpecSaveInitial = 0        # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 1        # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 1       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
SpecterFileSaveSwitch = 1     # Save 1 immediate specter to TXT file? (1 = yes, 0 = no)
ImmediateSpNo = 1             # Number of immediate specter to save to TXT file
where_save_pics = 0           # Where to save result pictures? (0 - to script folder, 1 - to data folder)

averOrMin = 0                    # Use average value (0) per data block or minimum value (1)
VminMan = -120                   # Manual lower limit of immediate spectrum figure color range
VmaxMan = -10                    # Manual upper limit of immediate spectrum figure color range
VminNormMan = 0                  # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
VmaxNormMan = 12                 # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
AmplitudeReIm = 1 * 10**(-12)    # Color range of Re and Im dynamic spectra
                                 # 10 * 10**(-12) is typical value enough for CasA for interferometer of 2 GURT subarrays

# Rarely changes parameters:
dir_data_on_server = '/media/data/DATA/To_process/'  # data folder on server, please do not change!
port = 38386                    # Port of the receiver to connect (always 38386)
telegram_chat_id = '927534685'  # Telegram chat ID to send messages  - '927534685' - YeS
default_parameters_file = 'Param_full_band_0.1s_16384_corr_int-clc.txt'

if receiver_ip.endswith('171'):
    schedule_txt_file = 'Observations_ADR_01.txt'
    obs_log_file_name = 'service_data/ADR_01_Observations_log.txt'

elif receiver_ip.endswith('172'):
    schedule_txt_file = 'Observations_ADR_02.txt'
    obs_log_file_name = 'service_data/ADR_02_Observations_log.txt'
else:
    print('\n\n !!! Unknown receiver address !!!')

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
from multiprocessing import Process
from datetime import datetime
from os import path
import time
import sys

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_receiver_control.f_wait_predefined_time_connected import f_wait_predefined_time_connected
from package_receiver_control.f_read_schedule_txt_for_adr import f_read_schedule_txt_for_adr
from package_receiver_control.f_connect_to_adr_receiver import f_connect_to_adr_receiver
from package_receiver_control.f_get_adr_parameters import f_get_adr_parameters
from package_receiver_control.f_copy_data_from_adr import f_copy_data_from_adr
from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
from package_receiver_control.f_synchronize_adr import f_synchronize_adr
from package_receiver_control.f_initialize_adr import f_initialize_adr

from package_receiver_control.f_read_and_set_adr_parameters import f_read_adr_parameters_from_txt_file
from package_receiver_control.f_read_and_set_adr_parameters import f_check_adr_parameters_correctness
from package_receiver_control.f_read_and_set_adr_parameters import f_set_adr_parameters

from package_common_modules.find_and_check_files_in_current_folder import find_and_check_files_in_current_folder
from package_common_modules.telegram_bot_sendtext import telegram_bot_sendtext
from package_ra_data_files_formats.ADR_file_reader import ADR_file_reader
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader


def copy_and_process_adr(copy_data, process_data, dir_data_on_server, data_directory_name, parameters_dict,
                        telegram_chat_id, receiver_ip, MaxNim, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                        VminCorrMag, VmaxCorrMag, customDPI, colormap, CorrelationProcess, DynSpecSaveInitial,
                        DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned, SpecterFileSaveSwitch,
                        ImmediateSpNo, averOrMin, VminMan, VmaxMan, VminNormMan, VmaxNormMan, AmplitudeReIm):

    time.sleep(10)

    if copy_data > 0:
        ok = f_copy_data_from_adr(receiver_ip, data_directory_name, dir_data_on_server, 0)

    if process_data > 0:

        time.sleep(5)

        # Processing data with ADR reader and DAT reader

        # Find all files in folder once more:
        file_name_list_current = find_and_check_files_in_current_folder(dir_data_on_server+data_directory_name+'/','.adr')

        file_name_list_current.sort()

        print('\n\n * ADR reader analyses data... \n')

        # Making a name of folder for storing the result figures and txt files
        result_path = dir_data_on_server + data_directory_name + '/' + 'ADR_Results_' + data_directory_name

        for file in range(len(file_name_list_current)):
            file_name_list_current[file] = dir_data_on_server + data_directory_name + '/' + file_name_list_current[file]

        # Run ADR reader for the current folder
        ok, DAT_file_name, DAT_file_list = ADR_file_reader(file_name_list_current, result_path, MaxNim,
                                                           RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                                                           VminCorrMag, VmaxCorrMag, customDPI, colormap,
                                                           CorrelationProcess, 0, 1, 1, 1, 1, 0,
                                                           DynSpecSaveInitial, DynSpecSaveCleaned, CorrSpecSaveInitial,
                                                           CorrSpecSaveCleaned,
                                                           SpecterFileSaveSwitch, ImmediateSpNo, 0)

        print('\n * DAT reader analyzes file:', DAT_file_name, ', of types:', DAT_file_list, '\n')

        result_path = dir_data_on_server + data_directory_name + '/'

        # Run DAT reader for the results of current folder
        ok = DAT_file_reader('', DAT_file_name, DAT_file_list, result_path, data_directory_name,
                             averOrMin, 0, 0, VminMan, VmaxMan, VminNormMan, VmaxNormMan,
                             RFImeanConst, customDPI, colormap, 0, 0, 0, AmplitudeReIm, 0, 0, '', '', 0, 0, [], 0)

    message = ''
    if process_data > 0:
        message = 'Data of ' + data_directory_name.replace('_', ' ') + ' observations (' + parameters_dict[
            "receiver_name"].replace('_', ' ') + ' receiver, IP: ' + receiver_ip + ') were copied and processed.'
    else:
        if copy_data > 0:
             message = 'Data of ' + data_directory_name.replace('_', ' ') + ' observations (' + \
                       parameters_dict["receiver_name"].replace('_', ' ') + ' receiver, IP: ' + receiver_ip + ') were copied.'

    print('\n * ' + message)

    # Sending message to Telegram
    try:
       test = telegram_bot_sendtext(telegram_chat_id, message)
    except:
        pass

    return 1


# def main_observation_control(receiver_ip, port, schedule_txt_file, dir_data_on_server, copy_data, process_data,
def main_observation_control(receiver_ip, port, schedule_txt_file, dir_data_on_server, telegram_chat_id,
                            Software_version, Software_name, MaxNim, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                            VminCorrMag, VmaxCorrMag, customDPI, colormap, CorrelationProcess, DynSpecSaveInitial,
                            DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned, SpecterFileSaveSwitch,
                            ImmediateSpNo, averOrMin, VminMan, VmaxMan, VminNormMan, VmaxNormMan, AmplitudeReIm):

    # *******************************************************************************
    #                           M A I N    P R O G R A M                            *
    # *******************************************************************************
    print('\n\n\n\n\n\n\n\n   *********************************************************************')
    print('   *            ', Software_name, '  v.', Software_version,'              *      (c) YeS 2020')
    print('   ********************************************************************* \n\n\n')

    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")
    print('   Today is ', currentDate, ' time is ', currentTime, '\n')

    # Read schedule
    schedule = f_read_schedule_txt_for_adr(schedule_txt_file)

    # Check correctness of parameters in txt files
    for obs_no in range(len(schedule)):
        parameters_file = 'service_data/' + schedule[obs_no][10]
        parameters_dict = f_read_adr_parameters_from_txt_file(parameters_file)
        parameters_dict = f_check_adr_parameters_correctness(parameters_dict)
    del parameters_dict, parameters_file
    print('\n   Parameters of all observations have been checked, they seem OK.')

    # Make or open Log file
    obs_log_file = open(obs_log_file_name, "a")
    obs_log_file.write('\n ' + currentDate + ' ' + currentTime + ' New schedule loaded: \n')
    # Printing overall schedule
    print('\n   *********************** OBSERVATIONS SCHEDULE ***********************')
    for obs_no in range(len(schedule)):
        line = ' ' + schedule[obs_no][0] + ' - ' + schedule[obs_no][1] + '   DIR: ' + schedule[obs_no][6]
        print('  ' + line)
        obs_log_file.write(line + '\n')
    print('   *********************************************************************')

    # Close Log file
    obs_log_file.write('\n')
    obs_log_file.close()

    # Connect to the ADR receiver via socket
    serversocket, input_parameters_str = f_connect_to_adr_receiver(receiver_ip, port, 1, 1)  # 1 - control, 1 - delay in sec

    # Check if the receiver is initialized, if it is not - initialize it
    serversocket.send(b"set prc/srv/ctl/adr 3 1\0")
    data = f_read_adr_meassage(serversocket, 0)

    if 'Failed!' in data or 'Stopped' in data:

        # Initialize ADR and set ADR parameters
        f_initialize_adr(serversocket, receiver_ip, 0)

    # Update synchronization of PC and ADR
    f_synchronize_adr(serversocket, receiver_ip, time_server)

    # Making separated IDs for each observation processing process
    p_processing = [None] * len(schedule)

    # Preparing and starting observations
    for obs_no in range(len(schedule)):

        print('\n   *********************************************************************\n           Observation # ',
              obs_no + 1, ' of ', len(schedule), '  ', schedule[obs_no][6],
              '\n   *********************************************************************')

        # Construct datetime variables to start and stop observations
        dt_time = schedule[obs_no][0]
        dt_time_to_start_record = datetime(int(dt_time[0:4]), int(dt_time[5:7]), int(dt_time[8:10]),
                                           int(dt_time[11:13]), int(dt_time[14:16]), int(dt_time[17:19]), 0)

        dt_time = schedule[obs_no][1]
        dt_time_to_stop_record = datetime(int(dt_time[0:4]), int(dt_time[5:7]), int(dt_time[8:10]),
                                          int(dt_time[11:13]), int(dt_time[14:16]), int(dt_time[17:19]), 0)

        # Check the correctness of start and stop time
        if (dt_time_to_start_record < dt_time_to_stop_record) and (dt_time_to_start_record > datetime.now()):
            print('   Recording start time: ', schedule[obs_no][0])
            print('   Recording stop time:  ', schedule[obs_no][1],
                  '\n   *********************************************************************')
        else:
            sys.exit('\n\n * ERROR! Time limits are wrong!!! \n\n')

        # Prepare directory for data recording
        dt_time = schedule[obs_no][0]  # Taking date from schedule start time
        data_directory_name = dt_time[0:10].replace('-', '.') + '_GURT_' + schedule[obs_no][6]
        serversocket.send(('set prc/srv/ctl/pth ' + data_directory_name + '\0').encode())  # set directory to store data
        data = f_read_adr_meassage(serversocket, 0)

        # if data.startswith('SUCCESS'):
        #     print ('\n * Directory name changed to: ', data_directory_name)

        # Set observation description:
        serversocket.send(('set prc/srv/ctl/dsc ' + schedule[obs_no][7] + '\0').encode())
        data = f_read_adr_meassage(serversocket, 0)

        # Apply other receiver parameters set in schedule (parameters file)
        parameters_file = 'service_data/' + schedule[obs_no][10]
        parameters_dict = f_read_adr_parameters_from_txt_file(parameters_file)
        f_set_adr_parameters(serversocket, parameters_dict, 0, 0.5)

        # Requesting and printing current ADR parameters
        parameters_dict = f_get_adr_parameters(serversocket, 1)

        if obs_no+1 == len(schedule):
            message = 'Last observation in schedule on receiver: ' + parameters_dict["receiver_name"].replace('_', ' ') + \
                      ' (IP: ' + receiver_ip + ') was set. It will end on: ' + schedule[obs_no][1] + \
                      '. Please, consider adding of a new schedule!'
            try:
                test = telegram_bot_sendtext(telegram_chat_id, message)
            except:
                pass

        # Waiting time to start record
        print('\n * Waiting time to synchronize and start recording...')
        ok = f_wait_predefined_time_connected(dt_time_to_start_record, serversocket, 1, receiver_ip, time_server)

        # Start record
        serversocket.send('set prc/srv/ctl/srd 0 1\0'.encode())    # start data recording
        data = f_read_adr_meassage(serversocket, 0)
        if data.startswith('SUCCESS'):
            print('\n * Recording started')
            message = 'GURT ' + data_directory_name.replace('_', ' ') + \
                      ' observations started successfully!\nStart time: ' + \
                      schedule[obs_no][0] + '\nStop time: ' + schedule[obs_no][1] + \
                      '\nReceiver: ' + parameters_dict["receiver_name"].replace('_', ' ') + \
                      '\nReceiver IP: ' + receiver_ip + \
                      '\nDescription: ' + parameters_dict["file_description"].replace('_', ' ') + \
                      '\nMode: ' + parameters_dict["operation_mode_str"] + \
                      '\nTime resolution: ' + str(round(parameters_dict["time_resolution"], 3)) + ' s.' + \
                      '\nFrequency resolution: ' + str(round(parameters_dict["frequency_resolution"] / 1000, 3)) + \
                      ' kHz.' + '\nFrequency range: ' + str(round(parameters_dict["lowest_frequency"] / 1000000, 3)) + \
                      ' - ' + str(round(parameters_dict["highest_frequency"] / 1000000, 3)) + ' MHz'

            try:
                test = telegram_bot_sendtext(telegram_chat_id, message)
            except:
                pass

        # Waiting time to stop record
        ok = f_wait_predefined_time_connected(dt_time_to_stop_record, serversocket, 0, receiver_ip, time_server)

        # Stop record
        serversocket.send('set prc/srv/ctl/srd 0 0\0'.encode())    # stop data recording
        data = f_read_adr_meassage(serversocket, 0)
        if data.startswith('SUCCESS'):
            print('\n * Recording stopped')

        # Sending message to Telegram
        message = 'GURT ' + data_directory_name.replace('_', ' ') + ' observations completed!\nStart time: ' \
                  + schedule[obs_no][0] + '\nStop time: ' + schedule[obs_no][1] + \
                  '\nReceiver: ' + parameters_dict["receiver_name"].replace('_', ' ') + \
                  '\nReceiver IP: ' + receiver_ip + \
                  '\nDescription: ' + parameters_dict["file_description"].replace('_', ' ') + \
                  '\nMode: ' + parameters_dict["operation_mode_str"] + \
                  '\nTime resolution: ' + str(round(parameters_dict["time_resolution"], 3)) + ' s.' + \
                  '\nFrequency resolution: ' + str(round(parameters_dict["frequency_resolution"] / 1000, 3)) + ' kHz.' + \
                  '\nFrequency range: ' + str(round(parameters_dict["lowest_frequency"] / 1000000, 3)) + ' - ' + \
                  str(round(parameters_dict["highest_frequency"] / 1000000, 3)) + ' MHz'

        if schedule[obs_no][8] > 0 and schedule[obs_no][9] == 0:
            message = message + '\nData will be copied to GURT server.'

        if schedule[obs_no][9] > 0:
            message = message + '\nData will be copied to GURT server and processed.'

        # Open Log file and write the data message there
        obs_log_file = open(obs_log_file_name, "a")
        obs_log_file.write(message + '\n\n')
        obs_log_file.close()

        if obs_no + 1 == len(schedule):
            message = message + '\n\nIt was the last observation in schedule. Please, consider adding of a new schedule!'
        try:
            test = telegram_bot_sendtext(telegram_chat_id, message)
        except:
            pass

        # Data copying processing
        if schedule[obs_no][8] > 0 or schedule[obs_no][9] > 0:
            p_processing[obs_no] = Process(target=copy_and_process_adr, args=(schedule[obs_no][8], schedule[obs_no][9],
                             dir_data_on_server, data_directory_name, parameters_dict,
                             telegram_chat_id, receiver_ip, MaxNim, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                             VminCorrMag, VmaxCorrMag, customDPI, colormap, CorrelationProcess, DynSpecSaveInitial,
                             DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned, SpecterFileSaveSwitch,
                             ImmediateSpNo, averOrMin, VminMan, VmaxMan, VminNormMan, VmaxNormMan, AmplitudeReIm))
            p_processing[obs_no].start()

        # If it was the last observation, set the default parameters of the receiver
        if obs_no+1 == len(schedule):
            # Apply other receiver parameters set in schedule (parameters file)
            parameters_file = 'service_data/' + default_parameters_file
            parameters_dict = f_read_adr_parameters_from_txt_file(parameters_file)
            parameters_dict = f_check_adr_parameters_correctness(parameters_dict)
            f_set_adr_parameters(serversocket, parameters_dict, 0, 0.5)

    for obs_no in range(len(schedule)):
        if schedule[obs_no][8] > 0 or schedule[obs_no][9] > 0:
            p_processing[obs_no].join()

    print('\n\n           *** Program ', Software_name, ' has finished! *** \n\n\n')

################################################################################


if __name__ == '__main__':

    p_main = Process(target=main_observation_control, args=(receiver_ip, port, schedule_txt_file, dir_data_on_server,
                            telegram_chat_id,
                            Software_version, Software_name, MaxNim, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                            VminCorrMag, VmaxCorrMag, customDPI, colormap, CorrelationProcess, DynSpecSaveInitial,
                            DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned, SpecterFileSaveSwitch,
                            ImmediateSpNo, averOrMin, VminMan, VmaxMan, VminNormMan, VmaxNormMan, AmplitudeReIm))

    p_main.start()
    p_main.join()
