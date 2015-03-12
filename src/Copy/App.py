#!/usr/bin/env python3

__author__ = 'atul'

from PyQt4 import QtCore, QtGui
from Copy.Ui import MainWindow
from Copy.Utils import AtUtils
import os
import shutil


class App(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAll(False)
        self.add_slots()

    def setAll(self, reset):
        pass

    def set_target_status_value(self, free, total=None):
        if free > 0:
            used = self.ui.targetStatus.realUsed = total-free
            self.ui.targetStatus.realFree = free
            self.ui.targetStatus.realTotal = total = total if total else self.ui.targetStatus.realTotal
            value = int((used/total) * 100)
            self.ui.targetStatus.setValue(value)

    def update_target_status(self, row, is_copying=True):
        item_val = self.ui.tblFiles.item(row, self.ui.tblFiles.f_size_col).realSize
        free = self.ui.targetStatus.realFree - item_val
        self.set_target_status_value(free)


    """ Returns Void
    a# Adds slots as Qt Designer 4 Do not support custom slots add those slots from this function
    """
    def add_slots(self):
        self.ui.btnCopyToDir.clicked.connect(self.open_copy_to_dir_dialog)
        #self.ui.tblFiles.dragMoved.connect(self.dragMoved)
        #self.ui.tblFiles.dragEntered.connect(self.dragEntered)
        #self.ui.tblFiles.dropped.connect(self.handleDrop)
        #self.emit(QtCore.SIGNAL("updateDest()"))
        self.ui.bxDirLevel.valueChanged.connect(self.update_destination)
        #self.ui.bxDirLevel.valueChanged.connect(self.ui.bxDirLevel.validate)
        self.ui.txtCopyToDir.textChanged.connect(self.update_destination)
        self.ui.btnStartCopy.clicked.connect(self.start_copy)
        QtCore.QObject.connect(self.ui.tblFiles, QtCore.SIGNAL("updateDest()"), self.update_destination)

    """ Returns vaoid
    a# Event handler to update destination column of table
    a# eg after textChanged of txtCopyDir, dropEvent of tblFiles, valueChanged of bxLevelDir
    """
    def update_destination(self, event=None):

        if not self.ui.txtCopyToDir.text():
            return
        # @todo: Create new handler function for text value changed event
        stats = AtUtils.get_free_space_mb(self.ui.txtCopyToDir.text())
        self.set_target_status_value(stats["free"], stats["total"])

        basepath = self.ui.txtCopyToDir.text()

        if basepath and os.path.isdir(basepath) and self.ui.tblFiles.rowCount() > 0:

            level = self.ui.bxDirLevel.value()
            level = level if level else 0
            level += 1
            rows = self.ui.tblFiles.rowCount()
            counter = 0

            while counter < rows:
                srcpath = self.ui.tblFiles.item(counter, 0).text()

                if not os.path.exists(srcpath):
                    """
                        Delete row and decrement row count
                    """
                    self.ui.tblFiles.removeRow(counter)
                    rows -= 1
                    continue

                path_list = srcpath.split(os.sep)
                path_list = path_list[(0-level):] if len(path_list) > level else path_list
                self.ui.tblFiles.update_dest(counter, os.path.join(basepath, *path_list))
                counter += 1

    def start_copy(self):
        rows = self.ui.tblFiles.rowCount()
        counter = 0

        while counter < rows:
            src_path = self.ui.tblFiles.item(counter, 0).text()

            if not os.path.exists(src_path):
                continue
            try:
                dest_path = self.ui.tblFiles.get_dest_path(counter)
                AtUtils.mkdir_p(dest_path)
                shutil.copy2(src_path, dest_path)
                self.ui.tblFiles.update_copy_status(counter, True)
                self.update_target_status(counter)
            except Exception as err:
                self.ui.tblFiles.update_copy_status(counter, False, err)

            counter += 1

    def stop_copy(self):
        pass

    def pause_copy(self):
        pass

    """
    a# Opens file dialog
    """
    def open_copy_to_dir_dialog(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        #dialog.setOption(QtGui.QFileDialog.ShowDirsOnly, True)
        options = QtGui.QFileDialog.ShowDirsOnly
        self.ui.txtCopyToDir.setText(dialog.getExistingDirectory(self, '/', self.ui.lblCopyTo.text(), options))

