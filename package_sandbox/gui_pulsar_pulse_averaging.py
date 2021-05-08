from threading import Thread
from tkinter import *
import tkinter.filedialog
from os import path
import numpy as np

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

"""
The GUI program requests for a txt file with some lines of some float numbers, reads the array from the file 
and averages the array according to the numbers of columns and rows specified by user.
If the number of rows/columns is not divisible to the number of rows/columns to average, 
the remain rows/columns are truncated   
"""


def chose_source_file():
    filetypes = (('text files', '*.txt'), ('All files', '*.*'))
    file_path = tkinter.filedialog.askopenfilename(title='Open a file', filetypes=filetypes)
    entry_source_file.delete(0, END)
    entry_source_file.insert(0, file_path)
    btn_start.focus_set()


def start_process_thread():
    lbl_status.config(text='Conversion in progress...', font='none 9 bold', fg="Dark blue")
    check_thread = Thread(target=process_file, daemon=True)
    check_thread.start()


def process_file():
    btn_start.config(relief=SUNKEN)
    btn_start.config(state=DISABLED)
    file_path = entry_source_file.get()
    time_aver_const = int(entry_time_aver.get())
    freq_aver_const = int(entry_freq_aver.get())
    try:
        file = open(file_path, 'r')
        array = np.array([[float(digit) for digit in line.split()] for line in file])
        file.close()
        a, b = array.shape

        # Cutting the array ends which are not divisible to average constants
        array = array[:(array.shape[0] // freq_aver_const) * freq_aver_const,
                      :(array.shape[1] // time_aver_const) * time_aver_const]

        # Time averaging
        if time_aver_const > 1:
            array = array.reshape(array.shape[0], -1, time_aver_const)
            array = np.mean(array, axis=2)

        # Frequency averaging
        if freq_aver_const > 1:
            array = np.transpose(array)
            array = np.mean(array.reshape(array.shape[0], -1, freq_aver_const), axis=2)
            array = np.transpose(array)

        c, d = array.shape

        # Save averaged data to a new txt file
        result_txt_file = open(file_path[:-4] + '_dtx' + str(time_aver_const) +
                               '_dfx' + str(freq_aver_const) + '.txt', "w")
        for freq in range(array.shape[0]):
            result_txt_file.write(' '.join('  {:+12.7E}'.format(array[freq, i])
                                  for i in range(array.shape[1])) + ' \n')
        result_txt_file.close()

        # Display results of the averaging in the main window
        text = 'Conversion finished, array of shape ' + str(a) + ' x ' + str(b) + \
               ' was reshaped to '+str(c)+' x '+str(d)
        lbl_status.config(text=text,  font='none 9 bold', fg="Dark blue")

    except FileNotFoundError:
        lbl_status.config(text='File not found, select new file!', font='none 9 bold', fg="Dark red")

    except ValueError:
        lbl_status.config(text='Conversion error! Check file correctness!', font='none 9 bold', fg="Dark red")

    except EOFError:
        lbl_status.config(text='Conversion error! Try another file.', font='none 9 bold', fg="Dark red")

    else:
        pass
    finally:
        pass
    btn_start.config(relief=RAISED)
    btn_start.config(state=NORMAL)


# *******************************************************************************
#                             M A I N    W I N D O W                            *
# *******************************************************************************

x_space = (5, 5)
y_space = (5, 5)

window = Tk()
window.title('Pulsar pulse averaging')
window.rowconfigure(0, minsize=30, weight=1)
window.columnconfigure(1, minsize=40, weight=1)

lbl_path_in = Label(window, text="  Path:")
btn_select_file = Button(window, text="Select file", relief='raised', command=chose_source_file)
btn_select_file.focus_set()
entry_source_file = Entry(window)

entry_time_aver = Spinbox(window, from_=1, to=100)
entry_freq_aver = Spinbox(window, from_=1, to=100)
lbl_time_aver = Label(window, text="Average time points:")
lbl_freq_aver = Label(window, text="Average frequency points:")
lbl_status = Label(window, text="")

btn_start = Button(window, text="Average pulse", relief='raised', command=start_process_thread)

lbl_copyright = Label(window, text="v.2021.05.07 (c) IRA NASU   Serge Yerin (YeS)   e-mail: yerin.serge@gmail.com")
lbl_copyright.config(font=("Arial", 8), fg="dark blue")

lbl_path_in.grid(row=0, column=1, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
btn_select_file.grid(row=0, column=0, rowspan=1, columnspan=1, stick='nswe', padx=x_space, pady=y_space)
entry_source_file.grid(row=0, column=2, rowspan=1, columnspan=2, stick='nswe', padx=x_space, pady=y_space)

entry_time_aver.grid(row=1, column=2, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space)
entry_freq_aver.grid(row=2, column=2, rowspan=1, columnspan=1, stick='w', padx=x_space, pady=y_space)

lbl_time_aver.grid(row=1, column=0, rowspan=1, columnspan=2, stick='e', padx=x_space, pady=y_space)
lbl_freq_aver.grid(row=2, column=0, rowspan=1, columnspan=2, stick='e', padx=x_space, pady=y_space)

btn_start.grid(row=1, column=3, rowspan=2, columnspan=2, stick='nswe', padx=x_space, pady=y_space)
lbl_status.grid(row=3, column=0, rowspan=1, columnspan=4, stick='nswe', padx=x_space, pady=y_space)
lbl_copyright.grid(row=4, column=2, rowspan=1, columnspan=2, stick='e', padx=x_space, pady=y_space)

window.mainloop()
