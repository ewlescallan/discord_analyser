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

dayChart.daySlider.param.watch(dayChart.chartChanged, 'value')
dayChart.axisLockBox.param.watch(dayChart.chartChanged, 'value')
for lineCheckBox in dayChart.linesBoxes:
    lineCheckBox.param.watch(dayChart.chartChanged, 'value')

pn.Column(
    pn.Row(
        dayChart.daySlider,
        dayChart.axisLockBox
    ),
    pn.Row(
        pn.Column(*dayChart.linesBoxes),
        dayChart.pane
    )
).servable()


