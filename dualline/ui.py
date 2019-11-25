#  This file is part of AIVolume.

#  AIVolume is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  AIVolume is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with AIVolume.  If not, see <http://www.gnu.org/licenses/>.
import logging
import random

from matplotlib.widgets import LassoSelector
from matplotlib import path

import matplotlib

from plugins.standard.plugin import Plugin
from structures.roidata import DATA, DummyData, StraightenedDATA, VolumetricData

matplotlib.use("QT5Agg")

import sys
from PyQt5 import QtCore, QtWidgets, QtGui

import h5py
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QFileDialog, QTextEdit, QLineEdit, \
    QMessageBox, QGroupBox, QGridLayout, QLabel, QHBoxLayout, QMainWindow, QDockWidget, QCheckBox
from matplotlib import lines

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from matplotlib.widgets import SpanSelector, LassoSelector

from dualline.logic import getData
from ui.valueselector import ValueSelector
from volume.elements import AreaROI
from volume.settings import Global






class VolumetricGraphWidget(QWidget):
    def __init__(self, routine):
        super(VolumetricGraphWidget, self).__init__()
        logging.info("Volumetricgraph Window Started")
        self.routine = routine
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Graph and Flourescence (+Volumetric)")
        self.roiindex = 0
        self.xmin = 0
        self.xmax = 1
        self.secondxmin = 0
        self.secondxmax = 1
        self.secondthreshold = 0.3
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.data = None
        self.shown = False
        self.showall = False
        self.secondchannelUI = 300

        self.flags = QLineEdit()
        self.flagsSave = QPushButton("Save")
        self.flagsSave.clicked.connect(self.save)

        self.minimumslider = ValueSelector("Threshold", 0, 100, self.thresholdChanged, ismin=True)
        self.minimumslider.valueslider.setValue(int(self.routine.settings.threshold * 100))

        self.dataCanvas = self.fig.add_subplot(513)
        self.data2Canvas = self.fig.add_subplot(515)
        self.pictureCanvas = self.fig.add_subplot(511)
        self.picture1Canvas = self.fig.add_subplot(512)
        self.picture2Canvas = self.fig.add_subplot(514)

        self.span = SpanSelector(self.data2Canvas, self.onsecondselect, 'horizontal', useblit=True,
                                 rectprops=dict(alpha=0.5, facecolor='red'))

        self.span2 = SpanSelector(self.dataCanvas, self.onselect, 'horizontal', useblit=True,
                                  rectprops=dict(alpha=0.5, facecolor='red'))

        self.setUI()
        self.show()

    def thresholdChanged(self, value, ismin, ismax):
        if self.shown is False: return
        self.newthreshold = float(value / 100)
        self.calculate()

    def secondthresholdChanged(self, value, ismin, ismax):
        if self.shown is False: return
        self.secondthreshold = float(value / 100)
        self.calculate()

    def onselect(self, xmin, xmax):
        self.xmin = int(xmin)
        self.xmax = int(xmax)
        print(xmin, xmax)
        self.calculate()

    def onsecondselect(self, xmin, xmax):
        self.secondxmin = int(xmin)
        self.secondxmax = int(xmax)
        print(xmin, xmax)
        self.calculate()


    def save(self):
        self.data.flags = self.flags.text().split(",")
        self.routine.onDataUpdate(self.data)

    def calculate(self):
        if self.data is not None:
            data = self.routine.processData(self.data, (self.xmin, self.xmax), (self.secondxmin, self.secondxmax), self.newthreshold, self.secondthreshold, self.secondchannelUI)
            self.displayData(data)

    def updateData(self):
        self.routine.onDataUpdate(self.data)

    def cleanUp(self):
        self.datasections = []

    def displayData(self, data: StraightenedDATA):
        self.cleanUp()
        self.shown = False
        self.data = data

        self.xmin = data.selectedxstart
        self.xmax = data.selectedxend

        channels = 1
        try:
            if len(self.data.intensitycurves.shape) > 1:
                channels = self.data.intensitycurves.shape[1]
        except: pass


        secondchannel = self.secondchannelUI if self.secondchannelUI < channels else channels - 1
        self.newthreshold = data.threshold
        self.pictureCanvas.imshow(data.roiimage, aspect="auto")
        self.picture1Canvas.imshow(data.roiimage[:,:,data.b4channel], aspect="auto")
        self.picture2Canvas.imshow(data.roiimage[:,:,secondchannel], aspect="auto")
        self.minimumslider.valueslider.setValue(int(data.threshold * 100))

        self.dataCanvas.clear()
        self.data2Canvas.clear()
        self.dataCanvas.set_xlim([0, data.piclength])
        self.data2Canvas.set_xlim([0, data.piclength])
        self.picture1Canvas.set_xlim([0, data.piclength])
        self.picture2Canvas.set_xlim([0, data.piclength])
        self.pictureCanvas.set_xlim([0, data.piclength])
        self.dataCanvas.axvline(x=self.xmin, color='k', linestyle='--')
        self.dataCanvas.axvline(x=self.xmax, color='k', linestyle='--')

        self.data.intensitycurves = np.nan_to_num(self.data.intensitycurves)

        if len(self.data.intensitycurves.shape) > 1:
            if self.showall:
                self.dataCanvas.plot(self.data.intensitycurves[:, 0], color="red")
                self.dataCanvas.plot(self.data.intensitycurves[:, 1], color="green")
                self.dataCanvas.plot(self.data.intensitycurves[:, 2], color="blue")
            else:
                self.dataCanvas.plot(self.data.intensitycurves[:, data.b4channel],color="red")
                self.data2Canvas.plot(self.data.intensitycurves[:, secondchannel], color="blue")
        else:
            self.dataCanvas.plot(self.data.intensitycurves[:])

        formatedreallength = "{0:.4f}".format(data.aisphysicallength)
        label = formatedreallength + " " + data.physicalsizeunit
        if data.aisstart == -1 or data.aisend == -1:
            self.dataCanvas.text(self.xmin, data.threshold + 0.1, "NO AIS")
        else:
            self.dataCanvas.plot([data.aisstart, data.aisend], [data.threshold, data.threshold], 'k-', lw=2)
            self.dataCanvas.text(data.aisstart + data.aislength / 2 - 10, data.threshold + 0.1, label)

        if data.hassecond:

            self.secondxmax = data.selectedsecondxend
            self.secondxmin = data.selectedsecondxstart

            formatedreallength = "{0:.4f}".format(data.secondphysicallength)
            label = formatedreallength + " " + data.physicalsizeunit

            self.data2Canvas.axvline(x=data.selectedsecondxstart, color='k', linestyle='--')
            self.data2Canvas.axvline(x=data.selectedsecondxend, color='k', linestyle='--')


            if data.secondstart == -1 or data.secondend == -1:
                self.data2Canvas.text(self.secondxmin, data.secondthreshold + 0.1, "NO SECOND")
            else:
                self.data2Canvas.plot([data.secondstart, data.secondend], [data.secondthreshold, data.secondthreshold], 'k-', lw=2)
                self.data2Canvas.text(data.secondstart + data.secondlength / 2 - 10, data.secondthreshold + 0.1, label)



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
        self.settingLayout.addWidget(self.minimumslider, 0, 2)
        self.settingLayout.addWidget(self.bt_button, 0, 4)
        # self.settingLayout.addWidget(self.calculatebutton,1,0)
        self.settingBox.setLayout(self.settingLayout)

        # SECOND DATA
        self.dataBox = QGroupBox("2ND")
        self.settingLayout2 = QGridLayout()

        self.secondthresholdselector = ValueSelector("Threshold", 0, 100, self.secondthresholdChanged, ismin=True)
        self.secondthresholdselector.valueslider.setValue(int(self.routine.settings.threshold * 100))
        self.secondchannelselector = SynpoChannelSelector("2ND Channel", self.secondchannelchanged)

        self.settingLayout2.addWidget(self.secondthresholdselector, 0, 1)
        self.settingLayout2.addWidget(self.secondchannelselector, 0, 2)
        # self.settingLayout.addWidget(self.calculatebutton,1,0)
        self.dataBox.setLayout(self.settingLayout2)



        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.settingBox)
        self.layout.addWidget(self.dataBox)

        self.bt_button.clicked.connect(self.doCheck)

        self.setLayout(self.layout)


    def secondchannelchanged(self, channel):
        self.secondchannelUI = channel
        self.calculate()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.hide()
        a0.ignore()


