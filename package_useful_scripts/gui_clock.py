from tkinter import *
import time

tk = Tk()

tk.rowconfigure(1, weight=1)
tk.columnconfigure(1, weight=1)

f = Frame(bg="Black")
f.grid(row=1, column=1, sticky="swne")

date_var = StringVar()
time_var = StringVar()
utime_var = StringVar()

date_label = Label(f, textvariable=date_var, font="Times 60 ", bg="Black", fg="#B0B000")
text_label = Label(f, text="  PC time:  ", font="Times 40 bold", bg="Black", fg="#B0B000")
time_label = Label(f, textvariable=time_var, font="Times 120 bold", bg="Black", fg="#F0F000")
utime_label = Label(f, textvariable=utime_var, font="Times 120 bold", bg="Black", fg="#F09000")

date_label.pack()
text_label.pack()
time_label.pack()
utime_label.pack()


"""Updating screen"""


def tick():
    t = time.localtime(time.time())
    ut = time.gmtime(time.time())
    fmt_d = " %A,   %Y / %m / %d   (LOC) "
    fmt_t = " LOC  %H:%M:%S  "
    fmt_ut = " UTC  %H:%M:%S  "
    date_var.set(time.strftime(fmt_d, t))
    time_var.set(time.strftime(fmt_t, t))
    utime_var.set(time.strftime(fmt_ut, ut))
    time_label.after(500, tick)  # next tick in 0.5 sec


time_label.after(500, tick)

tk.mainloop()

