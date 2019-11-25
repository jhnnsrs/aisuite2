import logging
import os

from plugins.bioparsers.standard import StandardBioParser
from plugins.calculators.standardcalculatorplugin import StandardCalculation
from plugins.excelexporter.excelexporter import ExcelExporter
from plugins.preconfigured import MainViewPlugin, StandardViewPluginRoi, AugmentedViewPlugin
from plugins.stageparser.stageparser import StageParserPlugin
from plugins.standard.h5filestorage import H5FilesStorage
from plugins.standard.samplestorage import SampleStorage
from plugins.standard.settings import StandardSettings
from plugins.standard.standardh5reader import StandardH5Reader
from plugins.transformers.linetorectangle import StandardTransformation
from plugins.ui.datadisplay import StandardDataDisplay
from plugins.ui.exportertoolbox import ExporterToolbox
from plugins.ui.funplugin import FunPlugin
from plugins.ui.imagedisplay import ImageWidgetPlugin
from plugins.ui.roilist import RoiListDisplay
from plugins.ui.stagelist import StageListDisplay
from structures.roidata import DATA
from structures.stage import Stage
from ui.serieschooser import SeriesDialog


class AISelect(StandardBioParser, StandardViewPluginRoi, StandardSettings, MainViewPlugin, StandardTransformation,
               StandardCalculation, SampleStorage, FunPlugin, StageParserPlugin):

    def onSeriesChosen(self,series):
        self.loadSampleFromFile(self.settings.filepath,series)

    def onChooseSeries(self, seriesnames):
        self.seriesChooser = SeriesDialog(seriesnames, self)

    def setFigLock(self, bool):
        self.setLock(bool)

    def onRequestSettingsSave(self,filepath):
        self.saveBioImageSettings(filepath)

    def onRequestReMap(self):
        self.calculateStage()

    def onRequestStageClean(self):
        self.cleanStages()
        self.resetStageIndices()

    def onCleanRoiListPushed(self):
        self.cleanDataRoiTransformation()
        self.deleteAllTransformations()
        self.resetRoiIndicesAndColours()

    def onRequestDisplayStage(self, key):
        self.setStageAsDisplayStage(key)

    def onRequestDataStage(self,key):
        self.setStageAsDataStage(key)

    def onDisplayStageChanged(self, stagela: Stage):
        self.displayStage(stagela)

    def onStageListChanged(self):
        self.stageListPlugin_reset()

    def onAddStagePressed(self):
        self.addTemporaryStageToStack()

    def onTemporaryStageChanged(self, stagechen: Stage):
        self.displayStage(stagechen)

    def onCleanSamplePushed(self):
        self.cleanDataRoiTransformation()

    def onLoadSettings(self, filepath):
        pass

    def onDoneWithFile(self):
        self.saveSampleToHDF()

    def onSaveSettings(self, filepath):
        pass

    def onFileSettingsLoaded(self):
        self.resetMainView()


    def onProjectionFunctionChanged(self):
        self.calculateStageAfterMapping()

    def onPostProcessedFunctionChanged(self):
        self.calculateStageAfterProjection()

    def onDataUpdate(self, data: DATA):
        self.updateData(data)

    def onPickAndDeleteItem(self, lastit):
        self.popAll(lastit)
        self.deleteTransformation(lastit)

    def onPickItem(self, index):
        self.displayData(self.activeSample.data[index])

    def onDeleteItem(self, index):
        self.imageWidget.deleteTransformation(index)
        self.popAll(index)

    def onSampleChanged(self):
        self.updateList()

    def onDataCalculated(self, data):
        self.displayData(data)
        self.addData(data)

    def onNewTransformation(self, transformation):
        self.displayTransformation(transformation)
        self.calculateFromTransformation(transformation)
        self.addTransformation(transformation)

    def __init__(self):
        super(AISelect, self).__init__()
        self.theroutine()
        self.image = None

    def theroutine(self):
        #Settings need to be loaded
        self.loadSettingsFromFile("settings.ini")

        #ROIBuilder needs to be initialized
        ax, fig = self.getAxAndFig()
        self.LineRoiBuilder_initialize(ax=ax,fig=fig)


    def onRoiAdded(self, roi):
        self.transformROI(roi, self.dataStage, self.settings)
        self.addRoi(roi)
        pass

    def setUIfromSettings(self, settings):
        super().setUIFromSettings(settings)

    def onFilepathChanged(self, filepath):

        # Clean Up everything from last Sample
        self.cleanDataRoiTransformation()
        self.cleanStages()
        self.deleteAllTransformations()
        self.resetRoiIndicesAndColours()
        self.resetStageIndices()

        # load File Specific Settings
        self.settings.directory = os.path.dirname(filepath)
        self.settings.filename = os.path.basename(filepath)
        self.settings.filepath = filepath


        self.loadBioImageSettings()
        self.loadSeriesFromFile(self.settings.filepath)



    def onSeriesChanged(self):
        # Clean Up everything from last Sample
        self.cleanDataRoiTransformation()
        self.cleanStages()
        self.deleteAllTransformations()
        self.resetRoiIndicesAndColours()
        self.resetStageIndices()

        if self.settings.filepath == "":
            self.raiseError("Please select a BioImageFile First")
            return

        self.loadBioImageSettings()
        self.loadSeriesFromFile(self.settings.filepath,force=True)

    def onBioImageLoaded(self, bioimage):
        self.loadPrimaryStage()


    def onClose(self):
        pass


