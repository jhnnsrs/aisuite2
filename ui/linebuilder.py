import logging

import numpy as np

import structures.maps as universal


class RoiBuilder:
    # Builds a ROI with matplotlib functions
    # also draws Patches for each roi and makes them deletable
    def __init__(self,routine =None):
        self.routine = routine

    def start(self,ax,fig):
        self.ax = ax
        self.fig = fig

    def addPatch(self,patch):
        pass



class LineBuilder(RoiBuilder):
    lock = None  # only one line can be build at a time

    def __init__(self,routine):
        super(LineBuilder,self).__init__(routine=routine)
        self.base_scale = 1.2

    def initialize(self,ax,fig):
        self.ax = ax
        self.fig = fig


        self.locked = False  # is set by other

        self.roicount = 0
        self.roi = None


        self.lastvector = np.array([0, 0])
        self.lastdot = np.array([0, 0])
        self.dotthreshold = 3
        self.vectorthreshold = 3
        self.linecallback = self.routine.addLines
        self.pickcallback = self.routine.onPick


        self.cid = fig.canvas.mpl_connect('button_press_event', self.on_pressevent)
        self.cidrelease = fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cid2 = fig.canvas.mpl_connect('key_press_event', self.on_keyevent)


        self.smoothingfactor = universal.smoothingfactor
        self.rawVectors = []
        self.smoothedVectors = []


    def on_pressevent(self, event):
        if self.locked: return
        if event.inaxes != self.ax: return
        if event.xdata == None or event.ydata == None: return #TODO: MIGHT FAULT
        # if not self.line: self.line, = self.ax.plot([event.xdata, event.ydata])  # first generate line
        LineBuilder.lock = self


        newvector = np.array([event.xdata, event.ydata])

        self.rawVectors.append(newvector)
        self.smoothedVectors.append(newvector)
        self.lastvector = event.xdata, event.ydata



    def on_motion(self, event):
        if self.locked: return
        if LineBuilder.lock is not self: return

        newvector = np.array([event.xdata, event.ydata])
        if event.xdata == None or event.ydata == None: return

        self.rawVectors.append(newvector)
        vectordistance = np.linalg.norm(newvector - self.lastvector)

        if vectordistance > self.smoothingfactor:
            self.smoothedVectors.append(newvector)
            self.lastvector = newvector.copy()

    def on_release(self, event):
        if self.locked: return
        LineBuilder.lock = None
        if len(self.smoothedVectors) > 2:
            self.linecallback(self.smoothedVectors)

        self.cleanUp()

    def cleanUp(self):
        self.rawVectors = []
        self.smoothedVectors = []
        self.line = None
        self.lastvector = np.array([0, 0])



    def on_keyevent(self, event):
        # Locks drawing on the screen
        logging.info('Keystroke {0} was recorded. Lock/Unlock drawing', event.key)
        if event.key == "i":
            self.locked = not self.locked

