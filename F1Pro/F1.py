import datetime
import mysql.connector as con

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QWidget, QTabWidget, QApplication, QProgressBar, QScrollArea, \
    QTableWidget, QTableWidgetItem, QHeaderView, QGridLayout, QVBoxLayout, QHBoxLayout, \
    QPushButton, QRadioButton, QButtonGroup, QLabel, QComboBox, QSpinBox, QMessageBox

from F1Pro.F1images import tabImage
from F1css import css_Style
from F1Loader import MultipleData
from F1dataScrape import WebScrape
from F1TabList import listSet
from F1Height import tabHeight
from F1Teams import TeamContent
from F1LoadBar import progressload
from F1adjustLay import adjustLay

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


class DataF1Table(QWidget):
    def __init__(self):
        super().__init__()
        self.VisualTab()

    def VisualTab(self):
        self.setWindowTitle("Formula1 Database")
        self.setWindowIcon(QIcon("images/f1-logo.png"))
        self.setGeometry(100, 100, 350, 350)
        self.setObjectName("RedWid")
        self.sideSQLtab()
        self.setMainTab()
        self.sideWEBtab()
        self.show()

    def sideSQLtab(self):
        self.sqltabs = QWidget()
        self.innerlay = QVBoxLayout()
        self.sqltabs.setLayout(self.innerlay)

        self.eraselbl = QLabel()
        self.savelbl = QLabel()
        self.layload = QVBoxLayout()
        self.introlbl = QLabel()

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
        tabImage('startup', 2, self.introlbl)

        self.loadtab = QProgressBar()
        self.loadtab.setMinimum(0)
        self.loadtab.setMaximum(10)
        self.loadtab.setVisible(False)

        addtoMainwid = [self.titel,self.introlbl,self.tablay,self.sortwid,self.loadtab]
        for item in addtoMainwid:
            if item!=self.tablay:
                self.mainwid.addWidget(item)
            else: self.mainwid.addLayout(item)


    def sideWEBtab(self):
        self.mygrid = QGridLayout()
        self.tabright = QWidget()
        self.tabright.setObjectName("White")
        self.tabright.setLayout(self.mainwid)
        self.mygrid.addWidget(self.tabright, 0, 1)

        loadwid = QWidget()
        loadwid.setLayout(self.layload)

        tabImage('menu', 4, self.layload)
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
        sections = ['calendar', 'race wins', 'driver ranks', 'team ranks']
        self.combo.addItems(sections)
        secrow.addWidget(self.datalbl)
        secrow.addWidget(self.combo)

        btn = QPushButton("Load Data in Table")
        btn.setObjectName("Mar")
        btn.clicked.connect(self.race_results)

        tabImage('saves', 1, self.savelbl)
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

        clearlab = QLabel()
        addtoLayload = [doubwid,btn,clearlab,self.savelbl,self.savedata]
        for item in addtoLayload:
            self.layload.addWidget(item)
        self.layload.addStretch()

        self.maintab = QTabWidget()
        self.maintab.setMaximumWidth(270)
        self.maintab.addTab(loadwid, "Load Data")
        self.maintab.addTab(self.sqltabs, "View Data")
        self.mygrid.addWidget(self.maintab, 0, 0)

        self.setLayout(self.mygrid)

    def race_results(self):

        if self.sortbool == True:
            adjustLay(self.sortlay,True)
            self.sorthide=True
            self.sortwid.setVisible(False)
            self.erase.setVisible(False)
            self.eraselbl.setVisible(False)
            self.sortbool = False

        calendar = int(self.spinyear.text())
        data = str(self.combo.currentText())

        if data == "team ranks" and calendar < 1958:
            QMessageBox.about(self, "Data Error", "No team Competitions before 1958!")
        else:

            self.savedata.setVisible(True)
            self.savelbl.setVisible(True)
            links, var, self.tabheader, numbers = MultipleData(data)

            for sector in links:

                table = WebScrape(calendar, sector)
                progressload(self.loadtab)
                self.content = []

                for tabrow in table:
                    racelist = tabrow.text.strip().replace("     ", "").split("\n")
                    racelist = list(filter(lambda x: x != '', racelist))

                    while len(racelist) < var:
                        racelist.append("")
                    rowdatas = []

                    if data == "team ranks":
                        teaminfo = TeamContent(sector,numbers,racelist,rowdatas)
                        self.content.append(teaminfo)

                    else:
                        for cell in numbers:
                            rowdatas.append(racelist[cell])
                        self.content.append(rowdatas)

            if self.tablemade != False:
                self.tablay.removeWidget(self.tabwid)
            self.makeTable()
            self.tabwid.setObjectName("BlackWid")

            tabImage(data.replace(" ", "-"), 0, self.introlbl)
            self.titel.setText("List of the " + data.title() + " for the " + str(calendar) + " Formula 1 Season")
            self.cols = int(len(self.tabheader))
            self.rows = int(len(self.content))

            vertic = []
            for i in range(self.rows):
                vertic.append(str(i + 1))

            self.fillTable(self.rows, self.cols, self.content, self.tabheader, vertic)

        self.goBack()

    def SQLsave(self):
        self.makeDB()
        calendar = int(self.spinyear.text())
        data = str(self.combo.currentText())

        name = (data + " " + str(calendar)).replace(" ", "_")
        ask = QMessageBox.question(self, "Saving Table", "Do you want to save table " + name + " ?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if ask == QMessageBox.Yes:

            curs = mydb.cursor()
            curs.execute("USE formula1db")
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
        curs.execute("USE formula1db")

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
        self.makeDB()
        curs = mydb.cursor()
        curs.execute("USE formula1db")
        curs.execute("SHOW TABLES")
        listname = self.sender().text()

        adjustLay(self.innerlay,True)
        self.allcontent = []
        for x in curs:
            titel = str(x)[1:-1].replace(",", "")
            if listname in titel:
                self.allcontent.append(titel.replace("'", "")[len(titel) - 6:len(titel)])

        maintag = QLabel("Category " + str(listname).replace("_", " ").title() + " Tables")
        maintag.setObjectName("BlackLab")
        maintag.setAlignment(Qt.AlignCenter)
        self.innerlay.addWidget(maintag)
        tabImage('menues', 3, self.innerlay)

        lbltag = QLabel("Select year:")
        lbltag.setObjectName("BlackLab")
        self.yearlist = QComboBox()
        self.yearlist.addItems(self.allcontent)
        twoinone = QHBoxLayout()
        twoinone.addWidget(lbltag)
        twoinone.addWidget(self.yearlist)
        twolinewid = QWidget()
        twolinewid.setObjectName("RedWid")
        twolinewid.setLayout(twoinone)

        btn = QPushButton("Load SQL Table")
        btn.clicked.connect(self.getSQLtab)
        self.listvar = listname

        backbtn = QPushButton("Back to Menu")
        backbtn.clicked.connect(self.goBack)

        clearlbl = QLabel()
        tabImage('btn-del', 1, self.eraselbl)

        self.erase = QPushButton("Erase SQL Table")
        self.erase.clicked.connect(self.eraseTab)

        addtoInnerLay = [twolinewid,btn,backbtn,clearlbl,self.eraselbl,self.erase]
        for item in addtoInnerLay:
            self.innerlay.addWidget(item)

        self.eraselbl.setVisible(False)
        self.erase.setVisible(False)
        adjustLay(self.innerlay,False)


    def getSQLtab(self):

        self.sorthide = False
        if len(self.allcontent) == 0:
            QMessageBox.about(self,"Empty Database","No tables are Saved in this Category!")
        else:
            self.ref = self.listvar + "_" + str(self.yearlist.currentText())
            curs = mydb.cursor()
            curs.execute("SELECT * FROM " + self.ref)

            cellsdata,vertic,self.rows = listSet(curs)
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

            tabImage(self.listvar.replace("_", "-"), 2, self.introlbl)
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

            self.fillTable(self.rows, self.cols, cellsdata, self.colname, vertic)

            if self.sortbool == True:
                adjustLay(self.sortlay,True)
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
                self.asc.setChecked(True)
                self.des = QRadioButton("DESC")
                gr = QButtonGroup()
                gr.addButton(self.asc)
                gr.addButton(self.des)

                sortbtn = QPushButton("  Sort Data  ")
                sortbtn.setObjectName("RedBtn")
                sortbtn.clicked.connect(self.sorting)

                addtoSortlay = [sortlbl,self.sortbox,order,self.asc,self.des,sortbtn]
                for item in addtoSortlay:
                    self.sortlay.addWidget(item)

                self.sortwid.setLayout(self.sortlay)
                self.sortbool = True


    def goBack(self):
        adjustLay(self.innerlay,True)
        sqltitel = QLabel("Choose a Table Category")
        sqltitel.setObjectName("BlackLab")
        sqltitel.setAlignment(Qt.AlignCenter)
        self.innerlay.addWidget(sqltitel)
        tabImage('menues', 3, self.innerlay)

        sections = ['calendar', 'race_wins', 'driver_ranks', 'team_ranks']
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

        adjustLay(self.innerlay,False)

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


    def eraseTab(self):
        year = str(self.yearlist.currentText())
        deltab = self.listvar + "_" + year
        ask = QMessageBox.question(self, "Delete Table", "Do you want to drop table " + deltab + " ?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if ask == QMessageBox.Yes:
            curs = mydb.cursor()
            curs.execute("USE formula1db")
            curs.execute("DROP TABLE " + deltab)
            mydb.commit()
            QMessageBox.about(self, "Delete Table", "The table was erased from the database!")
            self.goBack()
        else:
            pass


    def fillTable(self, tabrow, tabcol, filler, myheader, vertic):
        self.table.setRowCount(tabrow)
        self.table.setColumnCount(tabcol)
        self.table.setVerticalHeaderLabels(vertic)

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

        if 'Calendar' in self.titel.text():
            for i in range(tabcol):
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            header.setSectionResizeMode(tabcol - 1, QHeaderView.ResizeToContents)

        elif 'Team' in self.titel.text():
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setStretchLastSection(False)

        else:
            header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.setGeometry(100,100,0,0)

        if max <= 750:
            self.tabwid.setMinimumWidth(max)
            self.setFixedWidth(max + 350)
        else:
            self.scroll.setWidget(self.table)
            self.scroll.setVisible(True)
            self.table.setMinimumWidth(max)
            self.setFixedWidth(1050)

        tabHeight(self,self.sorthide,tabrow)

    def sorting(self):
        if self.asc.isChecked():
            direct = self.asc.text()
        elif self.des.isChecked():
            direct = self.des.text()

        sorter = self.sortbox.currentText()
        curs = mydb.cursor()
        curs.execute("USE formula1db")
        if sorter == "date" or sorter == "id" or sorter == "points":
            curs.execute("SELECT * FROM " + self.ref + " ORDER BY id" + " " + direct)
        elif sorter == "laps":
            curs.execute("SELECT * FROM " + self.ref + " ORDER BY ABS(" + sorter + ") " + direct)
        else:
            curs.execute("SELECT * FROM " + self.ref + " ORDER BY " + sorter + " " + direct)

        cellsdata,vertic,rows = listSet(curs)
        self.fillTable(rows, self.cols, cellsdata, self.colname, vertic)


    def makeDB(self):
        curs = mydb.cursor()
        curs.execute("CREATE DATABASE IF NOT EXISTS formula1db")
        mydb.commit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(css_Style)
    window = DataF1Table()
    sys.exit(app.exec_())
