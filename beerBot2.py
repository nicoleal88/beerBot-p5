import requests
import time

tmin_warning = 16
tmin_critical = 15

tmax_warning = 23
tmax_critical = 24

f1 = {
    "name": "Ferm. 1",
            "temp": -999,
            "label": "label1",
            "status": 999,
            "alarm": 999
}
f2 = {
    "name": "Ferm. 2",
            "temp": -999,
            "label": "label2",
            "status": 999,
            "alarm": 999
}
f3 = {
    "name": "Ferm. 3",
            "temp": -999,
            "label": "label3",
            "status": 999,
            "alarm": 999
}

print(f1)
print(f2)
print(f3)

while True:

    # Load last data and settings from database
    lastSettings = requests.get('http://localhost:3001/settings')
    lastData = requests.get('http://localhost:3001/data')

    # Convert the data into json
    data_json = lastData.json()
    settings_json = lastSettings.json()

    # Assign the data to each ferm.
    f1 = {
        "temp": data_json['t1'],
        "label": settings_json['label1']
    }
    f2 = {
        "temp": data_json['t2'],
        "label": settings_json['label2']
    }
    f3 = {
        "temp": data_json['t3'],
        "label": settings_json['label3']
    }

    print(f1)
    print(f2)
    print(f3)

    time.sleep(30)

# print (data_json)
# print(settings_json)
