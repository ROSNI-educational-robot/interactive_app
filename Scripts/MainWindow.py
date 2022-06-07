# Import the necessary libraries
import ctypes
from email.mime import image
import os
import socket
import sys
from math import *
from time import sleep
import webbrowser

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Import the other python scripts
from ConfigurateWiFiWindow import *
from EditCoordinatesWindow import *
from EditObstacleWindow import *
from InputIPWindow import *
from InputObstaclesWindow import *
from OpenWindow import *
from Robot import *
from SaveWindow import *
from ConfigWindow import *
from SendRouteWindow import *
from SLAMWindow import *
from CropImage import *

# Detect and save the screen sizes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

screenWidth = user32.GetSystemMetrics(0)
screenHeight = user32.GetSystemMetrics(1)

robotx = 325
roboty = 125

widg_pos = 50


# Create a function that computes the angle between two vectors
def VectorsAngle(x1, y1, x2, y2, xi, yi):

    angle = atan2(x1*y2-y1*x2, x1*x2+y1*y2)

    return angle


# Create a function that converts an angle from Radiants to Degrees
def RadToDeg(angleRad):

    angleDeg = angleRad*180/pi

    return angleDeg


# Create a function that computes the initial angle depending of the first x and y positions
def InitialAngle(x, y):

    if x == 0 and y == 0:
        initialAngle = 0
    elif x == 0 and y > 0:
        initialAngle = -90
    elif x == 0 and y < 0:
        initialAngle = 90
    elif y == 0 and x > 0:
        initialAngle = 0
    elif y == 0 and x < 0:
        initialAngle = 180
    else:
        initialAngle = RadToDeg(atan(y/x))
        if x < 0 and y < 0:
            initialAngle = (180-initialAngle)*(-1)
        elif x < 0 and y > 0:
            initialAngle = (-180-initialAngle)*(-1)
        else:
            initialAngle = initialAngle

    return initialAngle


####################################################################################
#MAIN WINDOW#
####################################################################################

