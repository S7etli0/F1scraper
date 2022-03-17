import time
import datetime
import mysql.connector as con

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QSpinBox, QHBoxLayout, QPushButton, \
    QComboBox, QMessageBox, QTableWidget, QVBoxLayout, QHeaderView, QLabel, QTableWidgetItem, \
    QProgressBar, QSizePolicy, QSpacerItem, QRadioButton, QButtonGroup

mydb = con.connect(
    host="localhost",
    user="root",
    passwd="Slav7528dokumape"
)

class InnerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tables Menu")
        self.setGeometry(200,200,200,200)
        self.setWindowIcon(QIcon("imgpics/f1-logo.png"))

# check whole page
# pictures,font,align
# Innertab layout, Keys
# remove repeats, set values
# 1956, resize
# descriptions
# methods
# sort

css_Style = """

    QWidget#TabTitel{ 
        font-size:20px; 
    } 
    
    QPushButton{ 
        font-size:16px;
    } 

"""

class DataF1Table(QWidget):
    def __init__(self):
        super().__init__()
        self.VisualTab()

    def VisualTab(self):
        self.setWindowTitle("Formula1 Data")
        self.setWindowIcon(QIcon("imgpics/f1-logo.png"))
        self.setGeometry(100, 100, 350, 350)
        self.TabContent()
        self.show()

    def TabContent(self):
        lay = QHBoxLayout()

        self.spinlbl = QLabel("Set year:")
        self.spinyear = QSpinBox()
        year = datetime.datetime.now().strftime("%Y")
        self.spinyear.setRange(1950, int(year) - 1)

        self.datalbl = QLabel("Set data:")
        self.combo = QComboBox()
        sections = ['calender', 'race wins', 'driver ranks', 'team ranks']
        self.combo.addItems(sections)

        btn = QPushButton("Load Data")
        btn.clicked.connect(self.race_results)

        lay.addStretch()
        lay.addWidget(self.spinlbl)
        lay.addWidget(self.spinyear)
        lay.addWidget(self.datalbl)
        lay.addWidget(self.combo)
        lay.addWidget(btn)
        lay.addStretch()

        self.rows = 0
        self.cols = 0
        self.sortbool = False
        self.tablemade = False
        self.tablay = QHBoxLayout()
        self.sortlay = QHBoxLayout()
        self.sortlay.setAlignment(Qt.AlignCenter)
        self.sortwid = QWidget()

        self.wid = QVBoxLayout()
        self.wid.addLayout(lay)
        self.titel = QLabel("The Results You are Looking For will Appear in a Table")
        self.titel.setAlignment(Qt.AlignCenter)
        self.titel.setObjectName("TabTitel")
        self.wid.addWidget(self.titel)

        self.introlbl = QLabel()
        self.myImage('startup',False)
        self.wid.addWidget(self.introlbl)

        self.wid.addLayout(self.tablay)

        self.savedata = QPushButton("Save SQL")
        self.savedata.clicked.connect(self.SQLsave)
        self.wid.addWidget(self.savedata)
        self.savedata.setVisible(False)
        self.wid.addWidget(self.sortwid)

        viewdata = QPushButton("View Data")
        viewdata.clicked.connect(self.SQLoptions)
        self.wid.addWidget(viewdata)

        self.loadtab = QProgressBar()
        self.loadtab.setMinimum(0)
        self.loadtab.setMaximum(5)
        self.loadtab.setVisible(False)
        self.wid.addWidget(self.loadtab)
        self.setLayout(self.wid)

    def race_results(self):
        if self.sortbool == True:
            self.clearLay(self.sortlay)
            self.sortbool = False
            self.sortwid.setVisible(False)

        self.calender = int(self.spinyear.text())
        self.data = str(self.combo.currentText())

        if self.data == "team ranks" and self.calender < 1958:
            QMessageBox.about(self, "Data Error", "No team Competitions before 1958!")
        else:

            if self.data == "calender" or self.data == "race wins":
                extra = ['races']
                var = 8
            elif self.data == 'driver ranks':
                extra = ['drivers']
                var = 7
            else:
                extra = ['drivers', 'team']
                var = 3
                dict = {}

            for sector in extra:

                driver = webdriver.Chrome()
                website = "https://www.formula1.com/en/results.html/{}/{}.html".format(self.calender, sector)
                driver.get(website)

                webpage = driver.find_element(By.TAG_NAME, "body")
                numbers=[]

                pages = 5
                while pages:
                    webpage.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.5)
                    pages -= 1
                    self.progressload(pages)


                if self.data == 'calender':
                    self.tabheader = ['country', 'date', 'laps', 'duration']
                    numbers = [0,1,6,7]

                elif self.data == 'race wins':
                    self.tabheader = ['country', 'first_name', 'last_name', 'nickname', 'team_name']
                    numbers = [0,2,3,4,5]

                elif self.data == 'driver ranks':
                    self.tabheader = ['first_name', 'last_name', 'nationality', 'team_name', 'points']
                    numbers = [1,2,4,5,6]

                else:
                    self.tabheader = ['team_name', 'drivers', 'points']

                soup = BeautifulSoup(driver.page_source, "lxml")
                table = soup.find("tbody")

                self.content = []
                for td in table.find_all("tr"):
                    racelist = td.text.strip().replace("\n", "/").replace("     ", "").strip("").split("/")
                    racelist = list(filter(lambda x: x != '', racelist))

                    while len(racelist)<var:
                        racelist.append("")

                    if self.data=="team ranks":
                        if sector == "drivers":
                            if racelist[5] not in dict:
                                dict[racelist[5]] = str(racelist[1]) + " " + str(racelist[2])
                            else:
                                dict[racelist[5]] += " & " + str(racelist[1]) + " " + str(racelist[2])

                        else:
                            rowdatas = []
                            rowdatas.append(racelist[1])
                            if racelist[1] in dict:
                                rowdatas.append(dict[str(racelist[1])])
                            else:
                                rowdatas.append("")
                            rowdatas.append(racelist[2])
                            self.content.append(rowdatas)

                    else:
                        rowdatas = []
                        for cell in numbers:
                            rowdatas.append(racelist[cell])
                        self.content.append(rowdatas)

            if self.tablemade==False:
                self.makeTable()

            self.myImage(self.data.replace(" ","-"),False)
            self.titel.setText("List of the " + self.data + " for the " + str(self.calender) + " Formula 1 Season")
            self.cols = int(len(self.tabheader))
            self.rows = int(len(self.content))

            self.savedata.setVisible(True)
            self.fillTable(self.rows,self.cols,self.content,self.tabheader)
            order = []
            for i in range(self.rows):
                order.append(str(i+1))
            self.table.setVerticalHeaderLabels(order)
            driver.quit()


    def SQLsave(self):
        if self.rows==0 or self.cols==0:
            QMessageBox.about(self,"Table Error","No data has been added!")
        else:
            # curs = mydb.cursor()
            # curs.execute("CREATE DATABASE IF NOT EXISTS formula1")
            # mydb.commit()

            name = (self.data + " " + str(self.calender)).replace(" ", "_")
            ask = QMessageBox.question(self, "Saving Table",
                        "Do you want to save table " + name + " ?", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)

            if ask == QMessageBox.Yes:

                curs = mydb.cursor()
                curs.execute("USE formula1")
                curs.execute("SHOW TABLES")

                alltables = []
                for x in curs:
                    clear = (str(x)[1:-1].replace(",", ""))
                    alltables.append(clear.replace("'", ""))
                mydb.commit()

                stock = []
                if name not in alltables:

                    curs = mydb.cursor()
                    curs.execute("USE formula1")

                    curs.execute("CREATE TABLE IF NOT EXISTS " + name + " (id int PRIMARY KEY AUTO_INCREMENT)")
                    for x in range(self.cols):
                        curs.execute("ALTER TABLE " + name + " ADD " + self.tabheader[x] + " VARCHAR(125)")

                    rep = []
                    for x in range(self.cols):
                        rep.append("%s")

                    datatag = str(self.tabheader)[1:-1].replace("'", "")
                    datavalue = str(rep)[1:-1].replace("'", "")
                    formula = "INSERT INTO " + name + " (" + datatag + ") VALUES (" + datavalue + ")"

                    for x in range(self.rows):
                        line = []
                        for y in range(self.cols):
                            line.append(self.content[x][y])
                        stock.append(line)

                    curs.executemany(formula, stock)
                    mydb.commit()

                    QMessageBox.about(self, "SQL Table", "The table was added to the database!")

                else:
                    QMessageBox.about(self, "SQL error", "The table is already in the database!")
            else:
                pass


    def getList(self):
        curs = mydb.cursor()
        curs.execute("USE formula1")
        curs.execute("SHOW TABLES")
        listname = self.sender().text()

        self.clearLay(self.innerlay)
        self.allcontent = []
        for x in curs:
            titel = str(x)[1:-1].replace(",", "")
            if listname in titel:
                self.allcontent.append(titel.replace("'", "")[len(titel)-6:len(titel)])

        maintag = QLabel("Category "+str(listname).replace("_"," ").title()+" Tables")
        maintag.setAlignment(Qt.AlignCenter)
        self.innerlay.addWidget(maintag)
        self.myImage('menu',True)

        lbltag = QLabel("Select year")
        self.listing = QComboBox()
        self.listing.addItems(self.allcontent)
        twoinone = QHBoxLayout()
        twoinone.addWidget(lbltag)
        twoinone.addWidget(self.listing)
        twolinewid = QWidget()
        twolinewid.setLayout(twoinone)
        self.innerlay.addWidget(twolinewid)

        btn = QPushButton("Load data in Table")
        btn.clicked.connect(self.getSQLtab)
        self.innerlay.addWidget(btn)

        # verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.innerlay.addItem(verticalSpacer)

        erase = QPushButton("Erase Table")
        erase.clicked.connect(self.eraseTab)
        self.innerlay.addWidget(erase)
        self.listvar = listname

        backbtn = QPushButton("Back to Menu")
        backbtn.clicked.connect(self.SQLoptions)
        self.innerlay.addWidget(backbtn)


    def getSQLtab(self):
        self.ref = self.listvar+"_"+str(self.listing.currentText())
        curs = mydb.cursor()
        curs.execute("SELECT * FROM "+self.ref)

        self.listSet(curs)
        if self.tablemade == False:
            self.makeTable()

        self.colname = []
        curs = mydb.cursor()
        curs.execute("SHOW COLUMNS FROM "+self.ref)
        for x in curs:
            self.colname.append(list(x)[0])
        self.colname.pop(0)
        self.cols = len(self.colname)

        self.myImage(self.listvar.replace("_", "-"),False)

        mytitle = self.ref.split("_")
        if len(mytitle)>2:
            self.titel.setText("List of the " + mytitle[0] + " " + mytitle[1] + " for the " + mytitle[2] + " Formula 1 Season")
        else:
            self.titel.setText("List of the " + mytitle[0] + " for the " + mytitle[1] + " Formula 1 Season")

        self.table.setVerticalHeaderLabels(self.vertic)
        self.savedata.setVisible(False)
        self.fillTable(self.rows, self.cols, self.transfer,  self.colname)

        if self.sortbool == True:
            self.clearLay(self.sortlay)
            self.sortbool = False

        if self.sortbool == False:
            self.sortwid.setVisible(True)
            sortlbl = QLabel("Sort data by")
            self.sortbox = QComboBox()

            if "race" in self.ref:
                self.colname.append("id")
            self.sortbox.addItems(self.colname)

            order = QLabel("Order by")
            self.asc = QRadioButton("ASC")
            self.des = QRadioButton("DESC")
            gr = QButtonGroup()
            gr.addButton(self.asc)
            gr.addButton(self.des)

            sortbtn = QPushButton("Sort Table")
            sortbtn.clicked.connect(self.sorting)

            # self.sortlay.addStretch()
            self.sortlay.addWidget(sortlbl)
            self.sortlay.addWidget(self.sortbox)
            self.sortlay.addWidget(order)
            self.sortlay.addWidget(self.asc)
            self.sortlay.addWidget(self.des)
            self.sortlay.addWidget(sortbtn)
            # self.sortlay.addStretch()

            self.sortwid.setLayout(self.sortlay)
            self.sortbool = True


    def SQLoptions(self):
        further=True
        options = self.sender().text()

        if options == "View Data":
            self.sqltabs = InnerTab()
            self.innerlay = QVBoxLayout()
        else:
            self.clearLay(self.innerlay)
            further = False

        sqltitel = QLabel("Choose a Table Category")
        sqltitel.setAlignment(Qt.AlignCenter)
        self.innerlay.addWidget(sqltitel)

        self.myImage('menu', True)
        sections = ['calender', 'race_wins', 'driver_ranks', 'team_ranks']
        for x in sections:
            btn = QPushButton(str(x))
            btn.clicked.connect(self.getList)
            self.innerlay.addWidget(btn)

        if further==True:
            self.sqltabs.setLayout(self.innerlay)
            self.sqltabs.show()


    def makeTable(self):
        self.tablemade = True
        self.table = QTableWidget()
        self.table.setRowCount(self.rows)
        self.table.setColumnCount(self.cols)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.tablay.addWidget(self.table)

    def progressload(self,pages):
        self.loadtab.setVisible(True)

        if pages!=0:
            self.loadtab.setValue(5-pages)
        else:
            self.loadtab.setVisible(False)

    def eraseTab(self):
        year = str(self.listing.currentText())
        deltab= self.listvar+"_"+year
        ask = QMessageBox.question(self,"Delete Table",
                "Do you want to drop table "+deltab+" ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if ask == QMessageBox.Yes:
            curs = mydb.cursor()
            curs.execute("USE formula1")
            curs.execute("DROP TABLE " + deltab)
            mydb.commit()
            QMessageBox.about(self,"Delete Table","The table was erased from the database!")
            self.SQLoptions()
        else:
            pass

    def myImage(self,imagelist,look):
        intropic = QPixmap("imgpics/f1-" + imagelist + ".jpg")

        if look == True:
            self.sqlpic = QLabel()
            self.sqlpic.setPixmap(intropic.scaled(260, 110, Qt.KeepAspectRatio))
            self.sqlpic.setAlignment(Qt.AlignCenter)
            self.innerlay.addWidget(self.sqlpic)
        else:
            self.introlbl.setPixmap(intropic)
            self.introlbl.setAlignment(Qt.AlignCenter)


    def fillTable(self, tabrow, tabcol, filler, myheader):
        self.table.setRowCount(tabrow)
        self.table.setColumnCount(tabcol)

        for rw in range(tabrow):
            for cl in range(tabcol):
                self.table.setItem(rw, cl, QTableWidgetItem(str(filler[rw][cl])))

        width=100
        for i in range(tabcol):
            width+=int(self.table.columnWidth(i))

        height = 35 * tabrow + 150
        if tabrow < 12:
            height += 300
        elif tabrow > 24:
            height -= 200
        elif tabrow > 20:
            height -= 100
        else:
            height += 100

        header = self.table.horizontalHeader()


        if self.cols>3:
            st=3
        else:
            st=1

        for i in range(st,tabcol-1):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        header.setSectionResizeMode(tabcol-1,QHeaderView.ResizeToContents)

        # header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.table.setHorizontalHeaderLabels(myheader)

        if 'calender' not in self.titel.text():
            header.setStretchLastSection(False)
        else:
            header.setStretchLastSection(True)
            width=width-100
        self.setGeometry(100,100,width,height)


    def sorting(self):
        direct=""
        if self.asc.isChecked():
            direct=self.asc.text()
        elif self.des.isChecked():
            direct=self.des.text()

        sorter = self.sortbox.currentText()
        curs = mydb.cursor()
        curs.execute("USE formula1")
        if sorter=="date" or sorter=="id" or sorter=="points":
            curs.execute("SELECT * FROM "+self.ref+" ORDER BY id"+" "+direct)
        elif sorter=="laps":
            curs.execute("SELECT * FROM "+self.ref+" ORDER BY ABS("+sorter+") "+direct)
        else:
            curs.execute("SELECT * FROM "+self.ref+" ORDER BY "+sorter+" "+direct)


        self.listSet(curs)
        self.table.setVerticalHeaderLabels(self.vertic)
        self.savedata.setVisible(False)
        self.fillTable(self.rows, self.cols, self.transfer, self.colname)

    def clearLay(self, layout):
        for i in reversed(range(layout.count())):
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().setParent(None)

    def listSet(self,curs):
        self.transfer=[]
        self.vertic=[]
        for x in curs:
            self.transfer.append(x[1:len(x)])
            self.vertic.append(str(x[0]))
        self.rows = len(self.transfer)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(css_Style)
    window = DataF1Table()
    sys.exit(app.exec_())
