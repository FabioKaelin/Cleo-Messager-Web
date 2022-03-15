import codecs
import json
import os
import platform
import random
import socket
import sys
import threading
import webbrowser
from datetime import *
from datetime import datetime
from os.path import exists
import time

import pyautogui
from flask import *
from flask import Flask, redirect, render_template, request, session, url_for

sep = "#SEP#"
end = "#END#"
nameAnswerTag = "#NAMEANSWER#"
messageTag = "#MES#"
logoutTag = "#LOGOUT#"
exitTag = "#EXIT#"
nameTag = "#NAME#"

name = "unbekannt"
port = 9898
buffer = 1024
oldName = "FabioDef"
notende = True
oldUpdate = "1"
name = oldName
messages = [("Fabio", "hallo du"),("Chris", "ich mag python")]
timestamp1 = datetime.now()
ort = None

StaticipListExists = exists(os.path.dirname(os.path.abspath(__file__))+"/data/StaticIP.txt")
if (StaticipListExists == False):
    f = open(os.path.dirname(os.path.abspath(__file__))+"/data/StaticIP.txt", "w")
    f.write("")
    f.close()

DataListExists = exists(os.path.dirname(os.path.abspath(__file__))+"/data/data.txt")
if (DataListExists == False):
    f = open(os.path.dirname(os.path.abspath(__file__))+"/data/data.txt", "w")
    f.write("")
    f.close()


f = open(os.path.dirname(os.path.abspath(__file__))+"/data/SessionIP.txt", "w")
f.write("")
f.close()


def server():
    port = 9898
    buffer = 1024
    # try:
    while True:
        sserver = socket.socket()
        sserver.bind((local_ip, port))
        sserver.listen()
        client_socket, address = sserver.accept()
        # print("Hallo")

        message = ""
        while True:
            text = client_socket.recv(buffer).decode()
            # print(text)
            message += text
            if  end in text:
                break
        # print(message)
        message = message.replace(end, "")
        # print(message)
        # print("exitTag: "+ str(exitTag) + "|||message: " + str(message) + "|||address[0]: " + str(address[0]) + "|||local_ip: " + str(local_ip))
        if (exitTag in message and address[0] == local_ip):
            if (address[0] == local_ip):
                message = message.replace(exitTag, "")
                message = message.replace(logoutTag, "")
                message = message.replace(sep, "")
                message = message.replace(nameTag, "")
                message = message.replace(messageTag, "")
                print(message + " ist ausgeloggt und das Programm wird beendet")
                exit()
        if (logoutTag in message):
            message = message.replace(exitTag, "")
            message = message.replace(logoutTag, "")
            message = message.replace(sep, "")
            message = message.replace(messageTag, "")
            message = message.replace(nameTag, "")
            print(message + " ist ausgeloggt")
            f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/data/SessionIP.txt", "r", "utf-8")
            content = f.read()
            f.close()
            content = content.replace("\r", "")
            if (len(content) > 5):
                contentArray = content.split("\n")
                filteredContent = []
                for i in reversed(contentArray):
                    # print(i)
                    if (len(i)> 5):
                        jsonObject = json.loads(i)
                        if(jsonObject["Name"] != message.lower()):
                            filteredContent.append('\n{"Name": "' + message.lower() + '", "Ip": "' + address[0] + '"}')
                for i in filteredContent:
                    f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/data/SessionIP.txt", "a", "utf-8")
                    f.write(i)
                    f.close()

        if (messageTag in message):
            message = message.replace(messageTag, "")
            messagesplit = message.split(sep)
            client_socket.close()
            sserver.close()
            print(messagesplit[0] + ": " + messagesplit[1])
            f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/data/data.txt", "a", "utf-8")
            f.write('\n{"Sender": "' + messagesplit[0] + '", "Message": "' + messagesplit[1] + '"}')
            f.close()
        elif (nameTag in message):
            message = message.replace(sep, "")
            message = message.replace(nameTag, "")
            if (address[0] == local_ip):
                global name
                name = message
                # print("Lokale IP")

                # z = threading.Thread(target=sayIP9899)
                # z.start()
                z2 = threading.Thread(target=sayIP9898)
                z2.start()
            else:
                # print("Andere IP")
                if(name != "unbekannt"):
                    # print("name ist nicht unbekannt")
                    # y9899 = threading.Thread(target=answerName, args=(address[0],9899,))
                    # y9899.start()
                    y9898 = threading.Thread(target=answerName, args=(address[0],9898,))
                    y9898.start()

            print(address[0] + " ist " + message)
            f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/data/SessionIP.txt", "a", "utf-8")
            f.write('\n{"Name": "' + message.lower() + '", "Ip": "' + address[0] + '"}')
            f.close()
        elif (nameAnswerTag in message):
            message = message.replace(sep, "")
            message = message.replace(nameAnswerTag, "")
            print(address[0] + " ist " + message)
            f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/data/SessionIP.txt", "a", "utf-8")
            f.write('\n{"Name": "' + message.lower() + '", "Ip": "' + address[0] + '"}')
            f.close()

        del sserver
        del client_socket
        del address

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
        ip = empfangToIp(empfang)
        s.connect((ip, port))
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

