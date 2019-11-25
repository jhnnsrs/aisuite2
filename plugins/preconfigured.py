import logging

from plugins.roibuilder.linebuilder import LineRoiBuilderPlugin
from plugins.ui.datadisplay import StandardDataDisplay, VolumetricDataDisplay
from plugins.ui.imagedisplay import ImageWidgetPlugin
from plugins.ui.roilist import RoiListDisplay
from plugins.ui.stagelist import StageListDisplay
from plugins.ui.toolbox import StandardToolbox
from ui.graphsettingsroilistwidget import GraphSettingsRoiLIstWidget


class MainViewPlugin(StandardToolbox, StandardDataDisplay, RoiListDisplay, StageListDisplay):

    def __init__(self):
        super(MainViewPlugin, self).__init__()

        logging.info("MainViewPlugin initialized")
        self.graphandsettingswidget = GraphSettingsRoiLIstWidget(self, self.toolbox, self.dataWidget, self.listWidget,
                                                                 self.stageListWidget)

    def resetMainView(self):
        self.resetStandardToolbox()

class AugmentedViewPlugin(StandardToolbox, VolumetricDataDisplay, RoiListDisplay, StageListDisplay):

    def __init__(self):
        super(AugmentedViewPlugin, self).__init__()

        logging.info("MainViewPlugin initialized")
        self.graphandsettingswidget = GraphSettingsRoiLIstWidget(self, self.toolbox, self.dataWidget, self.listWidget,
                                                                 self.stageListWidget)

    def resetMainView(self):
        self.resetStandardToolbox()



class StandardViewPluginRoi(LineRoiBuilderPlugin, ImageWidgetPlugin):
    def __init__(self):
        super(StandardViewPluginRoi, self).__init__()
        logging.info("Standard View Plugin initialized")