class VolumetricDataDisplay(Plugin):

    def __init__(self,callback):
        super(VolumetricDataDisplay, self).__init__()
        logging.info("Volumetric Data Display initialized")
        self.dataWidget = VolumetricGraphWidget(self)
        self.datacallback = callback

    def displayData(self, data: DATA):
        if isinstance(data, DummyData):
            self.dataWidget.displayDummy()
        else:
            self.dataWidget.displayData(data)

    def processData(self, data, segments, segments2, threshold, threshold2, secondchannel):
        from .logic import reprocessAISandSecond
        data = reprocessAISandSecond(data, segments, segments2, threshold, threshold2, secondchannel)
        return data

    def onDataUpdate(self, data: DATA):
        self.datacallback(data)


class SynpoChannelSelector(QtWidgets.QComboBox):
    def __init__(self, name, callback):
        super(SynpoChannelSelector, self).__init__()
        self.logprefix = "{0}"
        self.name = name
        self.itemnames = []
        self.channellist = []
        self.itemsToAdd()
        self.synpochannel = 2
        self.callback = callback

        self.currentIndexChanged.connect(self.selectionChanged)

    def itemsToAdd(self):
        self.newItem("R", 0)
        self.newItem("G", 1)
        self.newItem("B", 2)

    def selectionChanged(self, i):
        self.callback(i)

    def newItem(self, name, callback):
        self.addItem(name)
        self.itemnames.append(name)

    def changeSelected(self, i):
        raise NotImplementedError


