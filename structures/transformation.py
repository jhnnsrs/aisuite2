#
from matplotlib import patches
from matplotlib.path import Path


class TRANSFORMATION:

    def __init__(self, image = None):
        self.roikey = None #Tranformation from which roy
        self.stagekey = None #Transformation from which stage
        self.image = image
        self.index = None
        self.method = "Please set method in transformer-class"

    def getPatches(self):
        raise NotImplementedError

    def getHDF(self,item,settings):
        raise NotImplementedError


class RectangleTransformation(TRANSFORMATION):


    def __init__(self):
        super().__init__()
        self.key = None
        self.boxwidths = None
        self.pixelwidths = None
        self.image = None
        self.boxes = None
        self.colour = None
        self.colouralpha = 0.6
        self.type = "RectangleTransformation"

    def getPatches(self):
        thepatches = []
        # Draw Boxes
        for verts in self.boxes:
            vertices = verts + [[0, 0]]  # dummy
            codes = [Path.MOVETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.CLOSEPOLY,
                     ]

            path = Path(vertices, codes)

            patch = patches.PathPatch(path, lw=None)
            patch.set_facecolor(self.colour)
            patch.set_alpha(self.colouralpha)

            thepatches.append(patch)

        return thepatches

    def getHDF(self,item,settings):

        item.attrs["Key"] = self.key
        item.attrs["Stagekey"] = self.stagekey
        item.attrs["Roikey"] = self.roikey
        item.create_dataset("Image", data=self.image)
        item.create_dataset("Boxwidths", data=self.boxwidths)
        item.create_dataset("Pixelwidths", data=self.pixelwidths)

        return item

