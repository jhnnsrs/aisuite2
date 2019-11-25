import numpy as np

from structures.settings import Settings


class DATA:

    def __init__(self,key=None):
        self.type = "Data"
        self.stagekey = None
        self.roikey = None
        self.transformationkey = None
        self.key = key
        self.flags = []

    def getHDF(self,item, settings: Settings):
        return [("WARNING","Data Structure doesnt't implement getHDF")]
        pass


class DummyData(DATA):

    def __init__(self,key,transformationkey,stagekey,roikey):
        super().__init__(key)
        self.stagekey = stagekey
        self.roikey = roikey
        self.transformationkey = key
        self.flags = "ERRONOUS DATA PROCESSs"

    def getHDF(self,item, settings: Settings):
        item.attrs["Key"] = self.key
        item.attrs["Stagekey"] = self.stagekey
        item.attrs["Roikey"] = self.roikey
        item.attrs["Flags"] = self.flags

        return item


class StraightenedDATA(DATA):

    def __init__(self):
        super().__init__()
        self.physicalsizeunit = "µm"
        self.type = "Straightened"
        self.parsingmethod = "Straighten - standard"
        self.roindex = 0
        self.aislength = 0
        self.piclength= 0
        self.picheight = 0
        self.aisstart = 0
        self.aisend = 0
        self.b4channel = 0
        self.threshold = 0
        self.vectorlength = 0
        self.colour = ""
        self.selectedxend = 0
        self.selectedxstart = 0

        self.distancestart = 0
        self.distancestartphysical = 0

        self.stagestart = 0
        self.stageend = 0

        self.roiimage = None # TODO: Outsource to Transformation
        self.intensitycurves = []  # shape (length,values,amountchannels)
        self.aisphysicallength = 0
        self.aisphysicalstart = 0
        self.aisphysicalend = 0
        self.physicalsizex = 0
        self.physicalsizey = 0
        self.comment = 0

        #TODO: Maybe implement complete dependency on savable List
        #Would be easier to make an export routine for different data structures
        self.allHDFList = None

    def getHDF(self,item,settings: Settings):
        item.create_dataset("Intensitycurves", data= np.array(self.intensitycurves))
        item.create_dataset("Image", data=self.roiimage)
        item.attrs["Key"] = self.key
        item.attrs["Stagekey"] = self.stagekey
        item.attrs["Roikey"] = self.roikey
        item.attrs["Transformationkey"] = self.transformationkey
        item.attrs["Piclength"] = self.piclength
        item.attrs["AIS-Start"] = self.aisstart
        item.attrs["AIS-End"] = self.aisend
        item.attrs["B4-Channel"] = self.b4channel
        item.attrs["Threshold"] = self.threshold
        item.attrs["Method"] = self.parsingmethod
        item.attrs["Flags"] = settings.flagsseperator.join(self.flags)
        item.attrs["Comment"] = self.comment
        item.attrs["SelectedXStart"] = self.selectedxstart
        item.attrs["SelectedXEnd"] = self.selectedxend
        item.attrs["Stage-Start"] = self.stagestart
        item.attrs["Stage-End"] = self.stageend
        item.attrs["Colour"] = self.colour
        item.attrs["Physical-Length"] = self.aisphysicallength
        item.attrs["Physical-Pixelsize"] = self.physicalsizex
        item.attrs["Parsing Method"] = self.parsingmethod
        item.attrs["PhysicalSizeUnit"] = self.physicalsizeunit
        item.attrs["DistanceToStart"] = self.distancestart
        item.attrs["DistanceToStart-Physical"] = self.distancestartphysical

        return item

    @staticmethod
    def getDataFromHDF(item, settings: Settings) -> DATA:

        parsed = StraightenedDATA()
        parsed.roiimage = item["Image"]
        parsed.intensitycurves = item["Intensitycurves"]
        parsed.key = item.attrs["Key"]
        parsed.stagekey = item.attrs["Stagekey"]
        parsed.roikey = item.attrs["Roikey"]
        parsed.transformationkey = item.attrs["Transformationkey"]
        parsed.piclength = item.attrs["Piclength"]
        parsed.aisstart = item.attrs["AIS-Start"]
        parsed.aisend = item.attrs["AIS-End"]
        parsed.b4channel = item.attrs["B4-Channel"]
        parsed.threshold = item.attrs["Threshold"]
        parsed.parsingmethod = item.attrs["Method"]
        parsed.flags = item.attrs["Flags"].split(settings.flagsseperator)
        parsed.comment = item.attrs["Comment"]
        parsed.stagestart = item.attrs["Stage-Start"]
        parsed.stageend = item.attrs["Stage-End"]
        parsed.colour = item.attrs["Colour"]
        parsed.aisphysicallength = item.attrs["Physical-Length"]
        parsed.parsingmethod = item.attrs["Parsing Method"]

        # Get all Data that was saved in File into corresponding Attrs
        parsed.allHDFList = {}
        for key in item.attrs:
            parsed.allHDFList[key] = item.attrs[key]

        #TODO: Uncomment
        # parsed.physicalsizeunit= item.attrs["PhysicalSizeUnit"]

        return parsed


class VolumetricData(DATA):
    def __init__(self):
        super().__init__()


class StraightenedProcessDATA(DATA):
    pass