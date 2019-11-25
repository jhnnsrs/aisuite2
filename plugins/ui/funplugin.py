import logging

from plugins.standard.plugin import Plugin
from ui.fundialaogwidget import FunDialogPlayer


class FunPlugin(Plugin):

    def __init__(self):
        super(FunPlugin,self).__init__()
        logging.info("Fun Plugin initialized")

        self.fundialog = FunDialogPlayer()


    def showFun(self):
        self.fundialog.start()


    def hideFun(self):
        self.fundialog.stop()

