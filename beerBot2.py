import requests
import time

tmin_critical = 15
tmin_warning = 16

tmax_warning = 23
tmax_critical = 24

f1 = {
    "name": "Ferm. 1",
    "temp": -999,
    "label": "label1",
    "status": 999,
    "alarm": 0
}
f2 = {
    "name": "Ferm. 2",
    "temp": -999,
    "label": "label2",
    "status": 999,
    "alarm": 0
}
f3 = {
    "name": "Ferm. 3",
    "temp": -999,
    "label": "label3",
    "status": 999,
    "alarm": 0
}

while True:

    # Load last data and settings from database
    lastSettings = requests.get('http://localhost:3001/settings')
    lastData = requests.get('http://localhost:3001/data')

    # Convert the data into json
    data_json = lastData.json()
    settings_json = lastSettings.json()

    # Assign the data to each ferm.

    # Ferm 1:
    f1["temp"] = data_json['t1']
    f1["label"] = settings_json['label1']

    if (f1["temp"] > tmin_warning and f1["temp"] < tmax_warning):
        f1["status"] = 0
        f1["alarm"] = 0
        if f1["alarm"] == 2:
            print("Temp en estado normal")
            f1["alarm"] = 0
        if f1["alarm"] == -2:
            print("Temp en estado normal")
            f1["alarm"] = 0

    elif (f1["temp"] > tmax_warning and f1["temp"] < tmax_critical):
        f1["status"] = 1
        if f1["alarm"] == 0:
            print("Temp llegando al límite superior")
            f1["alarm"] = 1

    elif (f1["temp"] > tmax_critical):
        f1["status"] = 2
        if f1["alarm"] == 1:
            print("Temp sobre el límite superior!!")
            f1["alarm"] = 2

    elif (f1["temp"] < tmin_warning and f1["temp"] > tmin_critical):
        f1["status"] = -1
        if f1["alarm"] == 0:
            print("Temp llegando al límite inferior")
            f1["alarm"] = -1

    elif (f1["temp"] < tmin_critical):
        f1["status"] = -2
        if f1["alarm"] == -1:
            print("Temp debajo del límite inferior!!")
            f1["alarm"] = -2

    # Ferm 2:
    f2["temp"] = data_json['t2']
    f2["label"] = settings_json['label2']

    # Ferm 3:
    f3["temp"] = data_json['t3']
    f3["label"] = settings_json['label3']

    # print(f1)
    # print(f2)
    # print(f3)

    time.sleep(30)


# print (data_json)
# print(settings_json)