def answerName(empfang1, port):
        try:
            s = socket.socket()
            s.settimeout(0.01)
            s.connect((empfang1, port))
            s.send(bytes(nameAnswerTag + sep + name + end, 'UTF-8'))
            s.close()
        except:
            x = "a"

def execCollector():
    print("vor exeCollecoterexec")
    serverT = threading.Thread(target=server)
    serverT.start()
    # os.system("python " + os.path.dirname(os.path.abspath(__file__)) + "/collector.py " + os.path.dirname(os.path.abspath(__file__)))

def timeController():
    global timestamp1
    time.sleep(5)
    while True:
        now = datetime.now()
        a_timedelta = now - timestamp1
        # print(str(now)+"|||"+ str(a_timedelta))
        seconds = a_timedelta.total_seconds()
        if (seconds > 10):
            print(str(now) + "||| last: "+ str(timestamp1) + "||| sec: " + str(seconds))
            os.system("taskkill /F /IM python" + platform.python_version().split(".")[0] + "." + platform.python_version().split(".")[1] + ".exe")
        time.sleep(5)

def sayIP9898():
    for x in range(2, 255):
        try:
            ip = local_ip
            ip = ip.split(".")
            empfang1 = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(x)
            if (empfang1 != local_ip):
                # print(empfang1)
                s = socket.socket()
                s.settimeout(0.04)
                s.connect((empfang1, 9898))
                s.send(bytes(nameTag + sep + name + end, 'UTF-8'))
                s.close()
        except:
            x = "a"
    print("IP geteilt - Port:9898")

def sayIP9899():
    for x in range(2, 255):
        try:
            ip = local_ip
            ip = ip.split(".")
            empfang1 = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(x)
            # print(empfang1)
            s = socket.socket()
            s.settimeout(0.03)
            s.connect((empfang1, 9899))
            s.send(bytes(nameTag + sep + name + end, 'UTF-8'))
            s.close()
        except:
            x = "a"
    print("IP geteilt - Port:9899")

def logoutIP9898():
    global name
    nameuse = name
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
            message = logoutTag + sep + nameuse

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

def exitDelay():
    logoutT = threading.Thread(target=logoutIP9898)
    logoutT.start()
    logoutT.join()
    # time.sleep(1)
    os.system("taskkill /F /IM python" + platform.python_version().split(".")[0] + "." + platform.python_version().split(".")[1] + ".exe")

def empfangToIp(empfang):
    global ort
    # ort = "zli"
    f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/data/SessionIP.txt", "r", "utf-8")
    content = f.read()
    f.close()
    content = content.replace("\r", "")
    if (len(content) < 5):
        return empfang
    contentArray = content.split("\n")
    for i in reversed(contentArray):
        # print(i)
        if (len(i)> 5):
            jsonObject = json.loads(i)
            if(jsonObject["Name"]== empfang.lower()):
                return jsonObject["Ip"]
    if (StaticipListExists):
        global ort
        # ort = "zli"
        f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/data/StaticIP.txt", "r", "utf-8")
        content = f.read()
        f.close()
        content = content.replace("\r", "")
        if (len(content) < 5):
            return empfang
        contentArray = content.split("\n")
        for i in reversed(contentArray):
            # print(i)
            if (len(i)> 5):
                jsonObject = json.loads(i)
                if (jsonObject["Ort"] == ort.lower()):
                    if(jsonObject["Name"]== empfang.lower()):
                        return jsonObject["Ip"]
    return empfang




local_ip = getIP()
a = threading.Thread(target=execCollector)
a.start()
b = threading.Thread(target=timeController)
b.start()

