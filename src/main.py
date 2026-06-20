import panel as pn
import matplotlib.pyplot as plt
import datetime as dt

import reader


pn.extension()

messagesArray = reader.setUpMessagesArray()
startDate, endDate = reader.getStartAndEndDate(messagesArray)
messagesByDay = reader.getMessagesByDay(messagesArray, startDate, endDate)

def getDayChartVals(messagesByDay):
    days = list(messagesByDay.keys())
    vals = []
    for day in days:
        #Flatten nested list to get total messages
        vals.append(len([item for sublist in messagesByDay[day] for item in sublist]))
    return [days, vals]

def initDayChart(days, vals):
    fig,ax = plt.subplots(figsize = (4,3))
    ax.plot(days, vals)
    plt.close(fig)
    return fig


def updateDayChart(days, vals, startDate, endDate):
    dayCount = len(days)
    startGap, endGap = 0, 0
    if startDate != days[0]:
        startGap = int(str(startDate - days[0]).split(" ")[0])
    if endDate != days[-1]:
        endGap = int(str(days[-1] - endDate).split(" ")[0])
    days = days[startGap:dayCount - endGap]
    vals = vals[startGap:dayCount - endGap]
    fig,ax = plt.subplots(figsize = (4,3))
    ax.plot(days, vals)
    plt.close(fig)
    return fig



date_range_slider = pn.widgets.DateRangeSlider(
    label='Date Range Slider',
    start=startDate, end=endDate,
    value=(startDate, endDate),
    step=2
)

dayChartVals = getDayChartVals(messagesByDay)


a = initDayChart(dayChartVals[0], dayChartVals[1])
dayChart = pn.pane.Matplotlib(a)

def changed(event):
    print(f"{event.new}")   
    print(event.new[1] - event.new[0])
    dayChart.object = updateDayChart(dayChartVals[0], dayChartVals[1], event.new[0], event.new[1])
    dayChart.param.trigger('object')

date_range_slider.param.watch(changed, 'value')

pn.Column(
    date_range_slider,
    dayChart
).servable()

# initDayChart(messagesByDay, dt.date(2026, 5, 1), endDate)
