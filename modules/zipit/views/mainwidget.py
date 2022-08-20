from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

# import widgets
from .profile import ProfileBox
from .target import TargetBox
from .cargo import CargoBox
from .startbutton import StartButton

from ..db import DBManager


# mainwidget
class MainWidget(qtw.QWidget):

    load_profile_signal = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # signal and slot stuff

        # widgets
        self.__profile_groupbox = ProfileBox(mainwidget=self)
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

    @qtc.pyqtSlot(str)
    def new_profile(self, profile: str):
        DBManager.new_profile(name=profile)
        self.load_profile_signal.emit(profile)
