
import bioformats
import numpy as np
import javabridge
from bs4 import BeautifulSoup
import logging, os

from structures.biometa import BioMeta
from structures.bioimage import BioImage

javabridge.start_vm(class_path=bioformats.JARS)

def loadBioImageFromFile(filepath) -> BioImage:
    pass

def getSeriesNamesFromFile(filepath):
    meta = loadBioMetaFromFile(filepath)
    allmeta = meta.metadata.findAll("Image")

    serieslist = []
    for series in allmeta:
     serieslist.append(series.attrs["Name"])

    return serieslist


def loadFile(filepath) -> (BioMeta,BioImage):
    meta = loadBioMetaFromFile(filepath)
    image = loadBioImageFromFile(filepath)
    return meta, image

def loadBioMetaFromFile(filepath) -> BioMeta:
    biometa = BioMeta()

    try:
        biometa.unparsed = bioformats.get_omexml_metadata(filepath)
        biometa.metadata = BeautifulSoup(biometa.unparsed, "xml")
    except Exception as e:
        raise e
    return biometa


def loadBioMetaSeriesFromFile(filepath, series):
    meta = loadBioMetaFromFile(filepath)
    allmeta = meta.metadata.findAll("Image")
    assert series < len(allmeta), "Series to big for File"

    meta.valid = True
    # Basic Physical Data is Loaded
    try:
        seriesmeta = allmeta[series]

        meta.date = str(seriesmeta.find("AcquisitionDate").contents[0]) if seriesmeta.find("AcquisitionDate") is not None else "NOT-SET"
        meta.sizex = int(seriesmeta.find("Pixels").attrs["SizeX"]) if seriesmeta.find("Pixels").attrs["SizeX"] is not None else 0
        meta.sizey = int(seriesmeta.find("Pixels").attrs["SizeY"]) if seriesmeta.find("Pixels").attrs["SizeY"] is not None else 0
        meta.sizez = int(seriesmeta.find("Pixels").attrs["SizeZ"]) if seriesmeta.find("Pixels").attrs["SizeZ"] is not None else 0
        meta.frames = int(seriesmeta.find("Pixels").attrs["SizeT"]) if seriesmeta.find("Pixels").attrs["SizeT"] is not None else 0
        meta.sizet = int(seriesmeta.find("Pixels").attrs["SizeT"]) if seriesmeta.find("Pixels").attrs["SizeT"] is not None else 0
        meta.sizec = int(seriesmeta.find("Pixels").attrs["SizeC"]) if seriesmeta.find("Pixels").attrs["SizeC"] is not None else 0

        meta.physicalsizex = float(seriesmeta.find("Pixels").attrs.get("PhysicalSizeX",1)) or 1
        meta.physicalsizey = float(seriesmeta.find("Pixels").attrs.get("PhysicalSizeY",1)) or 1
        meta.physicalsizexunit = seriesmeta.find("Pixels").attrs.get("PhysicalSizeXUnit","pix") or "pix"
        meta.physicalsizeyunit = seriesmeta.find("Pixels").attrs.get("PhysicalSizeYUnit","pix") or "pix"

    except Exception as e:

        raise e
    finally:
        meta.series = series

    # Try to Load ChannelNames FallBack to R,G,B notation
    channelexplain = ["R","G","B","C4","C5","C6","C7","C8","C9"]
    try:
        meta.channellist = [i.attrs["Name"] for index, i in enumerate(allmeta[series].findAll("Channel"))]
    except KeyError:
        logging.info("File has no valid ChannelNames. Defaulting to Standard Range")
        meta.channellist = [channelexplain[i] for i in range(meta.sizec)]

    assert len(meta.channellist) == meta.sizec, "Channels are not defined correctly"

    # Load SeriesName
    try:
        meta.seriesname = allmeta[series].attrs["Name"]
    except KeyError:
        logging.info("File did not specify SeriesName")
        meta.seriesname = "Not Specified"

    # Load FileName
    meta.dirpath, meta.filename = os.path.split(filepath)

    # Set Shape
    meta.shape = (meta.sizex, meta.sizey, meta.sizec, meta.sizez, meta.sizet)

    return meta


def loadBioImageSeriesFromFile(filepath, meta: BioMeta) -> BioImage:
    bioimage = BioImage()


    assert meta.shape is not None, "No parsed BioMeta provided"
    file = np.zeros(meta.shape)
    try:
        # loads a cached reader that reads every frame
        with bioformats.ImageReader(filepath, perform_init=True) as reader:
            for c in range(meta.sizec):
                for z in range(meta.sizez):
                    for t in range(meta.sizet):

                        # bioformats appears to swap axes for tif images and read all three channels at a time for RGB
                        im1 = reader.read(c=c, z=z, t=t, series=meta.series, rescale=True, channel_names=None)
                        if im1.ndim == 3:
                            if im1.shape[2] == 3:
                                # Three channels are red
                                im2 = im1[:, :, c]
                            else:
                                im2 = im1
                        else:
                            im2 = im1
                        if (meta.sizex == im2.shape[1]) and (meta.sizey == im2.shape[0]) and not meta.sizex == meta.sizey:
                            # x and y are swapped
                            logging.warning("Image might be transposed. Swapping X and Y")
                            im3 = im2.transpose()
                        else:
                            im3 = im2

                        file[:, :, c, z, t] = im3

        logging.info("BioImage Parsed")
    except Exception as e:
        logging.error("Something went wrong whilst parsing the BioImageFile")
        logging.error(e)
    finally:
        bioformats.clear_image_reader_cache()

    bioimage.file = file
    bioimage.shape = meta.shape
    bioimage.filepath = filepath

    return bioimage


def loadSeriesFromFile(filepath,series) -> (BioMeta,BioImage):


    meta = loadBioMetaSeriesFromFile(filepath,series)
    image = loadBioImageSeriesFromFile(filepath,meta)
    #javabridge.kill_vm() right now thsi seems necessary

    return meta, image


