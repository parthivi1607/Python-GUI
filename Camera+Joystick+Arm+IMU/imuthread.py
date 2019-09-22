from joystickthread import *


class ThreadIMU(QThread):

    signalIMU = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=None)
        self.i = 0

    def run(self):
        while True:
            if self.i<=360:
                self.i = self.i + 1
            else:
                self.i=0
            val = str(self.i)+"°"
            self.signalIMU.emit(val)
            time.sleep(0.1)


