import pygame
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


class ThreadM(QThread):

    signalx = pyqtSignal(str)
    signaly = pyqtSignal(str)
    signalg = pyqtSignal(str)
    signalh = pyqtSignal(str)
    signala = pyqtSignal(str)
    signalm = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)

    def tcp_send(self, data):
        self.comm_sock.sendall(bytes([data]))

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

    def mast_cam(self):
        self.rhat=self.joy.get_hat(0)
        self.lhat=self.joy1.get_hat(0)
        msg='n'
        if self.rhat[0]==1:
            msg='p'
        elif self.rhat[0]==-1:
            msg='q'
        if  self.lhat[1]==1:
            msg='k'
        elif self.lhat[1]==-1:
            msg='h'
        print(msg)
        self.signalm.emit(msg)
        if self.mode == 's':
            self.ser.write(msg.encode())
        elif self.mode == 't':
            self.comm_sock.sendall(msg.encode())
            time.sleep(0.01)

    def arm_code(self):
        self.x_joy1 = self.joy1.get_axis(1)*-7999+7999
        self.y_joy1 = self.joy1.get_axis(0)*7999+7999
        self.x_joy = self.joy.get_axis(1)*-7999+7999
        self.y_joy = self.joy.get_axis(2)*7999+7999
        self.lhat=self.joy1.get_hat(0)
        self.rhat=self.joy.get_hat(0)
        right='b'
        left='b'
        grip='b'
        if self.rhat[1]==1:
            right="u"
        elif self.rhat[1]==-1:
            right="t"
        if  self.lhat[0]==-1:
            right="v"
        elif self.lhat[0]==1:
            right="w"
        if self.joy.get_button(5):
            grip='c'
        elif self.joy1.get_button(4):
            grip='d'
        msg='alx'+str(int(self.x_joy1)).zfill(5)+'y'+str(int(self.y_joy1)).zfill(5)+grip+'rx'+str(int(self.x_joy)).zfill(5)+'y'+str(int(self.y_joy)).zfill(5)+right
        print(msg)
        self.signala.emit(msg)

        if self.mode == 's':
            self.ser.write(msg.encode())
        elif self.mode == 't':
            self.comm_sock.sendall(msg.encode())
            time.sleep(0.01)

    def motor_code(self):
        self.x_joy = self.joy.get_axis(0)*8000 #-255 because the joystick was reverse mapped
        self.y_joy = self.joy.get_axis(1)*-8000
        self.gear = self.joy.get_axis(3)

        if self.joy.get_button(1):
            self.idle = not self.idle
        if self.joy.get_button(10):
            self.hill_assist = not self.hill_assist

        if self.idle == True:
            print ("idle")
            self.x_joy = self.y_joy = self.x_joy_last = self.y_joy_last = 0

        self.x_joy = int(self.x_joy)
        self.y_joy = int(self.y_joy)

        self.x_joy = self.x_joy + self.addx
        self.y_joy = self.y_joy + self.addy
        self.x_joy = max(min(16000, self.x_joy), 0)
        self.y_joy = max(min(16000, self.y_joy), 0)

        self.gear = int(((-self.gear+1)/2)*(self.numgears-1)) + 1
        print (self.x_joy, self.y_joy, self.gear)

        self.signalg.emit(str(self.gear))
        self.signalx.emit(str(self.x_joy))
        self.signaly.emit(str(self.y_joy))

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
            self.ser.write(bytes([self.gear_pack]))
            self.ser.write(bytes([self.x1]))
            self.ser.write(bytes([self.x2]))
            self.ser.write(bytes([self.x3]))
            self.ser.write(bytes([self.y1]))
            self.ser.write(bytes([self.y2]))
            self.ser.write(bytes([self.y3]))

        elif self.mode == 't':
            self.tcp_send(109)
            self.tcp_send(self.gear_pack)
            self.tcp_send(self.x1)
            self.tcp_send(self.x2)
            self.tcp_send(self.x3)
            self.tcp_send(self.y1)
            self.tcp_send(self.y2)
            self.tcp_send(self.y3)
            time.sleep(0.01)

    def run(self):
        print ("Rover Joystick")
        self.mode = input("Use [t]cp/ip or [s]erial: ")

        pygame.init()
        pygame.joystick.init()

        self.joy = pygame.joystick.Joystick(0)
        self.joy1 = pygame.joystick.Joystick(1)
        self.joy.init()
        self.joy1.init()

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
        self.switch=True
        self.active=True

        try:
            #self.check_thread = threading.Thread(target=self.check_joy, args=())
            #self.check_thread.start()

            while True:
                pygame.event.pump()
                self.on=self.joy.get_button(1)
                if self.on:
                    sleep(0.2)
                    if self.joy.get_button(1):
                        if self.active==True:
                            self.active=False
                            print('Idle')
                        else:
                            self.active=True
                            print('Active')

                if self.active:
                    self.change=self.joy.get_button(0)
                    if self.change:
                        time.sleep(0.2)
                        if self.joy.get_button(0):
                            if self.switch==True:
                                self.switch=False
                                print('Arm')
                            else:
                                self.switch=True
                                print('Motor')

                    if self.switch:
                        self.motor_code()
                    else:
                        self.arm_code()

                    self.mast_cam()

        except KeyboardInterrupt:
            self.check_running = False
            #self.check_thread.join()
            self.comm_sock.close()
            pass

        finally:
            self.check_running = False
            #self.check_thread.join()
            self.comm_sock.close()
            print ("Closed thread...")

        print ("Exiting joystick...")
        pygame.quit()
