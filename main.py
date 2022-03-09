from email.policy import default
import random
from flask import Flask, jsonify, redirect, render_template, session, url_for
from flask import request
from flask import *
# from turbo_flask import Turbo
import os
import socket
import sys
import threading
import time
import codecs
import sqlite3
import threading

from pkg_resources import Environment

# ...


# import logging
# logging.basicConfig(level=logging.DEBUG)


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


app = Flask(__name__)
app.config['ENVIRONMENT'] = "development"
app.secret_key = b'kdue#-_1adf'
# turbo = Turbo(app)


# def update_load():
#     with app.app_context():
#         while True:
#             time.sleep(2)
#             turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))

# @app.before_first_request
# def before_first_request():
#     threading.Thread(target=update_load).start()


messages = [("Fabio", "hallo du"),("Chris", "ich mag python")]


@app.route("/")
def index():
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(("8.8.8.8", 80))
    # local_ip = s.getsockname()[0]
    local_ip = request.remote_addr
    session['local_ip'] = local_ip
    # s.close()
    # del s
    if ('name' in session):
        return redirect(url_for('send'))
    f = codecs.open("./templates/login.html", "r", "utf-8")
    indexContent = f.read()
    indexContent = indexContent.replace("{title}", "Cleo-Messager")
    indexContent = indexContent.replace("{localIP}", local_ip)
    return indexContent

@app.route("/send", methods=['GET', 'POST'])
def send():
    global oldUpdate
    if ('name' not in session):
        name = request.args.get("name", "")
        session['name'] = name
    lastUpdate = request.form.get("lastUpdate", "")
    if(oldUpdate != lastUpdate):
        oldUpdate = lastUpdate
        empfang = request.form.get("empfang", "")
        nachricht = request.form.get("nachricht", "")
        print(lastUpdate)
        if(empfang and nachricht):
            # empfang = session["empfang"]
            # nachricht = session["nachricht"]
            print(empfang + " | bekommt | " + nachricht)
            print("Es wird eine Nachricht gesendet")
            sendMessage(nachricht, empfang, session['name'])



    # session['data'] = request.json
    # data = session.get('data')
    # print(data)
    # if('empfang' in session):

    f = codecs.open("./templates/send.html", "r", "utf-8")
    indexContent = f.read()
    indexContent = indexContent.replace("{title}", "Cleo-Messager")
    indexContent = indexContent.replace("{localIP}", session["local_ip"])
    # indexContent = indexContent.replace("{oldEmpfang}", empfang)
    indexContent = indexContent.replace("{name}", session['name'])
    # indexContent = indexContent.replace("{name}", name)
    return indexContent




@app.route("/empfang")
def empfang():
    global messages
    # if ('name' not in session):
    #     name = request.args.get("name", "")
    #     session['name'] = name

    if ('messages' not in session):
        session['messages'] = messages
    if ('messages' in session):
        # empfang = request.args.get("empfang", "")
        # nachricht = request.args.get("nachricht", "")
        text = ""

        for message in reversed(session["messages"]):
            text += "<b>" + message[0]+ "</b>: " + message[1] + "<br>"



        f = codecs.open("./templates/empfang.html", "r", "utf-8")
        indexContent = f.read()
        indexContent = indexContent.replace("{title}", "Cleo-Messager")
        indexContent = indexContent.replace("{localIP}", session['local_ip'])
        # indexContent = indexContent.replace("{name}", session['name'])
        indexContent = indexContent.replace("{empfangMessage}", text)
        # if nachricht!= "" and empfang != "":
        #     print("Es wird eine Nachricht gesendet")
        #     sendMessage(nachricht, empfang, name)
        return indexContent
    return "Keine Nachrichten"




@app.route('/test/', methods=['GET', 'POST']) # EDIT
def stat():
    token = request.args.get("token", "")
    # request.
    # print(request.args.getlist)
    # print(request.get_json()["token"])
    # print_r()
    print(token)
    a = 2
    b = 10
        # y = threading.Thread(target=NameListener)
        # y.start()
    text = f"{a} is not equal to {b}"
    return render_template("test.html", text=text, token="ölasdfjöaskldf")


