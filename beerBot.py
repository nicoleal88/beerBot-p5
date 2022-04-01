#!/usr/bin/python3

import json
import requests
from requests import ConnectionError
import time
import os
import datetime
from subprocess import Popen, PIPE
# import re
import sys

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
# chat_id = config['CHAT_ID']
botURL = "https://api.telegram.org/bot{}/".format(token)
logName = config['LOG']
logFile = dirPath + '/' + logName
# plotDir = config['PLOT_DIR']
# imgPath = dirPath + '/' + plotDir + '/output.png'
luser = config['LUSER']
# regDir = config['REG_DIR']
# regPath = dirPath + '/' + regDir
# tmpFile = dirPath + '/.tmp'


# def removeTempFile():
#     try:
#         os.remove(tmpFile)
#         print("Removing old tempFile...")
#     except:
#         print("Old tempFile not found")


# def removePlot(when):
#     try:
#         os.remove(imgPath)
#         print("Removing old plot {}...".format(when))
#     except:
#         print("Old plot not found")


# def trySendImage(chat, times, text):
#     for i in range(times):
#         try:
#             sendImage(chat)
#             log("Sent {} plot".format(text), "to: " + str(chat))
#             break
#         except:
#             print('Plot not found ({}), retrying...'.format(i))
#             time.sleep(1)


# -----------------------------------------------------------------------------
# Method that joins the register of the last two days.
# "today" timestamp is got from datetime method.
# "yesterday timestap is just got by substracting 1 to the "today" timestamp.
# Filtering has been added to avoid corrupted lines.
# Format - 19 characters for timestamp ("YYYYY/MM/DD HH:MM:SS")
#        - 4  columns separated by tabs (timestamp T1 T2 T3)
# The output file name is "DIR_PATH/tmpFile"
# -----------------------------------------------------------------------------


# def filesJoin():
#     removeTempFile()
#     today = datetime.date.today()
#     yesterday = today - datetime.timedelta(1)
#     todayFile = regPath + \
#         today.strftime('/%Y/%m/') + \
#         today.strftime('%Y-%m-%d.dat')
#     yesterdayFile = regPath + \
#         yesterday.strftime('/%Y/%m/') + \
#         yesterday.strftime('%Y-%m-%d.dat')
#     lines = [yesterdayFile, todayFile]
#     print (lines)
#     with open(tmpFile, 'w') as outfile:
#         for fname in lines:
#             print ("Trying to open {}".format(fname))
#             try:
#                 with open(fname, 'r') as infile:
#                     a = infile.readlines()
#                     for lines in a:
#                         thisLine = lines.rstrip()
#                         words = thisLine.split('\t')
#                         timeStamp = words[0]
#                         if (len(timeStamp) == 19) and (len(words) == 5):
#                             if ((float(words[1]) >= -30) and
#                                     (float(words[2]) >= -30) and
#                                     (float(words[3]) >= -30) and
#                                     (float(words[4]) >= -30)):
#                                 outfile.write(lines)
#             except:
#                 log('Error while reading file: ' + fname)
#     print("Done joining")

# -----------------------------------------------------------------------------
# Method that returns a report containg the data of the last 10 minutes
# 10 minutes is just got considering: 1 tic every 5 seconds,
#                                  -> 12 tics per minute,
#                                  -> 120 tics every 10 minutes.
# So just reading the last 120 lines of the last register is enough.
# A mean value is got every minute, so 10 lines of data are returned.
# -----------------------------------------------------------------------------


