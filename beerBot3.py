# -*- coding: utf-8 -*-
'''
Bot para telegram
'''

import logging
import threading
import requests
import prettytable as pt
from telegram.ext import (Updater, CommandHandler)
from telegram import (ParseMode)
import os
import datetime
userHome = os.getenv("HOME")
dirPath = userHome + '/beerBot-p5'

# [Opcional] Recomendable poner un log con los errores que apareceran por pantalla.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


config = {}
with open(dirPath + '/config', 'r') as f:
    File = f.readlines()
    for lines in File:
        splittedLine = lines.split('=')
        if len(splittedLine) == 2:
            config[splittedLine[0]] = splittedLine[1][:-1]

TOKEN = config['TOKEN']
chat_id = config['CHAT_ID']

# Messages
welcome_msg = """
📟 Iniciando DragerBot 🍻 \n
@pichedron
"""

status0_msg = """
👍 {} en estado normal
Temp: \t {:.1f} °C \n
Contenido:\t {}
"""

status1_msg = """
Alerta! ⚠️🔥 \n
{} llegando al límite superior \n
Temp: \t {:.1f} °C \n
Contenido:\t {}
"""

status2_msg = """
Alerta! 🚩🔥 \n
{} sobre el límite superior! \n
Temp: \t {:.1f} °C \n
Contenido:\t {}
"""

status_1_msg = """
Alerta! ⚠️❄️ \n
{} llegando al límite inferior \n
Temp: \t {:.1f} °C \n
Contenido:\t {}
"""

status_2_msg = """
Alerta! 🚩❄️ \n
{} bajo el límite inferior! \n
Temp: \t {:.1f} °C \n
Contenido:\t {}
"""

status_msg = """
Status: \n
--------------------------------------- \n
Temp. ambiente: \t {:.1f} °C \n
--------------------------------------- \n
{}: \n
- Temp: \t {:.1f} °C \n
- Contenido:\t {} \n
--------------------------------------- \n
{}: \n
- Temp: \t {:.1f} °C \n
- Contenido:\t {} \n
--------------------------------------- \n
{}: \n
- Temp: \t {:.1f} °C \n
- Contenido:\t {} \n
--------------------------------------- \n
"""
info_msg = """
Link a la web => http://34.227.26.80//
"""

tmin_critical = 15
tmin_warning = 16
# 17, 18, 19, 20, 21, 22
tmax_warning = 23
tmax_critical = 24


f0 = {
    "temp": -999,
}
f1 = {
    "name": "Ferm. 1",
    "temp": -999,
    "label": "label1",
    "status": 999,
    "alarm": 2
}
f2 = {
    "name": "Ferm. 2",
    "temp": -999,
    "label": "label2",
    "status": 999,
    "alarm": 2
}
f3 = {
    "name": "Ferm. 3",
    "temp": -999,
    "label": "label3",
    "status": 999,
    "alarm": 2
}


def start(update, context):
    ''' START '''
    # Enviar un mensaje a un ID determinado.
    context.bot.send_message(update.message.chat_id,
                             welcome_msg, parse_mode=ParseMode.HTML)


def status(update, context):
    '''
Envía el estado de los fermentadores
    '''
    cid = update.message.chat_id
    msg = status_msg.format(f0["temp"],
                            f1["name"], f1["temp"], f1["label"],
                            f2["name"], f2["temp"], f2["label"],
                            f3["name"], f3["temp"], f3["label"])
    # Responde directametne en el canal donde se le ha hablado.
    update.message.reply_text(msg)


def status2(update, context):
    '''
    Envía el estado de los fermentadores
    '''
    # lastStatus = requests.get('http://localhost:3001/status')

    # Convert the data into json
    # status_json = lastStatus.json()
    # f1["label"] = status_json['label1']

    table = pt.PrettyTable(['N', 'Cont', 'Temp', 'Prom', 'Dias'])
    table.align['N'] = 'l'
    table.align['Cont'] = 'l'
    table.align['Temp'] = 'r'
    table.align['Prom'] = 'r'
    table.align['Dias'] = 'l'

    data = [
        ('F1', f1["label"], f1["temp"], f1["temp"], '5'),
        ('F2', f2["label"], f2["temp"], f2["temp"], '4'),
        ('F3', f3["label"], f3["temp"], f3["temp"], '14'),
    ]
    for ferm, cont, temp, promedio, tiempo in data:
        table.add_row(
            [ferm,
             '{0:.6s}'.format(cont),
             '{0:.1f}'.format(temp),
             '{0:.1f}'.format(promedio),
             tiempo+"d"])

    update.message.reply_text(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)
    # or use markdown
    # update.message.reply_text(
    #     '`Lalala`', parse_mode=ParseMode.MARKDOWN_V2)


def info(update, context):
    '''
    Envía el link a la web
    '''
    cid = update.message.chat_id
    msg = info_msg
    # Responde directametne en el canal donde se le ha hablado.
    update.message.reply_text(msg)


