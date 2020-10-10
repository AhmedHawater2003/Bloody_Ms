from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from expensies import Expensies
from storage import Storage
from PyQt5.uic import loadUiType
import sys
import sqlite3
import datetime
import time
import string
import os
import concurrent.futures
from Bicon import H 
import base64
import icons2_rc, icons_rc

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
MainUI,_ = loadUiType('styles/admin_page - Copy.ui')

class Admin_Page_UI(QWidget, MainUI, Expensies):

    def __init__(self, admin_name, parent = None):
        super(Admin_Page_UI, self).__init__(parent)
        QWidget.__init__(self)
        x =  base64.decodebytes(H)
        m = QPixmap()
        m.loadFromData(x, 'png')
        self.setWindowIcon(QIcon(m)) 
        self.admin_name = admin_name
        self.setupUi(self)
        self.widget_changes()
        self.clicked_button()
        self.mamam()
        self.label_28.setText(f'Welcome MR {self.admin_name}')
        self.tableWidget_2.setStyleSheet(""""/*
thr field that i write table data in takes the same style as the QLineEdit
*/
  
QTableWidget{
background-color : #6c6c6c;
	alternate-background-color: #8c8c8c ;
font: normal normal bold 9pt "Segoe UI Black","Arial Black", "Bahij TheSansArabic"
,"Perpetua Titling MT", "Script MT Bold", "Traditional Arabic";
}

QTableWidget QLineEdit{
background-color:#272727;
border: 1px solid#aaaaaa;
font: normal normal bold 9pt "Segoe UI Black","ArialI Black", "Bahij TheSansArabic"
,"Perpetua Titling MT", "Script MT Bold", "Traditional Arabic";
color : white;
}

QTableWidget::item{
border : 0.5px solid #A40000;
border-radius : 1px;
color : white;
font: normal normal bold 9pt "Segoe UI Black","Arial Black","Bahij TheSansArabic"
,"Perpetua Titling MT", "Script MT Bold", "Traditional Arabic";
}

QTableWidget::item:focus{
background-color : rgb(255, 55, 55)
}

QHeaderView::section {
  background-color :#c20000;
  padding: 2px;
border : 1px solid transparent;
border-radius : 3px;
	margin-right : 1px;
margin-bottom : 1px;
font: 10pt "Segoe UI Black","Arial Black", "Bahij TheSansArabic","Perpetua Titling MT", "Script MT Bold", "Traditional Arabic";
color : white
}

QHeaderView::section:checked
{
font: 10pt  "Segoe UI Black","Arial Black", "Bahij TheSansArabic","Perpetua Titling MT", "Script MT Bold", "Traditional Arabic";
    background-color: #8b0000;
color : rgb(238, 238, 238);
}

QTableView QTableCornerButton::section{
background-color : transparent;
border : 1px solid  #A40000;
max-width : 5px
}


/*///////////////////////////////////////////////////////////////*/

""")

    def taboo0(self):
        if self.tabWidget.currentIndex() != 0:
            self.listWidget_2.clearSelection()
            self.listWidget_2.reset()
    def taboo1(self):
        if self.tabWidget.currentIndex() != 1:
            self.tableWidget.clearSelection()
            self.tableWidget.reset()
    def taboo2(self):
        if self.tabWidget.currentIndex() != 2:
            self.tableWidget_2.clearSelection()
            self.tableWidget_2.reset()
    def taboo3(self):
        if self.tabWidget.currentIndex() != 3:
            self.tableWidget_3.clearSelection()
            self.tableWidget_3.reset()
    def taboo4(self):
        if self.tabWidget.currentIndex() != 4:
            self.tableWidget_4.clearSelection()
            self.tableWidget_4.reset()
    def taboo5(self):    
        if self.tabWidget.currentIndex() != 5:
            self.tableWidget_5.clearSelection()
            self.tableWidget_5.reset()         

    def lamon(self, fun0, fun1, fun2, fun3, fun4, fun5 ):
        fun0()
        fun1()
        fun2()
        fun3()
        fun4()
        fun5()        

    def mamam(self):
        self.timer = QTimer()
        self.timer.timeout.connect(lambda : self.lamon(self.taboo0, self.taboo1, self.taboo2, self.taboo3, self.taboo4, self.taboo5))
        self.timer.start(500)

    def clicked_button(self):
# Food products buttons events
        self.Add_product_button.clicked.connect(self.add_procut_foods)
        self.Delete_row_foods.clicked.connect(self.delete_food_row)
