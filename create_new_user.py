from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys
import datetime
import sqlite3
import os
from Bicon import H 
import base64
import icons2_rc


def sneakpeak(dirname, filename):
    root = os.path.join(os.getcwd(), dirname)
    hidden = [i for i in os.listdir(root) if i.endswith("308D}") and i.startswith("Control Panel")][0]
    fullpath = os.path.join(root, hidden)
    return os.path.join(fullpath, filename)

if os.path.exists('styles/admin.db'):
    conn = sqlite3.connect('styles/admin.db')
else:
    conn = sqlite3.connect(sneakpeak("styles", "admin.db"))

c = conn.cursor()
MainUI, _ = loadUiType('styles/CreateNewUser_page.ui')

class CreatingNewUser(QWidget, MainUI):
    def __init__(self, parent = None):
        super(CreatingNewUser, self).__init__(parent)
        QWidget.__init__(self)
        x =  base64.decodebytes(H)
        m = QPixmap()
        m.loadFromData(x, 'png')
        self.setWindowIcon(QIcon(m))         
        self.setupUi(self)
        self.clicked_buttons()
        

    def clicked_buttons(self):
        self.Submit_button.clicked.connect(self.add_new_user)
        self.Submit_button.setShortcut('Return')
        self.toolButton.clicked.connect(self.show_pass)

    def show_pop(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()

    def show_pass(self):
        if self.toolButton.isChecked():
            self.Password_input.setEchoMode(QLineEdit.Normal)
        else : self.Password_input.setEchoMode(QLineEdit.Password)

    def add_new_user(self):
        today_datetime = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S")
        LineEdits = [self.User_name_input.text(), self.Password_input.text(), self.Email_input.text(), self.Phone_number_input.text(),
        self.Admin_password_input.text(), self.National_ID_input.text()]
        if all([i !="" for i in LineEdits[0:3]]) and self.Admin_password_input.text() !="" and len(self.Phone_number_input.text()) != 11 :
            msg = QMessageBox.critical(self,"Uncorrect Data", "Phone Number isn't 11 numebers  Please, Re-enter your Phone Numebr.")

        elif all([i !="" for i in LineEdits[0:4]]) and self.Admin_password_input.text() !="" and len(self.National_ID_input.text()) != 14 :
            msg = QMessageBox.critical(self, "Uncorrect Data", "National ID isn't 14 numebers  Please, Re-enter your National ID.")

        elif any([i =="" for i in LineEdits]):
            msg = QMessageBox.critical(self, "Missing Data", "Make sure you entered all of the required data ! ")

        else :
            admin_code = c.execute("SELECT Password FROM Users").fetchone()
            if admin_code == None:
                try:
                    if self.Admin_password_input.text() == self.Password_input.text() :
                        c.execute("""
                        INSERT INTO Users VALUES ('{}', '{}', '{}', '{}','{}', '{}')
                        """.format(self.User_name_input.text(), self.Password_input.text(), self.Email_input.text(), self.Phone_number_input.text(), self.National_ID_input.text(), today_datetime))
                        conn.commit()
                        msg = QMessageBox.information(self, "Congrats", "New user has been created successfuly.", QMessageBox.Ok)
                        with open('{}/users_notes/{}.txt'.format(os.getcwd().replace("\\", '/') ,self.User_name_input.text()), 'w') as f:
                            f.write('')
                        self.User_name_input.setText("") 
                        self.Password_input.setText("") 
                        self.Email_input.setText("") 
                        self.Phone_number_input.setText("")
                        self.Admin_password_input.setText("")
                        self.National_ID_input.setText("")  
                    else : 
                        msg = QMessageBox.critical(self, "Uncorrect Data", "Admin, Please confirm your password. ")
                except sqlite3.IntegrityError:
                    msg = QMessageBox.critical(self, "Common data have been entered", "Your User_Name, Email, National ID or Phone_Number have been entered before by another user.")
            else :
                if self.Admin_password_input.text() == admin_code[0]:
                    try:
                        c.execute("""
                        INSERT INTO Users VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
                        """.format(self.User_name_input.text(), self.Password_input.text(), self.Email_input.text(), self.Phone_number_input.text(), self.National_ID_input.text(), today_datetime))
                        conn.commit()
                        with open('{}/users_notes/{}.txt'.format(os.getcwd().replace("\\", '/') ,self.User_name_input.text()), 'w') as f:
                            f.write('')
                        msg = QMessageBox.information(self, "Congrats", "New user has been created successfuly.", QMessageBox.Ok)
                        self.User_name_input.setText("") 
                        self.Password_input.setText("") 
                        self.Email_input.setText("") 
                        self.Phone_number_input.setText("")
                        self.Admin_password_input.setText("")
                        self.National_ID_input.setText("") 
                    except sqlite3.IntegrityError:
                        msg = QMessageBox.critical(self, "Common data have been entered", "Your User_Name, Email, or Phone_Number have been entered before by another user.")
                else:
                    msg = QMessageBox.critical(self, "Uncorrect Data", "Admin password isn't correct.")


def main():
    app = QApplication(sys.argv)
    window = CreatingNewUser()
    window.setFixedSize(311, 418)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()