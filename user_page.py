from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from datetime import date, datetime, timedelta, time
import collections
import sqlite3
from playsound import playsound
import concurrent.futures
import os
import smtplib
from email.message import EmailMessage
import csv
from Methods_Dealer import check_TDtable_existant, check_rates_existant
from math import ceil
from Bicon import H 
import base64

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

cursor = conn.cursor()
cursor2 = conn2.cursor()
MainUI, _ = loadUiType('styles/user_page.ui')

class User_Page(QTabWidget, MainUI):

    def __init__(self, global_user_name,  parent = None):
        self.global_user_name = global_user_name
        self.exa = 0
        self.UntilNOw_Food = None
        super(User_Page, self).__init__(parent)
        QTabWidget.__init__(self)
        x =  base64.decodebytes(H)
        m = QPixmap()
        m.loadFromData(x, 'png')
        self.setWindowIcon(QIcon(m)) 
        self.setupUi(self)
        self.ClearReset()
        self.widget_changes()
        self.clicked_buttons()
        self.groupboxes = [self.groupBox, self.groupBox_2, self.groupBox_3, self.groupBox_4, self.groupBox_5, self.groupBox_6, self.groupBox_7
        ,self.groupBox_8, self.groupBox_9, self.groupBox_10, self.groupBox_11, self.groupBox_12, self.groupBox_13, self.groupBox_14, self.groupBox_15
        , self.groupBox_16, self.groupBox_17, self.groupBox_18]
        self.rename_groupBoxes()

    def taboo0(self):
        if self.currentIndex() != 0:
            self.listWidget_19.clearSelection()
            self.listWidget_19.reset()

    def ClearReset(self):
        self.ClearTimer = QTimer()
        self.ClearTimer.timeout.connect(self.taboo0)
        self.ClearTimer.start(1000)

    def Today_Inventory(self):
        try : 
            NotSeprated_Foods = []
            Level = []

            x = [i[0] for i in cursor2.execute(f'SELECT "Food" FROM "{date.today()}" WHERE "User Name" = "{self.global_user_name}" ').fetchall()]
            Level.extend([i.split(" / ") for i in x])
            for i in Level:
                NotSeprated_Foods.extend(i)


            Food_Inventory = []
            Food_Names = [i[0] for i in cursor.execute('SELECT Name FROM Foods ').fetchall()]

            for i in Food_Names:
                Level_0 =  list( filter(lambda x : x.split(":")[0] == i, NotSeprated_Foods) ) 

                OneItem_summ = sum([int(x.split(':')[1]) for x in Level_0])
                Food_Inventory.append(f'{i}:{OneItem_summ}')

            Food_Inventory = [i for i in Food_Inventory if i.split(":")[-1] != "0"]

            cursor2.execute('UPDATE users_rates SET food = "{}" WHERE date = "{}" AND user_name = "{}" '.format(' / '.join(Food_Inventory), date.today(), self.global_user_name))
            conn2.commit()

            self.listWidget_19.addItems(Food_Inventory)
            self.UntilNOw_Food =  " / ".join(Food_Inventory)
        except :
            msg = QMessageBox.warning(self.tab, "Connection Failed", "There is no internet connection", QMessageBox.Ok)

# Sending Emails Methods   
    def EmailOperationStyling(self):
        self.lineEdit_19.clear()
        self.lineEdit_19.setEchoMode(QLineEdit.Password)
        self.lineEdit_19.setStyleSheet("border: 2px solid#aaaaaa; min-height : 30px; font-size : 14pt")

    def sending(self):
        user_password = cursor.execute(f'SELECT Password FROM Users WHERE User_Name = "{self.global_user_name}" ').fetchone()[0]
        if self.lineEdit_19.text() == user_password:
            try:
                if self.SENDING_mechanics():
                    self.lineEdit_19.clear()
                    msg  = QMessageBox.information(self.tab, "Informative Message", "Email has been sent Successfully", QMessageBox.Ok)
                else : 
                    os.remove('TodayYields.csv')
                    self.lineEdit_19.clear() 
                    msg5 = QMessageBox.critical(self.tab, "Access Denied", "Sorry,  Admin's  Email  is  Unvalid", QMessageBox.Ok)
            except smtplib.socket.gaierror:
                os.remove('TodayYields.csv')
                self.lineEdit_19.clear()                
                msg2 = QMessageBox.warning(self.tab, "Connection Failed", "There is no internet connection", QMessageBox.Ok)
        else :
            self.lineEdit_19.setEchoMode(QLineEdit.Normal)
            self.lineEdit_19.setStyleSheet("color : red; border: 2px solid#aaaaaa; min-height : 30px; font-size : 14pt") 
            self.lineEdit_19.setText("Uncorrect Password")
            QTimer.singleShot(500,self.EmailOperationStyling)


    def SENDING_mechanics(self):
        exe = cursor2.execute(f'SELECT * FROM "{date.today()}" ').fetchall()
        exe_info = cursor2.execute(f'SELECT "Total Paid", "Paid for Hours", "Paid for Food" FROM "{date.today()}" ').fetchall()
        exe_columns_names = cursor2.execute(f'PRAGMA table_info("{date.today()}")').fetchall()
        columns_names = [name[1] for name in exe_columns_names]
        TotalYields = sum([i[0] for i in exe_info ])
        HoursCash = sum([i[1] for i in exe_info ])
        FoodCash = sum([i[2] for i in exe_info ])
        AdminEmail = cursor.execute("SELECT Email FROM Users ").fetchone()[0]

        with open('TodayYields.csv', 'w', newline='') as csv_file:
            csv.writer(csv_file).writerow(columns_names)
            csv.writer(csv_file).writerow(["" for i in range(10)])
            csv.writer(csv_file).writerows(exe)

        My_Address = 'ahmedhawater3@gmail.com'
        Password = 'hema12345'

        msg = EmailMessage()
        msg['Subject'] = f'Your yields for {date.today()}'
        msg['From'] = My_Address
        msg['To'] = AdminEmail
        msg.add_alternative(f"""
            <!DOCTYPE html>
            <html>
                <body>
                    <h2>Sent at {datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")} by {self.global_user_name}</h2>
                    <h1>Total yields for today until now is {TotalYields} EG</h1>
                    <h3>Hours Cash : {HoursCash} </h3>
                    <h3>Food Cash : {FoodCash} </h3>
                    <h3>Food Consumed : {self.UntilNOw_Food}</h3>
                </body>
            </html>
        """, subtype = 'html')

        with open('TodayYields.csv', 'rb', ) as f:
            file_data = f.read() 
            file_name = f.name

        msg.add_attachment(file_data, maintype = 'application', subtype = 'octet-stram', filename = file_name )
        try : 
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(user = My_Address, password= Password)
                smtp.send_message(msg)
        except smtplib.SMTPRecipientsRefused:
            return False
        os.remove('TodayYields.csv')
  

# Notes Methods
    def notes_show(self):
        with open('{}/users_notes/{}.txt'.format(os.getcwd().replace("\\", '/'), self.global_user_name), 'r', encoding = "utf-8") as f:
            content = f.read()
        self.plainTextEdit.setPlainText(content)      

    
    def notes_save(self):
        content = self.plainTextEdit.toPlainText()
        with open('{}/users_notes/{}.txt'.format(os.getcwd().replace("\\", '/') ,self.global_user_name), 'w', encoding = "utf-8") as f2:
            f2.write(content)

