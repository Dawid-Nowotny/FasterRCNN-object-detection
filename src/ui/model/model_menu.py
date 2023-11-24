from PyQt5.QtWidgets import QMenu, QAction, QMessageBox, QDialog, QLabel, QApplication, QVBoxLayout, QDesktopWidget, QMenu, QAction, QStyle
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore

from src.ui.show_alert import show_alert
from .model_dialog import ModelDialog
from src.ui.show_alert import show_alert

from src.models.create_fasterrcnn_mini_darknet_nano_head import create_fasterrcnn_mini_darknet_nano_head
from src.models.create_fasterrcnn_mobilenet_v3_large_320_fpn import create_fasterrcnn_mobilenet_v3_large_320_fpn
from src.models.create_fasterrcnn_mobilenet_v3_large_fpn import create_fasterrcnn_mobilenet_v3_large_fpn
from src.models.create_fasterrcnn_resnet50_fpn_v2 import create_fasterrcnn_resnet50_fpn_v2

class ModelMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("Model", parent)
        self.parent = parent

        create_model = QAction("Stwórz model Faster R-CNN", self)
        create_model.triggered.connect(lambda: self.__create_faster_rcnn_model())

        clear_model = QAction("Wyczyść załadowany model", self)
        clear_model.triggered.connect(lambda: self.__clear_model())

        load_model = QAction("Wczytaj wytrenowany model", self)
        load_model.triggered.connect(lambda: self.__load_model())

        save_model = QAction("Zapisz model", self)
        save_model.triggered.connect(lambda: self.__save_model())

        self.addAction(create_model)
        self.addSeparator()
        self.addAction(load_model)
        self.addAction(save_model)
        self.addSeparator()
        self.addAction(clear_model)

    def __create_faster_rcnn_model(self):
        if self.parent.model is not None:
            show_alert("Wiadomość!", "Model jest już załadowany.", QMessageBox.Information)
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
            self.parent.model = create_fasterrcnn_resnet50_fpn_v2()

        show_alert("Sukces!", f"Model {dialog.option} został stworzony!", QMessageBox.Information)

    def __clear_model(self):
        if self.parent.model is None:
            show_alert("Wiadomość!", "Model nie jest załadowany.", QMessageBox.Information)
            return

        self.parent.model = None
        show_alert("Wiadomość!", "Model został wyczyszczony.", QMessageBox.Information)

    def __load_model(self):
        pass

    def __save_model(self):
        pass