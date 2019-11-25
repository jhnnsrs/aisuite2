

class Settings:

    def __init__(self):

        self.seriesname = None
        self.overlapthreshold = 0.3
        self.filename = "h5file.h5"
        self.directory = ""
        self.t = 0
        import logic.projections as projections
        self.availableProjections = [("MaxISP", projections.maxisp),
                                     ("SlicedMaxISP", projections.slicedmaxisp)
                                     ]

        import logic.postprocessing as postprocessing
        self.availablePostProcessing = [("Void", postprocessing.void),
                                        ("Sobel (Unblurred)", postprocessing.sobelunblurred),
                                        ("Sobel (Blurred)", postprocessing.sobelblurred),
                                        ("Canny", postprocessing.canny),
                                        ("Selective Color", postprocessing.color),
                                        ("Selective Intensity", postprocessing.channelintensity),
                                        ("Overlap", postprocessing.overlap),
                                        ("Roberts Cross", postprocessing.robertoperator),
                                        ("Prewitt", postprocessing.prewitt),
                                        ("LaPlace", postprocessing.laplace),
                                        #("Harris Corner",postprocessing.harrisCorner)

                                        ]
        import logic.calculators as calculators
        self.availableCalculators = [("Standard (Engelhardt 2017)",calculators.rectangleAdvanced),
                                     ("Old",calculators.rectangleStandard)]

        import logic.transformers as transformers
        self.availableTransformers = [("Standard (Engelhardt 2017",transformers.transformROItoRectangle)]
        import logic.mappings as maps
        self.availableMappings = [("Normal", maps.standard)]

        # Global settings can't be altered through settingsFile
        # Changes here render h5files not readable by different version
        self.flagsseperator = "#"
        self.filepath = ""
        self.rmapping = [[0],[0]] # Mapped Channels, Mapped Structure
        self.gmapping = [[1],[1]]
        self.bmapping = [[2],[2]]
        self.version = "1.5"
        self.name = "AISelect "

        self.mappedchannelnames = ["(R) Alexa583 (gp-NeuN,TOPRO)","(G) Alexa583 (bIVSpec)","(B) Alexa583 (TOPRO)"]


        #will be set after mapping
        self.mapping = self.availableMappings[0][1]
        self.projection = self.availableProjections[0][1]
        self.postprocess = self.availablePostProcessing[0][1]
        self.calculator = self.availableCalculators[0][1]
        self.transformer = self.availableTransformers[0][1]

        #stage specifigc
        self.startstage = 0
        self.endstage = 0

        self.selectedmapping = 0
        self.selectedprojection = 0
        self.selectedpostprocess = 0
        self.selectedcalculator = 0
        self.selectedtransformer = 0

        self.saveBioImageToHDF = False
        # Spefific Date read from Userpreferences
        # These settings are global for each instance
        self.series = 0
        self.base_scale = 1.5 #ImageWidget ZoomFactor
        self.standard_mapping = [[0],[1],[2]]


        # Load from local settings file in same filepath or from
        # fallback global settings file
        self.selectiveChannel = 0

        self.colouralpha = 0.6
        self.scale = 10
        self.threshold = 0.2
        self.flags = ["",""]
        self.aischannel = 0
        self.dataimagesize = 5
        #Load From File


        #Will Load From File

        self.mapping_colouredstructure = ["gpNeuN","rbVSpec","TOPRO","rbGAB4","gtCFOS"]
        self.mapping_channels = ["R","G","B","C1","C2","C3","C4","C5"]
        self.channelnames = ["R","G","B"] #will be loaded by File
        self.startstack = 0
        self.endstack = 10 #needs to be set correctly

    def getMappedChannelNames\
                    (self):
        rchannel = "(R) {0} ({1})".format(",".join([self.getChannelName(i) for i in self.rmapping[0]]), ",".join([self.getStructureName(i) for i in self.rmapping[1]]))
        gchannel = "(G) {0} ({1})".format(",".join([self.getChannelName(i) for i in self.gmapping[0]]),",".join([self.getStructureName(i)  for i in self.gmapping[1]]))
        bchannel = "(B) {0} ({1})".format(",".join([self.getChannelName(i) for i in self.bmapping[0]]),",".join([self.getStructureName(i)  for i in self.bmapping[1]]))
        return (rchannel,gchannel,bchannel)

    def getChannelName(self,i):
        try:
            #catches if settings file is not big enough
            name = self.channelnames[i]
        except IndexError:
            name = "None"
        return name

    def getStructureName(self,i):
        try:
            name = self.mapping_colouredstructure[i]
        except IndexError:
            name = "None"
        return name


    def getHDF(self):
        return [("Flags",self.flagsseperator.join(self.flags)),
                ("R-Channel",self.rmapping),
                ("G-Channel",self.gmapping),
                ("")]




