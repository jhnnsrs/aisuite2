import numpy as np


class ROI:
    def __init__(self,key=None, colour= None):
        self.colour = colour
        self.key = key

    def __str__(self):
        return "Roi {0}".format(self.key)

    def getHDF(self,item, settings):

        return [("WARNING","Roi-Class doesnt Provided HDF Interface. please provide getHDF function")]

class LineROI(ROI):

    def __init__(self, image=None,key=None, boxwidths=None, pixelwidths=None, colour=None, vertices=None):
        super().__init__(key, colour)
        self.vertices = vertices
        #Reproducable Data from UserInput
        self.uservectors = None
        self.type = "LineROI"

    def getHDF(self,item,settings):


        item.attrs["Index"] = self.key
        item.create_dataset("Inputvectors", data=np.array(self.vertices))

        return item