class MainWindow(QMainWindow):

    # Create a signal when the window has been resized
    resized = pyqtSignal()

    def __init__(self):

        super().__init__()
        self.resize(1175, 630)
        self.setWindowTitle('Virtual Routes App')
        self.setMinimumSize(1175, 630)

        # Connect the signal of resized to a function named WindowResized
        self.resized.connect(self.WindowResized)
        self.setStyleSheet(
            "background-color: qlineargradient(x1: 0, x2: 1, stop: 0 #202020, stop: 1 #50005E)")

        self.image_Slam = b''

        # Create variables
        self.windowWidth = self.width()
        self.windowHeight = self.height()
        self.c = 0
        self.lpx = []
        self.lpy = []
        self.lpx_def = [0]
        self.lpy_def = [0]
        self.lpx_def_units = [0]
        self.lpy_def_units = [0]
        self.units = 1
        self.SNvariable = False
        self.flag = False
        self.flag_reset = False
        self.flag_robot_change = False
        self.flag_obstacle = False
        self.flagCoordRef = False
        self.CoordType = False
        self.cx = 0
        self.cy = 0
        self.robotRad = 50
        self.LimitZonex = screenWidth-robotx+25
        self.LimitZoney = screenHeight-roboty-35
        self.loxi = [0]
        self.loyi = [0]
        self.loxf = [0]
        self.loyf = [0]
        self.lpa = [0]
        self.lc = [0]
        self.lu = [1]
        self.cnt1 = 0
        self.simSpeed = 1
        self.angle = 0
        self.check_connection = 0
        self.port = 65432
        self.portROS = 54321

        # Import functions to the MainWindow
        self.MenuWidgets()
        self.RobOptionsWidgets()
        self.VirtRouteWidgets()
        self.flagCoordRef = False
        self.ConnectionsWidgets()

        # Make the main buttons visible
        self.RobOptionsButton.show()
        self.VirtRouteButton.show()
        self.RobConnectionsButton.show()

        # Hide the specific widgets (not visible in the main menu)
        self.R.hide()
        self.EditionFrame.hide()
        self.TopFrame.hide()
        self.LimitZone.hide()
        self.CoordTypeLabel.hide()
        self.AbsCoordButton.hide()
        self.IncCoordButton.hide()
        self.UnitsLabel.hide()
        self.cb.hide()
        self.CheckBox.hide()
        self.RobLabel.hide()
        self.RobxLineEdit.hide()
        self.RobyLineEdit.hide()
        self.AcceptRobButton.hide()
        self.CoordLabel.hide()
        self.PxLineEdit.hide()
        self.PyLineEdit.hide()
        self.AcceptButton.hide()
        self.EditCoordinatesButton.hide()
        self.ResetButton.hide()
        self.SimulateButton.hide()
        self.ResetSimulationButton.hide()
        self.RobxLabel.hide()
        self.RobyLabel.hide()
        self.pxLabel.hide()
        self.pyLabel.hide()
        self.MenuVRButton.hide()
        self.MenuCButton.hide()
        self.MenuROButton.hide()
        self.InputObstacleButton.hide()
        self.EditObstacleButton.hide()
        self.ResetObstaclesButton.hide()
        self.OpenButton.hide()
        self.SaveButton.hide()
        self.HelpButton.hide()
        self.x1Button.hide()
        self.x10Button.hide()
        self.x100Button.hide()
        self.ConnectToRobotButton.hide()
        self.ConfigurateWiFiButton.hide()
        self.ConfigButton.hide()
        self.RobCommandsButton.hide()
        self.RobWikiButton.hide()
        self.SendRouteButton.hide()
        self.SLAMButton.hide()

    # Create the function to resize the window

    def resizeEvent(self, event):

        # Emit the resized signal
        self.resized.emit()

    # Create the function to update the window sizes and the widgets sizes and positions depending on the width ans height of the window
    def WindowResized(self):

        self.windowWidth = self.width()
        self.windowHeight = self.height()

        self.RobOptionsButton.setGeometry(int(self.windowWidth*1/4.8), int(
            self.windowHeight*1/3), int(self.windowWidth/5.5), int(self.windowWidth/5.5))
        self.VirtRouteButton.setGeometry(int(self.windowWidth*2/4.8), int(
            self.windowHeight*1/3), int(self.windowWidth/5.5), int(self.windowWidth/5.5))
        self.RobConnectionsButton.setGeometry(int(self.windowWidth*3/4.8), int(
            self.windowHeight*1/3), int(self.windowWidth/5.5), int(self.windowWidth/5.5))

        self.MenuROButton.move(self.windowWidth-140, 10)
        self.RobCommandsButton.setGeometry(int(self.windowWidth*1/5), int(
            self.windowHeight/4), int(self.windowWidth/4), int(self.windowWidth/4))
        self.RobWikiButton.setGeometry(int(self.windowWidth*2/3.5), int(
            self.windowHeight/4), int(self.windowWidth/4), int(self.windowWidth/4))
        self.SLAMButton.setGeometry(int(self.windowWidth*1/5), int(
            self.windowHeight/4), int(self.windowWidth/4), int(self.windowWidth/4))
        self.SendRouteButton.setGeometry(int(self.windowWidth*2/3.5), int(
            self.windowHeight/4), int(self.windowWidth/4), int(self.windowWidth/4))

        self.MenuVRButton.move(self.windowWidth-140, 10)

        self.MenuCButton.move(self.windowWidth-140, 10)
        self.ConnectToRobotButton.setGeometry(int(self.windowWidth*1/5), int(
            self.windowHeight/4), int(self.windowWidth/4), int(self.windowWidth/4))
        self.ConfigurateWiFiButton.setGeometry(int(self.windowWidth*2/3.5), int(
            self.windowHeight/4), int(self.windowWidth/4), int(self.windowWidth/4))

    # Create a function to create the menu widgets
    def MenuWidgets(self):

        self.RobOptionsButton = QPushButton(self)
        self.RobOptionsButton.setText("Robot Options")
        self.RobOptionsButton.setGeometry(
            int(self.windowWidth/2-200)-75, int(self.windowHeight/2)-85, 160, 160)
        self.RobOptionsButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

        self.VirtRouteButton = QPushButton(self)
        self.VirtRouteButton.setText("Virtual Routes")
        self.VirtRouteButton.setGeometry(
            int(self.windowWidth/2)-75, int(self.windowHeight/2)-85, 160, 160)
        self.VirtRouteButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

        self.RobConnectionsButton = QPushButton(self)
        self.RobConnectionsButton.setText("Robot Connections")
        self.RobConnectionsButton.setGeometry(
            int(self.windowWidth/2+200)-75, int(self.windowHeight/2)-85, 160, 160)
        self.RobConnectionsButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

        # If the button is clicked connect it to a function
        self.RobOptionsButton.clicked.connect(lambda: self.RobOptionsWidgets())
        self.VirtRouteButton.clicked.connect(lambda: self.VirtRouteWidgets())
        self.RobConnectionsButton.clicked.connect(
            lambda: self.ConnectionsWidgets())

    # Create a function to create the robot stats widgets
    def RobOptionsWidgets(self):

        self.MenuROButton = QPushButton(self)
        self.MenuROButton.setText("Menu")
        self.MenuROButton.setGeometry(self.windowWidth-140, 10, 130, 30)
        self.MenuROButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.MenuROButton.show()

        self.RobCommandsButton = QPushButton(self)
        self.RobCommandsButton.setText("Robot Commands")
        self.RobCommandsButton.setGeometry(int(self.windowWidth*1/5), int(
            self.windowHeight/4), int(self.windowWidth/4), int(self.windowWidth/4))
        self.RobCommandsButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.RobCommandsButton.show()

        self.RobWikiButton = QPushButton(self)
        self.RobWikiButton.setText("Robot Wiki")
        self.RobWikiButton.setGeometry(int(self.windowWidth*2/3.5), int(
            self.windowHeight/4), int(self.windowWidth/4), int(self.windowWidth/4))
        self.RobWikiButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.RobWikiButton.show()

        self.SendRouteButton = QPushButton(self)
        self.SendRouteButton.setText("Send Route")
        self.SendRouteButton.setGeometry(int(self.windowWidth*1/5), int(
            self.windowHeight/4), int(self.windowWidth/4), int(self.windowWidth/4))
        self.SendRouteButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.SendRouteButton.hide()

        self.SLAMButton = QPushButton(self)
        self.SLAMButton.setText("SLAM")
        self.SLAMButton.setGeometry(int(self.windowWidth*2/3.5), int(
            self.windowHeight/4), int(self.windowWidth/4), int(self.windowWidth/4))
        self.SLAMButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.SLAMButton.hide()

        # If the button is clicked connect it to a function
        self.MenuROButton.clicked.connect(lambda: self.Menu())
        self.RobCommandsButton.clicked.connect(
            lambda: self.GoToRobCommandsWindow())
        self.SendRouteButton.clicked.connect(lambda: self.SendRouteWindow())
        self.RobWikiButton.clicked.connect(lambda: self.OpenWiki())
        self.SLAMButton.clicked.connect(lambda: self.OpenSLAMWindow())

        # Hide the menu widgets
        self.RobOptionsButton.hide()
        self.VirtRouteButton.hide()
        self.RobConnectionsButton.hide()

    # Create a function to create the connections widgets
    def ConnectionsWidgets(self):

        # Hide the menu widgets
        self.RobOptionsButton.hide()
        self.VirtRouteButton.hide()
        self.RobConnectionsButton.hide()

        self.ConnectToRobotButton = QPushButton(self)
        self.ConnectToRobotButton.setText("Connect To Robot")
        self.ConnectToRobotButton.setGeometry(int(self.windowWidth*1/5), int(
            self.windowHeight/4), int(self.windowWidth/4), int(self.windowWidth/4))
        self.ConnectToRobotButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.ConnectToRobotButton.show()

        self.ConfigurateWiFiButton = QPushButton(self)
        self.ConfigurateWiFiButton.setText("Configurate WiFi")
        self.ConfigurateWiFiButton.setGeometry(int(self.windowWidth*2/3.5), int(
            self.windowHeight/4), int(self.windowWidth/4), int(self.windowWidth/4))
        self.ConfigurateWiFiButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.ConfigurateWiFiButton.show()

        self.ConfigButton = QPushButton(self)
        self.ConfigButton.setGeometry(10, 10, 30, 30)
        self.ConfigButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.ConfigButton.setIcon(QIcon('Config.png'))
        self.ConfigButton.setIconSize(QSize(15, 15))
        self.ConfigButton.show()

        self.MenuCButton = QPushButton(self)
        self.MenuCButton.setText("Menu")
        self.MenuCButton.setGeometry(self.windowWidth-140, 10, 130, 30)
        self.MenuCButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.MenuCButton.show()

        # If the button is clicked connect it to a function
        self.MenuCButton.clicked.connect(lambda: self.Menu())
        self.ConnectToRobotButton.clicked.connect(lambda: self.GoToIPWindow())
        self.ConfigurateWiFiButton.clicked.connect(
            lambda: self.GoToWiFiWindow())
        self.ConfigButton.clicked.connect(lambda: self.GoToConfigWindow())

    # Create a function to create the virtual route widgets
    def VirtRouteWidgets(self):

        # Hide the menu widgets
        self.RobOptionsButton.hide()
        self.VirtRouteButton.hide()
        self.RobConnectionsButton.hide()

        self.R = Robot(self, 100, 100)
        self.R.move(robotx-self.robotRad, roboty-self.robotRad)
        self.R.resize(100, 100)
        self.R.setStyleSheet("background-color:transparent;")
        self.R.show()

        self.flagCoordRef = True

        self.EditionFrame = QWidget(self)
        self.EditionFrame.setStyleSheet(
            "background-color: rgba(255,255,255,20)")
        self.EditionFrame.resize(225, screenHeight)
        self.EditionFrame.move(0, 50)
        self.EditionFrame.show()

        self.TopFrame = QWidget(self)
        self.TopFrame.setStyleSheet("background-color: rgba(255,255,255,20)")
        self.TopFrame.resize(screenWidth, 50)
        self.TopFrame.move(0, 0)
        self.TopFrame.show()

        self.LimitZone = QWidget(self)
        self.LimitZone.setStyleSheet(
            "background-color: transparent; border-width: 3px; border-color: rgb(255,255,255,100); border-style: solid;")
        self.LimitZone.setGeometry(
            robotx-self.robotRad, roboty-self.robotRad, self.LimitZonex, self.LimitZoney)
        self.LimitZone.show()

        self.OpenButton = QPushButton(self)
        self.OpenButton.setText("Open")
        self.OpenButton.setGeometry(0, 0, 75, 30)
        self.OpenButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20);}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.OpenButton.show()

        self.SaveButton = QPushButton(self)
        self.SaveButton.setText("Save")
        self.SaveButton.setGeometry(75, 0, 75, 30)
        self.SaveButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20);}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.SaveButton.show()

        self.HelpButton = QPushButton(self)
        self.HelpButton.setText("Help")
        self.HelpButton.setGeometry(150, 0, 75, 30)
        self.HelpButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20);}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.HelpButton.show()

        self.MenuVRButton = QPushButton(self)
        self.MenuVRButton.setText("Menu")
        self.MenuVRButton.setGeometry(self.windowWidth-140, 10, 130, 30)
        self.MenuVRButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.MenuVRButton.show()

        self.CoordTypeLabel = QLabel('Coordinates Type', self)
        self.CoordTypeLabel.move(275, 10)
        self.CoordTypeLabel.resize(180, 30)
        self.CoordTypeLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color: white; font-weight: bold; font-size: 10pt; font-family: Helvetica")
        self.CoordTypeLabel.show()

        self.AbsCoordButton = QPushButton(self)
        self.AbsCoordButton.setText("A")
        self.AbsCoordButton.setGeometry(475, 10, 30, 30)
        self.AbsCoordButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,100); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.AbsCoordButton.setCheckable(True)
        self.AbsCoordButton.setEnabled(False)
        self.AbsCoordButton.show()

        self.IncCoordButton = QPushButton(self)
        self.IncCoordButton.setText("I")
        self.IncCoordButton.setGeometry(515, 10, 30, 30)
        self.IncCoordButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.IncCoordButton.setCheckable(True)
        self.IncCoordButton.show()

        self.UnitsLabel = QLabel('Units', self)
        self.UnitsLabel.move(600, 10)
        self.UnitsLabel.resize(100, 30)
        self.UnitsLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 10pt; font-family: Helvetica")
        self.UnitsLabel.show()

        self.cb = QComboBox(self)
        self.cb.move(670, 10)
        self.cb.addItems(["m", "dm", "cm", "mm"])
        self.cb.setStyleSheet(
            "selection-background-color: rgb(255,255,255,100); background-color: rgb(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.cb.show()

        self.CheckBox = QCheckBox('Show Numbers', self)
        self.CheckBox.move(820, 15)
        self.CheckBox.resize(200, 20)
        self.CheckBox.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica")
        self.CheckBox.show()

        self.RobLabel = QLabel('Robot Coordinates', self)
        self.RobLabel.move(10, 5+widg_pos)
        self.RobLabel.resize(190, 35)
        self.RobLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 10pt; font-family: Helvetica")
        self.RobLabel.show()

        self.RobxLineEdit = QLineEdit(self)
        self.RobxLineEdit.setGeometry(50, 50+widg_pos, 160, 35)
        self.RobxLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.RobxLineEdit.show()

        self.RobyLineEdit = QLineEdit(self)
        self.RobyLineEdit.setGeometry(50, 90+widg_pos, 160, 35)
        self.RobyLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.RobyLineEdit.show()

        self.AcceptRobButton = QPushButton(self)
        self.AcceptRobButton.setText("Accept")
        self.AcceptRobButton.setGeometry(50, 130+widg_pos, 160, 35)
        self.AcceptRobButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.AcceptRobButton.show()

        self.CoordLabel = QLabel('Route Coordinates', self)
        self.CoordLabel.move(10, 195+widg_pos)
        self.CoordLabel.resize(190, 35)
        self.CoordLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-weight: bold; font-size: 10pt; font-family: Helvetica")
        self.CoordLabel.show()

        self.PxLineEdit = QLineEdit(self)
        self.PxLineEdit.setGeometry(50, 240+widg_pos, 160, 35)
        self.PxLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.PxLineEdit.show()

        self.PyLineEdit = QLineEdit(self)
        self.PyLineEdit.setGeometry(50, 280+widg_pos, 160, 35)
        self.PyLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.PyLineEdit.show()

        self.AcceptButton = QPushButton(self)
        self.AcceptButton.setText("Accept")
        self.AcceptButton.setGeometry(50, 320+widg_pos, 160, 35)
        self.AcceptButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.AcceptButton.show()

        self.EditCoordinatesButton = QPushButton(self)
        self.EditCoordinatesButton.setText("Edit Coordinates")
        self.EditCoordinatesButton.setGeometry(50, 360+widg_pos, 160, 35)
        self.EditCoordinatesButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.EditCoordinatesButton.show()

        self.ResetButton = QPushButton(self)
        self.ResetButton.setText("Reset")
        self.ResetButton.setGeometry(50, 400+widg_pos, 160, 35)
        self.ResetButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.ResetButton.show()

        self.SimulateButton = QPushButton(self)
        self.SimulateButton.setText("Simulate")
        self.SimulateButton.setGeometry(10, 465+widg_pos, 200, 50)
        self.SimulateButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 11pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.SimulateButton.show()

        self.ResetSimulationButton = QPushButton(self)
        self.ResetSimulationButton.setText("Reset Simulation")
        self.ResetSimulationButton.setGeometry(10, 520+widg_pos, 200, 50)
        self.ResetSimulationButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 11pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.ResetSimulationButton.show()

        self.x1Button = QPushButton(self)
        self.x1Button.setText("x1")
        self.x1Button.setGeometry(15, 580+widg_pos, 60, 30)
        self.x1Button.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,100); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.x1Button.setCheckable(True)
        self.x1Button.setEnabled(False)
        self.x1Button.show()

        self.x10Button = QPushButton(self)
        self.x10Button.setText("x10")
        self.x10Button.setGeometry(80, 580+widg_pos, 60, 30)
        self.x10Button.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.x10Button.setCheckable(True)
        self.x10Button.show()

        self.x100Button = QPushButton(self)
        self.x100Button.setText("x100")
        self.x100Button.setGeometry(145, 580+widg_pos, 60, 30)
        self.x100Button.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.x100Button.setCheckable(True)
        self.x100Button.show()

        self.InputObstacleButton = QPushButton(self)
        self.InputObstacleButton.setText("Input Obstacle")
        self.InputObstacleButton.setGeometry(10, 650+widg_pos, 200, 50)
        self.InputObstacleButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 11pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.InputObstacleButton.show()

        self.EditObstacleButton = QPushButton(self)
        self.EditObstacleButton.setText("Edit Obstacle")
        self.EditObstacleButton.setGeometry(10, 705+widg_pos, 200, 50)
        self.EditObstacleButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 11pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.EditObstacleButton.show()

        self.ResetObstaclesButton = QPushButton(self)
        self.ResetObstaclesButton.setText("Reset Obstacles")
        self.ResetObstaclesButton.setGeometry(10, 760+widg_pos, 200, 50)
        self.ResetObstaclesButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 11pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.ResetObstaclesButton.show()

        self.RobxLabel = QLabel('Rx =', self)
        self.RobxLabel.move(10, 55+widg_pos)
        self.RobxLabel.resize(40, 30)
        self.RobxLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.RobxLabel.show()

        self.RobyLabel = QLabel('Ry =', self)
        self.RobyLabel.move(10, 95+widg_pos)
        self.RobyLabel.resize(40, 30)
        self.RobyLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.RobyLabel.show()

        self.pxLabel = QLabel('Px =', self)
        self.pxLabel.move(10, 245+widg_pos)
        self.pxLabel.resize(40, 30)
        self.pxLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.pxLabel.show()

        self.pyLabel = QLabel('Py =', self)
        self.pyLabel.move(10, 285+widg_pos)
        self.pyLabel.resize(40, 30)
        self.pyLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.pyLabel.show()

        # Set a place holder text in the line edit
        self.RobxLineEdit.setPlaceholderText('0')
        self.RobyLineEdit.setPlaceholderText('0')

        # Create an int validator
        intValidator = QIntValidator(self)

        # Apply the int validator to the line edit
        self.RobxLineEdit.setValidator(intValidator)
        self.RobyLineEdit.setValidator(intValidator)

        # Set a place holder text in the line edit
        self.PxLineEdit.setPlaceholderText('0')
        self.PyLineEdit.setPlaceholderText('0')

        # Apply the int validator to the line edit
        self.PxLineEdit.setValidator(intValidator)
        self.PyLineEdit.setValidator(intValidator)

        # If the button is clicked connect it to a function
        self.AcceptRobButton.clicked.connect(lambda: self.GetRobxy())
        self.AcceptButton.clicked.connect(lambda: self.Getxy())
        self.AcceptButton.clicked.connect(lambda: self.GetAngle())
        self.AcceptRobButton.clicked.connect(
            lambda: self.ResetRobotAnimation())
        self.AcceptButton.clicked.connect(lambda: self.ResetRobotAnimation())
        self.EditCoordinatesButton.clicked.connect(
            lambda: self.GoToEditCoordinatesWindow())
        self.ResetButton.clicked.connect(lambda: self.ResetValues())
        self.ResetButton.clicked.connect(lambda: self.ResetRobotAnimation())
        self.SimulateButton.clicked.connect(lambda: self.RobotAnimation())
        self.ResetSimulationButton.clicked.connect(
            lambda: self.ResetRobotAnimation())
        self.AbsCoordButton.clicked.connect(lambda: self.AbsCoord())
        self.IncCoordButton.clicked.connect(lambda: self.IncCoord())
        self.cb.activated.connect(lambda: self.Units())
        self.CheckBox.stateChanged.connect(self.ShowNumbers)
        self.MenuVRButton.clicked.connect(lambda: self.Menu())
        self.InputObstacleButton.clicked.connect(
            lambda: self.GoToInputObstacle())
        self.EditObstacleButton.clicked.connect(
            lambda: self.GoToEditObstacle())
        self.ResetObstaclesButton.clicked.connect(
            lambda: self.ResetObstacles())
        self.OpenButton.clicked.connect(lambda: self.GoToOpenWindow())
        self.SaveButton.clicked.connect(lambda: self.GoToSaveWindow())
        self.HelpButton.clicked.connect(lambda: self.GoToHelpWindow())
        self.x1Button.clicked.connect(lambda: self.SimulationSpeed1())
        self.x10Button.clicked.connect(lambda: self.SimulationSpeed10())
        self.x100Button.clicked.connect(lambda: self.SimulationSpeed100())


