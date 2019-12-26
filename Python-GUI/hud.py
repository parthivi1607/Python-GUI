#!/usr/bin/env python
from joy2 import *


class ThreadHud(QThread):

    signalHUD = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)

    def run(self):
        self.ih=0;

        font = cv2.FONT_HERSHEY_SIMPLEX

        self.crr = numpy.arange(60+self.ih,121+self.ih)
        #print(self.crr)
        #print(self.crr[-1])

        while True:
            self.arr = numpy.arange(181)
            self.arr = (self.arr - 90 + self.ih+360)%360
            #print(self.arr)
            #print(self.arr[60])
            #print(self.arr[90])
            #print(self.arr[120])

            img = numpy.zeros((80,660,3), numpy.uint8)

            self.brr = ["|","'","'","'","'","!","'","'","'","'","|","'","'","'","'","!","'","'","'","'","|","'","'","'","'","!","'","'","'","'","|","'","'","'","'","!","'","'","'","'","|","'","'","'","'","!","'","'","'","'","|","'","'","'","'","!","'","'","'","'","|"]
            x = self.ih%10
            self.drr = self.brr[x:61] + self.brr[1:x]
            k=17
            for j in self.drr:
                cv2.putText(img,j,(k,20),font,0.75,(255,255,255),2,cv2.LINE_AA)
                k=k+10

            k=14
            for l in self.crr:
                if self.arr[l]==self.ih:
                    cv2.putText(img,str(self.arr[l]),(k,60),font,0.75,(255,255,255),2,cv2.LINE_AA)
                if self.arr[l]%10 == 0:
                    cv2.putText(img,str(self.arr[l]),(k,60),font,0.75,(0,0,255),2,cv2.LINE_AA)
                k=k+10

            rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            convimg = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
            convimg = QPixmap.fromImage(convimg)
            image = convimg.scaled(640,480,Qt.KeepAspectRatio)

            if self.ih<360:
                self.ih = self.ih + 1
            else:
                self.ih=0

            self.signalHUD.emit(image)
            time.sleep(0.5)


class ThreadGPS(QThread):
    signalLat = pyqtSignal(str)
    signalLon = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)

    def run(self):
        self.lat = 0
        self.lon = 0
        while True:
            self.signalLat.emit(str(self.lat))
            self.signalLon.emit(str(self.lon))
'''
from sensor_msgs.msg import Imu,NavSatFix
from tf.transformations import euler_from_quaternion
from math import degrees
import rospy


lat = lon = heading = 0

def callback_imu(msg):
    global heading

    orientation_list = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

    yaw = degrees(yaw)
    if yaw < 0:
        yaw += 360
    yaw = (yaw) % 360

    heading = 360 - yaw


def callback_gps(msg):
    global lat,lon
    lat = msg.latitude
    lon = msg.longitude


class ThreadHud(QThread):

    signalHUD = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)

    def run(self):

        rospy.init_node('GUI_node', anonymous=True, disable_signals=True)
        rate = rospy.Rate(50)  # 1hz
        rospy.Subscriber("/imu_data/raw", Imu, callback_imu)

        self.ih = 0
        font = cv2.FONT_HERSHEY_SIMPLEX

        self.crr = numpy.arange(60+self.ih,121+self.ih)
        #print(self.crr)
        #print(self.crr[-1])

        while True:
            global heading

            self.ih = int(heading)
            self.arr = numpy.arange(181)
            self.arr = (self.arr - 90 + self.ih+360)%360
            #print(self.arr)
            #print(self.arr[60])
            #print(self.arr[90])
            #print(self.arr[120])

            img = numpy.zeros((80,660,3), numpy.uint8)

            self.brr = ["|","'","'","'","'","!","'","'","'","'","|","'","'","'","'","!","'","'","'","'","|","'","'","'","'","!","'","'","'","'","|","'","'","'","'","!","'","'","'","'","|","'","'","'","'","!","'","'","'","'","|","'","'","'","'","!","'","'","'","'","|"]
            x = self.ih%10
            self.drr = self.brr[x:61] + self.brr[1:x]
            k=17
            for j in self.drr:
                cv2.putText(img,j,(k,20),font,0.75,(255,255,255),2,cv2.LINE_AA)
                k=k+10

            k=14
            for l in self.crr:
                if self.arr[l]==self.ih:
                    cv2.putText(img,str(self.arr[l]),(k,60),font,0.75,(255,255,255),2,cv2.LINE_AA)
                if self.arr[l]%10 == 0:
                    cv2.putText(img,str(self.arr[l]),(k,60),font,0.75,(0,0,255),2,cv2.LINE_AA)
                k=k+10

            rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            convimg = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
            convimg = QPixmap.fromImage(convimg)
            image = convimg.scaled(640,480,Qt.KeepAspectRatio)

            self.signalHUD.emit(image)


class ThreadGPS(QThread):
    global lat,lon
    signalLat = pyqtSignal(str)
    signalLon = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)

    def run(self):

        rospy.Subscriber("/fix", NavSatFix, callback_gps)

        self.lat = 0
        self.lon = 0
        while True:
            self.lat = lat
            self.lon = lon
            self.signalLat.emit(str(self.lat))
            self.signalLon.emit(str(self.lon))
'''
