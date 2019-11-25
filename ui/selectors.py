import logging

from PyQt5 import QtWidgets
from plugins.standard.plugin import Plugin


class CallbackSelector(QtWidgets.QComboBox):
    def __init__(self, routine: Plugin, callback):
        super(CallbackSelector, self).__init__()
        self.logprefix = "{0}"
        self.routine = routine
        self.itemnames = []
        self.callbacklist = []
        self.itemsToAdd()
        self.callback = callback

        self.currentIndexChanged.connect(self.selectionChanged)

    def itemsToAdd(self):
        pass

    def setCallback(self, callback):
        self.callback(callback)

    def selectionChanged(self, i):
        self.changeSelected(i)

        logging.info(self.logprefix.format(self.itemnames[i]))
        self.setCallback(self.callbacklist[i])

    def newItem(self, name, callback):
        self.addItem(name)
        self.itemnames.append(name)
        self.callbacklist.append(callback)

    def changeSelected(self, i):
        raise NotImplementedError


class ProjectionsSelector(CallbackSelector):
    def changeSelected(self, i):
        self.routine.settings.selectedmapping = i

    def __init__(self, routine: Plugin, callback):
        super().__init__(routine, callback)
        self.logprefix = "Projection set to {0}"

    def itemsToAdd(self):
        for item in self.routine.settings.availableProjections:
            self.newItem(item[0], item[1])

        self.setCurrentIndex(self.routine.settings.selectedmapping)


class PostProcessSelector(CallbackSelector):
    def changeSelected(self, i):
        self.routine.settings.selectedpostprocess = i

    def __init__(self, routine: Plugin, callback):
        super().__init__(routine, callback)
        self.logprefix = "Postprocessing set to {0}"

    def itemsToAdd(self):
        for item in self.routine.settings.availablePostProcessing:
            self.newItem(item[0], item[1])

        self.setCurrentIndex(self.routine.settings.selectedpostprocess)

class CalculatorSelector(CallbackSelector):
    def changeSelected(self, i):
        self.routine.settings.selectedcalculator = i

    def __init__(self, routine: Plugin, callback):
        super().__init__(routine, callback)
        self.logprefix = "Calculator set to {0}"

    def itemsToAdd(self):
        for item in self.routine.settings.availableCalculators:
            self.newItem(item[0], item[1])

        self.setCurrentIndex(self.routine.settings.selectedpostprocess)


class ChannelSelector(CallbackSelector):

    def changeSelected(self, i):
        self.routine.settings.selectiveChannel = i

    def __init__(self, routine, callback):
        super().__init__(routine, callback)
        self.logprefix = "Selective Channel set to {0}"

    def itemsToAdd(self):
        channelnames = self.routine.settings.getMappedChannelNames()
        for index, i in enumerate(channelnames):
            self.newItem(i, index)

        self.setCurrentIndex(self.routine.settings.selectiveChannel)


class AISSelector(CallbackSelector):
    def changeSelected(self, i):
        self.routine.settings.aischannel = i

    def __init__(self, routine, callback):
        super().__init__(routine, callback)
        self.logprefix = "AIS-Channel set to {0}"

    def itemsToAdd(self):
        channelnames = self.routine.settings.getMappedChannelNames()
        for index, i in enumerate(channelnames):
            self.newItem(i, index)

        self.setCurrentIndex(self.routine.settings.aischannel)

class TransformerSelector(CallbackSelector):
    def changeSelected(self, i):
        self.routine.settings.selectedtransformer = i

    def __init__(self, routine: Plugin, callback):
        super().__init__(routine, callback)
        self.logprefix = "Transformer set to {0}"

    def itemsToAdd(self):
        for item in self.routine.settings.availableTransformers:
            self.newItem(item[0], item[1])

        self.setCurrentIndex(self.routine.settings.selectedpostprocess)
