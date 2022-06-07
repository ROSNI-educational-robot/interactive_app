# Import the necessary libraries
from math import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import ctypes
import os

from Robot import *

# Detect and save the screen sizes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

screenWidth = user32.GetSystemMetrics(0)
screenHeight = user32.GetSystemMetrics(1)

robotx = 325
roboty = 125

Directory = os.getcwd()
RoutesDirectory = Directory.replace('\Scripts', '\Routes')


class ShowMapWindow(QMainWindow):

    def __init__(self, mare, RouteName):

        super().__init__()
        self.setWindowTitle('Map')
        self.resize(screenWidth, screenHeight)
        self.setStyleSheet(
            "background-color: qlineargradient(x1: 0, x2: 1, stop: 0 #202020, stop: 1 #50005E)")

        self.mare = mare

        self.RouteName = RouteName
        self.robotRad = 50

        self.lpx = []
        self.lpy = []
        self.lpx_def = []
        self.lpy_def = []
        self.lpx_def_units = []
        self.lpy_def_units = []
        self.loxi = []
        self.loyi = []
        self.loxf = []
        self.loyf = []
        self.c = 0

        self.MainWidgets()
        self.GetRouteParameters()
        self.R.move(self.lpx[0]-self.robotRad, self.lpy[0]-self.robotRad)

    # Create a function to create the main widgets of the window

    def MainWidgets(self):

        self.R = Robot(self, 100, 100)
        self.R.move(robotx-self.robotRad, roboty-self.robotRad)
        self.R.resize(150, 150)
        self.R.setStyleSheet("background-color:transparent;")
        self.R.show()

        self.StopButton = QPushButton(self)
        self.StopButton.setText("Stop")
        self.StopButton.move(10, 10)
        self.StopButton.resize(160, 35)
        self.StopButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.StopButton.show()

        self.StopButton.clicked.connect(lambda: self.StopRobot())

    def GetRouteParameters(self):

        self.fr = open(RoutesDirectory+"\\"+self.RouteName, 'r')

        # Read the lines of the document and assign them to their respective variables
        self.cpx = self.fr.readline()
        self.cpy = self.fr.readline()
        self.cpx_def = self.fr.readline()
        self.cpy_def = self.fr.readline()
        self.cpx_def_units = self.fr.readline()
        self.cpy_def_units = self.fr.readline()
        self.coxi = self.fr.readline()
        self.coyi = self.fr.readline()
        self.coxf = self.fr.readline()
        self.coyf = self.fr.readline()
        self.cc = self.fr.readline()

        # If there's a ';' in the text split the text by the ';' to create a list
        if ';' in self.cpx:
            self.fpx = self.cpx.split(';')
        # If there's no ';' in the text create a list and appent the text to the list
        else:
            self.fpx = []
            self.fpx.append(self.cpx)
        if ';' in self.cpy:
            self.fpy = self.cpy.split(';')
        else:
            self.fpy = []
            self.fpy.append(self.cpy)
        if ';' in self.cpx_def:
            self.fpx_def = self.cpx_def.split(';')
        else:
            self.fpx_def = []
            self.fpx_def.append(self.cpx_def)
        if ';' in self.cpy_def:
            self.fpy_def = self.cpy_def.split(';')
        else:
            self.fpy_def = []
            self.fpy_def.append(self.cpy_def)
        if ';' in self.cpx_def_units:
            self.fpx_def_units = self.cpx_def_units.split(';')
        else:
            self.fpx_def_units = []
            self.fpx_def_units.append(self.cpx_def_units)
        if ';' in self.cpy_def_units:
            self.fpy_def_units = self.cpy_def_units.split(';')
        else:
            self.fpy_def_units = []
            self.fpy_def_units.append(self.cpy_def_units)
        if ';' in self.coxi:
            self.foxi = self.coxi.split(';')
        else:
            self.foxi = []
            self.foxi.append(self.coxi)
        if ';' in self.coyi:
            self.foyi = self.coyi.split(';')
        else:
            self.foyi = []
            self.foyi.append(self.coyi)
        if ';' in self.coxf:
            self.foxf = self.coxf.split(';')
        else:
            self.foxf = []
            self.foxf.append(self.coxf)
        if ';' in self.coyf:
            self.foyf = self.coyf.split(';')
        else:
            self.foyf = []
            self.foyf.append(self.coyf)

        # Initialize a counter
        i1 = 0

        # For the counter in range from 0 to the lenght of the coordinates lists proceed
        for i1 in range(0, len(self.fpx)):

            # Save the text in the position i1 of the list, supress the '\n', convert it into an integer and append it to its respective list
            string_fpx = self.fpx[i1]
            string_fpx = string_fpx.strip('\n')
            self.lpx.append(int(string_fpx))

            string_fpy = self.fpy[i1]
            string_fpy = string_fpy.strip('\n')
            self.lpy.append(int(string_fpy))

            string_fpx_def = self.fpx_def[i1]
            string_fpx_def = string_fpx_def.strip('\n')
            self.lpx_def.append(int(string_fpx_def))

            string_fpy_def = self.fpy_def[i1]
            string_fpy_def = string_fpy_def.strip('\n')
            self.lpy_def.append(int(string_fpy_def))

            string_fpx_def_units = self.fpx_def_units[i1]
            string_fpx_def_units = string_fpx_def_units.strip('\n')
            self.lpx_def_units.append(float(string_fpx_def_units))

            string_fpy_def_units = self.fpy_def_units[i1]
            string_fpy_def_units = string_fpy_def_units.strip('\n')
            self.lpy_def_units.append(float(string_fpy_def_units))

        # Initialize a counter
        i2 = 0

        # For the counter in range from 0 to the lenght of the obstacles lists proceed
        for i2 in range(0, len(self.foxi)):

            # Save the text in the position i2 of the list, supress the '\n', convert it into an integer and append it to its respective list
            string_foxi = self.foxi[i2]
            string_foxi = string_foxi.strip('\n')
            self.loxi.append(int(string_foxi))

            string_foyi = self.foyi[i2]
            string_foyi = string_foyi.strip('\n')
            self.loyi.append(int(string_foyi))

            string_foxf = self.foxf[i2]
            string_foxf = string_foxf.strip('\n')
            self.loxf.append(int(string_foxf))

            string_foyf = self.foyf[i2]
            string_foyf = string_foyf.strip('\n')
            self.loyf.append(int(string_foyf))

        # Erase the '\n' from the text
        self.c = self.cc.strip('\n')

    # Create a function to paint the coordinates and more in the map
    def paintEvent(self, event):

        p = QPainter(self)

        # Initialize the QPainter
        p.begin(self)

        # Initialize a counter
        self.cnt = 1

        # If the lenght of the coordinates list isn't 0...
        if len(self.lpx) != 0:

            # Call the function drawPoint to draw the initial coordinate
            self.drawPoint(p, self.lpx[0]-5, self.lpy[0]-5)

            # For the counter larger than 1 and shorter than the lenght of the coordinates list...
            for self.cnt in range(1, len(self.lpx)):

                # Call the function drawPoint to draw the coordinate and call the function drawLine to draw the trajectory
                self.drawPoint(
                    p, self.lpx[self.cnt]-5, self.lpy[self.cnt]-5)
                self.drawLine(
                    p, self.lpx[self.cnt-1], self.lpy[self.cnt-1], self.lpx[self.cnt], self.lpy[self.cnt])

                str_cnt = str(self.cnt)

                # Call the function drawText to draw the number of the coordinate on its positon
                self.drawText(
                    p, self.lpx[self.cnt]+10, self.lpy[self.cnt]-10, str_cnt)

            str_cnt = str(self.cnt)
            self.drawText(
                p, self.lpx[self.cnt]+10, self.lpy[self.cnt]-10, str_cnt)

        # If the lenght of the obstacles list isn't 0...
        if len(self.loxi) != 0:

            # Initialize a counter
            self.cnt = 1
            # For the counter larger than 1 and shorter than the lenght of the obstacles list...
            for self.cnt in range(0, len(self.loxi)):

                # Call the function drawRectangle to draw the obstacle on its position and also draw its contour using the function drawRectangleContour
                self.drawRectangle(
                    p, self.loxi[self.cnt], self.loyi[self.cnt], self.loxf[self.cnt], self.loyf[self.cnt])
                self.drawRectangleContour(
                    p, self.loxi[self.cnt], self.loyi[self.cnt], self.loxf[self.cnt], self.loyf[self.cnt])

                str_cnt = str(self.cnt)
                # Call the function drawText to draw the number of the obstacle on its position if the counter is larger than 0
                if int(str_cnt) > 0:
                    self.drawText(
                        p, self.loxi[self.cnt]+10, self.loyi[self.cnt]+25, str_cnt)

        # End the QPainter
        p.end()

    # Create the drawing functions

    def drawPoint(self, p, x, y):

        c = QColor(255, 255, 255)
        r = QRect(x, y, 10, 10)
        p.setPen(c)
        p.setBrush(c)
        p.drawEllipse(r)

    def drawLine(self, p, x0, y0, x1, y1):

        c = QColor(255, 255, 255, 100)
        p.setPen(QPen(c, 3))
        p.drawLine(x0, y0, x1, y1)

    def drawRectangle(self, p, xr, yr, wr, hr):

        c = QColor(32, 32, 32, 100)
        p.setPen(c)
        p.setBrush(c)
        p.drawRect(xr, yr, wr, hr)

    def drawRectangleContour(self, p, xc, yc, wc, hc):

        c = QColor(255, 255, 255, 100)
        p.setPen(QPen(c, 3))
        p.drawRect(xc, yc, wc, hc)

    def drawText(self, p, x, y, text):

        p.setPen(QColor(255, 255, 255, 100))
        p.setFont(QFont('Decorative', 10))
        p.drawText(x, y, text)

    def drawCoordRef(self, p, x, y, coordtext):

        p.setPen(QColor(255, 255, 255, 100))
        p.setFont(QFont('Decorative', 10))
        p.drawText(x, y, coordtext)

    # Create a function to stop the robot
    def StopRobot(self):

        self.mare.SocketSendBridge()
