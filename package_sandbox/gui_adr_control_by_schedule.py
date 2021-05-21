import sys  # needed for running in Linux
import numpy as np
import time
import socket
import select
import tkinter.filedialog
from pexpect import pxssh
from os import path
from time import strftime
from datetime import datetime
from tkinter import *
from PIL import ImageTk, Image
from threading import Thread
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
from package_receiver_control.f_read_schedule_txt_for_adr import find_parameter_value
from package_receiver_control.f_read_and_set_adr_parameters import f_read_adr_parameters_from_txt_file
from package_receiver_control.f_initialize_adr import f_initialize_adr
from package_receiver_control.f_get_adr_parameters import f_get_adr_parameters
from package_receiver_control.f_read_and_set_adr_parameters import f_set_adr_parameters
from package_common_modules.text_manipulations import find_between

"""
The GUI program to control ADR receiver according to schedule
"""
software_version = '2021.05.08'

# *******************************************************************************
#                     R U N   S T A T E   V A R I A B L E S                     *
# *******************************************************************************
adr_ip = '192.168.1.172'
adr_port = 38386                    # Port of the receiver to connect (always 38386)
relay_host = '192.168.1.170'
relay_port = 6722
time_server_ip = '192.168.1.150'
default_parameters_file = 'Param_full_band_0.1s_16384_corr_int-clc.txt'
logo_path = 'media_data/gurt_logo.png'
x_space = (5, 5)
y_space = (5, 5)
y_space_adr = 1
colors = ['chartreuse2', 'SpringGreen2', 'yellow2', 'orange red', 'SlateBlue1', 'Deep sky blue']
block_flag = True
block_selecting_new_schedule_flag = False
adr_connection_flag = False
pause_update_info_flag = False
schedule = []
# *******************************************************************************
#                                F U N C T I O N S                              *
# *******************************************************************************


def time_show():
    """
    Renew time readings each second
    """
    loc_time_str = strftime('%Y . %m . %d     %H : %M : %S ')
    utc_time_str = strftime('%Y . %m . %d     %H : %M : %S ', time.gmtime())
    time_lbl.config(text='\n     Local:     ' + loc_time_str +
                         '     \n      UTC:      ' + utc_time_str + '     \n')
    time_lbl.after(1000, time_show)


def synchronize_adr(serversocket, receiver_ip, time_server):
    """
    Function reads a message from ADR radio astronomy receiver
    ntp server must be installed on server PC (sudo apt install ntp)
    to start ntp-server on server pc use "sudo /etc/init.d/ntp start" or/and "sudo systemctl restart ntp"
    Input parameters:
        serversocket        - handle of socket to send and receive messages from server
        receiver_ip                - IP address of receiver_ip to connect for sntp synchro from server
        time_server         - IP address of the ntp time server (probably PC where the script runs)
    Output parameters:
    """
    # Update synchronization of PC and ADR
    lbl_sync_status.config(text='Synchro', font='none 9', bg='Deep sky blue')
    synchro_error_flag = False
    receiver_file = open('service_data/receiver.txt', 'r')
    rec_user = receiver_file.readline()[:-1]
    password = receiver_file.readline()[:-1]
    receiver_file.close()

    # SSH connection to ADR receiver to send sntp command to synchronize with server
    s = pxssh.pxssh()
    if not s.login(receiver_ip, rec_user, password):
        # print('\n   ERROR! SSH session failed on login!')
        # print(str(s))
        lbl_sync_status.config(text='SSH log error!', font='none 9', bg='orange')
        synchro_error_flag = True
    else:
        # print('\n   SSH session login successful')
        s.sendline('sntp -P no -r ' + time_server)
        s.prompt()  # match the prompt
        # print('\n   Answer: ', s.before)  # print everything before the prompt.
        if s.before == ('sntp -P no -r ' + time_server_ip + '\r\n').encode():
            pass
        else:
            lbl_sync_status.config(text='sntp error!', font='none 9', bg='orange')
            synchro_error_flag = True
        s.logout()

    time.sleep(1)

    serversocket.send(b'set prc/dsp/ctl/clc 0 1\0')
    data_0 = f_read_adr_meassage(serversocket, 0)
    serversocket.send(b'set prc/srv/ctl/adr 6 1\0')
    data_1 = f_read_adr_meassage(serversocket, 0)
    if data_0.startswith('SUCCESS') and data_1.startswith('SUCCESS'):
        # print('\n   UTC absolute second set')
        pass
    else:
        lbl_sync_status.config(text='Abs sec error!', font='none 9', bg='orange')
        synchro_error_flag = True
        # print('\n   ERROR! UTC absolute second was not set!')

    time.sleep(3)

    serversocket.send(b'set prc/dsp/ctl/clc 0 0\0')  # tune second
    data_0 = f_read_adr_meassage(serversocket, 0)
    serversocket.send(b'set prc/dsp/ctl/clc 1 0\0')  # tune second
    data_1 = f_read_adr_meassage(serversocket, 0)
    serversocket.send(b'set prc/srv/ctl/adr 6 1\0')
    data_2 = f_read_adr_meassage(serversocket, 0)
    if data_0.startswith('SUCCESS') and data_1.startswith('SUCCESS') and data_2.startswith('SUCCESS'):
        # print('\n   UTC absolute second tuned')
        pass
    else:
        lbl_sync_status.config(text='Tune sec error!', font='none 9', bg='orange')
        synchro_error_flag = True
    if not synchro_error_flag:
        lbl_sync_status.config(text='Synchro', font='none 9', bg='chartreuse2')


def f_connect_to_adr_receiver(host, adr_port):   # UNUSED NOW !!!
    """
    Function connects to the ADR receiver via specified socket
    Input parameters:
        host                - IP address to connect
        adr_port                - port to connect
        control             - to control (1) or to view (0) possibility
        delay               - delay in seconds to wait after connection
    Output parameters:
        socket        - handle of socket to send and receive messages from server
        input_parameters_s  - long string with all receiver parameters at the moment of connection
    """
    control = 1
    delay = 0.2
    socket_adr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        lbl_adr_status.config(text='Connecting...', bg='yellow2')
        socket_adr.settimeout(10)
        socket_adr.connect((host, adr_port))
    except TimeoutError:
        lbl_adr_status.config(text='Failed!', bg='orange')
    except OSError:  # works in Linux when there is no such IP in the net
        lbl_adr_status.config(text='Failed!', bg='orange')
    else:
        pass
    finally:
        pass

    socket_adr.send('ADRSCTRL'.encode())
    register_cc_msg = bytearray([108, 0, 0, 0])
    register_cc_msg.extend(b'YeS\0                                                            ')  # Name 64 bytes
    register_cc_msg.extend(b'adrs\0                           ')   # Password 32 bytes
    register_cc_msg.extend([0, 0, 0, control])                     # Priv 4 bytes
    register_cc_msg.extend([0, 0, 0, control])                     # CTRL 4 bytes
    register_cc_msg = bytes(register_cc_msg)
    socket_adr.send(register_cc_msg)

    data = f_read_adr_meassage(socket_adr, 0)
    data = socket_adr.recv(108)
    if data[-1] == 1:
        lbl_mast_status.config(text='Control', font='none 9', bg='chartreuse2')
    else:
        lbl_mast_status.config(text='View only', font='none 9', bg='orange')
        lbl_control_status.config(text='ADR view only connection!', font='none 12', bg='orange')
    adr_connection_flag = True

    # Reading all parameters valid now
    input_parameters_str = ''
    for i in range(23):
        input_parameters_str += f_read_adr_meassage(socket_adr, 0)
    time.sleep(delay)   # Making pause to read the data
    return socket_adr, input_parameters_str


