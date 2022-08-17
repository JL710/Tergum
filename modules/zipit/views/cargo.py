from PyQt5 import QtWidgets as qtw


# group box for cargo related widgets
class CargoBox(qtw.QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle("Cargo")
