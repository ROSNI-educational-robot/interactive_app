# Import the necessary libraries
from math import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class ConfigWindow(QDialog):

    def __init__(self):

        super().__init__()
        self.setFixedSize(260, 230)
        self.setWindowTitle('Configuration')
        self.setStyleSheet(
            "background-color: qlineargradient(x1: 0, x2: 1, stop: 0 #202020, stop: 1 #50005E)")
        self.MainWidgets()

    # Create a function to create the main widgets of the window
    def MainWidgets(self):

        # Open the txt file Configuration.txt to read it and assign it to the variable cfr
        self.cfr = open("Configuration.txt", "r")

        # Read the lines of the document and assign them to their respective variables
        self.RIP = self.cfr.readline()
        self.RSSID = self.cfr.readline()
        self.PORT = self.cfr.readline()
        self.ROSPORT = self.cfr.readline()

        # Close the document
        self.cfr.close()

        self.RIPLineEdit = QLineEdit(self)
        self.RIPLineEdit.move(85, 10)
        self.RIPLineEdit.resize(160, 35)
        self.RIPLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.RIPLineEdit.setText(self.RIP)

        self.RSSIDLineEdit = QLineEdit(self)
        self.RSSIDLineEdit.move(85, 50)
        self.RSSIDLineEdit.resize(160, 35)
        self.RSSIDLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.RSSIDLineEdit.setText(self.RSSID)

        self.PORTLineEdit = QLineEdit(self)
        self.PORTLineEdit.move(85, 90)
        self.PORTLineEdit.resize(160, 35)
        self.PORTLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.PORTLineEdit.setText(self.PORT)

        self.ROSPORTLineEdit = QLineEdit(self)
        self.ROSPORTLineEdit.move(85, 130)
        self.ROSPORTLineEdit.resize(160, 35)
        self.ROSPORTLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")
        self.ROSPORTLineEdit.setText(self.ROSPORT)

        self.RIPLabel = QLabel('Robot IP', self)
        self.RIPLabel.move(10, 10)
        self.RIPLabel.resize(70, 30)
        self.RIPLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.RSSIDLabel = QLabel('Robot SSID', self)
        self.RSSIDLabel.move(10, 50)
        self.RSSIDLabel.resize(70, 30)
        self.RSSIDLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.PORTLabel = QLabel('Port', self)
        self.PORTLabel.move(10, 90)
        self.PORTLabel.resize(70, 30)
        self.PORTLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.ROSPORTLabel = QLabel('ROS Port', self)
        self.ROSPORTLabel.move(10, 130)
        self.ROSPORTLabel.resize(70, 30)
        self.ROSPORTLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.SaveButton = QPushButton(self)
        self.SaveButton.setText("Save")
        self.SaveButton.move(85, 170)
        self.SaveButton.resize(160, 35)
        self.SaveButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

        # If the button is clicked connect to the function SaveChanges()
        self.SaveButton.clicked.connect(lambda: self.SaveChanges())

    # Create a function to save the changes of the three line edit in a txt file
    def SaveChanges(self):

        # Read the lines of the document and assign them to their respective variables
        self.WRIP = self.RIPLineEdit.text()
        self.WRSSID = self.RSSIDLineEdit.text()
        self.WPORT = self.PORTLineEdit.text()
        self.WROSPORT = self.ROSPORTLineEdit.text()

        # Open the txt file Configuration.txt and assign it to the variable cfr to write on it
        self.cfw = open("Configuration.txt", "w")

        if '\n' in self.WRIP:
            self.WRIP = self.WRIP.replace('\n', '')
        if '\n' in self.WRSSID:
            self.WRSSID = self.WRSSID.replace('\n', '')
        if '\n' in self.WPORT:
            self.WPORT = self.WPORT.replace('\n', '')
        if '\n' in self.WROSPORT:
            self.WROSPORT = self.WROSPORT.replace('\n', '')

        self.cfw.write(str(self.WRIP)+'\n')
        self.cfw.write(str(self.WRSSID)+'\n')
        self.cfw.write(str(self.WPORT)+'\n')
        self.cfw.write(str(self.WROSPORT)+'\n')

        # Close the txt file
        self.cfw.close()
