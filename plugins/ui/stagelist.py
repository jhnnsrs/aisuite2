import logging

from plugins.standard.plugin import Plugin


class StageListDisplay(Plugin):
    def __init__(self):
        super(StageListDisplay, self).__init__()
        logging.info("Stage List Plugin initialized")
        from ui.stagelistwidget import StageListWidget
        self.stageListWidget = StageListWidget(self)

    def stageListPlugin_reset(self):
        self.stageListWidget.reset()

    def onRequestStageClean(self):
        raise NotImplementedError

    def onRequestDataStage(self, key):
        raise NotImplementedError

    def onRequestDisplayStage(self, key):
        raise NotImplementedError