app = Flask(__name__)
app.config['ENVIRONMENT'] = "development"
app.secret_key = b'kdue#-_1adf'




@app.route("/",methods=['GET', 'POST'])
def index():
    # print(session)
    global name
    global ort
    local_ip = getIP()
    if ('local_ip' in session):
        if (session['local_ip'] == local_ip):
            if ("name" in session):
                ort = session['ort']
                name = session['name']
                try:
                    s = socket.socket()
                    # s.settimeout(0.001)
                    s.connect((local_ip, 9898))
                    s.send(bytes(nameTag + sep + name + end, 'UTF-8'))
                    s.close()
                    del s
                except:
                    x = "a"
                return redirect(url_for('send'))
    session['local_ip'] = local_ip
    if ('name' in session):
        ort = session['ort']
        try:
            s = socket.socket()
            # s.settimeout(0.001)
            s.connect((local_ip, 9898))
            s.send(bytes(nameTag + sep + name + end, 'UTF-8'))
            s.close()
            del s
        except:
            x = "a"
        return redirect(url_for('send'))
    if (request.form.get("name", "") != ""):
        ort = request.form.get("ort", "")
        session['ort'] = ort
        name = request.form.get("name", "")
        session['name'] = name
        try:
            s = socket.socket()
            # s.settimeout(0.001)
            s.connect((local_ip, 9898))
            s.send(bytes(nameTag + sep + name + end, 'UTF-8'))
            s.close()
            del s
        except:
            x = "a"
        return redirect(url_for('send'))
    f = codecs.open( os.path.dirname(os.path.abspath(__file__))+"/templates/login.html", "r", "utf-8")
    indexContent = f.read()
    indexContent = indexContent.replace("{title}", "Cleo-Messenger")
    indexContent = indexContent.replace("{localIP}", local_ip)

    data = ["Cleo-Messenger", session["local_ip"]]
    return render_template("login.html", data=data)
    return indexContent

@app.route("/logout")
def logout():
    del session["name"]
    del session["ort"]
    del session["local_ip"]
    logoutT = threading.Thread(target=logoutIP9898)
    logoutT.start()
    return redirect(url_for('index'))

@app.route("/staticIP",methods=['GET', 'POST'])
def staticIP():
    if (request.form.get("ort", "") != "" and request.form.get("name", "") != "" and request.form.get("ip", "") != ""):
        ort = request.form.get("ort", "")
        name = request.form.get("name", "")
        ip = request.form.get("ip", "")
        f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/data/StaticIP.txt", "a", "utf-8")
        f.write('\n{"Ort": "' + ort.lower() + '", "Name": "' + name.lower() + '", "Ip": "' + ip + '"}')
        f.close()
        return redirect(url_for('send'))
    else:
        data = ["Cleo-Messenger", session["local_ip"]]
        return render_template("staticIP.html", data=data)

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


    data = ["Cleo-Messenger", session["local_ip"],session["name"]]

    if ("ort" in session):
        if (session["ort"] != ""):
            data.append(session["ort"])
    return render_template("send.html", data=data)

@app.route('/empfang')
def empfang():
    global timestamp1
    timestamp1 = datetime.now()


    empfangs_list = []
    f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/data/data.txt", "r", "utf-8")
    content = f.read()
    f.close()
    content = content.replace("\r", "")
    # print(len(content))
    if (len(content) < 5):
        return render_template('empty.html')
    contentArray = content.split("\n")
    reverseContent = []
    for i in reversed(contentArray):
        # print(i)
        if (len(i) > 5):
            jsonObject = json.loads(i)
            if ("Message" in jsonObject):
                reverseContent.append(jsonObject["Sender"] + ": " + jsonObject["Message"])
    # print(reverseContent)
    return render_template('empfang.html', empfangs=reverseContent)

@app.route('/empty')
def empty():
    global timestamp1
    timestamp1 = datetime.now()
    return render_template('empty.html')

@app.route('/exit')
def exit():
    pyautogui.hotkey('ctrl', 'w')
    c = threading.Thread(target=exitDelay)
    c.start()
    return "exit"

webbrowser.get().open_new(
        "http://localhost:9897/")


if __name__ == "__main__":
    app.run(host="localhost", port=9897, debug=False)

# except KeyboardInterrupt:

input("Terminate")


os.system("taskkill /F /IM python" + platform.python_version().split(".")[0] + "." + platform.python_version().split(".")[1] + ".exe")
