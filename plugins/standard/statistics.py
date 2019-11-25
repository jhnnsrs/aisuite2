import logging

from plugins.standard.plugin import Plugin
from structures.settings import Settings


class StatisticsPlugin(Plugin):

    def __init__(self):
        super(StatisticsPlugin,self).__init__()
        logging.info("Statistics Plugin initialized")
        # TODO: Implement always increasing the era rois for total statistics
        self.era_rois = 0
