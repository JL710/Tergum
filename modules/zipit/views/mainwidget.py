from PyQt5 import QtWidgets as qtw

# import widgets
from .profile import ProfileBox
from .target import TargetBox
from .cargo import CargoBox
from .startbutton import StartButton


# mainwidget
class MainWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # widgets
        self.__profile_groupbox = ProfileBox()
        self.__target_groupbox = TargetBox()
        self.__cargo_groupbox = CargoBox()
        self.__startbutton = StartButton()

        # layout stuff
        self.__layout = qtw.QVBoxLayout()
        self.__layout.addWidget(self.__profile_groupbox)
        self.__layout.addWidget(self.__target_groupbox)
        self.__layout.addWidget(self.__cargo_groupbox)
        self.__layout.addWidget(self.__startbutton)
        self.setLayout(self.__layout)
