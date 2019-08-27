# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fin.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys, os
import cv2
import numpy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

class Thread1(QThread):

    signal1 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

    def run(self):
        cam = cv2.VideoCapture(0)
        while self.plzrun:
            b, img = cam.read()
            if b:
                rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(800,600)
                self.signal1.emit(image)

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Thread2(QThread):

    signal2 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

    def run(self):
        cam = cv2.VideoCapture(0)
        while self.plzrun:
            b, img = cam.read()
            if b:
                rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(800,600)
                self.signal2.emit(image)

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 801, 601))
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.open1 = QtWidgets.QPushButton(self.tab1)
        self.open1.setGeometry(QtCore.QRect(600, 530, 89, 25))
        self.open1.setObjectName("open1")
        self.label1 = QtWidgets.QLabel(self.tab1)
        self.label1.setGeometry(QtCore.QRect(0, 0, 791, 521))
        self.label1.setText("")
        self.label1.setObjectName("label1")
        self.close1 = QtWidgets.QPushButton(self.tab1)
        self.close1.setGeometry(QtCore.QRect(690, 530, 89, 25))
        self.close1.setObjectName("close1")
        self.tabWidget.addTab(self.tab1, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.open2 = QtWidgets.QPushButton(self.tab2)
        self.open2.setGeometry(QtCore.QRect(600, 530, 89, 25))
        self.open2.setObjectName("open2")
        self.label2 = QtWidgets.QLabel(self.tab2)
        self.label2.setGeometry(QtCore.QRect(0, 0, 791, 521))
        self.label2.setText("")
        self.label2.setObjectName("label2")
        self.close2 = QtWidgets.QPushButton(self.tab2)
        self.close2.setGeometry(QtCore.QRect(690, 530, 89, 25))
        self.close2.setObjectName("close2")
        self.tabWidget.addTab(self.tab2, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.open1.clicked.connect(self.cam1open)
        self.open2.clicked.connect(self.cam2open)
        self.close1.clicked.connect(self.cam1close)
        self.close2.clicked.connect(self.cam2close)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open1.setText(_translate("MainWindow", "Open"))
        self.close1.setText(_translate("MainWindow", "Close"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("MainWindow", "Tab 1"))
        self.open2.setText(_translate("MainWindow", "Open"))
        self.close2.setText(_translate("MainWindow", "Close"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("MainWindow", "Tab 2"))

    def cam1open(self):
        self.th1 = Thread1(self)
        self.th1.signal1.connect(self.label1.setPixmap)
        self.th1.start()

    def cam2open(self):
        self.th2 = Thread2(self)
        self.th2.signal2.connect(self.label2.setPixmap)
        self.th2.start()

    def cam1close(self):
        self.th1.stop()
        os.execl(sys.executable, sys.executable, * sys.argv)

    def cam2close(self):
        self.th2.stop()
        os.execl(sys.executable, sys.executable, * sys.argv)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
