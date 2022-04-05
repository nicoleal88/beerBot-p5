import requests

tmin_warning = 16
tmin_critical = 15

tmax_warning = 23
tmax_critical = 24

# Load last data and settings from database
lastSettings = requests.get('http://localhost:3001/settings')
lastData = requests.get('http://localhost:3001/data')

# Convert the data into json
data_json = lastData.json()
settings_json = lastSettings.json()

# Assign the data to each ferm.
f1 = {
        "name": "Ferm. 1",
        "temp": data_json['t1'],
        "label": settings_json['label1']
        }
f2 = {
        "name": "Ferm. 2",
        "temp": data_json['t2'],
        "label": settings_json['label2']
        }
f3 = {
        "name": "Ferm. 3",
        "temp": data_json['t3'],
        "label": settings_json['label3']
        }

print(f1)
print(f2)
print(f3)

# print (data_json)
# print(settings_json)
