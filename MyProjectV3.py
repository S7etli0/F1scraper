import time
import datetime
import mysql.connector as con

import requests
from bs4 import BeautifulSoup as soup

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtWidgets import QWidget, QTabWidget, QApplication, QProgressBar, QScrollArea, \
    QTableWidget, QTableWidgetItem, QHeaderView, QGridLayout, QVBoxLayout, QHBoxLayout, \
    QPushButton, QRadioButton, QButtonGroup, QLabel, QComboBox, QSpinBox, QMessageBox


mydb = con.connect(
    host="localhost",
    user="root",
    passwd="Slav7528dokumape"
)

# check whole page
# pictures,font,align
# Innertab layout, Keys
# 1956, resize, sort
# out methods, def
# remove repeats
# descriptions
# set values
# request + soup
# classes

css_Style = """

    QWidget#RedWid{
        background-color: red;
    }
    
    QWidget#BlackWid{
        background-color: black;
    }

    QWidget#White, QComboBox{
        background-color: white;
        font-size: 14px;
    }    
    
    QWidget, QPushButton, QLabel{ 
        font-size: 16px;
        border-radius: 10px;
    }
    
    QPushButton, QRadioButton, QLabel#RedLab, QLabel#Titel, QLabel#BlackLab, QLabel#Titel{ 
        color: white;
    }
    
    QLabel#BlackLab, QLabel#Titel{ 
        background-color: black;
        border: 5px solid black;
    }
    
    QLabel#Titel{ 
        font-size: 20px;
    }
    
    QLabel#RedLab{ 
        background-color: red;
        border: 5px solid red;
    }
    
    QPushButton{ 
        background-color: black;
        border: 5px solid black;
    }
    
    QPushButton#RedBtn, QPushButton#Mar{ 
        background-color: red;
        border: 5px solid red;
    }
    
    QPushButton:hover{
        font-size: 20px;
    }
    
    QPushButton:pressed, QPushButton#RedBtn:pressed, QPushButton#Mar:pressed{
        color: white;
        background-color: darkred;
        border: 5px solid darkred;
    }
    
    QPushButton#Mar{
        margin-top: 10px;        
    }

"""


