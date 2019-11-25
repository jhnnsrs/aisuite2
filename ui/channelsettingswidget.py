import logging

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QTableView, QHeaderView, QPushButton, QAbstractItemView

from plugins.ui.toolbox import StandardToolbox
from ui.tableview import TableView


class ChannelTableModel(QtCore.QAbstractTableModel):
    def __init__(self, model, *args):
        super(ChannelTableModel, self).__init__()
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

    def setData(self, index, value, role):
        self.datatable[index.row()][index.column()] = value
        return True

    def thisItem(self,row,column,value):
        self.datatable[row][column] = value

    def flags(self, index):
        if index.column() == 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


class MappingSettingsGroup(QGroupBox):
    def __init__(self, name, routine: StandardToolbox):
        super().__init__(name)
        self.model = None
        self.channels_model = None
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

        logging.info("Stage Settings reseted")

        del self.channels_model

        self.initUI()

    def initUI(self):

        self.channels_table = QTableView()

        self.reloadbutton = QPushButton("Remap")
        self.reloadbutton.clicked.connect(self.reload)  # needs to Preprocessed before routine is called


        # TODO: Make Readeable Headers
        self.layout.addWidget(self.channels_table)
        self.layout.addWidget(self.reloadbutton)
        print("RESETTING")
        self.model = self.calculateModel()
        self.channels_model = ChannelTableModel(self.model)
        self.channels_table.setModel(self.channels_model)

        self.channels_table.verticalHeader().setVisible(False)
        header = self.channels_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        self.channels_table.doubleClicked.connect(self.itemdoubleclicked)

        self.setLayout(self.layout)
        self.channels_table.reset()

    def calculateModel(self):
        model = []
        for index, (channel, colouredstructure, channelname) in enumerate(
                zip(self.routine.settings.mapping_channels, self.routine.settings.mapping_colouredstructure,
                    self.routine.settings.channelnames)):
            rvalue = "R" if index in self.routine.settings.rmapping[0] else ""
            gvalue = "G" if index in self.routine.settings.gmapping[0] else ""
            bvalue = "B" if index in self.routine.settings.bmapping[0] else ""
            model.append([channelname, colouredstructure, rvalue, gvalue, bvalue])

        return model

    def itemdoubleclicked(self, titem):
        row = titem.row()
        column = titem.column()
        if column == 1:
            return
        item = self.model[titem.row()][titem.column()]
        if column == 2:
            if item == "R":
                self.model[titem.row()][column] = ""
            else:
                self.model[titem.row()][column] = "R"
        if column == 3:
            if item == "G":
                self.model[titem.row()][column] = ""
            else:
                self.model[titem.row()][column] = "G"
        if column == 4:
            if item == "B":
                self.model[titem.row()][column] = ""
            else:
                self.model[titem.row()][column] = "B"


        self.channels_model.update(self.model)
        self.channels_table.reset()


    def reload(self, event):

        self.routine.settings.mapping_colouredstructure = []
        self.routine.settings.mapped_channelnames = []
        self.routine.settings.rmapping[0] = []
        self.routine.settings.gmapping[0] = []
        self.routine.settings.bmapping[0] = []
        self.routine.settings.rmapping[1] = []
        self.routine.settings.gmapping[1] = []
        self.routine.settings.bmapping[1] = []

        for channel, row in enumerate(self.model):
            isr = row[2] == "R"
            isg = row[3] == "G"
            isb = row[4] == "B"
            channelname = row[0]
            structure = row[1]
            self.routine.settings.mapping_colouredstructure.append(structure)
            if isr:
                self.routine.settings.rmapping[0].append(int(channel))
                self.routine.settings.rmapping[1].append(int(channel))
            if isg:
                self.routine.settings.gmapping[0].append(int(channel))
                self.routine.settings.gmapping[1].append(int(channel))
            if isb:
                self.routine.settings.bmapping[0].append(int(channel))
                self.routine.settings.bmapping[1].append(int(channel))


        logging.info("RMAPPING:" + str(self.routine.settings.rmapping))
        logging.info("GMAPPING:" + str(self.routine.settings.gmapping))
        logging.info("BMAPPING:" + str(self.routine.settings.bmapping))
        logging.info("COLOURED-STRUCTURES:" + str(self.routine.settings.mapping_colouredstructure))

        self.routine.mappingsChanged()
        self.routine.requestReMap()