def get_adr_params_and_set_indication(socket_adr):
    parameters_dict = f_get_adr_parameters(socket_adr, 0)
    if   parameters_dict["operation_mode_num"] == 0: lbl_adr_mode_val.config(text='Waveform A')
    elif parameters_dict["operation_mode_num"] == 1: lbl_adr_mode_val.config(text='Waveform B')
    elif parameters_dict["operation_mode_num"] == 2: lbl_adr_mode_val.config(text='Waveform A & B')
    elif parameters_dict["operation_mode_num"] == 3: lbl_adr_mode_val.config(text='Spectra A')
    elif parameters_dict["operation_mode_num"] == 4: lbl_adr_mode_val.config(text='Spectra B')
    elif parameters_dict["operation_mode_num"] == 5: lbl_adr_mode_val.config(text='Spectra A & B')
    elif parameters_dict["operation_mode_num"] == 6: lbl_adr_mode_val.config(text='Correlation')
    else: parameters_dict["operation_mode_str"] = lbl_adr_mode_val.config(text='Unknown mode')

    tmp = format(parameters_dict["clock_frequency"], ',').replace(',', ' ').replace('.', ',') + '  Hz'
    lbl_adr_fadc_val.config(text=tmp)

    if parameters_dict["external_clock"] == 'OFF':
        lbl_adr_sadc_val.config(text="External", bg='yellow')
    elif parameters_dict["external_clock"] == 'ON':
        lbl_adr_sadc_val.config(text="Internal", bg='chartreuse2')

    tmp = format(parameters_dict["number_of_channels"], ',').replace(',', ' ').replace('.', ',')
    lbl_adr_chnl_val.config(text=tmp)
    lbl_adr_fres_val.config(text=str(np.round(parameters_dict["frequency_resolution"] / 1000, 3))+' kHz')
    lbl_adr_tres_val.config(text=str(np.round(parameters_dict["time_resolution"], 3))+' s')
    lbl_adr_flow_val.config(text=str(np.round(parameters_dict["lowest_frequency"]/1000000, 3))+' MHz')
    lbl_adr_fhig_val.config(text=str(np.round(parameters_dict["highest_frequency"]/1000000, 3))+' MHz')
    lbl_adr_rnam_val.config(text=parameters_dict["receiver_name"])
    lbl_adr_obsn_val.config(text=parameters_dict["observation_place"])
    lbl_adr_desc_val.config(text=parameters_dict["file_description"])
    lbl_adr_sdms_val.config(text=parameters_dict["sum_diff_mode"])
    if parameters_dict["sum_diff_mode"] == 'OFF':
        lbl_adr_sdms_val.config(bg='chartreuse2')
    elif parameters_dict["sum_diff_mode"] == 'ON':
        lbl_adr_sdms_val.config(bg='yellow')
    else:
        lbl_adr_sdms_val.config(bg='orange')

    if parameters_dict["files_autocreation"] > 0:
        lbl_adr_nfcs_val.config(text='ON', bg='chartreuse2')
    else:
        lbl_adr_nfcs_val.config(text='OFF', bg='yellow')

    # parameters_dict["data_recording"]
    # parameters_dict["size_of_file"]
    # parameters_dict["time_of_file"]


def start_and_keep_adr_connection():
    global socket_adr, host_adr, pause_update_info_flag
    host_adr = ent_adr_ip.get()
    socket_adr, input_parameters_str = f_connect_to_adr_receiver(host_adr, adr_port)
    time.sleep(0.2)
    # Check if the receiver is initialized, if it is not - initialize it
    socket_adr.send(b"set prc/srv/ctl/adr 3 1\0")
    data = f_read_adr_meassage(socket_adr, 0)
    if 'Failed!' in data or 'Stopped' in data:
        lbl_recd_status.config(text='Initializing ADR...', font='none 12', bg='orange')
        # Initialize ADR and set ADR parameters
        f_initialize_adr(socket_adr, host_adr, 0)
        lbl_recd_status.config(text='Waiting', font='none 12', bg='light gray')

    # Update synchronization of PC and ADR
    synchronize_adr(socket_adr, host_adr, time_server_ip)
    lbl_adr_status.config(text='Connected', bg='chartreuse2')
    if schedule == []:
        lbl_control_status.config(text='Schedule is empty', bg='light gray')
    else:
        lbl_control_status.config(text='Ready to start', bg='chartreuse2')
    # Apply default receiver parameters set in schedule (parameters file)
    parameters_file = 'service_data/' + default_parameters_file
    parameters_dict = f_read_adr_parameters_from_txt_file(parameters_file)
    parameters_dict, error_msg = check_adr_parameters_correctness(parameters_dict)
    if error_msg == '':
        lbl_recd_status.config(text='Setting ADR parameters...', bg='yellow')
        f_set_adr_parameters(socket_adr, parameters_dict, 0, 0.5)
        lbl_recd_status.config(text='Waiting', font='none 12', bg='light gray')
    get_adr_params_and_set_indication(socket_adr)

    while True:
        time.sleep(1)
        if pause_update_info_flag:
            pass
        else:
            # Keeping connection active
            socket_adr.send('get prc/srv/ctl/adr 0 \0'.encode())
            data = f_read_adr_meassage(socket_adr, 0)

            # tmp = find_between(data, 'DSP Time: ', '\nPC1 Time:')  # Current time of DSP
            # tmp = find_between(data, 'PC1 Time: ', '\nPC2 Time:')  # Current time of PC1
            # tmp = find_between(data, 'PC2 Time: ', '\nFileSize:')  # Current time of PC2

            tmp = float(find_between(data, 'FileSize: ', '\nFileTime:'))  # Current file size in bytes
            tmp = '{:.1f} Mb'.format(tmp)
            lbl_adr_cfsz_val.config(text=tmp)
            tmp = float(find_between(data, 'FileTime: ', '\nF_ADC:'))  # Current file length in seconds
            tmp = '{:.1f} s'.format(tmp)
            lbl_adr_cfln_val.config(text=tmp)

            tmp = int(find_between(data, 'F_ADC: ', '\nFS_FREE'))  # ADC frequency indication
            tmp = format(tmp, ',').replace(',', ' ').replace('.', ',') + '  Hz'
            lbl_adr_fadc_val.config(text=tmp, font='none 10 bold')

            tmp = int(float(find_between(data, 'FS_FREE: ', '\nFS_PERC:')) / 1000)  # Free space in bytes
            tmp = format(tmp, ',').replace(',', ' ').replace('.', ',')
            lbl_adr_frsb_val.config(text=str(tmp) + ' GB')
            tmp = float(find_between(data, 'FS_PERC: ', '\n'))  # Free space in %
            tmp = '{:.1f} %'.format(tmp)
            lbl_adr_frsp_val.config(text=tmp)