class DataF1Table(QWidget):
    def __init__(self):
        super().__init__()
        self.VisualTab()

    def VisualTab(self):
        self.setWindowTitle("Formula1 Data V3")
        self.setWindowIcon(QIcon("imgpics/f1-logo.png"))
        self.setGeometry(100, 100, 350, 350)
        self.sideSQLtab()
        self.setMainTab()
        self.sideWEBtab()
        self.setObjectName("RedWid")
        self.show()

    def sideSQLtab(self):
        self.sqltabs = QWidget()
        self.innerlay = QVBoxLayout()
        self.sqltabs.setLayout(self.innerlay)
        self.goBack()

    def setMainTab(self):
        self.rows = 0
        self.cols = 0
        self.tablemade = False
        self.sortbool = False
        self.tablay = QVBoxLayout()
        self.sortlay = QHBoxLayout()
        self.sortlay.setAlignment(Qt.AlignCenter)

        self.sorthide=True
        self.sortwid = QWidget()
        self.sortwid.setObjectName("BlackWid")

        self.mainwid = QVBoxLayout()
        self.titel = QLabel("The Results You are Looking For will Appear in a Table")
        self.titel.setAlignment(Qt.AlignCenter)
        self.titel.setObjectName("Titel")
        self.mainwid.addWidget(self.titel)

        self.introlbl = QLabel()
        self.myImage('startup', 0)
        self.mainwid.addWidget(self.introlbl)

        self.mainwid.addLayout(self.tablay)
        self.mainwid.addWidget(self.sortwid)
        # self.stretcher(self.mainwid)

        self.loadtab = QProgressBar()
        self.loadtab.setMinimum(0)
        self.loadtab.setMaximum(5)
        self.loadtab.setVisible(False)
        self.mainwid.addWidget(self.loadtab)


    def sideWEBtab(self):
        self.mygrid = QGridLayout()
        self.tabright = QWidget()
        self.tabright.setObjectName("White")
        self.tabright.setLayout(self.mainwid)
        self.mygrid.addWidget(self.tabright, 0, 1)

        self.layload = QVBoxLayout()
        loadwid = QWidget()
        loadwid.setLayout(self.layload)

        self.myImage('menu', 4)
        firstrow = QHBoxLayout()
        self.spinlbl = QLabel("Set year:")
        self.spinlbl.setObjectName("RedLab")
        self.spinyear = QSpinBox()
        year = datetime.datetime.now().strftime("%Y")
        self.spinyear.setRange(1950, int(year) - 1)
        firstrow.addWidget(self.spinlbl)
        firstrow.addWidget(self.spinyear)

        secrow = QHBoxLayout()
        self.datalbl = QLabel("Set data:")
        self.datalbl.setObjectName("RedLab")
        self.combo = QComboBox()
        sections = ['calender', 'race wins', 'driver ranks', 'team ranks']
        self.combo.addItems(sections)
        secrow.addWidget(self.datalbl)
        secrow.addWidget(self.combo)

        btn = QPushButton("Load Data in Table")
        btn.setObjectName("Mar")
        btn.clicked.connect(self.race_results)

        self.savelbl = QLabel()
        self.myImage('saves', 2)
        self.savelbl.setVisible(False)

        self.savedata = QPushButton("Create SQL Table")
        self.savedata.clicked.connect(self.SQLsave)
        self.mainwid.addWidget(self.savedata)
        self.savedata.setVisible(False)

        doubwid = QWidget()
        doubwid.setObjectName("BlackWid")
        doublay = QVBoxLayout()
        doubwid.setLayout(doublay)

        firstlay = QWidget()
        firstlay.setLayout(firstrow)
        seclay = QWidget()
        seclay.setLayout(secrow)
        doublay.addWidget(firstlay)
        doublay.addWidget(seclay)

        self.layload.addWidget(doubwid)
        self.layload.addWidget(btn)

        clearlab = QLabel()
        self.layload.addWidget(clearlab)

        self.layload.addWidget(self.savelbl)
        self.layload.addWidget(self.savedata)
        self.layload.addStretch()

        self.maintab = QTabWidget()
        self.maintab.setMaximumWidth(270)
        self.maintab.addTab(loadwid, "Load Data")
        self.maintab.addTab(self.sqltabs, "View Data")
        self.mygrid.addWidget(self.maintab, 0, 0)

        self.setLayout(self.mygrid)

    def race_results(self):

        if self.sortbool == True:
            self.clearLay(self.sortlay)
            self.sorthide=True
            self.sortwid.setVisible(False)
            self.erase.setVisible(False)
            self.eraselbl.setVisible(False)
            self.sortbool = False

        self.calender = int(self.spinyear.text())
        self.data = str(self.combo.currentText())
        self.fullnames = {}

        if self.data == "team ranks" and self.calender < 1958:
            QMessageBox.about(self, "Data Error", "No team Competitions before 1958!")
        else:

            self.savedata.setVisible(True)
            self.savelbl.setVisible(True)
            links, var, self.tabheader, numbers = self.MultipleData()

            for sector in links:

                website = "https://www.formula1.com/en/results.html/{}/{}.html".format(self.calender, sector)

                pages = 7
                while pages:
                    time.sleep(0.5)
                    pages -= 1
                    self.progressload(pages)

                rec = requests.get(website)
                site_html = rec.text
                crawler = soup(site_html, 'lxml')
                table = soup.select(crawler, "tbody>tr")

                self.content = []

                for td in table:
                    racelist = td.text.strip().replace("\n", "/").replace("     ", "").strip("").split("/")
                    racelist = list(filter(lambda x: x != '', racelist))

                    while len(racelist) < var:
                        racelist.append("")

                    if self.data == "team ranks":
                        if sector == "drivers":

                            if racelist[5] not in numbers:
                                numbers[racelist[5]] = str(racelist[1]) + " " + str(racelist[2])
                                # numbers[racelist[5]] = str(racelist[3])
                                # self.fullnames[racelist[5]] = str(racelist[1]) + " " + str(racelist[2])
                            else:
                            # elif str(numbers[racelist[5]]).count('&') < 3:
                                numbers[racelist[5]] += " & " +str(racelist[1]) + " " + str(racelist[2])
                                # numbers[racelist[5]] += " & " + str(racelist[3])
                                # self.fullnames[racelist[5]] += " & " +str(racelist[1]) + " " + str(racelist[2])

                        else:
                            rowdatas = []
                            rowdatas.append(racelist[1])
                            if racelist[1] in numbers:
                                rowdatas.append(numbers[str(racelist[1])])
                            else:
                                rowdatas.append("")
                            rowdatas.append(racelist[2])
                            self.content.append(rowdatas)

                    else:
                        rowdatas = []
                        for cell in numbers:
                            rowdatas.append(racelist[cell])
                        self.content.append(rowdatas)

            if self.tablemade != False:
                self.tablay.removeWidget(self.tabwid)
            self.makeTable()
            self.tabwid.setObjectName("BlackWid")

            self.myImage(self.data.replace(" ", "-"), 0)
            self.titel.setText("List of the " + self.data.title() + " for the " + str(self.calender) + " Formula 1 Season")
            self.cols = int(len(self.tabheader))
            self.rows = int(len(self.content))

            self.fillTable(self.rows, self.cols, self.content, self.tabheader)

            order = []
            for i in range(self.rows):
                order.append(str(i + 1))
            self.table.setVerticalHeaderLabels(order)

        self.goBack()

    def SQLsave(self):
        # curs = mydb.cursor()
        # curs.execute("CREATE DATABASE IF NOT EXISTS formula1")
        # mydb.commit()

        name = (self.data + " " + str(self.calender)).replace(" ", "_")
        ask = QMessageBox.question(self, "Saving Table", "Do you want to save table " + name + " ?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if ask == QMessageBox.Yes:

            curs = mydb.cursor()
            curs.execute("USE formula1")
            curs.execute("SHOW TABLES")

            alltables = []
            for x in curs:
                clear = (str(x)[1:-1].replace(",", ""))
                alltables.append(clear.replace("'", ""))
            mydb.commit()

            if name not in alltables:
                self.createSQL(name)
            else:
                QMessageBox.about(self, "SQL error", "Table "+name+" is already in the database!")
        else:
            pass


    def createSQL(self, name):
        stock = []
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

        QMessageBox.about(self, "SQL Table", "Table "+name+" was added to the database!")


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
                self.allcontent.append(titel.replace("'", "")[len(titel) - 6:len(titel)])

        maintag = QLabel("Category " + str(listname).replace("_", " ").title() + " Tables")
        maintag.setObjectName("BlackLab")
        maintag.setAlignment(Qt.AlignCenter)
        self.innerlay.addWidget(maintag)
        self.myImage('menues', 3)

        lbltag = QLabel("Select year:")
        lbltag.setObjectName("BlackLab")
        self.listing = QComboBox()
        self.listing.addItems(self.allcontent)
        twoinone = QHBoxLayout()
        twoinone.addWidget(lbltag)
        twoinone.addWidget(self.listing)
        twolinewid = QWidget()
        twolinewid.setObjectName("RedWid")
        twolinewid.setLayout(twoinone)
        self.innerlay.addWidget(twolinewid)

        btn = QPushButton("Load SQL Table")
        btn.clicked.connect(self.getSQLtab)
        self.innerlay.addWidget(btn)
        self.listvar = listname

        backbtn = QPushButton("Back to Menu")
        backbtn.clicked.connect(self.goBack)
        self.innerlay.addWidget(backbtn)

        clearlbl = QLabel()
        self.innerlay.addWidget(clearlbl)

        self.eraselbl = QLabel()
        self.innerlay.addWidget(self.eraselbl)
        self.myImage('btn-del', 1)

        self.erase = QPushButton("Erase SQL Table")
        self.erase.clicked.connect(self.eraseTab)
        self.innerlay.addWidget(self.erase)

        self.eraselbl.setVisible(False)
        self.erase.setVisible(False)
        self.stretcher(self.innerlay)

    def stretcher(self, layspace):
        stretch = QWidget()
        strlay = QVBoxLayout()
        strlay.addStretch()
        stretch.setLayout(strlay)
        layspace.addWidget(stretch)

    def getSQLtab(self):

        self.sorthide = False
        if len(self.allcontent) == 0:
            QMessageBox.about(self,"Empty Database","No tables are Saved in this Category!")
        else:
            self.ref = self.listvar + "_" + str(self.listing.currentText())
            curs = mydb.cursor()
            curs.execute("SELECT * FROM " + self.ref)

            self.listSet(curs)
            if self.tablemade != False:
                self.tablay.removeWidget(self.tabwid)
            self.makeTable()

            self.colname = []
            curs = mydb.cursor()
            curs.execute("SHOW COLUMNS FROM " + self.ref)
            for x in curs:
                self.colname.append(list(x)[0])
            self.colname.pop(0)
            self.cols = len(self.colname)

            self.myImage(self.listvar.replace("_", "-"), 0)

            mytitle = self.ref.split("_")
            if len(mytitle) > 2:
                self.titel.setText(
                    "List of the " + str(mytitle[0] + " " + mytitle[1]).title() + " for the " + mytitle[2] + " Formula 1 Season")
            else:
                self.titel.setText("List of the " + str(mytitle[0]).title() + " for the " + mytitle[1] + " Formula 1 Season")

            self.savedata.setVisible(False)
            self.savelbl.setVisible(False)
            self.erase.setVisible(True)
            self.eraselbl.setVisible(True)

            self.table.setVerticalHeaderLabels(self.vertic)
            self.fillTable(self.rows, self.cols, self.transfer, self.colname)

            if self.sortbool == True:
                self.clearLay(self.sortlay)
                self.sortbool = False

            if self.sortbool == False:
                self.sortwid.setVisible(True)
                sortlbl = QLabel("Sort Label:")
                sortlbl.setObjectName("RedLab")
                self.sortbox = QComboBox()

                if "race" in self.ref:
                    self.colname.append("id")
                self.sortbox.addItems(self.colname)

                order = QLabel("Order by:")
                order.setObjectName("RedLab")
                self.asc = QRadioButton("ASC")
                self.des = QRadioButton("DESC")
                gr = QButtonGroup()
                gr.addButton(self.asc)
                gr.addButton(self.des)

                sortbtn = QPushButton("  Sort Data  ")
                sortbtn.setObjectName("RedBtn")
                sortbtn.clicked.connect(self.sorting)

                self.sortlay.addWidget(sortlbl)
                self.sortlay.addWidget(self.sortbox)
                self.sortlay.addWidget(order)
                self.sortlay.addWidget(self.asc)
                self.sortlay.addWidget(self.des)
                self.sortlay.addWidget(sortbtn)

                self.sortwid.setLayout(self.sortlay)
                self.sortbool = True


    def goBack(self):
        self.clearLay(self.innerlay)

        sqltitel = QLabel("Choose a Table Category")
        sqltitel.setObjectName("BlackLab")
        sqltitel.setAlignment(Qt.AlignCenter)
        self.innerlay.addWidget(sqltitel)
        self.myImage('menues', 3)

        sections = ['calender', 'race_wins', 'driver_ranks', 'team_ranks']
        btnlay = QVBoxLayout()
        for x in sections:
            btn = QPushButton(str(x))
            btn.setObjectName("RedBtn")
            btn.clicked.connect(self.getList)
            btnlay.addWidget(btn)

        btnwid = QWidget()
        btnwid.setObjectName("BlackWid")
        btnwid.setLayout(btnlay)
        self.innerlay.addWidget(btnwid)

        self.stretcher(self.innerlay)

    def makeTable(self):
        self.tablemade = True
        self.table = QTableWidget()
        self.table.setRowCount(self.rows)
        self.table.setColumnCount(self.cols)

        self.table.horizontalHeader().setStretchLastSection(True)

        self.tabwid = QWidget()
        self.form = QVBoxLayout()
        self.form.addWidget(self.table)
        self.tabwid.setLayout(self.form)

        self.scroll = QScrollArea()
        self.form.addWidget(self.scroll)
        self.scroll.setVisible(False)

        self.tablay.addWidget(self.tabwid)

    def progressload(self, pages):
        self.loadtab.setVisible(True)

        if pages != 0:
            self.loadtab.setValue(6 - pages)
        else:
            self.loadtab.setVisible(False)

    def eraseTab(self):
        year = str(self.listing.currentText())
        deltab = self.listvar + "_" + year
        ask = QMessageBox.question(self, "Delete Table", "Do you want to drop table " + deltab + " ?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if ask == QMessageBox.Yes:
            curs = mydb.cursor()
            curs.execute("USE formula1")
            curs.execute("DROP TABLE " + deltab)
            mydb.commit()
            QMessageBox.about(self, "Delete Table", "The table was erased from the database!")
            self.goBack()
        else:
            pass

    def myImage(self, picname, look):
        intropic = QPixmap("imgpics/f1-" + picname + ".jpg")
        wd, ln = 260, 110

        if look == 1:
            self.eraselbl.setPixmap(intropic.scaled(wd, ln, Qt.KeepAspectRatio))
        elif look == 2:
            self.savelbl.setPixmap(intropic.scaled(wd, ln, Qt.KeepAspectRatio))

        elif look == 3 or look == 4:
            self.sqlpic = QLabel()
            self.sqlpic.setPixmap(intropic.scaled(wd, ln, Qt.KeepAspectRatio))
            self.sqlpic.setAlignment(Qt.AlignCenter)

            if look == 3:
                self.innerlay.addWidget(self.sqlpic)
            else:
                loadlabl = QLabel("Scrape Data from the Website")
                loadlabl.setObjectName("BlackLab")
                loadlabl.setAlignment(Qt.AlignCenter)
                self.layload.addWidget(loadlabl)
                self.layload.addWidget(self.sqlpic)
        else:
            self.introlbl.setPixmap(intropic)
            self.introlbl.setAlignment(Qt.AlignCenter)

    def fillTable(self, tabrow, tabcol, filler, myheader):
        self.table.setRowCount(tabrow)
        self.table.setColumnCount(tabcol)

        color = QColor(190,190,190)
        for rw in range(tabrow):
            for cl in range(tabcol):
                self.table.setItem(rw, cl, QTableWidgetItem(str(filler[rw][cl])))
                if rw%2 == 0:
                    self.table.item(rw, cl).setBackground(color)

        style = "::section {background-color: red; color:white; font-size: 12pt; font-weight:bold;}"

        header = self.table.horizontalHeader()
        header.setFixedHeight(40)
        self.table.setHorizontalHeaderLabels(myheader)
        header.setDefaultAlignment(Qt.AlignHCenter)
        header.setStyleSheet(style)

        sidehead = self.table.verticalHeader()
        sidehead.setFixedWidth(35)
        sidehead.setDefaultAlignment(Qt.AlignCenter)
        sidehead.setStyleSheet(style)

        max = 75
        for j in range(tabcol):
            self.table.resizeColumnToContents(j)
            max += self.table.columnWidth(j)

        if 'Calender' in self.titel.text():
            for i in range(tabcol):
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            header.setSectionResizeMode(tabcol - 1, QHeaderView.ResizeToContents)

        elif 'Team' in self.titel.text():
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setStretchLastSection(False)

            # for i in range(tabrow):
            #     self.table.item(i, 1).setToolTip(str(self.fullnames[filler[i][0]]))

        else:
            header.setSectionResizeMode(QHeaderView.ResizeToContents)

        if max <= 750:
            self.tabwid.setMinimumWidth(max)
            self.setFixedWidth(max + 350)
        else:
            self.scroll.setWidget(self.table)
            self.scroll.setVisible(True)
            self.table.setMinimumWidth(max)
            self.setFixedWidth(1050)

        # if self.sorthide==False:
        self.setFixedHeight(850)
        self.table.setFixedHeight(340)
        # else:
        #     self.setFixedHeight(550)
        #     self.table.setFixedHeight(300)


    def sorting(self):
        if self.asc.isChecked():
            direct = self.asc.text()
        elif self.des.isChecked():
            direct = self.des.text()

        sorter = self.sortbox.currentText()
        curs = mydb.cursor()
        curs.execute("USE formula1")
        if sorter == "date" or sorter == "id" or sorter == "points":
            curs.execute("SELECT * FROM " + self.ref + " ORDER BY id" + " " + direct)
        elif sorter == "laps":
            curs.execute("SELECT * FROM " + self.ref + " ORDER BY ABS(" + sorter + ") " + direct)
        else:
            curs.execute("SELECT * FROM " + self.ref + " ORDER BY " + sorter + " " + direct)

        self.listSet(curs)
        self.table.setVerticalHeaderLabels(self.vertic)
        self.fillTable(self.rows, self.cols, self.transfer, self.colname)

    def clearLay(self, layout):
        for i in reversed(range(layout.count())):
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().setParent(None)

    def listSet(self, curs):
        self.transfer = []
        self.vertic = []
        for x in curs:
            self.transfer.append(x[1:len(x)])
            self.vertic.append(str(x[0]))
        self.rows = len(self.transfer)


    def MultipleData(self):
        if self.data == "calender" or self.data == "race wins":
            links = ['races']
            var = 8

            if self.data == 'calender':
                self.tabheader = ['country', 'date', 'laps', 'duration']
                numbers = [0, 1, 6, 7]
            else:
                self.tabheader = ['country', 'first_name', 'last_name', 'nickname', 'team_name']
                numbers = [0, 2, 3, 4, 5]

        elif self.data == 'driver ranks':
            links = ['drivers']
            var = 7
            self.tabheader = ['first_name', 'last_name', 'nationality', 'team_name', 'points']
            numbers = [1, 2, 4, 5, 6]
        else:
            links = ['drivers', 'team']
            var = 3
            numbers = {}
            self.tabheader = ['team_name', 'drivers', 'points']

        return links, var, self.tabheader, numbers

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(css_Style)
    window = DataF1Table()
    sys.exit(app.exec_())