####################################################################################
#MENU#
####################################################################################

    # Create a function to just show the menu widgets


    def Menu(self):

        self.flag = False
        self.flag_obstacle = False
        self.SNvariable = False
        self.flagCoordRef = False
        self.update()

        # Show the menu widgets
        self.RobOptionsButton.show()
        self.VirtRouteButton.show()
        self.RobConnectionsButton.show()

        # Hide the widgets that aren't from the menu
        self.R.hide()
        self.EditionFrame.hide()
        self.TopFrame.hide()
        self.LimitZone.hide()
        self.CoordTypeLabel.hide()
        self.AbsCoordButton.hide()
        self.IncCoordButton.hide()
        self.UnitsLabel.hide()
        self.CheckBox.hide()
        self.cb.hide()
        self.RobLabel.hide()
        self.RobxLineEdit.hide()
        self.RobyLineEdit.hide()
        self.AcceptRobButton.hide()
        self.CoordLabel.hide()
        self.PxLineEdit.hide()
        self.PyLineEdit.hide()
        self.AcceptButton.hide()
        self.EditCoordinatesButton.hide()
        self.ResetButton.hide()
        self.SimulateButton.hide()
        self.ResetSimulationButton.hide()
        self.RobxLabel.hide()
        self.RobyLabel.hide()
        self.pxLabel.hide()
        self.pyLabel.hide()
        self.MenuVRButton.hide()
        self.MenuCButton.hide()
        self.MenuROButton.hide()
        self.InputObstacleButton.hide()
        self.EditObstacleButton.hide()
        self.ResetObstaclesButton.hide()
        self.OpenButton.hide()
        self.SaveButton.hide()
        self.HelpButton.hide()
        self.x1Button.hide()
        self.x10Button.hide()
        self.x100Button.hide()
        self.ConnectToRobotButton.hide()
        self.ConfigurateWiFiButton.hide()
        self.ConfigButton.hide()
        self.RobCommandsButton.hide()
        self.RobWikiButton.hide()
        self.SendRouteButton.hide()
        self.SLAMButton.hide()

        # Call the functions to reset the values, obstacles and animation
        self.ResetValues()
        self.ResetObstacles()
        self.ResetRobotAnimation()

