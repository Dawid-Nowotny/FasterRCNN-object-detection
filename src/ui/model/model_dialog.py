from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QListWidget, QPushButton
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from src.ui.config import model_options
from src.ui.styles import LIST_STYLE

class ModelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.finished = False
        self.option = None
        self.setWindowTitle("Lista wyboru modelu")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        screen_geometry = QApplication.desktop().screenGeometry()
        self.move(int((screen_geometry.width() - self.width()) / 2) - 100, int((screen_geometry.height() - self.height()) / 2) - 100)

        self.__list_widget = QListWidget()
        self.__list_widget.addItems(model_options)
        self.__list_widget.setStyleSheet(LIST_STYLE)

        self.__button_ok = QPushButton("OK")
        self.__button_ok.clicked.connect(self.__get_selected_item)

        layout = QVBoxLayout()
        layout.addWidget(self.__list_widget)
        layout.addWidget(self.__button_ok)

        self.setLayout(layout)

    def __get_selected_item(self):
        selected_item = self.__list_widget.currentItem()
        if selected_item and selected_item.text() != "Wybierz opcję":
            self.option = selected_item.text()
        
        self.finished = True
        self.close()