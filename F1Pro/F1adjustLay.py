from PyQt5.QtWidgets import QWidget, QVBoxLayout

def adjustLay(layspace,bol):
    if bol == True:
        for i in reversed(range(layspace.count())):
            if layspace.itemAt(i).widget():
                layspace.itemAt(i).widget().setParent(None)
    else:
        stretch = QWidget()
        strlay = QVBoxLayout()
        strlay.addStretch()
        stretch.setLayout(strlay)
        layspace.addWidget(stretch)