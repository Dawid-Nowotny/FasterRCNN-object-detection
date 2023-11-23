from PyQt5.QtWidgets import QMenu, QAction, QApplication, QDialog, QMessageBox

from .transforms_dialog import SetTransformsDialog

from src.data_processing.transforms import create_transforms

class DatasetMenu(QMenu):
    def __init__(self, parent):
        super().__init__("Zbiór danych", parent)

        load_dataset = QAction("Wczytaj zbiór danych", self)
        load_dataset.triggered.connect(lambda: self.__load_dataset())

        set_transforms = QAction("Ustaw transformacje", self)
        set_transforms.triggered.connect(lambda: self.__set_transforms())

        self.addAction(load_dataset)
        self.addAction(set_transforms)

    def __load_dataset(self):
        pass

    def __set_transforms(self):
        dialog = SetTransformsDialog()
        dialog.exec_()
 
        data_transforms = create_transforms()
        print(data_transforms)