# @app.context_processor
# def inject_load():
#     if sys.platform.startswith('linux'):
#         with open('/proc/loadavg', 'rt') as f:
#             load = f.read().split()[0:3]
#     else:
#         load = [int(random.random() * 100) / 100 for _ in range(3)]
#     return {'load1': load[0], 'load5': load[1], 'load15': load[2]}




def server():
    global messages
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    del s
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
        # print(message)
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
        if (messageTag in message):
            message = message.replace(messageTag, "")
            messagesplit = message.split(sep)
            client_socket.close()
            sserver.close()
            print(messagesplit[0] + ": " + messagesplit[1])
            messages.append((messagesplit[0], messagesplit[1]))
        del sserver
        del client_socket
        del address
    # except:
    #     print("")
    #     print("Ende")


# y = threading.Thread(target=server)
# y.start()

def sendMessage(message, empfang, name):
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






def fahrenheit_from(celsius):
    """Convert Celsius to Fahrenheit degrees."""
    try:
        fahrenheit = float(celsius) * 9 / 5 + 32
        fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
        return str(fahrenheit)
    except ValueError:
        return "invalid input"

if __name__ == "__main__":
    app.run(host="10.80.4.124", port=8080, debug=True)



































# import os
# import socket
# import sys
# import threading
# import time

# NameToIP = []

# def get_ip_address(empfang):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect((empfang, 80))
#     return s.getsockname()[0]





# def NameListener():
#     global NameToIP

#     end = "#END#"
#     sep = "#SEP#"
#     nameAnswerTag = "#NAMEANSWER#"
#     exitTag = "#EXIT#"
#     nameTag = "#NAME#"
#     messageTag = "#MES#"
#     buffer = 1024

#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     local_ip = s.getsockname()[0]

#     NameListenerloop = True
#     del s

#     # try:
#     while NameListenerloop:
#         sserver = socket.socket()
#         sserver.bind((local_ip, 9899))
#         sserver.listen()
#         client_socket, address = sserver.accept()

#         message = ""
#         while NameListenerloop:
#             text = client_socket.recv(buffer).decode()
#             message += text
#             if end in text:
#                 break
#         message = message.replace(end, "")
#         if (nameTag in message):
#             message = message.replace(sep, "")
#             message = message.replace(nameTag, "")
#             NameToIP.append([address[0], message])
#         if (nameAnswerTag in message):
#             message = message.replace(sep, "")
#             message = message.replace(nameAnswerTag, "")
#             NameToIP.append([address[0], message])
#         if (logoutTag in message):
#             message = message.replace(sep, "")
#             message = message.replace(logoutTag, "")
#             NameToIP.remove([address[0], message])
#         if (exitTag in message):
#             if (address[0] == local_ip):
#                 # exit()
#                 print("Beenden")
#                 NameListenerloop = False


#         del sserver
#         del client_socket
#         del address
#     # except:
#     #     print("")
#     #     print("Ende")




# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# s.connect(("8.8.8.8", 80))
# local_ip = s.getsockname()[0]

# del s
# altEmpfang = local_ip
# print("Eigene IP: " + local_ip)
# name = input("Name: ")
# print("")

# sep = "#SEP#"
# end = "#END#"
# nameAnswerTag = "#NAMEANSWER#"
# exitTag = "#EXIT#"
# nameTag = "#NAME#"
# messageTag = "#MES#"
# logoutTag = "#LOGOUT#"
# port = 9898
# buffer = 1024
# notende = True

# def logoutIP9899():
#     for x in range(2, 255):
#         try:
#             ip = local_ip
#             ip = ip.split(".")
#             empfang1 = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(x)
#             host = get_ip_address(empfang1)
#             s = socket.socket()
#             s.settimeout(0.01)
#             s.connect((empfang1, 9899))
#             s.send(bytes(logoutTag + sep + name + end, 'UTF-8'))
#             s.close()
#         except:
#             x = "a"

# def logoutIP9898():
#     for x in range(2, 255):
#         try:
#             ip = local_ip
#             ip = ip.split(".")
#             empfang1 = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(x)
#             host = get_ip_address(empfang1)
#             s = socket.socket()
#             s.settimeout(0.01)
#             s.connect((empfang1, 9898))
#             s.send(bytes(logoutTag + sep + name + end, 'UTF-8'))
#             s.close()
#         except:
#             x = "a"

