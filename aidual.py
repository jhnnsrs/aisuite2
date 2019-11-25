import logging
import sys

import matplotlib

matplotlib.use("QT5Agg")

from PyQt5.QtWidgets import QApplication

from ui.flowselector import FlowDialog
from dualline.ui import DualWindow

FLOWS = [
         ("AIDual", DualWindow),
         ]

h_excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    h_excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

logging.basicConfig(stream=sys.stdout,level=logging.INFO)


def main():
    app = QApplication(sys.argv)
    hallo = FlowDialog(FLOWS)

    sys.exit(app.exec_())

if __name__ == '__main__':

    main()