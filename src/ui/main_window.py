import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize    
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets, QtGui

from .file_menubar import FileMenubar

from .config import WINDOW_WIDTH, WINDOW_HEIGHT

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__set_geometry()
        self.__init_GUI()
        
    def __set_geometry(self):
        self.showNormal()
        self.setWindowTitle("Future app name")
        self.setWindowIcon(QtGui.QIcon("src\\ui\\resources\\icon.png"))

        screen_size = QApplication.primaryScreen().size()
        self.window_x = int((screen_size.width() - WINDOW_WIDTH) / 2)
        self.window_y = int((screen_size.height() - WINDOW_HEIGHT) / 2)

        self.setGeometry(self.window_x, self.window_y, WINDOW_WIDTH, WINDOW_HEIGHT)

    def __init_GUI(self):
        menubar = FileMenubar()
        self.setMenuBar(menubar)