# def exit9899():
#     try:
#         ip = local_ip
#         host = get_ip_address(ip)
#         s = socket.socket()
#         s.settimeout(0.01)
#         s.connect((host, 9899))
#         s.send(bytes(exitTag + sep + name + end, 'UTF-8'))
#         s.close()
#     except:
#         x = "a"

# def exit9898():
#     try:
#         ip = local_ip
#         host = get_ip_address(ip)
#         s = socket.socket()
#         s.settimeout(0.01)
#         s.connect((host, 9898))
#         s.send(bytes(exitTag + sep + name + end, 'UTF-8'))
#         s.close()
#     except:
#         x = "a"

# def sayIP9898():
#     try:
#         host = get_ip_address(local_ip)
#         s = socket.socket()
#         # s.settimeout(0.001)
#         s.connect((host, 9898))
#         s.send(bytes(nameTag + sep + name + end, 'UTF-8'))
#         s.close()
#     except:
#         x = "a"



# x = threading.Thread(target=sayIP9898)
# x.start()
# y = threading.Thread(target=NameListener)
# y.start()




# # try:
# while notende:
#     empfang = input("Empfänger: ")
#     if empfang == "":
#         empfang = altEmpfang
#         var = input("Nachricht: ")
#         if (var == "ende"):
#             Threadlogout9898 = threading.Thread(target=logoutIP9898)
#             Threadlogout9899 = threading.Thread(target=logoutIP9899)
#             Threadexit9898 = threading.Thread(target=exit9898)
#             Threadexit9899 = threading.Thread(target=exit9899)

#             Threadlogout9899.start()
#             Threadlogout9898.start()
#             Threadexit9899.start()
#             Threadexit9898.start()

#             Threadlogout9899.join()
#             Threadlogout9898.join()
#             Threadexit9899.join()
#             Threadexit9898.join()
#             exit()
#             # logoutIP9899()
#             # logoutIP9898()
#             # exit9898()
#             # a = threading.Thread(target=exit9899)
#             # a.start()
#             # notende = False
#             # break
#     elif empfang == "ende":
#         Threadlogout9898 = threading.Thread(target=logoutIP9898)
#         Threadlogout9899 = threading.Thread(target=logoutIP9899)
#         Threadexit9898 = threading.Thread(target=exit9898)
#         Threadexit9899 = threading.Thread(target=exit9899)

#         Threadlogout9899.start()
#         Threadlogout9898.start()
#         Threadexit9899.start()
#         Threadexit9898.start()

#         Threadlogout9899.join()
#         Threadlogout9898.join()
#         Threadexit9899.join()
#         Threadexit9898.join()
#         exit()

#         notende = False
#         break
#     else:
#         empfang = empfang
#         for x in NameToIP:
#             if (x[1] == empfang):
#                 empfang = x[0]
#         altEmpfang = empfang
#         var = input("Nachricht: ")
#         if (var == "ende"):
#             logoutIP9899()
#             logoutIP9898()
#             exit9898()
#             a = threading.Thread(target=exit9899)
#             a.start()
#             notende = False
#             break

#     if var != "":
#         # host = get_ip_address(empfang)
#         host = empfang
#         notSkip = True
#         if end in var:
#             print("Die Nachricht darf nicht #END# enthalten")
#             notSkip = False
#         if sep in var:
#             print("Die Nachricht darf nicht #SEP# enthalten")
#             notSkip = False
#         if logoutTag in var:
#             print("Die Nachricht darf nicht #LOGOUT# enthalten")
#             notSkip = False
#         if exitTag in var:
#             print("Die Nachricht darf nicht #EXIT# enthalten")
#             notSkip = False
#         if nameTag in var:
#             print("Die Nachricht darf nicht #NAME# enthalten")
#             notSkip = False
#         if nameAnswerTag in var:
#             print("Die Nachricht darf nicht #NAMEANSWER# enthalten")
#             notSkip = False
#         if messageTag in var:
#             print("Die Nachricht darf nicht #MES# enthalten")
#             notSkip = False
#         if(notSkip):
#             s = socket.socket()
#             s.connect((host, port))
#             s.send(bytes(messageTag, 'UTF-8'))
#             s.send(bytes(name, 'UTF-8'))

