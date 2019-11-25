import logging

import numpy as np

from structures.biometa import BioMeta
from structures.roidata import StraightenedDATA
from structures.settings import Settings
from structures.transformation import RectangleTransformation


def rectangleStandard(transformation: RectangleTransformation, settings: Settings, meta: BioMeta) -> StraightenedDATA:
    '''Here should only go the routine no actual Calculations'''
    data = StraightenedDATA()
    data.transformationkey = transformation.key
    data.stagekey = transformation.stagekey
    data.roikey = transformation.roikey
    data.key = transformation.roikey
    data.piclength = transformation.image.shape[1]
    data.picheight = transformation.image.shape[0]
    data.roiimage = transformation.image
    data.colour = transformation.colour
    data.index = transformation.index
    data.b4channel = settings.aischannel
    data.vectorlength = np.sum(transformation.boxwidths)
    data.stagestart = settings.startstack
    data.stageend = settings.endstack
    data.physicalsizeunit = meta.physicalsizexunit
    data.physicalsizex = meta.physicalsizex
    data.physicalsizey = meta.physicalsizey

    height = data.picheight
    startx, endx = 0, data.piclength

    data.selectedxstart = startx
    data.selectedxend = endx

    middleup = int((height / 2) - (height/4))
    middledown = int((height / 2) + (height/4))

    bild = data.roiimage[middleup:middledown, :, :]

    np.seterr(divide='ignore', invalid='ignore')  #error level if a pixelvalue is 0
    averages = np.max(bild, axis=0)
    intensity = averages / averages.max(axis=0)

    data.intensitycurves = intensity

    physizex = meta.physicalsizex  # ATTENTION IF NOT SAME RATIO VOXEL IS FUCKED UP
    physizey = meta.physicalsizey

    c = settings.aischannel
    threshold = settings.threshold
    overindices = (intensity[:, c] > threshold).nonzero()[0]


    overindices = np.array([index for index in overindices if index > startx and index < endx])

    if (len(overindices) < 2):
        overindices = np.array([0, data.piclength])
        data.flags.append("Error")
        logging.info("ERROR ON AIS")

    data.flags = data.flags + settings.flags
    xstart = overindices.min()
    ystart = overindices.max()


    data.aisstart = xstart
    data.aisend = ystart

    data.aislength = ystart - xstart

    data.distancestart = data.aisstart
    data.distancestartphysical = data.distancestart * float(physizex)
    data.aisphysicallength = data.aislength * float(physizex)
    logging.info("Length: {0} at {1} resulting in a {2}".format(data.aislength, physizex, data.aisphysicallength))
    data.threshold = threshold

    return data

def rectangleAdvanced(transformation: RectangleTransformation, settings: Settings, meta: BioMeta) -> StraightenedDATA:
    '''Here should only go the routine no actual Calculations'''
    data = StraightenedDATA()
    data.transformationkey = transformation.key
    data.stagekey = transformation.stagekey
    data.roikey = transformation.roikey
    data.key = transformation.roikey
    data.piclength = transformation.image.shape[1]
    data.picheight = transformation.image.shape[0]
    if len(transformation.image.shape) > 2:
        logging.info("3 Channels Supplied")
        total_channels = transformation.image.shape[2]
    else:
        total_channels = 0

    data.roiimage = transformation.image
    data.colour = transformation.colour
    data.index = transformation.index
    data.b4channel = settings.aischannel
    data.vectorlength = np.sum(transformation.boxwidths)
    data.stagestart = settings.startstack
    data.stageend = settings.endstack
    data.physicalsizeunit = meta.physicalsizexunit
    data.physicalsizex = meta.physicalsizex
    data.physicalsizey = meta.physicalsizey
    startx, endx = 0, data.piclength

    data.selectedxstart = startx
    data.selectedxend = endx

    height = data.picheight


    middleup = int((height / 2) - (height/4))
    middledown = int((height / 2) + (height/4))

    if len(transformation.image.shape) > 2:
        bild = data.roiimage[middleup:middledown, :, :]
    else:
        bild = data.roiimage[middleup:middledown, :]

    np.seterr(divide='ignore', invalid='ignore')  #error level if a pixelvalue is 0
    averages = np.max(bild, axis=0)
    intensity = averages / averages.max(axis=0)

    data.intensitycurves = intensity

    physizex = meta.physicalsizex  # ATTENTION IF NOT SAME RATIO VOXEL IS FUCKED UP
    physizey = meta.physicalsizey

    threshold = settings.threshold
    if total_channels != 0:
        c = settings.aischannel
        overindices = (intensity[:, c] > threshold).nonzero()[0]
    else:
        overindices = (intensity > threshold).nonzero()[0]

    overindices = np.array([index for index in overindices if index >= startx and index <= endx])

    try:
        xstart = overindices.min()
        ystart = overindices.max()

        if "Error" in data.flags: data.flags.remove("Error")
    except:
        xstart = -1
        ystart = -1

        if "Error" not in data.flags: data.flags.append("Error")
        logging.info("ERROR ON AIS")

    data.selectedxstart = 0
    data.selectedxend = data.piclength

    data.aisstart = xstart
    data.aisend = ystart
    data.aislength = ystart - xstart
    data.distancestart = data.aisstart
    data.distancestartphysical = data.distancestart * float(physizex)
    data.aisphysicallength = data.aislength * float(physizex)
    logging.info("Length: {0} at {1} resulting in a {2}".format(data.aislength, physizex, data.aisphysicallength))
    data.threshold = threshold

    return data


def reprocessAIS(data: StraightenedDATA, segments, threshold):

    startx, endx = segments

    data.selectedxstart = startx
    data.selectedxend = endx

    if len(data.roiimage.shape) > 2:
        logging.info("3 Channels Supplied")
        total_channels = data.roiimage.shape[2]
    else:
        total_channels = 0

    height = data.picheight

    middleup = int((height / 2) - (height / 4))
    middledown = int((height / 2) + (height / 4))

    if len(data.roiimage.shape) > 2:
        bild = data.roiimage[middleup:middledown,:, :]
    else:
        bild = data.roiimage[middleup:middledown,:]

    np.seterr(divide='ignore', invalid='ignore')  # error level if a pixelvalue is 0
    averages = np.max(bild, axis=0)
    intensity = averages / averages.max(axis=0)

    data.intensitycurves = intensity

    physizex = data.physicalsizex  # ATTENTION IF NOT SAME RATIO VOXEL IS FUCKED UP
    physizey = data.physicalsizey

    threshold = threshold
    if total_channels != 0:
        c = data.b4channel
        overindices = (intensity[:, c] > threshold).nonzero()[0]
    else:
        overindices = (intensity > threshold).nonzero()[0]


    overindices = np.array([index for index in overindices if index >= startx and index <= endx])

    try:
        xstart = overindices.min()
        ystart = overindices.max()
    except:
        xstart = -1
        ystart = -1

        if "Error" not in data.flags: data.flags.append("Error")
        logging.info("ERROR ON AIS")


    data.aisstart = xstart
    data.aisend = ystart
    data.aislength = ystart - xstart
    data.distancestart = data.aisstart
    data.distancestartphysical = data.distancestart * float(physizex)
    data.aisphysicallength = data.aislength * float(physizex)
    logging.info("Length: {0} at {1} resulting in a {2}".format(data.aislength, physizex, data.aisphysicallength))
    data.threshold = threshold
    data.hassecond = True

    return data


