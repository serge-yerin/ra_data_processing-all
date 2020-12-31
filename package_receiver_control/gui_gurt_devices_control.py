# Python3
# The GUI-based program to check status of GURT devices and control them

# !!! Make read bot token only once on the program start !!!
# Add Settings section to set up the IP addresses of devices
# Add section for the second relay block

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import sys
import time
import socket
import select
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from wakeonlan import send_magic_packet
from time import strftime
from threading import Thread
from tkinter import *
from PIL import ImageTk, Image
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_common_modules.telegram_bot_sendtext import telegram_bot_sendtext
# *******************************************************************************
#                              V A R I A B L E S                                *
# *******************************************************************************
relay_host = '172.16.1.169'  # '10.0.15.170', 192.168.1.170
relay_port = 6722
logo_path = 'media_data/gurt_logo.png'
x_space = (5, 5)
y_space = (5, 5)
gurt_lan_log_file_name = 'service_data/gurt_lan_connection_log.txt'
telegram_chat_id = '927534685'  # Telegram chat ID to send messages  - '927534685' - YeS

# *******************************************************************************
#                                F U N C T I O N S                              *
# *******************************************************************************


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '2', host]
    return subprocess.call(command) == 0


def check_if_hosts_online():
    # hosts = ['8.8.8.8', '192.168.1.150'
    #          '192.168.1.171', '192.168.1.172'
    #          '192.168.1.11', '192.168.1.12',
    #          '192.168.1.170', '192.168.1.169']
    hosts = ['8.8.8.8', '172.16.1.100',
             '172.16.10.1', '172.16.1.1',
             '172.16.10.1', '172.16.1.1',
             '172.16.1.169', '172.16.10.1']
    device_names = ['Internet connection', 'GURT server',
                    'ADR 01', 'ADR 02',
                    'Beam control block 01', 'Beam control block 02',
                    'Relay block 01', 'Relay block 02']
    labels = [lbl_internet_online_clr, lbl_gurt_server_online_clr,
              lbl_adr01_online_clr, lbl_adr02_online_clr,
              lbl_ctrl_block_01_online_clr, lbl_ctrl_block_02_online_clr,
              lbl_relay_01_online_clr, lbl_relay_02_online_clr]
    previous_states = [False, False, False, False, False, False, False, False]
    lbl_start.config(text='Checking...', bg='yellow')
    lbl_check_interval_txt.config(text='Checking each 60 s.')
    first_check = True
    while True:
        for item in range(len(hosts)):
            answer = ping(hosts[item])
            if answer:
                if answer == previous_states[item]:
                    labels[item].config(text='Online', bg='chartreuse2')
                else:
                    labels[item].config(text='Just ON', bg='SpringGreen2')
                    t = strftime(" %Y-%m-%d %H:%M Loc")
                    message = t + ': ' + device_names[item] + ' (IP: ' + hosts[item] + ') connected'
                    gurt_lan_log_file = open(gurt_lan_log_file_name, "a")
                    gurt_lan_log_file.write(message + '\n')
                    gurt_lan_log_file.close()
                    if not first_check:
                        if send_tg_messages.get():
                            try:
                                test = telegram_bot_sendtext(telegram_chat_id, message)
                            except:
                                pass
            else:
                if answer == previous_states[item]:
                    labels[item].config(text='Offline', bg='gray')
                else:
                    labels[item].config(text='Just OFF', bg='orange red')
                    t = strftime(" %Y-%m-%d %H:%M Loc")
                    message = t + ': ' + device_names[item] + ' (IP: ' + hosts[item] + ') disconnected'
                    gurt_lan_log_file = open(gurt_lan_log_file_name, "a")
                    gurt_lan_log_file.write(message + '\n')
                    gurt_lan_log_file.close()
                    # Sending message to Telegram
                    if send_tg_messages.get():
                        try:
                            test = telegram_bot_sendtext(telegram_chat_id, message)
                        except:
                            pass

            previous_states[item] = answer
        # If the program has just started operation
        if first_check:
            lbl_start.config(text='Working', bg='chartreuse2')
        first_check = False
        time.sleep(60)


# Renew time readings each second
def time_show():
    loc_time_str = strftime('%Y . %m . %d     %H : %M : %S ')
    utc_time_str = strftime('%Y . %m . %d     %H : %M : %S ', time.gmtime())
    time_lbl.config(text='\n     Local:     ' + loc_time_str +
                         '     \n      UTC:      ' + utc_time_str + '     \n')
    time_lbl.after(1000, time_show)


