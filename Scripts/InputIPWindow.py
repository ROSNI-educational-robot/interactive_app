# Import the necessary libraries
from math import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class IPWindow(QDialog):

    # Here we declare a variable in the init called mare which allows us comunicate with the main window
    def __init__(self, mare):

        super().__init__()
        self.mare = mare
        self.setFixedSize(300, 170)
        self.setStyleSheet(
            "background-color: qlineargradient(x1: 0, x2: 1, stop: 0 #202020, stop: 1 #50005E)")

        self.MainWidgets()
        self.ConnectToWiFi()

        self.IPLineEdit.hide()
        self.IPLabel.hide()
        self.HotSpotButton.hide()
        self.ConnectButtonW.hide()
        self.TextLabel.show()
        self.WiFiButton.show()
        self.ConnectButton.show()

        self.setWindowTitle('Hotspot')

    # Create a function to create the main widgets of the window
    def MainWidgets(self):

        # Open the txt file Configuration.txt to read it and assign it to the variable cfr to read it
        self.cfr = open("Configuration.txt", "r")

        # Read the lines of the document and assign them to their respective variables
        self.IP = self.cfr.readline()
        self.SSID = self.cfr.readline()
        self.PORT = self.cfr.readline()
        self.ROSPORT = self.cfr.readline()

        # Close the document
        self.cfr.close()

        self.TextLabel = QLabel(
            "IP: "+str(self.IP)+"\nSSID: "+str(self.SSID)+"\n"+"Port: "+str(self.PORT)+"\n"+"ROS Port: "+str(self.ROSPORT), self)
        self.TextLabel.move(10, 10)
        self.TextLabel.resize(100, 100)
        self.TextLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.TextLabel.show()

        self.WiFiButton = QPushButton(self)
        self.WiFiButton.setText("WiFi")
        self.WiFiButton.move(200, 10)
        self.WiFiButton.resize(90, 35)
        self.WiFiButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.WiFiButton.show()

        self.ConnectButton = QPushButton(self)
        self.ConnectButton.setText("Connect")
        self.ConnectButton.move(200, 125)
        self.ConnectButton.resize(90, 35)
        self.ConnectButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.ConnectButton.show()

        self.CloseButton = QPushButton(self)
        self.CloseButton.setText("Disconnect")
        self.CloseButton.move(100, 125)
        self.CloseButton.resize(90, 35)
        self.CloseButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

        # If the button is clicked, go to the function
        self.WiFiButton.clicked.connect(lambda: self.ConnectToWiFi())
        self.ConnectButton.clicked.connect(lambda: self.ConnectToIp())
        self.CloseButton.clicked.connect(lambda: self.EndConnection())

    def ConnectToWiFi(self):

        # Change the window title
        self.setWindowTitle('WiFi')

        self.TextLabel.hide()
        self.WiFiButton.hide()
        self.ConnectButton.hide()

        self.IPLineEdit = QLineEdit(self)
        self.IPLineEdit.move(50, 10)
        self.IPLineEdit.resize(120, 35)
        self.IPLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.IPLineEdit.show()

        self.IPLabel = QLabel('IP', self)
        self.IPLabel.move(10, 10)
        self.IPLabel.resize(40, 30)
        self.IPLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.IPLabel.show()

        self.HotSpotButton = QPushButton(self)
        self.HotSpotButton.setText("HotSpot")
        self.HotSpotButton.move(200, 10)
        self.HotSpotButton.resize(90, 35)
        self.HotSpotButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.HotSpotButton.show()

        self.ConnectButtonW = QPushButton(self)
        self.ConnectButtonW.setText("Connect")
        self.ConnectButtonW.move(200, 125)
        self.ConnectButtonW.resize(90, 35)
        self.ConnectButtonW.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")
        self.ConnectButtonW.show()

        # If the button is clicked, go to the function
        self.HotSpotButton.clicked.connect(lambda: self.HotSpotWidgets())
        self.ConnectButtonW.clicked.connect(lambda: self.ConnectToIPW())

    def HotSpotWidgets(self):

        # Change the window title
        self.setWindowTitle('Hotspot')

        # Show the widgets of the HotSpot and hide the ones of the WiFi
        self.TextLabel.show()
        self.WiFiButton.show()
        self.ConnectButton.show()
        self.IPLineEdit.hide()
        self.IPLabel.hide()
        self.HotSpotButton.hide()
        self.ConnectButtonW.hide()

    # Create a function to connect to the IP
    def ConnectToIp(self):

        # Supress the space (\n) of the IP text
        self.IP = self.IP.replace('\n', '')

        self.port = self.mare.port
        self.portROS = self.mare.portROS

        # Count the number of points that the IP text contain
        self.npoints = self.IP.count(".")

        # Try to compute
        try:

            # If the number of points are not 3 show a warning window
            if self.npoints != 3:
                self.WarningIP()

            # Else connect with the server via socket using function SocketClient() from the main window
            else:

                if self.mare.check_connection == 0:

                    self.mare.SocketClientROS(self.IP, self.portROS)
                    #
                    # self.mare.SocketClient(self.IP, self.port)

                    self.mare.check_connection = 1

                    self.InformationConnected()

                else:
                    self.InformationConnected()
                    pass

        # If the program can't be computed show a warning window
        except:
            self.WarningConnection()

    def ConnectToIPW(self):

        # Take and save the text of the IP line edit in a variable
        self.IPWiFi = self.IPLineEdit.text()

        self.port = self.mare.port
        self.portROS = self.mare.portROS

        # Count the number of points that the IP text contain
        self.npoints = self.IPWiFi.count(".")

        # Try to compute
        try:

            # If the number of points are not 3 show a warning window
            if self.npoints != 3:
                self.WarningIP()

            # Else connect with the server via socket using function SocketClient() from the main window
            else:
                if self.mare.check_connection == 0:

                    #self.mare.SocketClient(self.IPWiFi, self.port)
                    self.mare.SocketClientROS(self.IPWiFi, self.portROS)

                    self.mare.check_connection = 1

                    self.InformationConnected()

                else:
                    self.InformationConnected()
                    pass

        # If the program can't be computed show a warning window
        except:
            self.WarningConnection()

    def EndConnection(self):

        try:
            self.mare.SockDisconnect()
        except:
            self.WarningDisonnection()

    def WarningIP(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! Incorrect IP format")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    # Create a warning window for connection errors
    def WarningConnection(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! Unable to connect with the server")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    def WarningDisonnection(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! You are not connected with any server")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    def InformationConnected(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Connected to the server")
        self.msg.setWindowTitle("Information Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()