# def get_10mReport():
#     filesJoin()
#     process = Popen(['tail', '-n', '120', tmpFile], stdout=PIPE,
#                     stderr=PIPE, universal_newlines=True)
#     stdout, stderr = process.communicate()
#     out = stdout
#     lines = out.split("\n")
#     previousMinute = lines[0].split("\t")[0][:-3]
#     count = 0
#     t1_m = 0
#     t2_m = 0
#     t3_m = 0
#     lt = ""
#     for ls in lines:
#         words = ls.split("\t")
#         thisMinute = words[0][:-3]
#         if (thisMinute == previousMinute):
#             count = count + 1
#             t1_m = t1_m + float(words[1])
#             t2_m = t2_m + float(words[2])
#             t3_m = t3_m + float(words[3])
#         else:
#             tws = previousMinute.split(" ")
#             t1_m = t1_m/count
#             t2_m = t2_m/count
#             t3_m = t3_m/count
#             lt += "{}/{} {}   {:.1f}   {:.1f}   {:.1f}\n".format(tws[0].split("/")[2],
#                                                                  tws[0].split("/")[1],
#                                                                  tws[1],
#                                                                  t1_m,
#                                                                  t2_m,
#                                                                  t3_m)
#             previousMinute = thisMinute
#             count = 1
#             if (words[0] != ""):
#                 t1_m = float(words[1])
#                 t2_m = float(words[2])
#                 t3_m = float(words[3])
#     return lt


# -----------------------------------------------------------------------------
# Method that returns a report containg the data of the last hour.
# 1 hour is just got considering: 1 tic every 5 seconds,
#                              -> 12 tics per minute,
#                              -> 720 tics per hour.
# So just reading the last 720 lines of the last register is enough.
# A mean value is got every 5 minutes, so 12 lines of data are returned.
# -----------------------------------------------------------------------------


# def get_1hReport():
#     filesJoin()
#     process = Popen(['tail', '-n', '720', tmpFile], stdout=PIPE,
#                     stderr=PIPE, universal_newlines=True)
#     stdout, stderr = process.communicate()
#     out = stdout
#     lines = out.split("\n")
#     if (int(lines[0].split("\t")[0][-4:-3]) < 5):
#         previous5mBin = lines[0].split("\t")[0][:-4] + '0'
#     else:
#         previous5mBin = lines[0].split("\t")[0][:-4] + '5'
#     count = 0
#     t1_m = 0
#     t2_m = 0
#     t3_m = 0
#     lt = ""
#     for ls in lines:
#         words = ls.split("\t")
#         if (len(words[0]) > 2):
#             if (int(words[0][-4:-3]) < 5):
#                 this5mBin = words[0][:-4] + '0'
#             else:
#                 this5mBin = words[0][:-4] + '5'
#         else:
#             this5mBin = previous5mBin[:-1] + '6'
#         if (this5mBin == previous5mBin):
#             count = count + 1
#             t1_m = t1_m + float(words[1])
#             t2_m = t2_m + float(words[2])
#             t3_m = t3_m + float(words[3])
#         else:
#             tws = previous5mBin.split(" ")
#             t1_m = t1_m/count
#             t2_m = t2_m/count
#             t3_m = t3_m/count
#             lt += "{}/{} {}   {:.1f}   {:.1f}   {:.1f}\n".format(tws[0].split("/")[2],
#                                                                  tws[0].split("/")[1],
#                                                                  tws[1],
#                                                                  t1_m,
#                                                                  t2_m,
#                                                                  t3_m)
#             previous5mBin = this5mBin
#             count = 1
#             if (words[0] != ""):
#                 t1_m = float(words[1])
#                 t2_m = float(words[2])
#                 t3_m = float(words[3])
#     return lt

# -----------------------------------------------------------------------------
# Method that returns a report containg the data of the last day.
# 1 day is just got considering: 1 tic every 5 seconds,
#                             -> 12 tics per minute,
#                             -> 720 tics per hour,
#                             -> 17280 tics per day.
# So just reading the last 17280 lines of the last register is enough.
# A mean value is got every 30 minutes, so 48 lines of data are returned.
# -----------------------------------------------------------------------------


