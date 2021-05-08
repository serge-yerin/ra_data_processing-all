from threading import Thread
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

"""
The GUI program to control ADR receiver according to schedule
"""
adr_ip = '192.168.1.171'


def start_adr_connection_thread():
    pass


# *******************************************************************************
#                             M A I N    W I N D O W                            *
# *******************************************************************************

x_space = (5, 5)
y_space = (5, 5)

window = Tk()
window.title('ADR control GUI v.2021.05.08 (c) YeS')
window.rowconfigure(0, minsize=30, weight=1)
window.columnconfigure(1, minsize=40, weight=1)

tab_parent = ttk.Notebook(window)

tab_main = ttk.Frame(tab_parent)
tab_settings = ttk.Frame(tab_parent)

tab_parent.add(tab_main, text='   Main window   ')
tab_parent.add(tab_settings, text='   Settings   ')
tab_parent.pack(expand=1, fill="both")

frame_adr_status = LabelFrame(tab_main, text="ADR connection status")

btn_adr_connect = Button(frame_adr_status, text="Connect to ADR", relief='raised', command=start_adr_connection_thread)
lbl_adr_status = Label(frame_adr_status, text='Disconnected', font='none 12', width=12, bg='gray')
lbl_adr_ip = Label(frame_adr_status, text="ADR IP address:")
ent_adr_ip = Entry(frame_adr_status, width=15)
ent_adr_ip.insert(0, adr_ip)

frame_adr_status.grid(row=0, column=0, rowspan=1, columnspan=1, stick='w', padx=10, pady=10)

btn_adr_connect.grid(row=0, column=0, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
lbl_adr_status.grid(row=0, column=1, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
lbl_adr_ip.grid(row=0, column=2, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
ent_adr_ip.grid(row=0, column=3, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)



window.mainloop()
