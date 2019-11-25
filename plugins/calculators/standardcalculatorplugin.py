import logging

from plugins.standard.plugin import Plugin
from structures.biometa import BioMeta
from structures.roidata import DummyData
from structures.settings import Settings
from structures.transformation import RectangleTransformation




class StandardCalculation(Plugin):
    def __init__(self):
        super(StandardCalculation, self).__init__()

        logging.info("Standard Calculation initialized")

    def calculateFromTransformation(self, transformation: RectangleTransformation):
        try:
            data = self.settings.calculator(transformation, self.settings, self.activeSample.biometa)
        except Exception as e:
            errormsg = "Erronous Data Calculation. Please Check Stages and Required Input for Data. Dummy Data was Provided Error: {0}".format(e)
            self.raiseError(errormsg)
            logging.info(errormsg)
            data = DummyData(transformation.key,transformationkey=transformation.key,stagekey=transformation.stagekey,roikey=transformation.roikey)

        self.onDataCalculated(data)

    def onDataCalculated(self, data):
        raise NotImplementedError