# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\work\geo\gabbs\plugins\drawingtool\WidgetDrawingTool.ui'
#
# Created: Wed Nov 11 11:03:53 2015
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

class Ui_WidgetDrawingTool(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(300, 100)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_1 = QtGui.QLabel(Form)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_1)
        self.labelUpLeft = QtGui.QLabel(Form)
        self.labelUpLeft.setText(_fromUtf8(""))
        self.labelUpLeft.setObjectName(_fromUtf8("labelUpLeft"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.labelUpLeft)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.labelButtomRight = QtGui.QLabel(Form)
        self.labelButtomRight.setText(_fromUtf8(""))
        self.labelButtomRight.setObjectName(_fromUtf8("labelButtomRight"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.labelButtomRight)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("WidgetDrawingTool", "Drawing Tool", None))
        self.label_1.setText(_translate("WidgetDrawingTool", "Up Left:", None))
        self.label_2.setText(_translate("WidgetDrawingTool", "Buttom Right:", None))

