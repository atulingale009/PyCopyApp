#!/usr/bin/env python3

__author__ = 'atul'

from PyQt4 import QtGui
from Copy import App
import sys

def main(arg):
    app = QtGui.QApplication(arg)
    w = App.App()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)