class AIViewer(SampleStorage, ImageWidgetPlugin, StandardDataDisplay, StageListDisplay, RoiListDisplay,
               StandardH5Reader, ExporterToolbox, StageParserPlugin, ExcelExporter, H5FilesStorage):

    def startExport(self):
        logging.info("Requesting Exporting of File List")
        if self.saveSingleFile:
            self.exportAccumulatedH5Files()
        else:
            self.exportSingleH5Files()

    def onDataKeysChanged(self):
        self.exportableDataKeys = self.availableDataKeys
        self.plannedDataKeys = self.exportableDataKeys
        self.setDataListWidgetFromAvailable(self.exportableDataKeys)


    def onH5FilesListChanged(self):
        self.exportableH5Files = self.availableH5Files
        self.plannedH5Files = self.exportableH5Files
        self.setH5FilesWidgetFromAvailable(self.exportableH5Files)

    def onSampleListChanged(self):
        pass

    def onStageListChanged(self):
        pass

    def onExportableDataKeysChanged(self):
        self.plannedDataKeys = self.exportableDataKeys

    def onDirectoryChanged(self, filepath):
        logging.info("Loading H5Files from Directory: {0}".format(filepath))
        self.loadH5FilesFromDirectory(filepath)

    def onExportableH5FilesChanged(self):
        logging.info("Setting Exporting files to {0}".format(self.exportableH5Files))
        self.plannedH5Files = self.exportableH5Files

    def __init__(self):
        super(AIViewer,self).__init__()
        self.startUp()

    def onH5FileChanged(self, filepath):
        self.readSampleFromH5File(filepath)

    def onSampleLoadedFromFile(self, loadedSample):
        self.setSample(loadedSample)

    def onRequestStageClean(self):
        self.cleanStages()
        self.resetStageIndices()

    def onCleanRoiListPushed(self):
        self.cleanDataRoiTransformation()
        self.deleteAllTransformations()
        self.resetRoiIndicesAndColours()

    def onRequestDisplayStage(self, key):
        self.setStageAsDisplayStage(key)

    def onRequestDataStage(self,key):
        self.setStageAsDataStage(key)

    def onDataUpdate(self, data: DATA):
        self.updateData(data)

    def onPickAndDeleteItem(self, lastit):
        self.popAll(lastit)
        self.deleteTransformation(lastit)

    def onPickItem(self, index):
        self.displayData(self.activeSample.data[index])

    def onDeleteItem(self, index):
        self.imageWidget.deleteTransformation(index)
        self.popAll(index)

    def onSampleChanged(self):
        self.updateList()

    def onClose(self):
        pass


class AIExporter(ExporterToolbox, ExcelExporter, H5FilesStorage):

    def startExport(self):

        logging.info("Requesting Exporting of File List")
        if self.saveSingleFile:
            self.exportAccumulatedH5Files()
        else:
            self.exportSingleH5Files()

    def onDataKeysChanged(self):
        self.exportableDataKeys = self.availableDataKeys
        self.plannedDataKeys = self.exportableDataKeys
        self.setDataListWidgetFromAvailable(self.exportableDataKeys)

    def onH5FileChanged(self, filepath):
        self.exportableH5Files = self.availableH5Files
        self.plannedH5Files = self.exportableH5Files
        print(self.exportableH5Files)
        self.setH5FilesWidgetFromAvailable(self.exportableH5Files)

    def onExportableDataKeysChanged(self):
        self.plannedDataKeys = self.exportableDataKeys

    def onDirectoryChanged(self, filepath):
        logging.info("Loading H5Files from Directory: {0}".format(filepath))
        self.loadH5FilesFromDirectory(filepath)

    def onH5FilesListChanged(self):
        self.exportableH5Files = self.availableH5Files
        self.plannedH5Files = self.exportableH5Files
        self.setH5FilesWidgetFromAvailable(self.exportableH5Files)

    def __init__(self):
        super(AIExporter,self).__init__()
        self.startUp()


    def startUp(self):
        pass

    def onSampleListChanged(self):
        pass

    def onExportableH5FilesChanged(self):
        logging.info("Setting Exporting files to {0}".format(self.exportableH5Files))
        self.plannedH5Files = self.exportableH5Files


