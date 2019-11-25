import logging

from plugins.standard.plugin import Plugin
from structures.roi import ROI
from structures.roidata import DATA
from structures.transformation import TRANSFORMATION


class SampleStorage(Plugin):

    def __init__(self):
        super(SampleStorage, self).__init__()
        logging.info("Sample Storage initialized")

    def setSample(self,sample):
        self.activeSample = sample
        self.onSampleChanged()

    def addRoi(self,roi: ROI):
        self.activeSample.rois[roi.key] = roi
        self.onSampleChanged()

    def addTransformation(self,transformation: TRANSFORMATION):
        self.activeSample.transformations[transformation.key] = transformation
        self.onSampleChanged()

    def addData(self,data : DATA):
        self.activeSample.data[data.key] = data
        self.onSampleChanged()

    def updateData(self,data : DATA):
        self.activeSample.data[data.key] = data
        self.onSampleChanged()

    def popRoi(self,index):
        if index in self.activeSample.rois:
            del self.activeSample.rois[index]
            self.onSampleChanged()

    def popTransformation(self,index):
        del self.activeSample.transformations[index]
        self.onTransformationPopped(index)
        self.onSampleChanged()

    def popData(self,index):
        del self.activeSample.data[index]
        self.onSampleChanged()

    def addAll(self,roi,transformation,data):
        assert roi.key == transformation.key == data.key, "Not all Index are the same, fatal"

    def popAll(self,index):
        self.popRoi(index)
        self.popData(index)
        self.popTransformation(index)

        self.onSampleChanged()

    def onSampleChanged(self):
        raise NotImplementedError

    def onTransformationPopped(self, index):
        pass

    def cleanDataRoiTransformation(self):
        self.activeSample.data = {}
        self.activeSample.transformations = {}
        self.activeSample.rois = {}

        #TODO: Implement a clean Sample Cleanup

        self.onSampleChanged()


    def saveSampleToHDF(self):
        from logic.io import saveSampleToHDF
        saveSampleToHDF(self.activeSample, self.settings)