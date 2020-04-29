# Python3
Software_version = '2020.04.26'
Software_name = 'ADR control by schedule'
# Script controls the ADR radio astronomy receiver according to schedule txt file
# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************
host = '192.168.1.171'          # Receiver IP address in local network
schedule_txt_file = 'Observations.txt'
dir_data_on_server = '/media/data/DATA/To_process/'  # data folder on server, please do not change!
process_data = 1                # Copy data from receiver and process them?

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
CorrelationProcess = 0        # Process correlation data or save time?  (1 = process, 0 = save)
DynSpecSaveInitial = 0        # Save dynamic spectra pictures before cleaning (1 = yes, 0 = no) ?
DynSpecSaveCleaned = 1        # Save dynamic spectra pictures after cleaning (1 = yes, 0 = no) ?
CorrSpecSaveInitial = 0       # Save correlation Amp and Phase spectra pictures before cleaning (1 = yes, 0 = no) ?
CorrSpecSaveCleaned = 0       # Save correlation Amp and Phase spectra pictures after cleaning (1 = yes, 0 = no) ?
SpecterFileSaveSwitch = 1     # Save 1 immediate specter to TXT file? (1 = yes, 0 = no)
ImmediateSpNo = 100           # Number of immediate specter to save to TXT file
where_save_pics = 0           # Where to save result pictures? (0 - to script folder, 1 - to data folder)

averOrMin = 0                    # Use average value (0) per data block or minimum value (1)
VminMan = -120                   # Manual lower limit of immediate spectrum figure color range
VmaxMan = -10                    # Manual upper limit of immediate spectrum figure color range
VminNormMan = 0                  # Manual lower limit of normalized dynamic spectrum figure color range (usually = 0)
VmaxNormMan = 12                 # Manual upper limit of normalized dynamic spectrum figure color range (usually = 15)
AmplitudeReIm = 1 * 10**(-12)    # Color range of Re and Im dynamic spectra
                                 # 10 * 10**(-12) is typical value enough for CasA for interferometer of 2 GURT subarrays


# Rarely changes parameters:
port = 38386                    # Port of the receiver to connect (always 38386)
telegram_chat_id = '927534685'  # Telegram chat ID to send messages  - '927534685' - YeS
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
from multiprocessing import Process
from datetime import datetime
from pexpect import pxssh
from os import path
import time
import sys

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
from package_receiver_control.f_connect_to_adr_receiver import f_connect_to_adr_receiver
from package_receiver_control.f_wait_predefined_time_connected import f_wait_predefined_time_connected
from package_receiver_control.f_get_adr_parameters import f_get_adr_parameters
from package_receiver_control.f_synchronize_adr import f_synchronize_adr
from package_receiver_control.f_read_schedule_txt_for_adr import f_read_schedule_txt_for_adr
from package_common_modules.telegram_bot_sendtext import telegram_bot_sendtext
from package_common_modules.find_and_check_files_in_current_folder import find_and_check_files_in_current_folder
from package_ra_data_files_formats.ADR_file_reader import ADR_file_reader
from package_ra_data_files_formats.DAT_file_reader import DAT_file_reader


def copy_and_process(dir_data_on_server, data_directory_name, telegram_chat_id, host,
                        MaxNim, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                        VminCorrMag, VmaxCorrMag, customDPI, colormap, CorrelationProcess, DynSpecSaveInitial,
                        DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned, SpecterFileSaveSwitch,
                        ImmediateSpNo, averOrMin, VminMan, VmaxMan, VminNormMan, VmaxNormMan, AmplitudeReIm):

    time.sleep(10)

    # Copy data from receiver to server with SSH login on receiver and using rsync
    print('\n * Copying recorded data to server')

    s = pxssh.pxssh(timeout=120000)
    if not s.login(host, 'root', 'ghbtvybr'):
        print('\n   ERROR! SSH session failed on login!')
        print(str(s))
    else:
        print('\n   SSH login successful, copying data to server...\n')
        command = ('rsync -r ' + '/data/' + data_directory_name + '/' +
                   ' gurt@192.168.1.150:'+ dir_data_on_server + data_directory_name + '/')
        s.sendline(command)
        s.prompt()  # match the prompt
        # print('\n   Answer: ', s.before)  # print everything before the prompt.
        s.logout()
    # To make this work properly one needs to pair receiver and server via SSH to not ask password each time
    # Execute commands directly on the receiver or via ssh:
    # ssh-keygen
    # ssh-copy-id -i /root/.ssh/id_rsa.pub gurt@192.168.1.150

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

    print('\n * Data of ' + data_directory_name + ' observation were copied and processed.')

    # Sending message to Telegram
    message = 'Data of ' + data_directory_name + ' observation were copied and processed.'
    try:
        test = telegram_bot_sendtext(telegram_chat_id, message)
    except:
        pass

    return 1