def checkBlacklist(text):
    blacklist = ["vacio", "vacío"]
    # blacklist = []

    if text.lower().strip() in blacklist:
        return False
    else:
        return True


def checkLastData(timestamp):

    limit_1 = 15
    limit_2 = 60
    limit_3 = 240

    ts = timestamp

    converted_ts = datetime.datetime.fromtimestamp(round(ts / 1000))
    current_time_utc = datetime.datetime.utcnow()

    #print((current_time_utc - converted_ts))
    minutes = ((current_time_utc - converted_ts).total_seconds() / 60)

    # if minutes < limit:
    #     print(minutes)

    if (minutes > limit_1 and minutes < (limit_1 + 1)):
        print("Last data is too old! " + str(round(minutes)) + " minutes ago.")
        telegram_bot_sendtext("Último dato muy viejo! Hace " +
                              str(round(minutes)) + " minutos. Revisar RPI", "-")
    if (minutes > limit_2 and minutes < (limit_2 + 1)):
        print("Last data is too old! " + str(round(minutes)) + " minutes ago.")
        telegram_bot_sendtext("Último dato muy viejo! Hace " +
                              str(round(minutes)) + " minutos. Revisar RPI", "-")
    if (minutes > limit_3 and minutes < (limit_3 + 1)):
        print("Last data is too old! " + str(round(minutes)) + " minutes ago.")
        telegram_bot_sendtext("Último dato muy viejo! Hace " +
                              str(round(minutes)) + " minutos. Revisar RPI", "-")


def telegram_bot_sendtext(bot_message, label):
    if checkBlacklist(label):
        bot_token = TOKEN
        bot_chatID = chat_id
        send_text = 'https://api.telegram.org/bot' + bot_token + \
            '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        response = requests.get(send_text)
        # 👍👌🥶🥵👀❄️🔥⚠️🚩📟🍺🍻
        return response.json()
    else:
        print("Alerta en fermentador vacío")


