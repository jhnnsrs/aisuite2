import logging

from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QLineEdit, QPushButton

from plugins.ui.toolbox import StandardToolbox
from structures.settings import Settings
from ui.selectors import PostProcessSelector, ProjectionsSelector, ChannelSelector


class PictureSettingsGroup(QGroupBox):

    def __init__(self,name, routine: StandardToolbox):
        super().__init__(name)
        self.routine = routine
        self.settings = routine.settings

        self.layout  = QGridLayout()
        self.initUI()

    def reset(self):
        for i in reversed(range(self.layout.count())):
            widgetToRemove = self.layout.itemAt(i).widget()
            # remove it from the layout list
            self.layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

        logging.info("Picture Settings reseted")

        self.initUI()

    def initUI(self):

        self.flagslabel = QLabel("Flags")
        self.flagstext = QLineEdit(self)


        self.postprocess_label = QLabel("Post-Processing")
        self.postprocess_select = PostProcessSelector(self.routine,self.routine.postProcessedChanged)


        self.projection_label = QLabel("Projection")
        self.projection_select = ProjectionsSelector(self.routine,self.routine.projectionChanged)

        self.selective_label = QLabel("Selective-Channel")
        self.selective_select = ChannelSelector(self.routine,self.routine.onSelectiveChannelChanged)

        self.layout.addWidget(self.flagslabel, 0, 0)
        self.layout.addWidget(self.flagstext, 0, 1)

        self.layout.addWidget(self.projection_label, 1, 0)
        self.layout.addWidget(self.projection_select, 1, 1)

        self.layout.addWidget(self.postprocess_label, 2, 0)
        self.layout.addWidget(self.postprocess_select, 2, 1)

        self.layout.addWidget(self.selective_label, 3, 0)
        self.layout.addWidget(self.selective_select, 3, 1)

        self.setLayout(self.layout)