####################################################################################
#ROBOT OPTIONS#
####################################################################################

    def GoToRobCommandsWindow(self):

        self.RobCommandsButton.hide()
        self.RobWikiButton.hide()

        self.SendRouteButton.show()
        self.SLAMButton.show()

    def SendRouteWindow(self):

        SRW = SendRouteWindow(self)
        SRW.show()

    def SocketSend(self, MessageToSend):

        self.message = MessageToSend
        self.len_message = str(len(MessageToSend))
        cnt = 0
        self.number_zeros = 10-len(self.len_message)

        if len(self.len_message) < 10:
            while cnt < self.number_zeros:
                self.len_message = '0'+self.len_message
                cnt = cnt+1

        self.message = self.len_message+self.message
        print(self.message[10:])
        self.message = self.message.encode('ascii')

        # Send the message
        self.sock.sendall(self.message)

        self.amount_received = -1

        # While the amount expected stays at -1, keep listening to receive a message from the server to prove that the server received the credentials correctly
        while self.amount_received == -1:
            self.len_message_received_ascii = self.sock.recv(10)
            self.len_message_received = int(self.len_message_received_ascii.decode(
                'ascii'))
            c = 0
            len_rcv = 5
            self.message_completed = ''

            while c <= (int(self.len_message_received/len_rcv)):
                self.message_received_ascii = self.sock.recv(len_rcv)
                self.message_received = self.message_received_ascii.decode(
                    'ascii')
                self.message_completed = self.message_completed+self.message_received
                c = c+1

            print(self.message_completed)
            self.amount_received = len(self.message_completed)

    def SocketSendROS(self, MessageToSend):

        self.message = MessageToSend
        self.len_message = str(len(MessageToSend))
        cnt = 0
        self.number_zeros = 10-len(self.len_message)

        if len(self.len_message) < 10:
            while cnt < self.number_zeros:
                self.len_message = '0'+self.len_message
                cnt = cnt+1

        self.message = self.len_message+self.message
        print(self.message[10:])
        self.message = self.message.encode('ascii')

        # Send the message
        self.sockR.sendall(self.message)

        self.amount_received = -1

        # While the amount expected stays at -1, keep listening to receive a message from the server to prove that the server received the credentials correctly
        while self.amount_received == -1:
            self.len_message_received_ascii = self.sockR.recv(10)
            self.len_message_received = int(self.len_message_received_ascii.decode(
                'ascii'))
            c = 0
            len_rcv = 5
            self.message_completed = ''

            # Mensaje recivido mi pana
            while c <= (int(self.len_message_received/len_rcv)):
                self.message_received_ascii = self.sockR.recv(len_rcv)
                self.message_received = self.message_received_ascii.decode(
                    'ascii')
                self.message_completed = self.message_completed+self.message_received
                c = c+1

            print(self.message_completed)
            self.amount_received = len(self.message_completed)

        # if 'Initialize_SLAM' in MessageToSend:
        #     self.ReceiveSLAMImage()

    def ReceiveSLAMImage(self):
        self.image_Slam += self.sockR.recv(1024)
        while not self.image_Slam:
            self.image_Slam += self.sockR.recv(1024)

        len_data = int(self.image_Slam[:10].decode(ascii))
        self.image_Slam = self.image_Slam[10:]
        while len(self.image_Slam) < len_data:
            self.image_Slam += self.sockR.recv(1024)
        frame = self.image_Slam[:len_data]
        self.image_Slam = self.image_Slam[len_data:]

        img = QImage.fromData(frame)
        pix_img = QPixmap(img)
        return pix_img

        # self.file1 = open('Received_Image.jpg', "wb")
        # self.chunk = 1024
        # self.image_len = self.sockR.recv(10)
        # self.image_len = int(self.image_len.decode('utf-8'))
        # self.data_complete = bytes('', 'utf-8')

        # while len(self.data_complete) < self.image_len:
        #     self.image_chunk = self.sockR.recv(self.chunk)
        #     self.data_complete = self.data_complete+self.image_chunk

        # self.data_complete = self.data_complete[:self.image_len]

        # self.file1.write(self.data_complete)

        # print('Image received')

        # self.file1.close()
        # CropImage()

    def OpenWiki(self):

        webbrowser.open('https://github.com/ROSNI-educational-robot')

    def OpenSLAMWindow(self):

        SLAMW = SLAMWindow(self)
        SLAMW.show()


