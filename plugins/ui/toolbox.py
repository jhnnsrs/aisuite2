import logging

from plugins.standard.plugin import Plugin
from structures.settings import Settings


class StandardToolbox(Plugin):
    def __init__(self):
        super(StandardToolbox, self).__init__()
        logging.info("Standard Toolbox Plugin initialized")
        from ui.toolboxwidget import ToolboxWidget
        self.toolbox = ToolboxWidget(self)

    def aisChannelChanged(self, value):
        self.settings.aischannel = value

    def resetStandardToolbox(self):

        self.toolbox.mappingsReset()
        self.toolbox.reset()

    def onSelectiveChannelChanged(self,channel):
        self.settings.selectiveChannel = channel
        self.onPostProcessedFunctionChanged()

    def postProcessedChanged(self, postprocessed):
        self.settings.postprocess = postprocessed
        self.onPostProcessedFunctionChanged()

    def projectionChanged(self, projection):
        self.settings.projection = projection
        self.onProjectionFunctionChanged()

    def onFilepathChanged(self, filepath):
        raise  NotImplementedError

    def onLoadSettings(self,filepath):
        raise NotImplementedError

    def onSaveSettings(self,filepath):
        raise NotImplementedError

    def mappingsChanged(self):
        logging.info("Maps changed called")
        self.toolbox.mappingsReset()
        self.onMappingsChanged()

    def onSettingsUpdate(self):
        self.toolbox.mappingsReset()
        self.toolbox.reset()

    def onMappingsChanged(self):
        pass

    def onPostProcessedFunctionChanged(self):
        raise NotImplementedError

    def onProjectionFunctionChanged(self):
        raise NotImplementedError

    def thresholdChanged(self, value):
        self.settings.threshold = float(value/100)

    def onDoneWithFile(self):
        raise NotImplementedError

    def onAddStagePressed(self):
        raise NotImplementedError

    def onRequestDisplayStage(self, key):
        raise NotImplementedError

    def onRequestDataStage(self, key):
        raise NotImplementedError

    def onRequestReMap(self):
        raise NotImplementedError

    def onStageSettingsChanged(self):
        self.onProjectionFunctionChanged()

    def onRequestSettingsSave(self,filepath):
        raise NotImplementedError

    def requestReMap(self):
        self.onSettingsUpdate()
        self.onRequestReMap()
        pass

    def onSeriesChanged(self):
        raise NotImplementedError

    def scalechanged(self, value):
        self.settings.scale = int(value)
        pass