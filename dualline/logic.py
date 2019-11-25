#  This file is part of AIVolume.

#  AIVolume is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  AIVolume is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with AIVolume.  If not, see <http://www.gnu.org/licenses/>.
import logging

import h5py
import numpy as np
import random
import copy
import os
from os.path import join

from structures.roidata import StraightenedDATA
from volume.settings import Global
from volume.elements import AreaROI

def overlap(image, aischannel, clusterchannel, threshold, synpothreshold):
    max = np.max(image[:,:,aischannel])
    max2 = np.max(image[:,:,clusterchannel])
    channel1 = aischannel
    channel2 = clusterchannel
    threshold = threshold * max
    synpothreshold = synpothreshold * max2
    overch1 = [1 if i == True else 0 for i in (image[:,:, channel1] > threshold).flatten()]
    overch2 = [1 if i == True else 0 for i in (image[:,:, channel2] > synpothreshold).flatten()]

    both = np.add(overch2,overch1)
    newimage = [255 if i == 2 else 0 for i in both]
    newimage = np.array(newimage).reshape((image.shape[0],image.shape[1]))

    return newimage

def getAIS(mypath):

    aish5list = []
    h5filelist = []
    for root, subdirs, files in os.walk(mypath):
        h5file = [join(root, f) for f in files if f.endswith(".h5")]
        h5filelist += h5file

    for h5file in h5filelist:
        if h5py.is_hdf5(h5file):
            with h5py.File(h5file, "r") as lala:

                try:
                    rois = [key for key in lala["Data"].keys()]
                    for roi in rois:
                        try:
                            nana = lala["Data/" + roi + "/Physical"].attrs["Diameter"]
                            print("FILE ", h5file, " already has a Diameter. Skipping")
                        except KeyError as e:
                            print("FILE ", h5file, " has no Diameter. Taking into account")
                            newroi = AreaROI()
                            try:
                                newroi.length = float(lala["Data/" + roi + "/Physical"].attrs["AISPhysicalLength"])
                                newroi.image = np.array(lala["Data/" + roi + "/Image"])
                                newroi.flags = str(lala["Data/" + roi].attrs["Flags"])
                                newroi.index = int(lala["Data/" + roi].attrs["index"])
                                newroi.b4channel = int(lala["Data/" + roi].attrs["B4-Channel"])
                                newroi.voxelsize = lala.attrs["physicalsizex"]
                                newroi.key = roi
                            except:
                                print("File has new  Structure")
                                newroi.length = float(lala["Data/" + roi].attrs["Physical-Length"])
                                newroi.image = np.array(lala["Data/" + roi + "/Image"])
                                newroi.flags = str(lala["Data/" + roi].attrs["Flags"])
                                newroi.index = int(lala["Data/" + roi].attrs["Key"])
                                newroi.b4channel = int(lala["Data/" + roi].attrs["B4-Channel"])
                                newroi.voxelsize = lala.attrs["Physicalsize-X"]
                                newroi.key = roi
                            print(newroi.flags)
                            # should only add the ones that are not already set
                            aish5list.append([newroi,h5file])
                except KeyError as e:
                    print("File {0} doesnt hava data Object: {1}".format(h5file, e))
                    pass

        else:
            print("File " + h5file + " doesn't conform with h5 standards")
            pass


    return aish5list

def dataAccessor(lala, roi,attribute):
    try:
        return lala["Data/" + roi].attrs[attribute]
    except:
        return False

def getData(mypath) -> [StraightenedDATA] :
    aish5list = []
    h5filelist = []
    for root, subdirs, files in os.walk(mypath):
        h5file = [join(root, f) for f in files if f.endswith(".h5")]
        h5filelist += h5file

    for h5file in h5filelist:
        if h5py.is_hdf5(h5file):
            with h5py.File(h5file, "r") as lala:

                try:
                    rois = [key for key in lala["Data"].keys()]
                    for roi in rois:
                        try:
                            nana = lala["Data/" + roi + "/Physical"].attrs["Diameter"]
                            print("FILE ", h5file, " already has a Diameter. Skipping")
                        except KeyError as e:
                            print("FILE ", h5file, " has no Diameter. Taking into account")
                            newroi = StraightenedDATA()
                            try:
                                print("File has new  Structure")
                                newroi.length = float(dataAccessor(lala,roi,"Physical-Length"))
                                newroi.physicalsizex = float(dataAccessor(lala,roi,"Physical-Pixelsize"))
                                newroi.physicalsizeunit = str(dataAccessor(lala,roi,"PhysicalSizeUnit"))
                                newroi.selectedxstart = float(dataAccessor(lala,roi,"SelectedXStart"))
                                newroi.threshold = float(dataAccessor(lala,roi,"Threshold"))
                                newroi.selectedxend = float(dataAccessor(lala,roi,"SelectedXEnd"))
                                newroi.intensitycurves = np.array(lala["Data/" + roi + "/Intensitycurves"])
                                newroi.roiimage = np.array(lala["Data/" + roi + "/Image"])
                                newroi.flags = str(lala["Data/" + roi].attrs["Flags"]).split(',')
                                newroi.index = int(lala["Data/" + roi].attrs["Key"])
                                newroi.b4channel = int(lala["Data/" + roi].attrs["B4-Channel"])
                                newroi.voxelsize = lala.attrs["Physicalsize-X"]
                                newroi.key = roi
                                newroi.piclength =  float(dataAccessor(lala,roi,"Piclength"))
                                newroi.picheight =  newroi.roiimage.shape[0] # TODO: Dirty
                                newroi.aisstart = float(dataAccessor(lala,roi,"AIS-Start"))
                                newroi.aisend = float(dataAccessor(lala,roi,"AIS-End"))
                                newroi.secondstart = dataAccessor(lala,roi,"SecondStart")
                                newroi.secondend = dataAccessor(lala,roi,"SecondEnd")
                                newroi.secondlength = dataAccessor(lala,roi,"SecondLength")
                                newroi.distancesecondstart = dataAccessor(lala,roi,"DistanceSecondStart")
                                newroi.distancesecondstartphysical = dataAccessor(lala,roi,"DistanceSecondStartPhysical")
                                newroi.selectedsecondxend = dataAccessor(lala,roi,"SelectedSecondXEnd")
                                newroi.selectedsecondxstart = dataAccessor(lala,roi,"SelectedSecondXStart")
                                newroi.secondphysicallength = dataAccessor(lala,roi,"SecondPhysicalLength")
                                newroi.secondthreshold = dataAccessor(lala,roi,"SecondThreshold")
                                newroi.secondchannel = dataAccessor(lala,roi,"SecondChannel")
                                newroi.hassecond = dataAccessor(lala,roi,"HasSecond")

                                print(newroi.flags)
                                # should only add the ones that are not already set
                                aish5list.append([newroi, h5file])
                            except:
                                print("Failure Loading")

                except KeyError as e:
                    print("File {0} doesnt hava data Object: {1}".format(h5file, e))
                    pass

        else:
            print("File " + h5file + " doesn't conform with h5 standards")
            pass


    return aish5list

