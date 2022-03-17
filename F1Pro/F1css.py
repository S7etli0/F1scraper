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