class DualWindow(QMainWindow):
    def __init__(self):
        super(DualWindow, self).__init__()
        self.ais = None
        self.h5file = None
        self.data = None
        self.setWindowTitle("AIDual")
        self.pix = None
        Global.imageWindow = self

        import matplotlib.pyplot as plt

        self.intensity = VolumetricDataDisplay(self.dataUpdated)
        self.intensitywidget = self.intensity.dataWidget


        self.roidock = QDockWidget("Settings", self)

        self.setCentralWidget(self.intensitywidget)

        self.settings = QWidget()
        self.settingsLayout = QVBoxLayout()

        self.settingBox = QGroupBox("Roi-Meta")
        self.settingLayout = QGridLayout()

        self.indexLabel = QLabel("Roi")
        self.indexEdit = QLineEdit()
        self.indexEdit.setDisabled(True)
        self.settingLayout.addWidget(self.indexLabel, 1, 0)
        self.settingLayout.addWidget(self.indexEdit, 1, 1)

        self.fileLabel = QLabel("File")
        self.fileEdit = QLineEdit()
        self.fileEdit.setDisabled(True)
        self.settingLayout.addWidget(self.fileLabel, 0, 0)
        self.settingLayout.addWidget(self.fileEdit, 0, 1)

        self.volumeLabel = QLabel("Volume")
        self.volumeEdit = QLineEdit()
        self.volumeEdit.setDisabled(True)
        self.settingLayout.addWidget(self.volumeLabel, 2, 0)
        self.settingLayout.addWidget(self.volumeEdit, 2, 1)

        self.diameterLabel = QLabel("Diameter")
        self.diameterEdit = QLineEdit()
        self.diameterEdit.setDisabled(True)
        self.settingLayout.addWidget(self.diameterLabel, 3, 0)
        self.settingLayout.addWidget(self.diameterEdit, 3, 1)

        self.diameterLabel = QLabel("SynpoVolume")
        self.diameterEdit = QLineEdit()
        self.diameterEdit.setDisabled(True)
        self.settingLayout.addWidget(self.diameterLabel, 4, 0)
        self.settingLayout.addWidget(self.diameterEdit, 4, 1)

        self.settingBox.setLayout(self.settingLayout)

        self.settingsLayout.addWidget(self.settingBox)

        self.fileBox = QGroupBox("Files")
        self.filesLayout = QGridLayout()

        self.changefilebutton = QPushButton('Change File')
        self.changefilebutton.clicked.connect(self.changeFile)
        self.filesLayout.addWidget(self.changefilebutton, 0, 1)

        # set button to call somefunction() when clicked

        self.flagsBox = QGroupBox("Flags")
        self.flagsLayout = QVBoxLayout()
        self.flagsText = QLineEdit()
        self.flagsLayout.addWidget(self.flagsText)
        self.flagsBox.setLayout(self.flagsLayout)
        self.settingsLayout.addWidget(self.flagsBox)

        self.fileBox.setLayout(self.filesLayout)
        self.settingsLayout.addWidget(self.fileBox)
        self.settingsLayout.addStretch()

        self.filebutton = QPushButton("Choose Directory", self)
        self.filebutton.clicked.connect(self.openDir)

        self.settingsLayout.addWidget(self.filebutton)

        self.settings.setLayout(self.settingsLayout)
        self.roidock.setWidget(self.settings)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.roidock)
        self.show()

    def dataUpdated(self,data):
        self.ais = data
        self.saveROI()

    def cannyselector1changed(self, value, ismax, ismin):
        if ismin is True:
            logging.info("Setting Canny1 to {0}".format(value))
            self.canny1 = value
            self.updateUI()
        if ismax is True:
            print("EROOR")
            logging.info("Setting Endstage to {0}".format(value))
            self.canny2 = value

    def updateUI(self, ais):
        self.setWindowTitle(Global.filepath)

        self.intensitywidget.displayData(self.ais)

    def setRoi(self):

        self.ais.linelist = self.linelist
        self.ais.sobel = self.sobelx

    def instantiateFiles(self):
        self.aish5list = getData(Global.filepath)
        random.shuffle(self.aish5list)
        self.newinstance()

    def newinstance(self):
        if len(self.aish5list) >= 1:
            self.ais, self.h5file = self.aish5list.pop()
            print("HFile", self.h5file, " ROI: ", self.ais.index)
            print("Resetting the pix matrix")
            self.updateUI(self.ais)
        else:
            QMessageBox.about(self, "All Done", "Every single file is already evaluated. YEAAHHHH")
            self.openDir()

    def saveROI(self):

        print(self.ais)

        with h5py.File(self.h5file, "a") as f:
            f["Data/" + self.ais.key].attrs["SecondStart"] = self.ais.secondstart
            f["Data/" + self.ais.key].attrs["SecondEnd"] = self.ais.secondend
            f["Data/" + self.ais.key].attrs["SecondLength"] = self.ais.secondlength
            f["Data/" + self.ais.key].attrs["DistanceSecondStart"] = self.ais.distancesecondstart
            f["Data/" + self.ais.key].attrs["DistanceSecondStartPhysical"] = self.ais.distancesecondstartphysical
            f["Data/" + self.ais.key].attrs["SelectedSecondXEnd"] = self.ais.selectedsecondxend
            f["Data/" + self.ais.key].attrs["SelectedSecondXStart"] = self.ais.selectedsecondxstart
            f["Data/" + self.ais.key].attrs["SecondPhysicalLength"] = self.ais.secondphysicallength
            f["Data/" + self.ais.key].attrs["SecondThreshold"] = self.ais.secondthreshold
            f["Data/" + self.ais.key].attrs["SecondChannel"] = self.ais.secondchannel
            f["Data/" + self.ais.key].attrs["HasSecond"] = self.ais.hassecond

        return 0

    def quit(self):
        pass

    def openDir(self):
        # this is called when button1 is clicked
        # put directory specific tasks here
        # examples:
        ddir = QFileDialog.getExistingDirectory(self, "Get Dir Path")
        print(ddir)
        # ddir is a QString containing the path to the directory you selected
        if ddir != "":
            Global.filepath = ddir
            self.instantiateFiles()

        # lets get a list of files from the directory:



    def startParsing(self):
        self.setRoi()
        self.ais.diameter, self.ais.volume = logic.calculateDiameterAndVolume(self.ais)
        self.synpodiameter, self.synpovolume = logic.calculateSynpoVolume(self.ais)

        self.volumeEdit.setText(str(self.ais.volume) + " µm")
        self.diameterEdit.setText(str(self.ais.diameter) + " µm")

    def changeFile(self, **kwargs):
        self.linelist = []
        self.newinstance()

    def onselect(self, xmin, xmax):
        print(xmin, xmax)
        self.ais.sections.append([xmin, xmax])

    def updateArray(self, array, indices):
        lin = np.arange(array.size)
        newArray = array.flatten()
        newArray[lin[indices]] = 1
        return newArray.reshape(array.shape)

    def onlassoselectcluster(self, verts):
        p = path.Path(verts)
        ind = p.contains_points(self.pix, radius=1)
        self.clustermask.flat[ind] = np.ones_like(self.ais.image[:, :, 0]).flat[ind]
        self.updateUI()

    def onlassoselectais(self, verts):
        p = path.Path(verts)
        ind = p.contains_points(self.pix, radius=1)
        self.aismask.flat[ind] = np.ones_like(self.ais.image[:, :, 0]).flat[ind]
        self.updateUI()


h_excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    h_excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
# sys.excepthook = my_exception_hook

if __name__ == '__main__':

    app = QApplication(sys.argv)

    image = SynpoWindow()

    image.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
