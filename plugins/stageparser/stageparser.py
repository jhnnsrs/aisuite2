import logging

import copy

from plugins.standard.plugin import Plugin
from structures.settings import Settings
from structures.stage import Stage


class StageParserPlugin(Plugin):

    def __init__(self):
        super(StageParserPlugin,self).__init__()
        logging.info("Stage Parser Plugin initialized")
        self.stageCount = 0
        self.displayedStage = Stage()
        self.temporaryStage = Stage()
        self.dataStage = Stage()

        self._mapped = None
        self._bioimage = None
        self._postprocessed = None
        self._projection = None

    def loadPrimaryStage(self):
        self._bioimage = self.activeSample.bioimage.file
        logging.info("Returned Bioimage {0}".format(str(self._bioimage.shape)))
        self.calculateStage()

        key = self.addTemporaryStageToStack()
        self.setStageAsDataStage(key)
        self.setStageAsDisplayStage(key)
        #Should be called in order for programm to Parse First Stage so user input is minimised


    def calculateStageAfterMapping(self):
        if self.checkState() is False: return
        logging.info("Calculating Stage (Skipping Mapping)")

        self.doProjection()
        self.doPostProcess()

        self.changeTemporaryStage()

    def calculateStageAfterProjection(self):
        if self.checkState() is False: return
        logging.info("Calculating Stage (Skipping Mapping and Projection")
        self.doPostProcess()


        self.changeTemporaryStage()

    def checkState(self):

        if self._bioimage is None: return False
        try:
            nana = self._bioimage.shape
            return True
        except:
            return False


    def calculateStage(self):
        if self.checkState() is False: return
        logging.info("Calculating Stage")
        self.doMap()
        self.doProjection()
        self.doPostProcess()

        self.changeTemporaryStage()

    def changeTemporaryStage(self):

        self.temporaryStage.image = self._postprocessed
        info = dict(self._postprocessedstageinfo)
        info.update(self._mappedstageinfo)
        info.update(self._projectionstageinfo)
        self.temporaryStage.info = info
        self.temporaryStage.istemporary = True
        self.temporaryStage.isdata = False
        self.temporaryStage.isdisplay = False

        self.onTemporaryStageChanged(self.temporaryStage)

    def setStageAsDataStage(self,index):

        logging.info("Setting Stage {0} as Data Stage".format(str(index)))
        for key in self.activeSample.stages:
            #Setting every other False
            self.activeSample.stages[key].isdata = False
        self.activeSample.stages[index].isdata = True
        self.dataStage = self.activeSample.stages[index]
        self.onDataStageChanged(self.activeSample.stages[index])
        self.onStageListChanged()

    def setStageAsDisplayStage(self,index):
        logging.info("Setting Stage {0} as Display Stage".format(str(index)))
        for key in self.activeSample.stages:
            #Setting every other False
            self.activeSample.stages[key].isdisplay = False
        self.activeSample.stages[index].isdisplay = True
        self.displayedStage = self.activeSample.stages[index]
        self.onDisplayStageChanged(self.activeSample.stages[index])
        self.onStageListChanged()

    def onTemporaryStageChanged(self,stage: Stage):
        pass

    def onDisplayStageChanged(self,stage: Stage):
        pass

    def onDataStageChanged(self,stage: Stage):
        pass


    def addTemporaryStageToStack(self):
        key = next(self.getStageIndices())
        logging.info("Stage {0} added to Stack".format(str(key)))
        self.activeSample.stages[key] = copy.deepcopy(self.temporaryStage) #TODO: DEEPCOPY BITCHES
        self.activeSample.stages[key].istemporary = False
        self.activeSample.stages[key].key = key
        self.activeSample.stages[key].name = "Stage {0}".format(key)
        self.setStageAsDisplayStage(key)
        self.onStageListChanged()
        return key

    def doPostProcess(self):
        self._postprocessed, self._postprocessedstageinfo = self.settings.postprocess(self._projection, self.settings)
        logging.info("PostProcessing Done" + str(self._postprocessedstageinfo))
        logging.info("Returned Postprocessedshape {0}".format(str(self._postprocessed.shape)))
        self.onPostProcessedLoaded(self._postprocessed)

    def doMap(self):
        self._mapped, self._mappedstageinfo = self.settings.mapping(self._bioimage, self.settings)
        logging.info("Mapping Done" + str(self._mappedstageinfo))
        logging.info("Returned Mappingshape {0}".format(str(self._mapped.shape)))
        self.onMappedLoaded(self._mapped)

    def doProjection(self):
        self._projection, self._projectionstageinfo = self.settings.projection(self._mapped, self.settings)
        logging.info("Projection" + str(self._projectionstageinfo))
        logging.info("Returned Projection {0}".format(str(self._projection.shape)))
        self.onProjectionLoaded(self._projection)

    def resetStageCount(self):
        self.stageCount = 0

    def onMappedLoaded(self, mapped):
        pass

    def onProjectionLoaded(self, projecion):
        pass

    def onPostProcessedLoaded(self, postprocessed):
        pass

    def cleanStages(self):
        self.activeSample.stages = {}
        self.onStageListChanged()

    def getActiveStage(self):

        return self.activeSample


    def onStageListChanged(self):
        raise NotImplementedError
