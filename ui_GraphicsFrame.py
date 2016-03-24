# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphicsFrame.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_GraphicsFrame(object):
    def setupUi(self, GraphicsFrame):
        GraphicsFrame.setObjectName(_fromUtf8("GraphicsFrame"))
        GraphicsFrame.resize(955, 768)
        GraphicsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        GraphicsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout = QtGui.QVBoxLayout(GraphicsFrame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.screenshotLE = QtGui.QLineEdit(GraphicsFrame)
        self.screenshotLE.setObjectName(_fromUtf8("screenshotLE"))
        self.horizontalLayout.addWidget(self.screenshotLE)
        self.savePB = QtGui.QPushButton(GraphicsFrame)
        self.savePB.setObjectName(_fromUtf8("savePB"))
        self.horizontalLayout.addWidget(self.savePB)
        self.saveAsPB = QtGui.QPushButton(GraphicsFrame)
        self.saveAsPB.setObjectName(_fromUtf8("saveAsPB"))
        self.horizontalLayout.addWidget(self.saveAsPB)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(GraphicsFrame)
        QtCore.QMetaObject.connectSlotsByName(GraphicsFrame)

    def retranslateUi(self, GraphicsFrame):
        GraphicsFrame.setWindowTitle(_translate("GraphicsFrame", "Frame", None))
        self.savePB.setText(_translate("GraphicsFrame", "Save", None))
        self.saveAsPB.setText(_translate("GraphicsFrame", "Save As...", None))

