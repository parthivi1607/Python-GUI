import pygame
import time
import subprocess
import time
import threading
import sys, os
import cv2
import numpy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton


class ThreadM(QThread):

    signalm = pyqtSignal(str)
    signalg = pyqtSignal(str)
    signalh = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)

    #def check_joy(self):
    #    while self.check_running == True:
    #        self.present = False
    #        cmd = "lsusb | grep -o ThrustMaster"
    #        #cmd = "lsusb | grep -o Logitech,\ Inc.\ Extreme"

    #        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    #        output = ps.communicate()[0]
    #        #if output == 'Logitech,\ Inc.\ Extreme\n':
    #        if output == 'ThrustMaster\n':
    #            self.present = True
    #        if self.present == False:
    #            print ("Joystick disconnected")
    #            self.reconnected = True
    #            self.y_joy = self.x_joy = self.x_joy_last = self.y_joy_last= 0
    #        if self.reconnected == True and self.present == True:
    #            pygame.joystick.quit()
    #            pygame.joystick.init()
    #            self.joy = pygame.joystick.Joystick(0)
    #            self.joy.init()
    #            self.reconnected = False

    def run(self):
        print ("Rover Joystick")
        self.mode = input("Use [t]cp/ip or [s]erial: ")

        pygame.init()
        pygame.joystick.init()

        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()

        ## SELECT MODE ##
        if self.mode == 's':
            import serial
            self.ser = serial.Serial('/dev/ttyUSB0', 115200)

        elif self.mode == 't':
            import socket
            self.host = '192.168.1.7'
            print (self.host)
            self.comm_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.port = 5005
            while True:
                try:
                    self.comm_sock.connect((self.host, self.port))
                    print ("opened socket at "), self.port
                    break
                except socket.error:
                    self.port += 1

            def tcp_send(data):
                self.comm_sock.sendall(data)

        self.check_running = True
        self.numgears = 10
        self.x_joy = 0
        self.y_joy = 0
        self.gear= 0
        self.x_joy_last = 8000
        self.y_joy_last = 8000
        self.gear_last = 0
        self.addx = 8000
        self.addy = 8000
        self.reconnected = False
        self.idle = False
        self.hill_assist = False

        try:
            #self.check_thread = threading.Thread(target=self.check_joy, args=())
            #self.check_thread.start()

            while True:

                self.x_joy = self.x_joy_last
                self.y_joy = self.y_joy_last
                self.gear = self.gear_last

                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        if event.axis == 0:
                            self.x_joy = event.value*8000 #-255 because the joystick was reverse mapped
                        elif event.axis == 1:
                            self.y_joy = event.value*-8000
                        elif event.axis == 3:
                            self.gear = event.value
                    elif event.type == pygame.JOYBUTTONDOWN:
                        if self.joy.get_button(1):
                            self.idle = not self.idle
                        if self.joy.get_button(10):
                            self.hill_assist = not self.hill_assist

                if self.idle == True:
                    print ("idle")
                    self.x_joy = self.y_joy = self.x_joy_last = self.y_joy_last = 0

                self.x_joy_last = self.x_joy
                self.y_joy_last = self.y_joy
                self.gear_last = self.gear

                self.x_joy = int(self.x_joy)
                self.y_joy = int(self.y_joy)

                self.x_joy = self.x_joy + self.addx
                self.y_joy = self.y_joy + self.addy
                self.x_joy = max(min(16000, self.x_joy), 0)
                self.y_joy = max(min(16000, self.y_joy), 0)

                self.gear = int(((-self.gear+1)/2)*(self.numgears-1)) + 1
                print (self.x_joy, self.y_joy, self.gear)

                val = "x: "+str(self.x_joy)+" y: "+str(self.y_joy)
                self.signalm.emit(val)
                self.signalg.emit(str(self.gear))

                if self.hill_assist == False:
                    print ("Hill assist OFF")
                    self.signalh.emit("OFF")
                    self.gear_pack = (0b00001111 & self.gear)
                elif self.hill_assist == True:
                    print ("Hill assist ON")
                    self.signalh.emit("ON")
                    self.gear_pack = (0b00001111 & self.gear)
                    self.gear_pack |= 0b00010000

                self.x1 = 0b00001111 & (self.x_joy >> 10)
                self.x1 |= 0b00100000

                self.x2 = 0b000011111 & (self.x_joy >> 5)
                self.x2 |= 0b01000000

                self.x3 = 0b00000000011111 & (self.x_joy >> 0)
                self.x3 |= 0b01100000

                self.y1 = 0b00001111 & (self.y_joy >> 10)
                self.y1 |= 0b10000000

                self.y2 = 0b000011111 & (self.y_joy >> 5)
                self.y2 |= 0b10100000

                self.y3 = 0b00000000011111 & (self.y_joy >> 0)
                self.y3 |= 0b11000000

                if self.mode == 's':
                    self.ser.write('m'.encode())
                    self.ser.write(chr(self.gear_pack).encode())
                    self.ser.write(chr(self.x1).encode())
                    self.ser.write(chr(self.x2).encode())
                    self.ser.write(chr(self.x3).encode())
                    self.ser.write(chr(self.y1).encode())
                    self.ser.write(chr(self.y2).encode())
                    self.ser.write(chr(self.y3).encode())

                elif self.mode == 't':
                    tcp_send('m'.encode())
                    tcp_send(chr(self.gear_pack))
                    tcp_send(chr(self.x1))
                    tcp_send(chr(self.x2))
                    tcp_send(chr(self.x3))
                    tcp_send(chr(self.y1))
                    tcp_send(chr(self.y2))
                    tcp_send(chr(self.y3))
                    time.sleep(0.01)

        except KeyboardInterrupt:
            self.check_running = False
            self.check_thread.join()
            self.comm_sock.close()
            pass

        finally:
            self.check_running = False
            self.check_thread.join()
            self.comm_sock.close()
            print ("Closed thread...")

        print ("Exiting joystick...")
        pygame.quit()
