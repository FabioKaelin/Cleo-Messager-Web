from datetime import datetime
from datetime import *
import random
from flask import Flask, redirect, render_template, session, url_for
from flask import request
from flask import *
import json
import codecs
import platform
import os
import os
import socket
import sys
import threading
import time
import codecs
import threading
import webbrowser
import pyautogui

sep = "#SEP#"
end = "#END#"
nameAnswerTag = "#NAMEANSWER#"
exitTag = "#EXIT#"
nameTag = "#NAME#"
messageTag = "#MES#"
logoutTag = "#LOGOUT#"
port = 9898
buffer = 1024
oldName = "FabioDef"
notende = True
oldUpdate = "1"
name = oldName
messages = [("Fabio", "hallo du"),("Chris", "ich mag python")]
timestamp1 = datetime.now()


def logoutIP9898():
    for x in range(2, 255):
        try:
            ip = local_ip
            ip = ip.split(".")
            empfang1 = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(x)
            # host = getIP()
            # print(empfang1)
            # print(type(logoutTag))
            # print(type(sep))
            # print(type(name))
            message = logoutTag + sep + name

            # print(message)
            s = socket.socket()
            s.settimeout(0.01)
            s.connect((empfang1, 9898))
            s.send(bytes(message, 'UTF-8'))
            s.send(bytes(end, 'UTF-8'))
            s.close()
        except:
            x = "a"

def exit9898():
    try:
        ip = local_ip
        # print(ip)
        # host = getIP()
        s = socket.socket()
        # s.settimeout(0.1)
        s.connect((ip, 9898))
        s.send(bytes(exitTag + sep + name + end, 'UTF-8'))
        s.close()
    except:
        x = "a"

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def sendMessage(message, empfang, name):
    try:
        s = socket.socket()
        # print(empfang)
        # print(port)
        # print(s)
        s.connect((empfang, port))
        s.send(bytes(messageTag, 'UTF-8'))
        s.send(bytes(name, 'UTF-8'))

        s.send(bytes(sep, 'UTF-8'))
        oldMessage = message

        while True:
            message_bytes = message[:buffer]
            message = message[buffer:]
            if message_bytes == "":
                s.sendall(bytes(end, 'UTF-8'))
                break
            s.sendall(bytes(message_bytes, 'UTF-8'))
        s.close()
        return oldMessage
    except:
        return message

def execCollector():
    os.system("python " + os.path.dirname(os.path.abspath(__file__)) + "/collector.py "+ os.path.dirname(os.path.abspath(__file__)))

def timeController():
    global timestamp1
    time.sleep(30)
    while True:
        now = datetime.now()
        a_timedelta = now - timestamp1
        # print(str(now)+"|||"+ str(a_timedelta))
        seconds = a_timedelta.total_seconds()
        timestamp1 = datetime.now()
        if (seconds > 10):
            os.system("taskkill /F /IM python" + platform.python_version().split(".")[0] + "." + platform.python_version().split(".")[1] + ".exe")
        time.sleep(5)

def sayIP9898():
    try:
        host = getIP()
        s = socket.socket()
        # s.settimeout(0.001)
        s.connect((host, 9898))
        s.send(bytes(nameTag + sep + name + end, 'UTF-8'))
        s.close()
    except:
        x = "a"

def exitDelay():
    time.sleep(1)
    os.system("taskkill /F /IM python" + platform.python_version().split(".")[0] + "." + platform.python_version().split(".")[1] + ".exe")


local_ip = getIP()
a = threading.Thread(target=execCollector)
a.start()



b = threading.Thread(target=timeController)
b.start()

app = Flask(__name__)
# try:

app.config['ENVIRONMENT'] = "development"
app.secret_key = b'kdue#-_1adf'

@app.route("/")
def index():
    global name
    local_ip = getIP()
    session['local_ip'] = local_ip
    # if ('name' in session):
    #     name = session['name']
    #     hello = threading.Thread(target=sayIP9898)
    #     hello.start()
    #     return redirect(url_for('send'))
    if (request.args.get("name", "") != ""):
        name = request.args.get("name", "")
        session['name'] = name
        return redirect(url_for('send'))
    f = codecs.open( os.path.dirname(os.path.abspath(__file__))+"/templates/login.html", "r", "utf-8")
    indexContent = f.read()
    indexContent = indexContent.replace("{title}", "Cleo-Messenger")
    indexContent = indexContent.replace("{localIP}", local_ip)

    data = ["Cleo-Messenger", session["local_ip"]]
    return render_template("login.html", data=data)
    return indexContent

@app.route("/send", methods=['GET', 'POST'])
def send():
    global oldUpdate
    lastUpdate = request.form.get("lastUpdate", "")
    if(oldUpdate != lastUpdate):
        oldUpdate = lastUpdate
        empfang = request.form.get("empfang", "")
        nachricht = request.form.get("nachricht", "")
        # print(lastUpdate)
        if(empfang and nachricht):
            # empfang = session["empfang"]
            # nachricht = session["nachricht"]
            print(empfang + " | bekommt | " + nachricht)
            # print("Es wird eine Nachricht gesendet")
            sendMessage(nachricht, empfang, session['name'])



    # session['data'] = request.json
    # data = session.get('data')
    # print(data)
    # if('empfang' in session):

    f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"\\templates\\send.html", "r", "utf-8")
    indexContent = f.read()
    indexContent = indexContent.replace("{title}", "Cleo-Messenger")
    indexContent = indexContent.replace("{localIP}", session["local_ip"])
    indexContent = indexContent.replace("{name}", session['name'])

    data = ["Cleo-Messenger", session["local_ip"],session["name"]]
    # return indexContent
    return render_template("send.html", data=data)

@app.route('/empfang')
def empfang():
    global timestamp1
    timestamp1 = datetime.now()


    empfangs_list = []
    f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/data.txt", "r", "utf-8")
    content = f.read()
    f.close()
    content = content.replace("\r", "")
    contentArray = content.split("\n")
    reverseContent = []
    for i in reversed(contentArray):
        # print(i)
        jsonObject = json.loads(i)
        if ("Message" in jsonObject):
            reverseContent.append(jsonObject["Sender"] + ": " + jsonObject["Message"])
    # print(reverseContent)
    return render_template('empfang.html', empfangs=reverseContent)

@app.route('/exit')
def exit():
    c = threading.Thread(target=exitDelay)
    c.start()
    pyautogui.hotkey('ctrl', 'w')

    return "exit"

webbrowser.get().open_new(
        "http://localhost:9897/")


if __name__ == "__main__":
    app.run(host="localhost", port=9897, debug=False)

# except KeyboardInterrupt:

input("Terminate")


os.system("taskkill /F /IM python" + platform.python_version().split(".")[0] + "." + platform.python_version().split(".")[1] + ".exe")