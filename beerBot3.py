# -*- coding: utf-8 -*-
'''
Bot para telegram
'''
import logging
import threading
import requests
from telegram.ext import (Updater, CommandHandler)
from telegram import (ParseMode)
import os
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
{}: \n
Temp: \t {:.1f} °C \n
Contenido:\t {}
{}: \n
Temp: \t {:.1f} °C \n
Contenido:\t {}
{}: \n
Temp: \t {:.1f} °C \n
Contenido:\t {}
"""
info_msg = """
Link a la web => http://34.227.26.80//
"""


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
    msg = status_msg
    # Responde directametne en el canal donde se le ha hablado.
    update.message.reply_text(msg)


def info(update, context):
    '''
Envía el link a la web
    '''
    cid = update.message.chat_id
    msg = info_msg
    # Responde directametne en el canal donde se le ha hablado.
    update.message.reply_text(msg)


def checkTemps():
    threading.Timer(30, checkTemps).start()
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

    dp.add_error_handler(error_callback)
    # Comienza el bot
    updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
    updater.idle()


print("i")

if __name__ == '__main__':
    print(('[Nombre del bot] Start...'))
    main()
