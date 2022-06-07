# Import the necessary libraries
from math import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class WiFiWindow(QDialog):

    # Here we declare a variable in the init called mare which allows us comunicate with the main window
    def __init__(self, mare):

        super().__init__()
        self.mare = mare
        self.setFixedSize(225, 175)
        self.setWindowTitle('Configurate WiFi')
        self.setStyleSheet(
            "background-color: qlineargradient(x1: 0, x2: 1, stop: 0 #202020, stop: 1 #50005E)")
        self.MainWidgets()

    # Create a function to create the main widgets of the window
    def MainWidgets(self):

        self.SSIDLineEdit = QLineEdit(self)
        self.SSIDLineEdit.move(50, 10)
        self.SSIDLineEdit.resize(160, 35)
        self.SSIDLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.PasswordLineEdit = QLineEdit(self)
        self.PasswordLineEdit.move(50, 50)
        self.PasswordLineEdit.resize(160, 35)
        self.PasswordLineEdit.setStyleSheet(
            "background-color: rgba(255,255,255,20); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        # Set the password  mode to hide the password
        self.PasswordLineEdit.setEchoMode(QLineEdit.Password)

        self.SSIDLabel = QLabel('SSID', self)
        self.SSIDLabel.move(10, 10)
        self.SSIDLabel.resize(40, 30)
        self.SSIDLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.PasswordLabel = QLabel('PWD', self)
        self.PasswordLabel.move(10, 50)
        self.PasswordLabel.resize(40, 30)
        self.PasswordLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        self.SendButton = QPushButton(self)
        self.SendButton.setText("Send")
        self.SendButton.move(50, 90)
        self.SendButton.resize(160, 35)
        self.SendButton.setStyleSheet(
            "QPushButton{color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; background-color:rgb(255,255,255,20); border-radius:5px}""QPushButton:hover{background-color : rgb(255,255,255,100);}")

        self.SendingLabel = QLabel('', self)
        self.SendingLabel.move(50, 130)
        self.SendingLabel.resize(130, 30)
        self.SendingLabel.setStyleSheet(
            "background-color: rgb(255,255,255,0); color:white; font-weight: bold; font-size: 8pt; font-family: Helvetica; border-radius:5px;")

        # If the button is clicked connect it to the function GetCredentials()
        self.SendButton.clicked.connect(lambda: self.GetCredentials())

    # Create a function to use the socket function from the main window to sent the WiFi credentials
    def GetCredentials(self):

        # Get the text of the line edit (SSID and Password)
        self.SSID = self.SSIDLineEdit.text()
        self.Password = self.PasswordLineEdit.text()

        if self.SSID == '':
            self.SSID = ' '
        if self.Password == '':
            self.Password = ' '

        self.credentials = self.SSID+'* *'+self.Password

        # Try to compute
        try:

            # Send the SSID ans Password via sockets
            self.mare.SocketSend(self.credentials)

            # Show the message 'Sended' on the window
            self.SendingLabel.setText('Sended')

        # If the program can't be computed show a warning window
        except:
            self.WarningNoConnection()

    # Create a warning window
    def WarningNoConnection(self):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Warning! No connection with the server")
        self.msg.setWindowTitle("Warning Window")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()
