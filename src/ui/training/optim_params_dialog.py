from PyQt5.QtWidgets import QDialog, QCheckBox, QDoubleSpinBox, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from src.ui.show_alert import show_alert
from src.ui.data_shelter import DataShelter

class SetOptimDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QtGui.QIcon("src\\ui\\resources\\icon.png"))
        self.setWindowTitle("Ustaw parametry SGD")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedWidth(200)

        self.__conf_button = QPushButton("OK")
        self.__conf_button.clicked.connect(lambda: self.__confirm())

        self.__set_params_type()
        self.__set_layouts()

    def __set_params_type(self):
        self.__lr = QDoubleSpinBox()
        self.__lr.setMinimum(0.0001)
        self.__lr.setMaximum(1.0)
        self.__lr.setSingleStep(0.0001)
        self.__lr.setDecimals(4)

        self.__momentum = QDoubleSpinBox()
        self.__momentum.setMinimum(0.0)
        self.__momentum.setMaximum(1.0)
        self.__momentum.setSingleStep(0.1)

        self.__weight_decay = QDoubleSpinBox()
        self.__weight_decay.setMinimum(0.0)
        self.__weight_decay.setMaximum(0.1)
        self.__weight_decay.setSingleStep(0.0001)
        self.__weight_decay.setDecimals(4)

        self.__dampening = QDoubleSpinBox()
        self.__dampening.setMinimum(0.0)
        self.__dampening.setMaximum(1.0)
        self.__dampening.setSingleStep(0.1) 

        self.__nesterov  = QCheckBox("Nesterov")
        self.__maximize = QCheckBox("Maximize")

    def __set_layouts(self):
        vbox = QVBoxLayout()

        vbox.addWidget(QLabel("Learning rate", self), alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__lr)

        vbox.addWidget(QLabel("Momentum", self), alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__momentum)

        vbox.addWidget(QLabel("Weight_decay", self), alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__weight_decay)

        vbox.addWidget(QLabel("Dampening", self), alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__dampening)

        vbox.addWidget(self.__nesterov)
        vbox.addWidget(self.__maximize)

        vbox.addWidget(self.__conf_button)

        vbox.setAlignment(QtCore.Qt.AlignCenter)
        container = QtWidgets.QWidget()
        container.setLayout(vbox)

        self.setLayout(vbox)

    def showEvent(self, event):
        super().showEvent(event)
        data_shelter = DataShelter()

        self.__lr.setValue(data_shelter.lr)
        self.__momentum.setValue(data_shelter.momentum)
        self.__weight_decay.setValue(data_shelter.weight_decay)
        self.__dampening.setValue(data_shelter.dampening)

        self.__nesterov.setChecked(data_shelter.nesterov)
        self.__maximize.setChecked(data_shelter.maximize)

    def __confirm(self):
        try:
            data_shelter = DataShelter()
            data_shelter.lr = self.__lr.value()
            data_shelter.momentum = self.__momentum.value()
            data_shelter.weight_decay = self.__weight_decay.value()
            data_shelter.dampening = self.__dampening.value()

            data_shelter.nesterov = self.__nesterov.isChecked()
            data_shelter.maximize = self.__maximize.isChecked()

        except Exception as e:
            show_alert("Błąd!", f"Error: {str(e)}\nNie udało się wykonac operacji", QMessageBox.Critical)
            self.close()

        self.close()