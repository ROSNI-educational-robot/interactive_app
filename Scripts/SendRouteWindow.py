# Import the necessary libraries
from math import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
import linecache

# Import the other python scripts
from ShowMapWindow import *

Directory = os.getcwd()
RoutesDirectory = Directory.replace('\Scripts', '\Routes')

routes_obj = os.scandir(RoutesDirectory)
routes_list = []

for route in routes_obj:
    if route.is_file():
        route_name = str(route.name)
        routes_list.append(route_name)
routes_obj.close()


class SendRouteWindow(QDialog):

    # Here we declare a variable in the init called mare which allows us comunicate with the main window
    def __init__(self, mare):

        super().__init__()
        self.mare = mare
        self.setFixedSize(225, 135)
        self.setWindowTitle('Send Route')
        self.setStyleSheet(
            "background-color: qlineargradient(x1: 0, x2: 1, stop: 0 #202020, stop: 1 #50005E)")
        self.MainWidgets()

    # Create a function to create the main widgets of the window
    def MainWidgets(self):

        self.cb = QComboBox(self)
        self.cb.move(50, 10)
        self.cb.resize(160, 35)
        self.index = 0
        for self.index in range(0, len(routes_list)):
            self.cb.addItems([routes_list[self.index]])
        self.cb.setStyleSheet(
            "selection-background-color: rgb(255,255,255,100); background-color: rgb(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.RouteLabel = QLabel('Route', self)
        self.RouteLabel.move(10, 10)
        self.RouteLabel.resize(40, 30)
        self.RouteLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.SendButton = QPushButton(self)
        self.SendButton.setText("Send")
        self.SendButton.move(50, 50)
        self.SendButton.resize(160, 35)
        self.SendButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

        self.SendingLabel = QLabel('', self)
        self.SendingLabel.move(50, 90)
        self.SendingLabel.resize(130, 30)
        self.SendingLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        # If the button is clicked connect it to the function SendRoute()
        self.SendButton.clicked.connect(lambda: self.SendRoute())
        self.SendButton.clicked.connect(lambda: self.GoToShowMapWindow())

    # Create a function to connect to the IP

    def SendRoute(self):

        # Save the text in the variable RouteName
        self.RouteName = self.cb.currentText()

        print(self.RouteName)

        # If the file doesn't name contain .csv add it
        if '.csv' in self.RouteName:
            self.RouteName = self.RouteName
        else:
            self.RouteName = self.RouteName+'.csv'

        # Try to open the file, read it and compute the pararameters
        try:
            self.routefile = open(RoutesDirectory+"\\"+self.RouteName, 'r')

            self.RouteX = linecache.getline(
                RoutesDirectory+"\\"+self.RouteName, 5)
            self.RouteY = linecache.getline(
                RoutesDirectory+"\\"+self.RouteName, 6)
            self.RouteCounter = linecache.getline(
                RoutesDirectory+"\\"+self.RouteName, 11)
            self.RouteAngles = linecache.getline(
                RoutesDirectory+"\\"+self.RouteName, 12)

            self.RouteX = self.RouteX.replace('\n', '')
            self.RouteX = 'X:'+self.RouteX
            self.RouteY = self.RouteY.replace('\n', '')
            self.RouteY = 'Y:'+self.RouteY
            self.RouteCounter = self.RouteCounter.replace('\n', '')
            self.RouteAngles = self.RouteAngles.replace('\n', '')

        # If the name of the file doesn't exist, sow a warning message
        except:
            self.WarningRoute()

        # Try to compute
        try:

            self.Route = self.RouteX+'* *'+self.RouteY
            self.mare.SocketSendROS(self.Route)

            # Show the message 'Sended' on the window
            self.SendingLabel.setText('Sended')

        # If the program can't be computed show a warning window
        except:
            self.SendingLabel.setText('')
            self.WarningConnection()

    def GoToShowMapWindow(self):

        SMW = ShowMapWindow(self, self.RouteName)
        SMW.show()

    # Create a warning window for connection errors
    def WarningConnection(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! Unable to connect with the server")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    # Create a warning window for file name error
    def WarningRoute(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! Unable to find the specified route")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    def SocketSendBridge(self):

        # Try to compute
        try:
            self.StopMessage = 'Stop_Route'
            self.mare.SocketSendROS(self.StopMessage)

        # If the program can't be computed show a warning window
        except:
            self.WarningConnection()
