# Import the necessary libraries
from math import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

robotx = 325
roboty = 125


class InputObstacleWindow(QDialog):

    def __init__(self, loxi, loyi, loxf, loyf, LimitZonex, LimitZoney, cnt1):

        super().__init__()
        self.setFixedSize(225, 215)
        self.setWindowTitle('Input Obstacle')
        self.setStyleSheet(
            "background-color: qlineargradient(x1: 0, x2: 1, stop: 0 #202020, stop: 1 #50005E)")
        self.MainWidgets()
        self.loxi = loxi
        self.loyi = loyi
        self.loxf = loxf
        self.loyf = loyf
        self.LimitZonex = LimitZonex
        self.LimitZoney = LimitZoney
        self.cnt1 = cnt1

    # Create a function to create the main widgets of the window
    def MainWidgets(self):

        self.PoxLineEdit = QLineEdit(self)
        self.PoxLineEdit.setGeometry(50, 10, 160, 35)
        self.PoxLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.PoyLineEdit = QLineEdit(self)
        self.PoyLineEdit.setGeometry(50, 50, 160, 35)
        self.PoyLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.WOLineEdit = QLineEdit(self)
        self.WOLineEdit.setGeometry(50, 90, 160, 35)
        self.WOLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.HOLineEdit = QLineEdit(self)
        self.HOLineEdit.setGeometry(50, 130, 160, 35)
        self.HOLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.AcceptOButton = QPushButton(self)
        self.AcceptOButton.setText("Accept")
        self.AcceptOButton.setGeometry(50, 170, 160, 35)
        self.AcceptOButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

        # Set a place holder text in the line edit
        self.PoxLineEdit.setPlaceholderText('0')
        self.PoyLineEdit.setPlaceholderText('0')
        self.WOLineEdit.setPlaceholderText('0')
        self.HOLineEdit.setPlaceholderText('0')

        # Configure an int validator
        intValidator = QIntValidator(self)

        # Set the int validator to the three line edit
        self.PoxLineEdit.setValidator(intValidator)
        self.PoyLineEdit.setValidator(intValidator)
        self.WOLineEdit.setValidator(intValidator)
        self.HOLineEdit.setValidator(intValidator)

        self.PoxLabel = QLabel('Px =', self)
        self.PoxLabel.setGeometry(10, 10, 40, 40)
        self.PoxLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.PoyLabel = QLabel('Py =', self)
        self.PoyLabel.setGeometry(10, 50, 40, 40)
        self.PoyLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.WOLabel = QLabel('W =', self)
        self.WOLabel.setGeometry(10, 90, 40, 40)
        self.WOLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.HOLabel = QLabel('H =', self)
        self.HOLabel.setGeometry(9, 130, 40, 40)
        self.HOLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        # If the button is clicked, go to the function ObstacleCoordinates() and close the window
        self.AcceptOButton.clicked.connect(lambda: self.ObstacleCoordinates())
        self.AcceptOButton.clicked.connect(self.close)

    # Create a warning window if the coordinates that you want to edit are out of the range of the map
    def WarningCoordinates(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! Coordinates out of range")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    # Create a function to input an obstacles on the map
    def ObstacleCoordinates(self):

        # Get the text of the line edit (Oxi, Oyi, Oxf and Oyf)
        self.Oxi = self.PoxLineEdit.text()
        self.Oyi = self.PoyLineEdit.text()
        self.Oxf = self.WOLineEdit.text()
        self.Oyf = self.HOLineEdit.text()

        # If the line edit is empty set it as 0
        if self.Oxi == '':
            self.Oxi = 0

        if self.Oyi == '':
            self.Oyi = 0

        if self.Oxf == '':
            self.Oxf = 0

        if self.Oyf == '':
            self.Oyf = 0

        # Convert the text of the line edit from string to integer
        self.Oxi = int(self.Oxi)
        self.Oyi = int(self.Oyi)
        self.Oxf = int(self.Oxf)
        self.Oyf = int(self.Oyf)

        # If the obstacle is in the range of the map append the coordinates and sizes to their resvective lists
        if -50 <= self.Oxi and self.Oxf <= self.LimitZonex+225-(self.Oxi+robotx) and -50 <= self.Oyi and self.Oyf <= self.LimitZoney+20-(self.Oyi+roboty):

            self.loxi.append(self.Oxi+robotx)
            self.loyi.append(self.Oyi+roboty)
            self.loxf.append(self.Oxf)
            self.loyf.append(self.Oyf)

            # Increment the obstacles counter
            self.cnt1 = self.cnt1+1

            flag_obstacle = 1

        # If the obstacle isn't in the range of the map show its warning window
        else:
            self.WarningCoordinates()