def start_adr_connection_thread():
    adr_connection_thread = Thread(target=start_and_keep_adr_connection, daemon=True)
    adr_connection_thread.start()


def read_schedule_txt_file(schedule_txt_file):
    """
    Read ADR (GURT) observations schedule from txt file of predefined format
    """
    schedule = []
    file = open(schedule_txt_file, "r")
    for line in file:
        if line.strip().startswith('#'):
            pass
        elif line.strip().startswith('START:'):
            line = line.replace(' ', '').rstrip('\n')
            start_time = find_parameter_value(line, 'START:')
            fft_size = find_parameter_value(line, 'FFT:')
            time_resolution = find_parameter_value(line, 'DT:')
            start_frequency = find_parameter_value(line, 'FSTART:')
            stop_frequency = find_parameter_value(line, 'FSTOP:')
            data_directory = find_parameter_value(line, 'NAME:')
            file_description = find_parameter_value(line, 'DESCR:')
            param_file_name = find_parameter_value(line, 'PARAM:')
        elif line.strip().startswith('STOP:'):
            line = line.replace(' ', '').rstrip('\n')
            stop_time = find_parameter_value(line, 'STOP:')
            copy_or_not = int(find_parameter_value(line, 'COPY:'))
            process_or_not = int(find_parameter_value(line, 'PROC:'))

            # The condition: to process you must copy data
            if process_or_not > 0:
                copy_or_not = 1
            # Adding parameters to list
            schedule.append([start_time[:10] + ' ' + start_time[10:], stop_time[:10] + ' ' + stop_time[10:], fft_size,
                             time_resolution, start_frequency, stop_frequency, data_directory, file_description,
                             copy_or_not, process_or_not, param_file_name])
        else:
            pass
    return schedule


def check_correctness_of_schedule(schedule):
    """
    Check time correctness (later then now, start is before stop): storing them in datetime format in one list
    """
    time_line = []
    schedule_comment_text = ''
    for item in range(len(schedule)):
        time_point = schedule[item][0]
        dt_time = datetime(int(time_point[0:4]), int(time_point[5:7]), int(time_point[8:10]),
                           int(time_point[11:13]), int(time_point[14:16]), int(time_point[17:19]), 0)
        time_line.append(dt_time)
        time_point = schedule[item][1]
        dt_time = datetime(int(time_point[0:4]), int(time_point[5:7]), int(time_point[8:10]),
                           int(time_point[11:13]), int(time_point[14:16]), int(time_point[17:19]), 0)
        time_line.append(dt_time)

    # Verifying that time limits in list go one after another
    for item in range(2 * len(schedule) - 1):
        if time_line[item+1] > time_line[item]:
            pass
        else:
            schedule_comment_text += ' Time is not in right order!'

    # Check if the first time in the list is in future
    now = datetime.now()
    diff = int((time_line[0] - now).total_seconds())
    if diff <= 0:
        schedule_comment_text += ' Time is in the past!'

    if schedule_comment_text == '':
        schedule_comment_text = 'Schedule seems to be OK, number of observations: ' + str(len(schedule))
        lbl_scedule_comments.config(text=schedule_comment_text, font='none 9 bold', fg="Dark blue", bg='gray95')
    else:
        lbl_scedule_comments.config(text=schedule_comment_text, font='none 9 bold', fg="black", bg="orange")
    return schedule


def check_adr_parameters_correctness(dict):
    """
    Checks dictionary with ADR parameters to set for correct values
    """
    error_msg = ''
    if int(dict["operation_mode_num"]) not in (0, 1, 2, 3, 4, 5, 6):
        error_msg += 'Operation mode is wrong!'
    if int(dict["FFT_size_samples"]) not in (2048, 4096, 8192, 16384, 32768):
        error_msg += 'FFT size is wrong!'
    if int(dict["operation_mode_num"])  == 6 and int(dict["FFT_size_samples"]) == 32768:
        error_msg += 'FFT size and ADR mode are incompatible!'
    if int(dict["spectra_averaging"]) < 16 or int(dict["spectra_averaging"]) > 32768:
        error_msg += 'Spectra averaging number is wrong!'
    if int(dict["start_line_freq"]) not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16):   # 0 … (SFFT-1024)/1024
        error_msg += 'Start frequency line is wrong!'
    if int(dict["width_line_freq"]) not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16):
        error_msg += 'Frequency width line is wrong!'
    if int(dict["width_line_freq"]) > ((int(dict["FFT_size_samples"]) - int(dict["start_line_freq"]) * 1024) / 1024): # 1 … (SFFT-SLINE*1024)/1024
        error_msg += 'Frequency width is bigger than FFT size allows!'
    if int(dict["clock_source"]) not in (0, 1):
        error_msg += 'Clock source is wrong!'
    if int(dict["sum_diff_mode_num"]) not in (0, 1):
        error_msg += 'Sum-diff mode is wrong!'
    if int(dict["data_file_size"]) < -1 or int(dict["data_file_size"]) > 4096:
        error_msg += 'File size value is wrong!'
    '''
    if (int(dict["chan_diff_delay"]) < 0 or int(parameters_dict["chan_diff_dalay"]) > 1024):
        error_msg += 'Channel difference delay is wrong!'
    '''
    return dict, error_msg


def check_parameters_of_observations(schedule):
    # Check correctness of parameters in txt files
    for obs_no in range(len(schedule)):
        parameters_file = 'service_data/' + schedule[obs_no][10]
        try:
            parameters_dict = f_read_adr_parameters_from_txt_file(parameters_file)
        except FileNotFoundError:
            lbl_scedule_comments.config(text='File not found: ' + schedule[obs_no][10],
                                        font='none 9 bold', fg="black", bg="orange")
        else:
            pass
        finally:
            pass
        parameters_dict, error_msg = check_adr_parameters_correctness(parameters_dict)
        if error_msg != '':
            text = 'Error in parameters observation # ' + str(obs_no+1) + ': ' + error_msg
            lbl_scedule_comments.config(text=text, font='none 9 bold', fg="black", bg="orange")
    del parameters_dict, parameters_file


def load_schedule_to_gui(schedule):
    ent_schedule.config(state=NORMAL)
    ent_schedule.delete('1.0', END)  # Erase everything from the schedule window
    first_line_of_schedule = "No | Start date / time |  | Stop date / time   |  Source  |  Description   \n"
    ent_schedule.insert(INSERT, first_line_of_schedule, 'first_line')
    ent_schedule.tag_config('first_line', background='light green')
    for obs_no in range(len(schedule)):
        line = '{:3d}'.format(obs_no+1) + ' ' + schedule[obs_no][0] + ' to ' + schedule[obs_no][1] + \
               '  ' + '{:10s}'.format(schedule[obs_no][6]) + ' ' + '{:25s}'.format(schedule[obs_no][7]) + '\n'
        ent_schedule.insert(INSERT, line, str(obs_no+1))
    ent_schedule.config(state=DISABLED)


