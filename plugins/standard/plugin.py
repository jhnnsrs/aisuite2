import logging

import numpy as np

from standardlibs.randcolours import rand_cmap
from structures.roi import ROI
from structures.sample import Sample
from structures.settings import Settings
from structures.stage import Stage


class Plugin:
    def __init__(self):

        super(Plugin, self).__init__()
        logging.info("Plugin initialized")

        self.colours = iter((rand_cmap(200,first_color_black=False)(np.linspace(0, 1, 200))))
        self.roiindex = iter(list(range(100)))
        self.stageindex = iter(list(range(100)))
        self.settings = Settings()
        self.activeSample = Sample()
        self.standardErrorRaiser = None

    def setStandardErrorRaiser(self, widget):
        self.standardErrorRaiser = widget

    def raiseError(self,errormsg,widget = None):
        raiser = widget if widget else self.standardErrorRaiser
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.about(raiser, "Error", errormsg)


    def resetRoiIndicesAndColours(self):
        self.colours = iter((rand_cmap(200,first_color_black=False)(np.linspace(0, 1, 200))))
        self.roiindex = iter(list(range(200)))

    def resetStageIndices(self):
        self.stageindex = iter(list(range(200)))

    def getStageIndices(self):
        return self.stageindex

    def getRoiIndices(self):
        return self.roiindex

    def getColourCodes(self):
        return self.colours

    def getSettings(self):
        return self.settings


