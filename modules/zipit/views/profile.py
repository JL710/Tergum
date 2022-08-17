from PyQt5 import QtWidgets as qtw


# group box for related widgets
class ProfileBox(qtw.QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle("Profile")

        # widgets
        self.__combobox = qtw.QComboBox()

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

    def __on_rename(self):
        print("on_rename")

    def __on_delete(self):
        print("on_delete")
