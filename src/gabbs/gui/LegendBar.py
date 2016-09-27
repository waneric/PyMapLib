from PyQt4.QtCore import *
from PyQt4.QtGui import *
from gabbs.MapUtils import iface

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class LegendBar:
    def __init__(self):
        self.colorBarFrame = QFrame(iface.mapCanvas)
        self.colorBarFrame.setGeometry(QRect(4, 5, 476, 31))
        self.colorBarFrame.setObjectName(_fromUtf8("colorBarFrame"))

        # print str(iface.mapCanvas.size().width())
        # print str(iface.mapCanvas.size().height())
        # self.barWidth = int( (iface.mapCanvas.size().width() - 40) / 10 )
        self.barWidth = 44

        self.colorBars = []
        self.color1 = QWidget(self.colorBarFrame)
        self.color1.setGeometry(QRect(20, 5, self.barWidth, 21))
        self.color1.setStyleSheet(_fromUtf8("background-color: rgba(107, 255, 147,220);"))
        self.color1.setObjectName(_fromUtf8("color1"))
        self.color2 = QWidget(self.colorBarFrame)
        self.color2.setGeometry(QRect(64, 5, self.barWidth, 21))
        self.color2.setStyleSheet(_fromUtf8("background-color: rgba(96, 230, 148,220);"))
        self.color2.setObjectName(_fromUtf8("color2"))
        self.color3 = QWidget(self.colorBarFrame)
        self.color3.setGeometry(QRect(108, 5, self.barWidth, 21))
        self.color3.setStyleSheet(_fromUtf8("background-color: rgba(85, 205, 150,220);"))
        self.color3.setObjectName(_fromUtf8("color3"))
        self.color4 = QWidget(self.colorBarFrame)
        self.color4.setGeometry(QRect(152, 5, self.barWidth, 21))
        self.color4.setStyleSheet(_fromUtf8("background-color: rgba(74, 180, 152,220);"))
        self.color4.setObjectName(_fromUtf8("color4"))
        self.color5 = QWidget(self.colorBarFrame)
        self.color5.setGeometry(QRect(196, 5, self.barWidth, 21))
        self.color5.setStyleSheet(_fromUtf8("background-color: rgba(63, 155, 154,220);"))
        self.color5.setObjectName(_fromUtf8("color5"))
        self.color6 = QWidget(self.colorBarFrame)
        self.color6.setGeometry(QRect(240, 5, self.barWidth, 21))
        self.color6.setStyleSheet(_fromUtf8("background-color: rgba(53, 131, 156,220);"))
        self.color6.setObjectName(_fromUtf8("color6"))
        self.color7 = QWidget(self.colorBarFrame)
        self.color7.setGeometry(QRect(284, 5, self.barWidth, 21))
        self.color7.setStyleSheet(_fromUtf8("background-color: rgba(42, 106, 158,220);"))
        self.color7.setObjectName(_fromUtf8("color7"))
        self.color8 = QWidget(self.colorBarFrame)
        self.color8.setGeometry(QRect(328, 5, self.barWidth, 21))
        self.color8.setStyleSheet(_fromUtf8("background-color: rgba(31, 81, 160,220);"))
        self.color8.setObjectName(_fromUtf8("color8"))
        self.color9 = QWidget(self.colorBarFrame)
        self.color9.setGeometry(QRect(372, 5, self.barWidth, 21))
        self.color9.setStyleSheet(_fromUtf8("background-color: rgba(20, 56, 162,220);"))
        self.color9.setObjectName(_fromUtf8("color9"))
        self.color10 = QWidget(self.colorBarFrame)
        self.color10.setGeometry(QRect(416, 5, self.barWidth, 21))
        self.color10.setStyleSheet(_fromUtf8("background-color: rgba(10, 32, 164,220);"))
        self.color10.setObjectName(_fromUtf8("color10"))

        self.colorBars.append(self.color1)
        self.colorBars.append(self.color2)
        self.colorBars.append(self.color3)
        self.colorBars.append(self.color4)
        self.colorBars.append(self.color5)
        self.colorBars.append(self.color6)
        self.colorBars.append(self.color7)
        self.colorBars.append(self.color8)
        self.colorBars.append(self.color9)
        self.colorBars.append(self.color10)

        self.legendValues = []
        self.l0 = QLabel(self.colorBarFrame)
        self.l0.setGeometry(QRect(22, 7, 41, 16))
        self.l0.setObjectName(_fromUtf8("l0"))
        self.l1 = QLabel(self.colorBarFrame)
        self.l1.setGeometry(QRect(55, 7, 41, 16))
        self.l1.setObjectName(_fromUtf8("l1"))
        self.l2 = QLabel(self.colorBarFrame)
        self.l2.setGeometry(QRect(99, 7, 41, 16))
        self.l2.setObjectName(_fromUtf8("l2"))
        self.l3 = QLabel(self.colorBarFrame)
        self.l3.setGeometry(QRect(143, 7, 41, 16))
        self.l3.setObjectName(_fromUtf8("l3"))
        self.l4 = QLabel(self.colorBarFrame)
        self.l4.setGeometry(QRect(187, 7, 41, 16))
        self.l4.setObjectName(_fromUtf8("l4"))
        self.l5 = QLabel(self.colorBarFrame)
        self.l5.setGeometry(QRect(231, 7, 41, 16))
        self.l5.setObjectName(_fromUtf8("l5"))
        self.l6 = QLabel(self.colorBarFrame)
        self.l6.setGeometry(QRect(275, 7, 41, 16))
        self.l6.setObjectName(_fromUtf8("l6"))
        self.l7 = QLabel(self.colorBarFrame)
        self.l7.setGeometry(QRect(319, 7, 41, 16))
        self.l7.setObjectName(_fromUtf8("l7"))
        self.l8 = QLabel(self.colorBarFrame)
        self.l8.setGeometry(QRect(363, 7, 41, 16))
        self.l8.setObjectName(_fromUtf8("l8"))
        self.l9 = QLabel(self.colorBarFrame)
        self.l9.setGeometry(QRect(407, 7, 41, 16))
        self.l9.setObjectName(_fromUtf8("l9"))


        self.legendValues.append(self.l0)
        self.legendValues.append(self.l1)
        self.legendValues.append(self.l2)
        self.legendValues.append(self.l3)
        self.legendValues.append(self.l4)
        self.legendValues.append(self.l5)
        self.legendValues.append(self.l6)
        self.legendValues.append(self.l7)
        self.legendValues.append(self.l8)
        self.legendValues.append(self.l9)

    def show(self):

        self.colorBarFrame.show()

        return

    def hide(self):

        self.colorBarFrame.hide()

        return

    def setColors(self, arr):
        if len(arr) != 10:
            raise ValueError("10 values (set of r,g,b,a) need to be provided")
        
        for i in range(0,10):   

            if len(arr[i]) != 4:
                raise ValueError("Set of r,g,b,a need to be provided as a list")


        for i in range(0,10):   
            cs = "background-color: rgba(" + str(arr[i][0]) + "," + str(arr[i][1]) + "," \
                    + str(arr[i][2]) + "," + str(arr[i][3]) + ");"

            self.colorBars[i].setStyleSheet(_fromUtf8(cs))

        return


    def setValues(self, arr):

        if len(arr) != 9:
            raise ValueError("9 values need to be provided")
            
        for i in range(1,10):
            self.legendValues[i].setText(_translate("Widget", arr[i-1], None))

        return

    def clearLegendValues(self):

        for i in range(0,10):
            self.legendValues[i].setText(_translate("Widget", "", None))

        return

