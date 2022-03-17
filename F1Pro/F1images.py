from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

def tabImage(picname, look, addimg):
    intropic = QPixmap("images/f1-" + picname + ".jpg")
    wd, ln = 260, 110

    if look == 1:
        addimg.setPixmap(intropic.scaled(wd, ln, Qt.KeepAspectRatio))
    elif look == 2:
        addimg.setPixmap(intropic.scaled(wd, ln, Qt.KeepAspectRatio))

    elif look == 3 or look == 4:
        sqlpic = QLabel()
        sqlpic.setPixmap(intropic.scaled(wd, ln, Qt.KeepAspectRatio))
        sqlpic.setAlignment(Qt.AlignCenter)

        if look == 3:
            addimg.addWidget(sqlpic)
        else:
            loadlabl = QLabel("Scrape Data from the Website")
            loadlabl.setObjectName("BlackLab")
            loadlabl.setAlignment(Qt.AlignCenter)
            addimg.addWidget(loadlabl)
            addimg.addWidget(sqlpic)
    else:
        addimg.setPixmap(intropic)
        addimg.setAlignment(Qt.AlignCenter)