# Users buttons events
        self.Delete_button.clicked.connect(self.delete_user_row)
        self.pushButton_2.clicked.connect(self.change_email)
# Consoles and Screens buttons events
        self.device_savechanges.setShortcut("Ctrl+S")
        self.device_savechanges.clicked.connect(self.save_new_additons_consolerdANDscreens)
        self.device_delete.clicked.connect(self.clean_row)
        self.clean_None_cells()
# Controllers list buttons events
        self.add_controller.clicked.connect(self.add_list_item)
        self.delete_controller.clicked.connect(self.delete_list_item)
# Yields buttons events
        self.Get_table_button.clicked.connect(self.show_yeild_table)
        self.rates_SearchBttn.clicked.connect(self.show_rates_execution)
        self.pushButton_5.clicked.connect(self.notes_save)
# Inventory Buttons
        self.pushButton.clicked.connect(self.inventory)

        self.tableWidget_3.doubleClicked.connect(self.show_storage)


    def widget_changes(self):
# Instant table showing 
        self.showing_table(self.tableWidget, "Users", "*", conn)
        self.showing_table(self.tableWidget_2, 'Consoles and Screens', 'Name, Model, Storage, Games, TV_company, TV_size, TV_resloution, Curved_or_Not, "Price/Hour", "Controller price/hour" ', conn)
        self.showing_table(self.tableWidget_3, "Foods", "*", conn)
        self.show_list_items()
# ------------------------
        self.yield_table_dateEdit.setDate(datetime.date.today())
        self.dateEdit.setDate(datetime.date.today())
        self.dateEdit_2.setDate(datetime.date.today())
        self.rates_changes()
        self.clock()
        self.notes_show()

        Expensies.__init__(self)

# Show the Storage widget from the Food table
    def show_storage(self):
        self.storage = Storage()
        self.storage.show()

#Inventory
    def inventory(self):
        try : 
            self.listWidget_2.clear()
            Cash_Count = []
            FoodCash = []
            HoursCash = []
            NotSeprated_Foods = []

            y1, m1, d1 = self.dateEdit.date().getDate()
            y2, m2, d2  = self.dateEdit_2.date().getDate()
            
            d1 = datetime.datetime(y1, m1, d1)
            d2 = datetime.datetime(y2, m2, d2)

            dif = (d2-d1).days

            Level_1 = []
            for i in range(dif + 1):
                x = datetime.timedelta(days=i)
                y = c2.execute(f'SELECT "Total Paid", "Food", "Paid for Hours", "Paid for Food" FROM "{(d1+x).date()}" ').fetchall()
                Cash_Count.append( sum([i[0] for i in y]) )
                HoursCash.append( sum( [i[2] for i in y] ) )
                FoodCash.append( sum([i[3] for i in y] ) )
                Level_1.extend([i[1].split(" / ") for i in y])

            for i in Level_1:
                NotSeprated_Foods.extend(i)


            Food_Inventory = []

            Food_Names = [i[0] for i in c.execute('SELECT Name FROM Foods ').fetchall()]

            for i in Food_Names:
                Level_0 =  list( filter(lambda x : x.split(":")[0] == i, NotSeprated_Foods) ) 

                OneItem_summ = [int(x.split(':')[1]) for x in Level_0]
                Food_Inventory.append(f'{i} : {sum(OneItem_summ)}')

            self.lineEdit.setText(f'{sum(Cash_Count)} EG')
            self.lineEdit_2.setText(f'{sum(FoodCash)} EG')
            self.lineEdit_3.setText(f'{sum(HoursCash)} EG')
            self.listWidget_2.addItems([i for i in Food_Inventory if i[-1] != "0"]) 
        except sqlite3.OperationalError as e:
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            msg = QMessageBox.warning(self.tab_5, "Unvalid Data Warining", f" Day {str(e).split(':')[1]} is not found", QMessageBox.Ok)


# Admin Notes
    def notes_show(self):
        with open('{}/users_notes/{}.txt'.format(os.getcwd().replace("\\", '/'), self.admin_name), 'r', encoding = "utf-8") as f:
            content = f.read()
        self.plainTextEdit_3.setPlainText(content)      

    
    def notes_save(self):
        content = self.plainTextEdit_3.toPlainText()
        with open('{}/users_notes/{}.txt'.format(os.getcwd().replace("\\", '/') ,self.admin_name), 'w', encoding = "utf-8") as f2:
            f2.write(content)
            
