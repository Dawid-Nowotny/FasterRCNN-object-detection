from PyQt5.QtWidgets import QMenu, QAction, QMessageBox, QDialog, QLabel, QApplication, QVBoxLayout
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore

import random
import cv2

from .transforms_dialog import SetTransformsDialog
from .loading_dialog import LoadDatasetDialog
from src.ui.data_shelter import DataShelter
from .loader_thread import DataLoaderThread
from src.ui.show_alert import show_alert

from src.data_processing.transforms import create_transforms
from src.utils.get_dataset_sample import get_dataset_sample
from src.utils.clear_cache_directory import clear_cache_directory

class DatasetMenu(QMenu):
    def __init__(self, parent):
        super().__init__("Zbiór danych", parent)
        self.parent = parent
        self.screen_geometry = QApplication.desktop().screenGeometry()

        load_dataset = QAction("Wczytaj zbiór danych", self)
        load_dataset.triggered.connect(lambda: self.__load_dataset())

        set_transforms = QAction("Ustaw transformacje", self)
        set_transforms.triggered.connect(lambda: self.__set_transforms())

        show_sample = QAction("Pokaż przykład ze zbioru", self)
        show_sample.triggered.connect(lambda: self.__show_sample())

        clear_dataset = QAction("Wyczyść załadowany zbiór", self)
        clear_dataset.triggered.connect(lambda: self.__clear_dataset())

        clear_cache = QAction("Usuń pobrane zbiory danych", self)
        clear_cache.triggered.connect(lambda: self.__clear_cache())

        self.addAction(load_dataset)
        self.addAction(set_transforms)
        self.addSeparator()
        self.addAction(show_sample)
        self.addSeparator()
        self.addAction(clear_dataset)
        self.addAction(clear_cache)

    def __load_dataset(self):
        if self.parent.train_loader is not None:
            show_alert("Ostrzeżenie!", "Zbiór danych został już załadowany!\nNie można załadować po raz kolejny!", QMessageBox.Warning)
            return

        dialog = LoadDatasetDialog()
        dialog.exec_()

        if not dialog.finished:
            return
        
        dialog.finished = False

        dialog.lower()
        data_shelter = DataShelter()
        transform = create_transforms(data_shelter.resize, data_shelter.resize1, data_shelter.resize2,
                                      data_shelter.horizontal_flip, data_shelter.vertical_flip, 
                                      data_shelter.color_jitter, data_shelter.brightness, data_shelter.contrast, data_shelter.saturation, data_shelter.hue, 
                                      data_shelter.random_rotation, data_shelter.angle, data_shelter.normalize,
                                      data_shelter.mean1, data_shelter.mean2, data_shelter.mean3, 
                                      data_shelter.std1, data_shelter.std2, data_shelter.std3
                                      )
        self.__init_loader_dialog()

        self.__loader_thread = DataLoaderThread(data_shelter.chosen_year_text, data_shelter.batch_size, transform)
        self.__loader_thread.data_loaded.connect(self.__on_data_loaded)
        self.__loader_thread.finished.connect(self.__on_loading_finished)
        self.__loader_thread.start()

        self.__loader_dialog.exec_()

    def __on_loading_finished(self):
        self.__loader_dialog.close()
        show_alert("Sukces!", "Zbiór danych został załadowany!", QMessageBox.Information)

    def __on_data_loaded(self, data):
        train_loader, val_loader, test_loader = data
        self.parent.train_loader = train_loader
        self.parent.val_loader = val_loader
        self.parent.test_loader = test_loader

    def __on_dialog_close(self, event):
        if self.__loader_thread.isRunning():
            self.__loader_thread.terminate()
            show_alert("Przerwano!", "Ładowanie zbioru danych zostało przerwane!", QMessageBox.Warning, self.__loader_dialog)
            self.__loader_dialog.lower()
            event.accept()

    def __init_loader_dialog(self):
        self.__loader_dialog = QDialog(self)
        self.__loader_dialog.setModal(True)
        self.__loader_dialog.setWindowTitle("Ładowanie zbioru danych")
        self.__loader_dialog.setMinimumSize(200, 100)
        self.__loader_dialog.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.__loader_dialog.closeEvent = self.__on_dialog_close

        gif_label = QLabel(self.__loader_dialog)
        movie = QMovie("src\\ui\\resources\\spinner.gif")
        movie.setScaledSize(QtCore.QSize(120, 120))
        gif_label.setMovie(movie)
        movie.start()

        layout = QVBoxLayout(self.__loader_dialog)
        layout.addWidget(QLabel("Trwa ładowanie...", self.__loader_dialog, alignment=QtCore.Qt.AlignCenter))
        layout.addWidget(gif_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel("Może to zająć od kilku do kilkunastu minut.", self.__loader_dialog, alignment=QtCore.Qt.AlignCenter))
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.__loader_dialog.setLayout(layout)
        self.__loader_dialog.move(int((self.screen_geometry.width() - self.width()) / 2), int((self.screen_geometry.height() - self.height()) / 2 - 100))

    def __set_transforms(self):
        dialog = SetTransformsDialog()
        dialog.exec_()

    def __clear_dataset(self):
        if self.parent.train_loader is None:
            show_alert("Wiadomość!", "Żaden zbiór nie jest załadowany.", QMessageBox.Information)
            return
        
        self.parent.train_loader = None
        self.parent.val_loader = None
        self.parent.test_loader = None
        show_alert("Wiadomość!", "Załadowany zbiór został wyczyszczony.", QMessageBox.Information)

    def __clear_cache(self):
        q = QMessageBox(self)
        q.setGeometry(0, 0, 300, 200)
        q.setWindowTitle('Pytanie')
        q.setText('Czy na pewno chcesz usunąć pobrane zbiory danych?')
        q.setStandardButtons(QMessageBox.NoButton)
        q.addButton('Tak', QMessageBox.YesRole)
        q.addButton('Nie', QMessageBox.NoRole)
        q.move(int((self.screen_geometry.width() - self.width()) / 2) - 75, int((self.screen_geometry.height() - self.height()) / 2) - 50)

        q.exec_()

        if q.clickedButton() and q.clickedButton().text() == 'Tak':
            cleared = clear_cache_directory()
            if cleared:
                show_alert("Sukces!", "Zbiory danych został usunięte.", QMessageBox.Information)
            else:
                show_alert("Błąd!", f"Nie udało się usunąć zbiorów!.", QMessageBox.Warning)
        else:
            return

    def __show_sample(self):
        if self.parent.train_loader is None:
            show_alert("Ostrzeżenie!", "Zbiór danych nie jest załadowany!\nNie można wykonać tej operacji bez załadowanego zbioru!", QMessageBox.Warning)
            return
        
        rand = random.randint(0, len(self.parent.train_loader))

        image = get_dataset_sample(self.parent.train_loader.dataset, rand)

        cv2.imshow('Sample', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()