def start_check_thread():
    check_thread = Thread(target=check_if_hosts_online, daemon=True)
    check_thread.start()


def server_on_block_control():
    if server_on_block_flag:
        server_on_unblock()
    else:
        server_on_block()


def server_on_unblock():
    global server_on_block_flag
    server_on_block_flag = False
    btn_unblock_server_on.config(text='BLOCK')
    btn_server_on.config(fg='black')


def server_on_block():
    global server_on_block_flag
    server_on_block_flag = True
    btn_unblock_server_on.config(text='UNBLOCK')
    btn_server_on.config(fg='gray')


def turn_on_server():
    if server_on_block_flag:
        pass
    else:
        send_magic_packet('74.d0.2b.28.5f.c8')


# ################# RELAY #####################


def read_relay_output():
    message = bytearray([])
    # Wait the response for only 3 sec., if not return empty string
    ready = select.select([serversocket], [], [], 3)  # 33 -time in seconds to wait respond
    if ready[0]:
        byte = serversocket.recv(8)
        message.extend(byte)
        message = bytes(message).decode()
        return message
    else:
        return ''


def f_send_command_to_relay(serversocket, relay_no, command):
    '''
    Function sends commands to the SR-201 relay block and shows the relay status
    Input parameters:
        serversocket        - socket of the relay to communicate
        relay_no            - number of the relay on the board
        command             - command 'ON' or 'OFF'
    Output parameters:
    '''
    relay_no_str = str(relay_no)
    if str(command).lower() == 'on':        # ON and keep state
        command = '1'
    elif str(command).lower() == '0':       # Check state
        command = '0'
    else:                                   # OFF and keep state
        command = '2'
    send_command = command + relay_no_str
    serversocket.send(send_command.encode())
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
    state = f_send_command_to_relay(serversocket, 0, 0)
    if len(state) > 0:
        set_indication_by_state(state)
    else:
        lbl_clr_0.config(text='Unknown', font='none 12', width=12, bg='yellow2')
        lbl_clr_1.config(text='Unknown', font='none 12', width=12, bg='yellow2')
        lbl_connect.config(text='Disconnected', font='none 12', width=12, bg='gray')
    return state


def click_on_0():
    if not block_flag:
        state = f_send_command_to_relay(serversocket, 1, 'ON')
        set_indication_by_state(state)


def click_on_1():
    if not block_flag:
        state = f_send_command_to_relay(serversocket, 2, 'ON')
        set_indication_by_state(state)


def click_off_0():
    if not block_flag:
        state = f_send_command_to_relay(serversocket, 1, 'OFF')
        set_indication_by_state(state)


def click_off_1():
    if not block_flag:
        state = f_send_command_to_relay(serversocket, 2, 'OFF')
        set_indication_by_state(state)


def click_connect():
    global block_flag
    block_flag = True
    global serversocket
    relay_host = ent_ip_addrs.get()    # Read the IP address from the entry
    btn_block_cntrl.focus_set()  # To prevent cursor blinking after setting the correct IP
    # Connect to relay
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.connect((relay_host, relay_port))
    serversocket.setblocking(False)  # To wait only the predefined time (see socket.recv())
    lbl_connect.config(text='Connected', font='none 12', width=12, bg='chartreuse2')
    connection_thread = Thread(target=keep_connection_alive, daemon=True)
    connection_thread.start()


def keep_connection_alive():
    while True:
        state = check_relay_state()
        time.sleep(1)
        if len(state) == 0:
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
        f_send_command_to_relay(serversocket, 1, 'ON')
        lbl_clr_0.config(text='ON', bg='orange red')
        time.sleep(0.3)
        f_send_command_to_relay(serversocket, 1, 'OFF')


def click_of_pc_0():
    if not block_flag:
        connection_thread = Thread(target=off_pc_0, daemon=True)
        connection_thread.start()


def off_pc_0():
    f_send_command_to_relay(serversocket, 1, 'ON')
    btn_pc_of_0.config(relief='sunken')
    time.sleep(11)
    f_send_command_to_relay(serversocket, 1, 'OFF')
    btn_pc_of_0.config(relief='raised')


def click_on_pc_1():
    if not block_flag:
        f_send_command_to_relay(serversocket, 2, 'ON')
        lbl_clr_1.config(text='ON', bg='orange red')
        time.sleep(0.3)
        f_send_command_to_relay(serversocket, 2, 'OFF')


