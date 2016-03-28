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
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.cut_plane_CB = QtGui.QCheckBox(GraphicsFrame)
        self.cut_plane_CB.setEnabled(True)
        self.cut_plane_CB.setChecked(True)
        self.cut_plane_CB.setObjectName(_fromUtf8("cut_plane_CB"))
        self.horizontalLayout_2.addWidget(self.cut_plane_CB)
        self.cut_axis_CB = QtGui.QComboBox(GraphicsFrame)
        self.cut_axis_CB.setObjectName(_fromUtf8("cut_axis_CB"))
        self.cut_axis_CB.addItem(_fromUtf8(""))
        self.cut_axis_CB.addItem(_fromUtf8(""))
        self.cut_axis_CB.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.cut_axis_CB)
        self.flip_visible_part_RB = QtGui.QRadioButton(GraphicsFrame)
        self.flip_visible_part_RB.setObjectName(_fromUtf8("flip_visible_part_RB"))
        self.horizontalLayout_2.addWidget(self.flip_visible_part_RB)
        self.cut_plane_pos_S = QtGui.QSlider(GraphicsFrame)
        self.cut_plane_pos_S.setOrientation(QtCore.Qt.Horizontal)
        self.cut_plane_pos_S.setObjectName(_fromUtf8("cut_plane_pos_S"))
        self.horizontalLayout_2.addWidget(self.cut_plane_pos_S)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
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
        QtCore.QObject.connect(self.cut_plane_CB, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cut_axis_CB.setEnabled)
        QtCore.QObject.connect(self.cut_plane_CB, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cut_plane_pos_S.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(GraphicsFrame)

    def retranslateUi(self, GraphicsFrame):
        GraphicsFrame.setWindowTitle(_translate("GraphicsFrame", "Frame", None))
        self.cut_plane_CB.setText(_translate("GraphicsFrame", "Enable cut plane", None))
        self.cut_axis_CB.setItemText(0, _translate("GraphicsFrame", "x", None))
        self.cut_axis_CB.setItemText(1, _translate("GraphicsFrame", "y", None))
        self.cut_axis_CB.setItemText(2, _translate("GraphicsFrame", "z", None))
        self.flip_visible_part_RB.setText(_translate("GraphicsFrame", "flip_visible_part", None))
        self.savePB.setText(_translate("GraphicsFrame", "Save", None))
        self.saveAsPB.setText(_translate("GraphicsFrame", "Save As...", None))

