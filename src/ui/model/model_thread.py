from PyQt5.QtCore import QThread, pyqtSignal

from src.models.load_model import load_model

class ModelLoaderThread(QThread):
    model_loaded = pyqtSignal(object)

    def __init__(self, dialog_option, file_name):
        super().__init__()
        self.dialog_option = dialog_option
        self.file_name = file_name
        
    def run(self):
        model = load_model(self.dialog_option, self.file_name)

        if model is None:
            self.model_loaded.emit(None)
        else:
            self.model_loaded.emit(model)
