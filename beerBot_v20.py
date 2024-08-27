#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import requests
import threading
import datetime
import prettytable as pt
from telegram import __version__ as TG_VER
import json
from typing import Dict, Any

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

userHome = os.getenv("HOME")
dirPath = userHome + '/beerBot-p5'

# Load config from file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN = config['TOKEN']
chat_id = config['CHAT_ID']
tmin_critical = config['tmin_critical']
tmin_warning = config['tmin_warning']
tmax_warning = config['tmax_warning']
tmax_critical = config['tmax_critical']
refresh_time = config['refresh_time']
api_base_url = config['api_base_url']
blacklist = config['blacklist']

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

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        welcome_msg
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send brief status."""
    msg = status_msg.format(f0["temp"],
                            f1["name"], f1["temp"], f1["label"],
                            f2["name"], f2["temp"], f2["label"],
                            f3["name"], f3["temp"], f3["label"])
    await update.message.reply_text(msg)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

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

    if (minutes > limit_1 and minutes <= (limit_1 + refresh_time/60)):
        print("Last data is too old! " + str(round(minutes)) + " minutes ago.")
        telegram_bot_sendtext("Último dato muy viejo! Hace " +
                              str(round(minutes)) + " minutos. Revisar RPI", "-")
    if (minutes > limit_2 and minutes <= (limit_2 + refresh_time/60)):
        print("Last data is too old! " + str(round(minutes)) + " minutes ago.")
        telegram_bot_sendtext("Último dato muy viejo! Hace " +
                              str(round(minutes)) + " minutos. Revisar RPI", "-")
    if (minutes > limit_3 and minutes <= (limit_3 + refresh_time/60)):
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

def check_temps() -> None:
    threading.Timer(refresh_time, check_temps).start()
    try:
        last_settings = requests.get('http://localhost:3001/settings').json()
        last_data = requests.get('http://localhost:3001/data').json()
        
        checkLastData(last_data['timestamp'])
        
        update_fermentor(f0, last_data, 't0')
        update_fermentor(f1, last_data, 't1', last_settings, 'label1')
        update_fermentor(f2, last_data, 't2', last_settings, 'label2')
        update_fermentor(f3, last_data, 't3', last_settings, 'label3')
        
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

def update_fermentor(ferm: Dict[str, Any], data: Dict[str, Any], temp_key: str, settings: Dict[str, Any] = None, label_key: str = None) -> None:
    ferm["temp"] = data[temp_key] if data[temp_key] != 'null' else -999
    if settings and label_key:
        ferm["label"] = settings[label_key]
    
    check_temperature_status(ferm)

def check_temperature_status(ferm: Dict[str, Any]) -> None:
    if (ferm["temp"] > tmin_warning and ferm["temp"] < tmax_warning):
        ferm["status"] = 0
        if(ferm["temp"] > (tmin_warning + 1) and ferm["temp"] < (tmax_warning - 1)):
            ferm["alarm"] = 0
        if (ferm["alarm"] == 2 and (ferm["temp"] > (tmin_warning + 1) and ferm["temp"] < (tmax_warning - 1))):
            telegram_bot_sendtext(status0_msg.format(ferm["name"]), ferm["label"])
            print("Temp en estado normal")
            ferm["alarm"] = 0
        if (ferm["alarm"] == -2 and (ferm["temp"] > (tmin_warning + 1) and ferm["temp"] < (tmax_warning - 1))):
            telegram_bot_sendtext(status0_msg.format(ferm["name"]), ferm["label"])
            print("Temp en estado normal")
            ferm["alarm"] = 0

    elif (ferm["temp"] > tmax_warning and ferm["temp"] < tmax_critical):
        ferm["status"] = 1
        if ferm["alarm"] == 0:
            telegram_bot_sendtext(status1_msg.format(
                ferm["name"], ferm["temp"], ferm["label"]), ferm["label"])
            print("Temp llegando al límite superior")
            ferm["alarm"] = 1

    elif (ferm["temp"] > tmax_critical):
        ferm["status"] = 2
        if ferm["alarm"] == 1:
            telegram_bot_sendtext(status2_msg.format(
                ferm["name"], ferm["temp"], ferm["label"]), ferm["label"])
            print("Temp sobre el límite superior!!")
            ferm["alarm"] = 2

    elif (ferm["temp"] < tmin_warning and ferm["temp"] > tmin_critical):
        ferm["status"] = -1
        if ferm["alarm"] == 0:
            telegram_bot_sendtext(status_1_msg.format(
                ferm["name"], ferm["temp"], ferm["label"]), ferm["label"])
            print("Temp llegando al límite inferior")
            ferm["alarm"] = -1

    elif (ferm["temp"] < tmin_critical):
        ferm["status"] = -2
        if ferm["alarm"] == -1:
            telegram_bot_sendtext(status_2_msg.format(
                ferm["name"], ferm["temp"], ferm["label"]), ferm["label"])
            print("Temp debajo del límite inferior!!")
            ferm["alarm"] = -2

check_temps()

def main() -> None:
    """Start the bot."""
    telegram_bot_sendtext(welcome_msg, "-")

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
