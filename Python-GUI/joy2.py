#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from std_msgs.msg import String
import rospy
import socket
import serial
import pickle
import struct

pygame.init()
pygame.joystick.init()

ob1 = String()
ob2 = String()
ob3 = String()

gear_pack=x1=x2=x3=y1=y2=y3=0b00000000
wasd_gear =1

xj=yj=8000

def joystick_decoder_wasd(x_joy,y_joy,gear,hill_assist):
    gear_pack = 0b00000001
    if not hill_assist:

        gear_pack = (0b00001111 & gear)
    elif hill_assist:
        gear_pack = (0b00001111 & gear)
        gear_pack |= 0b00010000

    x1 = 0b00001111 & (x_joy >> 10)
    x1 |= 0b00100000

    x2 = 0b000011111 & (x_joy >> 5)
    x2 |= 0b01000000

    x3 = 0b00000000011111 & (x_joy >> 0)
    x3 |= 0b01100000

    y1 = 0b00001111 & (y_joy >> 10)
    y1 |= 0b10000000

    y2 = 0b000011111 & (y_joy >> 5)
    y2 |= 0b10100000

    y3 = 0b00000000011111 & (y_joy >> 0)
    y3 |= 0b11000000

    return gear_pack,x1,x2,x3,y1,y2,y3


