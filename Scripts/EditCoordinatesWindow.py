# Import the necessary libraries
from math import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

robotx = 300
roboty = 125


class EditCoordinatesWindow(QDialog):

    def __init__(self, lpx, lpy, lpx_def, lpy_def, lpx_def_units, lpy_def_units, lpa, CoordType, LimitZonex, LimitZoney, units):

        super().__init__()
        self.setFixedSize(225, 215)
        self.setWindowTitle('Edit Coordinates')
        self.setStyleSheet(
            "background-color: qlineargradient(x1: 0, x2: 1, stop: 0 #202020, stop: 1 #50005E)")
        self.MainWidgets()
        self.CN = 0
        self.NewPx = 0
        self.NewPy = 0
        self.lpx = lpx
        self.lpy = lpy
        self.lpx_def = lpx_def
        self.lpy_def = lpy_def
        self.lpx_def_units = lpx_def_units
        self.lpy_def_units = lpy_def_units
        self.lpa = lpa
        self.CoordType = CoordType
        self.LimitZonex = LimitZonex
        self.LimitZoney = LimitZoney
        self.units = units

    # Create a warning window if the coordinate that you want to edit is the first one (Robot's position)
    def WarningInitialCoordinates(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(
            "Warning! The initial coordinates must be changed in the Robot Coordinates")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    # Create a warning window if the coordinates are out of the range of the map
    def WarningCoordinates(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! Coordinates out of range")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    # Create a warning window if the coordinate that you want to edit don't exixt
    def WarningNoCoordinates(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! There's no poin in each position")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    # Create a warning window if the coordinate that you want to erase is the first one (Robot's position)
    def WarningInitialCoordinatesErase(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! The initial coordinates can't be erased")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    # Create a function to create the main widgets of the window
    def MainWidgets(self):

        self.CNLineEdit = QLineEdit(self)
        self.CNLineEdit.setGeometry(50, 10, 160, 35)
        self.CNLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.ECxLineEdit = QLineEdit(self)
        self.ECxLineEdit.setGeometry(50, 50, 160, 35)
        self.ECxLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.ECyLineEdit = QLineEdit(self)
        self.ECyLineEdit.setGeometry(50, 90, 160, 35)
        self.ECyLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.AcceptECButton = QPushButton(self)
        self.AcceptECButton.setText("Accept")
        self.AcceptECButton.setGeometry(50, 130, 160, 35)
        self.AcceptECButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

        self.EraseECButton = QPushButton(self)
        self.EraseECButton.setText("Erase")
        self.EraseECButton.setGeometry(50, 170, 160, 35)
        self.EraseECButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

        # Set a place holder text in the line edit
        self.CNLineEdit.setPlaceholderText('0')
        self.ECxLineEdit.setPlaceholderText('0')
        self.ECyLineEdit.setPlaceholderText('0')

        # Configure an int validator
        intValidator = QIntValidator(self)

        # Set the int validator to the three line edit
        self.CNLineEdit.setValidator(intValidator)
        self.ECxLineEdit.setValidator(intValidator)
        self.ECyLineEdit.setValidator(intValidator)

        self.CNLabel = QLabel('Nº =', self)
        self.CNLabel.setGeometry(10, 10, 40, 40)
        self.CNLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.ECxLabel = QLabel('Px =', self)
        self.ECxLabel.setGeometry(10, 50, 40, 40)
        self.ECxLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.ECyLabel = QLabel('Py =', self)
        self.ECyLabel.setGeometry(9, 90, 40, 40)
        self.ECyLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        # If the vutton is clicked, go to the function and close the window
        self.AcceptECButton.clicked.connect(lambda: self.EditCoordinates())
        self.AcceptECButton.clicked.connect(self.close)
        self.EraseECButton.clicked.connect(lambda: self.EraseCoordinates())
        self.EraseECButton.clicked.connect(self.close)

    # Create a function to edit the coordinates of the route
    def EditCoordinates(self):

        # Get the text of the line edit (CN, ECx and ECy)
        self.CN = self.CNLineEdit.text()
        self.NewPx = self.ECxLineEdit.text()
        self.NewPy = self.ECyLineEdit.text()

        # If the line edit is empty set it as 0
        if self.CN == '':
            self.CN = 0

        if self.NewPx == '':
            self.NewPx = 0

        if self.NewPy == '':
            self.NewPy = 0

        # Convert the text of the line edit from string to integer
        self.CN = int(self.CN)
        self.NewPx = int(self.NewPx)
        self.NewPy = int(self.NewPy)

        # If the text in CN is higher than 0 and less than the lenght of the list of coordinates-1 (to avoid the first position of the Robot)
        if self.CN <= len(self.lpx)-1 and self.CN > 0:

            # If CoordType=1 (incremental coordinates) save lpx[CN] in cx and save lpy[CN] in cy
            if self.CoordType == 1:
                self.cx = self.lpx[self.CN]
                self.cy = self.lpy[self.CN]

            # If CoordType=0 (absolute coordinates) save the first position of the robot in cx and cy respectively
            else:
                self.cx = self.lpx[0]
                self.cy = self.lpy[0]

            # Compute the new x position
            if self.NewPx == 0:
                self.xm = self.cx
            else:
                self.xm = self.NewPx+self.cx

            # Compute the new y position
            if self.NewPy == 0:
                self.ym = self.cy
            else:
                self.ym = self.NewPy+self.cy

            # If the new x and y positions are in the range of the map append the coordinates to the list coordinates
            if robotx <= self.xm <= self.LimitZonex+225 and roboty <= self.ym <= self.LimitZoney+20:

                if self.NewPx == 0:
                    self.lpx[self.CN] = self.xm
                    self.lpx_def[self.CN] = self.xm-self.lpx[0]
                    self.lpx_def_units[self.CN] = (
                        self.xm-self.lpx[0])*self.units
                else:
                    self.lpx[self.CN] = self.xm
                    self.lpx_def[self.CN] = self.xm-self.lpx[0]
                    self.lpx_def_units[self.CN] = (
                        self.xm-self.lpx[0])*self.units

                if self.NewPy == 0:
                    self.lpy[self.CN] = self.ym
                    self.lpy_def[self.CN] = self.ym-self.lpy[0]
                    self.lpy_def_units[self.CN] = (
                        self.ym-self.lpy[0])*self.units
                else:
                    self.lpy[self.CN] = self.ym
                    self.lpy_def[self.CN] = self.ym-self.lpy[0]
                    self.lpy_def_units[self.CN] = (
                        self.ym-self.lpy[0])*self.units

            # If the new x and y positions aren't in the range of the map show its warning window
            else:
                self.WarningCoordinates()

        # If the coordinate to edit is the one which is in position 0 show its warning window
        elif self.CN == 0:
            self.WarningInitialCoordinates()

         # If the coordinate to edit don't exist show its warning window
        else:
            self.WarningNoCoordinates()

    # Function to erase a coordinate
    def EraseCoordinates(self):

        # Get the text of the line edit
        self.CN = self.CNLineEdit.text()

        # If the line edit is empty set it as 0
        if self.CN == '':
            self.CN = 0

        # Convert the text of the line edit from string to integer
        self.CN = int(self.CN)

        # If the text in CN is higher than 0 and less than the lenght of the list of coordinates-1 (to avoid the first position of the Robot)
        if self.CN <= len(self.lpx)-1 and self.CN > 0:

            # Erase the coordinate of the list
            self.lpx.pop(self.CN)
            self.lpy.pop(self.CN)
            self.lpx_def.pop(self.CN)
            self.lpy_def.pop(self.CN)
            self.lpx_def_units.pop(self.CN)
            self.lpy_def_units.pop(self.CN)
            self.lpa.pop(self.CN)

        # If the coordinate to edit is the one which is in position 0 show its warning window
        elif self.CN == 0:
            self.WarningInitialCoordinatesErase()

        # If the coordinate to edit don't exist show its warning window
        else:
            self.WarningNoCoordinates()