# def get_1dReport():
#     filesJoin()
#     process = Popen(['tail', '-n', '17280', tmpFile], stdout=PIPE,
#                     stderr=PIPE, universal_newlines=True)
#     stdout, stderr = process.communicate()
#     out = stdout
#     lines = out.split("\n")
#     if (int(lines[0].split("\t")[0][-5:-3]) < 30):
#         previous30mBin = lines[0].split("\t")[0][:-5] + '00:00'
#     else:
#         previous30mBin = lines[0].split("\t")[0][:-5] + '30:00'
#     count = 0
#     t1_m = 0
#     t2_m = 0
#     t3_m = 0
#     lt = ""
#     for ls in lines:
#         words = ls.split("\t")
#         if (len(words[0]) > 2):
#             if (int(words[0].split("\t")[0][-5:-3]) < 30):
#                 this30mBin = words[0].split("\t")[0][:-5] + '00:00'
#             else:
#                 this30mBin = words[0].split("\t")[0][:-5] + '30:00'
#         else:
#             this30mBin = previous30mBin[:-1] + '1'
#         if (this30mBin == previous30mBin):
#             count = count + 1
#             t1_m = t1_m + float(words[1])
#             t2_m = t2_m + float(words[2])
#             t3_m = t3_m + float(words[3])
#         else:
#             tws = previous30mBin.split(" ")
#             t1_m = t1_m/count
#             t2_m = t2_m/count
#             t3_m = t3_m/count
#             lt += "{}/{} {}   {:.1f}   {:.1f}   {:.1f}\n".format(tws[0].split("/")[2],
#                                                                  tws[0].split("/")[1],
#                                                                  tws[1][:-3],
#                                                                  t1_m,
#                                                                  t2_m,
#                                                                  t3_m)
#             previous30mBin = this30mBin
#             count = 1
#             if (words[0] != ""):
#                 t1_m = float(words[1])
#                 t2_m = float(words[2])
#                 t3_m = float(words[3])
#     return lt


# -----------------------------------------------------------------------------
# Method that gets URL in the telegram bot link.
# -----------------------------------------------------------------------------


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

# -----------------------------------------------------------------------------
# Method that gets the content of the URL using json package.
# -----------------------------------------------------------------------------


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

# -----------------------------------------------------------------------------
# Method that gets the updates in the telegram bot link.
# -----------------------------------------------------------------------------


def get_updates():
    url = botURL + "getUpdates"
    js = get_json_from_url(url)
    return js

# -----------------------------------------------------------------------------
# Method that gets the chat id and the text from the last chat input in the
# telegram bot link.
# -----------------------------------------------------------------------------


def get_last_chat_id_and_text(updates):
    try:
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)
    except KeyError:
        return ('error_Text', 'error_chat_id')

# -----------------------------------------------------------------------------
# Method that sends the input message to the telegram bot link.
# -----------------------------------------------------------------------------


def send_message(text, chat_id):
    url = botURL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

# -----------------------------------------------------------------------------
# Method that sends the input image to the telegram bot link.
# -----------------------------------------------------------------------------


def sendImage(chat_id):
    url = botURL + "sendPhoto"
    files = {'photo': open(imgPath, 'rb')}
    data = {'chat_id': chat_id}
    r = requests.post(url, files=files, data=data)
    log(str(r.status_code))
    log(r.reason)
    log(str(r.content))

# -----------------------------------------------------------------------------
# Method that process the input command.
# -----------------------------------------------------------------------------


