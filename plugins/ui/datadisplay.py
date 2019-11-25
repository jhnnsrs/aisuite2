import logging

from plugins.standard.plugin import Plugin
from structures.roidata import DATA, DummyData


class StandardDataDisplay(Plugin):
    def __init__(self):
        super(StandardDataDisplay, self).__init__()
        logging.info("Standard Data Display initialized")
        from ui.graphwidget import GraphWidget
        self.dataWidget = GraphWidget(self)

    def displayData(self, data: DATA):
        if isinstance(data, DummyData):
            self.dataWidget.displayDummy()
        else:
            self.dataWidget.displayData(data)

    def onDataUpdate(self, data: DATA):
        raise NotImplementedError


class VolumetricDataDisplay(Plugin):

    def __init__(self):
        super(VolumetricDataDisplay, self).__init__()
        logging.info("Volumetric Data Display initialized")
        from ui.graphwidget import VolumetricGraphWidget
        self.dataWidget = VolumetricGraphWidget(self)

    def displayData(self, data: DATA):
        if isinstance(data, DummyData):
            self.dataWidget.displayDummy()
        else:
            self.dataWidget.displayData(data)

    def processData(self,data,segments,threshold):
        from logic.calculators import reprocessAIS
        data = reprocessAIS(data,segments,threshold)
        return data

    def onDataUpdate(self, data: DATA):
        raise NotImplementedError