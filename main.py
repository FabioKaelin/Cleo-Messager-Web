from audioop import reverse
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
from pkg_resources import Environment


import pyautogui
from flask import *
from flask import Flask, redirect, render_template, request, session, url_for



# sys.dont_write_bytecode = True
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
oldName = "FabioDev"
notende = True
oldUpdate = "1"
name = oldName
messages = [("Fabio", "hallo du"),("Chris", "ich mag python")]
timestamp1 = datetime.now()
ort = None
folderPath = os.path.dirname(os.path.abspath(__file__))

dataExists = os.path.isdir(folderPath+'/data')
if (dataExists == False):
    os.mkdir(folderPath+"/data")


StaticipListExists = exists(folderPath+"/data/StaticIP.txt")
if (StaticipListExists == False):
    f = open(folderPath+"/data/StaticIP.txt", "w")
    f.write("")
    f.close()

DataListExists = exists(folderPath+"/data/data.txt")
if (DataListExists == False):
    f = open(folderPath+"/data/data.txt", "w")
    f.write("")
    f.close()

f = open(folderPath+"/data/SessionIP.txt", "w")
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

        message = ""
        while True:
            text = client_socket.recv(buffer).decode()
            message += text
            if  end in text:
                break
        message = message.replace(end, "")
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
            f = codecs.open(folderPath+"/data/SessionIP.txt", "r", "utf-8")
            content = f.read()
            f.close()
            content = content.replace("\r", "")
            if (len(content) > 5):
                contentArray = content.split("\n")
                filteredContent = []
                for i in reversed(contentArray):
                    if (len(i)> 5):
                        jsonObject = json.loads(i)
                        if(jsonObject["Name"] != message.lower()):
                            filteredContent.append('\n{"Name": "' + message.lower() + '", "Ip": "' + address[0] + '"}')

                f = codecs.open(folderPath+"/data/SessionIP.txt", "w", "utf-8")
                f.write("")
                f.close()
                for i in filteredContent:
                    f = codecs.open(folderPath+"/data/SessionIP.txt", "a", "utf-8")
                    f.write(i)
                    f.close()

        if (messageTag in message):
            message = message.replace(messageTag, "")
            messagesplit = message.split(sep)
            client_socket.close()
            sserver.close()
            print(messagesplit[0] + ": " + messagesplit[1])
            f = codecs.open(folderPath+"/data/data.txt", "a", "utf-8")
            f.write('\n{"Sender": "' + messagesplit[0].lower() + '", "Message": "' + messagesplit[1] + '", "Art": "Empfang"}')
            f.close()
        elif (nameTag in message):
            message = message.replace(sep, "")
            message = message.replace(nameTag, "")
            if (address[0] == local_ip):
                global name
                name = message
                z2 = threading.Thread(target=sayIP9898)
                z2.start()
            else:
                if(name != "unbekannt"):
                    y9898 = threading.Thread(target=answerName, args=(address[0],9898,))
                    y9898.start()

            print(address[0] + " ist " + message)
            f = codecs.open(folderPath+"/data/SessionIP.txt", "a", "utf-8")
            f.write('\n{"Name": "' + message.lower() + '", "Ip": "' + address[0] + '"}')
            f.close()
        elif (nameAnswerTag in message):
            message = message.replace(sep, "")
            message = message.replace(nameAnswerTag, "")
            print(address[0] + " ist " + message)
            f = codecs.open(folderPath+"/data/SessionIP.txt", "a", "utf-8")
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
        s.settimeout(0.1)

        ip = empfangToIp(empfang)
        EmpfangName = IpToName(ip)
        global folderPath
        f = codecs.open(folderPath+"/data/data.txt", "a", "utf-8")
        f.write('\n{"Sender": "' + EmpfangName + '", "Message": "' + message + '", "Art": "Send"}')
        f.close()
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
    serverT = threading.Thread(target=server)
    serverT.start()

def timeController():
    global timestamp1
    time.sleep(5)
    while True:
        now = datetime.now()
        a_timedelta = now - timestamp1
        seconds = a_timedelta.total_seconds()
        if (seconds > 10):
            print(str(now) + "||| last: "+ str(timestamp1) + "||| sec: " + str(seconds))
            exitDelay();
        time.sleep(5)

