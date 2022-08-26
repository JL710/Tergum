from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from pathlib import Path
import typing

from .error import error_popup
from ..db import DBManager



# group box for cargo related widgets
class CargoBox(qtw.QGroupBox):
    def __init__(self, title: str, include: bool):
        super().__init__()
        self.setTitle(title)

        self.__profile: str
        self.__include = include

        # widgets
        self.__listwidget = qtw.QListWidget()
        self.__add_file_button = qtw.QPushButton("Add File")
        self.__add_file_button.clicked.connect(self.__on_add_file)
        self.__add_dir_button = qtw.QPushButton("Add Directory")
        self.__add_dir_button.clicked.connect(self.__on_add_dir)
        self.__delete_dir_button = qtw.QPushButton("Delete")
        self.__delete_dir_button.clicked.connect(self.__on_delete)

        # layout
        self.__layout = qtw.QGridLayout()
        self.__layout.addWidget(self.__listwidget, 0, 0, 1, 3)
        self.__layout.addWidget(self.__add_file_button, 1, 0, 1, 1)
        self.__layout.addWidget(self.__add_dir_button, 1, 1, 1, 1)
        self.__layout.addWidget(self.__delete_dir_button, 1, 2, 1, 1)
        self.setLayout(self.__layout)
    
    def refresh(self, profile: str|None=None):
        if profile:
            self.__profile = profile
        self.__listwidget.clear()
        self.__listwidget.addItems([str(c) for c in DBManager.get_cargo(self.__profile, self.__include)]) 

    def __on_add_file(self):
        path = Path(qtw.QFileDialog.getOpenFileName(self, "Add File")[0])
        if not path.is_absolute():  # needs to be checked -> detects if user has canceled the selection
            pass
        elif path.is_file(): 
            DBManager.add_cargo(self.__profile, str(path), self.__include)
            self.refresh()
        else:
            error_popup("Error", "Path does not exist or is a directory!")

    def __on_add_dir(self):
        path = Path(qtw.QFileDialog.getExistingDirectory(self, "Add Directory"))
        if not path.is_absolute():  # needs to be checked -> detects if user has canceled the selection
            pass
        elif path.is_dir(): 
            DBManager.add_cargo(self.__profile, str(path), self.__include)
            self.refresh()
        else:
            error_popup("Error", "Path does not exist or is a file!")

    def __on_delete(self):
        current_item = self.__listwidget.currentItem()
        if not current_item == None:  # in case none is selected
            DBManager.remove_cargo(self.__profile, current_item.text(), self.__include)
            self.refresh()

