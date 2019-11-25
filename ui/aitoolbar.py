import logging

from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class PanOnlyToolbar(NavigationToolbar):
    # only display the buttons we need

    def __init__(self,canvas,imagewidget,*args, **kwargs):
        super(PanOnlyToolbar, self).__init__(parent=imagewidget,canvas=canvas,*args, **kwargs)
        self.name = "Hannes"
        self.imageWidget = imagewidget
        self.setOrientation(Qt.Vertical)
        self.setFixedSize(50,500)

    def home(self,*args,**kwargs):
        self.imageWidget.onHome()
        super(PanOnlyToolbar,self).home(*args,**kwargs)

    def pan(self,*args,**kwargs):
        super(PanOnlyToolbar,self).pan(*args,**kwargs)
        if self._active == 'PAN':
            logging.info("Pan Activated")
            self.imageWidget.setLock(True)
        else:
            logging.info("Pan Deactivated")
            self.imageWidget.setLock(False)

    def zoom(self,*args,**kwargs):
        super(PanOnlyToolbar, self).zoom(*args, **kwargs)
        if self._active == 'ZOOM':
            logging.info("Zoom Activated")
            self.imageWidget.setLock(True)
        else:
            logging.info("Zoom Deactivated")
            self.imageWidget.setLock(False)
