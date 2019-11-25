import logging

from plugins.roibuilder.roibuilder import RoiBuilderPlugin
from structures.roi import LineROI, ROI
from ui.linebuilder import LineBuilder


class LineRoiBuilderPlugin(RoiBuilderPlugin):
    def __init__(self):
        super(LineRoiBuilderPlugin, self).__init__()

        logging.info("LineRoiBuilder initialized")
        # LineBuilder has callbacks for addLines and onPick set
        self.roiBuilder = LineBuilder(self)

    def LineRoiBuilder_initialize(self, ax, fig):
        self.roiBuilder.initialize(ax=ax, fig=fig)

    def addLines(self, lines):
        roi = LineROI()
        roi.key= next(self.getRoiIndices())
        roi.colour = next(self.getColourCodes())
        roi.vertices = lines
        self.onRoiAdded(roi)

    def onPick(self, index):
        pass

    def setLock(self,lock):
        self.roiBuilder.locked = lock