def checkTemps():
    threading.Timer(30, checkTemps).start()
    # Load last data and settings from database
    lastSettings = requests.get('http://localhost:3001/settings')
    lastData = requests.get('http://localhost:3001/data')

    # Convert the data into json
    data_json = lastData.json()
    settings_json = lastSettings.json()

    ts = data_json['timestamp']

    checkLastData(ts)

    # Assign the data to each ferm.
    f0["temp"] = data_json['t0']
    # Ferm 1:
    f1["temp"] = data_json['t1']
    f1["label"] = settings_json['label1']

    if (f1["temp"] > tmin_warning and f1["temp"] < tmax_warning):
        f1["status"] = 0
        if(f1["temp"] > (tmin_warning + 1) and f1["temp"] < (tmax_warning - 1)):
            f1["alarm"] = 0
        if (f1["alarm"] == 2 and (f1["temp"] > (tmin_warning + 1) and f1["temp"] < (tmax_warning - 1))):
            telegram_bot_sendtext(status0_msg.format(f1["name"]), f1["label"])
            print("Temp en estado normal")
            f1["alarm"] = 0
        if (f1["alarm"] == -2 and (f1["temp"] > (tmin_warning + 1) and f1["temp"] < (tmax_warning - 1))):
            telegram_bot_sendtext(status0_msg.format(f1["name"]), f1["label"])
            print("Temp en estado normal")
            f1["alarm"] = 0

    elif (f1["temp"] > tmax_warning and f1["temp"] < tmax_critical):
        f1["status"] = 1
        if f1["alarm"] == 0:
            telegram_bot_sendtext(status1_msg.format(
                f1["name"], f1["temp"], f1["label"]), f1["label"])
            print("Temp llegando al límite superior")
            f1["alarm"] = 1

    elif (f1["temp"] > tmax_critical):
        f1["status"] = 2
        if f1["alarm"] == 1:
            telegram_bot_sendtext(status2_msg.format(
                f1["name"], f1["temp"], f1["label"]), f1["label"])
            print("Temp sobre el límite superior!!")
            f1["alarm"] = 2

    elif (f1["temp"] < tmin_warning and f1["temp"] > tmin_critical):
        f1["status"] = -1
        if f1["alarm"] == 0:
            telegram_bot_sendtext(status_1_msg.format(
                f1["name"], f1["temp"], f1["label"]), f1["label"])
            print("Temp llegando al límite inferior")
            f1["alarm"] = -1

    elif (f1["temp"] < tmin_critical):
        f1["status"] = -2
        if f1["alarm"] == -1:
            telegram_bot_sendtext(status_2_msg.format(
                f1["name"], f1["temp"], f1["label"]), f1["label"])
            print("Temp debajo del límite inferior!!")
            f1["alarm"] = -2

    # Ferm 2:
    f2["temp"] = data_json['t2']
    f2["label"] = settings_json['label2']

    if (f2["temp"] > tmin_warning and f2["temp"] < tmax_warning):
        f2["status"] = 0
        if(f2["temp"] > (tmin_warning + 1) and f2["temp"] < (tmax_warning - 1)):
            f2["alarm"] = 0
        if (f2["alarm"] == 2 and (f2["temp"] > (tmin_warning + 1) and f2["temp"] < (tmax_warning - 1))):
            telegram_bot_sendtext(status0_msg.format(f2["name"]), f2["label"])
            print("Temp en estado normal")
            f2["alarm"] = 0
        if (f2["alarm"] == -2 and (f2["temp"] > (tmin_warning + 1) and f2["temp"] < (tmax_warning - 1))):
            telegram_bot_sendtext(status0_msg.format(f2["name"]), f2["label"])
            print("Temp en estado normal")
            f2["alarm"] = 0

    elif (f2["temp"] > tmax_warning and f2["temp"] < tmax_critical):
        f2["status"] = 1
        if f2["alarm"] == 0:
            telegram_bot_sendtext(status1_msg.format(
                f2["name"], f2["temp"], f2["label"]), f2["label"])
            print("Temp llegando al límite superior")
            f2["alarm"] = 1

    elif (f2["temp"] > tmax_critical):
        f2["status"] = 2
        if f2["alarm"] == 1:
            telegram_bot_sendtext(status2_msg.format(
                f2["name"], f2["temp"], f2["label"]), f2["label"])
            print("Temp sobre el límite superior!!")
            f2["alarm"] = 2

    elif (f2["temp"] < tmin_warning and f2["temp"] > tmin_critical):
        f2["status"] = -1
        if f2["alarm"] == 0:
            telegram_bot_sendtext(status_1_msg.format(
                f2["name"], f2["temp"], f2["label"]), f2["label"])
            print("Temp llegando al límite inferior")
            f2["alarm"] = -1

    elif (f2["temp"] < tmin_critical):
        f2["status"] = -2
        if f2["alarm"] == -1:
            telegram_bot_sendtext(status_2_msg.format(
                f2["name"], f2["temp"], f2["label"]), f2["label"])
            print("Temp debajo del límite inferior!!")
            f2["alarm"] = -2

    # Ferm 3:
    f3["temp"] = data_json['t3']
    f3["label"] = settings_json['label3']

    if (f3["temp"] > tmin_warning and f3["temp"] < tmax_warning):
        f3["status"] = 0
        if(f3["temp"] > (tmin_warning + 1) and f3["temp"] < (tmax_warning - 1)):
            f3["alarm"] = 0
        if (f3["alarm"] == 2 and (f3["temp"] > (tmin_warning + 1) and f3["temp"] < (tmax_warning - 1))):
            telegram_bot_sendtext(status0_msg.format(f3["name"]), f3["label"])
            print("Temp en estado normal")
            f3["alarm"] = 0
        if (f3["alarm"] == -2 and (f3["temp"] > (tmin_warning + 1) and f3["temp"] < (tmax_warning - 1))):
            telegram_bot_sendtext(status0_msg.format(f3["name"]), f3["label"])
            print("Temp en estado normal")
            f3["alarm"] = 0

    elif (f3["temp"] > tmax_warning and f3["temp"] < tmax_critical):
        f3["status"] = 1
        if f3["alarm"] == 0:
            telegram_bot_sendtext(status1_msg.format(
                f3["name"], f3["temp"], f3["label"]), f3["label"])
            print("Temp llegando al límite superior")
            f3["alarm"] = 1

    elif (f3["temp"] > tmax_critical):
        f3["status"] = 2
        if f3["alarm"] == 1:
            telegram_bot_sendtext(status2_msg.format(
                f3["name"], f3["temp"], f3["label"]), f3["label"])
            print("Temp sobre el límite superior!!")
            f3["alarm"] = 2

    elif (f3["temp"] < tmin_warning and f3["temp"] > tmin_critical):
        f3["status"] = -1
        if f3["alarm"] == 0:
            telegram_bot_sendtext(status_1_msg.format(
                f3["name"], f3["temp"], f3["label"]), f3["label"])
            print("Temp llegando al límite inferior")
            f3["alarm"] = -1

    elif (f3["temp"] < tmin_critical):
        f3["status"] = -2
        if f3["alarm"] == -1:
            telegram_bot_sendtext(status_2_msg.format(
                f3["name"], f3["temp"], f3["label"]), f3["label"])
            print("Temp debajo del límite inferior!!")
            f3["alarm"] = -2


checkTemps()


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Eventos que activarán nuestro bot.
    # /comandos
    dp.add_handler(CommandHandler('start',	start))
    dp.add_handler(CommandHandler('status',	status))
    dp.add_handler(CommandHandler('status2', status2))
    dp.add_handler(CommandHandler('info', info))

    dp.add_error_handler(error_callback)
    # Comienza el bot
    updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
    updater.idle()


if __name__ == '__main__':
    print(('DragerBot Starting...'))
    main()
