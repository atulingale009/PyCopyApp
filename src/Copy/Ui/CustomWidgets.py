#!/usr/bin/env python3

__author__ = 'atul'

from PyQt4 import QtGui, QtCore
import os
from Copy.Utils import AtUtils


class DNDTableWidget(QtGui.QTableWidget):
    f_dest_col = 3
    f_size_col = 2
    f_name_col = 1
    f_src_col = 0

    def __init__(self, arg):
        print("in __init__")
        super(DNDTableWidget, self).__init__(arg)


    def dragEnterEvent(self, event):
        if self.can_drop(event):
            event.acceptProposedAction()
        else:
            super(DNDTableWidget, self).dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():

            """
                Checking Data
            ...
            """
            for url in event.mimeData().urls():
                urlpath = url.path()
                if os.path.isdir(urlpath):
                    self.scan_dir(urlpath)
                else:
                    self.add_next_row_with(urlpath)
            print("Emited 'addednewrows'")
            self.emit(QtCore.SIGNAL("updateDest()"))
            event.acceptProposedAction()

        else:
            super(DNDTableWidget, self).dropEvent(event)

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    """
        Check if dragged data can be droped
    """

    def can_drop(self, event):
        return event.mimeData().hasUrls()

    """
        Scans given directory for files
    """

    def scan_dir(self, root):
        for dirpath, dirnames, filenames in os.walk(root):
            for filename in filenames:
                self.add_next_row_with(os.path.join(dirpath, filename))

    """
        Checks if given file is valid to import in table or not
    """

    def is_valid_file(self, filepath):
        return True

    def add_next_row_with(self, filepath):
        if self.is_valid_file(filepath) and not self.findItems(filepath, QtCore.Qt.MatchExactly):
            r_index = self.rowCount()
            self.insertRow(r_index)

            # Source column
            item = QtGui.QTableWidgetItem(filepath)
            self.setItem(r_index, self.f_src_col, item)

            # Name column
            item = QtGui.QTableWidgetItem(os.path.split(filepath)[1])
            self.setItem(r_index, self.f_name_col, item)

            # Size column
            size = os.path.getsize(filepath)
            item = QtGui.QTableWidgetItem(AtUtils.get_size_to_show(size, 'B'))
            item.realSize = size
            self.setItem(r_index, self.f_size_col, item)
            return True
        else:
            return False

    def update_dest(self, r_ndex, filepath):
        item = QtGui.QTableWidgetItem(filepath)
        self.setItem(r_ndex, self.f_dest_col, item)

    def get_dest_path(self, r_ndex):
        return self.item(r_ndex, self.f_dest_col).text()

    def update_copy_status(self, r_ndex, ok, err=None):
        item = self.item(r_ndex, self.f_dest_col)
        if not item:
            return
        color = QtGui.QColor(0, 50, 0) if ok else QtGui.QColor(255, 0, 0)
        item.setBackground(color)
        item.setTextColor(QtGui.QColor(255, 255, 255))
        if err:
            item.setToolTip("Error:{0}".format(err))
        # self.setItem(r_ndex, self.f_dest_col, item)
