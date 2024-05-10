import sys
from PyQt5.QtWidgets import QApplication

from src.utils.setup_directories import setup_directories
from src.ui.data_shelter import DataShelter

def initialize_app(language):
   setup_directories()
   DataShelter().lang = language

   App = QApplication(sys.argv)

   from .main_window import MainWindow
   window = MainWindow()
   window.show()

   sys.exit(App.exec())