#             s.send(bytes(sep, 'UTF-8'))

#             while True:
#                 var_bytes = var[:buffer]
#                 var = var[buffer:]
#                 if var_bytes == "":
#                     s.sendall(bytes(end, 'UTF-8'))
#                     break
#                 s.sendall(bytes(var_bytes, 'UTF-8'))
#             s.close()
#             print("")
#     else:
#         print("Eine Nachricht wird benötigt")
# # except:
# #     print("Ende")







# import os
# import socket
# import sys
# import threading
# import time

# NameToIP = []

# def get_ip_address(empfang):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect((empfang, 80))
#     return s.getsockname()[0]





# def NameListener():
#     global NameToIP

#     end = "#END#"
#     sep = "#SEP#"
#     nameAnswerTag = "#NAMEANSWER#"
#     exitTag = "#EXIT#"
#     nameTag = "#NAME#"
#     messageTag = "#MES#"
#     buffer = 1024

#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     local_ip = s.getsockname()[0]

#     NameListenerloop = True
#     del s

#     # try:
#     while NameListenerloop:
#         sserver = socket.socket()
#         sserver.bind((local_ip, 9899))
#         sserver.listen()
#         client_socket, address = sserver.accept()

#         message = ""
#         while NameListenerloop:
#             text = client_socket.recv(buffer).decode()
#             message += text
#             if end in text:
#                 break
#         message = message.replace(end, "")
#         if (nameTag in message):
#             message = message.replace(sep, "")
#             message = message.replace(nameTag, "")
#             NameToIP.append([address[0], message])
#         if (nameAnswerTag in message):
#             message = message.replace(sep, "")
#             message = message.replace(nameAnswerTag, "")
#             NameToIP.append([address[0], message])
#         if (logoutTag in message):
#             message = message.replace(sep, "")
#             message = message.replace(logoutTag, "")
#             NameToIP.remove([address[0], message])
#         if (exitTag in message):
#             if (address[0] == local_ip):
#                 # exit()
#                 print("Beenden")
#                 NameListenerloop = False


#         del sserver
#         del client_socket
#         del address
#     # except:
#     #     print("")
#     #     print("Ende")




# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# s.connect(("8.8.8.8", 80))
# local_ip = s.getsockname()[0]

# del s
# altEmpfang = local_ip
# print("Eigene IP: " + local_ip)
# name = input("Name: ")
# print("")

# sep = "#SEP#"
# end = "#END#"
# nameAnswerTag = "#NAMEANSWER#"
# exitTag = "#EXIT#"
# nameTag = "#NAME#"
# messageTag = "#MES#"
# logoutTag = "#LOGOUT#"
# port = 9898
# buffer = 1024
# notende = True

# def logoutIP9899():
#     for x in range(2, 255):
#         try:
#             ip = local_ip
#             ip = ip.split(".")
#             empfang1 = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(x)
#             host = get_ip_address(empfang1)
#             s = socket.socket()
#             s.settimeout(0.01)
#             s.connect((empfang1, 9899))
#             s.send(bytes(logoutTag + sep + name + end, 'UTF-8'))
#             s.close()
#         except:
#             x = "a"

# def logoutIP9898():
#     for x in range(2, 255):
#         try:
#             ip = local_ip
#             ip = ip.split(".")
#             empfang1 = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(x)
#             host = get_ip_address(empfang1)
#             s = socket.socket()
#             s.settimeout(0.01)
#             s.connect((empfang1, 9898))
#             s.send(bytes(logoutTag + sep + name + end, 'UTF-8'))
#             s.close()
#         except:
#             x = "a"

# def exit9899():
#     try:
#         ip = local_ip
#         host = get_ip_address(ip)
#         s = socket.socket()
#         s.settimeout(0.01)
#         s.connect((host, 9899))
#         s.send(bytes(exitTag + sep + name + end, 'UTF-8'))
#         s.close()
#     except:
#         x = "a"

