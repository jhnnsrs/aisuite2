import logging

import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QGroupBox, QGridLayout, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.widgets import SpanSelector

from plugins.ui.datadisplay import StandardDataDisplay, VolumetricDataDisplay
from structures.roidata import StraightenedDATA, VolumetricData
from ui.valueselector import ValueSelector


class GraphWidget(QWidget):
    def __init__(self, routine: StandardDataDisplay):
        super(GraphWidget, self).__init__()
        logging.info("Graph Window Started")
        self.routine = routine
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Graph and Flourescence")
        self.roiindex = 0
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.data = None

        self.flags = QLineEdit()
        self.flagsSave = QPushButton("Save")
        self.flagsSave.clicked.connect(self.flagsChanged)

        self.dataCanvas = self.fig.add_subplot(212)
        self.pictureCanvas = self.fig.add_subplot(211)

        self.setUI()
        self.show()

    def flagsChanged(self):
        self.data.flags = self.flags.text().split(self.routine.settings.flagsseperator)
        self.routine.onDataUpdate(self.data)

    def displayData(self, data: StraightenedDATA):
        self.data = data

        self.pictureCanvas.imshow(data.roiimage)

        self.dataCanvas.clear()
        self.dataCanvas.set_xlim([0, data.piclength])
        print(data.intensitycurves.shape)
        if len(data.intensitycurves.shape) > 1:
            self.dataCanvas.plot(data.intensitycurves[:,1])
        else:
            self.dataCanvas.plot(data.intensitycurves[:])

        formatedreallength = "{0:.4f}".format(data.aisphysicallength)
        label = formatedreallength + " " + data.physicalsizeunit

        self.dataCanvas.plot([data.aisstart, data.aisend], [data.threshold, data.threshold], 'k-', lw=2)
        self.dataCanvas.text(data.aisstart + data.aislength / 2 - 10, data.threshold + 0.1, label)
        self.flags.setText(" ".join(data.flags))

        self.updateUI()

    def displayDummy(self):
        self.pictureCanvas.imshow(np.zeros(shape=(200, 10, 3), dtype=np.uint8))
        self.flags.setText("DUMMY DATA")
        self.updateUI()

    def updateUI(self):
        self.canvas.draw()
        self.show()

    def setUI(self):
        self.flagsLabel = QLabel("Flags")
        self.settingBox = QGroupBox("ROI Meta")
        self.settingLayout = QGridLayout()

        self.settingLayout.addWidget(self.flags, 0, 1)
        self.settingLayout.addWidget(self.flagsLabel, 0, 0)
        self.settingLayout.addWidget(self.flagsSave, 0, 2)
        self.settingBox.setLayout(self.settingLayout)

        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.settingBox)

        self.setLayout(self.layout)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.hide()
        a0.ignore()




