import logging

import cv2
import numpy as np

from structures.settings import Settings


def void(file, settings: Settings) -> np.array:
    stageinfo = {"Postprocessing":"Void"}
    return file,stageinfo

def laplace(image, settings: Settings):
    logging.info("LaPlacian of  Selective Channel")
    image = image[:, :, settings.selectiveChannel]
    laplacian = cv2.Laplacian(image, cv2.CV_64F)

    info = {"Postprocessing": "La Placian of Channel {0}".format(settings.getMappedChannelNames()[settings.selectiveChannel])}
    return laplacian, info

def channelintensity(image, settings: Settings):
    logging.info("Only display channel {0}".format(settings.selectiveChannel))
    images = image[:, :, settings.selectiveChannel]


    info = {"Postprocessing": "Intensity of {0}".format(settings.getMappedChannelNames()[settings.selectiveChannel])}
    return images, info

def prewitt(image, settings: Settings):
    logging.info("Only display channel {0}".format(settings.selectiveChannel))
    gray = image[:, :, settings.selectiveChannel]

    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])

    img_gaussian = cv2.GaussianBlur(gray, (3, 3), 0)
    img_prewittx = cv2.filter2D(img_gaussian, -1, kernelx)
    img_prewitty = cv2.filter2D(img_gaussian, -1, kernely)

    images = img_prewittx + img_prewitty
    info = {"Postprocessing": "Intensity of {0}".format(settings.getMappedChannelNames()[settings.selectiveChannel])}
    return images, info

def robertoperator(image, settings: Settings):
    logging.info("Only display channel {0}".format(settings.selectiveChannel))
    image = image[:, :, settings.selectiveChannel]
    image = np.asarray(image, dtype="int32")
    roberts_cross_v = np.array([[0, 0, 0],
                                [0, 1, 0],
                                [0, 0, -1]])

    roberts_cross_h = np.array([[0, 0, 0],
                                [0, 0, 1],
                                [0, -1, 0]])

    from scipy import ndimage
    vertical = ndimage.convolve( image, roberts_cross_v )
    horizontal = ndimage.convolve( image, roberts_cross_h )

    output_image = np.sqrt( np.square(horizontal) + np.square(vertical))

    info = {"Postprocessing": "Intensity of {0}".format(settings.getMappedChannelNames()[settings.selectiveChannel])}
    return output_image, info


def overlap(image, settings: Settings):
    max = np.max(image)
    channel1 = 0
    channel2 = 1
    threshold = settings.overlapthreshold * max
    overch1 = [1 if i == True else 0 for i in (image[:,:, channel1] > threshold).flatten()]
    overch2 = [1 if i == True else 0 for i in (image[:,:, channel2] > threshold).flatten()]

    both = np.add(overch2,overch1)
    newimage = [max if i == 2 else 0 for i in both]
    newimage = np.array(newimage).reshape((image.shape[0],image.shape[1]))
    info = {"Postprocessing": "Overlapping of Channel {0} and {1}".format(settings.getMappedChannelNames()[channel1], settings.getMappedChannelNames()[channel2])}

    return newimage, info

def canny(image, settings: Settings):
    cvimage = image[:, :, settings.selectiveChannel]
    blured = cv2.GaussianBlur(cvimage, (3, 3), 3)
    sobelx = cv2.Canny(blured, 100, 200)
    info = {"Postprocessing": "Canny Edge of Channel {0}".format(
        settings.getMappedChannelNames()[settings.selectiveChannel])}

    return sobelx, info


def color(image, settings: Settings):
    imager = np.zeros(image.shape, np.uint8)
    imager[:,:,settings.selectiveChannel] = image[:,:,settings.selectiveChannel]

    info = {"Postprocessing": "Selective color of Channel {0}".format(
        settings.getMappedChannelNames()[settings.selectiveChannel])}

    return imager, info


def sobelunblurred(image, settings: Settings):
    image = image[:, :, settings.selectiveChannel]
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
    info = {"Postprocessing": "Sobel of Channel {0}".format(
        settings.getMappedChannelNames()[settings.selectiveChannel])}

    return sobelx, info

def sobelblurred(image, settings: Settings):
    image = image[:, :, settings.selectiveChannel]
    blurred = cv2.GaussianBlur(image, (3, 3), 3)
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=5)
    info = {"Postprocessing": "Sobel of Blurred Channel {0}".format(
        settings.getMappedChannelNames()[settings.selectiveChannel])}

    return sobelx, info

def harrisCorner(image, settings: Settings):
    img = image
    gray = np.float32(image[:,:,settings.selectiveChannel])
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)

    # Threshold for an optimal value, it may vary depending on the image.
    c = [0,0,0]
    c[settings.selectiveChannel] = 255
    img[dst > settings.threshold * dst.max()] = c
    info = {"Postprocessing": "Harris Corner"}
    return img, info


