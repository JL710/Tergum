from PyQt5 import QtWidgets as qtw


# group box for the target related widgets
class TargetBox(qtw.QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle("Target")