class VolumetricGraphWidget(QWidget):
    def __init__(self, routine: VolumetricDataDisplay):
        super(VolumetricGraphWidget, self).__init__()
        logging.info("Volumetricgraph Window Started")
        self.routine = routine
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Graph and Flourescence (+Volumetric)")
        self.roiindex = 0
        self.xmin = 0
        self.xmax = 1
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.data = None
        self.shown = False
        self.showall = False

        self.flags = QLineEdit()
        self.flagsSave = QPushButton("Save")

        self.minimumslider = ValueSelector("Threshold", 0, 100, self.thresholdChanged, ismin=True)
        self.minimumslider.valueslider.setValue(int(self.routine.settings.threshold*100))


        self.dataCanvas = self.fig.add_subplot(212)
        self.pictureCanvas = self.fig.add_subplot(211)

        self.span = SpanSelector(self.pictureCanvas, self.onselect, 'horizontal', useblit=True,
                                 rectprops=dict(alpha=0.5, facecolor='red'))

        self.span2 = SpanSelector(self.dataCanvas, self.onselect, 'horizontal', useblit=True,
                                 rectprops=dict(alpha=0.5, facecolor='red'))

        self.setUI()
        self.show()

    def thresholdChanged(self,value,ismin,ismax):
        if self.shown is False: return
        self.newthreshold = float(value/100)
        self.calculate()

    def onselect(self, xmin, xmax):
        self.xmin = int(xmin)
        self.xmax = int(xmax)
        print(xmin,xmax)
        self.datasections.append([xmin,xmax])
        self.calculate()

    def save(self):
        self.data.flags = self.flags.text().split(self.routine.settings.flagsseperator)
        self.routine.onDataUpdate(self.data)


    def calculate(self):
        if self.data is not None:
            data = self.routine.processData(self.data,(self.xmin,self.xmax),self.newthreshold)
            self.displayData(data)

    def updateData(self):
        data = VolumetricData()
        self.routine.onDataUpdate(self.data)

    def cleanUp(self):
        self.datasections = []

    def displayData(self, data: StraightenedDATA):
        self.cleanUp()
        self.shown = False
        self.data = data

        self.xmin = data.selectedxstart
        self.xmax = data.selectedxend

        self.newthreshold = data.threshold
        self.pictureCanvas.imshow(data.roiimage)
        self.minimumslider.valueslider.setValue(int(data.threshold*100))

        self.dataCanvas.clear()
        self.dataCanvas.set_xlim([0,data.piclength])
        self.dataCanvas.axvline(x=self.xmin, color='k', linestyle='--')
        self.dataCanvas.axvline(x=self.xmax, color='k', linestyle='--')

        if len(data.intensitycurves.shape) > 1:
            if self.showall:
                self.dataCanvas.plot(data.intensitycurves[:, 0], color="red")
                self.dataCanvas.plot(data.intensitycurves[:, 1], color="green")
                self.dataCanvas.plot(data.intensitycurves[:, 2], color="blue")
            else:
                self.dataCanvas.plot(data.intensitycurves[:, data.b4channel])
        else:
            self.dataCanvas.plot(data.intensitycurves[:])

        formatedreallength = "{0:.4f}".format(data.aisphysicallength)
        label = formatedreallength + " " + data.physicalsizeunit
        if data.aisstart == -1 or data.aisend == -1 :
            self.dataCanvas.text(self.xmin, data.threshold + 0.1, "NO AIS")
        else:
            self.dataCanvas.plot([data.aisstart, data.aisend], [data.threshold, data.threshold], 'k-', lw=2)
            self.dataCanvas.text(data.aisstart + data.aislength / 2 - 10, data.threshold + 0.1, label)

        self.flags.setText(" ".join(data.flags))
        self.updateUI()

        self.shown = True

    def displayDummy(self):
        self.pictureCanvas.imshow(np.zeros(shape=(200, 10, 3), dtype=np.uint8))
        self.flags.setText("DUMMY DATA")
        self.updateUI()

    def updateUI(self):
        self.canvas.draw()
        self.show()

    def doCheck(self):
        if self.bt_button.isChecked():
            self.showall = True
            self.updateUI()
        else:
            self.showall = False
            self.updateUI()

    def setUI(self):
        self.flagsLabel = QLabel("Flags")
        self.settingBox = QGroupBox("ROI Meta")
        self.settingLayout = QGridLayout()
        self.bt_button = QCheckBox("Show All")
        self.bt_button.setChecked(self.showall)

        self.settingLayout.addWidget(self.flags, 0, 1)
        self.settingLayout.addWidget(self.flagsLabel, 0, 0)
        self.settingLayout.addWidget(self.flagsSave, 0, 3)
        self.settingLayout.addWidget(self.minimumslider,0,2)
        self.settingLayout.addWidget(self.bt_button,0,4)
        #self.settingLayout.addWidget(self.calculatebutton,1,0)
        self.settingBox.setLayout(self.settingLayout)

        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.settingBox)

        self.bt_button.clicked.connect(self.doCheck)

        self.setLayout(self.layout)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.hide()
        a0.ignore()
