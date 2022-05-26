from tkinter import *
from tkinter.ttk import *
import datetime
import platform
import os
import time

window = Tk()
window.title("Data Vis Offline")
# window.geometry('400x300')


def clock():
    date_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    date, time = date_time.split()
    # time2, time3 = time1.split('/')
    # hour, minutes, seconds = time2.split(':')
    # if int(hour) > 11 and int(hour) < 24:
    #     time = str(int(hour) - 12) + ':' + minutes + \
    #         ':' + seconds + ' ' + time3
    # else:
    #     time = time2 + ' ' + time3
    time_label.config(text=time)
    date_label.config(text=date)
    time_label.after(1000, clock)


def update():

    t0 = "-99"
    f1 = "-99"
    f2 = "-99"
    f3 = "-99"
    ts = "1"

    with open("data.txt", "r") as f:
        # Writing data to a file
        try:
            data = f.readlines()[0]
            t0, f1, f2, f3, ts = data.split()
            f.close()  # to change file access modes
        except:
            print("Couldn't load data.txt")
            time.sleep(120)

    converted_ts = datetime.datetime.fromtimestamp(round(int(ts) / 1000))
    current_time_utc = datetime.datetime.now()

    #print((current_time_utc - converted_ts))
    minutes = ((current_time_utc - converted_ts).total_seconds() / 60)

    t0_label.config(text="T amb.: {:.1f} °C".format(float(t0)))
    f1_label.config(text="T1: {:.1f} °C".format(float(f1)))
    f2_label.config(text="T2: {:.1f} °C".format(float(f2)))
    f3_label.config(text="T3: {:.1f} °C".format(float(f3)))
    ts_label.config(text="Ultimo dato: {}".format(converted_ts))
    if(minutes > 15):
        alarm_label.config(
            text="Último dato muy viejo!\nHace {} minutos! \nLlamar a Pichedron!".format(round(minutes)))
    else:
        alarm_label.config(text="")
    f1_label.after(1000, update)


time_label = Label(font='calibri 32', foreground='black')
time_label.grid(row=0, column=0)
# time_label.pack(anchor='center')
date_label = Label(font='calibri 32', foreground='black')
date_label.grid(row=0, column=2)
# date_label.pack(anchor='s')
t0_label = Label(font='calibri 20', foreground='black')
t0_label.grid(row=1, column=1, pady=4)
# t0_label.pack(anchor='center')
f1_label = Label(font='calibri 40 bold', foreground='black')
f1_label.grid(row=2, column=2, pady=24)
# f1_label.pack(anchor='center')
f2_label = Label(font='calibri 40 bold', foreground='black')
f2_label.grid(row=2, column=1, pady=24)
# f2_label.pack(anchor='center')
f3_label = Label(font='calibri 40 bold', foreground='black')
f3_label.grid(row=2, column=0, pady=24)
# f3_label.pack(anchor='center')
ts_label = Label(font='calibri 20', foreground='black')
ts_label.grid(row=5, column=1, pady=4)
# ts_label.pack(anchor='center')
alarm_label = Label(font='calibri 20 bold', foreground='red')
alarm_label.grid(row=6, column=1)
# alarm_label.pack(anchor='center')

clock()
update()
window.mainloop()
