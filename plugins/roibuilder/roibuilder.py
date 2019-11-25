import logging

from plugins.standard.plugin import Plugin
from structures.roi import ROI
from ui.linebuilder import RoiBuilder


class RoiBuilderPlugin(Plugin):
    def __init__(self):
        super(RoiBuilderPlugin, self).__init__()
        logging.info("RoiBuilderPlugin initialized")



    def onRoiAdded(self, roi: ROI):
        '''Gets called when new ROI is Added'''
        raise NotImplementedError
