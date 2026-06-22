import matplotlib.pyplot as plt
import panel as pn

class dayChartClass:
    def __init__(self, messagesByDay, startDate, endDate, participantCount):
        self.messagesByDay = messagesByDay
        self.days = list(messagesByDay.keys())
        self.dayCount = len(self.days)
        self.valsTotal, self.valsInd = self.getVals()
        self.chart = self.initDayChart()
        self.pane = pn.pane.Matplotlib(self.chart)
        self.daySlider = self.initDaySlider(startDate, endDate)
        self.rollingWindowSlider = pn.widgets.IntSlider(value=0, start=0, end=90, step=5)
        self.axisLockBox = pn.widgets.Checkbox(label="Lock Axis")
        self.linesBoxes = self.initLinesBoxes(participantCount)

    def getVals(self):
        valsTotal = []
        valsInd = [[] for i in range(len(self.messagesByDay[self.days[0]]))]
        for day in self.days:
            #Flatten nested list to get total messages
            valsTotal.append(len([item for sublist in self.messagesByDay[day] for item in sublist]))
            for memberNo in range(len(valsInd)):
                valsInd[memberNo].append(len(self.messagesByDay[day][memberNo]))
        return valsTotal, valsInd
    
    def getDayChartGap(self, startDate, endDate):
        startGap, endGap = 0, 0
        firstDay = self.days[0]
        lastDay = self.days[-1]
        if startDate != firstDay:
            startGap = int(str(startDate - firstDay).split(" ")[0])
        if endDate != lastDay:
            endGap = int(str(lastDay - endDate).split(" ")[0])
        return startGap, endGap
    
    def initDaySlider(self, startDate, endDate):
        return pn.widgets.DateRangeSlider(
            label='Date Range Slider',
            start=startDate, end=endDate,
            value=(startDate, endDate),
            step=2
        )

    def initLinesBoxes(self, participantCount):
        dayChartLines = [pn.widgets.Checkbox(label="Total")]
        dayChartLines[0].value = True
        for memberNo in range(participantCount):
            dayChartLines.append(pn.widgets.Checkbox(label=f"Participant {memberNo + 1}"))
        return dayChartLines

    #Create initial daily message chart
    def initDayChart(self):
        fig,ax = plt.subplots(figsize = (4,3))
        ax.plot(self.days, self.valsTotal)
        plt.close(fig)
        return fig

    #Update daily message chart, taking widgets into account
    def updateDayChart(self, startDate, endDate):
        maxValue = 0
        startGap, endGap = self.getDayChartGap(startDate, endDate)
        days = self.days[startGap : self.dayCount - endGap]
        fig,ax = plt.subplots(figsize = (4,3))
        if self.linesBoxes[0].value:
            maxValue = max(maxValue, max(self.valsTotal))
            valsTotal = self.valsTotal[startGap : self.dayCount - endGap]
            ax.plot(days, valsTotal)
        for dayChartLineNo in range(1, len(self.linesBoxes)):
            if self.linesBoxes[dayChartLineNo].value:
                maxValue = max(maxValue, max(self.valsInd[dayChartLineNo - 1]))
                indLine = self.valsInd[dayChartLineNo - 1][startGap : self.dayCount - endGap]
                ax.plot(days, indLine)
        if self.axisLockBox.value:
            ax.set_ylim(top=maxValue + 100)
        plt.close(fig)
        return fig
    
    def chartChanged(self, event):
        self.pane.object = self.updateDayChart(self.daySlider.value_start, self.daySlider.value_end)
        self.pane.param.trigger('object')

    def watchWidgets(self):
        self.daySlider.param.watch(self.chartChanged, 'value')
        self.rollingWindowSlider.param.watch(self.chartChanged, 'value')
        self.axisLockBox.param.watch(self.chartChanged, 'value')
        for lineCheckBox in self.linesBoxes:
            lineCheckBox.param.watch(self.chartChanged, 'value')