def click_of_pc_1():
    if not block_flag:
        connection_thread = Thread(target=off_pc_1, daemon=True)
        connection_thread.start()


def off_pc_1():
    f_send_command_to_relay(serversocket, 2, 'ON')
    btn_pc_of_1.config(relief='sunken')
    time.sleep(11)
    f_send_command_to_relay(serversocket, 2, 'OFF')
    btn_pc_of_1.config(relief='raised')


# *******************************************************************************
#                           M A I N     P R O G R A M                           *
# *******************************************************************************

global server_on_block_flag
server_on_block_flag = True

t = strftime(" %Y-%m-%d %H:%M Loc")
message = t + ': GURT online status board software started.'
gurt_lan_log_file = open(gurt_lan_log_file_name, "a")
gurt_lan_log_file.write('\n' + message + '\n\n')
gurt_lan_log_file.close()


# Main window creation
window = Tk()
window.title('GURT online status board     (YeS 2020)')
window.rowconfigure(0, minsize=30, weight=1)
window.columnconfigure(1, minsize=40, weight=1)

time_lbl = Label(window, font=('none', 14, 'bold'), background='black', foreground='yellow')


frame_online_status = LabelFrame(window, text="Network status of GURT devices")

btn_start = Button(frame_online_status, text='Start ping', width=10, command=start_check_thread)
btn_start.focus_set()
lbl_start = Label(frame_online_status, text='Stopped', font='none 12', width=12, bg='gray')
lbl_check_interval_txt = Label(frame_online_status, text='   ', font='none 9', width=20)

lbl_internet_online_txt = Label(frame_online_status, text='Internet', font='none 12', width=12)
lbl_internet_online_clr = Label(frame_online_status, text='Unknown', font='none 12', width=10, bg='gray77')

lbl_gurt_server_online_txt = Label(frame_online_status, text='GURT server', font='none 12', width=12)
lbl_gurt_server_online_clr = Label(frame_online_status, text='Unknown', font='none 12', width=10, bg='gray77')

lbl_adr01_online_txt = Label(frame_online_status, text='ADR 01', font='none 12', width=12)
lbl_adr01_online_clr = Label(frame_online_status, text='Unknown', font='none 12', width=10, bg='gray77')

lbl_adr02_online_txt = Label(frame_online_status, text='ADR 02', font='none 12', width=12)
lbl_adr02_online_clr = Label(frame_online_status, text='Unknown', font='none 12', width=10, bg='gray77')

lbl_ctrl_block_01_online_txt = Label(frame_online_status, text='Beam control 1', font='none 12', width=12)
lbl_ctrl_block_01_online_clr = Label(frame_online_status, text='Unknown', font='none 12', width=10, bg='gray77')

lbl_ctrl_block_02_online_txt = Label(frame_online_status, text='Beam control 2', font='none 12', width=12)
lbl_ctrl_block_02_online_clr = Label(frame_online_status, text='Unknown', font='none 12', width=10, bg='gray77')

lbl_relay_01_online_txt = Label(frame_online_status, text='Relay block 01', font='none 12', width=12)
lbl_relay_01_online_clr = Label(frame_online_status, text='Unknown', font='none 12', width=10, bg='gray77')

lbl_relay_02_online_txt = Label(frame_online_status, text='Relay block 02', font='none 12', width=12)
lbl_relay_02_online_clr = Label(frame_online_status, text='Unknown', font='none 12', width=10, bg='gray77')


frame_tg_notifications = LabelFrame(frame_online_status)

send_tg_messages = IntVar()
btn_send_tg_messages = Checkbutton(frame_tg_notifications, text="", variable=send_tg_messages)
lbl_send_tg_messages = Label(frame_tg_notifications, text='Send\nTelegram\nnotifications', font='none 12', width=12)

frame_on_server = LabelFrame(window, text="GURT server turning on")

btn_unblock_server_on = Button(frame_on_server, text='UNBLOCK', font='none 9 bold',
                               width=12, command=server_on_block_control)
btn_unblock_server_on.focus_set()
btn_server_on = Button(frame_on_server, text='Turn on GURT server', fg='gray', width=22, command=turn_on_server)
lbl_server_on = Label(frame_on_server, text='Works only if server power supply is ON!', font='none 9', width=32)
lbl_blank_server_txt = Label(frame_on_server, text=' ', font='none 12', width=3)