def start_choose_schedule_file_thread():
    schedule_choose_thread = Thread(target=choose_schedule_file, daemon=True)
    schedule_choose_thread.start()


def choose_schedule_file():
    if not block_selecting_new_schedule_flag:
        global schedule
        filetypes = (('text files', '*.txt'), ('All files', '*.*'))
        file_path = tkinter.filedialog.askopenfilename(title='Open a file', filetypes=filetypes)
        entry_schedule_file.delete(0, END)
        entry_schedule_file.insert(0, file_path)
        schedule = read_schedule_txt_file(file_path)
        if schedule == []:
            lbl_scedule_comments.config(text='Schedule is empty!', font='none 9 bold', fg="black", bg="orange")
            ent_schedule.config(state=NORMAL)
            ent_schedule.delete('1.0', END)  # Erase everything from the schedule window
            ent_schedule.config(state=DISABLED)
        check_correctness_of_schedule(schedule)
        check_parameters_of_observations(schedule)
        load_schedule_to_gui(schedule)


def block_control_button():
    if block_flag:
        unblock_control_by_schedule()
    else:
        block_control_by_schedule()


def block_control_by_schedule():
    global block_flag
    block_flag = True
    btn_start_unblock.config(text='UNBLOCK')
    btn_start_schedule.config(fg='gray')
    btn_send_tg_messages.config(state=DISABLED)


def unblock_control_by_schedule():
    global block_flag
    block_flag = False
    btn_start_unblock.config(text='BLOCK')
    btn_start_schedule.config(fg='black')
    btn_send_tg_messages.config(state=NORMAL)


def wait_predefined_time(time_to_start, serversocket, synchro=0, host='192.168.1.171', time_server='192.168.1.150'):
    """
    Function waits the predefined time and once a minute reads something from ADR receiver to
    save connection to ADR server
    Input parameters:
        time_to_start       - datetime variable with time to continue the script
        serversocket        - socket handle to keep the connection alive
        synchro             - to synchronize the receiver before timer end (1 - yes, 0 - no)
    Output parameter:
        result              - boolean variable (1) if time was chosen correctly (0) if not
    """
    global pause_update_info_flag
    now = datetime.now()
    diff = int((time_to_start - now).total_seconds())
    if diff > 0:
        result = True
        # Wait minutes
        if int(diff / 60) > 0:
            while True:
                time.sleep(60)
                now = datetime.now()
                diff = int((time_to_start - now).total_seconds())
                if int(diff / 60) <= 1:
                    break
        if synchro > 0:
            # Update synchronization of PC and ADR
            # synchro_flag = True
            pause_update_info_flag = True
            synchronize_adr(serversocket, host, time_server)
            pause_update_info_flag = False

        # Wait seconds
        while True:
            time.sleep(1)
            now = datetime.now()
            diff = int((time_to_start - now).total_seconds())
            if diff < 1:
                break
    else:
        result = False  # Time has passed!
    return result


def start_control_by_schedule_button():
    control_thread = Thread(target=start_control_by_schedule, daemon=True)
    control_thread.start()


def start_control_by_schedule():
    global block_selecting_new_schedule_flag
    if not block_flag:
        # if adr_connection_flag:
        block_selecting_new_schedule_flag = True
        btn_select_file.config(fg='gray')
        ent_schedule.tag_config('1', background='yellow')
        lbl_control_status.config(text='Schedule in progress!', bg='Deep sky blue')

        control_by_schedule()

        # time.sleep(15)

        block_selecting_new_schedule_flag = False
        btn_select_file.config(fg='black')
        lbl_control_status.config(text='Waiting to start', bg='light gray')


