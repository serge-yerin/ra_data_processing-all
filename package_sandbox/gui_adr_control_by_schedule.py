import sys  # needed for running in Linux
import time
import socket
import tkinter.filedialog
from os import path
from time import strftime
from datetime import datetime
from tkinter import *
from PIL import ImageTk, Image
from threading import Thread
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
from package_receiver_control.f_read_schedule_txt_for_adr import find_parameter_value
from package_receiver_control.f_read_and_set_adr_parameters import f_read_adr_parameters_from_txt_file

"""
The GUI program to control ADR receiver according to schedule
"""
software_version = '2021.05.08'

# *******************************************************************************
#                     R U N   S T A T E   V A R I A B L E S                     *
# *******************************************************************************
adr_ip = '192.168.1.171'
port = 38386                    # Port of the receiver to connect (always 38386)
logo_path = 'media_data/gurt_logo.png'
x_space = (5, 5)
y_space = (5, 5)
y_space_adr = 1
colors = ['chartreuse2', 'SpringGreen2', 'yellow2', 'orange red', 'SlateBlue1']
block_flag = True
block_selecting_new_schedule_flag = False
adr_connection_flag = False
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


def f_connect_to_adr_receiver(host, port):   # UNUSED NOW !!!
    """
    Function connects to the ADR receiver via specified socket
    Input parameters:
        host                - IP address to connect
        port                - port to connect
        control             - to control (1) or to view (0) possibility
        delay               - delay in seconds to wait after connection
    Output parameters:
        serversocket        - handle of socket to send and receive messages from server
        input_parameters_s  - long string with all receiver parameters at the moment of connection
    """
    control = 1
    delay = 1
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        lbl_adr_status.config(text='Connecting...', bg='yellow2')
        serversocket.settimeout(10)
        serversocket.connect((host, port))
    except TimeoutError:
        lbl_adr_status.config(text='Failed!', bg='orange')
    else:
        pass
    finally:
        lbl_adr_status.config(text='Failed!', bg='orange')  # Works in Linux instead except TimeoutError

    serversocket.send('ADRSCTRL'.encode())
    register_cc_msg = bytearray([108, 0, 0, 0])
    register_cc_msg.extend(b'YeS\0                                                            ')  # Name 64 bytes
    register_cc_msg.extend(b'adrs\0                           ')   # Password 32 bytes
    register_cc_msg.extend([0, 0, 0, control])                     # Priv 4 bytes
    register_cc_msg.extend([0, 0, 0, control])                     # CTRL 4 bytes
    register_cc_msg = bytes(register_cc_msg)
    serversocket.send(register_cc_msg)

    data = f_read_adr_meassage(serversocket, 0)
    data = serversocket.recv(108)
    if data[-1] == 1:
        lbl_mast_status.config(text='Control', font='none 9', bg='chartreuse2')
    else:
        lbl_mast_status.config(text='View only', font='none 9', bg='orange')
    lbl_adr_status.config(text='Connected', font='none 12', width=12, bg='chartreuse2')
    adr_connection_flag = True

    # Reading all parameters valid now
    input_parameters_str = ''
    for i in range(23):
        input_parameters_str += f_read_adr_meassage(serversocket, 0)
    time.sleep(delay)   # Making pause to read the data
    return serversocket, input_parameters_str


def start_and_keep_adr_connection():
    host = ent_adr_ip.get()
    serversocket, input_parameters_str = f_connect_to_adr_receiver(host, port)
    while True:
        time.sleep(1)


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


def choose_schedule_file():
    if not block_selecting_new_schedule_flag:
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
        lbl_control_status.config(text='Observation in progress!', bg='SlateBlue1')
        time.sleep(15)
        block_selecting_new_schedule_flag = False
        btn_select_file.config(fg='black')
        lbl_control_status.config(text='Waiting to start', bg='light gray')


# *******************************************************************************
#                             M A I N    W I N D O W                            *
# *******************************************************************************

window = Tk()
window.title('ADR control GUI v.'+software_version+' (c) YeS')
window.rowconfigure(0, minsize=30, weight=1)
window.columnconfigure(1, minsize=40, weight=1)

