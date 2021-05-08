from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import tkinter.filedialog
import time
from time import strftime
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

"""
The GUI program to control ADR receiver according to schedule
"""
adr_ip = '192.168.1.171'


# Renew time readings each second
def time_show():
    loc_time_str = strftime('%Y . %m . %d     %H : %M : %S ')
    utc_time_str = strftime('%Y . %m . %d     %H : %M : %S ', time.gmtime())
    time_lbl.config(text='\n     Local:     ' + loc_time_str +
                         '     \n      UTC:      ' + utc_time_str + '     \n')
    time_lbl.after(1000, time_show)


def choose_schedule_file():
    filetypes = (('text files', '*.txt'), ('All files', '*.*'))
    file_path = tkinter.filedialog.askopenfilename(title='Open a file', filetypes=filetypes)
    entry_schedule_file.delete(0, END)
    entry_schedule_file.insert(0, file_path)


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
frame_schedule = LabelFrame(tab_main, text="Schedule")
frame_control = LabelFrame(tab_main, text="Load schedule")
time_lbl.grid(row=0, column=0, rowspan=1, columnspan=1, stick='wens', padx=10, pady=10)
frame_adr_status.grid(row=1, column=0, rowspan=1, columnspan=1, stick='wn', padx=10, pady=10)
frame_schedule.grid(row=0, column=1, rowspan=5, columnspan=1, stick='wn', padx=10, pady=10)
frame_control.grid(row=2, column=0, rowspan=1, columnspan=1, stick='wne', padx=10, pady=10)


# Setting elements of the frame "ADR status"
btn_adr_connect = Button(frame_adr_status, text="Connect to ADR", relief='raised', command=start_adr_connection_thread)
lbl_adr_status = Label(frame_adr_status, text='Disconnected', font='none 12', width=12, bg='gray')
lbl_adr_ip = Label(frame_adr_status, text="ADR IP address:")
ent_adr_ip = Entry(frame_adr_status, width=15)
ent_adr_ip.insert(0, adr_ip)

btn_adr_connect.grid(row=0, column=0, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
lbl_adr_status.grid(row=0, column=1, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
lbl_adr_ip.grid(row=0, column=2, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
ent_adr_ip.grid(row=0, column=3, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)

y_space_adr = 1

lbl_adr_fadc_nam = Label(frame_adr_status, text="ADC frequency:")
lbl_adr_fadc_val = Label(frame_adr_status, text="")
lbl_adr_sadc_nam = Label(frame_adr_status, text="ADC source:")
lbl_adr_sadc_val = Label(frame_adr_status, text="Internal", font='none 9', width=12, bg='yellow')

lbl_adr_fadc_nam.grid(row=1, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_fadc_val.grid(row=1, column=1, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_sadc_nam.grid(row=1, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_sadc_val.grid(row=1, column=3, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)

lbl_adr_mode_nam = Label(frame_adr_status, text="ADC mode:")
lbl_adr_mode_val = Label(frame_adr_status, text="")
lbl_adr_chnl_nam = Label(frame_adr_status, text="Channels:")
lbl_adr_chnl_val = Label(frame_adr_status, text="")

lbl_adr_mode_nam.grid(row=2, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_mode_val.grid(row=2, column=1, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_chnl_nam.grid(row=2, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_chnl_val.grid(row=2, column=3, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)

lbl_adr_fres_nam = Label(frame_adr_status, text="Freq resolution:")
lbl_adr_fres_val = Label(frame_adr_status, text="")
lbl_adr_tres_nam = Label(frame_adr_status, text="Time resolution:")
lbl_adr_tres_val = Label(frame_adr_status, text="")

lbl_adr_fres_nam.grid(row=3, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_fres_val.grid(row=3, column=1, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_tres_nam.grid(row=3, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_tres_val.grid(row=3, column=3, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)

lbl_adr_flow_nam = Label(frame_adr_status, text="From frequency:")
lbl_adr_flow_val = Label(frame_adr_status, text="")
lbl_adr_fhig_nam = Label(frame_adr_status, text="To frequency:")
lbl_adr_fhig_val = Label(frame_adr_status, text="")

lbl_adr_flow_nam.grid(row=4, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_flow_val.grid(row=4, column=1, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_fhig_nam.grid(row=4, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_fhig_val.grid(row=4, column=3, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)


lbl_adr_rnam_nam = Label(frame_adr_status, text="Receiver name:")
lbl_adr_rnam_val = Label(frame_adr_status, text="")
lbl_adr_rnam_nam.grid(row=5, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_rnam_val.grid(row=5, column=1, rowspan=1, columnspan=3, stick='e', padx=x_space, pady=y_space_adr)

lbl_adr_obsn_nam = Label(frame_adr_status, text="Observatory:")
lbl_adr_obsn_val = Label(frame_adr_status, text="")
lbl_adr_obsn_nam.grid(row=6, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_obsn_val.grid(row=6, column=1, rowspan=1, columnspan=3, stick='e', padx=x_space, pady=y_space_adr)

lbl_adr_desc_nam = Label(frame_adr_status, text="Description:")
lbl_adr_desc_val = Label(frame_adr_status, text="")
lbl_adr_desc_nam.grid(row=7, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_desc_val.grid(row=7, column=1, rowspan=1, columnspan=3, stick='e', padx=x_space, pady=y_space_adr)

lbl_adr_sdms_nam = Label(frame_adr_status, text="Sum/diff mode:")
lbl_adr_sdms_val = Label(frame_adr_status, text="OFF", font='none 9', width=12, bg='light green')
lbl_adr_nfcs_nam = Label(frame_adr_status, text="New file create:")
lbl_adr_nfcs_val = Label(frame_adr_status, text="ON", font='none 9', width=12, bg='light green')

lbl_adr_sdms_nam.grid(row=8, column=0, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_sdms_val.grid(row=8, column=1, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_nfcs_nam.grid(row=8, column=2, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)
lbl_adr_nfcs_val.grid(row=8, column=3, rowspan=1, columnspan=1, stick='e', padx=x_space, pady=y_space_adr)

# Setting elements of the frame "Control"

lbl_path_in = Label(frame_control, text="  Path:")
btn_select_file = Button(frame_control, text="Select file", relief='raised', width=12, command=choose_schedule_file)
# btn_select_file.focus_set()
entry_schedule_file = Entry(frame_control, width=45)

lbl_path_in.grid(row=0, column=1, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
btn_select_file.grid(row=0, column=0, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
entry_schedule_file.grid(row=0, column=2, rowspan=1, columnspan=2, stick='nswe', padx=x_space, pady=y_space)

# Setting elements of the frame "Schedule"

ent_schedule = ScrolledText(frame_schedule, width=45)
ent_schedule.insert(INSERT, "Schedule appears here... \n", 'line')
ent_schedule.tag_config('line', background='light green')
# ent_schedule.insert(END, " in ScrolledText")
ent_schedule.config(state=DISABLED)



ent_schedule.grid(row=0, column=0, rowspan=15, columnspan=3, stick='nswe', padx=x_space, pady=y_space)

# Start time thread
time_display_thread = Thread(target=time_show, daemon=True)
time_display_thread.start()

window.mainloop()
