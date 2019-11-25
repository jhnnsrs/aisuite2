import logging

from plugins.standard.plugin import Plugin


class RoiListDisplay(Plugin):
    def __init__(self):
        super(RoiListDisplay, self).__init__()
        logging.info("Roi List Plugin initialized")

        from ui.roilistwidget import RoiListWidget
        self.listWidget = RoiListWidget(self)


    def onDeleteItem(self, index):
        raise NotImplementedError

    def updateList(self):
        self.listWidget.updateList(self.activeSample)

    def onPickItem(self,index):
        raise NotImplementedError


    def onCleanRoiListPushed(self):
        raise NotImplementedError