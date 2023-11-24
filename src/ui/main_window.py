import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize    
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets, QtGui

from .file_menubar import FileMenubar
from src.ui.dataset.dataset_menu import DatasetMenu
from src.ui.model.model_menu import ModelMenu

from .config import WINDOW_WIDTH, WINDOW_HEIGHT
from .styles import MENU_STYLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.train_loader = None
        self.val_loader = None
        self.test_loader = None
        self.model = None

        self.__set_geometry()
        self.__init_GUI()
        self.__init_menubar()
        
    def __set_geometry(self):
        self.showNormal()
        self.setWindowTitle("Future app name")
        self.setWindowIcon(QtGui.QIcon("src\\ui\\resources\\icon.png"))

        screen_size = QApplication.primaryScreen().size()
        self.__window_x = int((screen_size.width() - WINDOW_WIDTH) / 2)
        self.__window_y = int((screen_size.height() - WINDOW_HEIGHT) / 2)

        self.setGeometry(self.__window_x, self.__window_y, WINDOW_WIDTH, WINDOW_HEIGHT)

    def __init_GUI(self):
        pass

    def __init_menubar(self):
        menubar = FileMenubar()

        self.setMenuBar(menubar)
        menubar.setStyleSheet(MENU_STYLE)

        menubar.addMenu(DatasetMenu(self))
        menubar.addMenu(ModelMenu(self))