def control_by_schedule():
    global pause_update_info_flag
    print('Len:', len(schedule))
    # Preparing and starting observations
    for obs_no in range(len(schedule)):

        # Construct datetime variables to start and stop observations
        dt_time = schedule[obs_no][0]
        dt_time_to_start_record = datetime(int(dt_time[0:4]), int(dt_time[5:7]), int(dt_time[8:10]),
                                           int(dt_time[11:13]), int(dt_time[14:16]), int(dt_time[17:19]), 0)

        dt_time = schedule[obs_no][1]
        dt_time_to_stop_record = datetime(int(dt_time[0:4]), int(dt_time[5:7]), int(dt_time[8:10]),
                                          int(dt_time[11:13]), int(dt_time[14:16]), int(dt_time[17:19]), 0)

        # Check the correctness of start and stop time
        if (dt_time_to_start_record < dt_time_to_stop_record) and (dt_time_to_start_record > datetime.now()):
            pass
        else:
            break

        # Prepare directory for data recording
        dt_time = schedule[obs_no][0]  # Taking date from schedule start time
        data_directory_name = dt_time[0:10].replace('-', '.') + '_GURT_' + schedule[obs_no][6]
        pause_update_info_flag = True
        socket_adr.send(('set prc/srv/ctl/pth ' + data_directory_name + '\0').encode())  # set directory to store data
        data = f_read_adr_meassage(socket_adr, 0)

        # Set observation description:
        socket_adr.send(('set prc/srv/ctl/dsc ' + schedule[obs_no][7] + '\0').encode())
        data = f_read_adr_meassage(socket_adr, 0)

        # Apply other receiver parameters set in schedule (parameters file)
        parameters_file = 'service_data/' + schedule[obs_no][10]
        parameters_dict = f_read_adr_parameters_from_txt_file(parameters_file)
        lbl_recd_status.config(text='Setting ADR parameters...', font='none 12', bg='yellow')
        f_set_adr_parameters(socket_adr, parameters_dict, 0, 0.5)
        lbl_recd_status.config(text='Waiting', font='none 12', bg='light gray')
        pause_update_info_flag = False

        # # Requesting and printing current ADR parameters
        # parameters_dict = f_get_adr_parameters(socket_adr, 1)

        # if obs_no+1 == len(schedule):
        #     message = 'Last observation in schedule on receiver: ' + parameters_dict["receiver_name"].replace('_', ' ') + \
        #               ' (IP: ' + host_adr + ') was set. It will end on: ' + schedule[obs_no][1] + \
        #               '. Please, consider adding of a new schedule!'
        #     try:
        #         test = telegram_bot_sendtext(telegram_chat_id, message)
        #     except:
        #         pass

        # Waiting time to start record
        ok = wait_predefined_time(dt_time_to_start_record, socket_adr, 1, host_adr, time_server_ip)

        # Start record
        pause_update_info_flag = True
        socket_adr.send('set prc/srv/ctl/srd 0 1\0'.encode())    # start data recording
        data = f_read_adr_meassage(socket_adr, 0)
        pause_update_info_flag = False
        if data.startswith('SUCCESS'):
            lbl_recd_status.config(text='Recording!',  bg='Deep sky blue')
        else:
            lbl_recd_status.config(text='Failed to start record!', bg='orange')

        # if data.startswith('SUCCESS'):
        #     print('\n * Recording started')
        #     message = 'GURT ' + data_directory_name.replace('_', ' ') + \
        #               ' observations started successfully!\nStart time: ' + \
        #               schedule[obs_no][0] + '\nStop time: ' + schedule[obs_no][1] + \
        #               '\nReceiver: ' + parameters_dict["receiver_name"].replace('_', ' ') + \
        #               '\nReceiver IP: ' + receiver_ip + \
        #               '\nDescription: ' + parameters_dict["file_description"].replace('_', ' ') + \
        #               '\nMode: ' + parameters_dict["operation_mode_str"] + \
        #               '\nTime resolution: ' + str(round(parameters_dict["time_resolution"], 3)) + ' s.' + \
        #               '\nFrequency resolution: ' + str(round(parameters_dict["frequency_resolution"] / 1000, 3)) + \
        #               ' kHz.' + '\nFrequency range: ' + str(round(parameters_dict["lowest_frequency"] / 1000000, 3)) + \
        #               ' - ' + str(round(parameters_dict["highest_frequency"] / 1000000, 3)) + ' MHz'
        #
        #     try:
        #         test = telegram_bot_sendtext(telegram_chat_id, message)
        #     except:
        #         pass

        # Waiting time to stop record
        ok = wait_predefined_time(dt_time_to_stop_record, socket_adr, 0, host_adr, time_server_ip)

        # Stop record
        pause_update_info_flag = True
        socket_adr.send('set prc/srv/ctl/srd 0 0\0'.encode())    # stop data recording
        data = f_read_adr_meassage(socket_adr, 0)
        pause_update_info_flag = False
        if data.startswith('SUCCESS'):
            lbl_recd_status.config(text='Waiting...',  bg='light gray')
        else:
            lbl_recd_status.config(text='Failed to stop record!', bg='orange')

        # if data.startswith('SUCCESS'):
        #     print('\n * Recording stopped')

        # # Sending message to Telegram
        # message = 'GURT ' + data_directory_name.replace('_', ' ') + ' observations completed!\nStart time: ' \
        #           + schedule[obs_no][0] + '\nStop time: ' + schedule[obs_no][1] + \
        #           '\nReceiver: ' + parameters_dict["receiver_name"].replace('_', ' ') + \
        #           '\nReceiver IP: ' + host_adr + \
        #           '\nDescription: ' + parameters_dict["file_description"].replace('_', ' ') + \
        #           '\nMode: ' + parameters_dict["operation_mode_str"] + \
        #           '\nTime resolution: ' + str(round(parameters_dict["time_resolution"], 3)) + ' s.' + \
        #           '\nFrequency resolution: ' + str(round(parameters_dict["frequency_resolution"] / 1000, 3)) + ' kHz.' + \
        #           '\nFrequency range: ' + str(round(parameters_dict["lowest_frequency"] / 1000000, 3)) + ' - ' + \
        #           str(round(parameters_dict["highest_frequency"] / 1000000, 3)) + ' MHz'
        #
        # if schedule[obs_no][8] > 0 and schedule[obs_no][9] == 0:
        #     message = message + '\nData will be copied to GURT server.'
        #
        # if schedule[obs_no][9] > 0:
        #     message = message + '\nData will be copied to GURT server and processed.'

        # # Open Log file and write the data message there
        # obs_log_file = open(obs_log_file_name, "a")
        # obs_log_file.write(message + '\n\n')
        # obs_log_file.close()

        # if obs_no + 1 == len(schedule):
        #     message = message + '\n\nIt was the last observation in schedule. Please, consider adding of a new schedule!'
        # try:
        #     test = telegram_bot_sendtext(telegram_chat_id, message)
        # except:
        #     pass

        # # Data copying processing
        # if schedule[obs_no][8] > 0 or schedule[obs_no][9] > 0:
        #     p_processing[obs_no] = Process(target=copy_and_process_adr, args=(schedule[obs_no][8], schedule[obs_no][9],
        #                      dir_data_on_server, data_directory_name, parameters_dict,
        #                      telegram_chat_id, host_adr, MaxNim, RFImeanConst, Vmin, Vmax, VminNorm, VmaxNorm,
        #                      VminCorrMag, VmaxCorrMag, customDPI, colormap, CorrelationProcess, DynSpecSaveInitial,
        #                      DynSpecSaveCleaned, CorrSpecSaveInitial, CorrSpecSaveCleaned, SpecterFileSaveSwitch,
        #                      ImmediateSpNo, averOrMin, VminMan, VmaxMan, VminNormMan, VmaxNormMan, AmplitudeReIm))
        #     p_processing[obs_no].start()

        # If it was the last observation, set the default parameters of the receiver
        if obs_no+1 == len(schedule):
            # # Apply other receiver parameters set in schedule (parameters file)
            # parameters_file = 'service_data/' + default_parameters_file
            # parameters_dict = f_read_adr_parameters_from_txt_file(parameters_file)
            # parameters_dict = f_check_adr_parameters_correctness(parameters_dict)
            # f_set_adr_parameters(socket_adr, parameters_dict, 0, 0.5)

            # Apply default receiver parameters set in schedule (parameters file)
            parameters_file = 'service_data/' + default_parameters_file
            parameters_dict = f_read_adr_parameters_from_txt_file(parameters_file)
            parameters_dict, error_msg = check_adr_parameters_correctness(parameters_dict)
            if error_msg == '':
                lbl_recd_status.config(text='Setting ADR parameters', bg='yellow')
                pause_update_info_flag = True
                f_set_adr_parameters(socket_adr, parameters_dict, 0, 0.5)
                pause_update_info_flag = False
                lbl_recd_status.config(text='Waiting', font='none 12', bg='light gray')

    # for obs_no in range(len(schedule)):
    #     if schedule[obs_no][8] > 0 or schedule[obs_no][9] > 0:
    #         p_processing[obs_no].join()


# *******************************************************************************
#                             M A I N    W I N D O W                            *
# *******************************************************************************

window = Tk()
window.title('ADR control GUI v.' + software_version + ' (c) YeS')
window.rowconfigure(0, minsize=30, weight=1)
window.columnconfigure(1, minsize=40, weight=1)

# Setting tabs in the main window
tab_parent = ttk.Notebook(window)
tab_main = ttk.Frame(tab_parent)
tab_graphics = ttk.Frame(tab_parent)
tab_schedule = ttk.Frame(tab_parent)
tab_connection_control = ttk.Frame(tab_parent)
tab_settings = ttk.Frame(tab_parent)
tab_parent.add(tab_main, text='   Main window   ')
tab_parent.add(tab_graphics, text='   Plots   ')
tab_parent.add(tab_schedule, text='   Create schedule   ')
tab_parent.add(tab_connection_control, text='   Devices connection   ')
tab_parent.add(tab_settings, text='   Settings   ')
tab_parent.pack(expand=1, fill="both")


# *******************************************************************************
#                               M A I N    T A B                                *
# *******************************************************************************


# Setting frames in tab "Main window"
time_lbl = Label(tab_main, font=('none', 14, 'bold'), background='black', foreground='yellow')

