# Import the necessary libraries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

robotx = 300
roboty = 125

# Create a QWidget class which will represent the Robot


class Robot(QWidget):

    # We input the variable parent in the init to make it visible in the main window
    def __init__(self, parent, width, height):

        super().__init__(parent)
        self.setGeometry(0, 0, width, height)

        # We create a QLabel to input QPixmap in it and show an scaled image into the pixmap
        label = QLabel(self)
        pixmap = QPixmap('Rounded_Robot_White.png').scaled(width, height)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
