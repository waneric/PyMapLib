# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\work\geo\gabbs\gui\ui\DlgLayerStyle.ui'
#
# Created: Sat Sep 12 22:55:06 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_DlgLayerStyle(object):
    def setupUi(self, DlgLayerStyle):
        DlgLayerStyle.setObjectName(_fromUtf8("DlgLayerStyle"))
        DlgLayerStyle.resize(320, 320)
        self.verticalLayout = QtGui.QVBoxLayout(DlgLayerStyle)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gBoxSymbol = QtGui.QGroupBox(DlgLayerStyle)
        self.gBoxSymbol.setObjectName(_fromUtf8("gBoxSymbol"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.gBoxSymbol)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelColor = QtGui.QLabel(self.gBoxSymbol)
        self.labelColor.setObjectName(_fromUtf8("labelColor"))
        self.horizontalLayout_2.addWidget(self.labelColor)
        self.labelColorDisplay = QtGui.QLabel(self.gBoxSymbol)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelColorDisplay.sizePolicy().hasHeightForWidth())
        self.labelColorDisplay.setSizePolicy(sizePolicy)
        self.labelColorDisplay.setMinimumSize(QtCore.QSize(24, 24))
        self.labelColorDisplay.setAutoFillBackground(True)
        self.labelColorDisplay.setText(_fromUtf8(""))
        self.labelColorDisplay.setObjectName(_fromUtf8("labelColorDisplay"))
        self.horizontalLayout_2.addWidget(self.labelColorDisplay)
        self.btnChangeColor = QtGui.QPushButton(self.gBoxSymbol)
        self.btnChangeColor.setObjectName(_fromUtf8("btnChangeColor"))
        self.horizontalLayout_2.addWidget(self.btnChangeColor)
        self.verticalLayout.addWidget(self.gBoxSymbol)
        self.gBoxRendering = QtGui.QGroupBox(DlgLayerStyle)
        self.gBoxRendering.setObjectName(_fromUtf8("gBoxRendering"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.gBoxRendering)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelTransparency = QtGui.QLabel(self.gBoxRendering)
        self.labelTransparency.setObjectName(_fromUtf8("labelTransparency"))
        self.horizontalLayout.addWidget(self.labelTransparency)
        self.labelTickStart = QtGui.QLabel(self.gBoxRendering)
        self.labelTickStart.setObjectName(_fromUtf8("labelTickStart"))
        self.horizontalLayout.addWidget(self.labelTickStart)
        self.sliderTransparency = QtGui.QSlider(self.gBoxRendering)
        self.sliderTransparency.setMaximum(100)
        self.sliderTransparency.setOrientation(QtCore.Qt.Horizontal)
        self.sliderTransparency.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sliderTransparency.setTickInterval(10)
        self.sliderTransparency.setObjectName(_fromUtf8("sliderTransparency"))
        self.horizontalLayout.addWidget(self.sliderTransparency)
        self.labelTickEnd = QtGui.QLabel(self.gBoxRendering)
        self.labelTickEnd.setObjectName(_fromUtf8("labelTickEnd"))
        self.horizontalLayout.addWidget(self.labelTickEnd)
        self.verticalLayout.addWidget(self.gBoxRendering)
        self.btnBox = QtGui.QDialogButtonBox(DlgLayerStyle)
        self.btnBox.setOrientation(QtCore.Qt.Horizontal)
        self.btnBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btnBox.setObjectName(_fromUtf8("btnBox"))
        self.verticalLayout.addWidget(self.btnBox)

        self.retranslateUi(DlgLayerStyle)
        QtCore.QObject.connect(self.btnBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DlgLayerStyle.accept)
        QtCore.QObject.connect(self.btnBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DlgLayerStyle.reject)
        QtCore.QMetaObject.connectSlotsByName(DlgLayerStyle)

    def retranslateUi(self, DlgLayerStyle):
        DlgLayerStyle.setWindowTitle(_translate("DlgLayerStyle", "Layer Style", None))
        self.gBoxSymbol.setTitle(_translate("DlgLayerStyle", "Symbol", None))
        self.labelColor.setText(_translate("DlgLayerStyle", "Simple Label Color", None))
        self.btnChangeColor.setText(_translate("DlgLayerStyle", "Change", None))
        self.gBoxRendering.setTitle(_translate("DlgLayerStyle", "Layer Rendering", None))
        self.labelTransparency.setText(_translate("DlgLayerStyle", "Transparency", None))
        self.labelTickStart.setText(_translate("DlgLayerStyle", "0", None))
        self.labelTickEnd.setText(_translate("DlgLayerStyle", "100", None))

