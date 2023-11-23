from PyQt5.QtWidgets import QMenu, QAction, QMessageBox, QDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets

from .transforms_dialog import SetTransformsDialog
from .loading_dialog import LoadDatasetDialog
from src.ui.data_shelter import DataShelter
from .loader_thread import DataLoaderThread

from src.data_processing.transforms import create_transforms

from src.ui.show_alert import show_alert

class DatasetMenu(QMenu):
    def __init__(self, parent):
        super().__init__("Zbiór danych", parent)

        load_dataset = QAction("Wczytaj zbiór danych", self)
        load_dataset.triggered.connect(lambda: self.__load_dataset())

        set_transforms = QAction("Ustaw transformacje", self)
        set_transforms.triggered.connect(lambda: self.__set_transforms())

        clear_dataset = QAction("Wyczyść załadowany zbiór", self)
        clear_dataset.triggered.connect(lambda: self.__clear_dataset())

        show_sample = QAction("Pokaż przykład ze zbioru", self)
        show_sample.triggered.connect(lambda: self.__show_sample())

        self.addAction(load_dataset)
        self.addAction(set_transforms)
        self.addAction(show_sample)
        self.addAction(clear_dataset)

    def __load_dataset(self):
        dialog = LoadDatasetDialog()
        dialog.exec_()

        data_shelter = DataShelter()
        transform = create_transforms()
        
        self.__init_loader_dialog()

        self.__loader_thread = DataLoaderThread(data_shelter.chosen_year_text, data_shelter.batch_size, transform)
        self.__loader_thread.finished.connect(self.__on_loading_finished)
        self.__loader_thread.start()

        self.__loader_dialog.exec_()

    def __on_loading_finished(self):
        self.__loader_dialog.close()
        show_alert("Sukces!", "Zbiór danych został załadowany!", QMessageBox.Information)

    def __on_dialog_close(self, event):
        if self.__loader_thread.isRunning():
            self.__loader_thread.terminate()
            show_alert("Przerwano!", "Ładowanie zbioru danych zostało przerwane!", QMessageBox.Warning)
            event.accept()

    def __init_loader_dialog(self):
        self.__loader_dialog = QDialog(self)
        self.__loader_dialog.setModal(True)
        self.__loader_dialog.setWindowTitle("Proszę czekać")
        self.__loader_dialog.setMinimumSize(200, 100)
        self.__loader_dialog.closeEvent = self.__on_dialog_close

    def __set_transforms(self):
        dialog = SetTransformsDialog()
        dialog.exec_()

    def __clear_dataset(self):
        pass

    def show_sample(self):
        pass