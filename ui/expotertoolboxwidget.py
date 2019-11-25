import logging
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QVBoxLayout, QGroupBox, QListWidget, QAbstractItemView, \
    QHBoxLayout, QListWidgetItem, QLabel, QCheckBox

from plugins.ui.exportertoolbox import ExporterToolbox


class ExportList(QListWidget):
    parametersChanged = pyqtSignal(list)

    def __init__(self, keylist):
        super().__init__()
        self.datakeys = keylist

        self.availableDataParameters = None
        self.setParameters()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemChanged.connect(self.itemListChanged)

    def toggleAll(self,event):
        for index in range(self.count()):
            if self.item(index).checkState() == QtCore.Qt.Checked:
                self.item(index).setCheckState(QtCore.Qt.Unchecked)
            else:
                self.item(index).setCheckState(QtCore.Qt.Checked)
        self.itemListChanged()

    def updateParameters(self, keylist):
        self.datakeys = keylist
        self.availableDataParameters = None
        self.setParameters()

    def itemListChanged(self, **kwargs):
        intindices = []
        for index in range(self.count()):
            if self.item(index).checkState() == QtCore.Qt.Checked:
                intindices.append(int(index))

        self.exportabledatakeys = [key for index, key in enumerate(self.datakeys) if index in intindices]
        logging.info("Export the following keys {0}".format(self.exportabledatakeys))
        self.parametersChanged.emit(self.exportabledatakeys)

    def setParameters(self):
        # select these from the files
        self.clear()
        self.availableDataParameters = [key for key in self.datakeys]

        for key in self.availableDataParameters:
            item = QListWidgetItem()
            item.setText(key)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)
            self.addItem(item)


class H5FileListsGroup(QGroupBox):
    def __init__(self, routine: ExporterToolbox = None):
        super().__init__("H5FileList")
        self.routine = routine
        self.layout = QVBoxLayout()
        self.h5Files = []

        self.h5selectionlabel = QLabel("Please check files to Export")
        self.h5selection = ExportList(self.h5Files)
        self.h5selection.parametersChanged.connect(self.exportListChanged)
        self.initUI()

    def reset(self,params):
        self.h5selection.updateParameters(params)

    def initUI(self):
        self.layout.addWidget(self.h5selectionlabel)
        self.layout.addWidget(self.h5selection)
        self.setLayout(self.layout)

    def exportListChanged(self,list):
        self.routine.exportableH5Files = list
        self.routine.onExportableH5FilesChanged()




class ExportableKeysGroup(QGroupBox):
    def __init__(self, routine: ExporterToolbox = None):
        super().__init__("Export")
        self.layout = QVBoxLayout()
        self.routine = routine

        self.datakeys = []
        self.datalabel = QLabel("Export these Datakeys")
        self.togglebutton = QPushButton("Toggle All")
        self.dataselection = ExportList(self.datakeys)

        self.togglebutton.clicked.connect(self.dataselection.toggleAll)
        self.dataselection.parametersChanged.connect(self.dataParametersChanged)

        self.dataselection.updateParameters(["Hallo"])
        self.availableDataParameters = None
        self.initUI()

    def reset(self,params):
        self.dataselection.updateParameters(params)

    def initUI(self):
        self.layout.addWidget(self.datalabel)
        self.layout.addWidget(self.dataselection)
        self.layout.addWidget(self.togglebutton)
        self.setLayout(self.layout)

    def dataParametersChanged(self, params):
        self.routine.exportableDataKeys = params
        self.routine.onExportableDataKeysChanged()


class ExpoterToolboxWidget(QWidget):
    def __init__(self, routine: ExporterToolbox):
        super(ExpoterToolboxWidget, self).__init__()
        self.routine = routine
        self.setWindowTitle("AIExporter")
        self.layout = QVBoxLayout()

        self.changefilebutton = QPushButton('Change File')
        self.changefilebutton.clicked.connect(self.changeFile)

        self.changedirectorybutton = QPushButton("Change Directory")
        self.changedirectorybutton.clicked.connect(self.changeDirectory)

        self.exportbutton = QPushButton("Export")
        self.exportbutton.clicked.connect(self.export)

        self.dataSelection = ExportableKeysGroup(self.routine)
        self.h5filelist = H5FileListsGroup(self.routine)


        self.savesinglefilecheck = QCheckBox("Save As Single File")
        self.savesinglefilecheck.setChecked(self.routine.saveSingleFile)
        self.savesinglefilecheck.stateChanged.connect(self.singlefilecheck)


        self.layout.addWidget(self.changedirectorybutton)
        self.layout.addWidget(self.h5filelist)
        self.layout.addWidget(self.dataSelection)

        self.layout.addWidget(self.savesinglefilecheck)
        self.layout.addWidget(self.exportbutton)
        self.setLayout(self.layout)
        self.show()

    def resetH5FilesList(self,filelists):
        self.h5filelist.reset(filelists)

    def resetDataList(self,dataparams):
        self.dataSelection.reset(dataparams)

    def changeFile(self):
        filepath, _ = QFileDialog.getOpenFileName()

        if filepath != "":
            logging.info("Trying to open {0}".format(filepath))
            self.routine.onH5FileChanged(filepath)

    def changeDirectory(self):
        filepath = QFileDialog.getExistingDirectory()

        if filepath != "":
            logging.info("Trying to open {0}".format(filepath))
            self.routine.onDirectoryChanged(filepath)

    def export(self):
        self.routine.startExport()


    def singlefilecheck(self,state):
        ILCheck = (state == QtCore.Qt.Checked)
        if ILCheck == True:
            self.routine.setSaveSingleFile(True)
        if ILCheck == False:
            self.routine.setSaveSingleFile(False)

        logging.info("Saving to one Single File is set to: {0}".format(self.routine.saveSingleFile))