frame_adr_status = LabelFrame(tab_main, text="ADR connection status")
frame_schedule = LabelFrame(tab_main, text="Schedule (local time is used)")
frame_load_schedule = LabelFrame(tab_main, text="Load schedule")
frame_control = LabelFrame(tab_main, text="Control ADR by schedule")
time_lbl.grid(row=0, column=0, rowspan=1, columnspan=1, stick='wens', padx=10, pady=10)
text = 'v.' + software_version + ' (c) IRA NASU   Serge Yerin (YeS)   e-mail: yerin.serge@gmail.com'
lbl_copyright = Label(tab_main, text=text)
lbl_copyright.config(font=("Arial", 8), fg="dark blue")

frame_adr_status.grid(row=1, column=0, rowspan=1, columnspan=1, stick='wn', padx=10, pady=10)
frame_schedule.grid(row=0, column=1, rowspan=5, columnspan=1, stick='wn', padx=10, pady=10)
frame_load_schedule.grid(row=2, column=0, rowspan=1, columnspan=1, stick='wne', padx=10, pady=10)
frame_control.grid(row=3, column=0, rowspan=1, columnspan=1, stick='wne', padx=10, pady=10)
lbl_copyright.grid(row=4, column=0, rowspan=1, columnspan=2, stick='e', padx=1, pady=1)


# Setting elements of the frame "ADR status"
btn_adr_connect = Button(frame_adr_status, text="Connect to ADR", relief='raised', width=15,
                         command=start_adr_connection_thread)
lbl_adr_status = Label(frame_adr_status, text='Disconnected', font='none 12', width=12, bg='light gray')
lbl_adr_ip = Label(frame_adr_status, text="ADR IP address:")
ent_adr_ip = Entry(frame_adr_status, width=15)
ent_adr_ip.insert(0, adr_ip)

