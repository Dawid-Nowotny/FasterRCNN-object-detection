from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QGridLayout, QWidget, QFileDialog
from PyQt5.QtCore import QSize    
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets, QtGui

from .file_menubar import FileMenubar
from src.ui.dataset.dataset_menu import DatasetMenu
from src.ui.model.model_menu import ModelMenu
from src.ui.training.training_menu import TrainingMenu

from .detection_dialog import SetDetectionDialog
from .show_alert import show_alert
from .data_shelter import DataShelter
from .config import WINDOW_WIDTH, WINDOW_HEIGHT
from .styles import MENU_STYLE

from src.image_detection.load_image import load_image
from src.video_detection.load_video import load_video

from src.image_detection.image_detect_objects import image_detect_objects
from src.image_detection.visualize_detections import visualize_detections
from src.video_detection.process_video import process_video

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.train_loader = None
        self.val_loader = None
        self.test_loader = None
        self.model = None
        self.losses_list = None 
        self.val_losses_list = None
        self.accuracy_list = None
        self.val_accuracy_list = None
        self.test_mAP = None
        self.val_mAP = None

        self.__set_geometry()
        self.__init_menubar()
        self.__init_GUI()
        self.__set_layout()
        
    def __set_geometry(self):
        self.showNormal()
        self.setWindowTitle("Future app name")
        self.setWindowIcon(QtGui.QIcon("src\\ui\\resources\\icon.png"))

        screen_size = QApplication.primaryScreen().size()
        self.__window_x = int((screen_size.width() - WINDOW_WIDTH) / 2)
        self.__window_y = int((screen_size.height() - WINDOW_HEIGHT) / 2)

        self.setGeometry(self.__window_x, self.__window_y, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    def __init_menubar(self):
        menubar = FileMenubar()

        self.setMenuBar(menubar)
        menubar.setStyleSheet(MENU_STYLE)

        menubar.addMenu(DatasetMenu(self))
        menubar.addMenu(ModelMenu(self))
        menubar.addMenu(TrainingMenu(self))

    def __init_GUI(self):
        self.__img_button = QPushButton("Rozpoznaj obiekty za zdjęciu", self)
        self.__vid_button = QPushButton("Rozpoznaj obiekty za wideo", self)

        self.__img_button.clicked.connect(lambda: self.__open_file_for_detection("img"))
        self.__vid_button.clicked.connect(lambda: self.__open_file_for_detection("vid"))

    def __set_layout(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        layout.addWidget(self.__img_button)
        layout.addWidget(self.__vid_button)

        self.setCentralWidget(central_widget)

    def __open_file_for_detection(self, type):
        if self.model is None:
            show_alert("Wiadomość!", "Model nie jest załadowany.\nNie można rozpoznać obiektów.", QMessageBox.Information)
            return
        
        dialog = SetDetectionDialog()
        dialog.exec_()

        if not dialog.finished:
            return
        
        dialog.finished = False
        dialog.lower()
        data_shelter = DataShelter()

        options = QFileDialog.Options()
        file_dialog = QFileDialog()

        if type == "img":
            file_path, _ = file_dialog.getOpenFileName(self, "Wybierz obraz", "", "Image Files (*.png *.jpg)", options=options)
            if file_path:
                try:
                    image = load_image(file_path)

                    if image is None:
                        show_alert("Ostrzeżenie!", "Błąd podczas ładowania zdjęcia.", QMessageBox.Warning)
                        return

                    print(image)


                except:
                    show_alert("Ostrzeżenie!", "Niepoprawny plik.", QMessageBox.Warning)

        elif type == "vid":
            file_path, _ = file_dialog.getOpenFileName(self, "Wybierz wideo", "", "Video Files (*.mp4)", options=options)
            if file_path:
                try:
                    video = load_video(file_path)

                    if video is None:
                        show_alert("Ostrzeżenie!", "Błąd podczas ładowania wideo.", QMessageBox.Warning)
                        return
                    
                    print(video)

                except:
                    show_alert("Ostrzeżenie!", "Niepoprawny plik.", QMessageBox.Warning)