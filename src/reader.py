import os
import json 
import datetime
from classMessage import Message
from classMember import Member 

#Takes a timestamp from the JSON file and converts it into a datetime date object
def convertTimestampToDate(timestamp):
    timestamp = timestamp.split(" ")[0]
    timestamp = timestamp.split("-")
    return datetime.date(year = int(timestamp[0]), month = int(timestamp[1]), day = int(timestamp[2]))

#Takes a timestamp from the JSON file and converts it into a datetime time object
def convertTimestampToTime(timestamp):
    timestamp = timestamp.split(" ")[1]
    timestamp = timestamp.split(":")
    return datetime.time(hour = int(timestamp[0]), minute = int(timestamp[1]), second = int(timestamp[2]))

#Converts the JSON object into an array of Message objects
def convertJsonToMessage(messageJson, fileName):
    messageArray = []
    for messages in messageJson:
        date = convertTimestampToDate(messages["Timestamp"])
        time = convertTimestampToTime(messages["Timestamp"])
        contents = messages["Contents"]
        messageArray.append(Message(date, time, contents, fileName))
    return messageArray

#Returns the earliest and latest date messages were sent in the channel
#needs to be changed to get the latest start and earliest end
def getStartAndEndDate(messageArray):
    startDate = datetime.date(year = 3000, month = 1, day = 1)
    endDate = datetime.date(year = 1, month = 1, day = 1)
    for messages in messageArray:
        if startDate > messages[-1].date:
            startDate = messages[-1].date
        if endDate < messages[0].date:
            endDate = messages[0].date
    return startDate, endDate

#Creates the dictionary messagesByDay as such: {<date> : [[<list of messages from user1>], [<list of messages from user2>], ...]}
def getMessagesByDay(messageArray, startDate, endDate):
    messagesByDay = {}
    tempDate = startDate
    delta = datetime.timedelta(days=1)

    #Initialise messagesByDay keys
    while tempDate <= endDate:
        messagesByDay[tempDate] = [[] for i in range(len(messageArray))]
        tempDate += delta
    for memberNo in range(len(messageArray)):
        for msg in messageArray[memberNo]:
            messagesByDay[msg.date][memberNo].append(msg)
    return messagesByDay

#Sets up the basic array of Message objects and Member objects
def setUpMessagesArray():
    messageFiles = os.listdir("data")
    messageArray = []
    colourArray = ["#12A3D7FF", "indianred", "green", "purple", "yellow"]
    memberArray = []
    #Load files into json objects
    for messageFileNo in range(len(messageFiles)):
        fileName = str(messageFiles[messageFileNo])
        newMember = Member(fileName.split(".")[0], colourArray[messageFileNo])
        memberArray.append(newMember)
        with open("data/" + fileName, "r", encoding="utf-8") as f:
            messageArray.append(convertJsonToMessage(json.load(f), newMember))
    return messageArray, memberArray
