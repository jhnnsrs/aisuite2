from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QSlider


class ValueSelector(QWidget):
    def __init__(self, name, min, max, callback, ismax=False, ismin=False):
        super().__init__()
        self.min = min
        self.max = max
        self.callback = callback
        self.lastvalue = 0
        self.layout = QGridLayout()
        self.valuebox = QLineEdit(self)

        self.label = QLabel(name)
        self.valueslider = QSlider(Qt.Horizontal)

        self.valueslider = QSlider(Qt.Horizontal)
        self.valueslider.setMinimum(self.min)
        self.valueslider.setMaximum(self.max)

        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.valueslider, 1, 0)
        self.layout.addWidget(self.valuebox, 1, 1)

        if ismax == True and ismin == False:
            self.valueslider.setValue(self.max)
            self.valuebox.setText(str(self.max))
            self.ismax = True
            self.ismin = False
        else:
            # If ismax is not set it is a min selector
            self.valueslider.setValue(self.min)
            self.valuebox.setText(str(self.min))
            self.ismax = False
            self.ismin = True

        self.valueslider.valueChanged.connect(self.valuechanged)
        self.valuebox.textChanged.connect(self.valuechanged)

        self.setLayout(self.layout)

    def valuechanged(self, value):
        try:
            value = int(value)
        except ValueError:
            if self.ismax:
                value = self.max
            if self.ismin:
                value = self.min

        if value != self.lastvalue and self.min <= value <= self.max:
            self.callback(value, self.ismax, self.ismin)
            self.lastvalue = value

            self.valueslider.setValue(value)
            self.valuebox.setText(str(value))