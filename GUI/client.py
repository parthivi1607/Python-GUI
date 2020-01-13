import time
import subprocess
from time import sleep
import threading
import sys, os
import cv2
import numpy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
import socket
import serial
import pickle
import struct
import numpy as np
import base64
import zmq

class ClientThread(QThread):

    signalcam = pyqtSignal(QPixmap)

    def __init__(self, portno):
        QThread.__init__(self, parent=None)
        self.plzrun = True
        self.portno = portno

    def run(self):
        self.plzrun = True
        context = zmq.Context()
        footage_socket = context.socket(zmq.SUB)
        footage_socket.bind('tcp://*:5555')
        footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

        while True:
            try:
                frame = footage_socket.recv_string()
                img = base64.b64decode(frame)
                npimg = np.fromstring(img, dtype=np.uint8)
                source = cv2.imdecode(npimg, 1)
                rgbimg = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signalcam.emit(image)

            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break

    def stop(self):
        self.plzrun = False
