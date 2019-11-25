import logging

from plugins.standard.plugin import Plugin
from structures.roi import LineROI
from structures.sample import Sample
from structures.settings import Settings
from structures.stage import Stage
from structures.transformation import RectangleTransformation, TRANSFORMATION


class StandardTransformation(Plugin):
    def __init__(self):
        super(StandardTransformation,self).__init__()
        logging.info("Standard Transformation initialized")

    def transformROI(self, roi: LineROI, stage: Stage, settings: Settings):
        transformation = self.settings.transformer(roi,stage,settings)
        self.onNewTransformation(transformation)

    def onNewTransformation(self, transformation: TRANSFORMATION):
        raise NotImplementedError