# Clock
    def clock(self):
        self.label_30.setText(datetime.datetime.now().time().strftime('%I:%M:%S'))
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(lambda : self.label_30.setText(datetime.datetime.now().time().strftime('%I:%M:%S')) )
        self.clock_timer.start(1000)

# Rates Methods
    def rates_changes(self):
        users_names = [i[0] for i in c.execute('SELECT User_Name FROM Users').fetchall()]
        self.rates_comboBox.addItems(users_names[1:])
        self.comboBox.addItem("All")
        self.comboBox_2.addItem("All")

        try:
            years = list( { i[-1].split('-')[0] for i in c2.execute(f'SELECT * FROM users_rates').fetchall() } )
            months = list( { i[-1].split('-')[1] for i in c2.execute(f'SELECT * FROM users_rates').fetchall() } )
            years.sort()
            months.sort()
            self.comboBox.addItems(years)
            self.comboBox_2.addItems(months)
        except IndexError:
            pass


    def show_rates(self, RatesINeed,  DateSelection):
        embty = []
        table_names = [i[0] for i in c2.execute(f'SELECT name FROM sqlite_master WHERE name LIKE "{DateSelection}"').fetchall()]
        for i in table_names:
            embty.extend([x[0] for x in c2.execute(f'SELECT "Total Paid" FROM "{i}" WHERE "User Name" = "{self.rates_comboBox.currentText()}" ').fetchall()])

        Number_of_Clients = [i[0] for i in c2.execute(f'SELECT clients_numbers FROM users_rates WHERE {RatesINeed} ').fetchall()]
        Number_of_Days = c2.execute(f'SELECT COUNT(*) FROM users_rates WHERE {RatesINeed} ').fetchone()[0]
        average = sum(Number_of_Clients)
        conn2 = sqlite3.connect('styles/yields.db')
        self.showing_table(self.tableWidget_5, "users_rates", "*", conn2, f'WHERE {RatesINeed} ')
        self.rates_UserName.setText(f'User Name: {self.rates_comboBox.currentText()}')
        self.label.setText(f'Total Yields Made : {sum(embty)} EG')
        try:
            self.rates_average.setText(f'Average Clients / Day : {average//Number_of_Days}')
        except ZeroDivisionError:
            self.rates_average.setText(f'Average Clients / Day : 0 ')


    def show_rates_execution(self):
        if self.comboBox.currentText() == "All" and self.comboBox_2.currentText() == "All":
            self.show_rates(f'user_name = "{self.rates_comboBox.currentText()}" ', "2%")

        elif self.comboBox.currentText() == "All" and self.comboBox_2.currentText() != "All":
            self.show_rates(f'user_name = "{self.rates_comboBox.currentText()}" AND date LIKE "%-{self.comboBox_2.currentText()}-%" ', 
                            f'%-{self.comboBox_2.currentText()}-%')

        elif self.comboBox.currentText() != "All" and self.comboBox_2.currentText() == "All":
            self.show_rates(f'user_name = "{self.rates_comboBox.currentText()}" AND date LIKE "{self.comboBox.currentText()}%" ', 
                            f'{self.comboBox.currentText()}%')

        elif self.comboBox.currentText() != "All" and self.comboBox_2.currentText() != "All":
            self.show_rates(f'user_name = "{self.rates_comboBox.currentText()}" AND date LIKE "{self.comboBox.currentText()}-{self.comboBox_2.currentText()}-%" ', 
                            f'{self.comboBox.currentText()}-{self.comboBox_2.currentText()}-%')


# General Showing Table method 
    def showing_table(self, pyq_tbale , sql_tbale, query, database_connection, codition = None):
        Rnums = database_connection.cursor().execute(f'SELECT COUNT(*) FROM "{sql_tbale}" {codition} ').fetchone()
        pyq_tbale.setRowCount(int(Rnums[0]))
        exe_show = database_connection.cursor().execute(f'SELECT {query} FROM "{sql_tbale}" {codition} ')
        result = exe_show.fetchall()
        row_index = 0
        culomn_index =0       
        for row in result:
            for element in row:
                pyq_tbale.setItem(row_index, culomn_index, QTableWidgetItem(f"{str(element)}"))
                culomn_index+=1
            culomn_index = 0
            row_index +=1

