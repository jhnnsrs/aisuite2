from plugins.standard.plugin import Plugin


class StandardH5Reader(Plugin):

    def __init__(self):
        super(StandardH5Reader,self).__init__()
        self.h5file = None


    def readSampleFromH5File(self,filepath):
        from logic.io import loadSampleFromHDF
        loadedSample = loadSampleFromHDF(filepath,self.settings)

        self.onSampleLoadedFromFile(loadedSample)

    def onSampleLoadedFromFile(self, loadedSample):
        raise NotImplementedError