def sayIP9898():
    for x in range(2, 255):
        try:
            ip = local_ip
            ip = ip.split(".")
            empfang1 = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(x)
            if (empfang1 != local_ip):
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
            message = logoutTag + sep + nameuse

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
        s = socket.socket()
        s.connect((ip, 9898))
        s.send(bytes(exitTag + sep + name + end, 'UTF-8'))
        s.close()
    except:
        x = "a"

def clearEmpfang():
    f = codecs.open(folderPath+"/data/data.txt", "w", "utf-8")
    f.write('')
    f.close()

def exitDelay():
    logoutT = threading.Thread(target=logoutIP9898)
    logoutT.start()
    logoutT.join()
    # time.sleep(1)
    os.system("taskkill /F /IM python" + platform.python_version().split(".")[0] + "." + platform.python_version().split(".")[1] + ".exe")

def empfangToIp(empfang):
    global ort
    f = codecs.open(folderPath+"/data/SessionIP.txt", "r", "utf-8")
    content = f.read()
    f.close()
    content = content.replace("\r", "")
    if (len(content) < 5):
        return empfang
    contentArray = content.split("\n")
    for i in reversed(contentArray):
        if (len(i)> 5):
            jsonObject = json.loads(i)
            if(jsonObject["Name"].lower() == empfang.lower()):
                return jsonObject["Ip"]
    if (StaticipListExists):
        global ort
        f = codecs.open(folderPath+"/data/StaticIP.txt", "r", "utf-8")
        content = f.read()
        f.close()
        content = content.replace("\r", "")
        if (len(content) < 5):
            return empfang
        contentArray = content.split("\n")
        for i in reversed(contentArray):
            if (len(i)> 5):
                jsonObject = json.loads(i)
                if (jsonObject["Ort"].lower() == ort.lower()):
                    if(jsonObject["Name"].lower() == empfang.lower()):
                        return jsonObject["Ip"]
    return empfang

def IpToName(ip):
    global ort
    f = codecs.open(folderPath+"/data/SessionIP.txt", "r", "utf-8")
    content = f.read()
    f.close()
    content = content.replace("\r", "")
    if (len(content) < 5):
        return empfang
    contentArray = content.split("\n")
    for i in reversed(contentArray):
        if (len(i)> 5):
            jsonObject = json.loads(i)
            if(jsonObject["Ip"].lower() == ip.lower()):
                return jsonObject["Name"]
    if (StaticipListExists):
        global ort
        f = codecs.open(folderPath+"/data/StaticIP.txt", "r", "utf-8")
        content = f.read()
        f.close()
        content = content.replace("\r", "")
        if (len(content) < 5):
            return empfang
        contentArray = content.split("\n")
        for i in reversed(contentArray):
            if (len(i)> 5):
                jsonObject = json.loads(i)
                if (jsonObject["Ort"].lower() == ort.lower()):
                    if(jsonObject["Ip"].lower() == ip.lower()):
                        return jsonObject["Name"]
    return empfang

def eingabeUeberpruefung(eingabe):
    unerlaubtArray = ['"', "\\", sep, end, nameAnswerTag, nameTag, messageTag, exitTag, logoutTag]
    for i in unerlaubtArray:
        if i in eingabe:
            return False
    return True


local_ip = getIP()
a = threading.Thread(target=execCollector)
a.start()
b = threading.Thread(target=timeController)
b.start()

app = Flask(__name__)
app.secret_key = b'kdue#-_1iefm_.,.3|a654adf'




