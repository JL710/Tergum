from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from .. import code_behind


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
        popup = RunningPopup(self.__profile)
        popup.exec()


class RunningPopup(qtw.QDialog):
    def __init__(self, profile: str):
        super().__init__()
        self.setWindowTitle("Running")

        # widgets
        self.__scroll_label = self.ScrollLabel()
        self.__progressbar = qtw.QProgressBar()
        self.__finish_button = qtw.QPushButton("Finish")
        self.__finish_button.setDisabled(True)
        self.__finish_button.clicked.connect(self.__on_finish_button)

        # layout
        self.__layout = qtw.QGridLayout()
        self.__layout.addWidget(self.__scroll_label, 0, 0, 1, 2)
        self.__layout.addWidget(self.__progressbar, 1, 0, 1, 1)
        self.__layout.addWidget(self.__finish_button, 1, 1, 1, 1)
        self.setLayout(self.__layout)

        # thread stuff
        self.__thread = self.Thread(profile)
        self.__thread.progress.connect(self.__on_progress)
        self.__thread.start()

    def __on_progress(self, status_dict: dict):
        self.__scroll_label.add_text(status_dict["message"])
        self.__progressbar.setValue(status_dict["percentage"])
        if status_dict["finished"]:
            self.__finish_button.setDisabled(False)

    def __on_finish_button(self):
        self.close()

    class ScrollLabel(qtw.QScrollArea):  # FIXME: stick scroll to bottom nicely
            def __init__(self, text: int=""):
                super().__init__()
                self.__widget = qtw.QWidget()
                self.__label = qtw.QLabel(text)
                self.__layout = qtw.QVBoxLayout()
                self.__layout.addWidget(self.__label)
                self.__layout.addStretch()  # puts the label at the top

                self.__widget.setLayout(self.__layout)
                self.setWidget(self.__widget)

                self.setWidgetResizable(True) # allows the Wiget to resize when conent(Label) changes

            def add_text(self, text: str):
                self.__label.setText(self.__label.text() + "\n" + text)

            def set_text(self, text: str):
                self.__label.setText(text)

    class Thread(qtc.QThread):
        progress = qtc.pyqtSignal(dict)

        def __init__(self, profile: str):
            super().__init__()
            self.__profile = profile

        def run(self):
            for do in code_behind.zipit(self.__profile):
                self.progress.emit(do)