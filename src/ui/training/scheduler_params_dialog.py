from PyQt5.QtWidgets import QDialog, QCheckBox, QDoubleSpinBox, QPushButton, QVBoxLayout, QLabel, QMessageBox, QSpinBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from src.ui.show_alert import show_alert
from src.ui.data_shelter import DataShelter

class SetSchedulerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QtGui.QIcon("src\\ui\\resources\\icon.png"))
        self.setWindowTitle("Ustaw parametry STEPLR")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedWidth(200)

        self.__conf_button = QPushButton("OK")
        self.__conf_button.clicked.connect(lambda: self.__confirm())

        self.__set_params_type()
        self.__set_layouts()

    def __set_params_type(self):
        self.__step_size = QSpinBox()
        self.__step_size.setMinimum(1)
        self.__step_size.setMaximum(100)

        self.__gamma = QDoubleSpinBox()
        self.__gamma.setMinimum(0.01)
        self.__gamma.setMaximum(1.0)
        self.__gamma.setSingleStep(0.01)
        #self.__gamma.setDecimals(3)

    def __set_layouts(self):
        vbox = QVBoxLayout()

        vbox.addWidget(QLabel("Step size", self), alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__step_size)

        vbox.addWidget(QLabel("Gamma", self), alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__gamma)

        vbox.addWidget(self.__conf_button)

        vbox.setAlignment(QtCore.Qt.AlignCenter)
        container = QtWidgets.QWidget()
        container.setLayout(vbox)

        self.setLayout(vbox)

    def showEvent(self, event):
        super().showEvent(event)
        data_shelter = DataShelter()

        self.__step_size.setValue(data_shelter.step_size)
        self.__gamma.setValue(data_shelter.gamma)

    def __confirm(self):
        try:
            data_shelter = DataShelter()

            data_shelter.step_size = self.__step_size.value()
            data_shelter.gamma = self.__gamma.value()
            
        except Exception as e:
            show_alert("Błąd!", f"Error: {str(e)}\nNie udało się wykonac operacji", QMessageBox.Critical)
            self.close()

        self.close()