from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem


class SeriesDialog(QWidget):

    def __init__(self, seriesname, routine, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Series Chooser")
        self.routine = routine
        self.layout = QVBoxLayout()
        self.serieslabel = QLabel("Please select the wanted Series:")
        self.seriesselector = SeriesSelector(seriesname,self.seriesChosen,parent=self)
        self.layout.addWidget(self.serieslabel)
        self.layout.addWidget(self.seriesselector)

        self.setLayout(self.layout)
        self.show()

    def seriesChosen(self,index):
        self.hide()
        self.routine.onSeriesChosen(index)


class SeriesSelector(QListWidget):
    ''' A specialized QListWidget that displays the
        list of all image files in a given directory. '''

    def __init__(self, flows,callback, parent=None):
        QListWidget.__init__(self, parent)
        self.flows = flows
        self.selectedflow = None
        self.callback = callback

        self.setFlows(self.flows)
        self.itemClicked.connect(self.clicked)

    def setFlows(self, flows):
        self._flows = flows
        self._populate()

    def _populate(self):
        ''' Fill the list with images from the
            current directory in self._dirpath. '''

        # In case we're repopulating, clear the list
        self.clear()
        # Create a list item for each flows file,
        # setting the text and icon appropriately
        for flow in self._flows:
            item = QListWidgetItem(self)
            item.setText(flow)
            #item.setIcon(QIcon())

        self.show()

    def clicked(self, item: QListWidgetItem):
        index = int(self.currentIndex().row())
        self.callback(index)