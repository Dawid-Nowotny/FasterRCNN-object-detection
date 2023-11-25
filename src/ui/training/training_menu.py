from PyQt5.QtWidgets import QMenu, QAction, QMessageBox, QDialog, QLabel, QApplication, QVBoxLayout, QDesktopWidget, QMenu, QAction, QFileDialog
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore

from src.ui.show_alert import show_alert

from .training_params_dialog import SetTrainingDialog
from .optim_params_dialog import SetOptimDialog
from .scheduler_params_dialog import SetSchedulerDialog

class TrainingMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("Trening", parent)
        self.parent = parent

        train_model = QAction("Trenuj model", self)
        train_model.triggered.connect(lambda: self.__run_training())

        set_optim_params = QAction("Ustal parametry SGD", self)
        set_optim_params.triggered.connect(lambda: self.__set_optim_params())

        set_scheduler_params = QAction("Ustal parametry STEPLR", self)
        set_scheduler_params.triggered.connect(lambda: self.__set_scheduler_params())

        self.addAction(train_model)
        self.addAction(set_optim_params)
        self.addAction(set_scheduler_params)

    def __run_training(self):
        if self.parent.model is None:
            show_alert("Ostrzeżenie!", "Nie można rozpocząć treningu bez stworzonego modelu.", QMessageBox.Warning)
            return
        
        dialog = SetTrainingDialog()
        dialog.exec_()

        if not dialog.finished:
            return
        
        dialog.finished = False

    def __set_optim_params(self):
        dialog = SetOptimDialog()
        dialog.exec_()

    def __set_scheduler_params(self):
        dialog = SetSchedulerDialog()
        dialog.exec_()