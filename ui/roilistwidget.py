from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QGroupBox

from plugins.ui.roilist import RoiListDisplay
from structures.sample import Sample


class RoiListWidget(QGroupBox):

    def __init__(self,routine: RoiListDisplay):
        super(RoiListWidget,self).__init__("Roilist")
        self.setWindowTitle("ROIManager")
        self.layout = QVBoxLayout(self)
        self.roilist = []
        self.lastit = 0
        self.routine = routine

        self.listWidget = QListWidget()
        self.cleanbutton = QPushButton("Clean Rois/Data")
        self.cleanbutton.clicked.connect(self.cleanAll)
        self.listWidget.setToolTip("Hallo")

        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.cleanbutton)
        self.setLayout(self.layout)

        self.show()

    def cleanAll(self):
        self.routine.onCleanRoiListPushed()

    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_Delete:
            self.routine.onDeleteItem(self.lastit)


    def updateList(self, sample: Sample):
        self.listWidget.clear()

        for key, data in sample.data.items():
            item = QtWidgets.QListWidgetItem("Roi {0}".format(data.key))
            if "Error" in data.flags: item.setBackground(QColor(255,255,0))
            self.listWidget.addItem(item)

        self.updateUI()

    def roiitemclicked(self,item):
        if item == None: return
        it = item.text().split(" ")
        if len(it) > 1:
            dataindex = int(item.text().split(" ")[1]) #should be catched
            if dataindex != self.lastit:
                self.routine.onPickItem(dataindex)
                self.lastit = dataindex

    def roiitemchanged(self,current,previous):
        self.roiitemclicked(current)

    def updateUI(self):
        self.listWidget.currentItemChanged.connect(self.roiitemchanged)
