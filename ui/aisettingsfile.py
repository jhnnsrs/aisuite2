import logging

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel

from plugins.ui.toolbox import StandardToolbox
from ui.selectors import AISSelector
from ui.valueselector import ValueSelector


class AISSettingsGroup(QGroupBox):
    def __init__(self, name, routine: StandardToolbox):
        super().__init__(name)
        self.routine = routine
        self.layout = QVBoxLayout(self)

        self.initUI()


    def reset(self):
        for i in reversed(range(self.layout.count())):
            widgetToRemove = self.layout.itemAt(i).widget()
            # remove it from the layout list
            self.layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

        logging.info("AIS Settings reseted")

        self.initUI()

    def initUI(self):
        self.minimumslider = ValueSelector("Threshold", 0, 100, self.valueChanged, ismin=True)
        self.minimumslider.valueslider.setValue(int(self.routine.settings.threshold*100))

        self.sizeSlider = ValueSelector("Scale",5,40,self.sizeChanged,ismin=True)
        self.sizeSlider.valueslider.setValue(int(self.routine.settings.scale))
        self.b4selector = AISSelector(self.routine, self.routine.aisChannelChanged)

        self.flagslabel = QLabel("Channel")
        self.layout.addWidget(self.flagslabel)
        self.layout.addWidget(self.b4selector)
        self.layout.addWidget(self.minimumslider)
        self.layout.addWidget(self.sizeSlider)

        self.setLayout(self.layout)

    def valueChanged(self,value,ismin,ismax):
        if float(value) == float(self.routine.settings.threshold * 100): return
        self.routine.thresholdChanged(value)
        logging.info("Setting AIS-Threshold to {0}".format(str(value)))

    def sizeChanged(self,value,ismin,ismax):
        if int(value) == int(self.routine.settings.scale): return
        self.routine.scalechanged(value)
        logging.info("Setting DataImageSize to {0}".format(str(value)))