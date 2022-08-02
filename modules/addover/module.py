from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import modules.addover.code_behind as cb
from pathlib import Path


class Menu(qtw.QMenu):
    def __init__(self, main_widget):
        super().__init__("Add Over")

        self.__edit_command_action = qtw.QAction("Edit Command")
        self.__edit_command_action.triggered.connect(self.__on_edit_command)

        self.__reset_command_action = qtw.QAction("Reset Command")
        self.__reset_command_action.triggered.connect(self.__on_reset_command)

        self.addAction(self.__edit_command_action)
        self.addAction(self.__reset_command_action)

    def __on_edit_command(self):
        text, submit = qtw.QInputDialog.getText(self, "Edit Command", "Edit Command here:", text=cb.get_command())
        if submit:
            cb.set_command(text)

    def __on_reset_command(self):
        cb.reset_command()



class MainWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # Stack shit
        self.__startup_widget = SetupWidget()
        self.__action_widget = ActionWidget()
        self.__stack_widget = qtw.QStackedWidget(self)
        self.__stack_widget.addWidget(self.__startup_widget)
        self.__stack_widget.addWidget(self.__action_widget)

        self.__stack_widget.setCurrentIndex(0)

        # do layout for MainWidget
        self.layout = qtw.QVBoxLayout()
        self.layout.addWidget(self.__stack_widget)
        self.setLayout(self.layout)

        # signal connect
        self.__startup_widget.submit.connect(self.__switch)
        self.__action_widget.exit.connect(self.__switch)

    def __switch(self, profile: str=None):
        # swich stack
        if self.__stack_widget.currentIndex() == 0:
            self.__stack_widget.setCurrentIndex(1)
            self.__action_widget.start.emit(profile)        
        else:
            self.__stack_widget.setCurrentIndex(0)



