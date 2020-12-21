# Python3
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import socket
from tkinter import *
from threading import Thread
import time
from PIL import ImageTk, Image

# *******************************************************************************
#                              V A R I A B L E S                                *
# *******************************************************************************
host = '192.168.1.170'  # '10.0.15.170', 192.168.1.170
port = 6722
logo_path = 'media_data/ira_logo.gif'
x_space = (10, 10)
y_space = (10, 10)

# *******************************************************************************
#                               F U N C T I O N S                               *
# *******************************************************************************


def read_relay_output():
    message = bytearray([])
    byte = serversocket.recv(8)
    message.extend(byte)
    message = bytes(message).decode()
    return message


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
        lbl_clr_0.config(text='ON', bg='orange red')

    if state[1] == '0':
        lbl_clr_1.config(text='OFF', bg='chartreuse2')
    else:
        lbl_clr_1.config(text='ON', bg='orange red')


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
    host = ent_ip_addrs.get()    # Read the IP address from the entry
    btn_block_cntrl.focus_set()  # To prevent cursor blinking after setting the correct IP
    # Connect to relay
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.connect((host, port))
    lbl_connect.config(text='Connected', font='none 12', width=12, bg='chartreuse2')
    connection_thread = Thread(target=keep_connection_alive, daemon=True)
    connection_thread.start()


def keep_connection_alive():
    while True:
        check_relay_state()
        time.sleep(1)


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
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************


# Main window creation
window = Tk()
window.title('SR-201 relay control (YeS 2020)')
window.rowconfigure(0, minsize=30, weight=1)
window.columnconfigure(1, minsize=40, weight=1)

# Define all widgets
lbl_txt_ip = Label(window, text='IP address:', font='none 12', width=9)
ent_ip_addrs = Entry(window, width=15)
ent_ip_addrs.insert(0, host)
btn_connect = Button(window, text='Connect', width=10, command=click_connect)
btn_connect.focus_set()
lbl_connect = Label(window, text='Disconnected', font='none 12', width=12, bg='gray')

btn_block_cntrl = Button(window, text='UNBLOCK', font='none 9 bold', width=10, command=block_control)

lbl_txt_0 = Label(window, text='Relay 0:', font='none 12', width=9)
lbl_clr_0 = Label(window, text='Unknown', font='none 12', width=12, bg='yellow2')
btn_of_0 = Button(window, text='OFF', width=10, fg='gray', command=click_off_0)
btn_on_0 = Button(window, text='ON', width=10, fg='gray', command=click_on_0)
btn_pc_on_0 = Button(window, text='Click', width=4, fg='gray', command=click_on_pc_0)
btn_pc_of_0 = Button(window, text='10 s.', width=4, fg='gray', command=click_of_pc_0)

lbl_txt_1 = Label(window, text='Relay 1:', font='none 12', width=9)
lbl_clr_1 = Label(window, text='Unknown', font='none 12', width=12, bg='yellow2')
btn_of_1 = Button(window, text='OFF', width=10, fg='gray', command=click_off_1)
btn_on_1 = Button(window, text='ON', width=10, fg='gray', command=click_on_1)
btn_pc_on_1 = Button(window, text='Click', width=4, fg='gray', command=click_on_pc_1)
btn_pc_of_1 = Button(window, text='10 s.', width=4, fg='gray', command=click_of_pc_1)

img = ImageTk.PhotoImage(Image.open(logo_path))
ira_logo = Label(window, image = img)

# Place widgets on a grid
lbl_txt_ip.grid(row=0, column=0, stick='w', padx=x_space, pady=y_space)
ent_ip_addrs.grid(row=0, column=1, stick='w', padx=x_space, pady=y_space)
btn_connect.grid(row=0, column=2, stick='w', padx=x_space, pady=y_space)
lbl_connect.grid(row=0, column=3, stick='w', padx=x_space, pady=y_space)

ira_logo.grid(row=0, column=4, rowspan=2, columnspan=2, stick='nswe', padx=x_space, pady=y_space)

btn_block_cntrl.grid(row=1, column=2, stick='w', padx=x_space, pady=y_space)

lbl_txt_0.grid(row=2, column=0, stick='w', padx=x_space, pady=y_space)
lbl_clr_0.grid(row=2, column=1, stick='w', padx=x_space, pady=y_space)
btn_on_0.grid(row=2, column=3, stick='w', padx=x_space, pady=y_space)
btn_of_0.grid(row=2, column=2, stick='w', padx=x_space, pady=y_space)
btn_pc_on_0.grid(row=2, column=4, stick='w', padx=x_space, pady=y_space)
btn_pc_of_0.grid(row=2, column=5, stick='w', padx=x_space, pady=y_space)

lbl_txt_1.grid(row=3, column=0, stick='w', padx=x_space, pady=y_space)
lbl_clr_1.grid(row=3, column=1, stick='w', padx=x_space, pady=y_space)
btn_on_1.grid(row=3, column=3, stick='w', padx=x_space, pady=y_space)
btn_of_1.grid(row=3, column=2, stick='w', padx=x_space, pady=y_space)
btn_pc_on_1.grid(row=3, column=4, stick='w', padx=x_space, pady=y_space)
btn_pc_of_1.grid(row=3, column=5, stick='w', padx=x_space, pady=y_space)


window.mainloop()
