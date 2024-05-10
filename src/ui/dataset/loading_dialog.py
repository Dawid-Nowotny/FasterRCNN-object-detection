from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QVBoxLayout, QMessageBox
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt

from src.ui.config import voc_year_options
from src.ui.show_alert import show_alert
from src.ui.data_shelter import DataShelter

if DataShelter().lang == "pl":
    from src.ui.translations.pl import CONFIG_DS_TITLE, LOAD_DS_TITLE, VOC_EDITION, BATCH_TITLE, OPERATION_FAILED, ALERT_ERROR
else:
    from src.ui.translations.en import CONFIG_DS_TITLE, LOAD_DS_TITLE, VOC_EDITION, BATCH_TITLE, OPERATION_FAILED, ALERT_ERROR

class LoadDatasetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QtGui.QIcon("src\\ui\\resources\\icon.png"))
        self.setWindowTitle(CONFIG_DS_TITLE)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        
        self.finished = False

        self.__combo_box_year = QComboBox()
        self.__combo_box_year.addItems(voc_year_options)

        self.__batch_size = QtWidgets.QSpinBox(self)
        self.__batch_size.setRange(1, 128)

        self.__conf_button = QPushButton(LOAD_DS_TITLE)
        self.__conf_button.clicked.connect(lambda: self.__confirm())

        self.__set_layouts()

    def __set_layouts(self):
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(VOC_EDITION, self), alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__combo_box_year)

        vbox.addWidget(QLabel(BATCH_TITLE, self), alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__batch_size)

        vbox.addWidget(self.__conf_button)

        vbox.setAlignment(QtCore.Qt.AlignCenter)
        container = QtWidgets.QWidget()
        container.setLayout(vbox)

        self.setLayout(vbox)

    def showEvent(self, event):
        super().showEvent(event)
        data_shelter = DataShelter()

        self.__combo_box_year.setCurrentIndex(data_shelter.chosen_year_index)
        self.__batch_size.setValue(data_shelter.batch_size)

    def __confirm(self):
        try:
            data_shelter = DataShelter()

            data_shelter.chosen_year_index = self.__combo_box_year.currentIndex()
            data_shelter.chosen_year_text = self.__combo_box_year.currentText()
            data_shelter.batch_size = self.__batch_size.value()
        except Exception as e:
            show_alert(ALERT_ERROR, f"Error: {str(e)}\n{OPERATION_FAILED}", QMessageBox.Critical)
            self.close()

        self.finished = True
        self.close()