class ThreadM(QThread):
    #motor code
    signalx = pyqtSignal(str)
    signaly = pyqtSignal(str)
    signalg = pyqtSignal(str)
    signalh = pyqtSignal(str)
    #arm code
    signalL1 = pyqtSignal(str)
    signalL2 = pyqtSignal(str)
    signalG = pyqtSignal(str)
    signalS = pyqtSignal(str)
    #mast cam
    signalm = pyqtSignal(str)
    #code running
    signalc = pyqtSignal(str)
    #BMS
    signalbms = pyqtSignal(str)

    def __init__(self, mode):
        QThread.__init__(self, parent=None)
        self.mode = mode
        print(self.mode)

    def tcp_send(self, data):
        self.comm_sock.sendall(chr(data))  # for python 2.7
        #self.comm_sock.sendall(bytes([data])) #for python 3

    def mast_cam(self):
        self.rhat = self.joy.get_hat(0)
        self.M_msg = 'n'
        msgs = "Mast cam: c"
        if self.rhat[0] == 1:
            self.M_msg = 'p'
            msgs = "Mast cam: r"
        elif self.rhat[0] == -1:
            self.M_msg = 'q'
            msgs = "Mast cam: l"
        elif self.rhat[1] == 1:
            self.M_msg = 'k'
            msgs = "Mast cam: u"
        elif self.rhat[1] == -1:
            self.M_msg = 'h'
            msgs = "Mast cam: d"
        #print(msgs)
        self.signalm.emit(msgs)
        if self.mode == 's':
            self.ser.write(self.M_msg.encode())
        elif self.mode == 't':
            self.comm_sock.sendall(self.M_msg.encode())
            time.sleep(0.01)

    def arm_code(self):
        self.joy1 = pygame.joystick.Joystick(1)
        self.joy1.init()

        self.x_joy1 = self.joy1.get_axis(1) * -7999 + 7999
        self.y_joy1 = self.joy1.get_axis(0) * 7999 + 7999
        self.x_joy = self.joy.get_axis(1) * -7999 + 7999
        self.y_joy = 7999
        self.lhat = self.joy1.get_hat(0)
        right = 'b'
        left = 'b'
        grip = 'b'
        if self.lhat[1] == 1:
            right = "u"
        elif self.lhat[1] == -1:
            right = "t"
        if self.lhat[0] == -1:
            right = "v"
        elif self.lhat[0] == 1:
            right = "w"
        if self.joy.get_button(5):
            grip = 'c'
        elif self.joy1.get_button(4):
            grip = 'd'
        if self.joy.get_button(7):
            self.y_joy = 4000
        if self.joy.get_button(9):
            self.y_joy = 12000

        msg = 'alx' + str(int(self.x_joy1)).zfill(5) + 'y' + str(int(self.y_joy1)).zfill(5) + grip + 'rx' + str(int(self.x_joy)).zfill(5) + 'y' + str(int(self.y_joy)).zfill(5) + right
        print(msg)
        self.signalL1.emit("Link1: "+str(self.x_joy))
        self.signalL2.emit("Link2: "+str(self.x_joy1))

        if self.mode == 's':
            self.ser.write(msg.encode())
        elif self.mode == 't':
            self.comm_sock.sendall(msg.encode())
            time.sleep(0.01)

    # def bmsval(self):
    #     factor=[1.5623,3.21517,4.8031,6.671577,8.02571,9.42726,1.5745,3.20258,4.7876,6.54061,7.9482,9.36948]
    #
    #     while True:
    #         if(self.comm_sock.recv(1)=='j'):
    #             for i in range(24):
    #                 if(self.comm_sock.recv(1)=='w'):
    #                     x=((ord(self.comm_sock.recv(1))-48)+(ord(self.comm_sock.recv(1))-48)*10+(ord(self.comm_sock.recv(1))-48)*100+(ord(self.comm_sock.recv(1))-48)*1000)*2.9
    #                     x=x/4000
    #                     x=x*factor[i/2]
    #                     print round(x,2),"\t",
    #                     if i==10:
    #                         print"\t\t",
    #
    #             print('\n')
    #             time.sleep(0.3)

    def motor_code(self):
        try:
            self.joy = pygame.joystick.Joystick(0)
            self.joy.init()
        except:
            print("1st joystick not found")
            os.execl(sys.executable, sys.executable, * sys.argv)
        else:
            self.x_joy = self.joy.get_axis(0) * 8000  # -255 because the joystick was reverse mapped
            self.y_joy = self.joy.get_axis(1) * -8000
            self.gear = self.joy.get_axis(3)
            self.rotate = self.joy.get_axis(2)

            if self.rotate!=0 and self.x_joy==0 and self.y_joy==0:
                self.x_joy = self.rotate * 8000
                self.y_joy = self.rotate * -8000

            if self.joy.get_button(1):
                self.idle = not self.idle
            if self.joy.get_button(10):
                self.hill_assist = not self.hill_assist

            if self.idle:
                self.signalc.emit("idle")
                self.x_joy = self.y_joy = self.x_joy_last = self.y_joy_last = 0

            self.x_joy = int(self.x_joy)
            self.y_joy = int(self.y_joy)

            self.x_joy = self.x_joy + self.addx
            self.y_joy = self.y_joy + self.addy
            self.x_joy = max(min(16000, self.x_joy), 0)
            self.y_joy = max(min(16000, self.y_joy), 0)

            self.gear = int(((-self.gear + 1) / 2) * (self.numgears - 1)) + 1
            #print (self.x_joy, self.y_joy, self.gear)

            self.sending()

    def sending(self):
        self.signalg.emit("Gear : "+str(self.gear))
        self.signalx.emit("X = "+str(self.x_joy))
        self.signaly.emit("Y = "+str(self.y_joy))
        self.joystick_decoder()

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
            #self.tcprecv()

        elif self.mode == 'T':
            self.teleop_publisher()
            self.wasd_publisher()

    def joystick_decoder(self):
        if self.hill_assist == False:
            # print ("Hill assist OFF")
            self.signalh.emit("OFF")
            self.gear_pack = (0b00001111 & self.gear)
        elif self.hill_assist == True:
            # print ("Hill assist ON")
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

    def wasd_publisher(self):
        global xj,yj,gear_pack,x1,x2,x3,y1,y2,y3,wasd_gear
        self.clock.tick(30)
        pygame.event.pump()
        # a key has been pressed
        keyinput = pygame.key.get_pressed()

        # optional exit on window corner x click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()

        if (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_w]) and (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_d]):
            print('wd',wasd_gear)
            xj = 16000
            yj = 16000

        elif (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_w]) and (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_a]):
            print('wa',wasd_gear)
            xj = 0
            yj = 16000

        elif (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_s]) and (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_d]):
            print('sd',wasd_gear)
            xj = 16000
            yj = 0

        elif (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_s]) and (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_a]):
            print('sa',wasd_gear)
            xj = 0
            yj = 0

        elif (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_w]) and (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_s]) or (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_a]) and (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_d]):
            print('NULL',wasd_gear)
            xj = 8000
            yj = 8000

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_w]:
            print('w',wasd_gear)
            xj = 8000
            yj = 16000

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_a]:
            print('a',wasd_gear)
            xj = 0
            yj = 8000

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_s]:
            print('s',wasd_gear)
            xj = 8000
            yj = 0

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_d]:
            print('d',wasd_gear)
            xj = 16000
            yj = 8000

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_1]:
            wasd_gear =1

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_2]:
            wasd_gear =2

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_3]:
            wasd_gear =3

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_4]:
            wasd_gear =4

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_5]:
            wasd_gear =5

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_6]:
            wasd_gear =6

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_7]:
            wasd_gear =7

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_8]:
            wasd_gear =8

        elif keyinput[pygame.K_LCTRL] and keyinput[pygame.K_9]:
            wasd_gear =9

        if (not (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_w]) and not (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_a]) and (
                not (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_s]) and not (keyinput[pygame.K_LCTRL] and keyinput[pygame.K_d]))):
            print('joystick gear',self.gear,'wasd gear',wasd_gear)
            ob3.data = "{} {} {} {} {} {} {} {} {}".format('0','0','0','0','0','0','0','0','0')
            self.pub_wasd.publish(ob3)
            return

        gear_pack, x1, x2, x3, y1, y2, y3 = joystick_decoder_wasd(xj, yj, wasd_gear, self.hill_assist)
        ob3.data = "{} {} {} {} {} {} {} {} {}".format('m', gear_pack, x1, x2, x3, y1,y2,y3,self.M_msg)
        self.pub_wasd.publish(ob3)

    def teleop_publisher(self):
        ob1.data = "{} {}".format(self.x_joy, self.y_joy)
        ob2.data = "{} {} {} {} {} {} {} {} {}".format('m', self.gear_pack, self.x1, self.x2, self.x3, self.y1,self.y2,self.y3, self.M_msg)
        self.pub_jr.publish(ob1)
        self.pub_je.publish(ob2)

    def run(self):
        self.pub_je = rospy.Publisher('joystick_encoded', String, queue_size=10)
        self.pub_jr = rospy.Publisher('joystick_topic', String, queue_size=10)
        self.pub_wasd = rospy.Publisher('wasd', String, queue_size=10)

        try:
            while True:
                # self.mode = raw_input("Use [t]cp/ip, [s]erial, [T]eleop: ")
                # self.mode = input("Use [t]cp/ip, [s]erial, [T]eleop: ")

                if self.mode == 's':
                    try:
                        self.ser = serial.Serial('/dev/ttyUSB0', 115200)
                    except:
                        print("TTL not connected")
                        # os.execl(sys.executable, sys.executable, * sys.argv)
                    try:
                        print("Rover Joystick")
                        self.joy = pygame.joystick.Joystick(0)
                        self.joy.init()
                    except:
                        print("1st joystick not found")
                        self.mode = 'T'
                        # os.execl(sys.executable, sys.executable, * sys.argv)
                    break

                elif self.mode == 't':
                    #self.host = '10.42.0.201'
                    #self.host = '192.168.43.21'
                    self.host = '192.168.1.7' #LAN to UART
                    #self.host = '192.168.1.169'
                    print(self.host)
                    self.comm_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    #self.port = 1234
                    self.port = 5005 #LAN to UART

                    try:
                        print("Rover Joystick")
                        self.joy = pygame.joystick.Joystick(0)
                        self.joy.init()
                    except:
                        print("1st joystick not found")
                        self.mode = 'T'
                        # os.execl(sys.executable, sys.executable, * sys.argv)
                    else:
                        while True:
                            try:
                                self.comm_sock.connect((self.host, self.port))
                                print("opened socket at ",self.port)
                                break
                            except socket.error:
                                self.port += 1
                    break

                if self.mode == 'T':
                    screen = pygame.display.set_mode((300, 300))
                    pygame.display.set_caption("WASD OVERRIDE")
                    white = (255, 255, 255)
                    background = pygame.Surface(screen.get_size())
                    background.fill(white)
                    sprite = pygame.image.load("wasd.png")
                    sprite_rect = sprite.get_rect()
                    screen.blit(sprite, sprite_rect)
                    pygame.display.flip()
                    self.clock = pygame.time.Clock()
                    break

                elif self.mode!='s' and self.mode!='t':
                    print("Wrong input. Enter again.")
                    continue

            self.check_running = True
            self.numgears = 10
            self.x_joy = 0
            self.y_joy = 0
            self.gear = 0
            self.x_joy_last = 8000
            self.y_joy_last = 8000
            self.gear_last = 0
            self.addx = 8000
            self.addy = 8000
            self.reconnected = False
            self.idle = False
            self.hill_assist = False
            self.rotate = 0
            self.switch = True
            self.active = True
            self.M_msg = 'n'

            try:
                # self.check_thread = threading.Thread(target=self.check_joy, args=())
                # self.check_thread.start()
                while True:
                    pygame.event.pump()
                    self.on = self.joy.get_button(1)
                    if self.on:
                        sleep(0.2)
                        if self.joy.get_button(1):
                            if self.active == True:
                                self.active = False
                                print('Idle')
                                self.signalc.emit("Idle")
                            else:
                                self.active = True
                                print('Active')

                    if self.active:
                        self.change = self.joy.get_button(0)
                        if self.change:
                            time.sleep(0.2)
                            if self.joy.get_button(0):
                                if self.switch == True:
                                    self.switch = False
                                    print('Arm')
                                else:
                                    self.switch = True
                                    print('Motor')

                        if self.switch:
                            self.motor_code()
                            self.signalc.emit("Motor code")
                        else:
                            try:
                                self.arm_code()
                                self.signalc.emit("Arm code")
                            except:
                                self.signalc.emit("2nd joystick not found")
                                if self.mode == 'T':
                                    ob2.data = "{}".format('m 1 39 90 96 135 186 192 n')
                                    self.pub_je.publish(ob2)
                                    self.wasd_publisher()
                                else:
                                    self.x_joy = self.y_joy = 8000
                                    self.gear = 1
                                    #print(self.x_joy,self.y_joy,self.gear)
                                    self.sending()

                        self.mast_cam()

            except:
                print("Switched to Tele-op")
                while True:
                    self.teleop_publisher()
                    self.wasd_publisher()

            finally:
                self.check_running = False
                #self.check_thread.join()
                if self.mode == 't':
                    self.comm_sock.close()
                print("Closed thread...")

            print("Exiting joystick...")
            pygame.quit()

        except:
            sys.exit()
            QCoreApplication.quit()
            QCoreApplication.exit(0)
