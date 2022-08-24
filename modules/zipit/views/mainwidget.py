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
        self.__included_cargo_groupbox = CargoBox("Included Cargo", include=True)
        self.load_profile_signal.connect(self.__included_cargo_groupbox.refresh)
        self.__excluded_cargo_groupbox = CargoBox("Exclude from Cargo", include=False)
        self.load_profile_signal.connect(self.__excluded_cargo_groupbox.refresh)
        self.__startbutton = StartButton()
        self.__profile_groupbox = ProfileBox(mainwidget=self)  # needs to be the last to be initioated -> else others wont get the newest profile via signal -> extra call for signal (.refresh_combomox()) does not work why ever

        # layout stuff
        self.__layout = qtw.QVBoxLayout()
        self.__layout.addWidget(self.__profile_groupbox)
        self.__layout.addWidget(self.__target_groupbox)
        self.__layout.addWidget(self.__included_cargo_groupbox)
        self.__layout.addWidget(self.__excluded_cargo_groupbox)
        self.__layout.addWidget(self.__startbutton)
        self.setLayout(self.__layout)
        
