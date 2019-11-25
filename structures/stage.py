from structures.settings import Settings


class Stage:

    def __init__(self):
        self.istemporary = True
        self.isdisplay = False
        self.istosave = True
        self.isdata = False
        self.name = None
        self.key = None
        self.image = None
        self.info = {"Mapping": "R,G,B",
                     "Projection": "MaxISP",
                     "PostProcessed": "Sobel"
                     }

    def getHDF(self, item, settings: Settings):
        item.create_dataset("Image", data=self.image)
        for key in self.info:
            item.attrs[key] = self.info[key]
        item.attrs["Key"] = self.key
        item.attrs["Name"] = self.name
        return item

