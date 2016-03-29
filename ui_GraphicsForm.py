# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphicsForm.ui'
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

class Ui_GraphicsForm(object):
    def setupUi(self, GraphicsForm):
        GraphicsForm.setObjectName(_fromUtf8("GraphicsForm"))
        GraphicsForm.resize(931, 700)
        self.verticalLayout = QtGui.QVBoxLayout(GraphicsForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit = QtGui.QLineEdit(GraphicsForm)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton_2 = QtGui.QPushButton(GraphicsForm)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtGui.QPushButton(GraphicsForm)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 630, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(GraphicsForm)
        QtCore.QMetaObject.connectSlotsByName(GraphicsForm)

    def retranslateUi(self, GraphicsForm):
        GraphicsForm.setWindowTitle(_translate("GraphicsForm", "Form", None))
        self.pushButton_2.setText(_translate("GraphicsForm", "Save", None))
        self.pushButton.setText(_translate("GraphicsForm", "Save As...", None))

