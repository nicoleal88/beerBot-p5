from tkinter import *
from tkinter.ttk import *
import datetime
import platform
import os

window = Tk()
window.title("Data Vis Offline")
window.geometry('400x300')


def clock():
    date_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S/%p")
    date, time1 = date_time.split()
    time2, time3 = time1.split('/')
    hour, minutes, seconds = time2.split(':')
    if int(hour) > 11 and int(hour) < 24:
        time = str(int(hour) - 12) + ':' + minutes + \
            ':' + seconds + ' ' + time3
    else:
        time = time2 + ' ' + time3
    time_label.config(text=time)
    date_label.config(text=date)
    time_label.after(1000, clock)


def update():

    f1 = "test"
    f2 = "test2"
    f3 = "test3"

    with open("data.txt", "r") as f:
        # Writing data to a file
        last_line = f.readlines()[-1]
        f1, f2, f3 = last_line.split()
        f.close()  # to change file access modes

    f1_label.config(text=f1)
    f2_label.config(text=f2)
    f3_label.config(text=f3)
    f1_label.after(1000, update)


time_label = Label(font='calibri 40 bold', foreground='black')
time_label.pack(anchor='center')
date_label = Label(font='calibri 40 bold', foreground='black')
date_label.pack(anchor='s')
f1_label = Label(font='calibri 40 bold', foreground='black')
f1_label.pack(anchor='center')
f2_label = Label(font='calibri 40 bold', foreground='black')
f2_label.pack(anchor='center')
f3_label = Label(font='calibri 40 bold', foreground='black')
f3_label.pack(anchor='center')

clock()
update()
window.mainloop()
