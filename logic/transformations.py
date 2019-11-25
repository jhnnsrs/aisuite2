import logging

import cv2
import numpy as np



def translateImageFromLine(image, line, scale) -> (np.array, list, list, list):
    ''' Translates the Image according to the Line and the Scale'''

    boxes, boxeswidths = getBoxesFromLine(line,scale)
    image, pixelwidths = straightenImageFromBoxes(image,boxes,scale)

    return image, boxeswidths, pixelwidths, boxes


def getScaledOrtho(vertices, scale):
    '''Gets the 2D Orthogonal do the vertices provided'''
    perp = np.empty_like(vertices)
    perp[0] = -vertices[1]
    perp[1] = vertices[0]

    perpnorm = perp / np.linalg.norm(perp)
    perpscaled = perpnorm * scale
    return perpscaled

def getBoxesFromLine(line, scale):
    '''Index 0 Box is between 0 and 1 Vector'''
    line = np.array(line)
    boxes = []
    boxeswidths = []
    for pos in range(len(line)-1):
        a = line[pos]
        b = line[pos+1]

        perpnew = getScaledOrtho(a - b, scale=scale)

        c1 = a + perpnew
        c2 = a - perpnew
        c3 = b - perpnew
        c4 = b + perpnew
        width = np.linalg.norm(a - b)
        verts = [c1, c2, c3, c4]

        boxes.append(verts)
        boxeswidths.append(width)

    return boxes,boxeswidths


def straightenImageFromBoxes(image, boxes, scale) ->(np.array, float):
    images = []
    widths = []
    for box in boxes:
        partimage, pixelwidth = translateImageFromBox(image,box,scale)
        images.append(partimage)
        widths.append(pixelwidth)


    total_height = scale * 2
    total_width = np.sum(widths)
    if len(image.shape) > 2:
        total_channels = image.shape[2]
        logging.info("Straightened Multichannelimage has shape ({0},{1},{2})".format(total_height,total_width,total_channels))
        straigtened_image = np.zeros(shape=(total_height, total_width, total_channels), dtype=np.uint8)
    else:
        logging.info("Straightened SingleChannelImage has shape ({0},{1})".format(total_height, total_width))
        straigtened_image = np.zeros(shape=(total_height, total_width), dtype=np.uint8)

    widthincrement = 0
    for index, image in enumerate(images):
        width = widths[index]
        straigtened_image[:total_height,widthincrement:widthincrement+width]= image
        widthincrement += width


    return straigtened_image, widthincrement









def translateImageFromBox(image, box, scale) -> (np.array, int):
    height = scale * 2
    width = np.linalg.norm(box[1] - box[2])

    pts1 = np.float32(box)
    pts2 = np.float32([[0, height], [0, 0], [width, 0], [width, height]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    pixelwidth = int(round(width))
    dst = cv2.warpPerspective(image, M, (pixelwidth, int(height)))

    return dst, pixelwidth