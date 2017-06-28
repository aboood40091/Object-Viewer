#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Object Viewer
# Version v1.0
# Copyright © 2017 AboodXD

"""main.py: the Main executable."""

import json, os, struct, sys

from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt

class ObjectPickerWidget(QtWidgets.QListView):
    """
    Widget that shows a list of available objects
    """

    def __init__(self):
        """
        Initializes the widget
        """
        super(ObjectPickerWidget, self).__init__()

        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setIconSize(QtCore.QSize(120,120))
        self.setGridSize(QtCore.QSize(250,250))
        self.setMovement(QtWidgets.QListView.Static)
        self.setBackgroundRole(QtGui.QPalette.BrightText)
        self.setWrapping(False)
        self.setMinimumHeight(240)

        self.objmodel = QtGui.QStandardItemModel()
        self.setModel(self.objmodel)

    def addObjectsFromFolder(self):
        top_folder = QtWidgets.QFileDialog.getExistingDirectory(None, "Open Folder containing Objects")

        if not top_folder: return

        for file in os.listdir(top_folder):
            if file.endswith(".json"):
                dir = top_folder + "/"

                with open(dir + file) as inf:
                    jsonData = json.load(inf)

                pm = QtGui.QPixmap(dir + jsonData["img"])

                pm = pm.scaledToWidth(pm.width() * 32/60, Qt.SmoothTransformation)
                if pm.width() > 256:
                    pm = pm.scaledToWidth(256, Qt.SmoothTransformation)
                if pm.height() > 256:
                    pm = pm.scaledToHeight(256, Qt.SmoothTransformation)

                self.itemsize = QtCore.QSize(pm.width() + 4, pm.height() + 4)

                self.objmodel.appendRow(QtGui.QStandardItem(QtGui.QIcon(pm), os.path.splitext(file)[0]))

        self.setModel(self.objmodel)

    def addObjectsFromObjectFolder(self):
        top_folder = QtWidgets.QFileDialog.getExistingDirectory(None, "Open Folder containing Object folders")

        if not top_folder: return

        for folder in os.listdir(top_folder):
            for file in os.listdir(top_folder + "/" + folder):
                if file.endswith(".json"):
                    dir = top_folder + "/" + folder + "/"

                    with open(dir + file) as inf:
                        jsonData = json.load(inf)

                    pm = QtGui.QPixmap(dir + jsonData["img"])

                    pm = pm.scaledToWidth(pm.width() * 32/60, Qt.SmoothTransformation)
                    if pm.width() > 256:
                        pm = pm.scaledToWidth(256, Qt.SmoothTransformation)
                    if pm.height() > 256:
                        pm = pm.scaledToHeight(256, Qt.SmoothTransformation)

                    self.itemsize = QtCore.QSize(pm.width() + 4, pm.height() + 4)

                    self.objmodel.appendRow(QtGui.QStandardItem(QtGui.QIcon(pm), folder + "/" + os.path.splitext(file)[0]))

        self.setModel(self.objmodel)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Object Viewer v1.0")

        self.obj = QtWidgets.QWidget()

        oel = QtWidgets.QVBoxLayout(self.obj)
        self.createObjectLayout = oel

        self.objPicker = ObjectPickerWidget()
        oel.addWidget(self.objPicker, 1)

        self.obj.setLayout(self.createObjectLayout)

        self.setCentralWidget(self.obj)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        taskMenu = menuBar.addMenu('&Tasks')
        helpMenu = menuBar.addMenu('&Help')

        openFolder = QtWidgets.QAction("&Open Folder containing Objects", self)
        openFolder.triggered.connect(self.openFolder)
        fileMenu.addAction(openFolder)

        openObjectFolder = QtWidgets.QAction("&Open Folder containing Object folders", self)
        openObjectFolder.triggered.connect(self.openObjectFolder)
        fileMenu.addAction(openObjectFolder)

        clearList = QtWidgets.QAction("&Clear list", self)
        clearList.triggered.connect(self.clearList)
        taskMenu.addAction(clearList)

        about = QtWidgets.QAction("&About", self)
        about.triggered.connect(self.about)
        helpMenu.addAction(about)

    def openFolder(self):
        self.clearList()
        self.objPicker.addObjectsFromFolder()

    def openObjectFolder(self):
        self.clearList()
        self.objPicker.addObjectsFromObjectFolder()

    def clearList(self):
        self.obj = QtWidgets.QWidget()

        oel = QtWidgets.QVBoxLayout(self.obj)
        self.createObjectLayout = oel

        self.objPicker = ObjectPickerWidget()
        oel.addWidget(self.objPicker, 1)

        self.obj.setLayout(self.createObjectLayout)

        self.setCentralWidget(self.obj)

    def about(self):
        QtWidgets.QMessageBox.information(self, "About",
        "Object Viewer v1.0\n\n(C) 2017 AboodXD (aboood40091).",
        QtWidgets.QMessageBox.Ok)

if __name__ == '__main__':

    app = QtWidgets.QApplication([sys.argv[0]])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    app.deleteLater()
