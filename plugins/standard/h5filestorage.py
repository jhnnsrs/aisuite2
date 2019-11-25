import logging

import h5py

from plugins.standard.plugin import Plugin


class H5FilesStorage(Plugin):

    def __init__(self):
        super().__init__()
        self.availableH5Files = []
        self.availableDataKeys = []
        self.availableSamples = []
        self.old = True

    def loadH5FilesFromDirectory(self, directory):
        import os
        from os.path import join

        self.availableH5Files = []
        for root, subdirs, files in os.walk(directory):
            h5files = [join(root, f) for f in files if f.endswith(".h5")]
            self.availableH5Files += h5files

        self.onH5FilesListChanged()
        self.getAvailableDataKeys()

    def getAvailableDataKeys(self):
        #TODO: Implementing just shared keys
        availabledatakeys = []
        h5 = h5py.File(self.availableH5Files[0], "r")

        try:
            datakeys = [key for key in h5["Data"].keys()]
            #select first data
            for el in datakeys:
                for key in h5["Data/"+el].attrs:
                    if key in availabledatakeys:
                        pass
                    else:
                        availabledatakeys.append(str(key))
                if "Physical" in h5["Data/"+el]:
                    for key in h5["Data/"+el]["Physical"].attrs:
                        if str("Physical/" + key) in availabledatakeys:
                            pass
                        else:
                            availabledatakeys.append(str("Physical/" + key))
        except KeyError as e:
            logging.info("Something went wrong parsing the file",e)
            #implement trying different one

        self.availableDataKeys = availabledatakeys
        self.onDataKeysChanged()


    def onSampleListChanged(self):
        raise NotImplementedError

    def onH5FilesListChanged(self):
        raise NotImplementedError

    def onDataKeysChanged(self):
        raise NotImplementedError
