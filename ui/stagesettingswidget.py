import logging

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QGridLayout

from plugins.ui.toolbox import StandardToolbox
from ui.valueselector import ValueSelector


class StageSettingsGroup(QGroupBox):
    def __init__(self, name, routine: StandardToolbox):
        super().__init__(name)
        self.routine = routine
        self.settings = self.routine.settings

        self.resetStagebutton = QPushButton("Set Stage")
        self.resetStagebutton.clicked.connect(self.setStage)

        self.layout = QGridLayout()
        self.initUI()

    def reset(self):
        for i in reversed(range(self.layout.count())):
            widgetToRemove = self.layout.itemAt(i).widget()
            # remove it from the layout list
            self.layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

        logging.info("Stage Settings reseted")

        self.initUI()

    def initUI(self):
        self.minimumslider = ValueSelector("Minimum", self.settings.startstack, self.settings.endstack, self.valuechanged, ismin=True)
        self.maximumslider = ValueSelector("Maximum", self.settings.startstack, self.settings.endstack, self.valuechanged, ismax=True)

        self.minimumslider.valueslider.setValue(int(self.routine.settings.startstack))
        self.maximumslider.valueslider.setValue(int(self.routine.settings.endstack))

        # Minimum Box
        self.layout.addWidget(self.minimumslider)
        self.layout.addWidget(self.maximumslider)
        self.layout.addWidget(self.resetStagebutton)

        self.setLayout(self.layout)

    def valuechanged(self, value, ismax, ismin):
        if ismin is True:
            logging.info("Setting Startstage to {0}".format(value))
            self.routine.settings.startstage = value
        if ismax is True:
            logging.info("Setting Endstage to {0}".format(value))
            self.routine.settings.endstage = value


    def setStage(self):
        self.routine.onStageSettingsChanged()

    def snapshotAIS(self,event):
        pass
