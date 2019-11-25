import configparser
import logging

import os

from plugins.standard.plugin import Plugin
from structures.settings import Settings


class StandardSettings(Plugin):

    def __init__(self):
        super(StandardSettings, self).__init__()
        logging.info("Standard Settings initialized")

    def loadSettingsFromFile(self, file):
        import logic.projections as projections
        import logic.mappings as maps
        import logic.postprocessing as postprocessing
        # TODO Implement

        self.settings.aischannel = 0
        self.settings.projection = projections.maxisp
        self.settings.mapping = maps.standard
        self.settings.postprocess = postprocessing.void

        self.settings.series = 0

    def loadBioImageSettings(self):
        bioimagesettingspath = os.path.join(self.settings.directory,'immuno.ini')

        #FALLBACK
        if not os.path.isfile(bioimagesettingspath):
            script_dir = os.path.dirname("")
            rel_path = "examples/immuno.ini"
            bioimagesettingspath = os.path.join(script_dir, rel_path)
            if not os.path.isfile(bioimagesettingspath):
                logging.info("NO FILE FOUND")
                return
        logging.info("Opening Config File in {0}".format(bioimagesettingspath))
        import configparser
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(bioimagesettingspath)
        if 'IMMUNOCHANNELS' in config:
            self.settings.mapping_colouredstructure = []
            try:
                for key in config["IMMUNOCHANNELS"]:
                    self.settings.mapping_colouredstructure.append(str(key))
            except:
                logging.info("Something wrong with immuno.ini. Skipping Channel Assignment")
                self.settings.mapping_colouredstructure = ["None","None","None"]

        #self.settings.mapping_colouredstructure.extend("None" * (4 - len(self.settings.mapping_colouredstructure)))
        if 'R-MAPPING' in config:
            self.settings.rmapping[0] = []
            try:
                for key in config["R-MAPPING"]:
                    self.settings.rmapping[0].append(int(key))
            except Exception as e:
                self.settings.rmapping[0] = [0]


        if 'G-MAPPING' in config:
            self.settings.gmapping[0] = []
            try:
                for key in config["G-MAPPING"]:
                    self.settings.gmapping[0].append(int(key))
            except Exception as e:
                self.settings.gmapping[0] = [1]

        if 'B-MAPPING' in config:
            self.settings.bmapping[0] = []
            try:
                for key in config["B-MAPPING"]:
                    self.settings.bmapping[0].append(int(key))
            except Exception as e:
                self.settings.bmapping[0] = [2]


    def saveBioImageSettings(self,filepath):
        logging.info("Saving Settings File")

        # lets create that config file for next time...
        cfgfile = open(filepath, 'w')
        config = configparser.ConfigParser(allow_no_value=True)
        # add the settings to the structure of the file, and lets write it out...
        config.add_section('IMMUNOCHANNELS')
        for channel in self.settings.mapping_colouredstructure:
            config.set('IMMUNOCHANNELS', channel, "")

        config.add_section('R-MAPPING')
        for channel in self.settings.rmapping[0]:
            config.set('R-MAPPING', str(channel), "")

        config.add_section('G-MAPPING')
        for channel in self.settings.gmapping[0]:
            config.set('G-MAPPING', str(channel), "")

        config.add_section('B-MAPPING')
        for channel in self.settings.bmapping[0]:
            config.set('B-MAPPING', str(channel), "")


        config.write(cfgfile)

        cfgfile.close()

