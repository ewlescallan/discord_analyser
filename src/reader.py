import os
import json 
import datetime
from message import Message

#Takes a Timestamp from the JSON file and converts it into a datetime date object
def convertTimestampToDate(timestamp):
    timestamp = timestamp.split(" ")[0]
    timestamp = timestamp.split("-")
    return datetime.date(year = int(timestamp[0]), month = int(timestamp[1]), day = int(timestamp[2]))

#Takes a Timestamp from the JSON file and converts it into a datetime time object
def convertTimestampToTime(timestamp):
    timestamp = timestamp.split(" ")[1]
    timestamp = timestamp.split(":")
    return datetime.time(hour = int(timestamp[0]), minute = int(timestamp[1]), second = int(timestamp[2]))

#Converts the JSON object into an array of Message objects
def convertJsonToMessage(messageJson):
    messagesArray = []
    for messages in messageJson:
        date = convertTimestampToDate(messages["Timestamp"])
        time = convertTimestampToTime(messages["Timestamp"])
        contents = messages["Contents"]
        messagesArray.append(Message(date, time, contents))
    return messagesArray

messageFiles = os.listdir("data")
fileCount = len(messageFiles)
messages = []

#Load files into json objects
for messageFile in messageFiles:
    with open("data/" + str(messageFile), "r", encoding="utf-8") as f:
        messages.append(convertJsonToMessage(json.load(f)))

print(messages)

startDate = datetime.date(year = 3000, month = 1, day = 1)
endDate = datetime.date(year = 1, month = 1, day = 1)





def getStartAndEndDates(messageJsons):
    for messageJson in messageJsons:
        for messages in messageJson:
            print(messages["Timestamp"])
