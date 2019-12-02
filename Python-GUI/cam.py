from hud import *


img1 = None
img2 = None
img3 = None
img4 = None
img5 = None
img6 = None

class Thread1(QThread):
    global img1
    signal1 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

    def run(self):
        cam = cv2.VideoCapture('rtsp://192.168.1.10/user=admin&password=&channel=1&stream=1.sdp')
        while self.plzrun:
            b1, img1 = cam.read()
            if b1:
                rgbimg = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signal1.emit(image)

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Thread2(QThread):
    global img2
    signal2 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

    def run(self):
        cam = cv2.VideoCapture('http://root:mrm@192.168.1.90/axis-cgi/mjpg/video.cgi?camera=1')
        while self.plzrun:
            b2, img2 = cam.read()
            if b2:
                rgbimg = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signal2.emit(image)

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Thread3(QThread):
    global img3
    signal3 = pyqtSignal(QPixmap)
    signal4 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

    def run(self):
        cam = cv2.VideoCapture('http://root:mrm@192.168.1.90/axis-cgi/mjpg/video.cgi?camera=2')
        while self.plzrun:
            b3, img3 = cam.read()
            if b3:
                rgbimg = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signal3.emit(image)

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Thread4(QThread):
    global img4
    signal4 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

    def run(self):
        cam = cv2.VideoCapture('http://root:mrm@192.168.1.90/axis-cgi/mjpg/video.cgi?camera=3')
        while self.plzrun:
            b4, img4 = cam.read()
            if b4:
                rgbimg = cv2.cvtColor(img4, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signal4.emit(image)

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Thread5(QThread):
    global img5
    signal5 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

    def run(self):
        cam = cv2.VideoCapture('http://root:mrm@192.168.1.90/axis-cgi/mjpg/video.cgi?camera=4')
        while self.plzrun:
            b5, img5 = cam.read()
            if b5:
                rgbimg = cv2.cvtColor(img5, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signal5.emit(image)

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Thread6(QThread):
    global img6
    signal6 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

    def run(self):
        cam = cv2.VideoCapture('rtsp://192.168.1.8/user=admin&password=&channel=1&stream=1.sdp')
        while self.plzrun:
            b6, img6 = cam.read()
            if b6:
                rgbimg = cv2.cvtColor(img6, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signal6.emit(image)

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class CamFeed(QThread):
    global img1,img2,img3,img4,img5,img6

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)

    def accepting_connectns(self):
        for c in self.all_connections:
            c.close()
        del self.all_connections[:]
        del self.all_addresses[:]

        while True:
            try:
                conn, addr= self.s.accept()
                self.s.setblocking(1)

                self.all_connections.append(conn)
                self.all_addresses.append(addr)

            except:
                print ("Error accepting connection")

    def run(self):
        import socket
        import pickle
        import struct

        self.all_connections = []
        self.all_addresses = []

        try:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print('Socket created')
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error:
            print "Error creating socket"
            sys.exit(1)

        try:
            self.s.bind((socket.gethostname(),8486))
            print('Socket bind complete')
        except socket.gaierror:
            print "Address-related error connecting to server"
            sys.exit(1)
        except socket.error:
            print "Connection error"
            sys.exit(1)

        self.s.listen(10)
        print('Socket now listening')

        cam = cv2.VideoCapture(0)
        cam.set(3, 320)
        cam.set(4, 240)

        thr = threading.Thread(target=self.accepting_connectns)
        thr.start()

        img_counter = 0
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        while True:
            ret, frame = cam.read()
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            data = pickle.dumps(frame, 0)
            size = len(data)

            for conn in self.all_connections:
                try:
                    conn.sendall(struct.pack(">L", size) + data)
                except:
                    print("Error sending data")

        thr.join()
        cam.release()
        s.close()