class AISelectAndVolume(StandardBioParser, StandardViewPluginRoi, StandardSettings, AugmentedViewPlugin, StandardTransformation,
               StandardCalculation, SampleStorage, FunPlugin, StageParserPlugin):

    def onSeriesChosen(self,series):
        self.loadSampleFromFile(self.settings.filepath,series)

    def onChooseSeries(self, seriesnames):
        self.seriesChooser = SeriesDialog(seriesnames, self)

    def setFigLock(self, bool):
        self.setLock(bool)

    def onRequestSettingsSave(self,filepath):
        self.saveBioImageSettings(filepath)

    def onRequestReMap(self):
        self.calculateStage()

    def onRequestStageClean(self):
        self.cleanStages()
        self.resetStageIndices()

    def onCleanRoiListPushed(self):
        self.cleanDataRoiTransformation()
        self.deleteAllTransformations()
        self.resetRoiIndicesAndColours()

    def onRequestDisplayStage(self, key):
        self.setStageAsDisplayStage(key)

    def onRequestDataStage(self,key):
        self.setStageAsDataStage(key)

    def onDisplayStageChanged(self, stagela: Stage):
        self.displayStage(stagela)

    def onStageListChanged(self):
        self.stageListPlugin_reset()

    def onAddStagePressed(self):
        self.addTemporaryStageToStack()

    def onTemporaryStageChanged(self, stagechen: Stage):
        self.displayStage(stagechen)

    def onCleanSamplePushed(self):
        self.cleanDataRoiTransformation()

    def onLoadSettings(self, filepath):
        pass

    def onDoneWithFile(self):
        self.saveSampleToHDF()

    def onSaveSettings(self, filepath):
        pass

    def onFileSettingsLoaded(self):
        self.resetMainView()


    def onProjectionFunctionChanged(self):
        self.calculateStageAfterMapping()

    def onPostProcessedFunctionChanged(self):
        self.calculateStageAfterProjection()

    def onDataUpdate(self, data: DATA):
        self.updateData(data)

    def onPickAndDeleteItem(self, lastit):
        self.popAll(lastit)
        self.deleteTransformation(lastit)

    def onPickItem(self, index):
        self.displayData(self.activeSample.data[index])

    def onDeleteItem(self, index):
        self.imageWidget.deleteTransformation(index)
        self.popAll(index)

    def onSampleChanged(self):
        self.updateList()

    def onDataCalculated(self, data):
        self.displayData(data)
        self.addData(data)

    def onNewTransformation(self, transformation):
        self.displayTransformation(transformation)
        self.calculateFromTransformation(transformation)
        self.addTransformation(transformation)

    def __init__(self):
        super(AISelectAndVolume, self).__init__()
        self.theroutine()
        self.image = None

    def theroutine(self):
        #Settings need to be loaded
        self.loadSettingsFromFile("settings.ini")

        #ROIBuilder needs to be initialized
        ax, fig = self.getAxAndFig()
        self.LineRoiBuilder_initialize(ax=ax,fig=fig)


    def onRoiAdded(self, roi):
        self.transformROI(roi, self.dataStage, self.settings)
        self.addRoi(roi)
        pass

    def setUIfromSettings(self, settings):
        super().setUIFromSettings(settings)

    def onFilepathChanged(self, filepath):

        # Clean Up everything from last Sample
        self.cleanDataRoiTransformation()
        self.cleanStages()
        self.deleteAllTransformations()
        self.resetRoiIndicesAndColours()
        self.resetStageIndices()

        # load File Specific Settings
        self.settings.directory = os.path.dirname(filepath)
        self.settings.filename = os.path.basename(filepath)
        self.settings.filepath = filepath


        self.loadBioImageSettings()
        self.loadSeriesFromFile(self.settings.filepath)



    def onSeriesChanged(self):
        # Clean Up everything from last Sample
        self.cleanDataRoiTransformation()
        self.cleanStages()
        self.deleteAllTransformations()
        self.resetRoiIndicesAndColours()
        self.resetStageIndices()

        if self.settings.filepath == "":
            self.raiseError("Please select a BioImageFile First")
            return

        self.loadBioImageSettings()
        self.loadSeriesFromFile(self.settings.filepath,force=True)

    def onBioImageLoaded(self, bioimage):
        self.loadPrimaryStage()


    def onClose(self):
        pass