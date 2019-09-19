from joystickthread import *


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
                image = convimg2.scaled(400,300,Qt.KeepAspectRatio)
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
        cam = cv2.VideoCapture(2)
        while self.plzrun:
            b, img = cam.read()
            if b:
                rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(400,300,Qt.KeepAspectRatio)
                self.signal2.emit(image)

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Thread3(QThread):

    signal3 = pyqtSignal(QPixmap)
    signal4 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

    def run(self):
        cam = cv2.VideoCapture('rtsp://192.168.1.10/user=admin&password=&channel=1&stream=1.sdp')
        while self.plzrun:
            b, img = cam.read()
            if b:
                rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(400,300,Qt.KeepAspectRatio)
                self.signal3.emit(image)
                self.signal4.emit(image)

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()
