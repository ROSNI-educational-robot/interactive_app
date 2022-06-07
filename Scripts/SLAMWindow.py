# Import the necessary libraries
from math import *
from re import T
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import ctypes
import threading
import time

from Robot import *

# Detect and save the screen sizes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

screenWidth = user32.GetSystemMetrics(0)
screenHeight = user32.GetSystemMetrics(1)

robotx = 325
roboty = 125


class SLAMWindow(QMainWindow):

    # Create a signal when the window has been resized
    resized = pyqtSignal()

    def __init__(self, mare):

        super().__init__()
        self.setWindowTitle('SLAM Map')
        self.resize(screenWidth, screenHeight)
        self.setStyleSheet(
            "background-color: qlineargradient(x1: 0, x2: 1, stop: 0 #202020, stop: 1 #50005E)")

        self.mare = mare

        self.resized.connect(self.WindowResized)

        self.windowWidth = self.width()
        self.windowHeight = self.height()

        self.robotRad = 25
        self.image_SLAM = b''
        self.pix_img = QPixmap()

        self.MainWidgets()
        #self.GetSLAMImage()


    def resizeEvent(self, event):

        # Emit the resized signal
        self.resized.emit()

    # Create the function to update the window sizes and the widgets sizes and positions depending on the width ans height of the window
    def WindowResized(self):

        self.windowWidth = self.width()
        self.windowHeight = self.height()

        #.scaled(int(self.windowWidth*0.5), int(self.windowWidth*0.5))
        self.SLAMImage.setPixmap(self.pix_img)
        self.SLAMImage.resize(self.pix_img.width(), self.pix_img.height())

        self.SLAMImageW = self.SLAMImage.width()
        self.SLAMImageH = self.SLAMImage.height()

        self.R.move(int(300+self.SLAMImageW/2-self.robotRad),
                    int(10+self.SLAMImageH/2-self.robotRad))

    # Create a function to create the main widgets of the window

    def MainWidgets(self):
        self.StopButton = QPushButton(self)
        self.StopButton.setText("Stop")
        self.StopButton.move(10, 10)
        self.StopButton.resize(160, 35)
        self.StopButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.StopButton.show()

        self.SLAMImage = QLabel(self)
        self.SLAMImage.move(300, 10)
        #self.pix_img = QPixmap()#.scaled(
        #     int(self.windowWidth*0.5), int(self.windowWidth*0.5))
        self.SLAMImage.setPixmap(self.pix_img)
        self.SLAMImage.resize(self.pix_img.width(), self.pix_img.height())

        self.SLAMImageW = self.SLAMImage.width()
        self.SLAMImageH = self.SLAMImage.height()

        self.R = Robot(self, 50, 50)
        self.R.move(int(220+self.SLAMImageW/2-self.robotRad),
                    int(10+self.SLAMImageH/2-self.robotRad))
        self.R.resize(50, 50)
        self.R.setStyleSheet("background-color:transparent;")
        #self.R.show()

        self.StopButton.clicked.connect(lambda: self.StopRobot())
        self.slam_process = threading.Thread(target=self.GetSLAMImage, daemon=True)
        self.slam_process.start()

    def GetSLAMImage(self):
        # Try to compute
        try:
            self.SLAMMessage = 'Initialize_SLAM'
            self.mare.SocketSendROS(self.SLAMMessage)

            while True:
                #self.pix_img = ReceiveSLAMImage(self)
                self.image_SLAM += self.mare.sockR.recv(1024)
                while b'XXXXX' not in self.image_SLAM:
                    self.image_SLAM += self.mare.sockR.recv(1024)
                    time.sleep(0.5)
                self.image_SLAM = self.image_SLAM.split(b'XXXXX')[1]

                self.image_SLAM += self.mare.sockR.recv(10)
                len_data = int(self.image_SLAM[:10].decode("ascii"))
                self.image_SLAM = self.image_SLAM[10:]
                while len(self.image_SLAM)<len_data:
                    self.image_SLAM += self.mare.sockR.recv(1024)
                frame = self.image_SLAM[:len_data]
                self.image_SLAM = self.image_SLAM[len_data:]

                img = QImage.fromData(frame)
                #img.save("image1.jpg","JPG")
                self.pix_img = QPixmap(img).scaled(int(self.windowWidth*0.5), int(self.windowWidth*0.5))
                self.WindowResized()

        # If the program can't be computed show a warning window
        except:
            self.WarningConnection()

    def StopRobot(self):

        # Try to compute
        try:
            self.StopMessage = 'Stop_SLAM'
            self.mare.SocketSendROS(self.StopMessage)
            self.slam_process.kill()

        # If the program can't be computed show a warning window
        except:
            self.WarningConnection()

    # Create a warning window for connection errors
    def WarningConnection(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! Unable to connect with the server")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

def ReceiveSLAMImage(obj):
    obj.image_Slam += obj.sockR.recv(1024)
    while not obj.image_Slam:
        obj.image_Slam += obj.sockR.recv(1024)
    
    len_data = int(obj.image_Slam[:10].decode(ascii))
    obj.image_Slam = obj.image_Slam[10:]
    while len(obj.image_Slam)<len_data:
        obj.image_Slam += obj.sockR.recv(1024)
    frame = obj.image_Slam[:len_data]
    obj.image_Slam = obj.image_Slam[len_data:]

    img = QImage.fromData(frame)
    pix_img = QPixmap(img)
    return pix_img

def f():
    while True:
        print("hola")
        time.sleep(2)