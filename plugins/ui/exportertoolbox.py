from plugins.standard.plugin import Plugin


class ExporterToolbox(Plugin):
    def __init__(self):
        super(ExporterToolbox, self).__init__()
        from ui.expotertoolboxwidget import ExpoterToolboxWidget

        self.exportableH5Files = []
        self.exportableDataKeys = []
        self.saveSingleFile = True
        self.toolboxwidget = ExpoterToolboxWidget(self)

    def setSaveSingleFile(self,value):
        self.saveSingleFile = value

    def setH5FilesWidgetFromAvailable(self,h5filelist):
        self.toolboxwidget.resetH5FilesList(h5filelist)

    def setDataListWidgetFromAvailable(self, dataparams):
        self.toolboxwidget.resetDataList(dataparams)

    def onExportableH5FilesChanged(self):
        raise NotImplementedError

    def onExportableDataKeysChanged(self):
        raise NotImplementedError

    def onH5FileChanged(self, filepath):
        raise NotImplementedError

    def onDirectoryChanged(self, filepath):
        raise NotImplementedError

    def startExport(self):
        raise NotImplementedError
