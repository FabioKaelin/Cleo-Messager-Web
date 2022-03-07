import socket
import os
import threading
import time


end = "#END#"
sep = "#SEP#"
exitTag = "#EXIT#"
nameTag = "#NAME#"
nameAnswerTag = "#NAMEANSWER#"
messageTag = "#MES#"
logoutTag = "#LOGOUT#"
name = "unbekannt"

def get_ip_address(empfang):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((empfang, 80))
    return s.getsockname()[0]


def sayIP9898():
    for x in range(2, 255):
        try:
            ip = local_ip
            ip = ip.split(".")
            empfang1 = str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(x)
            if (empfang1 != local_ip):
                # print(empfang1)
                s = socket.socket()
                s.settimeout(0.03)
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



def answerName(empfang1, port):
        try:
            host = get_ip_address(empfang1)
            s = socket.socket()
            s.settimeout(0.01)
            s.connect((empfang1, port))
            s.send(bytes(nameAnswerTag + sep + name + end, 'UTF-8'))
            s.close()
        except:
            x = "a"



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
        elif (nameTag in message):
            message = message.replace(sep, "")
            message = message.replace(nameTag, "")
            if (address[0] == local_ip):
                global name
                name = message
                # print("Lokale IP")

                z = threading.Thread(target=sayIP9899)
                z.start()
                z2 = threading.Thread(target=sayIP9898)
                z2.start()
            else:
                # print("Andere IP")
                if(name != "unbekannt"):
                    # print("name ist nicht unbekannt")
                    y9899 = threading.Thread(target=answerName, args=(address[0],9899,))
                    y9899.start()
                    y9898 = threading.Thread(target=answerName, args=(address[0],9898,))
                    y9898.start()

            print(address[0] + " ist " + message)
        elif (nameAnswerTag in message):
            message = message.replace(sep, "")
            message = message.replace(nameAnswerTag, "")
            print(address[0] + " ist " + message)

        del sserver
        del client_socket
        del address
    # except:
    #     print("")
    #     print("Ende")


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
print("Eigene IP: " + local_ip)

del s

x = threading.Thread(target=server)
x.start()


# while True:
#     input("")
