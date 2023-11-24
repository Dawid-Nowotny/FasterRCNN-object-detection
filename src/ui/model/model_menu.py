from PyQt5.QtWidgets import QMenu, QAction, QMessageBox, QDialog, QLabel, QApplication, QVBoxLayout, QDesktopWidget
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore

class ModelMenu(QMenu):
    def __init__(self, parent):
        super().__init__("Model", parent)
        self.parent = parent

        create_model = QAction("Wczytaj zbiór danych", self)
        create_model.triggered.connect(lambda: self.__create_model())

        clear_model = QAction("Wczytaj zbiór danych", self)
        clear_model.triggered.connect(lambda: self.__clear_model())

        load_model = QAction("Wczytaj zbiór danych", self)
        load_model.triggered.connect(lambda: self.__load_model())

        save_model = QAction("Wczytaj zbiór danych", self)
        save_model.triggered.connect(lambda: self.__save_model())

        self.addAction(create_model)
        self.addSeparator()

    def __create_model(self):
        pass

    def __clear_model(self):
        pass

    def __load_model(self):
        pass

    def __load_model(self):
        pass

    def __save_model(self):
        pass