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


class OpenWindow(QWidget):

    def __init__(self, lpx, lpy, lpx_def, lpy_def, lpx_def_units, lpy_def_units, loxi, loyi, loxf, loyf, c, lpa, lc, units, lu):
        super().__init__()
        self.width = 640
        self.height = 480

        # Declare and relate the variables and clear the lists
        self.lpx = lpx
        self.lpy = lpy
        self.lpx_def = lpx_def
        self.lpx_def.clear()
        self.lpy_def = lpy_def
        self.lpy_def.clear()
        self.lpx_def_units = lpx_def_units
        self.lpx_def_units.clear()
        self.lpy_def_units = lpy_def_units
        self.lpy_def_units.clear()
        self.loxi = loxi
        self.loxi.clear()
        self.loyi = loyi
        self.loyi.clear()
        self.loxf = loxf
        self.loxf.clear()
        self.loyf = loyf
        self.loyf.clear()
        self.c = c
        self.lpa = lpa
        self.lpa.clear()
        self.lc = lc
        self.units = units
        self.lu = lu
        self.MainWidgets()

    # Create a function to create the main widgets of the window
    def MainWidgets(self):

        self.resize(self.width, self.height)

        self.setWindowTitle('Open File')

        self.openFileNameDialog()

        self.show()

    # Create an open file window using a QFileDialog
    def openFileNameDialog(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open File", RoutesDirectory)

        if fileName:

            try:

                # Save the file name to tha variable fn
                fn = str(fileName)

                # Open the txt file to read it and assign it to the variable fr
                fr = open(fn, "r")

                # Read the lines of the document and assign them to their respective variables
                self.cpx = fr.readline()
                self.cpy = fr.readline()
                self.cpx_def = fr.readline()
                self.cpy_def = fr.readline()
                self.cpx_def_units = fr.readline()
                self.cpy_def_units = fr.readline()
                self.coxi = fr.readline()
                self.coyi = fr.readline()
                self.coxf = fr.readline()
                self.coyf = fr.readline()
                self.cc = fr.readline()
                self.cpa = fr.readline()
                self.units = fr.readline()

                # If there's a ';' in the text split the text by the ';' to create a list
                if ';' in self.cpx:
                    self.fpx = self.cpx.split(';')
                # If there's no ';' in the text create a list and appent the text to the list
                else:
                    self.fpx = []
                    self.fpx.append(self.cpx)
                if ';' in self.cpy:
                    self.fpy = self.cpy.split(';')
                else:
                    self.fpy = []
                    self.fpy.append(self.cpy)
                if ';' in self.cpx_def:
                    self.fpx_def = self.cpx_def.split(';')
                else:
                    self.fpx_def = []
                    self.fpx_def.append(self.cpx_def)
                if ';' in self.cpy_def:
                    self.fpy_def = self.cpy_def.split(';')
                else:
                    self.fpy_def = []
                    self.fpy_def.append(self.cpy_def)
                if ';' in self.cpx_def_units:
                    self.fpx_def_units = self.cpx_def_units.split(';')
                else:
                    self.fpx_def_units = []
                    self.fpx_def_units.append(self.cpx_def_units)
                if ';' in self.cpy_def_units:
                    self.fpy_def_units = self.cpy_def_units.split(';')
                else:
                    self.fpy_def_units = []
                    self.fpy_def_units.append(self.cpy_def_units)
                if ';' in self.coxi:
                    self.foxi = self.coxi.split(';')
                else:
                    self.foxi = []
                    self.foxi.append(self.coxi)
                if ';' in self.coyi:
                    self.foyi = self.coyi.split(';')
                else:
                    self.foyi = []
                    self.foyi.append(self.coyi)
                if ';' in self.coxf:
                    self.foxf = self.coxf.split(';')
                else:
                    self.foxf = []
                    self.foxf.append(self.coxf)
                if ';' in self.coyf:
                    self.foyf = self.coyf.split(';')
                else:
                    self.foyf = []
                    self.foyf.append(self.coyf)
                if ';' in self.cpa:
                    self.fpa = self.cpa.split(';')
                else:
                    self.fpa = []
                    self.fpa.append(self.cpa)

                # Initialize a counter
                i1 = 0

                # For the counter in range from 0 to the lenght of the coordinates lists proceed
                for i1 in range(0, len(self.fpx)):

                    # Save the text in the position i1 of the list, supress the '\n', convert it into an integer and append it to its respective list
                    string_fpx = self.fpx[i1]
                    string_fpx = string_fpx.strip('\n')
                    self.lpx.append(int(string_fpx))

                    string_fpy = self.fpy[i1]
                    string_fpy = string_fpy.strip('\n')
                    self.lpy.append(int(string_fpy))

                    string_fpx_def = self.fpx_def[i1]
                    string_fpx_def = string_fpx_def.strip('\n')
                    self.lpx_def.append(int(string_fpx_def))

                    string_fpy_def = self.fpy_def[i1]
                    string_fpy_def = string_fpy_def.strip('\n')
                    self.lpy_def.append(int(string_fpy_def))

                    string_fpx_def_units = self.fpx_def_units[i1]
                    string_fpx_def_units = string_fpx_def_units.strip('\n')
                    self.lpx_def_units.append(float(string_fpx_def_units))

                    string_fpy_def_units = self.fpy_def_units[i1]
                    string_fpy_def_units = string_fpy_def_units.strip('\n')
                    self.lpy_def_units.append(float(string_fpy_def_units))

                # Initialize a counter
                i2 = 0

                # For the counter in range from 0 to the lenght of the obstacles lists proceed
                for i2 in range(0, len(self.foxi)):

                    # Save the text in the position i2 of the list, supress the '\n', convert it into an integer and append it to its respective list
                    string_foxi = self.foxi[i2]
                    string_foxi = string_foxi.strip('\n')
                    self.loxi.append(int(string_foxi))

                    string_foyi = self.foyi[i2]
                    string_foyi = string_foyi.strip('\n')
                    self.loyi.append(int(string_foyi))

                    string_foxf = self.foxf[i2]
                    string_foxf = string_foxf.strip('\n')
                    self.loxf.append(int(string_foxf))

                    string_foyf = self.foyf[i2]
                    string_foyf = string_foyf.strip('\n')
                    self.loyf.append(int(string_foyf))

                # Initialize a counter
                i3 = 0

                # For the counter in range from 0 to the lenght of the angles list proceed
                for i3 in range(0, len(self.fpa)):

                    # Save the text in the position i3 of the list, supress the '\n', convert it into an integer and append it to its respective list
                    string_fpa = self.fpa[i3]
                    string_fpa = string_fpa.strip('\n')
                    self.lpa.append(float(string_fpa))

                # Erase the '\n' from the text and append it to a list
                self.cc = self.cc.strip('\n')
                self.lc.append(self.cc)

                self.units = self.units.strip('\n')
                self.lu.append(self.units)

            except:
                pass
