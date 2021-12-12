import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from cjson import Ui_MainWindow
from logic import Bussiness


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myWnd = QMainWindow()
    myUI = Ui_MainWindow()
    myBussiness = Bussiness()

    myUI.setupUi(myWnd,myBussiness)
    myBussiness.set_ui(myUI)
    myWnd.show()
    sys.exit(myapp.exec_())