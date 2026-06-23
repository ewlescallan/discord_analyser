import panel as pn
import matplotlib.pyplot as plt
import datetime as dt

from dayChartClass import dayChartClass
import reader


pn.extension()

messagesArray = reader.setUpMessagesArray()
participantCount = len(messagesArray)
startDate, endDate = reader.getStartAndEndDate(messagesArray)
messagesByDay = reader.getMessagesByDay(messagesArray, startDate, endDate)

dayChart = dayChartClass(messagesByDay, startDate, endDate, participantCount)
dayChart.watchWidgets()

pn.Column(
    pn.Row(
        dayChart.daySlider,
        dayChart.rollingWindowSlider
    ),
    pn.Row(
        pn.Column(
                *dayChart.linesBoxes, 
                  dayChart.axisLockBox
                ),
        dayChart.pane
    )
).servable()

