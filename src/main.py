import panel as pn
import matplotlib.pyplot as plt
import datetime as dt

from classDayChart import dayChartClass
from classMemberPane import memberPaneClass
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

messageArray, memberArray = reader.setUpMessagesArray() # List of each member's list of message objects
participantCount = len(messageArray)

startDate, endDate = reader.getStartAndEndDate(messageArray)
totalDays = (endDate - startDate).days
messagesByDay = reader.getMessagesByDay(messageArray, startDate, endDate)

daySlider = initDaySlider(startDate, endDate, totalWidth)
dayChart = dayChartClass(messagesByDay, startDate, endDate, participantCount, daySlider, memberArray)
dayChart.watchWidgets() 
daySlider.param.watch(dayChart.chartChanged, 'value')

memberGrid = pn.GridSpec(width=totalWidth, height=450) #5x1
graphGrid = pn.GridSpec(width=totalWidth, height=600)  #2x2

for memberNo in range(len(memberArray)):
    currentMemberPane = memberPaneClass(memberArray[memberNo], daySlider, messageArray[memberNo], totalDays)
    currentMemberPane.watch()
    memberGrid[0, memberNo] = currentMemberPane.pane

if len(memberArray) < 5:
    for i in range(len(memberArray), 7 - len(memberArray)):
        memberGrid[0, i] = pn.Column(styles=dict(background="aliceblue"))

graphGrid[1, 0] = dayChart.pane
graphGrid[1, 1] = dayChart.pane
graphGrid[0, 1] = dayChart.pane
graphGrid[0, 0] = dayChart.setUp(int(totalWidth / 2), 400)


# template = pn.template.FastListTemplate(
#     title="Discord Stats",
#     )

template = pn.template.BootstrapTemplate(
    title="Discord Analysis"
)

template.main.append(pn.Column(
        memberGrid,
        daySlider,
        graphGrid)
)
template.servable()
