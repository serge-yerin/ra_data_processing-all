# Python3
# The GUI-based program to check status of GURT devices and control them
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import sys
import time
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from wakeonlan import send_magic_packet
from time import gmtime, strftime
from threading import Thread
from tkinter import *
from PIL import ImageTk, Image

from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# *******************************************************************************
#                              V A R I A B L E S                                *
# *******************************************************************************
logo_path = 'media_data/ira_logo.gif'
x_space = (5, 5)
y_space = (5, 5)
gurt_lan_log_file_name = 'service_data/gurt_lan_connection_log.txt'

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
             '172.16.10.1', '172.16.1.1']
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
                    t = strftime(" %Y-%m-%d %H:%M:%S", gmtime())
                    message = t + ' UTC: Device with IP: ' + hosts[item] + ' was connected!'
                    gurt_lan_log_file = open(gurt_lan_log_file_name, "a")
                    gurt_lan_log_file.write(message + '\n')
                    gurt_lan_log_file.close()
            else:
                if answer == previous_states[item]:
                    labels[item].config(text='Offline', bg='gray')
                else:
                    labels[item].config(text='Just OFF', bg='orange red')
                    t = strftime(" %Y-%m-%d %H:%M:%S", gmtime())
                    message = t + ' UTC: Device with IP: ' + hosts[item] + ' was disconnected!'
                    gurt_lan_log_file = open(gurt_lan_log_file_name, "a")
                    gurt_lan_log_file.write(message + '\n')
                    gurt_lan_log_file.close()
            previous_states[item] = answer
        # If the program has just started operation
        if first_check:
            lbl_start.config(text='Working', bg='chartreuse2')
            # # Save to log file all the connected and disconnected devices
            # gurt_lan_log_file = open(gurt_lan_log_file_name, "a")
            # for item in range(len(hosts)):
            #     gurt_lan_log_file.write('  ' + hosts[item] + ' ' + str(previous_states[item]) + '\n')
            # gurt_lan_log_file.close()

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

# *******************************************************************************
#                           M A I N     P R O G R A M                           *
# *******************************************************************************

global server_on_block_flag
server_on_block_flag = True

t = strftime(" %Y-%m-%d %H:%M:%S", gmtime())
message = t + ' UTC: GURT online status board software started.'
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

btn_unblock_server_on = Button(frame_on_server, text='UNBLOCK', width=12, command=server_on_block_control)
btn_unblock_server_on.focus_set()
btn_server_on = Button(frame_on_server, text='Turn on GURT server', fg='gray', width=22, command=turn_on_server)
lbl_server_on = Label(frame_on_server, text='Works only if server power supply is ON!', font='none 9', width=32)


# frame_relay_control_01 = LabelFrame(window, text="Relay control")
#
# btn_unblock_server_on = Button(frame_relay_control_01, text='UNBLOCK', width=12, command=block_control)
# btn_unblock_server_on.focus_set()
# btn_server_on = Button(frame_relay_control_01, text='Turn on GURT server', width=22, command=turn_on_server)
# lbl_server_on = Label(frame_relay_control_01, text='Works only if power supply is ON!', font='none 9', width=32)


time_display_thread = Thread(target=time_show, daemon=True)
time_display_thread.start()

img = ImageTk.PhotoImage(Image.open(logo_path))
ira_logo = Label(window, image = img)

time_lbl.grid(row=0, column=0, rowspan=2, columnspan=4, stick='nswe', padx=x_space, pady=y_space)
ira_logo.grid(row=0, column=4, rowspan=2, columnspan=2, stick='w', padx=x_space, pady=y_space)

btn_start.grid(row=2, column=0, stick='nswe', padx=10, pady=10)
lbl_start.grid(row=2, column=1, stick='nswe', padx=5, pady=10)
lbl_check_interval_txt.grid(row=2, column=2, columnspan=2, stick='w', padx=x_space, pady=y_space)

frame_online_status.grid(row=3, column=0, rowspan=2, columnspan=6, stick='w', padx=10, pady=10)

lbl_internet_online_txt.grid(row=3, column=0, stick='w', padx=x_space, pady=y_space)
lbl_internet_online_clr.grid(row=3, column=1, stick='w', padx=x_space, pady=y_space)

lbl_gurt_server_online_txt.grid(row=3, column=2, stick='w', padx=x_space, pady=y_space)
lbl_gurt_server_online_clr.grid(row=3, column=3, stick='w', padx=x_space, pady=y_space)

lbl_adr01_online_txt.grid(row=4, column=0, stick='w', padx=x_space, pady=y_space)
lbl_adr01_online_clr.grid(row=4, column=1, stick='w', padx=x_space, pady=y_space)

lbl_adr02_online_txt.grid(row=5, column=0, stick='w', padx=x_space, pady=y_space)
lbl_adr02_online_clr.grid(row=5, column=1, stick='w', padx=x_space, pady=y_space)

lbl_ctrl_block_01_online_txt.grid(row=4, column=2, stick='w', padx=x_space, pady=y_space)
lbl_ctrl_block_01_online_clr.grid(row=4, column=3, stick='w', padx=x_space, pady=y_space)

lbl_ctrl_block_02_online_txt.grid(row=5, column=2, stick='w', padx=x_space, pady=y_space)
lbl_ctrl_block_02_online_clr.grid(row=5, column=3, stick='w', padx=x_space, pady=y_space)

lbl_relay_01_online_txt.grid(row=6, column=0, stick='w', padx=x_space, pady=y_space)
lbl_relay_01_online_clr.grid(row=6, column=1, stick='w', padx=x_space, pady=y_space)

lbl_relay_02_online_txt.grid(row=6, column=2, stick='w', padx=x_space, pady=y_space)
lbl_relay_02_online_clr.grid(row=6, column=3, stick='w', padx=x_space, pady=y_space)

frame_tg_notifications.grid(row=3, column=4, rowspan=4, columnspan=2, stick='nswe', padx=x_space, pady=y_space)

btn_send_tg_messages.grid(row=3, column=4, rowspan=2, columnspan=2, stick='nswe', padx=x_space, pady=y_space)
lbl_send_tg_messages.grid(row=5, column=4, rowspan=2, columnspan=2, stick='nswe', padx=x_space, pady=y_space)

frame_on_server.grid(row=7, column=0, rowspan=1, columnspan=6, stick='w', padx=10, pady=10)

btn_unblock_server_on.grid(row=7, column=0, stick='w', padx=x_space, pady=y_space)
btn_server_on.grid(row=7, column=1, columnspan=2, stick='w', padx=x_space, pady=y_space)
lbl_server_on.grid(row=7, column=3, columnspan=3, stick='w', padx=x_space, pady=y_space)

window.mainloop()


