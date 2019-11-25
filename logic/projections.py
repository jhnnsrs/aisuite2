import logging

import numpy as np
from standardlibs.misc import *
from structures.settings import Settings


def tonumpy(image):
    # Handles the CVImage to NumpyConversion
    cvimg = toimage(image)
    img = np.array(cvimg)
    return img


def maxisp(file,settings: Settings) -> np.array:
    if file.shape[3] == 0:
        logging.info("File already Projected")
        return tonumpy(file[:,:,:])

    maxproj = np.nanmax(file[:,:,:,:,settings.t], axis=3)  # TODO: Make good looking
    return tonumpy(maxproj), {"Projection":"MaxISP"}

def slicedmaxisp(file,settings: Settings) -> np.array:
    startstage = settings.startstage
    endstage = settings.endstage
    if startstage > endstage: startstage = settings.startstack
    if endstage < startstage: endstage = settings.endstack

    logging.info("Trying to map file with Startstage: {0}/{2} and Endstage {1}/{2}".format(startstage,endstage,settings.endstack))
    slicedmax, info = maxisp(file[:, :, :, startstage:endstage, :], settings)
    info = {"Projection": "Sliced Max ISP Start: {0} End: {1}".format(startstage, endstage)}
    return slicedmax, info