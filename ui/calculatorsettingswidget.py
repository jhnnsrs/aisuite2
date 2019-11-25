import logging

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QGridLayout, QLabel

from plugins.ui.toolbox import StandardToolbox
from ui.selectors import CalculatorSelector, TransformerSelector
from ui.valueselector import ValueSelector


class CalculatorSettingsGroup(QGroupBox):
    def __init__(self, name, routine: StandardToolbox):
        super().__init__(name)
        self.routine = routine

        self.layout  = QGridLayout()

        self.initUI()


    def reset(self):
        for i in reversed(range(self.layout.count())):
            widgetToRemove = self.layout.itemAt(i).widget()
            # remove it from the layout list
            self.layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

        logging.info("Calculator and Transformation Settings reseted")

        self.initUI()

    def initUI(self):
        self.calculator_label = QLabel("Calculator")
        self.calculator_select = CalculatorSelector(self.routine, self.calculatorChanged)

        self.transformer_label = QLabel("Transformer")
        self.transformer_select = TransformerSelector(self.routine,self.transformerChanged)

        self.layout.addWidget(self.calculator_select,0,1)
        self.layout.addWidget(self.calculator_label,0,0)
        self.layout.addWidget(self.transformer_select,1,1)
        self.layout.addWidget(self.transformer_label,1,0)

        self.setLayout(self.layout)

    def calculatorChanged(self,calculator):
        self.routine.settings.calculator = calculator

    def transformerChanged(self,transformer):
        self.routine.settings.transformer = transformer