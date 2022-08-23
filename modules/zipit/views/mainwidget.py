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
        self.__target_groupbox = TargetBox()
        self.load_profile_signal.connect(self.__target_groupbox.on_profile_change)
        self.__cargo_groupbox = CargoBox()
        self.__startbutton = StartButton()
        self.__profile_groupbox = ProfileBox(mainwidget=self)  # needs to be the last to be initioated -> else others wont get the newest profile via signal -> extra call for signal (.refresh_combomox()) does not work why ever

        # layout stuff
        self.__layout = qtw.QVBoxLayout()
        self.__layout.addWidget(self.__profile_groupbox)
        self.__layout.addWidget(self.__target_groupbox)
        self.__layout.addWidget(self.__cargo_groupbox)
        self.__layout.addWidget(self.__startbutton)
        self.setLayout(self.__layout)
        
