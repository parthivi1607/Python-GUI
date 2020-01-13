from hud import *

'''
'rtsp://192.168.1.10/user=admin&password=&channel=1&stream=1.sdp'
'http://root:mrm@192.168.1.90/axis-cgi/mjpg/video.cgi?camera=1'
'http://root:mrm@192.168.1.90/axis-cgi/mjpg/video.cgi?camera=2'
'http://root:mrm@192.168.1.90/axis-cgi/mjpg/video.cgi?camera=3'
'http://root:mrm@192.168.1.90/axis-cgi/mjpg/video.cgi?camera=4'
'rtsp://192.168.1.8/user=admin&password=&channel=1&stream=1.sdp'
'''


class ThreadCam(QThread):
    signalcam = pyqtSignal(QPixmap)

    def __init__(self, camname, portno):
        QThread.__init__(self, parent=None)
        self.plzrun = True
        self.camname = camname
        self.portno = portno
        self.all_connections = []
        self.all_addresses = []

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

    def sendcamfeed(self):
        while True:
            for conn in self.all_connections:
                if conn.fileno() != -1:
                    try:
                        conn.sendall(struct.pack(">L", self.size) + self.data)
                    except:
                        continue

    def run(self):
        self.plzrun = True
        context = zmq.Context()
        footage_socket = context.socket(zmq.PUB)
        footage_socket.connect('tcp://localhost:5555')

        cam = cv2.VideoCapture(self.camname)

        while self.plzrun:
            b, img = cam.read()
            if b:
                rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signalcam.emit(image)

                try:
                    frame = cv2.resize(img, (640, 480))  # resize the frame
                    encoded, buffer = cv2.imencode('.jpg', frame)
                    jpg_as_text = base64.b64encode(buffer)
                    footage_socket.send(jpg_as_text)

                except KeyboardInterrupt:
                    camera.release()
                    cv2.destroyAllWindows()
                    break

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()

'''
class Thread1(QThread):
    signal1 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self)
        self.plzrun = True

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
        self.all_connections = []
        self.all_addresses = []

        try:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print('Socket created')
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error:
            print "Error creating socket"
            # sys.exit(1)

        try:
            self.s.bind((socket.gethostname(),8481))
            print('Socket bind complete')
        except socket.gaierror:
            print "Address-related error connecting to server"
            # sys.exit(1)
        except socket.error:
            print "Connection error"
            # sys.exit(1)

        self.s.listen(10)
        print('Socket now listening')

        cam = cv2.VideoCapture(0)

        thr = threading.Thread(target=self.accepting_connectns)
        thr.start()
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        while self.plzrun:
            b, img = cam.read()
            if b:
                rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signal1.emit(image)

                result, frame = cv2.imencode('.jpg', img, self.encode_param)
                data = pickle.dumps(frame, 0)
                size = len(data)

                for conn in self.all_connections:
                    if conn.fileno() != -1:
                        try:
                            conn.sendall(struct.pack(">L", size) + data)
                        except:
                            continue

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Thread2(QThread):
    signal2 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

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
        self.all_connections = []
        self.all_addresses = []

        try:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print('Socket created')
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error:
            print "Error creating socket"
            # sys.exit(1)

        try:
            self.s.bind((socket.gethostname(),8482))
            print('Socket bind complete')
        except socket.gaierror:
            print "Address-related error connecting to server"
            # sys.exit(1)
        except socket.error:
            print "Connection error"
            # sys.exit(1)

        self.s.listen(10)
        print('Socket now listening')

        cam = cv2.VideoCapture(0)

        thr = threading.Thread(target=self.accepting_connectns)
        thr.start()
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        while self.plzrun:
            b, img = cam.read()
            if b:
                rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signal2.emit(image)

                result, frame = cv2.imencode('.jpg', img, self.encode_param)
                data = pickle.dumps(frame, 0)
                size = len(data)

                for conn in self.all_connections:
                    if conn.fileno() != -1:
                        try:
                            conn.sendall(struct.pack(">L", size) + data)
                        except:
                            continue

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Thread3(QThread):
    signal3 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

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
        self.all_connections = []
        self.all_addresses = []

        try:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print('Socket created')
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error:
            print "Error creating socket"
            # sys.exit(1)

        try:
            self.s.bind((socket.gethostname(),8483))
            print('Socket bind complete')
        except socket.gaierror:
            print "Address-related error connecting to server"
            # sys.exit(1)
        except socket.error:
            print "Connection error"
            # sys.exit(1)

        self.s.listen(10)
        print('Socket now listening')

        cam = cv2.VideoCapture(0)

        thr = threading.Thread(target=self.accepting_connectns)
        thr.start()
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        while self.plzrun:
            b, img = cam.read()
            if b:
                rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signal3.emit(image)

                result, frame = cv2.imencode('.jpg', img, self.encode_param)
                data = pickle.dumps(frame, 0)
                size = len(data)

                for conn in self.all_connections:
                    if conn.fileno() != -1:
                        try:
                            conn.sendall(struct.pack(">L", size) + data)
                        except:
                            continue

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Thread4(QThread):
    signal4 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

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
        self.all_connections = []
        self.all_addresses = []

        try:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print('Socket created')
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error:
            print "Error creating socket"
            # sys.exit(1)

        try:
            self.s.bind((socket.gethostname(),8484))
            print('Socket bind complete')
        except socket.gaierror:
            print "Address-related error connecting to server"
            # sys.exit(1)
        except socket.error:
            print "Connection error"
            # sys.exit(1)

        self.s.listen(10)
        print('Socket now listening')

        cam = cv2.VideoCapture(0)

        thr = threading.Thread(target=self.accepting_connectns)
        thr.start()
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        while self.plzrun:
            b, img = cam.read()
            if b:
                rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signal4.emit(image)

                result, frame = cv2.imencode('.jpg', img, self.encode_param)
                data = pickle.dumps(frame, 0)
                size = len(data)

                for conn in self.all_connections:
                    if conn.fileno() != -1:
                        try:
                            conn.sendall(struct.pack(">L", size) + data)
                        except:
                            continue

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Thread5(QThread):
    signal5 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

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
        self.all_connections = []
        self.all_addresses = []

        try:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print('Socket created')
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error:
            print "Error creating socket"
            # sys.exit(1)

        try:
            self.s.bind((socket.gethostname(),8485))
            print('Socket bind complete')
        except socket.gaierror:
            print "Address-related error connecting to server"
            # sys.exit(1)
        except socket.error:
            print "Connection error"
            # sys.exit(1)

        self.s.listen(10)
        print('Socket now listening')

        cam = cv2.VideoCapture(0)

        thr = threading.Thread(target=self.accepting_connectns)
        thr.start()
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        while self.plzrun:
            b, img = cam.read()
            if b:
                rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signal5.emit(image)

                result, frame = cv2.imencode('.jpg', img, self.encode_param)
                data = pickle.dumps(frame, 0)
                size = len(data)

                for conn in self.all_connections:
                    if conn.fileno() != -1:
                        try:
                            conn.sendall(struct.pack(">L", size) + data)
                        except:
                            continue

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()


class Thread6(QThread):
    signal6 = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.plzrun = True

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
        self.all_connections = []
        self.all_addresses = []

        try:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print('Socket created')
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error:
            print "Error creating socket"
            # sys.exit(1)

        try:
            self.s.bind((socket.gethostname(),8486))
            print('Socket bind complete')
        except socket.gaierror:
            print "Address-related error connecting to server"
            # sys.exit(1)
        except socket.error:
            print "Connection error"
            # sys.exit(1)

        self.s.listen(10)
        print('Socket now listening')

        cam = cv2.VideoCapture(0)

        thr = threading.Thread(target=self.accepting_connectns)
        thr.start()
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        while self.plzrun:
            b, img = cam.read()
            if b:
                rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convimg1 = QImage(rgbimg.data, rgbimg.shape[1], rgbimg.shape[0], QImage.Format_RGB888)
                convimg2 = QPixmap.fromImage(convimg1)
                image = convimg2.scaled(500,500,Qt.KeepAspectRatio)
                self.signal6.emit(image)

                result, frame = cv2.imencode('.jpg', img, self.encode_param)
                data = pickle.dumps(frame, 0)
                size = len(data)

                for conn in self.all_connections:
                    if conn.fileno() != -1:
                        try:
                            conn.sendall(struct.pack(">L", size) + data)
                        except:
                            continue

    def stop(self):
        self.plzrun = False
        self.quit()
        self.wait()
'''

