#!/usr/bin/python3
import RPi.GPIO as GPIO
import os
# import threading

# importing the requests library
import requests
import json
import random
import time
from datetime import datetime
endpoint = "http://34.227.26.80/data"
# endpoint = "http://localhost:3000/data"

idSensorA = '28-020291770688'
idSensor1 = '28-020592453487'
idSensor2 = '28-02049245c8d5'
idSensor3 = '28-020192451d5e'

Temps = [20, 20, 20, 20]

dataBuffer = []

pin3v3 = 7
# pinRelayCON = 37
# pinRelayEV1 = 33
# pinRelayEV2 = 36
# pinRelayEV3 = 32
# pinButton1 = 18
# pinButton2 = 22
# pinButton3 = 29
# pinButton4 = 31
pinOneWire1 = 12    # BCM 18
pinOneWire2 = 13    # BCM 27
pinOneWire3 = 15    # BCM 22
pinOneWire4 = 16    # BCM 23

GPIO.setwarnings(False)         # to avoid default oneWire pin assignment(pin4)
GPIO.setmode(GPIO.BOARD)        # set board mode to board
GPIO.setup(pin3v3, GPIO.OUT)        # setup pin
# GPIO.setup(pinRelayEV1, GPIO.OUT)   # setup pin
# GPIO.setup(pinRelayEV2, GPIO.OUT)   # setup pin
# GPIO.setup(pinRelayEV3, GPIO.OUT)   # setup pin
# GPIO.setup(pinRelayCON, GPIO.OUT)   # setup pin
# GPIO.setup(pinButton1, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # setup pin
# GPIO.setup(pinButton2, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # setup pin
# GPIO.setup(pinButton3, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # setup pin
# GPIO.setup(pinButton4, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # setup pin
GPIO.output(pin3v3, GPIO.HIGH)      # turn on pin

time.sleep(2)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

baseDir = '/sys/bus/w1/devices/'
# deviceFolder = glob.glob(baseDir + '28*')[0]
# deviceFile = deviceFolder + '/w1_slave'

userHome = os.getenv("HOME")


def read_temp_raw(id):
    deviceFile = baseDir + id + '/w1_slave'
    f = open(deviceFile, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(id):
    lines = read_temp_raw(id)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        # temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c


def readTemps():
    # threading.Timer(30, readTemps).start()
    Temps[0] = read_temp(idSensorA)
    Temps[1] = read_temp(idSensor1)
    Temps[2] = read_temp(idSensor2)
    Temps[3] = read_temp(idSensor3)


def postData(data):
    r = requests.post(url=endpoint, json=data)
    # extracting response text
    resp = r.text
    status = r.status_code
    # print(data)
    print(resp, status)
    return status

# readTemps()


while True:

    readTemps()

    # current date and time
    now = datetime.now()
    timestamp = int(datetime.timestamp(now)*1000)

    # Generate payload to be sent
    payload = {'timestamp': timestamp,
               't0': Temps[0], 't1': Temps[1], 't2': Temps[2], 't3': Temps[3]}

    try:
        if status == 200:
            with open("/home/pi/beerBot-p5/data.txt", "w") as file:
                text = "{}\t{}\t{}\t{}\t{}".format(
                    payload["t0"], payload["t1"], payload["t2"], payload["t3"], payload["timestamp"])
                file.write(text)
    except:
        print("Couldn't write data.txt")

    try:
        # sending post request and saving response as response object
        status = postData(payload)

        if status != 200:
            print("The status was: " + str(status))
            dataBuffer.append(payload)
            print("The data in buffer is: ")
            print(dataBuffer)

        if len(dataBuffer) > 0 and status == 200:
            time.sleep(2)
            print("Starting to send data in buffer...")
            for i in range(10):
                b = dataBuffer.pop()
                print("Posting data from buffer")
                postData(b)
                print("Data remaining in buffer: " + str(len(dataBuffer)))
                if len(dataBuffer) == 0:
                    break
                else:
                    time.sleep(2)

    except:
        dataBuffer.append(payload)
        print("An exeption has ocurred! ")
        print("The data in buffer is: ")
        print(dataBuffer)

    time.sleep(30)
