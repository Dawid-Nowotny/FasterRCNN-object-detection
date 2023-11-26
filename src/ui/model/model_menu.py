from PyQt5.QtWidgets import QMenu, QAction, QMessageBox, QMenu, QAction, QFileDialog

from src.ui.show_alert import show_alert
from .model_dialog import ModelDialog

from src.models.create_fasterrcnn_mini_darknet_nano_head import create_fasterrcnn_mini_darknet_nano_head
from src.models.create_fasterrcnn_mobilenet_v3_large_320_fpn import create_fasterrcnn_mobilenet_v3_large_320_fpn
from src.models.create_fasterrcnn_mobilenet_v3_large_fpn import create_fasterrcnn_mobilenet_v3_large_fpn
from src.models.create_fasterrcnn_resnet50_fpn_v2 import create_fasterrcnn_resnet50_fpn_v2

from src.models.load_model import load_model
from src.models.save_model import save_model

from src.config import MODELS_PATH

class ModelMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("Model", parent)
        self.parent = parent

        create_model = QAction("Stwórz model Faster R-CNN", self)
        create_model.triggered.connect(lambda: self.__create_faster_rcnn_model())

        clear_model = QAction("Wyczyść załadowany model", self)
        clear_model.triggered.connect(lambda: self.__clear_model())

        load_model = QAction("Wczytaj model z pliku", self)
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
        if self.parent.model is not None:
            show_alert("Wiadomość!", "Model jest już załadowany.", QMessageBox.Information)
            return
        
        dialog = ModelDialog(self)
        dialog.exec_()

        if not dialog.finished:
            return
        
        dialog.finished = False

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz plik modelu", MODELS_PATH, "PyTorch Model Files (*.pth)", options=options)
        
        if file_name:
            model = load_model(dialog.option, file_name)

            if model is None:
                show_alert("Ostrzeżenie!", "Błąd podczas ładowania modelu, upewnij się, że:\
                            \n- ładujesz model Faster R-CNN z odpowiednim backbonem \
                            \n- jest on wytrenowany.", QMessageBox.Warning)
                return

            self.parent.model = model
            show_alert("Wiadomość!", "Model został załadowany.", QMessageBox.Information)

    def __save_model(self):
        if self.parent.model is None:
            show_alert("Wiadomość!", "Nie ma modelu do zapisania.", QMessageBox.Information)
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Model As", MODELS_PATH, "PyTorch Model Files (*.pth)", options=options)

        if file_name:
            value = save_model(self.parent.model, file_name)

            if value is True:
                show_alert("Wiadomość!", "Model został pomyślnie zapisany.", QMessageBox.Information)
            else:
                show_alert("Błąd!", "Błąd podczas zapisu modelu.", QMessageBox.Critical)