# Others Methods
    def clock(self):
        self.label_21.setText(datetime.now().time().strftime('%I:%M:%S'))
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(lambda : self.label_21.setText(datetime.now().time().strftime('%I:%M:%S')) )
        self.clock_timer.start(1000)

    def show_targrt(self):
        try:
            Nclients = str(cursor2.execute(f'SELECT clients_numbers FROM users_rates WHERE user_name = "{self.global_user_name}" AND date = "{date.today()}" ').fetchone()[0])
            self.label_22.setText(Nclients.zfill(3))
        except TypeError:
            check_rates_existant(self.global_user_name, conn2)
            self.show_targrt()

    def blabla(self):
        try:
            TotalMoney = cursor2.execute(f'SELECT total FROM users_rates WHERE user_name = "{self.global_user_name}" AND date = "{date.today()}" ').fetchone()[0]
            HoursCash = sum([i[0] for i in cursor2.execute(f'SELECT "Paid for Hours" FROM "{date.today()}" WHERE "User name" = "{self.global_user_name}"').fetchall()])
            FoodCash = sum([i[0] for i in cursor2.execute(f'SELECT "Paid for Food" FROM "{date.today()}" WHERE "User name" = "{self.global_user_name}"').fetchall()])
            self.label_23.setText(f"Total Cash : {TotalMoney}    Hours Cash : {HoursCash}    Food Cash : {FoodCash}")
        except:
            check_rates_existant(self.global_user_name, conn2)
            check_TDtable_existant(conn2)
            self.blabla()

            
        
    def widget_changes(self):
        self.label_19.setText(f'Welcome {self.global_user_name}')
        self.blabla()
        self.show_targrt()
        self.clock()
        self.notes_show()
        self.Today_Inventory()
        
        self.Mcounter = self.Pcounter = self.Tcounter = 0
        self.is_open = False
        self.is_timeout = False
        self.products_prices_list = []
        self.products_list = []
        self.single_radioBttn.setChecked(True)
        self.pause_bttn.setDisabled(True)
        self.timer = QTimer(); self.Ptimer = QTimer(); self.Ttimer = QTimer()
        self.show_foods(self.comboBox)

        self.Mcounter2 = self.Pcounter2 = self.Tcounter2 = 0
        self.is_open2 = False
        self.is_timeout2 = False        
        self.products_prices_list_2 = []
        self.products_list_2 = []
        self.single_radioBttn_2.setChecked(True)
        self.pause_bttn_2.setDisabled(True)
        self.timer_2 = QTimer(); self.Ptimer_2 = QTimer(); self.Ttimer_2 = QTimer()
        self.show_foods(self.comboBox_2)

        self.Mcounter3 = self.Pcounter3 = self.Tcounter3 = 0
        self.is_open3 = False
        self.is_timeout3 = False
        self.products_prices_list_3 = []
        self.products_list_3 = []
        self.single_radioBttn_3.setChecked(True)
        self.pause_bttn_3.setDisabled(True)
        self.timer_3 = QTimer(); self.Ptimer_3 = QTimer(); self.Ttimer_3 = QTimer()
        self.show_foods(self.comboBox_3)

        self.Mcounter4 = self.Pcounter4 = self.Tcounter4 = 0
        self.is_open4 = False
        self.is_timeout4 = False
        self.products_prices_list_4 = []
        self.products_list_4 = []
        self.single_radioBttn_4.setChecked(True)
        self.pause_bttn_4.setDisabled(True)
        self.timer_4 = QTimer(); self.Ptimer_4 = QTimer(); self.Ttimer_4 = QTimer()
        self.show_foods(self.comboBox_4)

        self.Mcounter5 = self.Pcounter5 = self.Tcounter5 = 0
        self.is_open5 = False
        self.is_timeout5 = False
        self.products_prices_list_5 = []
        self.products_list_5 = []
        self.single_radioBttn_5.setChecked(True)
        self.pause_bttn_5.setDisabled(True)
        self.timer_5 = QTimer(); self.Ptimer_5 = QTimer(); self.Ttimer_5 = QTimer()
        self.show_foods(self.comboBox_5)

        self.Mcounter6 = self.Pcounter6 = self.Tcounter6 = 0
        self.is_open6 = False
        self.is_timeout6 = False
        self.products_prices_list_6 = []
        self.products_list_6 = []
        self.single_radioBttn_6.setChecked(True)
        self.pause_bttn_6.setDisabled(True)
        self.timer_6 = QTimer(); self.Ptimer_6 = QTimer(); self.Ttimer_6 = QTimer()
        self.show_foods(self.comboBox_6)

        self.Mcounter7 = self.Pcounter7 = self.Tcounter7 = 0
        self.is_open7 = False
        self.is_timeout7 = False
        self.products_prices_list_7 = []
        self.products_list_7 = []
        self.single_radioBttn_7.setChecked(True)
        self.pause_bttn_7.setDisabled(True)
        self.timer_7 = QTimer(); self.Ptimer_7 = QTimer(); self.Ttimer_7 = QTimer()
        self.show_foods(self.comboBox_7)

        self.Mcounter8 = self.Pcounter8 = self.Tcounter8 = 0
        self.is_open8 = False
        self.is_timeout8 = False
        self.products_prices_list_8 = []
        self.products_list_8 = []
        self.single_radioBttn_8.setChecked(True)
        self.pause_bttn_8.setDisabled(True)
        self.timer_8 = QTimer(); self.Ptimer_8 = QTimer(); self.Ttimer_8 = QTimer()
        self.show_foods(self.comboBox_8)

        self.Mcounter9 = self.Pcounter9 = self.Tcounter9 = 0
        self.is_open9 = False
        self.is_timeout9 = False
        self.products_prices_list_9 = []
        self.products_list_9 = []
        self.single_radioBttn_9.setChecked(True)
        self.pause_bttn_9.setDisabled(True)
        self.timer_9 = QTimer(); self.Ptimer_9 = QTimer(); self.Ttimer_9 = QTimer()
        self.show_foods(self.comboBox_9)

        self.Mcounter10 = self.Pcounter10 = self.Tcounter10 = 0
        self.is_open10 = False
        self.is_timeout10 = False
        self.products_prices_list_10 = []
        self.products_list_10 = []
        self.single_radioBttn_10.setChecked(True)
        self.pause_bttn_10.setDisabled(True)
        self.timer_10 = QTimer(); self.Ptimer_10 = QTimer(); self.Ttimer_10 = QTimer()
        self.show_foods(self.comboBox_10)                

        self.Mcounter11 = self.Pcounter11 = self.Tcounter11 = 0
        self.is_open11 = False
        self.is_timeout11 = False
        self.products_prices_list_11 = []
        self.products_list_11 = []
        self.single_radioBttn_11.setChecked(True)
        self.pause_bttn_11.setDisabled(True)
        self.timer_11 = QTimer(); self.Ptimer_11 = QTimer(); self.Ttimer_11 = QTimer()
        self.show_foods(self.comboBox_11)

        self.Mcounter12 = self.Pcounter12 = self.Tcounter12 = 0
        self.is_open12 = False
        self.is_timeout12 = False
        self.products_prices_list_12 = []
        self.products_list_12 = []
        self.single_radioBttn_12.setChecked(True)
        self.pause_bttn_12.setDisabled(True)
        self.timer_12 = QTimer(); self.Ptimer_12 = QTimer(); self.Ttimer_12 = QTimer()
        self.show_foods(self.comboBox_12)

        self.Mcounter13 = self.Pcounter13 = self.Tcounter13 = 0
        self.is_open13 = False
        self.is_timeout13 = False
        self.products_prices_list_13 = []
        self.products_list_13 = []
        self.single_radioBttn_13.setChecked(True)
        self.pause_bttn_13.setDisabled(True)
        self.timer_13 = QTimer(); self.Ptimer_13 = QTimer(); self.Ttimer_13 = QTimer()
        self.show_foods(self.comboBox_13)

        self.Mcounter14 = self.Pcounter14 = self.Tcounter14 = 0
        self.is_open14 = False
        self.is_timeout14 = False
        self.products_prices_list_14 = []
        self.products_list_14 = []
        self.single_radioBttn_14.setChecked(True)
        self.pause_bttn_14.setDisabled(True)
        self.timer_14 = QTimer(); self.Ptimer_14 = QTimer(); self.Ttimer_14 = QTimer()
        self.show_foods(self.comboBox_14)

        self.Mcounter15 = self.Pcounter15 = self.Tcounter15 = 0
        self.is_open15 = False
        self.is_timeout15 = False
        self.products_prices_list_15 = []
        self.products_list_15 = []
        self.single_radioBttn_15.setChecked(True)
        self.pause_bttn_15.setDisabled(True)
        self.timer_15 = QTimer(); self.Ptimer_15 = QTimer(); self.Ttimer_15 = QTimer()
        self.show_foods(self.comboBox_15)

        self.Mcounter16 = self.Pcounter16 = self.Tcounter16 = 0
        self.is_open16 = False
        self.is_timeout16 = False
        self.products_prices_list_16 = []
        self.products_list_16 = []
        self.single_radioBttn_16.setChecked(True)
        self.pause_bttn_16.setDisabled(True)
        self.timer_16 = QTimer(); self.Ptimer_16 = QTimer(); self.Ttimer_16 = QTimer()
        self.show_foods(self.comboBox_16)

        self.Mcounter17 = self.Pcounter17 = self.Tcounter17 = 0
        self.is_open17 = False
        self.is_timeout17 = False
        self.products_prices_list_17 = []
        self.products_list_17 = []
        self.single_radioBttn_17.setChecked(True)
        self.pause_bttn_17.setDisabled(True)
        self.timer_17 = QTimer(); self.Ptimer_17 = QTimer(); self.Ttimer_17 = QTimer()
        self.show_foods(self.comboBox_17)
        
        self.Mcounter18 = self.Pcounter18 = self.Tcounter18 = 0
        self.is_open18 = False
        self.is_timeout18 = False
        self.products_prices_list_18 = []
        self.products_list_18 = []
        self.single_radioBttn_18.setChecked(True)
        self.pause_bttn_18.setDisabled(True)
        self.timer_18 = QTimer(); self.Ptimer_18 = QTimer(); self.Ttimer_18 = QTimer()
        self.show_foods(self.comboBox_18)


    def device_counter(self, special):
        if special == 1 :
            self.Mcounter = self.Mcounter + 1
        elif special == 0 :
            self.Mcounter = 0
    def device_Pcounter(self, special):
        if special == 1 :
            self.Pcounter = self.Pcounter + 1
        elif special == 0 :
            self.Pcounter = 0
    def device_Tcounter(self, special):
        if special == 1 :
            self.Tcounter = self.Tcounter + 1
        elif special == 0 :
            self.Tcounter = 0             
    def device_open(self, special):
        if special == 1 :
            self.is_open = True
        elif special == 0 :
            self.is_open = False
    def set_timeout(self, special):
        if special == 1 :
            self.is_timeout = True
        elif special == 0 :
            self.is_timeout = False        
    def clear(self):
        self.products_list.clear()
    # ------------------------------
    def device2_counter(self, special):
        if special == 1 :
            self.Mcounter2 = self.Mcounter2 + 1
        elif special == 0 :
            self.Mcounter2 = 0
    def device2_Pcounter(self, special):
        if special == 1 :
            self.Pcounter2 = self.Pcounter2 + 1
        elif special == 0 :
            self.Pcounter2 = 0
    def device2_Tcounter(self, special):
        if special == 1 :
            self.Tcounter2 = self.Tcounter2 + 1
        elif special == 0 :
            self.Tcounter2 = 0             
    def device2_open(self, special):
        if special == 1 :
            self.is_open2 = True
        elif special == 0 :
            self.is_open2 = False
    def set_timeout2(self, special):
        if special == 1 :
            self.is_timeout2 = True
        elif special == 0 :
            self.is_timeout2 = False                 
    def clear2(self):
        self.products_list_2.clear()
    # -------------------------------
    def device3_counter(self, special):
        if special == 1 :
            self.Mcounter3 = self.Mcounter3 + 1
        elif special == 0 :
            self.Mcounter3 = 0
    def device3_Pcounter(self, special):
        if special == 1 :
            self.Pcounter3 = self.Pcounter3 + 1
        elif special == 0 :
            self.Pcounter3 = 0
    def device3_Tcounter(self, special):
        if special == 1 :
            self.Tcounter3 = self.Tcounter3 + 1
        elif special == 0 :
            self.Tcounter3 = 0              
    def device3_open(self, special):
        if special == 1 :
            self.is_open3 = True
        elif special == 0 :
            self.is_open3 = False
    def set_timeout3(self, special):
        if special == 1 :
            self.is_timeout3 = True
        elif special == 0 :
            self.is_timeout3 = False             
    def clear3(self):
        self.products_list_3.clear()
    # -------------------------------
    def device4_counter(self, special):
        if special == 1 :
            self.Mcounter4 = self.Mcounter4 + 1
        elif special == 0 :
            self.Mcounter4 = 0
    def device4_Pcounter(self, special):
        if special == 1 :
            self.Pcounter4 = self.Pcounter4 + 1
        elif special == 0 :
            self.Pcounter4 = 0
    def device4_Tcounter(self, special):
        if special == 1 :
            self.Tcounter4 = self.Tcounter4 + 1
        elif special == 0 :
            self.Tcounter4 = 0              
    def device4_open(self, special):
        if special == 1 :
            self.is_open4 = True
        elif special == 0 :
            self.is_open4 = False
    def set_timeout4(self, special):
        if special == 1 :
            self.is_timeout4 = True
        elif special == 0 :
            self.is_timeout4 = False             
    def clear4(self):
        self.products_list_4.clear()
    # -------------------------------
    def device5_counter(self, special):
        if special == 1 :
            self.Mcounter5 = self.Mcounter5 + 1
        elif special == 0 :
            self.Mcounter5 = 0
    def device5_Pcounter(self, special):
        if special == 1 :
            self.Pcounter5 = self.Pcounter5 + 1
        elif special == 0 :
            self.Pcounter5 = 0
    def device5_Tcounter(self, special):
        if special == 1 :
            self.Tcounter5 = self.Tcounter5 + 1
        elif special == 0 :
            self.Tcounter5 = 0              
    def device5_open(self, special):
        if special == 1 :
            self.is_open5 = True
        elif special == 0 :
            self.is_open5 = False
    def set_timeout5(self, special):
        if special == 1 :
            self.is_timeout5 = True
        elif special == 0 :
            self.is_timeout5 = False             
    def clear5(self):
        self.products_list_5.clear()
    # -------------------------------
    def device6_counter(self, special):
        if special == 1 :
            self.Mcounter6 = self.Mcounter6 + 1
        elif special == 0 :
            self.Mcounter6 = 0
    def device6_Pcounter(self, special):
        if special == 1 :
            self.Pcounter6 = self.Pcounter6 + 1
        elif special == 0 :
            self.Pcounter6 = 0
    def device6_Tcounter(self, special):
        if special == 1 :
            self.Tcounter6 = self.Tcounter6 + 1
        elif special == 0 :
            self.Tcounter6 = 0              
    def device6_open(self, special):
        if special == 1 :
            self.is_open6 = True
        elif special == 0 :
            self.is_open6 = False
    def set_timeout6(self, special):
        if special == 1 :
            self.is_timeout6 = True
        elif special == 0 :
            self.is_timeout6 = False             
    def clear6(self):
        self.products_list_6.clear()
    # -------------------------------
    def device7_counter(self, special):
        if special == 1 :
            self.Mcounter7 = self.Mcounter7 + 1
        elif special == 0 :
            self.Mcounter7 = 0
    def device7_Pcounter(self, special):
        if special == 1 :
            self.Pcounter7 = self.Pcounter7 + 1
        elif special == 0 :
            self.Pcounter7 = 0
    def device7_Tcounter(self, special):
        if special == 1 :
            self.Tcounter7 = self.Tcounter7 + 1
        elif special == 0 :
            self.Tcounter7 = 0              
    def device7_open(self, special):
        if special == 1 :
            self.is_open7 = True
        elif special == 0 :
            self.is_open7 = False
    def set_timeout7(self, special):
        if special == 1 :
            self.is_timeout7 = True
        elif special == 0 :
            self.is_timeout7 = False             
    def clear7(self):
        self.products_list_7.clear()
    # -------------------------------
    def device8_counter(self, special):
        if special == 1 :
            self.Mcounter8 = self.Mcounter8 + 1
        elif special == 0 :
            self.Mcounter8 = 0
    def device8_Pcounter(self, special):
        if special == 1 :
            self.Pcounter8 = self.Pcounter8 + 1
        elif special == 0 :
            self.Pcounter8 = 0
    def device8_Tcounter(self, special):
        if special == 1 :
            self.Tcounter8 = self.Tcounter8 + 1
        elif special == 0 :
            self.Tcounter8 = 0              
    def device8_open(self, special):
        if special == 1 :
            self.is_open8 = True
        elif special == 0 :
            self.is_open8 = False
    def set_timeout8(self, special):
        if special == 1 :
            self.is_timeout8 = True
        elif special == 0 :
            self.is_timeout8 = False             
    def clear8(self):
        self.products_list_8.clear()
    # -------------------------------
    def device9_counter(self, special):
        if special == 1 :
            self.Mcounter9 = self.Mcounter9 + 1
        elif special == 0 :
            self.Mcounter9 = 0
    def device9_Pcounter(self, special):
        if special == 1 :
            self.Pcounter9 = self.Pcounter9 + 1
        elif special == 0 :
            self.Pcounter9 = 0
    def device9_Tcounter(self, special):
        if special == 1 :
            self.Tcounter9 = self.Tcounter9 + 1
        elif special == 0 :
            self.Tcounter9 = 0              
    def device9_open(self, special):
        if special == 1 :
            self.is_open9 = True
        elif special == 0 :
            self.is_open9 = False
    def set_timeout9(self, special):
        if special == 1 :
            self.is_timeout9 = True
        elif special == 0 :
            self.is_timeout9 = False             
    def clear9(self):
        self.products_list_9.clear()
    # -------------------------------
    def device10_counter(self, special):
        if special == 1 :
            self.Mcounter10 = self.Mcounter10 + 1
        elif special == 0 :
            self.Mcounter10 = 0
    def device10_Pcounter(self, special):
        if special == 1 :
            self.Pcounter10 = self.Pcounter10 + 1
        elif special == 0 :
            self.Pcounter10 = 0
    def device10_Tcounter(self, special):
        if special == 1 :
            self.Tcounter10 = self.Tcounter10 + 1
        elif special == 0 :
            self.Tcounter10 = 0              
    def device10_open(self, special):
        if special == 1 :
            self.is_open10 = True
        elif special == 0 :
            self.is_open10 = False
    def set_timeout10(self, special):
        if special == 1 :
            self.is_timeout10 = True
        elif special == 0 :
            self.is_timeout10 = False             
    def clear10(self):
        self.products_list_10.clear()
    # -------------------------------
    def device11_counter(self, special):
        if special == 1 :
            self.Mcounter11 = self.Mcounter11 + 1
        elif special == 0 :
            self.Mcounter11 = 0
    def device11_Pcounter(self, special):
        if special == 1 :
            self.Pcounter11 = self.Pcounter11 + 1
        elif special == 0 :
            self.Pcounter11 = 0
    def device11_Tcounter(self, special):
        if special == 1 :
            self.Tcounter11 = self.Tcounter11 + 1
        elif special == 0 :
            self.Tcounter11 = 0              
    def device11_open(self, special):
        if special == 1 :
            self.is_open11 = True
        elif special == 0 :
            self.is_open11 = False
    def set_timeout11(self, special):
        if special == 1 :
            self.is_timeout11 = True
        elif special == 0 :
            self.is_timeout11 = False             
    def clear11(self):
        self.products_list_11.clear()
    # -------------------------------
    def device12_counter(self, special):
        if special == 1 :
            self.Mcounter12 = self.Mcounter12 + 1
        elif special == 0 :
            self.Mcounter12 = 0
    def device12_Pcounter(self, special):
        if special == 1 :
            self.Pcounter12 = self.Pcounter12 + 1
        elif special == 0 :
            self.Pcounter12 = 0
    def device12_Tcounter(self, special):
        if special == 1 :
            self.Tcounter12 = self.Tcounter12 + 1
        elif special == 0 :
            self.Tcounter12 = 0          
    def device12_open(self, special):
        if special == 1 :
            self.is_open12 = True
        elif special == 0 :
            self.is_open12 = False
    def set_timeout12(self, special):
        if special == 1 :
            self.is_timeout12 = True
        elif special == 0 :
            self.is_timeout12 = False             
    def clear12(self):
        self.products_list_12.clear()        
    # -------------------------------
    def device13_counter(self, special):
        if special == 1 :
            self.Mcounter13 = self.Mcounter13 + 1
        elif special == 0 :
            self.Mcounter13 = 0
    def device13_Pcounter(self, special):
        if special == 1 :
            self.Pcounter13 = self.Pcounter13 + 1
        elif special == 0 :
            self.Pcounter13 = 0
    def device13_Tcounter(self, special):
        if special == 1 :
            self.Tcounter13 = self.Tcounter13 + 1
        elif special == 0 :
            self.Tcounter13 = 0              
    def device13_open(self, special):
        if special == 1 :
            self.is_open13 = True
        elif special == 0 :
            self.is_open13 = False
    def set_timeout13(self, special):
        if special == 1 :
            self.is_timeout13 = True
        elif special == 0 :
            self.is_timeout13 = False             
    def clear13(self):
        self.products_list_13.clear()
    # -------------------------------
    def device14_counter(self, special):
        if special == 1 :
            self.Mcounter14 = self.Mcounter14 + 1
        elif special == 0 :
            self.Mcounter14 = 0
    def device14_Pcounter(self, special):
        if special == 1 :
            self.Pcounter14 = self.Pcounter14 + 1
        elif special == 0 :
            self.Pcounter14 = 0
    def device14_Tcounter(self, special):
        if special == 1 :
            self.Tcounter14 = self.Tcounter14 + 1
        elif special == 0 :
            self.Tcounter14 = 0              
    def device14_open(self, special):
        if special == 1 :
            self.is_open14 = True
        elif special == 0 :
            self.is_open14 = False
    def set_timeout14(self, special):
        if special == 1 :
            self.is_timeout14 = True
        elif special == 0 :
            self.is_timeout14 = False             
    def clear14(self):
        self.products_list_14.clear()
    # -------------------------------
    def device15_counter(self, special):
        if special == 1 :
            self.Mcounter15 = self.Mcounter15 + 1
        elif special == 0 :
            self.Mcounter15 = 0
    def device15_Pcounter(self, special):
        if special == 1 :
            self.Pcounter15 = self.Pcounter15 + 1
        elif special == 0 :
            self.Pcounter15 = 0
    def device15_Tcounter(self, special):
        if special == 1 :
            self.Tcounter15 = self.Tcounter15 + 1
        elif special == 0 :
            self.Tcounter15 = 0              
    def device15_open(self, special):
        if special == 1 :
            self.is_open15 = True
        elif special == 0 :
            self.is_open15 = False
    def set_timeout15(self, special):
        if special == 1 :
            self.is_timeout15 = True
        elif special == 0 :
            self.is_timeout15 = False             
    def clear15(self):
        self.products_list_15.clear()
    # -------------------------------
    def device16_counter(self, special):
        if special == 1 :
            self.Mcounter16 = self.Mcounter16 + 1
        elif special == 0 :
            self.Mcounter16 = 0
    def device16_Pcounter(self, special):
        if special == 1 :
            self.Pcounter16 = self.Pcounter16 + 1
        elif special == 0 :
            self.Pcounter16 = 0
    def device16_Tcounter(self, special):
        if special == 1 :
            self.Tcounter16 = self.Tcounter16 + 1
        elif special == 0 :
            self.Tcounter16 = 0              
    def device16_open(self, special):
        if special == 1 :
            self.is_open16 = True
        elif special == 0 :
            self.is_open16 = False
    def set_timeout16(self, special):
        if special == 1 :
            self.is_timeout16 = True
        elif special == 0 :
            self.is_timeout16 = False             
    def clear16(self):
        self.products_list_16.clear()
    # -------------------------------
    def device17_counter(self, special):
        if special == 1 :
            self.Mcounter17 = self.Mcounter17 + 1
        elif special == 0 :
            self.Mcounter17 = 0
    def device17_Pcounter(self, special):
        if special == 1 :
            self.Pcounter17 = self.Pcounter17 + 1
        elif special == 0 :
            self.Pcounter17 = 0
    def device17_Tcounter(self, special):
        if special == 1 :
            self.Tcounter17 = self.Tcounter17 + 1
        elif special == 0 :
            self.Tcounter17 = 0              
    def device17_open(self, special):
        if special == 1 :
            self.is_open17 = True
        elif special == 0 :
            self.is_open17 = False
    def set_timeout17(self, special):
        if special == 1 :
            self.is_timeout17 = True
        elif special == 0 :
            self.is_timeout17 = False             
    def clear17(self):
        self.products_list_17.clear()
    # -------------------------------
    def device18_counter(self, special):
        if special == 1 :
            self.Mcounter18 = self.Mcounter18 + 1
        elif special == 0 :
            self.Mcounter18 = 0
    def device18_Pcounter(self, special):
        if special == 1 :
            self.Pcounter18 = self.Pcounter18 + 1
        elif special == 0 :
            self.Pcounter18 = 0
    def device18_Tcounter(self, special):
        if special == 1 :
            self.Tcounter18 = self.Tcounter18 + 1
        elif special == 0 :
            self.Tcounter18 = 0                    
    def device18_open(self, special):
        if special == 1 :
            self.is_open18 = True
        elif special == 0 :
            self.is_open18 = False
    def set_timeout18(self, special):
        if special == 1 :
            self.is_timeout18 = True
        elif special == 0 :
            self.is_timeout18 = False             
    def clear18(self):
        self.products_list_18.clear()



    def clicked_buttons(self):
        self.pushButton.clicked.connect(self.notes_save)
        self.pushButton_2.clicked.connect(self.sending)


        """
                    Change the "Super Dober number" for each device EXCEPT (self.multi2.radioButton)   

           << Super Dober number : is the unique number for each [method, attr ,label, button, lineEdit, etc] >>

    explaination : using setters methods to change the value of the counter and the is_open attrs.

    more explaination : replacing  // Mcounter +=1 & Mcounter = 0 // with the setter method "device_counter"
                                   // is_open = False & is_open = True // with the setter method "device_open" 

    more more explaination : i did this cause i coould  not change the counter & is_open vlaue by passing it as an argument in the main methods
    of the program and cause i could not use {- + =} operators to modify the counter value , and i had to write 175 lines of code for every device.
    so i came out with the idea of using setters. its a little bit complicated but i will make it clear for you now :

        i had put functions parameters in the main program methods, and these functions are going to be called using lambda
        and these function "setters" are going to do all the work for me .

        I had made 2 setters functions for each device starting from the line " 166 ".
        
        """
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 1 st $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn.clicked.connect(lambda : self.add(self.spinBox, self.listWidget, self.comboBox, self.products_list))

        self.delete_bttn.clicked.connect(lambda : self.delete_list_item(self.listWidget, self.products_list))

        self.start_time_bttn.clicked.connect(lambda : self.timer_execution(self.timeEdit, self.timer, self.Ptimer,
            [self.start_time_bttn, self.start_open_time_bttn, self.pause_bttn], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit, self.timer, self.Ttimer, self.label,
                [self.start_time_bttn, self.start_open_time_bttn, self.pause_bttn],
                 lambda : self.device_counter(1), lambda : self.set_timeout(1), lambda : self.device_Tcounter(1) )))

        self.pause_bttn.clicked.connect(lambda : self.pause_time( self.timer, self.Ptimer,
            [self.start_time_bttn, self.start_open_time_bttn, self.pause_bttn], self.is_open, lambda : self.device_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn.clicked.connect(lambda : self.submit(self.Mcounter, self.Pcounter, self.Tcounter,
                                            self.timer, self.Ptimer, self.Ttimer, self.timeEdit, self.groupBox,
            [self.single_radioBttn, self.multi1_radioBttn, self.multi2_radioBttn], self.lineEdit, self.listWidget, 
            self.products_list, self.products_prices_list, self.label, [self.start_time_bttn, self.start_open_time_bttn],
            lambda : self.device_counter(0), lambda : self.device_open(0), self.clear, self.is_timeout, lambda : self.set_timeout(0),
            lambda : self.device_Pcounter(0), lambda : self.device_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn.clicked.connect(lambda : self.cancel(self.products_prices_list, self.listWidget, self.lineEdit, self.label, self.timeEdit, 
        [self.start_time_bttn, self.start_open_time_bttn, self.pause_bttn], [self.single_radioBttn, self.multi1_radioBttn, self.multi2_radioBttn],
        lambda : self.device_counter(0), lambda : self.device_Pcounter(0), lambda : self.device_Tcounter(0), self.clear,
        lambda : self.device_open(0), lambda : self.set_timeout(0), self.timer, self.Ptimer, self.Ttimer, self.groupBox))

        self.start_open_time_bttn.clicked.connect(lambda : self.open_time_execution(self.timer, self.Ptimer, self.timeEdit, 
            [self.start_time_bttn, self.start_open_time_bttn, self.pause_bttn], 
                lambda : self.open_time_mechanics(self.timeEdit, lambda : self.device_counter(1) ), lambda : self.device_open(1) ) )
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 2 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_2.clicked.connect(lambda : self.add(self.spinBox_2, self.listWidget_2, self.comboBox_2, self.products_list_2))

        self.delete_bttn_2.clicked.connect(lambda : self.delete_list_item(self.listWidget_2, self.products_list_2))

        self.start_time_bttn_2.clicked.connect(lambda : self.timer_execution(self.timeEdit_2, self.timer_2, self.Ptimer_2,
            [self.start_time_bttn_2, self.start_open_time_bttn_2, self.pause_bttn_2], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_2, self.timer_2, self.Ttimer_2, self.label_2,
                [self.start_time_bttn_2, self.start_open_time_bttn_2, self.pause_bttn_2],
                 lambda : self.device2_counter(1), lambda : self.set_timeout2(1), lambda : self.device2_Tcounter(1)  )))

        self.pause_bttn_2.clicked.connect(lambda : self.pause_time( self.timer_2, self.Ptimer_2,
            [self.start_time_bttn_2, self.start_open_time_bttn_2, self.pause_bttn_2], self.is_open2, lambda : self.device2_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_2.clicked.connect(lambda : self.submit(self.Mcounter2 ,self.Pcounter2, self.Tcounter2,self.timer_2,
        self.Ptimer_2, self.Ttimer_2, self.timeEdit_2, self.groupBox_2,
            [self.single_radioBttn_2, self.multi1_radioBttn_2, self.multi2_radioBttn_2], self.lineEdit_2, self.listWidget_2, 
            self.products_list_2, self.products_prices_list_2, self.label_2, [self.start_time_bttn_2, self.start_open_time_bttn_2],
            lambda : self.device2_counter(0), lambda : self.device2_open(0), self.clear2 , self.is_timeout2, lambda : self.set_timeout2(0),
            lambda : self.device2_Pcounter(0), lambda : self.device2_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_2.clicked.connect(lambda : self.cancel(self.products_prices_list_2, self.listWidget_2, self.lineEdit_2, self.label_2, self.timeEdit_2, 
        [self.start_time_bttn_2, self.start_open_time_bttn_2, self.pause_bttn_2], [self.single_radioBttn_2, self.multi1_radioBttn_2, self.multi2_radioBttn_2],
        lambda : self.device2_counter(0), lambda : self.device2_Pcounter(0), lambda : self.device2_Tcounter(0), self.clear2,
        lambda : self.device2_open(0), lambda : self.set_timeout2(0), self.timer_2, self.Ptimer_2, self.Ttimer_2, self.groupBox_2))        

        self.start_open_time_bttn_2.clicked.connect(lambda : self.open_time_execution(self.timer_2, self.Ptimer_2, self.timeEdit_2, 
            [self.start_time_bttn_2, self.start_open_time_bttn_2, self.pause_bttn_2], 
                lambda : self.open_time_mechanics(self.timeEdit_2, lambda : self.device2_counter(1) ), lambda : self.device2_open(1) ) ) 
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 3 rd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_3.clicked.connect(lambda : self.add(self.spinBox_3, self.listWidget_3, self.comboBox_3, self.products_list_3))

        self.delete_bttn_3.clicked.connect(lambda : self.delete_list_item(self.listWidget_3, self.products_list_3))

        self.start_time_bttn_3.clicked.connect(lambda : self.timer_execution(self.timeEdit_3, self.timer_3, self.Ptimer_3,
            [self.start_time_bttn_3, self.start_open_time_bttn_3, self.pause_bttn_3], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_3, self.timer_3, self.Ttimer_3, self.label_3,
                [self.start_time_bttn_3, self.start_open_time_bttn_3, self.pause_bttn_3],
                 lambda : self.device3_counter(1), lambda : self.set_timeout3(1), lambda : self.device3_Tcounter(1)  )))

        self.pause_bttn_3.clicked.connect(lambda : self.pause_time( self.timer_3, self.Ptimer_3,
            [self.start_time_bttn_3, self.start_open_time_bttn_3, self.pause_bttn_3], self.is_open3, lambda : self.device3_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_3.clicked.connect(lambda : self.submit(self.Mcounter3 ,self.Pcounter3, self.Tcounter3,self.timer_3,
        self.Ptimer_3, self.Ttimer_3, self.timeEdit_3, self.groupBox_3,
            [self.single_radioBttn_3, self.multi1_radioBttn_3, self.multi2_radioBttn_3], self.lineEdit_3, self.listWidget_3, 
            self.products_list_3, self.products_prices_list_3, self.label_3, [self.start_time_bttn_3, self.start_open_time_bttn_3],
            lambda : self.device3_counter(0), lambda : self.device3_open(0), self.clear3 , self.is_timeout3, lambda : self.set_timeout3(0),
            lambda : self.device3_Pcounter(0), lambda : self.device3_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_3.clicked.connect(lambda : self.cancel(self.products_prices_list_3, self.listWidget_3, self.lineEdit_3, self.label_3, self.timeEdit_3, 
        [self.start_time_bttn_3, self.start_open_time_bttn_3, self.pause_bttn_3], [self.single_radioBttn_3, self.multi1_radioBttn_3, self.multi2_radioBttn_3],
        lambda : self.device3_counter(0), lambda : self.device3_Pcounter(0), lambda : self.device3_Tcounter(0), self.clear3,
        lambda : self.device3_open(0), lambda : self.set_timeout3(0), self.timer_3, self.Ptimer_3, self.Ttimer_3, self.groupBox_3))        

        self.start_open_time_bttn_3.clicked.connect(lambda : self.open_time_execution(self.timer_3, self.Ptimer_3, self.timeEdit_3, 
            [self.start_time_bttn_3, self.start_open_time_bttn_3, self.pause_bttn_3], 
                lambda : self.open_time_mechanics(self.timeEdit_3, lambda : self.device3_counter(1) ), lambda : self.device3_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 4 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_4.clicked.connect(lambda : self.add(self.spinBox_4, self.listWidget_4, self.comboBox_4, self.products_list_4))

        self.delete_bttn_4.clicked.connect(lambda : self.delete_list_item(self.listWidget_4, self.products_list_4))

        self.start_time_bttn_4.clicked.connect(lambda : self.timer_execution(self.timeEdit_4, self.timer_4, self.Ptimer_4,
            [self.start_time_bttn_4, self.start_open_time_bttn_4, self.pause_bttn_4], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_4, self.timer_4, self.Ttimer_4, self.label_4,
                [self.start_time_bttn_4, self.start_open_time_bttn_4, self.pause_bttn_4],
                 lambda : self.device4_counter(1), lambda : self.set_timeout4(1), lambda : self.device4_Tcounter(1)  )))

        self.pause_bttn_4.clicked.connect(lambda : self.pause_time( self.timer_4, self.Ptimer_4,
            [self.start_time_bttn_4, self.start_open_time_bttn_4, self.pause_bttn_4], self.is_open4, lambda : self.device4_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_4.clicked.connect(lambda : self.submit(self.Mcounter4 ,self.Pcounter4, self.Tcounter4,self.timer_4,
        self.Ptimer_4, self.Ttimer_4, self.timeEdit_4, self.groupBox_4,
            [self.single_radioBttn_4, self.multi1_radioBttn_4, self.multi2_radioBttn_4], self.lineEdit_4, self.listWidget_4, 
            self.products_list_4, self.products_prices_list_4, self.label_4, [self.start_time_bttn_4, self.start_open_time_bttn_4],
            lambda : self.device4_counter(0), lambda : self.device4_open(0), self.clear4 , self.is_timeout4, lambda : self.set_timeout4(0),
            lambda : self.device4_Pcounter(0), lambda : self.device4_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_4.clicked.connect(lambda : self.cancel(self.products_prices_list_4, self.listWidget_4, self.lineEdit_4, self.label_4, self.timeEdit_4, 
        [self.start_time_bttn_4, self.start_open_time_bttn_4, self.pause_bttn_4], [self.single_radioBttn_4, self.multi1_radioBttn_4, self.multi2_radioBttn_4],
        lambda : self.device4_counter(0), lambda : self.device4_Pcounter(0), lambda : self.device4_Tcounter(0), self.clear4,
        lambda : self.device4_open(0), lambda : self.set_timeout4(0), self.timer_4, self.Ptimer_4, self.Ttimer_4, self.groupBox_4))        

        self.start_open_time_bttn_4.clicked.connect(lambda : self.open_time_execution(self.timer_4, self.Ptimer_4, self.timeEdit_4, 
            [self.start_time_bttn_4, self.start_open_time_bttn_4, self.pause_bttn_4], 
                lambda : self.open_time_mechanics(self.timeEdit_4, lambda : self.device4_counter(1) ), lambda : self.device4_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 5 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_5.clicked.connect(lambda : self.add(self.spinBox_5, self.listWidget_5, self.comboBox_5, self.products_list_5))

        self.delete_bttn_5.clicked.connect(lambda : self.delete_list_item(self.listWidget_5, self.products_list_5))

        self.start_time_bttn_5.clicked.connect(lambda : self.timer_execution(self.timeEdit_5, self.timer_5, self.Ptimer_5,
            [self.start_time_bttn_5, self.start_open_time_bttn_5, self.pause_bttn_5], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_5, self.timer_5, self.Ttimer_5, self.label_5,
                [self.start_time_bttn_5, self.start_open_time_bttn_5, self.pause_bttn_5],
                 lambda : self.device5_counter(1), lambda : self.set_timeout5(1), lambda : self.device5_Tcounter(1)  )))

        self.pause_bttn_5.clicked.connect(lambda : self.pause_time( self.timer_5, self.Ptimer_5,
            [self.start_time_bttn_5, self.start_open_time_bttn_5, self.pause_bttn_5], self.is_open5, lambda : self.device5_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_5.clicked.connect(lambda : self.submit(self.Mcounter5 ,self.Pcounter5, self.Tcounter5,self.timer_5,
        self.Ptimer_5, self.Ttimer_5, self.timeEdit_5, self.groupBox_5,
            [self.single_radioBttn_5, self.multi1_radioBttn_5, self.multi2_radioBttn_5], self.lineEdit_5, self.listWidget_5, 
            self.products_list_5, self.products_prices_list_5, self.label_5, [self.start_time_bttn_5, self.start_open_time_bttn_5],
            lambda : self.device5_counter(0), lambda : self.device5_open(0), self.clear5 , self.is_timeout5, lambda : self.set_timeout5(0),
            lambda : self.device5_Pcounter(0), lambda : self.device5_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_5.clicked.connect(lambda : self.cancel(self.products_prices_list_5, self.listWidget_5, self.lineEdit_5, self.label_5, self.timeEdit_5, 
        [self.start_time_bttn_5, self.start_open_time_bttn_5, self.pause_bttn_5], [self.single_radioBttn_5, self.multi1_radioBttn_5, self.multi2_radioBttn_5],
        lambda : self.device5_counter(0), lambda : self.device5_Pcounter(0), lambda : self.device5_Tcounter(0), self.clear5,
        lambda : self.device5_open(0), lambda : self.set_timeout5(0), self.timer_5, self.Ptimer_5, self.Ttimer_5, self.groupBox_5))        

        self.start_open_time_bttn_5.clicked.connect(lambda : self.open_time_execution(self.timer_5, self.Ptimer_5, self.timeEdit_5, 
            [self.start_time_bttn_5, self.start_open_time_bttn_5, self.pause_bttn_5], 
                lambda : self.open_time_mechanics(self.timeEdit_5, lambda : self.device5_counter(1) ), lambda : self.device5_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 6 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_6.clicked.connect(lambda : self.add(self.spinBox_6, self.listWidget_6, self.comboBox_6, self.products_list_6))

        self.delete_bttn_6.clicked.connect(lambda : self.delete_list_item(self.listWidget_6, self.products_list_6))

        self.start_time_bttn_6.clicked.connect(lambda : self.timer_execution(self.timeEdit_6, self.timer_6, self.Ptimer_6,
            [self.start_time_bttn_6, self.start_open_time_bttn_6, self.pause_bttn_6], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_6, self.timer_6, self.Ttimer_6, self.label_6,
                [self.start_time_bttn_6, self.start_open_time_bttn_6, self.pause_bttn_6],
                 lambda : self.device6_counter(1), lambda : self.set_timeout6(1), lambda : self.device6_Tcounter(1)  )))

        self.pause_bttn_6.clicked.connect(lambda : self.pause_time( self.timer_6, self.Ptimer_6,
            [self.start_time_bttn_6, self.start_open_time_bttn_6, self.pause_bttn_6], self.is_open6, lambda : self.device6_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_6.clicked.connect(lambda : self.submit(self.Mcounter6 ,self.Pcounter6, self.Tcounter6,self.timer_6,
        self.Ptimer_6, self.Ttimer_6, self.timeEdit_6, self.groupBox_6,
            [self.single_radioBttn_6, self.multi1_radioBttn_6, self.multi2_radioBttn_6], self.lineEdit_6, self.listWidget_6, 
            self.products_list_6, self.products_prices_list_6, self.label_6, [self.start_time_bttn_6, self.start_open_time_bttn_6],
            lambda : self.device6_counter(0), lambda : self.device6_open(0), self.clear6 , self.is_timeout6, lambda : self.set_timeout6(0),
            lambda : self.device6_Pcounter(0), lambda : self.device6_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_6.clicked.connect(lambda : self.cancel(self.products_prices_list_6, self.listWidget_6, self.lineEdit_6, self.label_6, self.timeEdit_6, 
        [self.start_time_bttn_6, self.start_open_time_bttn_6, self.pause_bttn_6], [self.single_radioBttn_6, self.multi1_radioBttn_6, self.multi2_radioBttn_6],
        lambda : self.device6_counter(0), lambda : self.device6_Pcounter(0), lambda : self.device6_Tcounter(0), self.clear6,
        lambda : self.device6_open(0), lambda : self.set_timeout6(0), self.timer_6, self.Ptimer_6, self.Ttimer_6, self.groupBox_6))        

        self.start_open_time_bttn_6.clicked.connect(lambda : self.open_time_execution(self.timer_6, self.Ptimer_6, self.timeEdit_6, 
            [self.start_time_bttn_6, self.start_open_time_bttn_6, self.pause_bttn_6], 
                lambda : self.open_time_mechanics(self.timeEdit_6, lambda : self.device6_counter(1) ), lambda : self.device6_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 7 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_7.clicked.connect(lambda : self.add(self.spinBox_7, self.listWidget_7, self.comboBox_7, self.products_list_7))

        self.delete_bttn_7.clicked.connect(lambda : self.delete_list_item(self.listWidget_7, self.products_list_7))

        self.start_time_bttn_7.clicked.connect(lambda : self.timer_execution(self.timeEdit_7, self.timer_7, self.Ptimer_7,
            [self.start_time_bttn_7, self.start_open_time_bttn_7, self.pause_bttn_7], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_7, self.timer_7, self.Ttimer_7, self.label_7,
                [self.start_time_bttn_7, self.start_open_time_bttn_7, self.pause_bttn_7],
                 lambda : self.device7_counter(1), lambda : self.set_timeout7(1), lambda : self.device7_Tcounter(1)  )))

        self.pause_bttn_7.clicked.connect(lambda : self.pause_time( self.timer_7, self.Ptimer_7,
            [self.start_time_bttn_7, self.start_open_time_bttn_7, self.pause_bttn_7], self.is_open7, lambda : self.device7_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_7.clicked.connect(lambda : self.submit(self.Mcounter7 ,self.Pcounter7, self.Tcounter7,self.timer_7,
        self.Ptimer_7, self.Ttimer_7, self.timeEdit_7, self.groupBox_7,
            [self.single_radioBttn_7, self.multi1_radioBttn_7, self.multi2_radioBttn_7], self.lineEdit_7, self.listWidget_7, 
            self.products_list_7, self.products_prices_list_7, self.label_7, [self.start_time_bttn_7, self.start_open_time_bttn_7],
            lambda : self.device7_counter(0), lambda : self.device7_open(0), self.clear7 , self.is_timeout7, lambda : self.set_timeout7(0),
            lambda : self.device7_Pcounter(0), lambda : self.device7_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_7.clicked.connect(lambda : self.cancel(self.products_prices_list_7, self.listWidget_7, self.lineEdit_7, self.label_7, self.timeEdit_7, 
        [self.start_time_bttn_7, self.start_open_time_bttn_7, self.pause_bttn_7], [self.single_radioBttn_7, self.multi1_radioBttn_7, self.multi2_radioBttn_7],
        lambda : self.device7_counter(0), lambda : self.device7_Pcounter(0), lambda : self.device7_Tcounter(0), self.clear7,
        lambda : self.device7_open(0), lambda : self.set_timeout7(0), self.timer_7, self.Ptimer_7, self.Ttimer_7, self.groupBox_7))        

        self.start_open_time_bttn_7.clicked.connect(lambda : self.open_time_execution(self.timer_7, self.Ptimer_7, self.timeEdit_7, 
            [self.start_time_bttn_7, self.start_open_time_bttn_7, self.pause_bttn_7], 
                lambda : self.open_time_mechanics(self.timeEdit_7, lambda : self.device7_counter(1) ),
                lambda : self.device7_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 8 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_8.clicked.connect(lambda : self.add(self.spinBox_8, self.listWidget_8, self.comboBox_8, self.products_list_8))

        self.delete_bttn_8.clicked.connect(lambda : self.delete_list_item(self.listWidget_8, self.products_list_8))

        self.start_time_bttn_8.clicked.connect(lambda : self.timer_execution(self.timeEdit_8, self.timer_8, self.Ptimer_8,
            [self.start_time_bttn_8, self.start_open_time_bttn_8, self.pause_bttn_8], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_8, self.timer_8, self.Ttimer_8, self.label_8,
                [self.start_time_bttn_8, self.start_open_time_bttn_8, self.pause_bttn_8],
                 lambda : self.device8_counter(1), lambda : self.set_timeout8(1), lambda : self.device8_Tcounter(1)  )))

        self.pause_bttn_8.clicked.connect(lambda : self.pause_time( self.timer_8, self.Ptimer_8,
            [self.start_time_bttn_8, self.start_open_time_bttn_8, self.pause_bttn_8], self.is_open8, lambda : self.device8_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_8.clicked.connect(lambda : self.submit(self.Mcounter8 ,self.Pcounter8, self.Tcounter8,self.timer_8,
        self.Ptimer_8, self.Ttimer_8, self.timeEdit_8, self.groupBox_8,
            [self.single_radioBttn_8, self.multi1_radioBttn_8, self.multi2_radioBttn_8], self.lineEdit_8, self.listWidget_8, 
            self.products_list_8, self.products_prices_list_8, self.label_8, [self.start_time_bttn_8, self.start_open_time_bttn_8],
            lambda : self.device8_counter(0), lambda : self.device8_open(0), self.clear8 , self.is_timeout8, lambda : self.set_timeout8(0),
            lambda : self.device8_Pcounter(0), lambda : self.device8_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_8.clicked.connect(lambda : self.cancel(self.products_prices_list_8, self.listWidget_8, self.lineEdit_8, self.label_8, self.timeEdit_8, 
        [self.start_time_bttn_8, self.start_open_time_bttn_8, self.pause_bttn_8], [self.single_radioBttn_8, self.multi1_radioBttn_8, self.multi2_radioBttn_8],
        lambda : self.device8_counter(0), lambda : self.device8_Pcounter(0), lambda : self.device8_Tcounter(0), self.clear8,
        lambda : self.device8_open(0), lambda : self.set_timeout8(0), self.timer_8, self.Ptimer_8, self.Ttimer_8, self.groupBox_8))        

        self.start_open_time_bttn_8.clicked.connect(lambda : self.open_time_execution(self.timer_8, self.Ptimer_8, self.timeEdit_8, 
            [self.start_time_bttn_8, self.start_open_time_bttn_8, self.pause_bttn_8], 
                lambda : self.open_time_mechanics(self.timeEdit_8, lambda : self.device8_counter(1) ),
                lambda : self.device8_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 
         
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 9 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_9.clicked.connect(lambda : self.add(self.spinBox_9, self.listWidget_9, self.comboBox_9, self.products_list_9))

        self.delete_bttn_9.clicked.connect(lambda : self.delete_list_item(self.listWidget_9, self.products_list_9))

        self.start_time_bttn_9.clicked.connect(lambda : self.timer_execution(self.timeEdit_9, self.timer_9, self.Ptimer_9,
            [self.start_time_bttn_9, self.start_open_time_bttn_9, self.pause_bttn_9], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_9, self.timer_9, self.Ttimer_9, self.label_9,
                [self.start_time_bttn_9, self.start_open_time_bttn_9, self.pause_bttn_9],
                 lambda : self.device9_counter(1), lambda : self.set_timeout9(1), lambda : self.device9_Tcounter(1)  )))

        self.pause_bttn_9.clicked.connect(lambda : self.pause_time( self.timer_9, self.Ptimer_9,
            [self.start_time_bttn_9, self.start_open_time_bttn_9, self.pause_bttn_9], self.is_open9, lambda : self.device9_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_9.clicked.connect(lambda : self.submit(self.Mcounter9 ,self.Pcounter9, self.Tcounter9,self.timer_9,
        self.Ptimer_9, self.Ttimer_9, self.timeEdit_9, self.groupBox_9,
            [self.single_radioBttn_9, self.multi1_radioBttn_9, self.multi2_radioBttn_9], self.lineEdit_9, self.listWidget_9, 
            self.products_list_9, self.products_prices_list_9, self.label_9, [self.start_time_bttn_9, self.start_open_time_bttn_9],
            lambda : self.device9_counter(0), lambda : self.device9_open(0), self.clear9 , self.is_timeout9, lambda : self.set_timeout9(0),
            lambda : self.device9_Pcounter(0), lambda : self.device9_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_9.clicked.connect(lambda : self.cancel(self.products_prices_list_9, self.listWidget_9, self.lineEdit_9, self.label_9, self.timeEdit_9, 
        [self.start_time_bttn_9, self.start_open_time_bttn_9, self.pause_bttn_9], [self.single_radioBttn_9, self.multi1_radioBttn_9, self.multi2_radioBttn_9],
        lambda : self.device9_counter(0), lambda : self.device9_Pcounter(0), lambda : self.device9_Tcounter(0), self.clear9,
        lambda : self.device9_open(0), lambda : self.set_timeout9(0), self.timer_9, self.Ptimer_9, self.Ttimer_9, self.groupBox_9))        

        self.start_open_time_bttn_9.clicked.connect(lambda : self.open_time_execution(self.timer_9, self.Ptimer_9, self.timeEdit_9, 
            [self.start_time_bttn_9, self.start_open_time_bttn_9, self.pause_bttn_9], 
                lambda : self.open_time_mechanics(self.timeEdit_9, lambda : self.device9_counter(1) ),
                lambda : self.device9_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
         
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 10 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_10.clicked.connect(lambda : self.add(self.spinBox_10, self.listWidget_10, self.comboBox_10, self.products_list_10))

        self.delete_bttn_10.clicked.connect(lambda : self.delete_list_item(self.listWidget_10, self.products_list_10))

        self.start_time_bttn_10.clicked.connect(lambda : self.timer_execution(self.timeEdit_10, self.timer_10, self.Ptimer_10,
            [self.start_time_bttn_10, self.start_open_time_bttn_10, self.pause_bttn_10], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_10, self.timer_10, self.Ttimer_10, self.label_10,
                [self.start_time_bttn_10, self.start_open_time_bttn_10, self.pause_bttn_10],
                 lambda : self.device10_counter(1), lambda : self.set_timeout10(1), lambda : self.device10_Tcounter(1)  )))

        self.pause_bttn_10.clicked.connect(lambda : self.pause_time( self.timer_10, self.Ptimer_10,
            [self.start_time_bttn_10, self.start_open_time_bttn_10, self.pause_bttn_10], self.is_open10, lambda : self.device10_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_10.clicked.connect(lambda : self.submit(self.Mcounter10 ,self.Pcounter10, self.Tcounter10,self.timer_10,
        self.Ptimer_10, self.Ttimer_10, self.timeEdit_10, self.groupBox_10,
            [self.single_radioBttn_10, self.multi1_radioBttn_10, self.multi2_radioBttn_10], self.lineEdit_10, self.listWidget_10, 
            self.products_list_10, self.products_prices_list_10, self.label_10, [self.start_time_bttn_10, self.start_open_time_bttn_10],
            lambda : self.device10_counter(0), lambda : self.device10_open(0), self.clear10 , self.is_timeout10, lambda : self.set_timeout10(0),
            lambda : self.device10_Pcounter(0), lambda : self.device10_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_10.clicked.connect(lambda : self.cancel(self.products_prices_list_10, self.listWidget_10, self.lineEdit_10, self.label_10, self.timeEdit_10, 
        [self.start_time_bttn_10, self.start_open_time_bttn_10, self.pause_bttn_10], [self.single_radioBttn_10, self.multi1_radioBttn_10, self.multi2_radioBttn_10],
        lambda : self.device10_counter(0), lambda : self.device10_Pcounter(0), lambda : self.device10_Tcounter(0), self.clear10,
        lambda : self.device10_open(0), lambda : self.set_timeout10(0), self.timer_10, self.Ptimer_10, self.Ttimer_10, self.groupBox_10))        

        self.start_open_time_bttn_10.clicked.connect(lambda : self.open_time_execution(self.timer_10, self.Ptimer_10, self.timeEdit_10, 
            [self.start_time_bttn_10, self.start_open_time_bttn_10, self.pause_bttn_10], 
                lambda : self.open_time_mechanics(self.timeEdit_10, lambda : self.device10_counter(1) ),
                lambda : self.device10_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 11 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_11.clicked.connect(lambda : self.add(self.spinBox_11, self.listWidget_11, self.comboBox_11, self.products_list_11))

        self.delete_bttn_11.clicked.connect(lambda : self.delete_list_item(self.listWidget_11, self.products_list_11))

        self.start_time_bttn_11.clicked.connect(lambda : self.timer_execution(self.timeEdit_11, self.timer_11, self.Ptimer_11,
            [self.start_time_bttn_11, self.start_open_time_bttn_11, self.pause_bttn_11], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_11, self.timer_11, self.Ttimer_11, self.label_11,
                [self.start_time_bttn_11, self.start_open_time_bttn_11, self.pause_bttn_11],
                 lambda : self.device11_counter(1), lambda : self.set_timeout11(1), lambda : self.device11_Tcounter(1)  )))

        self.pause_bttn_11.clicked.connect(lambda : self.pause_time( self.timer_11, self.Ptimer_11,
            [self.start_time_bttn_11, self.start_open_time_bttn_11, self.pause_bttn_11], self.is_open11, lambda : self.device11_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_11.clicked.connect(lambda : self.submit(self.Mcounter11 ,self.Pcounter11, self.Tcounter11,self.timer_11,
        self.Ptimer_11, self.Ttimer_11, self.timeEdit_11, self.groupBox_11,
            [self.single_radioBttn_11, self.multi1_radioBttn_11, self.multi2_radioBttn_11], self.lineEdit_11, self.listWidget_11, 
            self.products_list_11, self.products_prices_list_11, self.label_11, [self.start_time_bttn_11, self.start_open_time_bttn_11],
            lambda : self.device11_counter(0), lambda : self.device11_open(0), self.clear11 , self.is_timeout11, lambda : self.set_timeout11(0),
            lambda : self.device11_Pcounter(0), lambda : self.device11_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_11.clicked.connect(lambda : self.cancel(self.products_prices_list_11, self.listWidget_11, self.lineEdit_11, self.label_11, self.timeEdit_11, 
        [self.start_time_bttn_11, self.start_open_time_bttn_11, self.pause_bttn_11], [self.single_radioBttn_11, self.multi1_radioBttn_11, self.multi2_radioBttn_11],
        lambda : self.device11_counter(0), lambda : self.device11_Pcounter(0), lambda : self.device11_Tcounter(0), self.clear11,
        lambda : self.device11_open(0), lambda : self.set_timeout11(0), self.timer_11, self.Ptimer_11, self.Ttimer_11, self.groupBox_11))        

        self.start_open_time_bttn_11.clicked.connect(lambda : self.open_time_execution(self.timer_11, self.Ptimer_11, self.timeEdit_11, 
            [self.start_time_bttn_11, self.start_open_time_bttn_11, self.pause_bttn_11], 
                lambda : self.open_time_mechanics(self.timeEdit_11, lambda : self.device11_counter(1) ),
                lambda : self.device11_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$        
         
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 12 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_12.clicked.connect(lambda : self.add(self.spinBox_12, self.listWidget_12, self.comboBox_12, self.products_list_12))

        self.delete_bttn_12.clicked.connect(lambda : self.delete_list_item(self.listWidget_12, self.products_list_12))

        self.start_time_bttn_12.clicked.connect(lambda : self.timer_execution(self.timeEdit_12, self.timer_12, self.Ptimer_12,
            [self.start_time_bttn_12, self.start_open_time_bttn_12, self.pause_bttn_12], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_12, self.timer_12, self.Ttimer_12, self.label_12,
                [self.start_time_bttn_12, self.start_open_time_bttn_12, self.pause_bttn_12],
                 lambda : self.device12_counter(1), lambda : self.set_timeout12(1), lambda : self.device12_Tcounter(1)  )))

        self.pause_bttn_12.clicked.connect(lambda : self.pause_time( self.timer_12, self.Ptimer_12,
            [self.start_time_bttn_12, self.start_open_time_bttn_12, self.pause_bttn_12], self.is_open12, lambda : self.device12_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_12.clicked.connect(lambda : self.submit(self.Mcounter12 ,self.Pcounter12, self.Tcounter12,self.timer_12,
        self.Ptimer_12, self.Ttimer_12, self.timeEdit_12, self.groupBox_12,
            [self.single_radioBttn_12, self.multi1_radioBttn_12, self.multi2_radioBttn_12], self.lineEdit_12, self.listWidget_12, 
            self.products_list_12, self.products_prices_list_12, self.label_12, [self.start_time_bttn_12, self.start_open_time_bttn_12],
            lambda : self.device12_counter(0), lambda : self.device12_open(0), self.clear12 , self.is_timeout12, lambda : self.set_timeout12(0),
            lambda : self.device12_Pcounter(0), lambda : self.device12_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_12.clicked.connect(lambda : self.cancel(self.products_prices_list_12, self.listWidget_12, self.lineEdit_12, self.label_12, self.timeEdit_12, 
        [self.start_time_bttn_12, self.start_open_time_bttn_12, self.pause_bttn_12], [self.single_radioBttn_12, self.multi1_radioBttn_12, self.multi2_radioBttn_12],
        lambda : self.device12_counter(0), lambda : self.device12_Pcounter(0), lambda : self.device12_Tcounter(0), self.clear12,
        lambda : self.device12_open(0), lambda : self.set_timeout12(0), self.timer_12, self.Ptimer_12, self.Ttimer_12, self.groupBox_12))        

        self.start_open_time_bttn_12.clicked.connect(lambda : self.open_time_execution(self.timer_12, self.Ptimer_12, self.timeEdit_12, 
            [self.start_time_bttn_12, self.start_open_time_bttn_12, self.pause_bttn_12], 
                lambda : self.open_time_mechanics(self.timeEdit_12, lambda : self.device12_counter(1) ),
                lambda : self.device12_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$                                              

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 13 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_13.clicked.connect(lambda : self.add(self.spinBox_13, self.listWidget_13, self.comboBox_13, self.products_list_13))

        self.delete_bttn_13.clicked.connect(lambda : self.delete_list_item(self.listWidget_13, self.products_list_13))

        self.start_time_bttn_13.clicked.connect(lambda : self.timer_execution(self.timeEdit_13, self.timer_13, self.Ptimer_13,
            [self.start_time_bttn_13, self.start_open_time_bttn_13, self.pause_bttn_13], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_13, self.timer_13, self.Ttimer_13, self.label_13,
                [self.start_time_bttn_13, self.start_open_time_bttn_13, self.pause_bttn_13],
                 lambda : self.device13_counter(1), lambda : self.set_timeout13(1), lambda : self.device13_Tcounter(1)  )))

        self.pause_bttn_13.clicked.connect(lambda : self.pause_time( self.timer_13, self.Ptimer_13,
            [self.start_time_bttn_13, self.start_open_time_bttn_13, self.pause_bttn_13], self.is_open13, lambda : self.device13_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_13.clicked.connect(lambda : self.submit(self.Mcounter13 ,self.Pcounter13, self.Tcounter13,self.timer_13,
        self.Ptimer_13, self.Ttimer_13, self.timeEdit_13, self.groupBox_13,
            [self.single_radioBttn_13, self.multi1_radioBttn_13, self.multi2_radioBttn_13], self.lineEdit_13, self.listWidget_13, 
            self.products_list_13, self.products_prices_list_13, self.label_13, [self.start_time_bttn_13, self.start_open_time_bttn_13],
            lambda : self.device13_counter(0), lambda : self.device13_open(0), self.clear13 , self.is_timeout13, lambda : self.set_timeout13(0),
            lambda : self.device13_Pcounter(0), lambda : self.device13_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_13.clicked.connect(lambda : self.cancel(self.products_prices_list_13, self.listWidget_13, self.lineEdit_13, self.label_13, self.timeEdit_13, 
        [self.start_time_bttn_13, self.start_open_time_bttn_13, self.pause_bttn_13], [self.single_radioBttn_13, self.multi1_radioBttn_13, self.multi2_radioBttn_13],
        lambda : self.device13_counter(0), lambda : self.device13_Pcounter(0), lambda : self.device13_Tcounter(0), self.clear13,
        lambda : self.device13_open(0), lambda : self.set_timeout13(0), self.timer_13, self.Ptimer_13, self.Ttimer_13, self.groupBox_13))        

        self.start_open_time_bttn_13.clicked.connect(lambda : self.open_time_execution(self.timer_13, self.Ptimer_13, self.timeEdit_13, 
            [self.start_time_bttn_13, self.start_open_time_bttn_13, self.pause_bttn_13], 
                lambda : self.open_time_mechanics(self.timeEdit_13, lambda : self.device13_counter(1) ),
                lambda : self.device13_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 14 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_14.clicked.connect(lambda : self.add(self.spinBox_14, self.listWidget_14, self.comboBox_14, self.products_list_14))

        self.delete_bttn_14.clicked.connect(lambda : self.delete_list_item(self.listWidget_14, self.products_list_14))

        self.start_time_bttn_14.clicked.connect(lambda : self.timer_execution(self.timeEdit_14, self.timer_14, self.Ptimer_14,
            [self.start_time_bttn_14, self.start_open_time_bttn_14, self.pause_bttn_14], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_14, self.timer_14, self.Ttimer_14, self.label_14,
                [self.start_time_bttn_14, self.start_open_time_bttn_14, self.pause_bttn_14],
                 lambda : self.device14_counter(1), lambda : self.set_timeout14(1), lambda : self.device14_Tcounter(1)  )))

        self.pause_bttn_14.clicked.connect(lambda : self.pause_time( self.timer_14, self.Ptimer_14,
            [self.start_time_bttn_14, self.start_open_time_bttn_14, self.pause_bttn_14], self.is_open14, lambda : self.device14_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_14.clicked.connect(lambda : self.submit(self.Mcounter14 ,self.Pcounter14, self.Tcounter14,self.timer_14,
        self.Ptimer_14, self.Ttimer_14, self.timeEdit_14, self.groupBox_14,
            [self.single_radioBttn_14, self.multi1_radioBttn_14, self.multi2_radioBttn_14], self.lineEdit_14, self.listWidget_14, 
            self.products_list_14, self.products_prices_list_14, self.label_14, [self.start_time_bttn_14, self.start_open_time_bttn_14],
            lambda : self.device14_counter(0), lambda : self.device14_open(0), self.clear14 , self.is_timeout14, lambda : self.set_timeout14(0),
            lambda : self.device14_Pcounter(0), lambda : self.device14_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_14.clicked.connect(lambda : self.cancel(self.products_prices_list_14, self.listWidget_14, self.lineEdit_14, self.label_14, self.timeEdit_14, 
        [self.start_time_bttn_14, self.start_open_time_bttn_14, self.pause_bttn_14], [self.single_radioBttn_14, self.multi1_radioBttn_14, self.multi2_radioBttn_14],
        lambda : self.device14_counter(0), lambda : self.device14_Pcounter(0), lambda : self.device14_Tcounter(0), self.clear14,
        lambda : self.device14_open(0), lambda : self.set_timeout14(0), self.timer_14, self.Ptimer_14, self.Ttimer_14, self.groupBox_14))        

        self.start_open_time_bttn_14.clicked.connect(lambda : self.open_time_execution(self.timer_14, self.Ptimer_14, self.timeEdit_14, 
            [self.start_time_bttn_14, self.start_open_time_bttn_14, self.pause_bttn_14], 
                lambda : self.open_time_mechanics(self.timeEdit_14, lambda : self.device14_counter(1) ),
                lambda : self.device14_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 15 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_15.clicked.connect(lambda : self.add(self.spinBox_15, self.listWidget_15, self.comboBox_15, self.products_list_15))

        self.delete_bttn_15.clicked.connect(lambda : self.delete_list_item(self.listWidget_15, self.products_list_15))

        self.start_time_bttn_15.clicked.connect(lambda : self.timer_execution(self.timeEdit_15, self.timer_15, self.Ptimer_15,
            [self.start_time_bttn_15, self.start_open_time_bttn_15, self.pause_bttn_15], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_15, self.timer_15, self.Ttimer_15, self.label_15,
                [self.start_time_bttn_15, self.start_open_time_bttn_15, self.pause_bttn_15],
                 lambda : self.device15_counter(1), lambda : self.set_timeout15(1), lambda : self.device15_Tcounter(1)  )))

        self.pause_bttn_15.clicked.connect(lambda : self.pause_time( self.timer_15, self.Ptimer_15,
            [self.start_time_bttn_15, self.start_open_time_bttn_15, self.pause_bttn_15], self.is_open15, lambda : self.device15_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_15.clicked.connect(lambda : self.submit(self.Mcounter15 ,self.Pcounter15, self.Tcounter15,self.timer_15,
        self.Ptimer_15, self.Ttimer_15, self.timeEdit_15, self.groupBox_15,
            [self.single_radioBttn_15, self.multi1_radioBttn_15, self.multi2_radioBttn_15], self.lineEdit_15, self.listWidget_15, 
            self.products_list_15, self.products_prices_list_15, self.label_15, [self.start_time_bttn_15, self.start_open_time_bttn_15],
            lambda : self.device15_counter(0), lambda : self.device15_open(0), self.clear15 , self.is_timeout15, lambda : self.set_timeout15(0),
            lambda : self.device15_Pcounter(0), lambda : self.device15_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_15.clicked.connect(lambda : self.cancel(self.products_prices_list_15, self.listWidget_15, self.lineEdit_15, self.label_15, self.timeEdit_15, 
        [self.start_time_bttn_15, self.start_open_time_bttn_15, self.pause_bttn_15], [self.single_radioBttn_15, self.multi1_radioBttn_15, self.multi2_radioBttn_15],
        lambda : self.device15_counter(0), lambda : self.device15_Pcounter(0), lambda : self.device15_Tcounter(0), self.clear15,
        lambda : self.device15_open(0), lambda : self.set_timeout15(0), self.timer_15, self.Ptimer_15, self.Ttimer_15, self.groupBox_15))        

        self.start_open_time_bttn_15.clicked.connect(lambda : self.open_time_execution(self.timer_15, self.Ptimer_15, self.timeEdit_15, 
            [self.start_time_bttn_15, self.start_open_time_bttn_15, self.pause_bttn_15], 
                lambda : self.open_time_mechanics(self.timeEdit_15, lambda : self.device15_counter(1) ),
                lambda : self.device15_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 16 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_16.clicked.connect(lambda : self.add(self.spinBox_16, self.listWidget_16, self.comboBox_16, self.products_list_16))

        self.delete_bttn_16.clicked.connect(lambda : self.delete_list_item(self.listWidget_16, self.products_list_16))

        self.start_time_bttn_16.clicked.connect(lambda : self.timer_execution(self.timeEdit_16, self.timer_16, self.Ptimer_16,
            [self.start_time_bttn_16, self.start_open_time_bttn_16, self.pause_bttn_16], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_16, self.timer_16, self.Ttimer_16, self.label_16,
                [self.start_time_bttn_16, self.start_open_time_bttn_16, self.pause_bttn_16],
                 lambda : self.device16_counter(1), lambda : self.set_timeout16(1), lambda : self.device16_Tcounter(1)  )))

        self.pause_bttn_16.clicked.connect(lambda : self.pause_time( self.timer_16, self.Ptimer_16,
            [self.start_time_bttn_16, self.start_open_time_bttn_16, self.pause_bttn_16], self.is_open16, lambda : self.device16_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_16.clicked.connect(lambda : self.submit(self.Mcounter16 ,self.Pcounter16, self.Tcounter16,self.timer_16,
        self.Ptimer_16, self.Ttimer_16, self.timeEdit_16, self.groupBox_16,
            [self.single_radioBttn_16, self.multi1_radioBttn_16, self.multi2_radioBttn_16], self.lineEdit_16, self.listWidget_16, 
            self.products_list_16, self.products_prices_list_16, self.label_16, [self.start_time_bttn_16, self.start_open_time_bttn_16],
            lambda : self.device16_counter(0), lambda : self.device16_open(0), self.clear16 , self.is_timeout16, lambda : self.set_timeout16(0),
            lambda : self.device16_Pcounter(0), lambda : self.device16_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_16.clicked.connect(lambda : self.cancel(self.products_prices_list_16, self.listWidget_16, self.lineEdit_16, self.label_16, self.timeEdit_16, 
        [self.start_time_bttn_16, self.start_open_time_bttn_16, self.pause_bttn_16], [self.single_radioBttn_16, self.multi1_radioBttn_16, self.multi2_radioBttn_16],
        lambda : self.device16_counter(0), lambda : self.device16_Pcounter(0), lambda : self.device16_Tcounter(0), self.clear16,
        lambda : self.device16_open(0), lambda : self.set_timeout16(0), self.timer_16, self.Ptimer_16, self.Ttimer_16, self.groupBox_16))        

        self.start_open_time_bttn_16.clicked.connect(lambda : self.open_time_execution(self.timer_16, self.Ptimer_16, self.timeEdit_16, 
            [self.start_time_bttn_16, self.start_open_time_bttn_16, self.pause_bttn_16], 
                lambda : self.open_time_mechanics(self.timeEdit_16, lambda : self.device16_counter(1) ),
                lambda : self.device16_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 17 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_17.clicked.connect(lambda : self.add(self.spinBox_17, self.listWidget_17, self.comboBox_17, self.products_list_17))

        self.delete_bttn_17.clicked.connect(lambda : self.delete_list_item(self.listWidget_17, self.products_list_17))

        self.start_time_bttn_17.clicked.connect(lambda : self.timer_execution(self.timeEdit_17, self.timer_17, self.Ptimer_17,
            [self.start_time_bttn_17, self.start_open_time_bttn_17, self.pause_bttn_17], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_17, self.timer_17, self.Ttimer_17, self.label_17,
                [self.start_time_bttn_17, self.start_open_time_bttn_17, self.pause_bttn_17],
                 lambda : self.device17_counter(1), lambda : self.set_timeout17(1), lambda : self.device17_Tcounter(1)  )))

        self.pause_bttn_17.clicked.connect(lambda : self.pause_time( self.timer_17, self.Ptimer_17,
            [self.start_time_bttn_17, self.start_open_time_bttn_17, self.pause_bttn_17], self.is_open17, lambda : self.device17_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_17.clicked.connect(lambda : self.submit(self.Mcounter17 ,self.Pcounter17, self.Tcounter17,self.timer_17,
        self.Ptimer_17, self.Ttimer_17, self.timeEdit_17, self.groupBox_17,
            [self.single_radioBttn_17, self.multi1_radioBttn_17, self.multi2_radioBttn_17], self.lineEdit_17, self.listWidget_17, 
            self.products_list_17, self.products_prices_list_17, self.label_17, [self.start_time_bttn_17, self.start_open_time_bttn_17],
            lambda : self.device17_counter(0), lambda : self.device17_open(0), self.clear17 , self.is_timeout17, lambda : self.set_timeout17(0),
            lambda : self.device17_Pcounter(0), lambda : self.device17_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_17.clicked.connect(lambda : self.cancel(self.products_prices_list_17, self.listWidget_17, self.lineEdit_17, self.label_17, self.timeEdit_17, 
        [self.start_time_bttn_17, self.start_open_time_bttn_17, self.pause_bttn_17], [self.single_radioBttn_17, self.multi1_radioBttn_17, self.multi2_radioBttn_17],
        lambda : self.device17_counter(0), lambda : self.device17_Pcounter(0), lambda : self.device17_Tcounter(0), self.clear17,
        lambda : self.device17_open(0), lambda : self.set_timeout17(0), self.timer_17, self.Ptimer_17, self.Ttimer_17, self.groupBox_17))        

        self.start_open_time_bttn_17.clicked.connect(lambda : self.open_time_execution(self.timer_17, self.Ptimer_17, self.timeEdit_17, 
            [self.start_time_bttn_17, self.start_open_time_bttn_17, self.pause_bttn_17], 
                lambda : self.open_time_mechanics(self.timeEdit_17, lambda : self.device17_counter(1) ),
                lambda : self.device17_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 18 nd $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.add_bttn_18.clicked.connect(lambda : self.add(self.spinBox_18, self.listWidget_18, self.comboBox_18, self.products_list_18))

        self.delete_bttn_18.clicked.connect(lambda : self.delete_list_item(self.listWidget_18, self.products_list_18))

        self.start_time_bttn_18.clicked.connect(lambda : self.timer_execution(self.timeEdit_18, self.timer_18, self.Ptimer_18,
            [self.start_time_bttn_18, self.start_open_time_bttn_18, self.pause_bttn_18], 
            lambda : self.timer_timeEdit_mechanics(self.timeEdit_18, self.timer_18, self.Ttimer_18, self.label_18,
                [self.start_time_bttn_18, self.start_open_time_bttn_18, self.pause_bttn_18],
                 lambda : self.device18_counter(1), lambda : self.set_timeout18(1), lambda : self.device18_Tcounter(1)  )))

        self.pause_bttn_18.clicked.connect(lambda : self.pause_time( self.timer_18, self.Ptimer_18,
            [self.start_time_bttn_18, self.start_open_time_bttn_18, self.pause_bttn_18], self.is_open18, lambda : self.device18_Pcounter(1) ))

                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #
        self.submit_bttn_18.clicked.connect(lambda : self.submit(self.Mcounter18 ,self.Pcounter18, self.Tcounter18,self.timer_18,
        self.Ptimer_18, self.Ttimer_18, self.timeEdit_18, self.groupBox_18,
            [self.single_radioBttn_18, self.multi1_radioBttn_18, self.multi2_radioBttn_18], self.lineEdit_18, self.listWidget_18, 
            self.products_list_18, self.products_prices_list_18, self.label_18, [self.start_time_bttn_18, self.start_open_time_bttn_18],
            lambda : self.device18_counter(0), lambda : self.device18_open(0), self.clear18 , self.is_timeout18, lambda : self.set_timeout18(0),
            lambda : self.device18_Pcounter(0), lambda : self.device18_Tcounter(0) ))
                                # - - - - - - - - - -  - - - - - - - - - - - - - - -  #

        self.cancel_bttn_18.clicked.connect(lambda : self.cancel(self.products_prices_list_18, self.listWidget_18, self.lineEdit_18, self.label_18, self.timeEdit_18, 
        [self.start_time_bttn_18, self.start_open_time_bttn_18, self.pause_bttn_18], [self.single_radioBttn_18, self.multi1_radioBttn_18, self.multi2_radioBttn_18],
        lambda : self.device18_counter(0), lambda : self.device18_Pcounter(0), lambda : self.device18_Tcounter(0), self.clear18,
        lambda : self.device18_open(0), lambda : self.set_timeout18(0), self.timer_18, self.Ptimer_18, self.Ttimer_18, self.groupBox_18))        

        self.start_open_time_bttn_18.clicked.connect(lambda : self.open_time_execution(self.timer_18, self.Ptimer_18, self.timeEdit_18, 
            [self.start_time_bttn_18, self.start_open_time_bttn_18, self.pause_bttn_18], 
                lambda : self.open_time_mechanics(self.timeEdit_18, lambda : self.device18_counter(1) ),
                lambda : self.device18_open(1) ) )  
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def rename_groupBoxes(self):
        ID_index = 1
        for i in self.groupboxes:
            name  = cursor.execute(f'SELECT Name FROM "Consoles and Screens" WHERE ID = {ID_index}').fetchone()[0]
            i.setTitle(name)
            ID_index +=1


    # buttons = [Start, Start open, Pause]
    def timer_execution(self, time_edit, timer, Ptimer, buttons, function):
        if time_edit.time().toPyTime() != time(0,0,0):
            if Ptimer.isActive():
                Ptimer.stop()
                Ptimer.disconnect()  
            timer.timeout.connect(function)
            timer.start(1000)
            buttons[0].setDisabled(True)
            buttons[1].setDisabled(True)
            buttons[2].setEnabled(True)
            time_edit.setReadOnly(True)


    def show_foods(self, combobox):
        products_list = [i[0] for i  in cursor.execute('SELECT Name FROM Foods').fetchall()]
        combobox.addItems(products_list)


    def add(self, spinbox, listwidget, combobox, products_list):
        for i in range(spinbox.value()):
            listwidget.addItem(combobox.currentText())
            products_list.append(combobox.currentText())
  


    def delete_list_item(self, listwidget ,products_list):
        try :
            if listwidget.count() != 0:
                row_index  = listwidget.currentRow()
                products_list.remove(listwidget.item(row_index).text())
                listwidget.takeItem(row_index)
            else :
                pass
        except AttributeError :
            pass

    def reset_ring_tone(self):
        self.exa = 0
    # buttons = [Start, Start open, Pause]
    def timer_timeEdit_mechanics(self, time_edit, timer, Ttimer,  label,  buttons, fun, fun2, fun3):
        if time_edit.time().toPyTime() != time(0,0,0):
            currentTime = time_edit.time().toPyTime()
            current = datetime.combine(date.today(), currentTime)
            deltaT = timedelta(seconds= 1)
            current -= deltaT
            time_edit.setTime(current.time())
            fun()
        else :
            if self.exa == 0 : 
                with concurrent.futures.ThreadPoolExecutor() as ex:
                    ex.submit(lambda : playsound('styles/annoy.mp3', block= False) )
                    self.exa = 1
            QTimer.singleShot(13300, self.reset_ring_tone)
            buttons[0].setEnabled(True)
            timer.stop()
            timer.disconnect()
            buttons[2].setDisabled(True)
            buttons[1].setDisabled(True)
            buttons[0].setDisabled(True)
            time_edit.setDisabled(True)
            fun2()
            label.setText("Time out")
            label.setStyleSheet("background-color: white; color: #8b0000; min-height : 25px; font: 11pt 'Impact'; border : 1px solid #8b0000")
            Ttimer.timeout.connect(fun3)
            Ttimer.start(1000)


         

    def open_time_mechanics(self, time_edit, fun):
        currentTime = time_edit.time().toPyTime()
        current = datetime.combine(date.today(), currentTime)
        deltaT = timedelta(seconds= 1)
        current += deltaT
        time_edit.setTime(current.time())
        fun()


    # buttons = [Start, Start open, Pause]    
    def open_time_execution(self, timer, Ptimer, time_edit, buttons, function, fun):
        fun()
        if Ptimer.isActive():
            Ptimer.stop()
            Ptimer.disconnect()        
        timer.timeout.connect(function)
        timer.start(1000)
        buttons[2].setEnabled(True)
        buttons[0].setDisabled(True)
        buttons[1].setDisabled(True)
        time_edit.setReadOnly(True)


    # buttons = [Start, Start open, Pause]
    def pause_time(self, timer, Ptimer, buttons, TimeOpen,  fun):
        try :
            if TimeOpen:
                timer.stop()
                timer.disconnect()
                buttons[1].setEnabled(True)
                buttons[2].setDisabled(True)
            else:
                timer.stop()
                timer.disconnect()
                buttons[0].setEnabled(True)
                buttons[2].setDisabled(True)
            Ptimer.timeout.connect(fun)
            Ptimer.start(1000)
        except TypeError:
            pass


     # radios = [Singl radio, Multi1 radio, Multi2 radio]
     # buttons  = [Start, Start open]   
    def submit(self, counter, Pcounter, Tcounter, timer, Ptimer, Ttimer,  time_edit ,groupbox, radios, password_input, food_list, products_list,
    products_prices_list, price_label, buttons, fun, fun2, fun3, timeout, fun4, fun5, fun6):
        check_rates_existant(self.global_user_name, conn2)
        check_TDtable_existant(conn2)
        if (not timer.isActive()):
            try : 
                user_name = self.global_user_name
                user_password = cursor.execute(f'SELECT Password FROM Users WHERE User_Name = "{user_name}" ').fetchone()[0]
                singleHour = float(cursor.execute(f'SELECT "Price/Hour" FROM "Consoles and Screens" WHERE Name = "{groupbox.title()}" ').fetchone()[0])
                controllerHour = float(cursor.execute(f'SELECT "Controller price/hour" FROM "Consoles and Screens" WHERE Name = "{groupbox.title()}" ').fetchone()[0])
                if radios[0].isChecked():
                    HoursType = "Signle"
                    PricePerHour = singleHour
                elif radios[1].isChecked():
                    HoursType = "Multi 1"
                    PricePerHour = singleHour + controllerHour
                elif radios[2].isChecked():
                    HoursType = "Multi 2"
                    PricePerHour = singleHour + (2*controllerHour)
                
                if password_input.text() == user_password:
    # Setting "itmes:count" to be put in the list with the correct form
                    products_list = collections.Counter(products_list)
                    products_list = [f"{i}:{products_list[i]}" for i in products_list.keys()]

    # Setting variables that will sent to the table
                    device = groupbox.title()
                    start_time =( datetime.now() - timedelta(seconds= counter + Pcounter + Tcounter) ).time().strftime("%I:%M %p")
                    end_time = datetime.now().time().strftime("%I:%M %p")
                    total_foods_prices = 0
                    total_hours_prices = round((counter + Tcounter)/60) * (PricePerHour/60)
                    food_list_items = " / ".join(products_list)
                    
    # Getting the price for each item in the ListWidget & and all the prices to the "total_foods_prices"
    # Setting the "total_prices" variable
                    for i in range(food_list.count()):
                        products_prices_list.append(cursor.execute(f'''
                        SELECT "Price" FROM Foods WHERE "Name" = "{food_list.item(i).text()}" 
                        ''').fetchone()[0])
                    for i in products_prices_list:
                        total_foods_prices += i
                    

                    total_prices = ( total_foods_prices + ceil(total_hours_prices) )

    # Sending the data to the table
                  
                # Insert data into yields
                    cursor2.execute(f'''
                    INSERT INTO "{date.today()}" VALUES ("{user_name}", "{device}", "{HoursType}", "{start_time}", "{end_time}", "{f'{round((counter + Tcounter)/60)} ' + 'Minutes' }", {ceil(total_hours_prices)}, "{food_list_items}", {total_foods_prices}, {total_prices});
                    ''')

                # Update clients numbers for this user
                    current_numbers_of_clients = cursor2.execute(f'SELECT clients_numbers FROM users_rates WHERE user_name = "{user_name}" AND date = "{date.today()}" ').fetchone()[0] 
                    cursor2.execute(f'UPDATE users_rates SET clients_numbers = {current_numbers_of_clients+1} WHERE user_name = "{user_name}" AND date = "{date.today()}"  ')
                    
                    TotalMoney1 =  cursor2.execute(f'SELECT total FROM users_rates WHERE user_name = "{self.global_user_name}" AND date = "{date.today()}" ').fetchone()[0]
                    cursor2.execute(f'UPDATE users_rates SET total = {TotalMoney1 + total_prices} WHERE user_name = "{self.global_user_name}" AND date = "{date.today()}" ')

                    HoursCash = cursor2.execute(f'SELECT hourscash FROM users_rates WHERE user_name = "{self.global_user_name}" AND date = "{date.today()}" ').fetchone()[0]
                    cursor2.execute(f'UPDATE users_rates SET hourscash = {HoursCash + ceil(total_hours_prices)} WHERE user_name = "{self.global_user_name}" AND date = "{date.today()}" ')

                    FoodCash = cursor2.execute(f'SELECT foodcash FROM users_rates WHERE user_name = "{self.global_user_name}" AND date = "{date.today()}" ').fetchone()[0]
                    cursor2.execute(f'UPDATE users_rates SET foodcash = {FoodCash + total_foods_prices} WHERE user_name = "{self.global_user_name}" AND date = "{date.today()}" ')

                    conn2.commit()


                    self.blabla()
                    self.show_targrt()
                    self.listWidget_19.clear()
                    self.Today_Inventory()

                    price_label.setText(f"Required Paid is only {total_prices} EG")
                    price_label.setStyleSheet("background-color: #22c601; color: white; min-height : 25px; font: 11pt 'Impact'; border : 1px solid white")
                    QTimer.singleShot(20000,lambda : price_label.setStyleSheet("background-color : none; font: 10pt 'Impact'; min-height : 25px; color :transparent; border : 1px solid white") )
                    if Ptimer.isActive():
                        Ptimer.stop()
                        Ptimer.disconnect()  
                    if Ttimer.isActive():
                        Ttimer.stop()
                        Ttimer.disconnect() 

                    
    # Cleaning the form to start another operation
                    fun()
                    fun2()
                    fun4()
                    fun5()
                    fun6()

                    products_prices_list.clear()
                    fun3()
                    food_list.clear()
                    password_input.setText("")
                    time_edit.setEnabled(True)
                    time_edit.setTime(time(0,0))
                    time_edit.setReadOnly(False)
                    buttons[1].setEnabled(True)
                    buttons[0].setEnabled(True)
                    radios[0].setChecked(True)
                    

                else :
                    price_label.setText('Uncorrect password')
                    price_label.setStyleSheet("background-color: red; color: white; min-height : 25px; font: 11pt 'Impact'; border : 1px solid white")
                    QTimer.singleShot(3000, lambda : self.check_timeout(timeout, price_label, password_input))
                    pass

            except:
                price_label.setText('Unrecoginzed Prices')
                price_label.setStyleSheet("background-color: #666666; color: white; min-height : 25px; font: 11pt 'Impact'; border : 1px solid white")
                QTimer.singleShot(3000,lambda : price_label.setStyleSheet(" background-color : none; font: 10pt 'Impact'; min-height : 25px; color :transparent; border : 1px solid white ") )
                password_input.setText("")

                
        else:
            price_label.setText('Timer is running')
            price_label.setStyleSheet("background-color: #e1ad01; color: white; min-height : 25px; font: 11pt 'Impact'; border : 1px solid white")
            QTimer.singleShot(3000,lambda : price_label.setStyleSheet(" background-color : none; font: 10pt 'Impact'; min-height : 25px; color :transparent; border : 1px solid white ") )
            pass 


    def cancel(self, products_prices_list, food_list_widget, pass_input, price_label, time_edit, buttons, radios,  
    counter0Fun, Pcounter0Fun, Tcounter0Fun,  clr_PL_fun, set_OpenFun, set_TimeoutFun, timer, Ptimer, Ttimer, GroupBox):
        user_password = cursor.execute(f'SELECT Password FROM Users WHERE User_Name = "{self.global_user_name}" ').fetchone()[0]
        if  pass_input.text() == user_password:
            msg = QMessageBox.question(self, 'Question Meassage', f'Are you suer you want to cancel "{GroupBox.title()}" operation ? ', QMessageBox.Yes | QMessageBox.No)
            if msg == QMessageBox.Yes:
                counter0Fun(); Pcounter0Fun(); Tcounter0Fun(); set_OpenFun(); set_TimeoutFun()
                if Ptimer.isActive():
                    Ptimer.stop(); Ptimer.disconnect()
                if Ttimer.isActive():
                    Ttimer.stop(); Ttimer.disconnect()
                if timer.isActive():
                    timer.stop(); timer.disconnect()

                products_prices_list.clear()
                clr_PL_fun()
                food_list_widget.clear()  
                pass_input.setText("")
                time_edit.setEnabled(True)
                time_edit.setTime(time(0,0))
                time_edit.setReadOnly(False)  
                buttons[1].setEnabled(True)
                buttons[0].setEnabled(True)
                buttons[2].setEnabled(False)
                radios[0].setChecked(True)
            else : pass     
        else :   
            price_label.setText('Uncorrect password')
            price_label.setStyleSheet("background-color: red; color: white; min-height : 25px; font: 11pt 'Impact'; border : 1px solid white")
            QTimer.singleShot(3000, lambda : price_label.setStyleSheet(" background-color : none; font: 10pt 'Impact'; min-height : 25px; color :transparent; border : 1px solid white ") )
            pass
            

    def check_timeout(self, timeout, price_label, password_input):
        if timeout:
            price_label.setText("Time out")
            price_label.setStyleSheet("background-color: white; color: #8b0000; min-height : 25px; font: 11pt 'Impact'; border : 1px solid #8b0000")
            password_input.setText("")
        else :
            price_label.setStyleSheet(" background-color : none; font: 10pt 'Impact'; min-height : 25px; color :transparent; border : 1px solid white ") 
            password_input.setText("")
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = User_Page("holder")
    window.showMaximized()
    app.exec_()