# Users Methods
    # General row deleting method -- Deleting users method --
    def delete_user_row(self):
        try:
            if self.tableWidget.currentRow() != 0:
                user_name = self.tableWidget.item(self.tableWidget.currentRow(), 0 ).text()
                msg1 = QMessageBox.question(self.Users_tab, 'Question Message', f'Are you sure you want to delete "{user_name}" from Users table ?', QMessageBox.Yes|QMessageBox.No)
                if msg1 == QMessageBox.Yes:
                    c.execute(f"DELETE FROM Users WHERE User_Name = '{user_name}' ")
                    conn.commit()
                    self.tableWidget.removeRow(self.tableWidget.currentRow())
                    self.tableWidget.clearSelection()
                    self.tableWidget.reset()
                else :
                    self.tableWidget.clearSelection()
                    self.tableWidget.reset()
                    pass
            else :
                msg2 = QMessageBox.warning(self.Users_tab, "Warning Message", "You can't delete the admin ! ", QMessageBox.Ok)
                self.tableWidget.clearSelection()
                self.tableWidget.reset()
                pass
        except AttributeError:
            msg3 = QMessageBox.information(self.Users_tab, 'Informative Message', 'Please make sure you have selected the row you want to delete.', QMessageBox.Ok)

    def change_email(self):
        if self.lineEdit_4.text():
            admin_name  = c.execute("SELECT User_Name FROM Users").fetchone()[0]
            msg = QMessageBox.question(self.Users_tab, 'Question Message', f'Are you sure you want to change your email to "{self.lineEdit_4.text()}"',
            QMessageBox.Yes|QMessageBox.No)
            if msg == QMessageBox.Yes:
                c.execute(f'Update Users SET Email = "{self.lineEdit_4.text()}" WHERE User_Name = "{admin_name}" ')
                conn.commit()
                self.lineEdit_4.clear()
                self.showing_table(self.tableWidget, "Users", "*", conn)


        

# Cleaning methods
    def clean_None_cells(self):
        row_index = 0
        column_index = 0
        for _ in range(18):
            for _ in range(10):
                if self.tableWidget_2.item(row_index, column_index).text() == "None":
                    self.tableWidget_2.setItem(row_index, column_index, QTableWidgetItem(""))
                column_index +=1      
            column_index = 0
            row_index +=1  
    
    def clean_row(self):
        column_index = 0
        index = 0 
        exe = [i[1] for i in c.execute('PRAGMA table_info("Consoles and screens")').fetchall()]
        exe.remove("ID")
        row_index = self.tableWidget_2.currentRow()
        if row_index >= 0:
            row_name  = self.tableWidget_2.item(row_index, 0).text()
            msg1 = QMessageBox.question(self.tab_2, 'Question Message', f'Are you sure you want to clean "{row_name}" row ?', QMessageBox.Yes|QMessageBox.No)
            if msg1 == QMessageBox.Yes:
                for _ in range(10):
                    c.execute(f'UPDATE "Consoles and screens" SET "{exe[index]}" = "" WHERE ID = {row_index + 1}')
                    index += 1
                conn.commit()
                for _ in range(10):
                    self.tableWidget_2.setItem(row_index, column_index, QTableWidgetItem(""))
                    column_index += 1
            else : 
                self.tableWidget_2.clearSelection()
                self.tableWidget_2.reset()
                pass
        else:
            QMessageBox.information(self.tab_2, 'Informative Message', 'Please, Make sure you have selected the row you want to clean', QMessageBox.Ok)

# Consoles and Screens methods 
    def save_new_additons_consolerdANDscreens(self):
        prices = []
        Unvalid_prices = []
        prices_indexes = 0
        for i in range(self.tableWidget_2.rowCount()):
            prices.append(self.tableWidget_2.item(prices_indexes, 8).text())
            prices.append(self.tableWidget_2.item(prices_indexes, 9).text())
            prices_indexes += 1

        for item in prices :
            Unvalid_prices.append(any([ch not in string.digits and ch != "." and ch != "" for ch in item]))

        if any(Unvalid_prices):
            msg1 = QMessageBox.warning(self.tab_2, 'Warning Message', 'Make sure Price/Hour & Controllers Price/Hour column cells are embty or contain numbers only', QMessageBox.Ok)
            
        else :
            index = 0
            row_index = 0
            column_index = 0
            ID_index = 1
            exe = [i[1] for i in c.execute('PRAGMA table_info("Consoles and screens")').fetchall()]
            exe.remove("ID")
            msg2 = QMessageBox.question(self.tab_2, 'Question Message', 'Are you sure you want to Save these additions ?', QMessageBox.Yes|QMessageBox.No)
            if msg2 == QMessageBox.Yes:
                for _ in range(18):
                    for _ in range(10):
                        c.execute(f'UPDATE "Consoles and screens" SET "{exe[index]}" = "{self.tableWidget_2.item(row_index, column_index).text()}" WHERE ID = {ID_index}') 
                        index += 1
                        column_index +=1
                    index = 0
                    column_index = 0
                    row_index +=1
                    ID_index += 1
            conn.commit()

        

