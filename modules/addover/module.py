import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import modules.addover.code_behind as cb
from pathlib import Path


class Menu(QtWidgets.QMenu):
    def __init__(self, main_widget):
        super().__init__("Add Over")

        self.__edit_command_action = QtWidgets.QAction("Edit Command")
        self.__edit_command_action.triggered.connect(self.__on_edit_command)

        self.__reset_command_action = QtWidgets.QAction("Reset Command")
        self.__reset_command_action.triggered.connect(self.__on_reset_command)

        self.addAction(self.__edit_command_action)
        self.addAction(self.__reset_command_action)

    def __on_edit_command(self):
        text, submit = QtWidgets.QInputDialog.getText(self, "Edit Command", "Edit Command here:", text=cb.get_command())
        if submit:
            cb.set_command(text)

    def __on_reset_command(self):
        cb.reset_command()



class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Stack shit
        self.__startup_widget = SetupWidget()
        self.__action_widget = ActionWidget()
        self.__stack_widget = QtWidgets.QStackedWidget(self)
        self.__stack_widget.addWidget(self.__startup_widget)
        self.__stack_widget.addWidget(self.__action_widget)

        self.__stack_widget.setCurrentIndex(0)

        # do layout for MainWidget
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.__stack_widget)
        self.setLayout(self.layout)

        # signal connect
        self.__startup_widget.submit.connect(self.__switch)
        self.__action_widget.exit.connect(self.__switch)

    def __switch(self):
        # swich stack
        if self.__stack_widget.currentIndex() == 0:
            self.__stack_widget.setCurrentIndex(1)
            self.__action_widget.start.emit()        
        else:
            self.__stack_widget.setCurrentIndex(0)



class SetupWidget(QtWidgets.QWidget):
    # signal
    submit = qtc.pyqtSignal()
    
    def __init__(self):
        super().__init__()

        # target widgets
        self.__target_group_bot = self.TargetGroupBox()
        
        self.__payload_list = self.PayloadList()

        self.__start_button = QtWidgets.QPushButton("Start")
        self.__start_button.clicked.connect(self.on_start)
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

    @qtc.pyqtSlot()
    def on_start(self):
        if not cb.load_target().is_dir():
            error = QtWidgets.QMessageBox()
            error.setWindowTitle("Error")
            error.setText("Target does not exist!")
            error.setIcon(QtWidgets.QMessageBox.Critical)
            error.exec_()
            return
        qm = QtWidgets.QMessageBox
        shure = qm.question(self, "Make Shure", f'Is the Target "{str(cb.load_target())}" correct?', qm.Yes | qm.No)
        if shure == qm.Yes:  # the pass is validated by the user
            self.submit.emit()


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
            if path != "":  # checks if user canceled selection without any select
                cb.add_payload(path)
            self.refresh()

        @qtc.pyqtSlot()
        def remove(self):
            item = self.currentItem()
            if not item == None:
                cb.remove_payload(item.text())
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
            if not path.is_absolute():
                pass # needs to be checked -> if user cancels the selection process
            elif path.is_dir():
                self.__target = path
                self.__status_label.setText(str(self.__target))
                cb.set_target(str(self.__target))
            else:
                error = QtWidgets.QMessageBox()
                error.setWindowTitle("Error")
                error.setText("Path does not exist!")
                error.setIcon(QtWidgets.QMessageBox.Critical)
                error.exec_()




class ActionWidget(QtWidgets.QWidget):
    start = qtc.pyqtSignal()
    exit = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()

        # connect signal and slots
        self.start.connect(self.on_start)

        # Widgets 
        self.__scroll_label = self.ScrollLabel()

        self.__progress_bar = QtWidgets.QProgressBar()
        self.__progress_bar.setValue(25)

        self.__finish_button = QtWidgets.QPushButton("Finish")
        self.__finish_button.clicked.connect(self.__on_finish)
        self.__finish_button.setDisabled(True)

        self.__layout = QtWidgets.QGridLayout()
        self.__layout.addWidget(self.__scroll_label, 0, 0, 1, 2)
        self.__layout.addWidget(self.__progress_bar, 1, 0, 1, 1)
        self.__layout.addWidget(self.__finish_button, 1, 1, 1, 1)
        self.setLayout(self.__layout)

        # thread
        self.__thread = self.Thread()
        self.__thread.progress.connect(self.__update_progress)

    def __on_finish(self):
        self.exit.emit()

    def on_start(self):
        self.__scroll_label.set_text("")
        self.__finish_button.setDisabled(True)
        self.__thread.start()

    @qtc.pyqtSlot(dict)
    def __update_progress(self, do: dict):
        self.__progress_bar.setValue(do["percentage"])
        self.__scroll_label.add_text(do["event-message"])
        if do["finished"]:
            self.__finish_button.setDisabled(False)

            # message
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Finished")
            messagebox.setText("The process finished.")
            messagebox.setIcon(QtWidgets.QMessageBox.Information)
            messagebox.exec_()

    class Thread(qtc.QThread):
        progress = qtc.pyqtSignal(dict)

        def run(self):
            for do in cb.start():
                self.progress.emit(do)

    class ScrollLabel(QtWidgets.QScrollArea):
        def __init__(self, text: int=""):
            super().__init__()
            self.__widget = QtWidgets.QWidget()
            self.__label = QtWidgets.QLabel(text)
            self.__layout = QtWidgets.QVBoxLayout()
            self.__layout.addWidget(self.__label)
            self.__layout.addStretch()  # puts the label at the top

            self.__widget.setLayout(self.__layout)
            self.setWidget(self.__widget)

            self.setWidgetResizable(True) # allows the Wiget to resize when conent(Label) changes

        def add_text(self, text: str):
            self.__label.setText(text + "\n" + self.__label.text())

        def set_text(self, text: str):
            self.__label.setText(text)

