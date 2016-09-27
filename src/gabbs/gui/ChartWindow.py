import os, time
from os.path import expanduser
from subprocess import call
from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


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


class ChartWindow(QtGui.QDialog):
	def __init__(self, parent):
		super(ChartWindow, self).__init__(parent)
		self.imagePath = None

		self.setGeometry(QtCore.QRect(90, 60, 620, 470))

		homePath = expanduser("~")
		tempPath = homePath + "/mapsTempOutput"

		if not os.path.exists(tempPath):
			os.makedirs(tempPath)

	def downloadImage(self):

		call(["/usr/bin/exportfile", self.imagePath])

		return

	def prepare(self, x, y, plotTitle, xlabelString, ylabelString, xtickInterval = 1):

		plt.figure(figsize=(12,9))

		max = -999999.0
		min = 999999.0

		for value in y:
			if value > max:
				max = value

			if value < min:
				min = value

		plt.gca().set_ylim(bottom=min-0.05, top = max + 0.05)

		
		plt.plot(x,y)

		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y\n%H:%M:%S'))
		plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=xtickInterval))

		
		plt.gcf().autofmt_xdate()

		plt.title(plotTitle, fontsize=22)


		plt.xlabel(xlabelString, fontsize=22)

		plt.gca().xaxis.set_label_coords(0.5, -0.18)

		plt.ylabel(ylabelString, fontsize=22)

		homePath = expanduser("~")
		tempPath = homePath + "/mapsTempOutput"

		ts = time.time()
		fileName = tempPath + "/" + str(ts) + ".png"

		plt.savefig(fileName)
		plt.close()

		self.imagePath = fileName

		return

	def draw(self):
		pic = QtGui.QLabel(self)
		pic.setGeometry(10, 10, 600, 450)
		
		image = QtGui.QPixmap(self.imagePath)
		# self.imagePath = fileName
		
		scaled = image.scaled(600, 450, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
		pic.setPixmap(scaled)

		self.saveButton = QtGui.QPushButton(self)
		self.saveButton.setGeometry(QtCore.QRect(500, 420, 80, 25))
		self.saveButton.setObjectName(_fromUtf8("downloadPushButton"))


		QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.downloadImage)

		self.saveButton.setText(_translate("Widget", "Download", None))