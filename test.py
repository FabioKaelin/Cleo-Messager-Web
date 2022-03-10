import json
import codecs
import os
f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/sample_file.txt", "r", "utf-8")
content = f.read()
f.close()
content = content.replace("\r", "")
contentArray = content.split("\n")
reverseContent = []
for i in reversed(contentArray):
    print(i)
    jsonObject = json.loads(i)
    if ("Message" in jsonObject):
        reverseContent.append(jsonObject["Sender"] + ": " + jsonObject["Message"])
print(reverseContent)



message = "Hallo ich bin Fabio"
sender = "Fabio1234"
f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/sample_file.txt", "r", "utf-8")
content = f.read()
f.close()
f = codecs.open(os.path.dirname(os.path.abspath(__file__))+"/sample_file.txt", "w", "utf-8")
f.write(content+'\n{"Sender": "' + sender + '", "Message": "' + message + '"}')
# {"Sender": "Fabio4", "Message": "Hallo4 du"}
f.close()

