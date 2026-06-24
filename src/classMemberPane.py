import datetime as dt
import panel as pn
import math
import stop_words
import pandas as pd
from collections import Counter

class memberPaneClass: 
    def __init__(self, member, daySlider, messageArray, totalDays):
        self.member = member
        self.daySlider = daySlider
        self.startIndex = 0
        self.endIndex = len(messageArray) - 1
        self.totalDays = totalDays
        self.messageArray = messageArray[::-1]
        self.wordsToCount = [
            w.lower()
            for msg in self.messageArray
            for w in msg.contents.split()
            if w.lower() not in self.getDisallowedWords()
        ]
        self.totalMessages = len(messageArray)
        self.selectedMessages = len(messageArray)
        self.wordCounts = self.initMostCommonWords()
        self.averageMessagingTime = self.getAverageMessagingTime()
        self.HTMLPane = pn.pane.HTML(self.getHTML())
        self.wordTable = pn.widgets.DataFrame(
            pd.DataFrame(columns=["Word", "Count"]),
            disabled=True,
            height=250,
            sizing_mode="stretch_width"
        )
        self.pane = pn.Column(self.HTMLPane, self.wordTable, styles=dict(background=self.member.colour))
        self.setMostCommonWordsDf()
        
    
    def getMessagesFromStartOfTimeFrame(self):
        startDate = self.daySlider.value_start
        i = 0
        currentMessage = self.messageArray[0]
        while currentMessage.date < startDate:
            i += 1
            currentMessage = self.messageArray[i]
        currentMessage = self.messageArray[-1]
        return i
    
    def getMessagesFromEndOfTimeFrame(self):
        endDate = self.daySlider.value_end
        i = 0
        currentMessage = self.messageArray[-1]
        while currentMessage.date > endDate:
            i += 1
            currentMessage = self.messageArray[-1 * (i + 1)]
        return i


    def getMessagesInTimeFrame(self):
        self.selectedMessages = len(self.messageArray) - (self.getMessagesFromStartOfTimeFrame() + self.getMessagesFromEndOfTimeFrame())

    def getAverageMessagingTime(self):
        selectedMessageArray = self.messageArray[self.getMessagesFromStartOfTimeFrame() : self.totalMessages - (self.getMessagesFromEndOfTimeFrame() + 1)]
        if len(selectedMessageArray) > 0:
            times = [message.time for message in selectedMessageArray]
            angles = []
            for t in times:
                avg_seconds = (t.hour * 3600 + t.minute * 60 + t.second) / 86400
                angles.append(2 * math.pi * avg_seconds)
            x = sum(math.cos(a) for a in angles) / len(angles)
            y = sum(math.sin(a) for a in angles) / len(angles)
            mean_angle = math.atan2(y, x)
            while mean_angle < 0:
                mean_angle += 2 * math.pi
            avg_seconds = int(mean_angle * 86400 / (2 * math.pi))
            avg_time = dt.time(
                hour=int(avg_seconds // 3600),
                minute=int((avg_seconds % 3600) // 60),
                second=int(avg_seconds % 60)
            )
            return avg_time
        else:
            return 0

    def getDaysSelectedPercent(self):
        startDate, endDate = self.daySlider.value_start, self.daySlider.value_end
        daysSelected = (endDate - startDate).days
        return int((daysSelected / self.totalDays) * 100)
    
    def setMostCommonWordsDf(self):
        # print(self.wordCounts)
        df = pd.DataFrame(
            self.getSortedWordCounts(),
            columns=["Word", "Count"]
        ).sort_values("Count", ascending=False)

        new_table = pn.widgets.DataFrame(
            df,
            disabled=True,
            height=250,
            sizing_mode="stretch_width"
        )
        self.pane[1] = new_table
        self.wordTable = new_table

    def getDisallowedWords(self):
        disallowedWords = stop_words.get_stop_words("en")
        for word in ["i’m", "don’t", "it’s", "yea", "", "ur", "that’s", "you’re", "abt",
                      "didn’t", "tho", "i’ve", "smthng", "cos", "can’t", "yeah", "he’s", 
                      "i’ll", "what’s", "1", "2", "3", "4", "5", "kinda", "they’re", "bit",
                      "time", "day", "gunna", "lot"]:
            disallowedWords.append(word)
        return disallowedWords
    
    def initMostCommonWords(self):
        wordCounts = {}
        selectedWordsArray = self.wordsToCount#[self.getMessagesFromStartOfTimeFrame() : self.totalMessages - (self.getMessagesFromEndOfTimeFrame() + 1)]
        for word in selectedWordsArray:
            if word not in wordCounts: wordCounts[word] = 1
            else: wordCounts[word] += 1
        return wordCounts
    
    def updateWordCounts(self):
        startDate, endDate = self.daySlider.value_start, self.daySlider.value_end

        i = 0
        currentMessage = self.messageArray[0]
        while currentMessage.date < startDate:
            i += 1
            currentMessage = self.messageArray[i]

        j = 0
        currentMessage = self.messageArray[-1]
        while currentMessage.date > endDate:
            j += 1
            currentMessage = self.messageArray[-(j + 1)]
        
        newStart = i
        newEnd = len(self.messageArray) - j - 1
        while newStart > self.startIndex:
            self.remove_words(self.messageArray[self.startIndex])
            self.startIndex += 1

        while newStart < self.startIndex:
            self.startIndex -= 1
            self.add_words(self.messageArray[self.startIndex])

        while newEnd > self.endIndex:
            self.endIndex += 1
            self.add_words(self.messageArray[self.endIndex])

        while newEnd < self.endIndex:
            self.remove_words(self.messageArray[self.endIndex])
            self.endIndex -= 1

    def getSortedWordCounts(self):
        return list(sorted(self.wordCounts.items(), key=lambda item: item[1], reverse=True))[:20]
    
    def getHTML(self):
        return f"""
            <div style="color:Linen;">
                <div style="font-size:32px;font-weight:bold;">
                    {self.member.name}
                </div>

                <div style="font-size:16px;font-weight:bold;margin-top:10px;margin-bottom:5px;">
                    Messages Sent:
                </div>

                <div style="margin-bottom:2px;">
                    <span style="font-weight:bold;">Total:</span>
                    <span>{self.totalMessages}, </span>
                    <span style="font-weight:bold;">Selected:</span>
                    <span>{self.selectedMessages}</span>
                </div>

                <div>
                    <span style="font-weight:bold;margin-bottom:2px;">Percent:</span>
                    <span>
                        {self.getDaysSelectedPercent()}% of days,
                        {int((self.selectedMessages / self.totalMessages) * 100)}% of messages
                    </span>
                </div>

                <div>
                    <span style="font-weight:bold;margin-bottom:2px;">Average Message Time:</span>
                    <span> {self.averageMessagingTime}</span>
                </div>
            </div>
            """
    
    def updateElements(self, event=None):
        self.getMessagesInTimeFrame()
        self.averageMessagingTime = self.getAverageMessagingTime()
        self.updateWordCounts()
        self.setMostCommonWordsDf()
        self.HTMLPane.object = self.getHTML()
    
    def watch(self):
        self.daySlider.param.watch(self.updateElements, 'value')

    def add_words(self, message):
        for word in message.contents.split():
            if word in self.wordCounts:
                word = word.lower()
                self.wordCounts[word] += 1

    def remove_words(self, message):
        for word in message.contents.split():
            if word in self.wordCounts:
                word = word.lower()
                self.wordCounts[word] -= 1
                if self.wordCounts[word] == 0:
                    del self.wordCounts[word]