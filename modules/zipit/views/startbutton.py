from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


class StartButton(qtw.QPushButton):
    def __init__(self):
        super().__init__("Start")
        self.__profile = ""
        self.clicked.connect(self.on_start)

    @qtc.pyqtSlot(str)
    def on_profile_change_slot(self, profile: str):
        self.__profile = profile
        
    def on_start(self):
        print(f"Start: {self.__profile}")


class RunningPopup(qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Running")