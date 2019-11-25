import logging

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QTableView, QHeaderView, QPushButton

from plugins.ui.stagelist import StageListDisplay


class StageTableModel(QtCore.QAbstractTableModel):
    def __init__(self, model, *args):
        super(StageTableModel, self).__init__()
        self.datatable = model

    def update(self, dataIn):
        self.datatable = dataIn

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable[0])

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            i = index.row()
            j = index.column()
            return '{0}'.format(self.datatable[i][j])
        else:
            return QtCore.QVariant()

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled


class StageListWidget(QGroupBox):
    def __init__(self, routine: StageListDisplay):
        super().__init__("StageList")
        logging.info("StageList Widget initialized")
        self.data_label = "Data"
        self.routine = routine
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)


        self.stages_table = QTableView()

        self.reloadbutton = QPushButton("Clean Stages")
        self.reloadbutton.clicked.connect(self.reload)  # needs to Preprocessed before routine is called

        self.setLayout(self.layout)


        # TODO: Spell out labels
        self.layout.addWidget(self.stages_table)
        self.layout.addWidget(self.reloadbutton)

        self.setLayout(self.layout)

    def reset(self):
        self.model = self.calculateModel()
        self.stages_model = StageTableModel(self.model)
        self.stages_table.setModel(self.stages_model)

        self.stages_table.verticalHeader().setVisible(False)
        header = self.stages_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        self.stages_table.doubleClicked.connect(self.itemdoubleclicked)

        self.stages_table.clicked.connect(self.currentChanged)


    def calculateModel(self):
        model = []
        somethingadded = False
        for key, stage in self.routine.activeSample.stages.items():
            isdata = self.data_label if stage.isdata else ""
            model.append([key, "Stage {0}".format(str(key)), isdata])
            somethingadded = True
        if not somethingadded:
            model.append(["N", "Void Stage", "D"])

        return model

    def currentChanged(self, item):
        if item.column() == 0 or item.column() == 1:
            key = self.model[item.row()][0]

            if str(key) != "N":
                self.routine.onRequestDisplayStage(key)

    def itemdoubleclicked(self, item):
        row = item.row()
        column = item.column()
        logging.info("Double Clicked")
        if column == 2:

            logging.info("Double 2 Clicked")
            if item.data() != self.data_label:
                key = self.model[item.row()][0]
                if str(key) != "N":
                    logging.info("Request Data Stage Change")
                    self.routine.onRequestDataStage(key)

        self.stages_table.reset()

    def reload(self, event):
        logging.info("Stage Selection was called")
        self.routine.onRequestStageClean()