frame_relay_control_01 = LabelFrame(window, text="Relay block 01 control")

lbl_txt_ip = Label(frame_relay_control_01, text='IP address:', font='none 12', width=12)
ent_ip_addrs = Entry(frame_relay_control_01, width=15)
ent_ip_addrs.insert(0, relay_host)
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


time_display_thread = Thread(target=time_show, daemon=True)
time_display_thread.start()

img = ImageTk.PhotoImage(Image.open(logo_path))
ira_logo = Label(window, image=img)

time_lbl.grid(row=0, column=0, rowspan=2, columnspan=4, stick='nswe', padx=x_space, pady=y_space)
ira_logo.grid(row=0, column=4, rowspan=2, columnspan=2, stick='w', padx=x_space, pady=y_space)

btn_start.grid(row=2, column=0, stick='nswe', padx=10, pady=10)
lbl_start.grid(row=2, column=1, stick='nswe', padx=5, pady=10)
lbl_check_interval_txt.grid(row=2, column=2, columnspan=2, stick='w', padx=x_space, pady=y_space)


frame_online_status.grid(row=3, column=0, rowspan=2, columnspan=6, stick='w', padx=10, pady=10)

lbl_internet_online_txt.grid(row=3, column=0, stick='w', padx=x_space, pady=y_space)
lbl_internet_online_clr.grid(row=3, column=1, stick='w', padx=x_space, pady=y_space)

lbl_gurt_server_online_txt.grid(row=4, column=0, stick='w', padx=x_space, pady=y_space)
lbl_gurt_server_online_clr.grid(row=4, column=1, stick='w', padx=x_space, pady=y_space)

lbl_adr01_online_txt.grid(row=5, column=0, stick='w', padx=x_space, pady=y_space)
lbl_adr01_online_clr.grid(row=5, column=1, stick='w', padx=x_space, pady=y_space)

lbl_adr02_online_txt.grid(row=6, column=0, stick='w', padx=x_space, pady=y_space)
lbl_adr02_online_clr.grid(row=6, column=1, stick='w', padx=x_space, pady=y_space)

lbl_ctrl_block_01_online_txt.grid(row=3, column=2, stick='w', padx=x_space, pady=y_space)
lbl_ctrl_block_01_online_clr.grid(row=3, column=3, stick='w', padx=x_space, pady=y_space)

lbl_ctrl_block_02_online_txt.grid(row=4, column=2, stick='w', padx=x_space, pady=y_space)
lbl_ctrl_block_02_online_clr.grid(row=4, column=3, stick='w', padx=x_space, pady=y_space)

lbl_relay_01_online_txt.grid(row=5, column=2, stick='w', padx=x_space, pady=y_space)
lbl_relay_01_online_clr.grid(row=5, column=3, stick='w', padx=x_space, pady=y_space)

lbl_relay_02_online_txt.grid(row=6, column=2, stick='w', padx=x_space, pady=y_space)
lbl_relay_02_online_clr.grid(row=6, column=3, stick='w', padx=x_space, pady=y_space)


frame_tg_notifications.grid(row=3, column=4, rowspan=4, columnspan=2, stick='nswe', padx=x_space, pady=y_space)

btn_send_tg_messages.grid(row=3, column=4, rowspan=2, columnspan=2, stick='nswe', padx=x_space, pady=y_space)
lbl_send_tg_messages.grid(row=5, column=4, rowspan=2, columnspan=2, stick='nswe', padx=x_space, pady=y_space)


frame_on_server.grid(row=7, column=0, rowspan=1, columnspan=6, stick='w', padx=10, pady=10)

btn_unblock_server_on.grid(row=7, column=0, stick='w', padx=x_space, pady=y_space)
btn_server_on.grid(row=7, column=1, columnspan=2, stick='w', padx=x_space, pady=y_space)
lbl_server_on.grid(row=7, column=3, columnspan=3, stick='w', padx=x_space, pady=y_space)
lbl_blank_server_txt.grid(row=7, column=6, stick='w', padx=6, pady=y_space)

frame_relay_control_01.grid(row=8, column=0, rowspan=1, columnspan=6, stick='w', padx=10, pady=10)

lbl_txt_ip.grid(row=8, column=0, stick='w', padx=x_space, pady=y_space)
ent_ip_addrs.grid(row=8, column=1, stick='w', padx=x_space, pady=y_space)
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

window.mainloop()
