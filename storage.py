from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys

MainUI,_ = loadUiType('styles/storage.ui')

class Storage(QWidget, MainUI):
    def __init__(self, parent = None):
        super(Storage, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Storage")
        self.setFixedSize(self.size())

