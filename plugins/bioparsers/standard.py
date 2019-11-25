import logging

from plugins.standard.plugin import Plugin
from structures.settings import Settings


class StandardBioParser(Plugin):
    def __init__(self):
        # should load Sample and First
        super(StandardBioParser, self).__init__()

        logging.info("Standard Bio Parser initialized")

    def loadSeriesFromFile(self,filepath,force=False):
        from logic.bioparser import getSeriesNamesFromFile
        # first show different options for Series
        try:
            seriesnames = getSeriesNamesFromFile(filepath)
        except Exception as e:
            self.raiseError("Please select a valid BioImageFile: Error {0}".format(str(e)))
            return
        if len(seriesnames)> 1 or force:
            self.onChooseSeries(seriesnames)
        else:
            self.loadSampleFromFile(filepath,0)


    def loadSampleFromFile(self, filepath, series):
        from logic.bioparser import loadSeriesFromFile as load
        biometa, bioimage = load(filepath, series)
        self.activeSample.bioimage = bioimage
        self.activeSample.biometa = biometa
        self.onBioMetaLoaded(biometa)
        self.onBioImageLoaded(bioimage)



    def onBioMetaLoaded(self, biometa):
        self.settings.seriesname = self.activeSample.biometa.seriesname
        self.settings.channelnames = self.activeSample.biometa.channellist
        self.settings.startstack = 0
        self.settings.endstack = self.activeSample.biometa.sizez
        self.settings.startstage = self.settings.startstack if self.settings.startstage == 0 or self.settings.startstage >= self.settings.endstage else self.settings.startstage
        self.settings.endstage = self.settings.endstack if self.settings.endstage == 0 or self.settings.startstage >= self.settings.endstage else self.settings.endstage
        self.onFileSettingsLoaded()
        pass

    def onChooseSeries(self,seriesnames):
        raise NotImplementedError

    def onBioImageLoaded(self, bioimage):
        pass

    def onFileSettingsLoaded(self):
        raise NotImplementedError