def main_observation_control(host, port, schedule_txt_file, dir_data_on_server, process_data, telegram_chat_id,
                            Software_version, Software_name, MaxNim, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                            VminCorrMag, VmaxCorrMag, customDPI, colormap, CorrelationProcess, DynSpecSaveInitial,
                            DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned, SpecterFileSaveSwitch,
                            ImmediateSpNo, averOrMin, VminMan, VmaxMan, VminNormMan, VmaxNormMan, AmplitudeReIm):


    # *******************************************************************************
    #                           M A I N    P R O G R A M                            *
    # *******************************************************************************
    print ('\n\n\n\n\n\n\n\n   *********************************************************************')
    print ('   *            ', Software_name, '  v.', Software_version,'              *      (c) YeS 2020')
    print ('   ********************************************************************* \n\n\n')

    startTime = time.time()
    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%d.%m.%Y")
    print ('   Today is ', currentDate, ' time is ', currentTime, '\n')

    # Read schedule
    schedule = f_read_schedule_txt_for_adr(schedule_txt_file)

    '''
    Check correctness and recalculate the parameters to variables sent to ADR receiver
    '''
    # Printing overall schedule
    print('\n   *********************** OBSERVATIONS SCHEDULE ***********************')
    for obs_no in range (len(schedule)):
        print('   ' + schedule[obs_no][0] + ' - ' + schedule[obs_no][1] + '   DIR: ' + schedule[obs_no][6])
    print('   *********************************************************************')


    # Connect to the ADR receiver via socket
    serversocket, input_parameters_str = f_connect_to_adr_receiver(host, port, 1, 1)  # 1 - control, 1 - delay in sec

    # Update synchronization of PC and ADR
    f_synchronize_adr(serversocket, host)

    # Making separated IDs for each observation processing process
    p_processing = [None]*len(schedule)

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
            print('\n   Recording start time: ', schedule[obs_no][0])
            print('\n   Recording stop time:  ', schedule[obs_no][1],
                  '\n   *********************************************************************')
        else:
            sys.exit('\n\n * ERROR! Time limits are wrong!!! \n\n')


        # Prepare directory for data recording
        data_directory_name = schedule[obs_no][6]
        serversocket.send(('set prc/srv/ctl/pth ' + data_directory_name + '\0').encode())    # set directory to store data
        data = f_read_adr_meassage(serversocket, 0)
        #if data.startswith('SUCCESS'):
        #    print ('\n * Directory name changed to: ', data_directory_name)

        # Requesting and printing current ADR parameters
        parameters_dict = f_get_adr_parameters(serversocket, 1)


        '''
        To apply other parameters set in schedule
        '''

        # Waiting time to start record
        print('\n * Waiting time to synchronize and start recording...')
        ok = f_wait_predefined_time_connected(dt_time_to_start_record, serversocket, 1, host)

        # Start record
        serversocket.send('set prc/srv/ctl/srd 0 1\0'.encode())    # start data recording
        data = f_read_adr_meassage(serversocket, 0)
        if data.startswith('SUCCESS'):
            print ('\n * Recording started')

        # Waiting time to stop record
        ok = f_wait_predefined_time_connected(dt_time_to_stop_record, serversocket)

        # Stop record
        serversocket.send('set prc/srv/ctl/srd 0 0\0'.encode())    # stop data recording
        data = f_read_adr_meassage(serversocket, 0)
        if data.startswith('SUCCESS'):
            print ('\n * Recording stopped')


        # Sending message to Telegram
        message = 'GURT ' + data_directory_name.replace('_',' ') + ' observations completed!\nStart time: '\
                +schedule[obs_no][0] + '\nStop time: '+schedule[obs_no][1] + \
                '\nReceiver: '+ parameters_dict["receiver_name"].replace('_',' ') + \
                '\nDescription: ' + parameters_dict["file_description"].replace('_',' ') + \
                '\nMode: ' + parameters_dict["operation_mode_str"] + \
                '\nTime resolution: ' + str(round(parameters_dict["time_resolution"], 3)) + ' s.' + \
                '\nFrequency resolution: ' + str(round(parameters_dict["frequency_resolution"] / 1000, 3)) + ' kHz.' + \
                '\nFrequency range: ' + str(round(parameters_dict["lowest_frequency"] / 1000000, 3)) + ' - ' + \
                str(round(parameters_dict["highest_frequency"] / 1000000, 3)) + ' MHz'
        try:
            test = telegram_bot_sendtext(telegram_chat_id, message)
        except:
            pass

        # Data copying processing
        if process_data > 0:
            p_processing[obs_no] = Process(target = copy_and_process, args=(dir_data_on_server, data_directory_name,
                             telegram_chat_id, host, MaxNim, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                             VminCorrMag, VmaxCorrMag, customDPI, colormap, CorrelationProcess, DynSpecSaveInitial,
                             DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned, SpecterFileSaveSwitch,
                             ImmediateSpNo, averOrMin, VminMan, VmaxMan, VminNormMan, VmaxNormMan, AmplitudeReIm))
            p_processing[obs_no].start()

    if process_data > 0:
        for obs_no in range(len(schedule)):
            p_processing[obs_no].join()

    print ('\n\n           *** Program ', Software_name, ' has finished! *** \n\n\n')

################################################################################

if __name__ == '__main__':

    p_main = Process(target=main_observation_control, args=(host, port, schedule_txt_file, dir_data_on_server,
                            process_data, telegram_chat_id,
                            Software_version, Software_name, MaxNim, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
                            VminCorrMag, VmaxCorrMag, customDPI, colormap, CorrelationProcess, DynSpecSaveInitial,
                            DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned, SpecterFileSaveSwitch,
                            ImmediateSpNo, averOrMin, VminMan, VmaxMan, VminNormMan, VmaxNormMan, AmplitudeReIm))
    p_main.start()
    p_main.join()