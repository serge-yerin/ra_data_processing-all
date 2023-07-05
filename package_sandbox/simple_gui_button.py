from tkinter import *
from time import strftime
from threading import Thread
import time
import tkinter.ttk

x_space = (10, 10)
y_space = (10, 10)

def click_on_0():
    lbl_clr_0.config(text='OFF', bg='light green')
def click_on_1():
    lbl_clr_1.config(text='OFF', bg='light green')
def click_on_2():
    lbl_clr_2.config(text='OFF', bg='light green')
def click_on_all():
    lbl_clr_0.config(text='OFF', bg='light green')
    lbl_clr_1.config(text='OFF', bg='light green')
    lbl_clr_2.config(text='OFF', bg='light green')


def click_off_0():
    lbl_clr_0.config(text='ON', bg='pink')
def click_off_1():
    lbl_clr_1.config(text='ON', bg='pink')
def click_off_2():
    lbl_clr_2.config(text='ON', bg='pink')
def click_off_all():
    lbl_clr_0.config(text='ON', bg='pink')
    lbl_clr_1.config(text='ON', bg='pink')
    lbl_clr_2.config(text='ON', bg='pink')

# Renew time readings each second
def time_show():
    loc_time_str = strftime('%Y . %m . %d     %H : %M : %S ')
    utc_time_str = strftime('%Y . %m . %d     %H : %M : %S ', time.gmtime())
    time_lbl.config(text='\n     Local:     ' + loc_time_str +
                         '     \n      UTC:      ' + utc_time_str + '     \n')
    time_lbl.after(1000, time_show)

# Renew progress bar value
def bar():
    for i in range(100):
        progressbar['value'] = i * 1
        window.update_idletasks()
        time.sleep(0.1)
    progressbar['value'] = 100

# Start another thread for progress bar
def another_thread():
    control_thread = Thread(target=bar, daemon=True)
    control_thread.start()

# Main window creation
window = Tk()
window.title('Simple GUI')
window.rowconfigure(0, minsize=30, weight=1)
window.columnconfigure(1, minsize=40, weight=1)

time_lbl = Label(window, font=('none', 14, 'bold'), background='black', foreground='yellow')

btn_of_all = Button(window, text='All OFF', font = 'none 9 bold', width=10, command=click_on_all )
btn_on_all = Button(window, text='All ON', font = 'none 9 bold',  width=10, command=click_off_all)

lbl_txt_0 = Label(window, text = 'LED 1:', font = 'none 12', width=10)
lbl_clr_0 = Label(window, text = 'Unknown state', font = 'none 12', width=12, bg='yellow')
btn_of_0 = Button(window, text='OFF', width=10, command=click_on_0 )
btn_on_0 = Button(window, text='ON',  width=10, command=click_off_0)

lbl_txt_1 = Label(window, text = 'LED 2:', font = 'none 12', width=10)
lbl_clr_1 = Label(window, text = 'Unknown state', font = 'none 12', width=12, bg='yellow')
btn_of_1 = Button(window, text='OFF', width=10, command=click_on_1 )
btn_on_1 = Button(window, text='ON',  width=10, command=click_off_1)

lbl_txt_2 = Label(window, text = 'LED 3:', font = 'none 12', width=10)
lbl_clr_2 = Label(window, text = 'Unknown state', font = 'none 12', width=12, bg='yellow')
btn_of_2 = Button(window, text='OFF', width=10, command=click_on_2 )
btn_on_2 = Button(window, text='ON',  width=10, command=click_off_2)


btn_start = Button(window, text='Start', width=10, command=another_thread)

control_thread = Thread(target=time_show, daemon=True)
control_thread.start()

# Progress bar widget
progressbar = tkinter.ttk.Progressbar(window, orient=HORIZONTAL, length=400, mode='determinate')


# Place widgets on a grid
time_lbl.grid(row=0, column=0, columnspan=4, padx=10, pady=y_space)

btn_on_all.grid(row=1, column=3, stick='w', padx=x_space, pady=y_space)
btn_of_all.grid(row=1, column=2, stick='w', padx=x_space, pady=y_space)

lbl_txt_0.grid(row=2, column=0, stick='w', padx=x_space, pady=y_space)
lbl_clr_0.grid(row=2, column=1, stick='w', padx=x_space, pady=y_space)
btn_on_0.grid(row=2, column=3, stick='w', padx=x_space, pady=y_space)
btn_of_0.grid(row=2, column=2, stick='w', padx=x_space, pady=y_space)

lbl_txt_1.grid(row=3, column=0, stick='w', padx=x_space, pady=y_space)
lbl_clr_1.grid(row=3, column=1, stick='w', padx=x_space, pady=y_space)
btn_on_1.grid(row=3, column=3, stick='w', padx=x_space, pady=y_space)
btn_of_1.grid(row=3, column=2, stick='w', padx=x_space, pady=y_space)

lbl_txt_2.grid(row=4, column=0, stick='w', padx=x_space, pady=y_space)
lbl_clr_2.grid(row=4, column=1, stick='w', padx=x_space, pady=y_space)
btn_on_2.grid(row=4, column=3, stick='w', padx=x_space, pady=y_space)
btn_of_2.grid(row=4, column=2, stick='w', padx=x_space, pady=y_space)

btn_start.grid(row=5, column=0, stick='w', padx=x_space, pady=y_space)
progressbar.grid(row=5, column=1, stick='w', columnspan=3, padx=10, pady=y_space)

window.mainloop()