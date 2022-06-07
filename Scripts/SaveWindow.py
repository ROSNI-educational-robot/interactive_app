# Import the necessary libraries
from math import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os

# Save the directory of the scripts and save the directory of the routes
Directory = os.getcwd()
RoutesDirectory = Directory.replace('\Scripts', '\Routes')

robotx = 300
roboty = 125


class SaveWindow(QWidget):

    def __init__(self, lpx, lpy, lpx_def, lpy_def, lpx_def_units, lpy_def_units, loxi, loyi, loxf, loyf, c, lpa, units):

        super().__init__()
        self.width = 640
        self.height = 480

        # Declare and relate the variables
        self.lpx = lpx
        self.lpy = lpy
        self.lpx_def = lpx_def
        self.lpy_def = lpy_def
        self.lpx_def_units = lpx_def_units
        self.lpy_def_units = lpy_def_units
        self.loxi = loxi
        self.loyi = loyi
        self.loxf = loxf
        self.loyf = loyf
        self.c = c
        self.lpa = lpa
        self.units = units

        self.MainWidgets()

    # Create a function to create the main widgets of the window
    def MainWidgets(self):

        self.resize(self.width, self.height)
        self.setWindowTitle('Save File')

        self.saveFileDialog()

        self.show()

    # Create a save file window using a QFileDialog
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save File", RoutesDirectory)

        if fileName:

            # Save the file name to tha variable q1
            q1 = fileName

            # If the file name contains a '.csv', save it to a variable named q2
            if '.csv' in str(q1):
                q2 = str(q1)

            # If the file name don't contains a '.csv', add a '.csv' on it and save it to a variable named q2
            else:
                q2 = str(q1)+'.csv'

            # Open the txt file to write on it and assign it to the variable q2
            fw = open(q2, "w")

            # Convert every list into a chain of characters united by ';' and the varables into str
            cpx = ';'.join(map(str, self.lpx))
            cpy = ';'.join(map(str, self.lpy))
            cpx_def = ';'.join(map(str, self.lpx_def))
            cpy_def = ';'.join(map(str, self.lpy_def))
            cpx_def_units = ';'.join(map(str, self.lpx_def_units))
            cpy_def_units = ';'.join(map(str, self.lpy_def_units))
            coxi = ';'.join(map(str, self.loxi))
            coyi = ';'.join(map(str, self.loyi))
            coxf = ';'.join(map(str, self.loxf))
            coyf = ';'.join(map(str, self.loyf))
            c = str(self.c)
            cpa = ';'.join(map(str, self.lpa))
            units = str(self.units)

            # Write the chains and strings into the .csv file line under line
            fw.write(cpx+'\n')
            fw.write(cpy+'\n')
            fw.write(cpx_def+'\n')
            fw.write(cpy_def+'\n')
            fw.write(cpx_def_units+'\n')
            fw.write(cpy_def_units+'\n')
            fw.write(coxi+'\n')
            fw.write(coyi+'\n')
            fw.write(coxf+'\n')
            fw.write(coyf+'\n')
            fw.write(c+'\n')
            fw.write(cpa+'\n')
            fw.write(units)

            # Close the .csv file
            fw.close()