# Controllers list methods
    def show_list_items(self):
        items = [i[0] for i in c.execute('SELECT * FROM Controllers ORDER BY controller').fetchall()]
        self.listWidget.addItems(items)
    
    def add_list_item(self):
        if self.add_controller_input.text():
            self.listWidget.addItem(self.add_controller_input.text())
            c.execute(f'INSERT INTO Controllers VALUES("{self.add_controller_input.text()}")')
            conn.commit()
            self.add_controller_input.setText("")

    def delete_list_item(self):
        try :
            if self.listWidget.count() != 0:
                row_index  = self.listWidget.currentRow()
                c.execute(f'DELETE FROM Controllers WHERE controller = "{self.listWidget.item(row_index).text()}" ')
                conn.commit()
                self.listWidget.takeItem(row_index)
            else :
                msg1 = QMessageBox.information(self.tab_2, 'Informative Message', "You can't delete items from an embty list.", QMessageBox.Ok)
        except AttributeError :
            msg2 = QMessageBox.information(self.tab_2, 'Informative Message', 'Please, Make sure you have selected the row you want to delete', QMessageBox.Ok)



# Food products methods
    def add_procut_foods(self):
        if self.Product_name_input.text():
            name = self.Product_name_input.text()
            price = self.Price_doublespinbox.value()
            c.execute(f'INSERT INTO Foods VALUES ("{name}",  {price})')
            conn.commit()
            self.Product_name_input.setText("")
            self.Price_doublespinbox.setValue(0.00)
            self.showing_table(self.tableWidget_3, "Foods", "*", conn)

    def delete_food_row(self):
        try:
            if self.tableWidget_3.rowCount() != 0 :
                product_name = self.tableWidget_3.item(self.tableWidget_3.currentRow(), 0).text()
                msg1 = QMessageBox.question(self.Users_tab, 'QuestionMEssage', f'Are you sure you want to delete "{product_name}" from Foods ?', QMessageBox.Yes|QMessageBox.No)
                if msg1 == QMessageBox.Yes:
                    food_name = self.tableWidget_3.item(self.tableWidget_3.currentRow(), 0).text()
                    c.execute(f"DELETE FROM Foods WHERE Name = '{food_name}' ")
                    conn.commit()
                    self.tableWidget_3.removeRow(self.tableWidget_3.currentRow())
                    self.tableWidget_3.clearSelection()
                    self.tableWidget_3.reset()
                else : 
                    self.tableWidget_3.clearSelection()
                    self.tableWidget_3.reset()                    
                    pass
            else : 
                msg3 = QMessageBox.information(self.tab_2, 'Informative Message', "You can't delete items from an embty table.", QMessageBox.Ok)
                self.tableWidget_3.clearSelection()
                self.tableWidget_3.reset()
                pass
        except AttributeError:
            msg2 = QMessageBox.information(self.tab_3, 'Informative Message', 'Please make sure you have selected the row you want to delete.', QMessageBox.Ok)

# SPECIAL Showing yields table method
    def show_yeild_table(self):
        conn2 = sqlite3.connect("styles/yields.db")
        c2 = conn2.cursor()
        y, m, d = self.yield_table_dateEdit.date().getDate()
        date = str(datetime.date(y, m, d))
        table_names = [i[0] for i in c2.execute("SELECT name FROM sqlite_master WHERE name NOT LIKE 'sqlite%' ").fetchall()]
         
        if date in table_names :
            self.showing_table(self.tableWidget_4, date, "*", conn2)
            self.Table_date_label.setText(f'Table Date: {date}')
        else:
            msg = QMessageBox.information(self.tab_4, "Informative Message", "Table Can't be found", QMessageBox.Ok)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Admin_Page_UI('holder')
    window.showMaximized()
    app.exec_()


 