class SetupWidget(qtw.QWidget):
    # signal
    submit = qtc.pyqtSignal(str)
    s_profile_reload = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()
        # slot / signal
        self.s_profile_reload.connect(self.profile_change)

        # some var
        self.__current_profile = cb.get_profile_names()[0]

        # widgets
        self.__profile_group_box = self.ProfileGroupBox(s_profile_reload=self.s_profile_reload, setup_widget = self)
        self.__profile_group_box.switch_profile.connect(self.on_profile_switch)

        self.__target_group_box = self.TargetGroupBox(parent=self)
        
        self.__payload_list = self.PayloadList(parent=self)

        self.__start_button = qtw.QPushButton("Start")
        self.__start_button.clicked.connect(self.on_start)
        self.__add_dir_payload_button = qtw.QPushButton("Add Directory")
        self.__add_dir_payload_button.clicked.connect(self.__payload_list.add_dir)
        self.__add_file_payload_button = qtw.QPushButton("Add File")
        self.__add_file_payload_button.clicked.connect(self.__payload_list.add_file)
        self.__remove_payload_button = qtw.QPushButton("Remove")
        self.__remove_payload_button.clicked.connect(self.__payload_list.remove)

        # layout
        self.layout = qtw.QGridLayout()
        self.layout.addWidget(self.__profile_group_box, 0, 0, 1, 2)
        self.layout.addWidget(self.__target_group_box, 1, 0, 1, 2)
        self.layout.addWidget(self.__payload_list, 2, 0, 1, 2)
        self.layout.addWidget(self.__remove_payload_button, 3, 0, 1, 1)
        self.layout.addWidget(self.__add_dir_payload_button, 3, 1, 1, 1)
        self.layout.addWidget(self.__add_file_payload_button, 4 ,1 , 1, 1)
        self.layout.addWidget(self.__start_button, 4, 0, 1, 1)
        self.setLayout(self.layout)

    @qtc.pyqtSlot()
    def on_start(self):
        if not cb.get_target(SetupWidget.current_profile).is_dir():
            error = qtw.QMessageBox()
            error.setWindowTitle("Error")
            error.setText("Target does not exist!")
            error.setIcon(qtw.QMessageBox.Critical)
            error.exec_()
            return
        qm = qtw.QMessageBox
        shure = qm.question(self, "Make Shure", f'Is the Target "{str(cb.get_target(SetupWidget.current_profile))}" correct?', qm.Yes | qm.No)
        if shure == qm.Yes:  # the pass is validated by the user
            self.submit.emit(SetupWidget.current_profile)

    @property
    def current_profile(self):
        return self.__current_profile
    @current_profile.setter
    def current_profile(self, value):
        print("setter")
        self.__current_profile = value

    def on_profile_switch(self, profile: str):
        self.__current_profile = profile
        self.__payload_list.refresh()
        self.__target_group_box.reload()

    def profile_change(self):
        self.__payload_list.refresh()
        self.__target_group_box.reload()
        self.__profile_group_box.reload_combobox()

    class PayloadList(qtw.QListWidget):
        def __init__(self, parent):
            self.__parent = parent
            super().__init__()
            self.refresh()

        def refresh(self):
            self.clear()
            for load in cb.get_payloads(self.__parent.current_profile):
                self.addItem(load)

        @qtc.pyqtSlot()
        def add_dir(self):
            path = qtw.QFileDialog.getExistingDirectory()
            if path != "":  # checks if user canceled selection without any select
                cb.add_payload(self.__parent.current_profile, path)
            self.refresh()

        @qtc.pyqtSlot()
        def add_file(self):
            path = qtw.QFileDialog.getOpenFileName()
            print(path[0])
            if Path(path[0]).is_file():
                cb.add_payload(self.__parent.current_profile, path[0])
            self.refresh()

        @qtc.pyqtSlot()
        def remove(self):
            item = self.currentItem()
            if not item == None:
                cb.remove_payload(self.__parent.current_profile, item.text())
            self.refresh()

    class TargetGroupBox(qtw.QGroupBox):
        def __init__(self, parent):
            self.__parent = parent
            super().__init__()
            self.setTitle("Target")

            self.setSizePolicy(qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Maximum))

            self.__target = cb.get_target(self.__parent.current_profile)

            # widgets
            self.__status_label = qtw.QLabel(str(self.__target))
            self.__vstretch_sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Fixed)
            self.__vstretch_sizePolicy.setHorizontalStretch(1)
            self.__status_label.setSizePolicy(self.__vstretch_sizePolicy)
            self.__change_button = qtw.QPushButton("Change")
            self.__change_button.clicked.connect(self.on_change_target)

            # layout
            self.__layout = qtw.QHBoxLayout()
            self.__layout.addWidget(self.__status_label)
            self.__layout.addWidget(self.__change_button)
            self.setLayout(self.__layout)

        def reload(self):
            self.__target = cb.get_target(self.__parent.current_profile)
            self.__status_label.setText(str(self.__target))

        @qtc.pyqtSlot()
        def on_change_target(self):
            path = Path(qtw.QFileDialog.getExistingDirectory(self, "New Target"))
            if not path.is_absolute():
                pass # needs to be checked -> if user cancels the selection process
            elif path.is_dir():
                self.__target = path
                cb.set_target(self.__parent.current_profile, str(self.__target))
                self.reload()
            else:
                error = qtw.QMessageBox()
                error.setWindowTitle("Error")
                error.setText("Path does not exist!")
                error.setIcon(qtw.QMessageBox.Critical)
                error.exec_()

    class ProfileGroupBox(qtw.QGroupBox):
        switch_profile = qtc.pyqtSignal(str)

        def __init__(self, s_profile_reload: qtc.pyqtSignal, setup_widget):
            super().__init__()
            # singnal and slots
            self.s_profile_reload = s_profile_reload
            self.setup_widget = setup_widget

            # set Title
            self.setTitle("Profile")

            # create widgets
            self.__combo_box = qtw.QComboBox()
            self.__vstretch_sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Fixed)
            self.__vstretch_sizePolicy.setHorizontalStretch(1)
            self.__combo_box.setSizePolicy(self.__vstretch_sizePolicy)
            self.__combo_box.currentTextChanged.connect(self.switch_profile)
            self.__edit_button = qtw.QPushButton("Edit")
            self.__edit_button.clicked.connect(self.__on_change)

            # layout stuff
            self.__layout = qtw.QHBoxLayout()
            self.__layout.addWidget(self.__combo_box)
            self.__layout.addWidget(self.__edit_button)

            self.setLayout(self.__layout)

            self.reload_combobox()
        
        def reload_combobox(self): # TODO: set when possible to current profile
            self.__combo_box.currentTextChanged.disconnect(self.switch_profile)
            self.__combo_box.clear()
            self.__combo_box.addItems(cb.get_profile_names())
            self.__combo_box.currentTextChanged.connect(self.switch_profile)

        def __on_change(self):
            change_profile_popup = self.EditProfilesPopup(s_profile_reload=self.s_profile_reload, setup_widget=self.setup_widget)
            change_profile_popup.exec()

        class EditProfilesPopup(qtw.QDialog):
            def __init__(self, s_profile_reload, setup_widget):
                super().__init__()
                # slot / signal
                self.s_profile_reload = s_profile_reload
                self.setup_widget = setup_widget

                self.setWindowTitle("Edit Profiles")

                self.__scroll_area = qtw.QScrollArea()
                self.__scroll_widget = qtw.QWidget()
                self.__scroll_widget.setLayout(self.__get_new_layout())
                self.__scroll_area.setWidget(self.__scroll_widget)
                self.__scroll_area.setWidgetResizable(True)

                self.__layout = qtw.QVBoxLayout()
                self.__layout.addWidget(self.__scroll_area)

                self.setLayout(self.__layout)
            
            def __get_new_layout(self): 
                layout = qtw.QVBoxLayout()
                for profile in cb.get_profile_names():
                    layout.addWidget(self.ProfileWidget(profile, s_profile_reload=self.s_profile_reload, setup_widget=self.setup_widget))
                layout.addStretch()
                return layout

            class ProfileWidget(qtw.QWidget):  # TODO: make it work

                def __init__(self, profile: str, s_profile_reload: qtc.pyqtSignal, setup_widget):
                    super().__init__()
                    # slot / signal
                    self.s_profile_reload = s_profile_reload
                    self.setup_widget = setup_widget

                    self.__profile = profile

                    # create widgets
                    self.__line_edit = qtw.QLineEdit(self.__profile)
                    self.__line_edit.setReadOnly(True)
                    self.__line_edit.returnPressed.connect(self.__on_rename)
                    self.__rename_button = qtw.QPushButton()
                    self.__rename_button.setIcon(qtg.QIcon(str(Path("modules", "addover", "icon_rename.png"))))
                    self.__rename_button.clicked.connect(self.__on_rename)
                    self.__delete_button = qtw.QPushButton()
                    self.__delete_button.setIcon(qtg.QIcon(str(Path("modules", "addover", "icon_trashcan.png"))))
                    self.__delete_button.clicked.connect(self.__on_delete)

                    # layout stuff
                    self.__layout = qtw.QHBoxLayout()
                    self.__layout.setContentsMargins(9, 3, 3, 3)
                    self.__layout.addWidget(self.__line_edit)
                    self.__layout.addWidget(self.__rename_button)
                    self.__layout.addWidget(self.__delete_button)
                    self.setLayout(self.__layout)

                def __on_rename(self):
                    if self.__line_edit.isReadOnly():
                        self.__line_edit.setReadOnly(False)
                    else:
                        self.__line_edit.setReadOnly(True)
                        if not self.__profile == self.__line_edit.text():
                            cb.rename_profile(self.__profile, self.__line_edit.text())
                            if self.__profile == self.setup_widget.current_profile: # rename current profile as well
                                self.setup_widget.current_profile = self.__line_edit.text()
                            self.__profile = self.__line_edit.text()
                            self.s_profile_reload.emit()

                def __on_delete(self):
                    print("delete")
                    # TODO: erverything