btn_adr_connect.grid(row=0, column=0, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
lbl_adr_status.grid(row=0, column=1, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
lbl_adr_ip.grid(row=0, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space)
ent_adr_ip.grid(row=0, column=3, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)

lbl_adr_fadc_nam = Label(frame_adr_status, text="ADC frequency:")
lbl_adr_fadc_val = Label(frame_adr_status, text="", font='none 10 bold')
lbl_adr_sadc_nam = Label(frame_adr_status, text="ADC source:")
lbl_adr_sadc_val = Label(frame_adr_status, text="Unknown", font='none 9', width=12, bg='light gray')

lbl_adr_fadc_nam.grid(row=1, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_fadc_val.grid(row=1, column=1, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)
lbl_adr_sadc_nam.grid(row=1, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_sadc_val.grid(row=1, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_mode_nam = Label(frame_adr_status, text="ADR mode:")
lbl_adr_mode_val = Label(frame_adr_status, text="", font='none 10 bold')
lbl_adr_chnl_nam = Label(frame_adr_status, text="Channels:")
lbl_adr_chnl_val = Label(frame_adr_status, text="", font='none 10 bold')

lbl_adr_mode_nam.grid(row=2, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_mode_val.grid(row=2, column=1, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)
lbl_adr_chnl_nam.grid(row=2, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_chnl_val.grid(row=2, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_fres_nam = Label(frame_adr_status, text="Frequency resolution:")
lbl_adr_fres_val = Label(frame_adr_status, text="", font='none 10 bold')
lbl_adr_tres_nam = Label(frame_adr_status, text="Time resolution:")
lbl_adr_tres_val = Label(frame_adr_status, text="", font='none 10 bold')

lbl_adr_fres_nam.grid(row=3, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_fres_val.grid(row=3, column=1, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)
lbl_adr_tres_nam.grid(row=3, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_tres_val.grid(row=3, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_flow_nam = Label(frame_adr_status, text="Lowest frequency:")
lbl_adr_flow_val = Label(frame_adr_status, text="", font='none 10 bold')
lbl_adr_fhig_nam = Label(frame_adr_status, text="Highest frequency:")
lbl_adr_fhig_val = Label(frame_adr_status, text="", font='none 10 bold')

lbl_adr_flow_nam.grid(row=4, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_flow_val.grid(row=4, column=1, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)
lbl_adr_fhig_nam.grid(row=4, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_fhig_val.grid(row=4, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_rnam_nam = Label(frame_adr_status, text="Receiver name:")
lbl_adr_rnam_val = Label(frame_adr_status, text="", font='none 10 bold')
lbl_adr_rnam_nam.grid(row=5, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_rnam_val.grid(row=5, column=1, rowspan=1, columnspan=3, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_obsn_nam = Label(frame_adr_status, text="Observatory:")
lbl_adr_obsn_val = Label(frame_adr_status, text="", font='none 10 bold')
lbl_adr_obsn_nam.grid(row=6, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_obsn_val.grid(row=6, column=1, rowspan=1, columnspan=3, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_desc_nam = Label(frame_adr_status, text="Description:")
lbl_adr_desc_val = Label(frame_adr_status, text="", font='none 10 bold')
lbl_adr_desc_nam.grid(row=7, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_desc_val.grid(row=7, column=1, rowspan=1, columnspan=3, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_sdms_nam = Label(frame_adr_status, text="Sum/diff mode:")
lbl_adr_sdms_val = Label(frame_adr_status, text="Unknown", font='none 9', width=12, bg='light gray')
lbl_adr_nfcs_nam = Label(frame_adr_status, text="New file create:")
lbl_adr_nfcs_val = Label(frame_adr_status, text="Unknown", font='none 9', width=12, bg='light gray')

lbl_adr_sdms_nam.grid(row=8, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_sdms_val.grid(row=8, column=1, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)
lbl_adr_nfcs_nam.grid(row=8, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_nfcs_val.grid(row=8, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_frsb_nam = Label(frame_adr_status, text="Free disk space:")
lbl_adr_frsb_val = Label(frame_adr_status, text="", font='none 10 bold')
lbl_adr_cfsz_nam = Label(frame_adr_status, text="Current file size:")
lbl_adr_cfsz_val = Label(frame_adr_status, text="", font='none 10 bold')

lbl_adr_frsb_nam.grid(row=9, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_frsb_val.grid(row=9, column=1, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)
lbl_adr_cfsz_nam.grid(row=9, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_cfsz_val.grid(row=9, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_frsp_nam = Label(frame_adr_status, text="or:")
lbl_adr_frsp_val = Label(frame_adr_status, text="", font='none 10 bold')
lbl_adr_cfln_nam = Label(frame_adr_status, text="Current file length:")
lbl_adr_cfln_val = Label(frame_adr_status, text="", font='none 10 bold')

lbl_adr_frsp_nam.grid(row=10, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_frsp_val.grid(row=10, column=1, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)
lbl_adr_cfln_nam.grid(row=10, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_cfln_val.grid(row=10, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)

lbl_sync_status = Label(frame_adr_status, text='Synchro', font='none 9', width=12, bg='light gray')
lbl_recd_status = Label(frame_adr_status, text='Waiting', font='none 12', width=15, bg='light gray')
lbl_mast_status = Label(frame_adr_status, text='Unknown', font='none 9', width=12, bg='light gray')
lbl_sync_status.grid(row=11, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space)
lbl_recd_status.grid(row=11, column=1, rowspan=1, columnspan=2, stick='nswe', padx=x_space, pady=y_space)
lbl_mast_status.grid(row=11, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space)


# Setting elements of the frame "Load schedule"
lbl_path_in = Label(frame_load_schedule, text="  Path:")
btn_select_file = Button(frame_load_schedule, text="Select file", relief='raised', width=12,
                         command=choose_schedule_file)
# btn_select_file.focus_set()
entry_schedule_file = Entry(frame_load_schedule, width=45)  # 45 works fine for Linux
lbl_scedule_comments = Label(frame_load_schedule, text="")

btn_select_file.grid(row=0, column=0, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
lbl_path_in.grid(row=0, column=1, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
entry_schedule_file.grid(row=0, column=2, rowspan=1, columnspan=2, stick='nswe', padx=x_space, pady=y_space)
lbl_scedule_comments.grid(row=1, column=0, rowspan=1, columnspan=4, stick='nswe', padx=x_space, pady=y_space)


# Frame control ADR by schedule

btn_start_unblock = Button(frame_control, text="UNBLOCK", font='none 9 bold', relief='raised', width=12,
                           command=block_control_button)
btn_start_schedule = Button(frame_control, text="Start control", font='none 9 bold', relief='raised', fg='gray',
                            width=27, command=start_control_by_schedule_button)
btn_start_unblock.grid(row=0, column=0, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
btn_start_schedule.grid(row=0, column=1, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)


send_tg_messages = IntVar(value=1)
lbl_send_tg_messages = Label(frame_control, text='Send Telegram\nnotifications', font='none 9', width=12)
btn_send_tg_messages = Checkbutton(frame_control, text="", variable=send_tg_messages, bg='light gray',
                                   fg='black', activebackground='gray77', activeforeground='SlateBlue1',
                                   selectcolor="white")
btn_send_tg_messages.config(state=DISABLED)

lbl_send_tg_messages.grid(row=1, column=0, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
btn_send_tg_messages.grid(row=1, column=1, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)

img = ImageTk.PhotoImage(Image.open(logo_path))
ira_logo = Label(frame_control, image=img, width=145)
ira_logo.grid(row=0, column=2, rowspan=3, columnspan=2, stick='nswe', padx=x_space, pady=y_space)

lbl_control_status = Label(frame_control, text='ADR is not connected!', font='none 12', width=15, bg='light gray')
lbl_control_status.grid(row=2, column=0, rowspan=1, columnspan=2, stick='nswe', padx=x_space, pady=y_space)

# Setting elements of the frame "Schedule"

ent_schedule = ScrolledText(frame_schedule, width=90, height=39)
ent_schedule.config(state=DISABLED)
ent_schedule.grid(row=0, column=0, rowspan=2, columnspan=1, stick='nswe', padx=x_space, pady=y_space)

# Start time thread
time_display_thread = Thread(target=time_show, daemon=True)
time_display_thread.start()

# *******************************************************************************
#                               T A B    P L O T S                              *
# *******************************************************************************


def plot_schedule():
    fig = Figure(figsize=(12, 6), dpi=100)

    y = [i ** 2 for i in range(101)]

    main_plot = fig.add_subplot(111)
    main_plot.plot(y)
    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,  master=tab_graphics)
    canvas.draw()
    canvas.get_tk_widget().pack()  # placing the canvas on the Tkinter window
    toolbar = NavigationToolbar2Tk(canvas, tab_graphics)  # creating the Matplotlib toolbar
    toolbar.update()
    canvas.get_tk_widget().pack()  # placing the toolbar on the Tkinter window


plot_button = Button(master=tab_graphics, command=plot_schedule, height=2, width=10, text="Plot")
plot_button.grid(row=0, column=0, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
plot_button.pack()


# *******************************************************************************
#              T A B    C O N N E C T I O N    C O N T R O L                    *
# *******************************************************************************
# tab_connection_control
# ################# RELAY #####################


def read_relay_output():
    message = bytearray([])
    # Wait the response for only 3 sec., if not return empty string
    ready = select.select([socket_relay_01], [], [], 3)  # 3 -time in seconds to wait respond
    if ready[0]:
        byte = socket_relay_01.recv(8)
        message.extend(byte)
        message = bytes(message).decode()
        return message
    else:
        return ''


def f_send_command_to_relay(socket, relay_no, command):
    """
    Function sends commands to the SR-201 relay block and shows the relay status
    Input parameters:
        socket_relay_01     - socket of the relay to communicate
        relay_no            - number of the relay on the board
        command             - command 'ON' or 'OFF'
    Output parameters:
    """
    relay_no_str = str(relay_no)
    if str(command).lower() == 'on':        # ON and keep state
        command = '1'
    elif str(command).lower() == '0':       # Check state
        command = '0'
    else:                                   # OFF and keep state
        command = '2'
    send_command = command + relay_no_str
    socket.send(send_command.encode())
    message = read_relay_output()
    return message


def set_indication_by_state(state):
    if state[0] == '0':
        lbl_clr_0.config(text='OFF', bg='chartreuse2')
    else:
        lbl_clr_0.config(text='ON', bg='SlateBlue1')  # orange red

    if state[1] == '0':
        lbl_clr_1.config(text='OFF', bg='chartreuse2')
    else:
        lbl_clr_1.config(text='ON', bg='SlateBlue1')  # orange red


def check_relay_state():
    state = f_send_command_to_relay(socket_relay_01, 0, 0)
    if len(state) > 0:
        set_indication_by_state(state)
    else:
        lbl_clr_0.config(text='Unknown', font='none 12', width=12, bg='yellow2')
        lbl_clr_1.config(text='Unknown', font='none 12', width=12, bg='yellow2')
        lbl_connect.config(text='Disconnected', font='none 12', width=12, bg='gray')
    return state


def click_on_0():
    if not block_flag:
        state = f_send_command_to_relay(socket_relay_01, 1, 'ON')
        set_indication_by_state(state)


def click_on_1():
    if not block_flag:
        state = f_send_command_to_relay(socket_relay_01, 2, 'ON')
        set_indication_by_state(state)


def click_off_0():
    if not block_flag:
        state = f_send_command_to_relay(socket_relay_01, 1, 'OFF')
        set_indication_by_state(state)


def click_off_1():
    if not block_flag:
        state = f_send_command_to_relay(socket_relay_01, 2, 'OFF')
        set_indication_by_state(state)


def click_connect():
    global block_flag
    block_flag = True
    global socket_relay_01
    relay_host = ent_relay_ip.get()  # Read the IP address from the entry
    btn_block_cntrl.focus_set()  # To prevent cursor blinking after setting the correct IP
    # Connect to relay
    socket_relay_01 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_relay_01.connect((relay_host, relay_port))
    socket_relay_01.setblocking(False)  # To wait only the predefined time (see socket.recv())
    lbl_connect.config(text='Connected', font='none 12', width=12, bg='chartreuse2')
    connection_thread = Thread(target=keep_connection_alive, daemon=True)
    connection_thread.start()


def keep_connection_alive():
    while True:
        state = check_relay_state()
        time.sleep(1)
        if len(state) == 0:  # If the connection to relay block is lost
            block()  # Call block function to block buttons as at the beginning of operation
            break


def block_control():
    if block_flag:
        unblock()
    else:
        block()


def unblock():
    global block_flag
    block_flag = False
    btn_block_cntrl.config(text='BLOCK')
    btn_of_0.config(fg='black')
    btn_on_0.config(fg='black')
    btn_of_1.config(fg='black')
    btn_on_1.config(fg='black')
    btn_pc_on_0.config(fg='black')
    btn_pc_of_0.config(fg='black')
    btn_pc_on_1.config(fg='black')
    btn_pc_of_1.config(fg='black')


def block():
    global block_flag
    block_flag = True
    btn_block_cntrl.config(text='UNBLOCK')
    btn_of_0.config(fg='gray')
    btn_on_0.config(fg='gray')
    btn_of_1.config(fg='gray')
    btn_on_1.config(fg='gray')
    btn_pc_on_0.config(fg='gray')
    btn_pc_of_0.config(fg='gray')
    btn_pc_on_1.config(fg='gray')
    btn_pc_of_1.config(fg='gray')


def click_on_pc_0():
    if not block_flag:
        f_send_command_to_relay(socket_relay_01, 1, 'ON')
        lbl_clr_0.config(text='ON', bg='SlateBlue1')
        time.sleep(0.3)
        f_send_command_to_relay(socket_relay_01, 1, 'OFF')


def click_of_pc_0():
    if not block_flag:
        connection_thread = Thread(target=off_pc_0, daemon=True)
        connection_thread.start()


def off_pc_0():
    f_send_command_to_relay(socket_relay_01, 1, 'ON')
    btn_pc_of_0.config(relief='sunken')
    time.sleep(11)
    f_send_command_to_relay(socket_relay_01, 1, 'OFF')
    btn_pc_of_0.config(relief='raised')


def click_on_pc_1():
    if not block_flag:
        f_send_command_to_relay(socket_relay_01, 2, 'ON')
        lbl_clr_1.config(text='ON', bg='SlateBlue1')
        time.sleep(0.3)
        f_send_command_to_relay(socket_relay_01, 2, 'OFF')


def click_of_pc_1():
    if not block_flag:
        connection_thread = Thread(target=off_pc_1, daemon=True)
        connection_thread.start()


def off_pc_1():
    f_send_command_to_relay(socket_relay_01, 2, 'ON')
    btn_pc_of_1.config(relief='sunken')
    time.sleep(11)
    f_send_command_to_relay(socket_relay_01, 2, 'OFF')
    btn_pc_of_1.config(relief='raised')


frame_relay_control_01 = LabelFrame(tab_connection_control, text="Relay block 01 control")

lbl_txt_ip = Label(frame_relay_control_01, text='IP address:', font='none 12', width=12)
ent_relay_ip = Entry(frame_relay_control_01, width=15)
ent_relay_ip.insert(0, relay_host)
btn_connect = Button(frame_relay_control_01, text='Connect', width=10, command=click_connect)
btn_connect.focus_set()
lbl_connect = Label(frame_relay_control_01, text='Disconnected', font='none 12', width=12, bg='gray')
lbl_blank_relay_txt = Label(frame_relay_control_01, text='    ', font='none 12', width=13)

btn_block_cntrl = Button(frame_relay_control_01, text='UNBLOCK', font='none 9 bold', width=10, command=block_control)

lbl_txt_0 = Label(frame_relay_control_01, text='Pin 0 (ADR):', font='none 12', width=12)
lbl_clr_0 = Label(frame_relay_control_01, text='Unknown', font='none 12', width=12, bg='yellow2')
btn_of_0 = Button(frame_relay_control_01, text='OFF', width=10, fg='gray', command=click_off_0)
btn_on_0 = Button(frame_relay_control_01, text='ON', width=10, fg='gray', command=click_on_0)
btn_pc_on_0 = Button(frame_relay_control_01, text='Click', width=4, fg='gray', command=click_on_pc_0)
btn_pc_of_0 = Button(frame_relay_control_01, text='10 s.', width=4, fg='gray', command=click_of_pc_0)

lbl_txt_1 = Label(frame_relay_control_01, text='Pin 1 (Beam):', font='none 12', width=12)
lbl_clr_1 = Label(frame_relay_control_01, text='Unknown', font='none 12', width=12, bg='yellow2')
btn_of_1 = Button(frame_relay_control_01, text='OFF', width=10, fg='gray', command=click_off_1)
btn_on_1 = Button(frame_relay_control_01, text='ON', width=10, fg='gray', command=click_on_1)
btn_pc_on_1 = Button(frame_relay_control_01, text='Click', width=4, fg='gray', command=click_on_pc_1)
btn_pc_of_1 = Button(frame_relay_control_01, text='10 s.', width=4, fg='gray', command=click_of_pc_1)

frame_relay_control_01.grid(row=8, column=0, rowspan=1, columnspan=6, stick='w', padx=10, pady=10)

lbl_txt_ip.grid(row=8, column=0, stick='w', padx=x_space, pady=y_space)
ent_relay_ip.grid(row=8, column=1, stick='w', padx=x_space, pady=y_space)
btn_connect.grid(row=8, column=2, stick='nswe', padx=x_space, pady=10)
lbl_connect.grid(row=8, column=3, stick='nswe', padx=x_space, pady=10)
lbl_blank_relay_txt.grid(row=8, column=4, columnspan=3, stick='w', padx=4, pady=y_space)

btn_block_cntrl.grid(row=9, column=2, stick='w', padx=x_space, pady=y_space)

lbl_txt_0.grid(row=10, column=0, stick='w', padx=x_space, pady=y_space)
lbl_clr_0.grid(row=10, column=1, stick='w', padx=x_space, pady=y_space)
btn_of_0.grid(row=10, column=2, stick='w', padx=x_space, pady=y_space)
btn_on_0.grid(row=10, column=3, stick='w', padx=x_space, pady=y_space)
btn_pc_on_0.grid(row=10, column=4, stick='w', padx=x_space, pady=y_space)
btn_pc_of_0.grid(row=10, column=5, stick='w', padx=x_space, pady=y_space)

lbl_txt_1.grid(row=11, column=0, stick='w', padx=x_space, pady=y_space)
lbl_clr_1.grid(row=11, column=1, stick='w', padx=x_space, pady=y_space)
btn_of_1.grid(row=11, column=2, stick='w', padx=x_space, pady=y_space)
btn_on_1.grid(row=11, column=3, stick='w', padx=x_space, pady=y_space)
btn_pc_on_1.grid(row=11, column=4, stick='w', padx=x_space, pady=y_space)
btn_pc_of_1.grid(row=11, column=5, stick='w', padx=x_space, pady=y_space)

# *******************************************************************************
#              T A B    C O N N E C T I O N    C O N T R O L                    *
# *******************************************************************************
# tab_settings


window.mainloop()
