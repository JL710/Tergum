from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from pathlib import Path

from ..db import DBManager
from .error import error_popup


# group box for the target related widgets
class TargetBox(qtw.QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle("Target")

        self.__current_profile = ""

        # widgets
        self.__label = qtw.QLabel("-----")
        self.__change_button = qtw.QPushButton("Change")
        self.__change_button.clicked.connect(self.__on_change)

        # layout stuff
        self.__layout = qtw.QHBoxLayout()
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__change_button)
        self.setLayout(self.__layout)

    @qtc.pyqtSlot(str)
    def on_profile_change(self, profile: str):
        self.__current_profile = profile
        self.__label.setText(DBManager.get_target(profile))

    def __on_change(self):
        path = Path(qtw.QFileDialog.getExistingDirectory(self, "New Target"))
        if not path.is_absolute():
            pass
        elif path.is_dir():
            DBManager.set_target(self.__current_profile, str(path))  # change target in db
            self.__label.setText(str(path)) # change label
        else:
            error_popup("Error", "Path does not exist or is a file!")
