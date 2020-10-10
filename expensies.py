from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import datetime, sys


MainUI,_ = loadUiType('styles/admin_page - Copy.ui')

class Expensies(MainUI):
    def __init__(self):
        self.check_headers(); self.reset_dates()

    def check_headers(self):
        if self.tableWidget_7.rowCount() > 0 : 
            for i in range(self.tableWidget_7.columnCount()):
                self.tableWidget_7.horizontalHeader().resizeSection(i, 307)

        others = [self.tableWidget_10, self.tableWidget_8, self.tableWidget_6,
        self.tableWidget_9, self.tableWidget_11]
        for table in others:
            if table.rowCount() > 0 :
                for i in range(table.columnCount()):
                    table.horizontalHeader().resizeSection(i, 408)


    def reset_dates(self):
        Dates = [self.dateEdit_5, self.dateEdit_6, self.dateEdit_15, self.dateEdit_16, self.dateEdit_7, 
        self.dateEdit_8, self.dateEdit_3, self.dateEdit_4, self.dateEdit_9, self.dateEdit_10,
        self.dateEdit_18, self.dateEdit_17, self.dateEdit_12, self.dateEdit_19, self.dateEdit_11]
        for i in Dates :
            i.setDate(datetime.datetime.today())
"""
Expensies Columns : 
    Foods : with rows = 307, wihtour rows = 325
    Else : with rows = 408 , wihtour rows = 433
"""