@app.route("/",methods=['GET', 'POST'])
def index():
    global name
    global ort
    local_ip = getIP()
    if(eingabeUeberpruefung(session["ort"]) and eingabeUeberpruefung(session["name"])):
        if ('local_ip' in session):
            if (session['local_ip'] == local_ip):
                if ("name" in session):
                    if ("ort" in session):
                        ort = session['ort'].lower()
                        name = session['name'].lower()
                        try:
                            s = socket.socket()
                            # s.settimeout(0.1)
                            s.connect((local_ip, 9898))
                            s.send(bytes(nameTag + sep + name + end, 'UTF-8'))
                            s.close()
                            del s
                        except:
                            x = "a"
                        return redirect(url_for('send'))
        session['local_ip'] = local_ip.lower()
        if ('name' in session):
            name = session["name"]
            if ("ort" in session):
                ort = session['ort'].lower()
            else:
                ort = request.form.get("ort", "").lower()
                session["ort"] = ort
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
        if (request.form.get("name", "") != "" and request.form.get("ort", "") != ""):
            ort = request.form.get("ort", "").lower()
            session['ort'] = ort
            name = request.form.get("name", "").lower()
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
    f = codecs.open( folderPath+"/templates/login.html", "r", "utf-8")
    indexContent = f.read()
    indexContent = indexContent.replace("{title}", "Cleo-Messenger")
    indexContent = indexContent.replace("{localIP}", local_ip)

    data = ["Cleo-Messenger", session["local_ip"]]
    return render_template("login.html", data=data)

@app.route('/chat')
def chat():
    global timestamp1
    timestamp1 = datetime.now()
    CurrentPerson = request.args.get('person').lower()
    session["CurrentPerson"] = CurrentPerson
    nachrichtenList = []
    if ("ort" in session):
        f = codecs.open(folderPath+"/data/data.txt", "r", "utf-8")
        content = f.read()
        f.close()
        content = content.replace("\r", "")
        contentArray = content.split("\n")
        for i in contentArray:
            if (len(i) > 5):
                jsonObject = json.loads(i)
                if (jsonObject["Sender"] == CurrentPerson):
                    nachrichtenList.append((jsonObject["Sender"].capitalize(), jsonObject["Message"], jsonObject["Art"]))
    global name
    nachrichten = []
    for i in nachrichtenList:
        if(i[2] == "Send"):
            j = list(i)
            j[0] = name.capitalize()
            i = tuple(j)
        nachrichten.append(i)
    return render_template('chat.html', nachrichten=nachrichten)

@app.route("/chats",methods=['GET', 'POST'])
def chats():
    personenList = []
    if ("ort" in session):
        f = codecs.open(folderPath+"/data/data.txt", "r", "utf-8")
        content = f.read()
        f.close()
        content = content.replace("\r", "")
        contentArray = content.split("\n")
        for i in reversed(contentArray):
            if (len(i) > 5):
                jsonObject = json.loads(i)
                if (jsonObject["Sender"].capitalize() in personenList):
                    x = "a"
                else:
                    personenList.append(jsonObject["Sender"].capitalize())
    data = ["Cleo-Messenger", len(personenList)]
    personen = personenList
    if ("CurrentPerson" in session):
        currentPerson = session["CurrentPerson"]
    else:
        if (len(personen) > 0):
            currentPerson = personen[0]
        else:
            currentPerson = session["name"]
        session["CurrentPerson"] = currentPerson
    return render_template('chats.html', personen=personen, data=data, currentPerson=currentPerson)

