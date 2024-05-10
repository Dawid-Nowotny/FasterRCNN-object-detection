from PyQt5.QtWidgets import QMenu, QAction, QMessageBox, QDialog, QLabel, QApplication, QVBoxLayout
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore

import random

from .transforms_dialog import SetTransformsDialog
from .loading_dialog import LoadDatasetDialog
from src.ui.data_shelter import DataShelter
from .loader_thread import DataLoaderThread
from src.ui.show_alert import show_alert

from src.data_processing.transforms import create_transforms
from src.utils.get_dataset_sample import get_dataset_sample
from src.utils.clear_cache_directory import clear_cache_directory

if DataShelter().lang == "pl":
    from src.ui.translations.pl import (
        DATASET_MENU_TITLE, LOAD_DATASET_TITLE, SET_TRANSFORMS_TEXT, DATASET_SAMPLE_TEXT, CLEAR_DATASET_TEXT, CLEAR_CACHE_TEXT, 
        ALREADY_LOADED_TEXT, DATASET_LOADED_TEXT, LOADING_DATASET_INTERRUPTED_TEXT, LOADING_DATASET_TEXT, LOADING_TEXT, TIME_DATASET_TEXT,
        NONE_DATASET_TEXT, CLEARED_DATASET_TEXT, QUESTION_DATASET_DEL, CLEARD_DATASET_TEXT, CLEARD_DATASET_FAILED_TEXT, DATASET_NOT_LOADED_TEXT,
        ALERT_ERROR, ALERT_WARNING, ALERT_SUCCESS, ALERT_MSG, ALERT_INTERRUPTED, ALERT_QUESTION, YES, NO
        )
else:
    from src.ui.translations.en import (
        DATASET_MENU_TITLE, LOAD_DATASET_TITLE, SET_TRANSFORMS_TEXT, DATASET_SAMPLE_TEXT, CLEAR_DATASET_TEXT, CLEAR_CACHE_TEXT, 
        ALREADY_LOADED_TEXT, DATASET_LOADED_TEXT, LOADING_DATASET_INTERRUPTED_TEXT, LOADING_DATASET_TEXT, LOADING_TEXT, TIME_DATASET_TEXT,
        NONE_DATASET_TEXT, CLEARED_DATASET_TEXT, QUESTION_DATASET_DEL, CLEARD_DATASET_TEXT, CLEARD_DATASET_FAILED_TEXT, DATASET_NOT_LOADED_TEXT,
        ALERT_ERROR, ALERT_WARNING, ALERT_SUCCESS, ALERT_MSG, ALERT_INTERRUPTED, ALERT_QUESTION, YES, NO
        )
    
class DatasetMenu(QMenu):
    def __init__(self, parent):
        super().__init__(DATASET_MENU_TITLE, parent)
        self.parent = parent
        self.screen_geometry = QApplication.desktop().screenGeometry()

        load_dataset = QAction(LOAD_DATASET_TITLE, self)
        load_dataset.triggered.connect(lambda: self.__load_dataset())

        set_transforms = QAction(SET_TRANSFORMS_TEXT, self)
        set_transforms.triggered.connect(lambda: self.__set_transforms())

        show_sample = QAction(DATASET_SAMPLE_TEXT, self)
        show_sample.triggered.connect(lambda: self.__show_sample())

        clear_dataset = QAction(CLEAR_DATASET_TEXT, self)
        clear_dataset.triggered.connect(lambda: self.__clear_dataset())

        clear_cache = QAction(CLEAR_CACHE_TEXT, self)
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
            show_alert(ALERT_WARNING, ALREADY_LOADED_TEXT, QMessageBox.Warning)
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
        show_alert(ALERT_SUCCESS, DATASET_LOADED_TEXT, QMessageBox.Information)

    def __on_data_loaded(self, data):
        train_loader, val_loader, test_loader = data
        self.parent.train_loader = train_loader
        self.parent.val_loader = val_loader
        self.parent.test_loader = test_loader

    def __on_dialog_close(self, event):
        if self.__loader_thread.isRunning():
            self.__loader_thread.terminate()
            show_alert(ALERT_INTERRUPTED, LOADING_DATASET_INTERRUPTED_TEXT, QMessageBox.Warning, self.__loader_dialog)
            self.__loader_dialog.lower()
            event.accept()

    def __init_loader_dialog(self):
        self.__loader_dialog = QDialog(self)
        self.__loader_dialog.setModal(True)
        self.__loader_dialog.setWindowTitle(LOADING_DATASET_TEXT)
        self.__loader_dialog.setMinimumSize(200, 100)
        self.__loader_dialog.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.__loader_dialog.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.__loader_dialog.closeEvent = self.__on_dialog_close

        gif_label = QLabel(self.__loader_dialog)
        movie = QMovie("src\\ui\\resources\\spinner.gif")
        movie.setScaledSize(QtCore.QSize(120, 120))
        gif_label.setMovie(movie)
        movie.start()

        layout = QVBoxLayout(self.__loader_dialog)
        layout.addWidget(QLabel(LOADING_TEXT, self.__loader_dialog, alignment=QtCore.Qt.AlignCenter))
        layout.addWidget(gif_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel(TIME_DATASET_TEXT, self.__loader_dialog, alignment=QtCore.Qt.AlignCenter))
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.__loader_dialog.setLayout(layout)
        self.__loader_dialog.move(int((self.screen_geometry.width() - self.width()) / 2), int((self.screen_geometry.height() - self.height()) / 2 - 100))

    def __set_transforms(self):
        dialog = SetTransformsDialog()
        dialog.exec_()

    def __clear_dataset(self):
        if self.parent.train_loader is None:
            show_alert(ALERT_MSG, NONE_DATASET_TEXT, QMessageBox.Information)
            return
        
        self.parent.train_loader = None
        self.parent.val_loader = None
        self.parent.test_loader = None
        show_alert(ALERT_MSG, CLEARED_DATASET_TEXT, QMessageBox.Information)

    def __clear_cache(self):
        q = QMessageBox(self)
        q.setGeometry(0, 0, 300, 200)
        q.setWindowTitle(ALERT_QUESTION)
        q.setText(QUESTION_DATASET_DEL)
        q.setStandardButtons(QMessageBox.NoButton)
        q.addButton(YES, QMessageBox.YesRole)
        q.addButton(NO, QMessageBox.NoRole)
        q.move(int((self.screen_geometry.width() - self.width()) / 2) - 75, int((self.screen_geometry.height() - self.height()) / 2) - 50)

        q.exec_()

        if q.clickedButton() and q.clickedButton().text() == 'Tak' or q.clickedButton().text() == 'Yes':
            cleared = clear_cache_directory()
            if cleared:
                show_alert(ALERT_SUCCESS, CLEARD_DATASET_TEXT, QMessageBox.Information)
            else:
                show_alert(ALERT_ERROR, CLEARD_DATASET_FAILED_TEXT, QMessageBox.Warning)
        else:
            return

    def __show_sample(self):
        if self.parent.train_loader is None:
            show_alert(ALERT_WARNING, DATASET_NOT_LOADED_TEXT, QMessageBox.Warning)
            return
        
        rand = random.randint(0, len(self.parent.train_loader))

        image = get_dataset_sample(self.parent.train_loader.dataset, rand)
        self.parent.image = image
        self.parent.interface_state = "display_image"
        self.parent.update_interface()