####################################################################################
#ROBOT CONNECTIONS#
####################################################################################

    # Create a function to show the IP window

    def GoToIPWindow(self):

        IPW = IPWindow(self)
        IPW.show()

    # Create a function to show the WiFi window
    def GoToWiFiWindow(self):

        WFW = WiFiWindow(self)
        WFW.show()

    # Create a function to show the config window
    def GoToConfigWindow(self):

        CW = ConfigWindow()
        CW.show()

    # Create a function to create a socket client
    def SocketClient(self, IP, port):

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = (IP, port)
        print('Connecting to {} port {}'.format(*server_address))
        self.sock.connect(server_address)
        print('Connected')

        print('###########################################')

    # Create a function to create a socket client for ROS
    def SocketClientROS(self, IP, portROS):

        # Create a TCP/IP socket
        self.sockR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = (IP, portROS)
        print('Connecting to {} port {}'.format(*server_address))
        self.sockR.connect(server_address)
        print('Connected')

        print('###########################################')

    # Create a function to end the client connection
    def SockDisconnect(self):

        self.SocketSend('Disconnect_Client')
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.sockR.shutdown(socket.SHUT_RDWR)
        self.sockR.close()
        self.check_connection = 0
        self.InformationDisconnected()

    # Create an information message function
    def InformationDisconnected(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Client Disconnected from the server")
        self.msg.setWindowTitle("Information Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()


####################################################################################
#VIRTUAL ROUTES#
####################################################################################

    # Create a warning message function

    def WarningCoordinates(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! Coordinates out of range")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    # Create a function to show the open window
    def GoToOpenWindow(self):

        # Call the functions to reset the values, obstacles and animation
        self.ResetRobotAnimation()
        self.ResetValues()
        self.ResetObstacles()

        OW = OpenWindow(self.lpx, self.lpy, self.lpx_def, self.lpy_def, self.lpx_def_units, self.lpy_def_units,
                        self.loxi, self.loyi, self.loxf, self.loyf, self.c, self.lpa, self.lc, self.units, self.lu)
        OW.show()

        # If the obstacles list is empty call the function to reset obstacles
        if len(self.loxi) == 0:
            self.ResetObstacles()

        # If the coordinates list is empty call the function to reset coordinates
        if len(self.lpx) == 0:
            self.ResetValues()

        self.flag = True
        self.flag_obstacle = True
        self.update()

        # Recuperate the variable c from the lc list
        if len(self.lc) > 1:
            self.c = int(self.lc[1])
        else:
            self.c = int(self.lc[0])

        # Move the Robot widget
        if len(self.lpx) > 0:
            self.R.move(self.lpx[0]-self.robotRad, self.lpy[0]-self.robotRad)

        # Recuperate the variable units from the lu list
        if len(self.lu) > 1:
            self.units = float(self.lu[1])
        else:
            self.units = float(self.lu[0])

        # Save and place the item variable depending on the units in the combo box
        if self.units == 1:
            item = 'm'
        elif self.units == 0.1:
            item = 'dm'
        elif self.units == 0.01:
            item = 'cm'
        else:
            item = 'mm'

        self.cb.setCurrentText(item)

        # Compute the initial angle
        if len(self.lpx_def) >= 2:

            self.xa = self.lpx_def[1]-self.lpx_def[0]
            self.ya = self.lpy_def[1]-self.lpy_def[0]

            self.initialAngle = InitialAngle(self.xa, self.ya)

    # Create a function to show the save window
    def GoToSaveWindow(self):

        SW = SaveWindow(self.lpx, self.lpy, self.lpx_def, self.lpy_def, self.lpx_def_units,
                        self.lpy_def_units, self.loxi, self.loyi, self.loxf, self.loyf, self.c, self.lpa, self.units)
        SW.show()

    # Create a function to show the help script
    def GoToHelpWindow(self):

        # Save the path of the scripts to the variable path
        path = os.path.abspath(os.getcwd())

        # Save the path of the Help script to the variable pathHelp
        pathHelp = path.replace("\Scripts", "\Help.txt")

        # Open the Help.txt file
        os.startfile(pathHelp)

    # Create a function to compute the units depending on the combo box value
    def Units(self):

        self.unitsText = self.cb.currentText()

        c1 = 0

        if self.unitsText == 'm':
            self.units = 1
        elif self.unitsText == 'dm':
            self.units = 0.1
        elif self.unitsText == 'cm':
            self.units = 0.01
        elif self.unitsText == 'mm':
            self.units = 0.001

        # Compute the coordinates value according to the units
        if len(self.lpx) > 0:
            for c1 in range(1, len(self.lpx_def)):
                self.lpx_def_units[c1] = self.lpx_def[c1]*self.units
                self.lpy_def_units[c1] = self.lpy_def[c1]*self.units
                c1 = c1+1

    # Create a function to set a variable to True or false depending on the check box, if it is checked True
    def ShowNumbers(self, state):

        if state == Qt.Checked:
            self.SNvariable = True
        else:
            self.SNvariable = False

    # Create a function to set the first position of the Robot
    def GetRobxy(self):

        # Get the Robx and Roby Line Edit text
        self.robx = self.RobxLineEdit.text()
        self.roby = self.RobyLineEdit.text()

        # If the text is empty interpret it as 0
        if self.robx == '':
            self.robx = 0

        if self.roby == '':
            self.roby = 0

        # Convert the text from str to int
        self.robx = int(self.robx)
        self.roby = int(self.roby)

        # If the lenght of the coordinates list is 0 and it's in the range of the map append it to the list, and if it's not in range, mantain the list with the first coordinates established
        if len(self.lpx) == 0 and len(self.lpy) == 0:

            if robotx <= (self.robx+robotx) <= self.LimitZonex+200 and roboty <= (self.roby+roboty) <= self.LimitZoney+20:
                self.lpx.append(self.robx+robotx)
                self.lpy.append(self.roby+roboty)
            else:
                self.lpx = [robotx]
                self.lpy = [roboty]

                self.WarningCoordinates()

        # If the lenght of the coordinates list isn't 0...
        else:
            # If CoordType=1 (incremental coordinates) save lpx[0] in cx and save lpy[0] in cy
            if self.CoordType == 1:
                self.cx = self.lpx[0]
                self.cy = self.lpy[0]
            # If CoordType=0 (absolute coordinates) save robotx in cx and save roboty in cy
            else:
                self.cx = robotx
                self.cy = roboty

            # Compute robx
            if self.robx == 0:
                self.robx = self.cx
            else:
                self.robx = int(self.robx)+int(self.cx)

            # Compute roby
            if self.roby == 0:
                self.roby = self.cy
            else:
                self.roby = int(self.roby)+int(self.cy)

            # If robx and roby are in the range of the map append the coordinates to the list coordinates and move the Robot to each coordinates
            if robotx <= (self.robx) <= self.LimitZonex+200 and roboty <= (self.roby) <= self.LimitZoney+20:
                self.lpx[0] = self.robx
                self.lpy[0] = self.roby
                self.lpx_def[0] = self.robx-robotx
                self.lpy_def[0] = self.roby-roboty
                self.R.move(self.lpx[0]-self.robotRad,
                            self.lpy[0]-self.robotRad)

            # Else show the warning window
            else:
                self.WarningCoordinates()

            # If the lenght of the coordinates list is higher than 2 compute the initial angle
            if len(self.lpx_def) >= 2:

                self.xa = self.lpx_def[1]-self.lpx_def[0]
                self.ya = self.lpy_def[1]-self.lpy_def[0]

                self.initialAngle = InitialAngle(self.xa, self.ya)

        self.flag_reset = True
        self.update()

    # Create a function to set the next positions of the Robot
    def Getxy(self):

        # If the Robot's initial position hasn't been setted, set it to robotx and roboty
        if len(self.lpx) == 0 and len(self.lpy) == 0:
            self.lpx.append(robotx)
            self.lpy.append(roboty)

        # Initialize counter and save the px and py line edit text to x and y variables respectively
        self.c = self.c+1
        self.x = self.PxLineEdit.text()
        self.y = self.PyLineEdit.text()

        # If the text is empty interpret it as 0
        if self.x == '':
            self.x = 0

        if self.y == '':
            self.y = 0

        # Convert the text from str to int
        self.x = int(self.x)
        self.y = int(self.y)

        # If CoordType=1 (incremental coordinates) save lpx[0] in cx and save lpy[0] in cy
        if self.CoordType == 1:
            self.cx = self.lpx[self.c-1]
            self.cy = self.lpy[self.c-1]

        # If CoordType=0 (absolute coordinates) save robotx in cx and save roboty in cy
        else:
            self.cx = robotx
            self.cy = roboty

        # Compute the x position
        if self.x == 0:
            self.xm = self.cx
        else:
            self.xm = self.x+self.cx

        # Compute the y position
        if self.y == 0:
            self.ym = self.cy
        else:
            self.ym = self.y+self.cy

        # If x and y positions are in the range of the map append the coordinates to the list coordinates
        if robotx <= self.xm <= self.LimitZonex+225 and roboty <= self.ym <= self.LimitZoney+20:

            if self.x == 0:
                self.lpx.append(self.xm)
                self.lpx_def.append(self.xm-self.lpx[0])
                self.lpx_def_units.append((self.xm-self.lpx[0])*self.units)
            else:
                self.lpx.append(self.xm)
                self.lpx_def.append(self.xm-self.lpx[0])
                self.lpx_def_units.append((self.xm-self.lpx[0])*self.units)

            if self.y == 0:
                self.lpy.append(self.ym)
                self.lpy_def.append(self.ym-self.lpy[0])
                self.lpy_def_units.append((self.ym-self.lpy[0])*self.units)
            else:
                self.lpy.append(self.ym)
                self.lpy_def.append(self.ym-self.lpy[0])
                self.lpy_def_units.append((self.ym-self.lpy[0])*self.units)

            if len(self.lpx_def) == 2:

                self.xa = self.lpx_def[1]-self.lpx_def[0]
                self.ya = self.lpy_def[1]-self.lpy_def[0]

                self.initialAngle = InitialAngle(self.xa, self.ya)

        # If the x and y positions aren't in the range of the map rest 1 to the counter and don't append the coordinates to each respectively list
        else:
            self.WarningCoordinates()
            self.c = self.c-1

        self.flag = True
        self.update()

    # Create a function to sget the rotation angle that the robot must do to follow the route
    def GetAngle(self):

        # If the lenght of the coordinates list is larger than 2 proceed
        if len(self.lpx) > 2:

            # Compute the variables that must be used to compute the angle
            self.x1 = self.lpx_def[self.c-2]
            self.y1 = self.lpy_def[self.c-2]
            self.x2 = self.lpx_def[self.c]
            self.y2 = self.lpy_def[self.c]
            self.xi = self.lpx_def[self.c-1]
            self.yi = self.lpy_def[self.c-1]

            self.dx1 = self.x1-self.xi
            self.dy1 = self.y1-self.yi
            self.dx2 = self.x2-self.xi
            self.dy2 = self.y2-self.yi

            # Compute the angle depending on the variables setted previously and converting it from radiants to degrees
            self.angle = RadToDeg(VectorsAngle(
                self.dx1, self.dy1, self.dx2, self.dy2, self.xi, self.yi))

            # Setting the direction of rotation of the angle depending on the result of the angle previously computed
            if self.angle == 180 or self.angle == -180:
                self.angle = 0
            elif self.angle > 0:
                self.angle = 180-self.angle
            elif self.angle < 0:
                self.angle = (self.angle+180)*(-1)
            else:
                self.angle = 180

            # Append the angle to the rotation angle list
            self.lpa.append(self.angle)

    # Create a function to reset the values of the position coordinates
    def ResetValues(self):

        if len(self.lpx) != 0 and len(self.lpy) != 0:

            # Clear the coordinates lists
            self.lpx.clear()
            self.lpy.clear()
            self.lpx_def.clear()
            self.lpy_def.clear()
            self.lpx_def_units.clear()
            self.lpy_def_units.clear()

            self.lpx_def = [0]
            self.lpy_def = [0]
            self.lpx_def_units = [0]
            self.lpy_def_units = [0]

            # Set the counter to 0
            self.c = 0

            # Move the Robot to its initial position
            self.R.move(robotx-self.robotRad, roboty-self.robotRad)

            self.flag_reset = True
            self.update()

        if len(self.lpa) != 0:

            # Clear the rotation angle list
            self.lpa.clear()

            self.lpa = [0]

        self.lc = [0]
        self.lu = [1]

        self.units = 1

        self.initialAngle = 0

    # Create a function to paint the coordinates and more in the map
    def paintEvent(self, event):

        p = QPainter(self)

        # If the falgCoordRef is setted to True...
        if self.flagCoordRef:

            # Initialize the QPainter
            p.begin(self)

            # Call the function drawCoordRef
            self.drawCoordRef(p, robotx-5, roboty-55, '0')
            self.drawCoordRef(p, robotx-70, roboty+5, '0')
            self.drawCoordRef(p, self.LimitZonex+robotx-120,
                              roboty-55, str(self.LimitZonex-100))
            self.drawCoordRef(p, robotx-90, self.LimitZoney +
                              25, str(self.LimitZoney-100-5))
            self.drawCoordRef(p, int((self.LimitZonex+robotx-30)/2),
                              roboty-55, str(int((self.LimitZonex-robotx)/2)))
            self.drawCoordRef(p, robotx-90, int((self.LimitZoney +
                              roboty+10)/2), str(int((self.LimitZoney-roboty)/2)))
            # End the QPainter
            p.end()

        # If the falg, the falg_robot_change and the flag_obstacle are setted to True...
        if self.flag or self.flag_robot_change or self.flag_obstacle:

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

                    # If the SNvariable has been setted to True...
                    if self.SNvariable:
                        str_cnt = str(self.cnt)

                        # Call the function drawText to draw the number of the coordinate on its positon
                        self.drawText(
                            p, self.lpx[self.cnt]+10, self.lpy[self.cnt]-10, str_cnt)

                 # If the SNvariable has been setted to True...
                if self.SNvariable:
                    str_cnt = str(self.cnt)
                    # Call the function drawText to draw the number of the first coordinate on its position
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

                    # If the SNvariable has been setted to True...
                    if self.SNvariable:
                        str_cnt = str(self.cnt)
                        # Call the function drawText to draw the number of the obstacle on its position if the counter is larger than 0
                        if int(str_cnt) > 0:
                            self.drawText(
                                p, self.loxi[self.cnt]+10, self.loyi[self.cnt]+25, str_cnt)

            # End the QPainter
            p.end()

        self.flag_robot_change = False
        self.update()

    # Create a function erase the drawings
    def paintEventReset(self, event):

        # If the flag_reset has been setted to True just draw the first coordinate
        if self.flag_reset:
            p = QPainter(self)
            p.begin(self)
            self.drawPoint(p, self.lpx[0]-500, self.lpy[0]-500)
            p.end()

        self.flag_robot_change = True
        self.update()

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

    # Create a function to show the Edit Coordinates Window
    def GoToEditCoordinatesWindow(self):

        ECW = EditCoordinatesWindow(self.lpx, self.lpy, self.lpx_def, self.lpy_def, self.lpx_def_units,
                                    self.lpy_def_units, self.lpa, self.CoordType, self.LimitZonex, self.LimitZoney, self.units)
        ECW.show()

    # Create a function to set the speed of the simulation
    def SimulationSpeed1(self):

        self.simSpeed = 1

        # Enable the speed x1 button and disable the others
        self.x1Button.setEnabled(False)
        self.x10Button.setEnabled(True)
        self.x100Button.setEnabled(True)

        self.x1Button.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,100); border-radius:5px}")
        self.x10Button.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.x100Button.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

    # Create a function to set the speed of the simulation
    def SimulationSpeed10(self):

        self.simSpeed = 10

        # Enable the speed x10 button and disable the others
        self.x1Button.setEnabled(True)
        self.x10Button.setEnabled(False)
        self.x100Button.setEnabled(True)

        self.x10Button.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,100); border-radius:5px}")
        self.x1Button.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.x100Button.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

    # Create a function to set the speed of the simulation
    def SimulationSpeed100(self):

        self.simSpeed = 100

        # Enable the speed x10 button and disable the others
        self.x1Button.setEnabled(True)
        self.x10Button.setEnabled(True)
        self.x100Button.setEnabled(False)

        self.x100Button.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,100); border-radius:5px}")
        self.x10Button.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.x1Button.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

    # Create a function to simulate the route that the Robot must follow
    def RobotAnimation(self):

        # Initialize a counter
        self.n = 0

        self.anim_group = QSequentialAnimationGroup()

        # For the counter in range of 0 to the number of coordinates...
        for self.n in range(0, self.c, 1):

            # Set the animation as anim and configurate it to be done by the Robot widget and type position
            self.anim = QPropertyAnimation(self.R, b"pos")

            # Set the start value of the animation (n)
            self.anim.setStartValue(
                QPoint(self.lpx[self.n]-self.robotRad, self.lpy[self.n]-self.robotRad))

            # Set the end value of the animation (n+1)
            self.anim.setEndValue(
                QPoint(self.lpx[self.n+1]-self.robotRad, self.lpy[self.n+1]-self.robotRad))

            # Compute the duration of the animation depending on the distance that the robot has to move
            duration = ((((((self.lpx[self.n+1]-self.lpx[self.n])**2)+(
                (self.lpy[self.n+1]-self.lpy[self.n])**2))**(1/2))*500)/self.simSpeed)*self.units

            # Set the duration of the move
            self.anim.setDuration(int(duration))

            # Add the animation to the ani ation group
            self.anim_group.addAnimation(self.anim)

            # Set another animation as anim and configurate it to be done by the Robot widget and type position
            self.animS = QPropertyAnimation(self.R, b"pos")

            # Set the start value and the end value in the same position to make the robot stop when it ends the move
            self.animS.setStartValue(
                QPoint(self.lpx[self.n+1]-self.robotRad, self.lpy[self.n+1]-self.robotRad))
            self.animS.setEndValue(
                QPoint(self.lpx[self.n+1]-self.robotRad, self.lpy[self.n+1]-self.robotRad))

            # Compute the angle that the robot has to rotate and compute the duration depending on the angle that it has to rotate
            if self.n < self.c-1:

                self.ang_rot = self.lpa[self.n+1]

                duration = (self.ang_rot*1500/self.simSpeed)*self.units

                if duration < 0:
                    duration = duration*(-1)
                else:
                    duration = duration

                # Set the duration of the animation and add it to the animation group
                self.animS.setDuration(int(duration))
                self.anim_group.addAnimation(self.animS)

        # Start the animation
        self.anim_group.start()

    # Create a class to reset the robot animation
    def ResetRobotAnimation(self):

        # If the list of coordinates is not empty...
        if len(self.lpx) != 0:

            # Set the animation as anim and configurate it to be done by the Robot widget and type position
            self.anim = QPropertyAnimation(self.R, b"pos")

            # Set the end value as the first position of the robot
            self.anim.setEndValue(
                QPoint(self.lpx[0]-self.robotRad, self.lpy[0]-self.robotRad))

            # Set the duration as 0
            duration = 0
            self.anim.setDuration(int(duration))

            # Start the animation
            self.anim.start()

    # Create a function to show the Input Obstacle Window
    def GoToInputObstacle(self):

        IOW = InputObstacleWindow(self.loxi, self.loyi, self.loxf,
                                  self.loyf, self.LimitZonex, self.LimitZoney, self.cnt1)
        IOW.show()
        self.flag_obstacle = True
        self.update()

    # Create a function to show the Edit Obstacle Window
    def GoToEditObstacle(self):

        EOW = EditObstacleWindow(self.lpx, self.lpy, self.loxi, self.loyi,
                                 self.loxf, self.loyf, self.CoordType, self.LimitZonex, self.LimitZoney)
        EOW.show()

    # Create a function to reset the obstacles
    def ResetObstacles(self):

        # If the obstacles lists aren't empty clear them
        if len(self.loxi) != 0 and len(self.loyi) != 0:

            self.loxi.clear()
            self.loyi.clear()
            self.loxf.clear()
            self.loyf.clear()

            self.loxi = [0]
            self.loyi = [0]
            self.loxf = [0]
            self.loyf = [0]

        else:

            self.loxi = [0]
            self.loyi = [0]
            self.loxf = [0]
            self.loyf = [0]

    # Create a function to set the type of coordinates as absolute coordinates
    def AbsCoord(self):

        # Save the coordinates type variable as 0
        self.CoordType = 0
        self.AbsCoordButton.setEnabled(False)
        self.IncCoordButton.setEnabled(True)
        self.AbsCoordButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,100); border-radius:5px}")
        self.IncCoordButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

    # Create a function to set the type of coordinates as incremental coordinates
    def IncCoord(self):

        # Save the coordinates type variable as 0
        self.CoordType = 1
        self.IncCoordButton.setEnabled(False)
        self.AbsCoordButton.setEnabled(True)
        self.IncCoordButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,100); border-radius:5px}")
        self.AbsCoordButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")


# Execute the program and show the main window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())