'''
class CamFeed(QThread):
    global img1,img2,img3,img4,img5,img6

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)

    # def sendtoclient(self, conn):
    #     while True:
    #         ret, frame = self.cam.read()
    #         result, frame = cv2.imencode('.jpg', frame, self.encode_param)
    #         data = pickle.dumps(frame, 0)
    #         size = len(data)
    #
    #         try:
    #             conn.sendall(struct.pack(">L", size) + data)
    #         except:
    #             print("Error sending data")

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
        self.all_connections = []
        self.all_addresses = []

        try:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print('Socket created')
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error:
            print "Error creating socket"
            # sys.exit(1)

        try:
            self.s.bind((socket.gethostname(),8486))
            print('Socket bind complete')
        except socket.gaierror:
            print "Address-related error connecting to server"
            # sys.exit(1)
        except socket.error:
            print "Connection error"
            # sys.exit(1)

        self.s.listen(10)
        print('Socket now listening')

        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 320)
        self.cam.set(4, 240)

        thr = threading.Thread(target=self.accepting_connectns)
        thr.start()

        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        # while True:
        #     try:
        #         conn, addr= self.s.accept()
        #         threading.Thread(target=self.sendtoclient,args=(conn,)).start()
        #     except:
        #         print "Error accepting connection"

        while True:
            ret, frame = self.cam.read()
            img1 = img2 = img3 = img4 = img5 = img6 = frame
            vis1 = numpy.concatenate((img1, img2, img3), axis=1)
            vis2 = numpy.concatenate((img1, img2, img3), axis=1)
            vis = numpy.concatenate((vis1,vis2), axis=0)
            result, frame = cv2.imencode('.jpg', vis, self.encode_param)
            data = pickle.dumps(frame, 0)
            size = len(data)

            for conn in self.all_connections:
                if conn.fileno() != -1:
                    try:
                        conn.sendall(struct.pack(">L", size) + data)
                    except:
                        continue


        thr.join()
        cam.release()
        s.close()
'''