# Setting tabs in the main window
tab_parent = ttk.Notebook(window)
tab_main = ttk.Frame(tab_parent)
tab_settings = ttk.Frame(tab_parent)
tab_parent.add(tab_main, text='   Main window   ')
tab_parent.add(tab_settings, text='   Settings   ')
tab_parent.pack(expand=1, fill="both")

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
lbl_adr_ip.grid(row=0, column=2, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
ent_adr_ip.grid(row=0, column=3, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)

lbl_adr_fadc_nam = Label(frame_adr_status, text="ADC frequency:")
lbl_adr_fadc_val = Label(frame_adr_status, text="")
lbl_adr_sadc_nam = Label(frame_adr_status, text="ADC source:")
lbl_adr_sadc_val = Label(frame_adr_status, text="Internal", font='none 9', width=12, bg='yellow')

lbl_adr_fadc_nam.grid(row=1, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_fadc_val.grid(row=1, column=1, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)
lbl_adr_sadc_nam.grid(row=1, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_sadc_val.grid(row=1, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_mode_nam = Label(frame_adr_status, text="ADC mode:")
lbl_adr_mode_val = Label(frame_adr_status, text="")
lbl_adr_chnl_nam = Label(frame_adr_status, text="Channels:")
lbl_adr_chnl_val = Label(frame_adr_status, text="")

lbl_adr_mode_nam.grid(row=2, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_mode_val.grid(row=2, column=1, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)
lbl_adr_chnl_nam.grid(row=2, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_chnl_val.grid(row=2, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_fres_nam = Label(frame_adr_status, text="Frequency resolution:")
lbl_adr_fres_val = Label(frame_adr_status, text="")
lbl_adr_tres_nam = Label(frame_adr_status, text="Time resolution:")
lbl_adr_tres_val = Label(frame_adr_status, text="")

lbl_adr_fres_nam.grid(row=3, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_fres_val.grid(row=3, column=1, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)
lbl_adr_tres_nam.grid(row=3, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_tres_val.grid(row=3, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_flow_nam = Label(frame_adr_status, text="Lowest frequency:")
lbl_adr_flow_val = Label(frame_adr_status, text="")
lbl_adr_fhig_nam = Label(frame_adr_status, text="Highest frequency:")
lbl_adr_fhig_val = Label(frame_adr_status, text="")

lbl_adr_flow_nam.grid(row=4, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_flow_val.grid(row=4, column=1, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)
lbl_adr_fhig_nam.grid(row=4, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_fhig_val.grid(row=4, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_rnam_nam = Label(frame_adr_status, text="Receiver name:")
lbl_adr_rnam_val = Label(frame_adr_status, text="")
lbl_adr_rnam_nam.grid(row=5, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_rnam_val.grid(row=5, column=1, rowspan=1, columnspan=3, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_obsn_nam = Label(frame_adr_status, text="Observatory:")
lbl_adr_obsn_val = Label(frame_adr_status, text="")
lbl_adr_obsn_nam.grid(row=6, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_obsn_val.grid(row=6, column=1, rowspan=1, columnspan=3, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_desc_nam = Label(frame_adr_status, text="Description:")
lbl_adr_desc_val = Label(frame_adr_status, text="")
lbl_adr_desc_nam.grid(row=7, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_desc_val.grid(row=7, column=1, rowspan=1, columnspan=3, stick='w', padx=x_space, pady=y_space_adr)

lbl_adr_sdms_nam = Label(frame_adr_status, text="Sum/diff mode:")
lbl_adr_sdms_val = Label(frame_adr_status, text="OFF", font='none 9', width=12, bg='chartreuse2')
lbl_adr_nfcs_nam = Label(frame_adr_status, text="New file create:")
lbl_adr_nfcs_val = Label(frame_adr_status, text="ON", font='none 9', width=12, bg='chartreuse2')

lbl_adr_sdms_nam.grid(row=8, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_sdms_val.grid(row=8, column=1, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)
lbl_adr_nfcs_nam.grid(row=8, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_nfcs_val.grid(row=8, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space_adr)

lbl_sync_status = Label(frame_adr_status, text='Synchro', font='none 9', width=12, bg='light gray')
lbl_recd_status = Label(frame_adr_status, text='Waiting', font='none 12', width=15, bg='light gray')
lbl_mast_status = Label(frame_adr_status, text='Unknown', font='none 9', width=12, bg='light gray')
lbl_sync_status.grid(row=9, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space)
lbl_recd_status.grid(row=9, column=1, rowspan=1, columnspan=2, stick='nswe', padx=x_space, pady=y_space)
lbl_mast_status.grid(row=9, column=3, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space)

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

window.mainloop()
