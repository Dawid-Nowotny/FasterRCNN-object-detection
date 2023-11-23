import sys
from PyQt5.QtWidgets import QApplication

from .main_window import MainWindow

def initialize_app():
   App = QApplication(sys.argv)
   window = MainWindow()
   window.show()

   sys.exit(App.exec())