def getSobel(image,b4channel=Global.b4channel, canny1 = 100, canny2 = 100):
    import cv2

    try:
        cvimage = image[:, :, b4channel]
        blured = cv2.GaussianBlur(cvimage, (3, 3), 3)
    except:
        cvimage = image
        blured = np.uint8(cvimage)
    logging.info("Creating Canny Edged Picture with Parameters: {0} and {1}".format(canny1,canny2))
    sobelx = cv2.Canny(blured, canny1, canny2)

    return sobelx

def getLineListSobel(sobelx):

    firstover = np.argmax(sobelx, axis=0)
    lastover = sobelx.shape[0] - np.argmax(np.flip(sobelx, axis=0), axis=0)

    linelist = []
    for index, (ystart, yend) in enumerate(zip(firstover, lastover)):
        if ystart > 0 and yend < sobelx.shape[1]:
            linelist.append([np.array([index, ystart]), np.array([index, yend])])

    return linelist


def calculateDiameterAndVolume(roi: AreaROI):
    # in pixel right now

    linelengths = []
    for slice in roi.linelist:
        length = np.linalg.norm(slice[0]-slice[1])
        linelengths.append(length)

    lengthmeans = []
    for startx, starty in roi.sections:
        sectionmean = np.mean(linelengths[int(startx):int(starty)])
        lengthmeans.append(sectionmean)

    #1 approach
    diameter = np.mean(lengthmeans) * roi.voxelsize
    volume = np.math.pi * (diameter/2) ** 2 * roi.length


    print("Volume: ",volume)
    print("Diameter: ",diameter)
    return diameter, volume


def calculateSynpoVolume(ais):
    return None


def reprocessAISandSecond(data: StraightenedDATA, segments, segments2, threshold, threshold2, secondchannelUI):

    startx, endx = segments
    startsecondx, endsecondx = segments2

    data.selectedxstart = startx
    data.selectedxend = endx
    data.selectedsecondxstart = startsecondx
    data.selectedsecondxend = endsecondx

    if len(data.roiimage.shape) > 2:
        logging.info("3 Channels Supplied")
        total_channels = data.roiimage.shape[2]
    else:
        total_channels = 0

    secondchannel = secondchannelUI if secondchannelUI < total_channels else total_channels - 1

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
        d = secondchannel
        overindices = (intensity[:, c] > threshold).nonzero()[0]
        overindices2 = (intensity[:, d] > threshold2).nonzero()[0]
    else:
        overindices = (intensity > threshold).nonzero()[0]
        overindices2 = (intensity > threshold2).nonzero()[0]


    overindices = np.array([index for index in overindices if index >= startx and index <= endx])
    overindices2 = np.array([index for index in overindices2 if index >= startsecondx and index <= endsecondx])

    try:
        xstart = overindices.min()
        ystart = overindices.max()
        secondstart = overindices2.min()
        secondend = overindices2.max()
    except:
        xstart = -1
        ystart = -1
        secondstart = -1
        secondend = -1

        if "Error" not in data.flags: data.flags.append("Error")
        logging.info("ERROR ON AIS")

    data.aisstart = xstart
    data.aisend = ystart
    data.secondstart = secondstart
    data.secondend = secondend
    data.aislength = ystart - xstart
    data.secondlength = secondend - secondstart
    data.distancestart = data.aisstart
    data.distancesecondstart = data.secondstart
    data.distancestartphysical = data.distancestart * float(physizex)
    data.distancesecondstartphysical = data.distancesecondstart * float(physizex)
    data.aisphysicallength = data.aislength * float(physizex)
    data.secondphysicallength = data.secondlength * float(physizex)
    logging.info("Length: {0} at {1} resulting in a {2}".format(data.aislength, physizex, data.aisphysicallength))
    logging.info("SecondLength: {0} at {1} resulting in a {2}".format(data.secondlength, physizex, data.secondphysicallength))
    data.threshold = threshold
    data.secondthreshold = threshold2
    data.secondchannel = secondchannel
    data.hassecond = True

    return data


