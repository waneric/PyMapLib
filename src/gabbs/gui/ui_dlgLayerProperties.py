# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\work\geo\gabbs\gui\dlgLayerProperties.ui'
#
# Created: Thu Sep 10 21:58:30 2015
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

class Ui_LayerProperties(object):
    def setupUi(self, LayerProperties):
        LayerProperties.setObjectName(_fromUtf8("LayerProperties"))
        LayerProperties.resize(313, 277)
        self.gridLayout_2 = QtGui.QGridLayout(LayerProperties)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(LayerProperties)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.txtLayerName = QtGui.QLineEdit(LayerProperties)
        self.txtLayerName.setMinimumSize(QtCore.QSize(140, 0))
        self.txtLayerName.setMaximumSize(QtCore.QSize(200, 21))
        self.txtLayerName.setCursorPosition(0)
        self.txtLayerName.setObjectName(_fromUtf8("txtLayerName"))
        self.horizontalLayout.addWidget(self.txtLayerName)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblDisplayField = QtGui.QLabel(LayerProperties)
        self.lblDisplayField.setObjectName(_fromUtf8("lblDisplayField"))
        self.horizontalLayout_2.addWidget(self.lblDisplayField)
        self.cboDisplayFieldName = QtGui.QComboBox(LayerProperties)
        self.cboDisplayFieldName.setMinimumSize(QtCore.QSize(140, 0))
        self.cboDisplayFieldName.setMaximumSize(QtCore.QSize(200, 21))
        self.cboDisplayFieldName.setObjectName(_fromUtf8("cboDisplayFieldName"))
        self.horizontalLayout_2.addWidget(self.cboDisplayFieldName)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.frame = QtGui.QFrame(LayerProperties)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkScale = QtGui.QCheckBox(self.frame)
        self.chkScale.setObjectName(_fromUtf8("chkScale"))
        self.gridLayout.addWidget(self.chkScale, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem2 = QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.lblMaxScale = QtGui.QLabel(self.frame)
        self.lblMaxScale.setEnabled(True)
        self.lblMaxScale.setObjectName(_fromUtf8("lblMaxScale"))
        self.horizontalLayout_4.addWidget(self.lblMaxScale)
        self.maxScaleSpinBox = QtGui.QSpinBox(self.frame)
        self.maxScaleSpinBox.setEnabled(True)
        self.maxScaleSpinBox.setMinimumSize(QtCore.QSize(140, 0))
        self.maxScaleSpinBox.setMaximumSize(QtCore.QSize(16777215, 21))
        self.maxScaleSpinBox.setMinimum(1)
        self.maxScaleSpinBox.setMaximum(100000000)
        self.maxScaleSpinBox.setSingleStep(1000)
        self.maxScaleSpinBox.setProperty("value", 1000)
        self.maxScaleSpinBox.setObjectName(_fromUtf8("maxScaleSpinBox"))
        self.horizontalLayout_4.addWidget(self.maxScaleSpinBox)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem3 = QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.lblMinScale = QtGui.QLabel(self.frame)
        self.lblMinScale.setEnabled(True)
        self.lblMinScale.setObjectName(_fromUtf8("lblMinScale"))
        self.horizontalLayout_3.addWidget(self.lblMinScale)
        self.minScaleSpinBox = QtGui.QSpinBox(self.frame)
        self.minScaleSpinBox.setEnabled(True)
        self.minScaleSpinBox.setMinimumSize(QtCore.QSize(140, 0))
        self.minScaleSpinBox.setMaximumSize(QtCore.QSize(16777215, 21))
        self.minScaleSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.minScaleSpinBox.setAccelerated(True)
        self.minScaleSpinBox.setMinimum(1)
        self.minScaleSpinBox.setMaximum(100000000)
        self.minScaleSpinBox.setSingleStep(1000)
        self.minScaleSpinBox.setProperty("value", 1000000)
        self.minScaleSpinBox.setObjectName(_fromUtf8("minScaleSpinBox"))
        self.horizontalLayout_3.addWidget(self.minScaleSpinBox)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 3, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem4, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(LayerProperties)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 5, 0, 1, 1)

        self.retranslateUi(LayerProperties)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LayerProperties.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LayerProperties.reject)
        QtCore.QMetaObject.connectSlotsByName(LayerProperties)

    def retranslateUi(self, LayerProperties):
        LayerProperties.setWindowTitle(_translate("LayerProperties", "Layer properties", None))
        self.label.setText(_translate("LayerProperties", "Layer name", None))
        self.lblDisplayField.setText(_translate("LayerProperties", "Display field", None))
        self.chkScale.setText(_translate("LayerProperties", "Use scale dependent rendering", None))
        self.lblMaxScale.setText(_translate("LayerProperties", "Maximum scale", None))
        self.lblMinScale.setText(_translate("LayerProperties", "Minimum scale", None))

