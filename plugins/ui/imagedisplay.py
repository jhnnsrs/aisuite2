import logging

from plugins.standard.plugin import Plugin
from structures.stage import Stage
from structures.transformation import TRANSFORMATION


class ImageWidgetPlugin(Plugin):

    def __init__(self):
        super(ImageWidgetPlugin, self).__init__()
        logging.info("Image Widget Plugin initialized")
        from ui.imagewidget import ImageWidget
        self.imageWidget = ImageWidget(self)

    def displayStage(self, stage: Stage):
        self.imageWidget.displayStage(stage)

    def getAxAndFig(self):
        return self.imageWidget.ax, self.imageWidget.fig

    def deleteTransformation(self,index):
        self.imageWidget.deleteTransformation(index)

    def displayTransformation(self,transformation: TRANSFORMATION):
        self.imageWidget.displayTransformation(transformation)

    def onStageDisplayed(self,stage: Stage):
        pass

    def onPickItem(self, item):
        raise NotImplementedError

    def onTransformationDeleted(self, index):
        pass

    def onPickAndDeleteItem(self, lastit):
        raise NotImplementedError

    def deleteAllTransformations(self):
        self.imageWidget.deleteAllTransformations()

    def setFigLock(self, bool):
        raise NotImplementedError
