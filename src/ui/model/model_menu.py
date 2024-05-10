from PyQt5.QtWidgets import QMenu, QAction, QMessageBox, QMenu, QAction, QFileDialog, QDialog, QLabel, QVBoxLayout, QApplication
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore

from src.ui.show_alert import show_alert
from .model_thread import ModelLoaderThread
from .model_dialog import ModelDialog

from src.models.create_fasterrcnn_mini_darknet_nano_head import create_fasterrcnn_mini_darknet_nano_head
from src.models.create_fasterrcnn_mobilenet_v3_large_320_fpn import create_fasterrcnn_mobilenet_v3_large_320_fpn
from src.models.create_fasterrcnn_mobilenet_v3_large_fpn import create_fasterrcnn_mobilenet_v3_large_fpn
from src.models.create_fasterrcnn_vgg16 import create_fasterrcnn_vgg16

from src.models.save_model import save_model

from src.config import MODELS_PATH

from src.ui.data_shelter import DataShelter
if DataShelter().lang == "pl":
    from src.ui.translations.pl import (
        CREATE_MODEL_TEXT, CLEAR_MODEL_TEXT, LOAD_MODEL_TEXT, SAVE_MODEL_TEXT, MODEL_ALREADY_LOADED_TEXT, MODEL_CREATED_TEXT, MODEL_NOT_LOADED_TEXT,
        MODEL_CLEARED_TEXT, PICK_MODEL_FILE_TEXT, MODEL_LOADED_TEXT, MODEL_BACKBONE_WARN_TEXT, LOADING_MODEL_INTERRUPTED, MODEL_CURRENTLY_LOADING_TEXT,
        LOADING_MODEL_TIME_TEXT, NO_MODEL_TO_SAVE, MODEL_WAS_SAVED_TEXT, ERROR_WHILE_SAVING_MODEL_TEXT,
        ALERT_MSG, ALERT_SUCCESS, ALERT_WARNING, ALERT_INTERRUPTED, ALERT_ERROR, LOADING_TEXT
    )
else:
    from src.ui.translations.en import (
        CREATE_MODEL_TEXT, CLEAR_MODEL_TEXT, LOAD_MODEL_TEXT, SAVE_MODEL_TEXT, MODEL_ALREADY_LOADED_TEXT, MODEL_CREATED_TEXT, MODEL_NOT_LOADED_TEXT,
        MODEL_CLEARED_TEXT, PICK_MODEL_FILE_TEXT, MODEL_LOADED_TEXT, MODEL_BACKBONE_WARN_TEXT, LOADING_MODEL_INTERRUPTED, MODEL_CURRENTLY_LOADING_TEXT,
        LOADING_MODEL_TIME_TEXT, NO_MODEL_TO_SAVE, MODEL_WAS_SAVED_TEXT, ERROR_WHILE_SAVING_MODEL_TEXT,
        ALERT_MSG, ALERT_SUCCESS, ALERT_WARNING, ALERT_INTERRUPTED, ALERT_ERROR, LOADING_TEXT
    )

class ModelMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("Model", parent)
        self.parent = parent

        create_model = QAction(CREATE_MODEL_TEXT, self)
        create_model.triggered.connect(lambda: self.__create_faster_rcnn_model())

        clear_model = QAction(CLEAR_MODEL_TEXT, self)
        clear_model.triggered.connect(lambda: self.__clear_model())

        load_model = QAction(LOAD_MODEL_TEXT, self)
        load_model.triggered.connect(lambda: self.__load_model())

        save_model = QAction(SAVE_MODEL_TEXT, self)
        save_model.triggered.connect(lambda: self.__save_model())

        self.addAction(create_model)
        self.addSeparator()
        self.addAction(load_model)
        self.addAction(save_model)
        self.addSeparator()
        self.addAction(clear_model)

    def __create_faster_rcnn_model(self):
        if self.parent.model is not None:
            show_alert(ALERT_MSG, MODEL_ALREADY_LOADED_TEXT, QMessageBox.Warning)
            return
        
        dialog = ModelDialog(self)
        dialog.exec_()

        if not dialog.finished:
            return
        
        dialog.finished = False

        if dialog.option == "Mini Darknet":
            self.parent.model = create_fasterrcnn_mini_darknet_nano_head()
        elif dialog.option == "Mobilenet_v3 large 320":
            self.parent.model = create_fasterrcnn_mobilenet_v3_large_320_fpn()
        elif dialog.option == "Mobilenet_v3 large":
            self.parent.model = create_fasterrcnn_mobilenet_v3_large_fpn()
        else:
            self.parent.model = create_fasterrcnn_vgg16()
        
        show_alert(ALERT_SUCCESS, MODEL_CREATED_TEXT, QMessageBox.Information)

    def __clear_model(self):
        if self.parent.model is None:
            show_alert(ALERT_MSG, MODEL_NOT_LOADED_TEXT, QMessageBox.Warning)
            return

        self.parent.model = None
        self.parent.show_training_results.setEnabled(False)
        show_alert(ALERT_MSG, MODEL_CLEARED_TEXT, QMessageBox.Information)

    def __load_model(self):
        if self.parent.model is not None:
            show_alert(ALERT_MSG, MODEL_ALREADY_LOADED_TEXT, QMessageBox.Warning)
            return
        
        dialog = ModelDialog(self)
        dialog.exec_()

        if not dialog.finished:
            return
        
        dialog.finished = False

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, PICK_MODEL_FILE_TEXT, MODELS_PATH, "PyTorch Model Files (*.pth)", options=options)
        
        if file_name:
            self.__init_loader_dialog()

            self.__loader_thread = ModelLoaderThread(dialog.option, file_name)
            self.__loader_thread.model_loaded.connect(self.__on_data_loaded)
            self.__loader_thread.start()

            self.__loader_dialog.exec_()

    def __on_data_loaded(self, data):
        model = data
        self.__loader_dialog.close()

        if model is not None:
            self.parent.model = model
            show_alert(ALERT_MSG, MODEL_LOADED_TEXT, QMessageBox.Information)
        else:
            show_alert(ALERT_WARNING, MODEL_BACKBONE_WARN_TEXT, QMessageBox.Warning)

    def __on_dialog_close(self, event):
        if self.__loader_thread.isRunning():
            self.__loader_thread.terminate()
            show_alert(ALERT_INTERRUPTED, LOADING_MODEL_INTERRUPTED, QMessageBox.Warning, self.__loader_dialog)
            self.__loader_dialog.lower()
            event.accept()

    def __init_loader_dialog(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        self.__loader_dialog = QDialog(self)
        self.__loader_dialog.setModal(True)
        self.__loader_dialog.setWindowTitle(MODEL_CURRENTLY_LOADING_TEXT)
        self.__loader_dialog.setMinimumSize(250, 100)
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
        layout.addWidget(QLabel(LOADING_MODEL_TIME_TEXT, self.__loader_dialog, alignment=QtCore.Qt.AlignCenter))
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.__loader_dialog.setLayout(layout)
        self.__loader_dialog.move(int((screen_geometry.width() - self.width()) / 2) - 50, int((screen_geometry.height() - self.height()) / 2 ) - 100)

    def __save_model(self):
        if self.parent.model is None:
            show_alert(ALERT_MSG, NO_MODEL_TO_SAVE, QMessageBox.Warning)
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Model As", MODELS_PATH, "PyTorch Model Files (*.pth)", options=options)

        if file_name:
            value = save_model(self.parent.model, file_name)

            if value is True:
                show_alert(ALERT_MSG, MODEL_WAS_SAVED_TEXT, QMessageBox.Information)
            else:
                show_alert(ALERT_ERROR, ERROR_WHILE_SAVING_MODEL_TEXT, QMessageBox.Critical)