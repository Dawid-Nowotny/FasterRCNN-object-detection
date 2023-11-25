from PyQt5.QtWidgets import QMenu, QAction, QMessageBox, QDialog, QLabel, QApplication, QVBoxLayout, QDesktopWidget, QMenu, QAction, QFileDialog
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore

from src.ui.show_alert import show_alert

class TrainingMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("Trening", parent)
        self.parent = parent

        train_model = QAction("Trenuj model", self)
        train_model.triggered.connect(lambda: self.__run_training())

        set_training_params = QAction("Ustal parametry uczenia", self)
        set_training_params.triggered.connect(lambda: self.__set_training_params())

        self.addAction(train_model)
        self.addAction(set_training_params)

    def __run_training(self):
        pass

    def __set_training_params(self):
        pass