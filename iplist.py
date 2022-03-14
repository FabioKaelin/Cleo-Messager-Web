import socket
import datetime
from datetime import date
from datetime import *
import os


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

f = open(os.path.dirname(os.path.abspath(__file__)) + "/iplist.txt", "r")
content = f.read()
f.close()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today = date.today()
ort = input("Ort: ")

f = open(os.path.dirname(os.path.abspath(__file__)) + "/iplist.txt", "w")
f.write(content + "\n" + getIP() + " ||| " + str(current_time) + " " + str(today) + " ||| " + ort)
f.close()