# def exit9898():
#     try:
#         ip = local_ip
#         host = get_ip_address(ip)
#         s = socket.socket()
#         s.settimeout(0.01)
#         s.connect((host, 9898))
#         s.send(bytes(exitTag + sep + name + end, 'UTF-8'))
#         s.close()
#     except:
#         x = "a"

# def sayIP9898():
#     try:
#         host = get_ip_address(local_ip)
#         s = socket.socket()
#         # s.settimeout(0.001)
#         s.connect((host, 9898))
#         s.send(bytes(nameTag + sep + name + end, 'UTF-8'))
#         s.close()
#     except:
#         x = "a"



# x = threading.Thread(target=sayIP9898)
# x.start()
# y = threading.Thread(target=NameListener)
# y.start()




# # try:
# while notende:
#     empfang = input("Empfänger: ")
#     if empfang == "":
#         empfang = altEmpfang
#         var = input("Nachricht: ")
#         if (var == "ende"):
#             Threadlogout9898 = threading.Thread(target=logoutIP9898)
#             Threadlogout9899 = threading.Thread(target=logoutIP9899)
#             Threadexit9898 = threading.Thread(target=exit9898)
#             Threadexit9899 = threading.Thread(target=exit9899)

#             Threadlogout9899.start()
#             Threadlogout9898.start()
#             Threadexit9899.start()
#             Threadexit9898.start()

#             Threadlogout9899.join()
#             Threadlogout9898.join()
#             Threadexit9899.join()
#             Threadexit9898.join()
#             exit()
#             # logoutIP9899()
#             # logoutIP9898()
#             # exit9898()
#             # a = threading.Thread(target=exit9899)
#             # a.start()
#             # notende = False
#             # break
#     elif empfang == "ende":
#         Threadlogout9898 = threading.Thread(target=logoutIP9898)
#         Threadlogout9899 = threading.Thread(target=logoutIP9899)
#         Threadexit9898 = threading.Thread(target=exit9898)
#         Threadexit9899 = threading.Thread(target=exit9899)

#         Threadlogout9899.start()
#         Threadlogout9898.start()
#         Threadexit9899.start()
#         Threadexit9898.start()

#         Threadlogout9899.join()
#         Threadlogout9898.join()
#         Threadexit9899.join()
#         Threadexit9898.join()
#         exit()

#         notende = False
#         break
#     else:
#         empfang = empfang
#         for x in NameToIP:
#             if (x[1] == empfang):
#                 empfang = x[0]
#         altEmpfang = empfang
#         var = input("Nachricht: ")
#         if (var == "ende"):
#             logoutIP9899()
#             logoutIP9898()
#             exit9898()
#             a = threading.Thread(target=exit9899)
#             a.start()
#             notende = False
#             break

#     if var != "":
#         # host = get_ip_address(empfang)
#         host = empfang
#         notSkip = True
#         if end in var:
#             print("Die Nachricht darf nicht #END# enthalten")
#             notSkip = False
#         if sep in var:
#             print("Die Nachricht darf nicht #SEP# enthalten")
#             notSkip = False
#         if logoutTag in var:
#             print("Die Nachricht darf nicht #LOGOUT# enthalten")
#             notSkip = False
#         if exitTag in var:
#             print("Die Nachricht darf nicht #EXIT# enthalten")
#             notSkip = False
#         if nameTag in var:
#             print("Die Nachricht darf nicht #NAME# enthalten")
#             notSkip = False
#         if nameAnswerTag in var:
#             print("Die Nachricht darf nicht #NAMEANSWER# enthalten")
#             notSkip = False
#         if messageTag in var:
#             print("Die Nachricht darf nicht #MES# enthalten")
#             notSkip = False
#         if(notSkip):
#             s = socket.socket()
#             s.connect((host, port))
#             s.send(bytes(messageTag, 'UTF-8'))
#             s.send(bytes(name, 'UTF-8'))

#             s.send(bytes(sep, 'UTF-8'))

#             while True:
#                 var_bytes = var[:buffer]
#                 var = var[buffer:]
#                 if var_bytes == "":
#                     s.sendall(bytes(end, 'UTF-8'))
#                     break
#                 s.sendall(bytes(var_bytes, 'UTF-8'))
#             s.close()
#             print("")
#     else:
#         print("Eine Nachricht wird benötigt")
# # except:
# #     print("Ende")

