import os
import socket
import sys
import threading
import time

NameToIP = []

def get_ip_address(empfang):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((empfang, 80))
    return s.getsockname()[0]





def NameListener():
    global NameToIP

    end = "#END#"
    sep = "#SEP#"
    nameAnswerTag = "#NAMEANSWER#"
    exitTag = "#EXIT#"
    nameTag = "#NAME#"
    messageTag = "#MES#"
    buffer = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]

    NameListenerloop = True
    del s

    # try:
    while NameListenerloop:
        sserver = socket.socket()
        sserver.bind((local_ip, 9899))
        sserver.listen()
        client_socket, address = sserver.accept()

        message = ""
        while NameListenerloop:
            text = client_socket.recv(buffer).decode()
            message += text
            if end in text:
                break
        message = message.replace(end, "")
        if (nameTag in message):
            message = message.replace(sep, "")
            message = message.replace(nameTag, "")
            NameToIP.append([address[0], message])
        if (nameAnswerTag in message):
            message = message.replace(sep, "")
            message = message.replace(nameAnswerTag, "")
            NameToIP.append([address[0], message])
        if (logoutTag in message):
            message = message.replace(sep, "")
            message = message.replace(logoutTag, "")
            NameToIP.remove([address[0], message])
        if (exitTag in message):
            if (address[0] == local_ip):
                # exit()
                print("Beenden")
                NameListenerloop = False


        del sserver
        del client_socket
        del address
    # except:
    #     print("")
    #     print("Ende")




s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]

del s
altEmpfang = local_ip
print("Eigene IP: " + local_ip)
name = input("Name: ")
print("")

sep = "#SEP#"
end = "#END#"
nameAnswerTag = "#NAMEANSWER#"
exitTag = "#EXIT#"
nameTag = "#NAME#"
messageTag = "#MES#"
logoutTag = "#LOGOUT#"
port = 9898
buffer = 1024
notende = True

def logoutIP9899():
    for x in range(2, 255):
        try:
            ip = local_ip
            ip = ip.split(".")
            empfang1 = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(x)
            host = get_ip_address(empfang1)
            s = socket.socket()
            s.settimeout(0.01)
            s.connect((empfang1, 9899))
            s.send(bytes(logoutTag + sep + name + end, 'UTF-8'))
            s.close()
        except:
            x = "a"

def logoutIP9898():
    for x in range(2, 255):
        try:
            ip = local_ip
            ip = ip.split(".")
            empfang1 = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(x)
            host = get_ip_address(empfang1)
            s = socket.socket()
            s.settimeout(0.01)
            s.connect((empfang1, 9898))
            s.send(bytes(logoutTag + sep + name + end, 'UTF-8'))
            s.close()
        except:
            x = "a"

def exit9899():
    try:
        ip = local_ip
        host = get_ip_address(ip)
        s = socket.socket()
        s.settimeout(0.01)
        s.connect((host, 9899))
        s.send(bytes(exitTag + sep + name + end, 'UTF-8'))
        s.close()
    except:
        x = "a"

def exit9898():
    try:
        ip = local_ip
        host = get_ip_address(ip)
        s = socket.socket()
        s.settimeout(0.01)
        s.connect((host, 9898))
        s.send(bytes(exitTag + sep + name + end, 'UTF-8'))
        s.close()
    except:
        x = "a"

def sayIP9898():
    try:
        host = get_ip_address(local_ip)
        s = socket.socket()
        # s.settimeout(0.001)
        s.connect((host, 9898))
        s.send(bytes(nameTag + sep + name + end, 'UTF-8'))
        s.close()
    except:
        x = "a"



x = threading.Thread(target=sayIP9898)
x.start()
y = threading.Thread(target=NameListener)
y.start()


# try:
while notende:

    empfang = input("Empfänger: ")
    if empfang == "":
        empfang = altEmpfang
        var = input("Nachricht: ")
        if (var == "ende"):
            Threadlogout9898 = threading.Thread(target=logoutIP9898)
            Threadlogout9899 = threading.Thread(target=logoutIP9899)
            Threadexit9898 = threading.Thread(target=exit9898)
            Threadexit9899 = threading.Thread(target=exit9899)

            Threadlogout9899.start()
            Threadlogout9898.start()
            Threadexit9899.start()
            Threadexit9898.start()

            Threadlogout9899.join()
            Threadlogout9898.join()
            Threadexit9899.join()
            Threadexit9898.join()
            exit()
            # logoutIP9899()
            # logoutIP9898()
            # exit9898()
            # a = threading.Thread(target=exit9899)
            # a.start()
            # notende = False
            # break
    elif empfang == "ende":
        Threadlogout9898 = threading.Thread(target=logoutIP9898)
        Threadlogout9899 = threading.Thread(target=logoutIP9899)
        Threadexit9898 = threading.Thread(target=exit9898)
        Threadexit9899 = threading.Thread(target=exit9899)

        Threadlogout9899.start()
        Threadlogout9898.start()
        Threadexit9899.start()
        Threadexit9898.start()

        Threadlogout9899.join()
        Threadlogout9898.join()
        Threadexit9899.join()
        Threadexit9898.join()
        exit()

        notende = False
        break
    else:
        empfang = empfang
        for x in NameToIP:
            if (x[1] == empfang):
                empfang = x[0]
        altEmpfang = empfang
        var = input("Nachricht: ")
        if (var == "ende"):
            logoutIP9899()
            logoutIP9898()
            exit9898()
            a = threading.Thread(target=exit9899)
            a.start()
            notende = False
            break

    if var != "":
        # host = get_ip_address(empfang)
        host = empfang
        notSkip = True
        if end in var:
            print("Die Nachricht darf nicht #END# enthalten")
            notSkip = False
        if sep in var:
            print("Die Nachricht darf nicht #SEP# enthalten")
            notSkip = False
        if logoutTag in var:
            print("Die Nachricht darf nicht #LOGOUT# enthalten")
            notSkip = False
        if exitTag in var:
            print("Die Nachricht darf nicht #EXIT# enthalten")
            notSkip = False
        if nameTag in var:
            print("Die Nachricht darf nicht #NAME# enthalten")
            notSkip = False
        if nameAnswerTag in var:
            print("Die Nachricht darf nicht #NAMEANSWER# enthalten")
            notSkip = False
        if messageTag in var:
            print("Die Nachricht darf nicht #MES# enthalten")
            notSkip = False
        if(notSkip):
            s = socket.socket()
            s.connect((host, port))
            s.send(bytes(messageTag, 'UTF-8'))
            s.send(bytes(name, 'UTF-8'))

            s.send(bytes(sep, 'UTF-8'))

            while True:
                var_bytes = var[:buffer]
                var = var[buffer:]
                if var_bytes == "":
                    s.sendall(bytes(end, 'UTF-8'))
                    break
                s.sendall(bytes(var_bytes, 'UTF-8'))
            s.close()
            print("")
    else:
        print("Eine Nachricht wird benötigt")
# except:
#     print("Ende")