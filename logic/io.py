import datetime
import logging

import h5py
import os

import numpy as np

from structures.biometa import BioMeta
from structures.roi import ROI
from structures.roidata import DATA, StraightenedDATA
from structures.sample import Sample
from structures.settings import Settings


def settingsFileToSettings(filepath: str) -> Settings:
    # TODO: Implement
    # TODO: make best fit settings search automatically

    settings = Settings()

    return settings

def HDFtoDATA(hdfdata,settings) -> (int, DATA):
    data = StraightenedDATA.getDataFromHDF(hdfdata,settings)
    return data.key, data

def loadSampleFromHDF(filepath: str, settings: Settings) -> Sample:
    #TODO: Implement Loading ALL Data from Sample
    # Right now only data is loaded
    sample = Sample()


    if h5py.is_hdf5(filepath):
        h5file = h5py.File(filepath, "r")

        try:
            datalist = {}
            for key in h5file["Data"]:
                print(key)
                key, dataobject = HDFtoDATA(h5file["Data"][key],settings)
                datalist[key] = dataobject

            sample.data = datalist

        except KeyError as e:
            print("File {0} doesnt hava data Object: {1}".format(filepath, e))
            pass

    return sample

def settingsToSettingsFile(settings: Settings, filepath: str) -> bool:
    # TODO: Implement

    import configparser
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'ServerAliveInterval': '45',
                         'Compression': 'yes',
                         'CompressionLevel': '9'}

    with open('example.ini', 'w') as configfile:
        config.write(configfile)
    return True


def ROItoHDF(roi: ROI):
    return roi.getHDF()


def DATAtoHDF(data: DATA):
    return data.getHDF()
    pass


def SETTINGStoHDF(settings: Settings):
    pass


def METAtoHDF(meta: BioMeta):
    pass


def saveSampleToHDF(sample: Sample, settings: Settings):



    rchannel, gchannel, bchannel = settings.getMappedChannelNames()

    filename = "Test - {0}.h5".format(rchannel)
    #TODO: Find good naming scheme
    filename = settings.seriesname

    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    filename = str(filename) + ".h5"
    dirname = settings.directory

    h5file = h5py.File(os.path.join(dirname, filename), "w")

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    h5file.attrs['Filename'] = filename

    h5file.attrs["Physicalsize-X"] = sample.biometa.physicalsizex
    h5file.attrs["Physicalsize-Y"] = sample.biometa.physicalsizey
    h5file.attrs["Physicalsize-X-Unit"] = sample.biometa.physicalsizexunit
    h5file.attrs["Physicalsize-Y-Unit"] = sample.biometa.physicalsizeyunit

    h5file.attrs["R"] = rchannel
    h5file.attrs["B"] = bchannel
    h5file.attrs["G"] = gchannel

    h5file.attrs['Creator'] = settings.name
    h5file.attrs['Script-Version'] = settings.version

    h5file.attrs['HDF5_Version'] = h5py.version.hdf5_version
    h5file.attrs['h5py_version'] = h5py.version.version

    # give the HDF5 root some more attributes
    h5file.attrs['File-Time'] = timestamp

    if settings.saveBioImageToHDF:
        bioimagegroup = h5file.create_group("BioImage")
        bioimagegroup.attrs["Unparsed-Meta"] = sample.biometa.unparsed
        nana = np.array(sample.bioimage.file)
        file = bioimagegroup.create_dataset("Numpy-Array",data =nana, compression="gzip",compression_opts=7)

    datagroup = h5file.create_group('Data')
    for key, data in sample.data.items():
        dataitem = datagroup.create_group("Data " + str(data.key))
        dataitem = data.getHDF(dataitem, settings)

    roisgroup = h5file.create_group('ROIs')
    for key, roi in sample.rois.items():
        roiitem = roisgroup.create_group("Roi " + str(roi.key))
        roiitem = roi.getHDF(roiitem, settings)

    transformationssgroup = h5file.create_group('Transformations')
    for key, transformation in sample.transformations.items():
        transformationitem = transformationssgroup.create_group("Transformation " + str(transformation.key))
        transformationitem = transformation.getHDF(transformationitem, settings)

    stagegroup = h5file.create_group('Stages')
    for key, stage in sample.stages.items():
        stageitem= stagegroup.create_group("Stage " + str(stage.key))
        stageitem = stage.getHDF(stageitem ,settings)

    logging.info("HDF5 Written")
    h5file.close()


def saveSampleToExcel(sample: Sample, settings: Settings):
    from openpyxl import Workbook
    wb = Workbook()

    filepath = sample.filename  # TODO Make good filepath

    for data in sample.data:
        data.getExcel()

    pass
