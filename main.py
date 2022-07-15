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
        self.layout = QtWidgets.QVBoxLayout()

        # Tabwidget
        self.tabs = QtWidgets.QTabWidget()
        for widget in load_from_module.load_widgets():
            self.tabs.addTab(widget, "Tab1")

        # mainlayout shit
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

