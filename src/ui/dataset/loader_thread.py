from PyQt5.QtCore import QThread, pyqtSignal

from src.data_processing.load_PASCAL_VOC import load_PASCAL_VOC

class DataLoaderThread(QThread):
    finished = pyqtSignal()

    def __init__(self, year, batch_size, transform):
        super().__init__()
        self.year = year
        self.batch_size = batch_size
        self.transform = transform

    def run(self):
        train_loader, val_loader, test_loader = load_PASCAL_VOC(self.year, self.batch_size, self.transform)
        self.finished.emit()