def processCommand(command, chat_id):
    words = command.split("@")
    log("Processing received command", command + " from " + str(chat_id))
    if (words[0] == "/blabla"):
        send_message("balinazo", chat_id)
        log("Test response")
    # elif (words[0] == "/reporte_10m"):
    #     send_message(get_10mReport(), str(chat_id))
    #     log("Sending 10-minute report", "to: " + str(chat_id))
    # elif (words[0] == "/reporte_1h"):
    #     send_message(get_1hReport(), str(chat_id))
    #     log("Sending 1-hour report", "to: " + str(chat_id))
    # elif (words[0] == "/reporte_1d"):
    #     send_message(get_1dReport(), str(chat_id))
    #     log("Sending 1-day report", "to: " + str(chat_id))
    # elif (words[0] == "/grafico_10m"):
    #     filesJoin()
    #     run_cmd = dirPath + '/plot.py'
    #     process = Popen([run_cmd, '120'], stdout=PIPE,
    #                     stderr=PIPE, universal_newlines=True)
    #     stdout, stderr = process.communicate()
    #     out = stdout
    #     lines = out.split("\n")
    #     try:
    #         done = lines[1].split(" ")
    #         doneSt = done[0] + ' ' + done[1]
    #         if (doneSt == 'Plot done'):
    #             log(done[0] + ' ' + done[1])
    #             trySendImage(chat_id, 10, '10-min')
    #             removePlot('after sending 10-min plot')
    #     except:
    #         log('plot.py error output')
    # elif (words[0] == "/grafico_1h"):
    #     filesJoin()
    #     run_cmd = dirPath + '/plot.py'
    #     process = Popen([run_cmd, '720'], stdout=PIPE,
    #                     stderr=PIPE, universal_newlines=True)
    #     stdout, stderr = process.communicate()
    #     out = stdout
    #     lines = out.split("\n")
    #     try:
    #         done = lines[1].split(" ")
    #         doneSt = done[0] + ' ' + done[1]
    #         if (doneSt == 'Plot done'):
    #             log(done[0] + ' ' +  done[1])
    #             trySendImage(chat_id, 10, '1-hour')
    #             removePlot('after sending 1-hour plot')
    #     except:
    #         log('plot.py error output')
    # elif (words[0] == "/grafico_1d"):
    #     filesJoin()
    #     run_cmd = dirPath + '/plot.py'
    #     process = Popen([run_cmd, '17280'], stdout=PIPE,
    #                     stderr=PIPE, universal_newlines=True)
    #     stdout, stderr = process.communicate()
    #     out = stdout
    #     lines = out.split("\n")
    #     try:
    #         done = lines[1].split(" ")
    #         doneSt = done[0] + ' ' + done[1]
    #         if (doneSt == 'Plot done'):
    #             log(done[0] + ' ' + done[1])
    #             trySendImage(chat_id, 10, '1-day')
    #             removePlot('after sending 1-day plot')
    #     except:
    #         log('plot.py error output')
    elif (words[0] == '/kill'):
        send_message('Hasta la vista...' + luser, str(chat_id))
        killBot(str(chat_id))
    # elif (words[0][:1] == '/'):
    #     if words[0][1].isnumeric() and words[0][2] == ' ':
    #         send_message(historyLog(words[0]), chat_id)
    else:
        send_message("nosee", chat_id)
        log("Invalid command")

# -----------------------------------------------------------------------------
# Method that log the input into the log file.
# -----------------------------------------------------------------------------


def log(text, data=''):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime("%Y/%m/%d %H:%M:%S")
    file = open(logFile, 'a')
    file.write(st + '\t' + text + '\t' + data + '\n')
    file.close()

# -----------------------------------------------------------------------------
# Method that returns a history log tag to the bot (to be printed out).
# It also modifies three history files: 1.txt, 2.txt and 3.txt, one per
# sensor. Those history files stores: 1- timestamp
#                                     2- name
#                                     3- stage (fermentacion-maduracion)
# These files are used to get the plot tags (plot.py) and a complete
# report at the end of the process.
# -----------------------------------------------------------------------------


