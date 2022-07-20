import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore as qtc
import modules.addover.code_behind as cb
from pathlib import Path



class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Stack shit
        self.stack_widget = QtWidgets.QStackedWidget(self)
        self.stack_widget.addWidget(SetupWidget())
        self.stack_widget.addWidget(MonitorWidget())

        self.stack_widget.setCurrentIndex(0)

        # do layout for MainWidget
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.stack_widget)
        self.setLayout(self.layout)



class SetupWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # target widgets
        self.__target_group_bot = self.TargetGroupBox()
        
        self.__payload_list = self.PayloadList()

        self.__start_button = QtWidgets.QPushButton("Start")
        self.__add_payload_button = QtWidgets.QPushButton("Add")
        self.__add_payload_button.clicked.connect(self.__payload_list.add)
        self.__remove_payload_button = QtWidgets.QPushButton("Remove")
        self.__remove_payload_button.clicked.connect(self.__payload_list.remove)

        # layout
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.__target_group_bot, 0, 0, 1, 2)
        self.layout.addWidget(self.__payload_list, 1, 0, 1, 2)
        self.layout.addWidget(self.__remove_payload_button, 2, 0, 1, 1)
        self.layout.addWidget(self.__add_payload_button, 2, 1, 1, 1)
        self.layout.addWidget(self.__start_button, 3, 0, 1, 1)
        self.setLayout(self.layout)

    class PayloadList(QtWidgets.QListWidget):
        def __init__(self):
            super().__init__()
            self.refresh()

        def refresh(self):
            self.clear()
            for load in cb.load_paylods():
                self.addItem(load)

        @qtc.pyqtSlot()
        def add(self):
            path = QtWidgets.QFileDialog.getExistingDirectory()
            cb.add_payload(path)
            self.refresh()

        @qtc.pyqtSlot()
        def remove(self):
            cb.remove_payload(self.currentItem().text())
            self.refresh()

    class TargetGroupBox(QtWidgets.QGroupBox):
        def __init__(self):
            super().__init__()
            self.setTitle("Target")

            self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum))

            self.__target = cb.load_target()

            # widgets
            self.__status_label = QtWidgets.QLabel(str(self.__target))
            self.__change_button = QtWidgets.QPushButton("Change")
            self.__change_button.clicked.connect(self.on_change_target)

            # layout
            self.__layout = QtWidgets.QHBoxLayout()
            self.__layout.addWidget(self.__status_label)
            self.__layout.addWidget(self.__change_button)
            self.setLayout(self.__layout)

        @qtc.pyqtSlot()
        def on_change_target(self):
            path = Path(QtWidgets.QFileDialog.getExistingDirectory(self, "New Target"))
            if path.is_dir():
                self.__target = path
                self.__status_label.setText(str(self.__target))
                cb.set_target(str(self.__target))
            else:
                error = QtWidgets.QMessageBox()
                error.setWindowTitle("Error")
                error.setText("Path does not exist!")
                error.setIcon(QtWidgets.QMessageBox.Critical)
                error.exec_()




class MonitorWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
