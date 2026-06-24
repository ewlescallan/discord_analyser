import matplotlib.pyplot as plt
import panel as pn

class dayChartClass:
    def __init__(self, messagesByDay, startDate, endDate, participantCount, daySlider, memberArray):
        self.messagesByDay = messagesByDay
        self.days = list(messagesByDay.keys())
        self.dayCount = len(self.days)
        self.originalVals = self.getOriginalVals()
        self.originalAverages = self.getAverages(self.originalVals)
        self.memberArray = memberArray
        self.lineColours = ["dimgrey"] + [member.colour for member in memberArray]
        self.vals = self.getVals()
        self.chart = self.initDayChart()
        self.pane = pn.pane.Matplotlib(self.chart, width=400, height=400)
        self.rollingWindowSlider = pn.widgets.IntSlider(value=0, start=0, end=90, step=5, name='Rolling Window')
        self.daySlider = daySlider
        self.axisLockBox = pn.widgets.Checkbox(label="Lock Axis")
        self.averages = self.originalAverages
        self.averageLinesBox = pn.widgets.Checkbox(label="Average Lines")
        self.linesBoxes = self.initLinesBoxes(participantCount)
    
    def getAverages(self, vals):
        originalAverages = [0 for i in range(len(vals))]
        for memberNo in range(len(self.originalVals)):
            originalAverages[memberNo] = sum(self.originalVals[memberNo]) / self.dayCount 
        return originalAverages

    #Obtains message totals per day without a rolling window (ie = 1)
    def getOriginalVals(self):
        vals = [[] for i in range(len(self.messagesByDay[self.days[0]]) + 1)]
        for dayNo in range(len(self.days)):
            day = self.days[dayNo]
            vals[0].append(len([item for sublist in self.messagesByDay[day] for item in sublist]))
            for lineNo in range(1, len(vals)):
                vals[lineNo].append(len(self.messagesByDay[day][lineNo - 1]))
        return vals

    #Obtains message totals. Rolling window means the last x days are summed, reducing variability
    def getVals(self, rollingWindow=0):
        if rollingWindow == 0: return self.getOriginalVals()
        rollingWindow += 1
        vals = [[] for i in range(len(self.messagesByDay[self.days[0]]) + 1)]
        totals = [0 for i in range(len(vals))]
        for dayNo in range(len(self.days)):
            day = self.days[dayNo]
            totals[0] += len([item for sublist in self.messagesByDay[day] for item in sublist])
            for lineNo in range(len(vals)):
                if lineNo > 0 :
                    totals[lineNo] += len(self.messagesByDay[day][lineNo - 1])
                if dayNo - rollingWindow >= 0:
                    totals[lineNo] -= self.originalVals[lineNo][dayNo - rollingWindow]
                vals[lineNo].append(totals[lineNo])
        return vals
    
    #Returns the gap between the actual start and end date and the selected dates from the slider
    def getDayChartGap(self, startDate, endDate):
        startGap, endGap = 0, 0
        firstDay = self.days[0]
        lastDay = self.days[-1]
        if startDate != firstDay:
            startGap = int(str(startDate - firstDay).split(" ")[0])
        if endDate != lastDay:
            endGap = int(str(lastDay - endDate).split(" ")[0])
        return startGap, endGap

    #Initialises the checkboxes allowing for certain lines to be shown or hidden
    def initLinesBoxes(self, participantCount):
        dayChartLines = [pn.widgets.Checkbox(label="Total")]
        dayChartLines[0].value = True
        for memberNo in range(participantCount):
            dayChartLines.append(pn.widgets.Checkbox(label=f"{self.memberArray[memberNo].name}"))
        return dayChartLines

    #Create initial daily message chart
    def initDayChart(self):
        fig,ax = plt.subplots(figsize = (4,3))
        ax.plot(self.days, self.vals[0], color=self.lineColours[0])
        fig.subplots_adjust(
            left=0.15,
            right=0.98,
            bottom=0.15,
            top=0.95
        )
        plt.close(fig)
        return fig

    #Update daily message chart, taking widgets into account
    def updateDayChart(self, startDate, endDate):
        maxValue = 0
        startGap, endGap = self.getDayChartGap(startDate, endDate)
        days = self.days[startGap : self.dayCount - endGap]
        fig,ax = plt.subplots(figsize = (4,3))
        for dayChartLineNo in range(len(self.linesBoxes)):
            if self.linesBoxes[dayChartLineNo].value:
                maxValue = max(maxValue, max(self.vals[dayChartLineNo]))
                line = self.vals[dayChartLineNo][startGap : self.dayCount - endGap]
                ax.plot(days, line, color=self.lineColours[dayChartLineNo])
            if self.averageLinesBox.value:
                ax.plot(days, [self.averages[dayChartLineNo] for i in range(self.dayCount)][startGap : self.dayCount - endGap], linestyle="dashed", color=self.lineColours[dayChartLineNo])
        if self.axisLockBox.value:
            ax.set_ylim(top=maxValue * 1.05)
        fig.subplots_adjust(
            left=0.15,
            right=0.98,
            bottom=0.15,
            top=0.95
        )
        plt.close(fig)
        return fig
    
    #Called when the rolling window slider has been changed to get new values
    def rollingWindowChanged(self, event=None):
        self.vals = self.getVals(self.rollingWindowSlider.value)
        self.averages = list(map(lambda x: x * (self.rollingWindowSlider.value + 1), self.originalAverages))
        self.chartChanged()
    
    #Called when any parameter attached to the chart has changed via a widget
    def chartChanged(self, event=None):
        self.pane.object = self.updateDayChart(self.daySlider.value_start, self.daySlider.value_end)
        self.pane.param.trigger('object')

    #Sets all widgets to watch for changes
    def watchWidgets(self):
        self.rollingWindowSlider.param.watch(self.rollingWindowChanged, 'value')
        self.averageLinesBox.param.watch(self.chartChanged, 'value')
        self.axisLockBox.param.watch(self.chartChanged, 'value')
        for lineCheckBox in self.linesBoxes:
            lineCheckBox.param.watch(self.chartChanged, 'value')

    def setUp(self, width, height):
        grid = pn.GridSpec(width=width, height=height)
        grid[0:6, 0:4] = pn.Column(
                    self.rollingWindowSlider,
                    self.axisLockBox,
                    self.averageLinesBox,
                    pn.Column(*self.linesBoxes)
                    )
        grid[0:6, 4:16] = self.pane
        return grid