# def historyLog(hLog):
#     ferNum = hLog[1]
#     fase = ''
#     name = hLog[3:].split(' ')
#     fermList = ['fermentacion',
#                 'ferment',
#                 'ferme',
#                 'ferm',
#                 'fer',
#                 'fe',
#                 'f']
#     maduList = ['maduracion',
#                 'madurac',
#                 'madura',
#                 'madu',
#                 'mad',
#                 'ma',
#                 'm']
#     if (name[-1].lower() in fermList):
#         name.pop()
#         fase = 'Fermentacion'
#     if (name[-1].lower() in maduList):
#         name.pop()
#         fase = 'Maduracion'
#     ts = time.time()
#     timeTag = datetime.datetime.fromtimestamp(ts).strftime("%Y/%m/%d %H:%M:%S\t")
#     regTag = timeTag
#     for words in name:
#         regTag += words + '_'
#     regTag = regTag[:-1] + '\t' + fase + '\n'
#     historyLogFile = dirPath + '/' + ferNum + '.txt'
#     file = open(historyLogFile, 'a')
#     process = Popen(['tail', '-n', '1', historyLogFile], stdout=PIPE,
#                     stderr=PIPE, universal_newlines=True)
#     stdout, stderr = process.communicate()
#     out = stdout
#     lines = out.split("\n")
#     if (len(lines) > 1):
#         idNum = int(lines[0].split('\t')[0])
#         idNum = str(idNum + 1)
#     else:
#         idNum = ferNum + '001'
#     print(idNum)
#     file.write(idNum + '\t' + regTag)
#     file.close()
#     retStr = '______________________________\n'
#     retStr += 'Nuevo registro historico\n'
#     retStr += 'Fecha: ' + timeTag[:-1] + '\n'
#     retStr += 'Fermentador: ' + ferNum + '\n'
#     retStr += 'Tipo: ' + ' '.join(map(str, name)) + '\n'
#     retStr += 'Fase: ' + fase + '\n'
#     retStr += '______________________________\n'
#     print(retStr)
#     return retStr


# -----------------------------------------------------------------------------
# Method that kills the bot when called.
# The idea is to kill the bot using the text input of the bot.
# The watchdog should launch it again when crontab executes it.
# -----------------------------------------------------------------------------


def killBot(chat_id):
    log('Killed by bot message!', 'by: ' + chat_id)
    sys.exit()

# -----------------------------------------------------------------------------
# Main method that removes temp files and plots; initialize the last
# chat_id and text of the bot; shows a 'Hola mundo' message with information
# of the running dragerBot.py; checks the .pid file and try to get
# errors; finally it checks every 3 seconds the bot chat_id and text
# processing commnads input in the bot. Connection error stops the bot 30
# seconds and then try to get bot paramenters.
# -----------------------------------------------------------------------------


def main():
    # removeTempFile()
    # removePlot('for the first time')
    last_text, last_chat = get_last_chat_id_and_text(get_updates())
    beerBotPath = dirPath + '/beerBot.py'
    if os.path.isfile(beerBotPath):
        last_modified_date = datetime.datetime.fromtimestamp(
            os.path.getmtime(beerBotPath))
    else:
        last_modified_date = datetime.datetime.fromtimestamp(0)
    send_message("Hola mundo...\nArchivo modificado el " +
                 last_modified_date.strftime("%Y/%m/%d %H:%M:%S"), last_chat)
    log("Bot relanzado. Version del " +
        last_modified_date.strftime("%Y/%m/%d %H:%M:%S"))
    while True:
        # pidCheck()
        try:
            thisText, thisChat = get_last_chat_id_and_text(get_updates())
            if (thisText == 'error_Text' and thisChat == 'error_chat_id'):
                thisText = last_text
                thisChat = last_chat
            if (thisText != last_text) or (thisChat != last_chat):
                if (thisText[:1] == "/"):
                    processCommand(thisText, thisChat)
                else:
                    send_message(thisText, thisChat)
                last_text = thisText
                last_chat = thisChat
            else:
                pass
            time.sleep(3)
        except ConnectionError:
            print("--> ", datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                  "Sin conexion - Esperando red...")
            log("Waiting for network...")
            time.sleep(30)


# -----------------------------------------------------------------------------
# Main program.
# -----------------------------------------------------------------------------


if __name__ == '__main__':
    while True:
        main()
