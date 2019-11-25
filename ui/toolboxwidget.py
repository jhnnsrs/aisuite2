import logging

import os
from PyQt5 import Qt, QtCore

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QGroupBox, QGridLayout, QSlider, \
    QFileDialog, QHBoxLayout, QCheckBox

from structures.settings import Settings
from plugins.ui.toolbox import StandardToolbox
from ui.aisettingsfile import AISSettingsGroup
from ui.calculatorsettingswidget import CalculatorSettingsGroup
from ui.channelsettingswidget import MappingSettingsGroup
from ui.picturesettingswidget import PictureSettingsGroup
from ui.stagesettingswidget import StageSettingsGroup


class StandardSettings(QWidget):
    def __init__(self, routine: StandardToolbox):
        super().__init__()
        self.routine = routine
        self.layout = QVBoxLayout(self)
        self.changefilebutton = QPushButton('Change File')
        self.changeseriesbutton = QPushButton("Change Series")
        self.changeseriesbutton.clicked.connect(self.changeSeries)
        self.addstagebutton = QPushButton("Add Stage")
        self.changefilebutton.clicked.connect(self.changeFile)
        self.addstagebutton.clicked.connect(self.addStage)
        self.addstagebutton.setStyleSheet("background-color: rgb(255,204,204)")

        self.layout.addWidget(self.changefilebutton)

        self.picturesettings = PictureSettingsGroup("Picture-Settings", self.routine)
        self.channelsettings = MappingSettingsGroup("Mapping-Settings", self.routine)

        self.layout.addWidget(self.changeseriesbutton)
        self.layout.addWidget(self.channelsettings)
        self.layout.addWidget(self.picturesettings)

        self.layout.addWidget(self.addstagebutton)


        self.setLayout(self.layout)

    def changeSeries(self):
        self.routine.onSeriesChanged()

    def mappingsReset(self):
        self.channelsettings.reset()

    def pictureReset(self):
        self.picturesettings.reset()

    def addStage(self):
        self.routine.onAddStagePressed()

    def changeFile(self):
        filepath, _ = QFileDialog.getOpenFileName()

        if filepath != "":
            logging.info("Trying to open {0}".format(filepath))
            self.routine.onFilepathChanged(filepath)




class DataSettings(QWidget):
    def __init__(self, routine: StandardToolbox):
        super().__init__()
        self.routine = routine
        self.layout = QVBoxLayout()
        self.stagesettings = StageSettingsGroup("Stage-Settings", self.routine)
        self.calculatorsettings = CalculatorSettingsGroup("Parsing-Settings",self.routine)
        self.aissettings = AISSettingsGroup("AIS-Settings", self.routine)

        self.savesettingsbutton = QPushButton("Save Settings")
        self.savesettingsbutton.clicked.connect(self.saveSettings)


        self.donefilebutton = QPushButton('Done')
        self.donefilebutton.setStyleSheet("background-color: rgb(240,255,240)")
        self.donefilebutton.clicked.connect(self.done)

        self.layout.addWidget(self.stagesettings)
        self.layout.addWidget(self.calculatorsettings)
        self.layout.addWidget(self.aissettings)

        self.savebioimagecheck = QCheckBox("Save Bioimage with File")
        self.savebioimagecheck.setChecked(self.routine.settings.saveBioImageToHDF)
        self.savebioimagecheck.stateChanged.connect(self.bioimagecheck)

        self.layout.addWidget(self.savebioimagecheck)
        self.layout.addWidget(self.savesettingsbutton)

        self.layout.addStretch()
        self.layout.addWidget(self.donefilebutton)


        self.setLayout(self.layout)

    def bioimagecheck(self,state):
        ILCheck = (state == QtCore.Qt.Checked)
        if ILCheck == True:
            self.routine.settings.saveBioImageToHDF = True
        if ILCheck == False:
            self.routine.settings.saveBioImageToHDF = False

        logging.info("Saving the Bioimage file is set to: {0}".format(self.routine.settings.saveBioImageToHDF))

    def saveSettings(self):
        filepath, filter = QFileDialog.getSaveFileName(self, 'Dialog Title', directory=self.routine.settings.directory, initialFilter='*.ini')
        if filepath != "":
            print(filepath)
            self.routine.onRequestSettingsSave(filepath)

    def reset(self):
        self.stagesettings.reset()
        self.aissettings.reset()


    def done(self):

        self.routine.onDoneWithFile()

    def loadSettings(self):

        pass



class ToolboxWidget(QWidget):
    def __init__(self, routine: StandardToolbox):
        super(ToolboxWidget, self).__init__()
        self.routine = routine
        self.setWindowTitle("AISelect")
        #Settings this as a Default
        self.routine.setStandardErrorRaiser(self)


        self.layout = QHBoxLayout(self)

        logging.info("Settings Window Started")

        self.setUI()
        self.show()

    def mappingsReset(self):
        self.standardsettings.mappingsReset()

    def reset(self):
        self.standardsettings.pictureReset()
        self.datasettings.reset()

    def setUI(self):

        self.standardsettings = StandardSettings(self.routine)
        self.datasettings = DataSettings(self.routine)


        self.layout.addWidget(self.standardsettings)
        self.layout.addWidget(self.datasettings)

        self.setLayout(self.layout)