class ActionWidget(qtw.QWidget):
    start = qtc.pyqtSignal(str)
    exit = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()

        # connect signal and slots
        self.start.connect(self.on_start)

        # Widgets 
        self.__scroll_label = self.ScrollLabel()

        self.__progress_bar = qtw.QProgressBar()
        self.__progress_bar.setValue(25)

        self.__finish_button = qtw.QPushButton("Finish")
        self.__finish_button.clicked.connect(self.__on_finish)
        self.__finish_button.setDisabled(True)

        self.__layout = qtw.QGridLayout()
        self.__layout.addWidget(self.__scroll_label, 0, 0, 1, 2)
        self.__layout.addWidget(self.__progress_bar, 1, 0, 1, 1)
        self.__layout.addWidget(self.__finish_button, 1, 1, 1, 1)
        self.setLayout(self.__layout)

        # thread
        self.__thread = self.Thread()
        self.__thread.progress.connect(self.__update_progress)

    def __on_finish(self):
        self.exit.emit()

    @qtc.pyqtSlot(str)
    def on_start(self, profile: str):
        self.__scroll_label.set_text("")
        self.__finish_button.setDisabled(True)
        self.__thread.set_profile(profile)
        self.__thread.start()

    @qtc.pyqtSlot(dict)
    def __update_progress(self, do: dict):
        self.__progress_bar.setValue(do["percentage"])
        self.__scroll_label.add_text(do["event-message"])
        if do["finished"]:
            self.__finish_button.setDisabled(False)

            # message
            messagebox = qtw.QMessageBox()
            messagebox.setWindowTitle("Finished")
            messagebox.setText("The process finished.")
            messagebox.setIcon(qtw.QMessageBox.Information)
            messagebox.exec_()

    class Thread(qtc.QThread):
        progress = qtc.pyqtSignal(dict)

        def __init__(self):
            super().__init__()
            self.__profile = ""

        def set_profile(self, profile):
            self.__profile = profile

        def run(self):
            for do in cb.start(self.__profile):
                self.progress.emit(do)

    class ScrollLabel(qtw.QScrollArea):
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
            self.__label.setText(text + "\n" + self.__label.text())

        def set_text(self, text: str):
            self.__label.setText(text)

