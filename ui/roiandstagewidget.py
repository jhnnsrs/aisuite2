import logging
from PyQt5 import QtGui

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout


class RoiAndStageWidget(QWidget):
    def __init__(self,roilist,stagelist):
        super(RoiAndStageWidget, self).__init__()

        self.layout = QVBoxLayout(self)

        self.stagelistwidget= stagelist
        self.roilistwidget = roilist

        self.layout.addWidget(self.stagelistwidget)
        self.layout.addWidget(self.roilistwidget)

        self.setLayout(self.layout)

        logging.info("Roi and Stage Window Started")

        self.start()

    def start(self):
        self.show()


