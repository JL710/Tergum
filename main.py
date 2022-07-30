from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import sys

import load_from_module

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 500, 400) # xpos, ypos, width, height
        self.setWindowTitle("Tergum")
        self.initUI()
 
    def initUI(self):
        self.__layout = QtWidgets.QVBoxLayout()

        # menu
        self.__menubar = QtWidgets.QMenuBar(self)        

        # Tabwidget
        self.__tabs = QtWidgets.QTabWidget()

        # load modules
        self.__modules = load_from_module.load_modules()  # needs to be stored as attribut, because of menus
        for module in self.__modules:
            if module["menu"] != None:
                self.__menubar.addAction(module["menu"].menuAction())
            self.__tabs.addTab(module["widget"], module["title"])

        # mainlayout shit
        self.__layout.setMenuBar(self.__menubar)
        self.__layout.addWidget(self.__tabs)
        self.setLayout(self.__layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

