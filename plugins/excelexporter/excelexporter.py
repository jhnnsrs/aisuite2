import logging

import h5py
import os

from plugins.standard.plugin import Plugin


class ExcelExporter(Plugin):

    def __init__(self):
        super(ExcelExporter,self).__init__()
        self.plannedH5Files = []
        self.plannedSamples = []
        self.plannedDataKeys = []
        self.plannedRoiKeys = []
        self.plannedStageKey = []

    def exportSingleH5Files(self, plannedH5Files = None):
        logging.info('Starting Export Process')
        plannedH5Files = plannedH5Files if plannedH5Files is not None else self.plannedH5Files
        for h5file in plannedH5Files:
            logging.info('Starting Export Process of H5File {0}'.format(h5file))
            self.exportH5FileFromFilepath(h5file)


    def exportAccumulatedH5Files(self,plannedH5Files = None, exportdir = None):
        logging.info('Starting Export Process')
        plannedH5Files = plannedH5Files if plannedH5Files is not None else self.plannedH5Files

        #get current timestamp for best export
        import datetime, time
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')

        dirname = os.path.dirname(plannedH5Files[0])
        filename = "Export {0}.xlsx".format(st)
        filepath = exportdir if exportdir else os.path.join(dirname, filename)
        from openpyxl import Workbook
        wb = Workbook()

        ws = wb.active
        writefirstline = True
        for h5filepath in plannedH5Files:
            logging.info('Starting Export Process of H5File {0}'.format(h5filepath))
            h5 = h5py.File(h5filepath, "r")
            preparedws = self.getExcelData(h5file=h5,writefirstline=writefirstline,prependFileName=h5filepath)
            for line in preparedws:
                ws.append(line)
            writefirstline = False


        logging.info("SAVING FILE TO {0}".format(filepath))
        wb.save(filepath)

    def exportH5FileFromFilepath(self,h5filepath, exportdir=None):
        h5 = h5py.File(h5filepath, "r")
        dirname = os.path.dirname(h5filepath)
        filename = os.path.basename(h5filepath)
        filepath = exportdir if exportdir else os.path.join(dirname, "{0}.xlsx".format(filename))
        from openpyxl import Workbook
        wb = Workbook()

        # grab the active worksheet
        ws = wb.active
        preparedws = self.getExcelData(h5file=h5)
        for line in preparedws:
            ws.append(line)

        logging.info("SAVING FILE TO {0}".format(filepath))
        wb.save(filepath)

    def getExcelData(self, h5file,writefirstline=True,prependFileName=None):

        ws = []
        datakeys = [key for key in h5file["Data"].keys()]
        firstlinewritten = False
        skippedvalue = False
        for datakey in datakeys:
            dataobject = h5file["Data"][datakey]
            #TODO: Export image here as well
            dataexportraw = []
            for key in self.plannedDataKeys:
                try:
                    if "/" in key:
                        keytree = key.split("/")
                        dataexportraw.append(dataobject[keytree[0]].attrs[keytree[1]])
                    else:
                        dataexportraw.append(dataobject.attrs[key])
                except:
                    dataexportraw.append("Error with key: {0}".format(key))
            dataexport = []

            for element in dataexportraw:
                elements = "None"
                try:
                    #HELPS WITH WRONGLY SET PARAMETERS
                    if type(element) is not int or not float:
                        elements = str(element)
                except:
                    skippedvalue = True
                finally:
                    dataexport.append(elements)

            if firstlinewritten is False and writefirstline is True:
                # is setting the header for the file
                firstline = [key for key in self.plannedDataKeys]
                if prependFileName is not None: firstline = ["Filename"] + firstline
                print(firstline)
                ws.append(firstline)
                firstlinewritten = True
            
            if prependFileName is not None: dataexport = [prependFileName] + dataexport
            ws.append(dataexport)

        if skippedvalue == True: logging.info("Skipped some values because of incompatible schema")

        return ws



    def exportSampleList(self,sampleList = None):

        sampleList = sampleList if sampleList is not None else self.plannedSamples
        for sample in sampleList:
            self.exportSample(sample)


    def exportSample(self,sample = None):
        pass




