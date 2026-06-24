import panel as pn
import matplotlib.pyplot as plt
import datetime as dt

from dayChartClass import dayChartClass
import reader

#Initialises the slider allowing for date selection
def initDaySlider(startDate, endDate, totalWidth):
    return pn.widgets.DateRangeSlider(
        label='Date Range',
        start=startDate, end=endDate,
        value=(startDate, endDate),
        step=7,
        margin = (0, int(totalWidth / 2) - 150),
    )

pn.extension()

totalWidth = 1440
totalHeight = 800

messagesArray = reader.setUpMessagesArray()
participantCount = len(messagesArray)
startDate, endDate = reader.getStartAndEndDate(messagesArray)
messagesByDay = reader.getMessagesByDay(messagesArray, startDate, endDate)

daySlider = initDaySlider(startDate, endDate, totalWidth)
dayChart = dayChartClass(messagesByDay, startDate, endDate, participantCount, daySlider)
dayChart.watchWidgets()
daySlider.param.watch(dayChart.chartChanged, 'value')

memberGrid = pn.GridSpec(width=1440, height=260) #5x1
graphGrid = pn.GridSpec(width=1440, height=700)  #2x2

memberGrid[0, 0] = pn.Spacer(styles=dict(background='red'))
memberGrid[0, 1] = pn.Spacer(styles=dict(background='green'))
memberGrid[0, 2] = pn.Spacer(styles=dict(background='purple'))
memberGrid[0, 3] = pn.Spacer(styles=dict(background='orange'))
memberGrid[0, 4] = pn.Spacer(styles=dict(background='blue'))

graphGrid[1, 0] = dayChart.pane
graphGrid[1, 1] = dayChart.pane
graphGrid[0, 1] = dayChart.pane
graphGrid[0, 0] = dayChart.setUp(int(totalWidth / 2), 400)

pn.Column(
    memberGrid,
    daySlider,
    graphGrid
).servable()

