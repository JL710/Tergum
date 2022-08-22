from sqlite3 import DatabaseError
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from ..db import DBManager
from .error import error_popup



# group box for related widgets
class ProfileBox(qtw.QGroupBox):
    def __init__(self, mainwidget):
        super().__init__()

        # set title
        self.setTitle("Profile")

        # some attrs
        self.__mainwidget = mainwidget

        # widgets
        self.__combobox = qtw.QComboBox()
        self.refresh_combobox()

        minsize_policy = qtw.QSizePolicy(qtw.QSizePolicy.Maximum, qtw.QSizePolicy.Fixed)
        self.__new_button = qtw.QPushButton("New")
        self.__new_button.setSizePolicy(minsize_policy)
        self.__new_button.clicked.connect(self.__on_new)
        self.__rename_button = qtw.QPushButton("Rename")
        self.__rename_button.setSizePolicy(minsize_policy)
        self.__rename_button.clicked.connect(self.__on_rename)
        self.__delete_button = qtw.QPushButton("Delete")
        self.__delete_button.setSizePolicy(minsize_policy)
        self.__delete_button.clicked.connect(self.__on_delete)

        # layout stuff
        self.__layout = qtw.QHBoxLayout()
        self.__layout.addWidget(self.__combobox)
        self.__layout.addWidget(self.__new_button)
        self.__layout.addWidget(self.__rename_button)
        self.__layout.addWidget(self.__delete_button)
        self.setLayout(self.__layout)

    def __on_new(self):
        print("on_new")
        popup = NewProfileName()
        popup.submit_signal.connect(self.__on_new_submit)
        popup.submit_signal.connect(self.refresh_combobox)
        popup.exec()

    def __on_new_submit(self, profile):
        DBManager.new_profile(name=profile)
        self.__mainwidget.load_profile_signal.emit(profile)

    def __on_rename(self):
        print("on_rename") # TODO: everything -> maby use NewProfileName to get the new name -> should work perfectly
        if DBManager.get_profiles() == []: # check if any profile exists
            error_popup("Error", "No profile found to rename.")
            return
        if not self.__combobox.currentText() in DBManager.get_profiles():  # check if current profile exists
            error_popup("Error", "Current profile not found in the Database.")
            return
        new_name_popup = NewProfileName()
        new_name_popup.submit_signal.connect(self.__on_rename_submit)
        new_name_popup.exec()
    
    def __on_rename_submit(self, new_name):
        DBManager.rename_profile(self.__combobox.currentText(), new_name)
        self.refresh_combobox(new_name)

    def __on_delete(self):
        profiles = DBManager.get_profiles()
        if len(profiles) <= 1:
            # open error popup
            error_popup("Error", f'Only one profile is left.')
            return
        if not self.__combobox.currentText() in DBManager.get_profiles():  # check if current profile exists
            error_popup("Error", "Current profile not found in the Database.")
            return
        DBManager.delete_profile(self.__combobox.currentText())
        self.__mainwidget.load_profile_signal.emit(profiles[0])
        self.refresh_combobox(profiles[0])

    @qtc.pyqtSlot(str)
    def refresh_combobox(self, profile: str|None=None):
        """Reloads the combobox and sets the current profile if passed."""
        if profile == None:  # check if profile exists
            if DBManager.profile_exists(self.__combobox.currentText()):
                profile = self.__combobox.currentText()
            else:
                profile = DBManager.get_profiles()[0]

        if not DBManager.profile_exists(profile):  # FIXME: what if no profile at all exists
            raise DatabaseError(f'Profile "{profile}" does not exist. Checks failed.')

        self.__combobox.clear()
        self.__combobox.addItems(DBManager.get_profiles())
        self.__combobox.setCurrentText(profile)
        self.__mainwidget.load_profile_signal.emit(profile)  # emit to other widgets the new current profile


# Popup for getting a new valid profile name
class NewProfileName(qtw.QDialog):
    submit_signal = qtc.pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        # signal and slot stuff

        # set window title
        self.setWindowTitle("New Profile Name")

        # widgets
        self.__textinput = qtw.QLineEdit()
        self.__submit_button = qtw.QPushButton("Submit")
        self.__submit_button.clicked.connect(self.__on_submit)
        self.__cancel_button = qtw.QPushButton("Cancel")
        self.__cancel_button.clicked.connect(self.close)

        # layout
        self.__layout = qtw.QGridLayout()
        self.__layout.addWidget(self.__textinput, 0, 0, 1, 1)
        self.__layout.addWidget(self.__submit_button, 1, 0, 1, 1)
        self.__layout.addWidget(self.__cancel_button, 1, 1, 1, 1)
        self.setLayout(self.__layout)

    def __on_submit(self):
        name = self.__textinput.text()
        if not DBManager.profile_exists(name): # check if profile already exists
            self.submit_signal.emit(name)
            self.close()
            return
        
        # open error popup
        error_popup("Error", f'Profile "{name}" already exists.')