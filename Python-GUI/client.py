import time
import subprocess
import time
from time import sleep
import threading
import sys, os
import cv2
import numpy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from std_msgs.msg import String
import rospy
import socket
import serial
import pickle
import struct
import numpy as np

class ClientThread(QThread):

    signalcam = pyqtSignal(QPixmap)

    def __init__(self, portno):
        QThread.__init__(self, parent=None)
        self.plzrun = True
        self.portno = portno

    def run(self):
        self.plzrun = True
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error:
            print "Error creating socket"
            sys.exit(1)

        try:
            client_socket.connect((socket.gethostname(), int(self.portno)))
        except socket.gaierror:
            print "Address-related error connecting to server"
            sys.exit(1)
        except socket.error:
            print "Connection error"
            sys.exit(1)

        connection = client_socket.makefile('wb')
        data = b""
        payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(payload_size))

        while self.plzrun:
            while len(data) < payload_size:
                print("Recv: {}".format(len(data)))
                data += client_socket.recv(4096)

            print("Done Recv: {}".format(len(data)))
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            print("msg_size: {}".format(msg_size))

            while len(data) < msg_size:
                data += client_socket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame=pickle.loads(frame_data)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            rgbimg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
            convimg2 = QPixmap.fromImage(convimg1)
            image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
            self.signalcam.emit(image)

    def stop(self):
        self.plzrun = False
