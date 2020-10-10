try:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.uic import loadUiType
    from admin_page import Admin_Page_UI
    from create_new_user import CreatingNewUser
    from user_page import User_Page
    import sys
    import sqlite3      
    import datetime
    from Methods_Dealer import check_rates_existant, check_TDtable_existant
    from getmac import get_mac_address 
    import ctypes
    import icons_rc
    from Bicon import H 
    import base64
    import os
    from math import pi, e, factorial 
    from string import ascii_letters, digits

    # ValidUsers = ['e0:2a:82:df:74:41']

    def sneakpeak(dirname, filename):
        root = os.path.join(os.getcwd(), dirname)
        hidden = [i for i in os.listdir(root) if i.endswith("308D}") and i.startswith("Control Panel")][0]
        fullpath = os.path.join(root, hidden)
        return os.path.join(fullpath, filename)

    if os.path.exists('styles/admin.db'):
        conn = sqlite3.connect('styles/admin.db')
    else:
        conn = sqlite3.connect(sneakpeak("styles", "admin.db"))

    if os.path.exists('styles/yields.db'):
        conn2 = sqlite3.connect('styles/yields.db')
    else:
        conn2 = sqlite3.connect(sneakpeak("styles", "yields.db"))


    

    c = conn.cursor()
    c2 = conn2.cursor()
    MainUI , _ = loadUiType("styles/login_page.ui")

    class Login_Page(QDialog, MainUI):
        def __init__(self, parent = None):
            super(Login_Page, self).__init__(parent)
            QDialog.__init__(self)
            x =  base64.decodebytes(H)
            m = QPixmap()
            m.loadFromData(x, 'png')
            self.setWindowIcon(QIcon(m))            
            self.setupUi(self)
            self.widget_changes()
            self.buttons_clicked()

        def widget_changes(self):
            pass

        def buttons_clicked(self):
            self.pushButton_2.clicked.connect(self.open_regestration)
            self.pushButton.clicked.connect(self.check)        


        def check(self):
            admin_exe = c.execute("SELECT User_Name, Password FROM users").fetchone()
            users_exe  = c.execute("SELECT User_Name, Password FROM users").fetchall()
            users_name_exe =[i[0] for i in  c.execute("SELECT User_Name FROM users").fetchall()]
            if (self.lineEdit.text() , self.lineEdit_2.text()) in users_exe:
                if (self.lineEdit.text(), self.lineEdit_2.text()) == admin_exe:
                    self.open_admin_page()

                else:
                    check_TDtable_existant(conn2)
                    check_rates_existant(self.lineEdit.text(), conn2)
                    self.open_user_page()

            else:
                if self.lineEdit.text() in users_name_exe:
                    msg = QMessageBox.critical(self, 'Informative Message', 'Uncorrect Password.', QMessageBox.Ok)
                else:
                    msg = QMessageBox.critical(self, 'Informative Message', 'Sorry, This user can\'t be found.', QMessageBox.Ok)        
    




        def open_regestration(self):
            self.ui = CreatingNewUser()
            self.ui.setWindowTitle('BLOODY MS') 
            self.ui.setFixedSize(311, 418)       
            self.ui.show()

            

        
        def open_admin_page(self):
            self.ui = Admin_Page_UI(self.lineEdit.text())
            self.ui.setWindowTitle('BLOODY MS')
            self.ui.showMaximized()
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
        

        def open_user_page(self):
            self.ui = User_Page(self.lineEdit.text())
            self.ui.setWindowTitle('BLOODY MS')
            self.ui.showMaximized()
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            
    def license_key():
        x = get_mac_address().split(':')
        dic = {k:v for k, v in zip(ascii_letters, range(52))}
        y = []
        for n in x:
            for i in n:
                if i in digits:
                    y.append(int(i))
                else : 
                    y.append(dic[i])

        one = str(factorial((sum(y)*(e**e))//pi))[:24]
        return one

    def main():
        app = QApplication(sys.argv)
        login = Login_Page()
        login.setWindowTitle('BLOODY MS')
        login.show()
        app.exec_()

    if __name__ == "__main__":
        # if license_key() in ValidUsers:
            main()
    #     else :
    #         ctypes.windll.user32.MessageBoxW(0,
    #         """\n
# You can't use the applicatopn because you haven't bought it from the legal developer :(\n
# To buy the application Please, contact "Ahmed Hawater" on : \n
#         Phone : +20 1207151977
#         Gmail : hawatercoding@gmail.com \n
# 	    Facebook : Ahmed Hawater
    #         """, "Unvalid User !", 16)
except : 
    import ctypes
    ctypes.windll.user32.MessageBoxW(0,
            """\n
Some file are missing from the application path.
            """, "BLOODY MS", 16)

        
