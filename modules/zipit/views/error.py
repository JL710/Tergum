from PyQt5 import QtWidgets as qtw


def error_popup(title: str="Error", prompt: str="An error has occurred!"):
    messagebox = qtw.QMessageBox()
    messagebox.setWindowTitle(title)
    messagebox.setText(prompt)
    messagebox.setIcon(qtw.QMessageBox.Critical)
    messagebox.exec_()