# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './View/GUI/widget.ui'
#
# Created: Mon Jun 29 22:39:55 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName(_fromUtf8("Widget"))
        Widget.resize(400, 398)
        self.tableWidget = QtGui.QTableWidget(Widget)
        self.tableWidget.setGeometry(QtCore.QRect(30, 60, 331, 331))
        self.tableWidget.setRowCount(15)
        self.tableWidget.setColumnCount(15)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.horizontalHeader().setDefaultSectionSize(20)
        self.tableWidget.verticalHeader().setDefaultSectionSize(20)
        self.gridLayoutWidget = QtGui.QWidget(Widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(29, 10, 346, 41))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.stopButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.gridLayout.addWidget(self.stopButton, 0, 1, 1, 1)
        self.startButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.gridLayout.addWidget(self.startButton, 0, 0, 1, 1)
        self.openButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.gridLayout.addWidget(self.openButton, 0, 2, 1, 1)
        self.resetButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.gridLayout.addWidget(self.resetButton, 0, 3, 1, 1)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(_translate("Widget", "Widget", None))
        self.stopButton.setText(_translate("Widget", "Stop", None))
        self.startButton.setText(_translate("Widget", "Start", None))
        self.openButton.setText(_translate("Widget", "Open", None))
        self.resetButton.setText(_translate("Widget", "Reset", None))

