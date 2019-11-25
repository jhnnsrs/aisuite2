import logging
from PyQt5 import QtGui, QtCore

import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMainWindow
from matplotlib import pylab as pl

from plugins.ui.imagedisplay import ImageWidgetPlugin
from structures.stage import Stage
from structures.transformation import RectangleTransformation
from ui.aitoolbar import PanOnlyToolbar
from ui.canvas import MplCanvas


class ImageWidget(QMainWindow):
    def __init__(self, routine: ImageWidgetPlugin):
        super(ImageWidget, self).__init__()
        self.setWindowTitle("BioImageFile")
        self.routine = routine

        self.warninglabel = None
        self.fig = None
        self.ax = None
        self.axesImage = None
        self.transformationpatches = {}
        self.textpatches = {}
        self.base_scale = 1.5
        self.lastpicked = 0
        self.pickcallback = self.routine.onPickItem

        self.imagexlims = [0,1024]
        self.imageylims = [0,1024]
        self.homexlims = [0,1024]
        self.homeylims = [0,1024]


        self.initUI()

    def toggleTransformation(self, index: int):
        logging.info("Toggling Transformation {0}".format(str(index)))
        if index in self.transformationpatches:
            patches = self.transformationpatches[index]
            for patch in patches:
                patch.set_visible(not patch.get_visible())
        else:
            logging.warning("Transformation {0} was not found in Graph".format(str(index)))

        self.updateUI()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()

        if key == QtCore.Qt.Key_Delete:
            self.routine.onPickAndDeleteItem(self.lastpicked)

    def initUI(self):

        self.fig = plt.figure()
        self.canvas = MplCanvas(self.fig)

        self.imageCanvas = self.fig.add_subplot(111)
        self.ax = self.imageCanvas

        self.toolbar = PanOnlyToolbar(self.canvas, self)
        self.setCentralWidget(self.canvas)
        self.addToolBar(Qt.RightToolBarArea, self.toolbar)
        self.fig.tight_layout()

        self.picker = self.fig.canvas.mpl_connect('pick_event', self.onpick)
        #self.zoom = self.fig.canvas.mpl_connect('scroll_event', self.zoom)

        self.show()

    def onHome(self):
        self.ax.set_xlim(self.homexlims)
        self.ax.set_ylim(self.homeylims)
        self.ax.figure.canvas.draw()

    def setLock(self,bool):
        self.routine.setFigLock(bool)

    def updateUI(self):
        self.fig.canvas.update()
        self.canvas.draw()
        self.show()

    def onpick(self, event):
        self.lastpicked = int(event.artist._text)
        self.toggleTransformation(self.lastpicked)
        self.pickcallback(self.lastpicked)
        return True

    def zoom(self, event):
        if event.inaxes != self.ax: return
        if event.xdata == None or event.ydata == None: return #TODO: MIGHT FAULT
        cur_xlim = list(self.ax.get_xlim())
        cur_ylim = list(self.ax.get_ylim())

        cur_xlim[0] = self.imagexlims[0] if cur_xlim[0] < self.imagexlims[0] else cur_xlim[0]
        cur_xlim[1] = self.imagexlims[1] if cur_xlim[1] > self.imagexlims[1] else cur_xlim[1]
        cur_ylim[0] = self.imageylims[0] if cur_ylim[0] < self.imageylims[0] else cur_ylim[0]
        cur_ylim[1] = self.imageylims[1] if cur_ylim[1] > self.imageylims[1] else cur_ylim[1]

        xdata = event.xdata  # get event x location
        ydata = event.ydata  # get event y location

        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1 / self.base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = self.base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        new_width = new_width if new_width < self.imagexlims[1] else self.imagexlims[1]
        new_height = new_height if new_height < self.imageylims[1] else self.imageylims[1]

        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

        self.ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
        self.ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
        self.ax.figure.canvas.draw()

    def displayStage(self, stage: Stage):

        if self.fig: pl.close(self.fig)
        if self.axesImage: pl.cla()
        # Delete maybe existing warning
        if self.warninglabel is not None:
            self.warninglabel.remove()
            self.warninglabel = None

        self.axesImage = self.imageCanvas.imshow(stage.image)
        # self.imageCanvas.axis("off")
        # self.figure.axes.get_xaxis().set_visible(False)
        # self.figure.axes.get_yaxis().set_visible(False)
        self.imagexlims = [0, stage.image.shape[1]]
        self.homexlims = [0,stage.image.shape[1]]
        self.homeylims = [0,stage.image.shape[0]]
        self.imageCanvas.set_xlim(self.imagexlims)
        self.imageylims = [0, stage.image.shape[0]]
        self.imageCanvas.set_ylim(self.imageylims)
        self.setWindowTitle("{0} (Stage {1})".format(self.routine.activeSample.biometa.seriesname, stage.key))
        if stage.istemporary:
            font = {'family': 'sans-serif', 'color': 'white', 'weight': 'bold', 'size': 9}
            self.warninglabel = self.imageCanvas.text(0, 0, "ATTENTION TEMPORARY STAGE. PLEASE ADD BEFORE PROCESSING", fontdict=font)

        self.fig.tight_layout()
        self.updateUI()

        self.routine.onStageDisplayed(stage)

    def displayTransformation(self, transformation: RectangleTransformation):
        thepatches = []
        patches = transformation.getPatches()
        for patch in patches:
            patch = self.imageCanvas.add_patch(patch)
            patch.set_facecolor(transformation.colour)
            patch.set_alpha(0.6)
            thepatches.append(patch)

        middlebox = transformation.boxes[int(len(transformation.boxes) / 2)]
        middleofbox = 0.5 * middlebox[1] + 0.5 * middlebox[3]

        label = transformation.key

        font = {'family': 'sans-serif', 'color': 'black', 'weight': 'bold', 'size': 9}
        bbox = dict(boxstyle="circle,pad=0.2", fc="white", ec="white", lw=2, alpha=0.8)

        text = self.imageCanvas.text(middleofbox[0], middleofbox[1], label, fontdict=font, bbox=bbox, picker=5)

        self.transformationpatches[transformation.key] = thepatches
        self.textpatches[transformation.key] = text

        self.updateUI()

    def deleteTransformation(self, index: int):
        logging.info("Trying to delete Transformation {0}".format(str(index)))
        if index in self.transformationpatches:
            patches = self.transformationpatches[index]
            for patch in patches:
                patch.remove()

            del self.transformationpatches[index]
            self.textpatches[index].remove()
            del self.textpatches[index]
            logging.info("Transformation {0} deleted".format(str(index)))
        else:
            logging.warning("Transformation {0} was not found in Graph".format(str(index)))

        self.updateUI()
        self.routine.onTransformationDeleted(index)

    def deleteAllTransformations(self):
        for key in self.transformationpatches:
            patches = self.transformationpatches[key]
            for patch in patches:
                patch.remove()

            logging.info("ROI {0} deleted".format(str(key)))
            self.routine.onTransformationDeleted(key)

        for key in self.textpatches:
            self.textpatches[key].remove()

        self.transformationpatches = {}
        self.textpatches = {}

        self.updateUI()
