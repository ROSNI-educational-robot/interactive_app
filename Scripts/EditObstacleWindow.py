# Import the necessary libraries
from math import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

robotx = 325
roboty = 125


class EditObstacleWindow(QDialog):

    def __init__(self, lpx, lpy, loxi, loyi, loxf, loyf, CoordType, LimitZonex, LimitZoney):

        super().__init__()
        self.setFixedSize(225, 295)
        self.setWindowTitle('Edit Obstacle')
        self.setStyleSheet(
            "background-color: qlineargradient(x1: 0, x2: 1, stop: 0 #202020, stop: 1 #50005E)")
        self.CN = 0
        self.Newx = 0
        self.Newy = 0
        self.Neww = 0
        self.Newh = 0
        self.lpx = lpx
        self.lpy = lpy
        self.loxi = loxi
        self.loyi = loyi
        self.loxf = loxf
        self.loyf = loyf
        self.CoordType = CoordType
        self.LimitZonex = LimitZonex
        self.LimitZoney = LimitZoney
        self.MainWidgets()

    # Create a warning window if the coordinates that you want to edit are out of the range of the map
    def WarningCoordinates(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! Coordinates out of range")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    # Create a warning window if the obstacle that you want to edit don't exist
    def WarningNoObstacle(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! There's no obstacle in each position")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

    # Create a function to create the main widgets of the window
    def MainWidgets(self):

        self.CNLineEdit = QLineEdit(self)
        self.CNLineEdit.setGeometry(50, 10, 160, 35)
        self.CNLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.xLineEdit = QLineEdit(self)
        self.xLineEdit.setGeometry(50, 50, 160, 35)
        self.xLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.yLineEdit = QLineEdit(self)
        self.yLineEdit.setGeometry(50, 90, 160, 35)
        self.yLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.wLineEdit = QLineEdit(self)
        self.wLineEdit.setGeometry(50, 130, 160, 35)
        self.wLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.hLineEdit = QLineEdit(self)
        self.hLineEdit.setGeometry(50, 170, 160, 35)
        self.hLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.AcceptECButton = QPushButton(self)
        self.AcceptECButton.setText("Accept")
        self.AcceptECButton.setGeometry(50, 210, 160, 35)
        self.AcceptECButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

        self.EraseECButton = QPushButton(self)
        self.EraseECButton.setText("Erase")
        self.EraseECButton.setGeometry(50, 250, 160, 35)
        self.EraseECButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

        # Set a place holder text in the line edit
        self.CNLineEdit.setPlaceholderText('0')
        self.xLineEdit.setPlaceholderText('0')
        self.yLineEdit.setPlaceholderText('0')
        self.wLineEdit.setPlaceholderText('0')
        self.hLineEdit.setPlaceholderText('0')

        # Configure an int validator
        intValidator = QIntValidator(self)

        # Set the int validator to the three line edit
        self.CNLineEdit.setValidator(intValidator)
        self.xLineEdit.setValidator(intValidator)
        self.yLineEdit.setValidator(intValidator)
        self.wLineEdit.setValidator(intValidator)
        self.hLineEdit.setValidator(intValidator)

        self.CNLabel = QLabel('Nº =', self)
        self.CNLabel.setGeometry(10, 10, 40, 40)
        self.CNLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.xLabel = QLabel('Px =', self)
        self.xLabel.setGeometry(10, 50, 40, 40)
        self.xLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.yLabel = QLabel('Py =', self)
        self.yLabel.setGeometry(9, 90, 40, 40)
        self.yLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.wLabel = QLabel('W =', self)
        self.wLabel.setGeometry(10, 130, 40, 40)
        self.wLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.hLabel = QLabel('H =', self)
        self.hLabel.setGeometry(9, 170, 40, 40)
        self.hLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        # If the button is clicked, go to the function and close the window
        self.AcceptECButton.clicked.connect(lambda: self.EditObstacle())
        self.AcceptECButton.clicked.connect(self.close)
        self.EraseECButton.clicked.connect(lambda: self.EraseObstacle())
        self.EraseECButton.clicked.connect(self.close)

    # Create a function to edit the obstacles of the map
    def EditObstacle(self):

        # Get the text of the line edit (CN, Newx, Newy, Neww and Newh)
        self.CN = self.CNLineEdit.text()
        self.Newx = self.xLineEdit.text()
        self.Newy = self.yLineEdit.text()
        self.Neww = self.wLineEdit.text()
        self.Newh = self.hLineEdit.text()

        # If the line edit is empty set it as 0
        if self.CN == '':
            self.CN = 0

        if self.Newx == '':
            self.Newx = 0

        if self.Newy == '':
            self.Newy = 0

        if self.Neww == '':
            self.Neww = 0

        if self.Newh == '':
            self.Newh = 0

        # Convert the text of the line edit from string to integer
        self.CN = int(self.CN)
        self.Newx = int(self.Newx)
        self.Newy = int(self.Newy)
        self.Neww = int(self.Neww)
        self.Newh = int(self.Newh)

        # If the text in CN is higher than 0 and less than the lenght of the list of obstacles
        if self.CN < len(self.loxi) and self.CN > 0:

            # If CoordType=1 (incremental coordinates) save loxi[CN] in cx, save loyi[CN] in cy, loxf[CN] in cw and save loyf[CN] in ch
            if self.CoordType == 1:
                self.cx = self.loxi[self.CN]
                self.cy = self.loyi[self.CN]
                self.cw = self.loxf[self.CN]
                self.ch = self.loyf[self.CN]

            # If CoordType=0 (absolute coordinates) save first position of the robot in cx and cy respectively
            else:

                # If the list of coordinates is set cx ans cy as robotx and roboty respectively
                if len(self.lpx) == 0:
                    self.cx = robotx
                    self.cy = roboty

                # If the coordinates list isn't empty set cx and cy as the fist position of the coordinates lists respectively
                else:
                    self.cx = self.lpx[0]
                    self.cy = self.lpy[0]

                # Set the obstacle width and height to 0
                self.cw = 0
                self.ch = 0

            # Compute the new x position
            if self.Newx == 0:
                self.xm = self.cx
            else:
                self.xm = self.Newx+self.cx

            # Compute the new x position
            if self.Newy == 0:
                self.ym = self.cy
            else:
                self.ym = self.Newy+self.cy

            # Compute the new width
            self.Neww = self.Neww+self.cw

            # Compute the new height
            self.Newh = self.Newh+self.ch

            # If the obstacle is in the range of the map append the coordinates and sizes to their resvective lists
            if (225+50) <= self.xm and self.Neww <= self.LimitZonex+225-(self.xm-50) and (20+50) <= self.ym and self.Newh <= self.LimitZoney+20-(self.ym-50):
                self.loxi[self.CN] = self.xm
                self.loyi[self.CN] = self.ym
                self.loxf[self.CN] = self.Neww
                self.loyf[self.CN] = self.Newh

            # If the obstacle isn't in the range of the map show its warning window
            else:
                self.WarningCoordinates()

        # If the obstacle don't exist show its warning window
        else:
            self.WarningNoObstacle()

    # Create a function to erase an obstacles from the route
    def EraseObstacle(self):

        # Get the text of the line edit
        self.CN = self.CNLineEdit.text()

        # If the line edit is empty set it as 0
        if self.CN == '':
            self.CN = 0

        # Convert the text of the line edit from string to integer
        self.CN = int(self.CN)

        # If the text in CN is higher than 0 and less than the lenght of the list of obstacles
        if self.CN <= len(self.loxi) and self.CN > 0:

            # Erase the coordinate of the list
            self.loxi.pop(self.CN)
            self.loyi.pop(self.CN)
            self.loxf.pop(self.CN)
            self.loyf.pop(self.CN)

        # If the obstacle to erase don't exist show its warning window
        else:
            self.WarningNoObstacle()
