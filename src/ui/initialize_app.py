import sys
from PyQt5.QtWidgets import QApplication

from src.utils.setup_directories import setup_directories

from .main_window import MainWindow

def initialize_app():
   setup_directories()

   App = QApplication(sys.argv)
   window = MainWindow()
   window.show()

   sys.exit(App.exec())