@app.route("/addressBook",methods=['GET', 'POST'])
def addressBook():
    reverseContentstatic = []
    if ("ort" in session):
        f = codecs.open(folderPath+"/data/StaticIP.txt", "r", "utf-8")
        content = f.read()
        f.close()
        content = content.replace("\r", "")
        contentArray = content.split("\n")
        for i in reversed(contentArray):
            if (len(i) > 5):
                jsonObject = json.loads(i)
                if (jsonObject["Ort"] == session["ort"].lower()):
                    reverseContentstatic.append(jsonObject["Name"] + " --> " + jsonObject["Ip"])


    reverseContentSession = []
    f = codecs.open(folderPath+"/data/SessionIP.txt", "r", "utf-8")
    content = f.read()
    f.close()
    content = content.replace("\r", "")
    contentArray = content.split("\n")
    for i in reversed(contentArray):
        if (len(i) > 5):
            jsonObject = json.loads(i)
            if((jsonObject["Name"] + " --> " + jsonObject["Ip"]) in reverseContentstatic):
                x = "a"
            else:
                reverseContentSession.append(jsonObject["Name"] + " --> " + jsonObject["Ip"])
    textsSession = reverseContentSession
    textsStatic = reverseContentstatic
    data = ["Cleo-Messenger", session["local_ip"],len(textsStatic),len(textsSession)]

    return render_template('addressBook.html', textsSession=textsSession, textsStatic=textsStatic, data=data)

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
    data = ["Cleo-Messenger", session["local_ip"]]
    if (request.form.get("ort", "") != "" and request.form.get("name", "") != "" and request.form.get("ip", "") != ""):
        f = codecs.open(folderPath+"/data/StaticIP.txt", "r", "utf-8")
        content = f.read()
        f.close()
        content = content.replace("\r", "")
        if (len(content) < 5):
            return render_template("staticIP.html", data=data)
        contentArray = content.split("\n")
        for i in reversed(contentArray):
            if (len(i)> 5):
                jsonObject = json.loads(i)
                if(request.form.get("ort").lower() == jsonObject["Ort"].lower()):
                    if(request.form.get("name").lower() == jsonObject["Name"].lower()):
                        return render_template("staticIP.html", data=data)
                    if(request.form.get("ip").lower() == jsonObject["Ip"].lower()):
                        return render_template("staticIP.html", data=data)
        ort = request.form.get("ort", "").lower()
        name = request.form.get("name", "").lower()
        ip = request.form.get("ip", "").lower()
        f = codecs.open(folderPath+"/data/StaticIP.txt", "a", "utf-8")
        f.write('\n{"Ort": "' + ort.lower() + '", "Name": "' + name.lower() + '", "Ip": "' + ip + '"}')
        f.close()
        return redirect(url_for('send'))
    else:
        return render_template("staticIP.html", data=data)

@app.route("/send", methods=['GET', 'POST'])
def send():
    if (request.form.get("Type") == "Send"):
        global oldUpdate
        lastUpdate = request.form.get("lastUpdate", "").lower()
        if(oldUpdate != lastUpdate):
            oldUpdate = lastUpdate
            empfang = request.form.get("empfang", "").lower()
            nachricht = request.form.get("nachricht", "")
            if(empfang and nachricht):
                print(empfang + " | bekommt | " + nachricht)
                sendMessage(nachricht, empfang, session['name'])

        data = ["Cleo-Messenger", session["local_ip"],session["name"].capitalize()]
        if ("ort" in session):
            if (session["ort"] != ""):
                data.append(session["ort"])
        return render_template("send.html", data=data)

    if (request.form.get("Type") == "Chats"):
        nachricht = request.form.get("nachricht", "")
        empfang = session["CurrentPerson"]
        sendMessage(nachricht, empfang, session['name'])
        return redirect(url_for('chats'))

    data = ["Cleo-Messenger", session["local_ip"],session["name"].capitalize()]
    if ("ort" in session):
        if (session["ort"] != ""):
            data.append(session["ort"].capitalize())
    return render_template("send.html", data=data)

@app.route('/empfang')
def empfang():
    if(request.args.get('clear') == "true"):
        clearEmpfang();
    global timestamp1
    timestamp1 = datetime.now()
    empfangs_list = []
    f = codecs.open(folderPath+"/data/data.txt", "r", "utf-8")
    content = f.read()
    f.close()
    content = content.replace("\r", "")
    if (len(content) < 5):
        return render_template('empty.html')
    contentArray = content.split("\n")
    reverseContent = []
    for i in reversed(contentArray):
        if (len(i) > 5):
            jsonObject = json.loads(i)
            if ("Message" in jsonObject and jsonObject["Art"] == "Empfang"):
                reverseContent.append(jsonObject["Sender"].capitalize() + ": " + jsonObject["Message"])
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
    app.env = "development"
    app.run(host="localhost", port=9897, debug=False)

# except KeyboardInterrupt:

input("Terminate")


os.system("taskkill /F /IM python" + platform.python_version().split(".")[0] + "." + platform.python_version().split(".")[1] + ".exe")
