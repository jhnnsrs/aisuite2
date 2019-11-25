import logging
from PyQt5 import QtGui

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QMainWindow, QDockWidget, QAction, QDialog, QPushButton, QStatusBar, QLabel

from ui.roiandstagewidget import RoiAndStageWidget

class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QStatusBar(parent)

    def emit(self, record):
        msg = self.format(record)
        self.widget.showMessage(msg)


class HideableQDockWidget(QDockWidget):


    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.hide()
        a0.ignore()


class GraphSettingsRoiLIstWidget(QMainWindow):

    def __init__(self,routine, toolbox, graph, roilist, stagelist):

        super(GraphSettingsRoiLIstWidget, self).__init__()
        bar = self.menuBar()

        file = bar.addMenu("File")
        file.triggered[QAction].connect(self.openAction)
        about = QAction("About", self)
        file.addAction(about)
        windows = QAction("Show All Windows", self)
        file.addAction(windows)

        self.logTextBox = QPlainTextEditLogger(self)
        # You can format what is printed to text box
        self.logTextBox.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self.logTextBox)
        # You can control the logging level
        logging.getLogger().setLevel(logging.DEBUG)

        self.setStatusBar(self.logTextBox.widget)
        logging.info("Graph Window Started")
        self.graphWidget = graph
        self.toolboxWidget = toolbox
        self.roiandstageList = RoiAndStageWidget(roilist, stagelist)

        self.roidock = HideableQDockWidget("Graph and Flourescence", self)

        self.roidock.setWidget(self.graphWidget)
        self.roidock.setFloating(False)

        self.roilistdock = HideableQDockWidget("Roi- and Stagelist",self)
        self.roilistdock.setWidget(self.roiandstageList)
        self.roilistdock.setFloating(False)


        self.addDockWidget(Qt.RightDockWidgetArea, self.roidock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.roilistdock)

        self.setCentralWidget(self.toolboxWidget)

        self.setWindowTitle(routine.settings.name + routine.settings.version)

        self.show()

    def closing(self,event):
        print(event)

    def openAction(self,action):
        # TODO: ADD ABOUT DIALOG
        logging.info("Pressed Button {0}".format(action.text()))
        if action.text() == "About":
            d = QDialog()
            b1 = QLabel("AISelect V.12", d)
            d.setWindowTitle("About")
            d.setWindowModality(Qt.ApplicationModal)
            d.exec_()
        if action.text() == "Show All Windows":
            logging.info("CALLED")
            self.roilistdock.show()
            self.roidock.show()

