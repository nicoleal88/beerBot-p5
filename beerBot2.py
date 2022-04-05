import requests
import time
import os

connection_timeout = 30  # seconds

userHome = os.getenv("HOME")
dirPath = userHome + '/beerBot-p5'

config = {}
with open(dirPath + '/config', 'r') as f:
    File = f.readlines()
    for lines in File:
        splittedLine = lines.split('=')
        if len(splittedLine) == 2:
            config[splittedLine[0]] = splittedLine[1][:-1]

token = config['TOKEN']
chat_id = config['CHAT_ID']
botURL = "https://api.telegram.org/bot{}/".format(token)
logName = config['LOG']
logFile = dirPath + '/' + logName
luser = config['LUSER']


def telegram_bot_sendtext(bot_message):

    bot_token = token
    bot_chatID = chat_id
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    # 👍👌🥶🥵👀❄️⚠️🚩📟🍺🍻
    return response.json()


telegram_bot_sendtext("📟 Iniciando DragerBot 🍻")

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
            telegram_bot_sendtext("👍 Temp en estado normal")
            print("Temp en estado normal")
            f1["alarm"] = 0
        if f1["alarm"] == -2:
            telegram_bot_sendtext("👍 Temp en estado normal")
            print("Temp en estado normal")
            f1["alarm"] = 0

    elif (f1["temp"] > tmax_warning and f1["temp"] < tmax_critical):
        f1["status"] = 1
        if f1["alarm"] == 0:
            telegram_bot_sendtext("⚠️ 🥵👀 Temp llegando al límite superior")
            print("Temp llegando al límite superior")
            f1["alarm"] = 1

    elif (f1["temp"] > tmax_critical):
        f1["status"] = 2
        if f1["alarm"] == 1:
            telegram_bot_sendtext("🚩 🔥🔥 Temp sobre el límite superior!!")
            print("Temp sobre el límite superior!!")
            f1["alarm"] = 2

    elif (f1["temp"] < tmin_warning and f1["temp"] > tmin_critical):
        f1["status"] = -1
        if f1["alarm"] == 0:
            telegram_bot_sendtext("⚠️ 🥶👀 Temp llegando al límite inferior")
            print("Temp llegando al límite inferior")
            f1["alarm"] = -1

    elif (f1["temp"] < tmin_critical):
        f1["status"] = -2
        if f1["alarm"] == -1:
            telegram_bot_sendtext("🚩 ❄️❄️ Temp debajo del límite inferior!!")
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
