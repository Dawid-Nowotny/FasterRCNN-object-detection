from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QWidget, QFileDialog, QSizePolicy, QGraphicsScene, QLabel, QGraphicsView
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QMovie, QPixmap, QImage
from PyQt5 import QtCore, QtWidgets, QtGui
import cv2

from .file_menubar import FileMenubar
from src.ui.dataset.dataset_menu import DatasetMenu
from src.ui.model.model_menu import ModelMenu
from src.ui.training.training_menu import TrainingMenu

from .detection_dialog import SetDetectionDialog
from .data_shelter import DataShelter
from .image_detection_thread import ImageDetectionThread
from .video_detection_thread import VideoDetectionThread
from .config import WINDOW_WIDTH, WINDOW_HEIGHT
from .styles import MENU_STYLE
from .show_alert import show_alert

from src.config import EVALUATION_DATA

from src.image_detection.load_image import load_image
from src.video_detection.load_video import load_video

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.interface_state = "initial"

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

        self.image = None
        self.frames = None

        self.__set_geometry()
        self.__init_menubar()
        self.__init_GUI()
        self.__set_layout()
        
    def __set_geometry(self):
        self.showNormal()
        self.setWindowTitle("Faster R-CNN object detector")
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

        self.__clear_display_btn = QPushButton("Wyczyść wyświetlany zdjęcie/film", self)
        self.__clear_display_btn.clicked.connect(lambda: self.__clear_display())

        self.__show_training_results = QPushButton("Pokaż wyniki treningu", self)
        self.__show_training_results.clicked.connect(lambda: print("todo"))

        self.__image_label = QLabel(self)
        self.__image_label.setAlignment(QtCore.Qt.AlignLeft)

        self.__video_scene = QGraphicsScene()
        self.__video_view = QGraphicsView(self)
        self.__video_view.setScene(self.__video_scene)
        self.__video_view.setAlignment(QtCore.Qt.AlignCenter)

    def __set_layout(self):
        self.__img_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__vid_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        central_widget = QWidget()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout(central_widget)
        secRow_vbox = QVBoxLayout()

        vbox.addWidget(self.__img_button)
        vbox.addWidget(self.__vid_button)

        vbox.addWidget(self.__image_label)
        vbox.addWidget(self.__video_view)
        self.__image_label.hide()
        self.__video_view.hide()
        
        secRow_vbox.addWidget(self.__clear_display_btn)
        secRow_vbox.addWidget(self.__show_training_results)

        hbox.addLayout(vbox)
        hbox.addLayout(secRow_vbox)

        self.setCentralWidget(central_widget)

    def update_interface(self):
        if self.interface_state == "display_image":
            height, width, _ = self.image.shape
            bytes_per_line = 3 * width

            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            qt_image = QImage(self.image.data, width, height, bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(qt_image)
            self.__image_label.setPixmap(pixmap)
            self.__image_label.setScaledContents(True)

            self.__image_label.show()
            self.__video_view.hide()
            self.__img_button.hide()
            self.__vid_button.hide()

        elif self.interface_state == "display_video":
            height, width, _ = self.frames[0].shape
            bytes_per_line = 3 * width

            self.frame_index = 0
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.display_next_frame)
            self.timer.start(33)

            pixmap = QPixmap.fromImage(QImage(self.frames[0].data, width, height, bytes_per_line, QImage.Format_RGB888))
            self.__video_scene.addPixmap(pixmap)
            self.__video_view.setScene(self.__video_scene)

            self.__video_view.show()
            self.__image_label.hide()
            self.__img_button.hide()
            self.__vid_button.hide()

    def display_next_frame(self):
        if self.frames and self.frame_index < len(self.frames):
            height, width, _ = self.frames[self.frame_index].shape
            bytes_per_line = 3 * width

            pixmap = QPixmap.fromImage(QImage(self.frames[self.frame_index].data, width, height, bytes_per_line, QImage.Format_RGB888))
            self.__video_scene.clear()
            self.__video_scene.addPixmap(pixmap)
            self.__video_view.setScene(self.__video_scene)
            self.frame_index += 1
        else:
            self.timer.stop()

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
            file_path, _ = file_dialog.getOpenFileName(self, "Wybierz obraz", EVALUATION_DATA, "Image Files (*.png *.jpg)", options=options)

            if file_path:
                try:
                    image = load_image(file_path)

                    if image is None:
                        show_alert("Ostrzeżenie!", "Błąd podczas ładowania zdjęcia.", QMessageBox.Warning)
                        return

                except:
                    show_alert("Ostrzeżenie!", "Niepoprawny plik.", QMessageBox.Warning)
                    return

                self.__init_detection_dialog(self.__on_dialog_close_image)
                self.__image__detection_thread = ImageDetectionThread(self.model, image, data_shelter.iou_threshold_detect, data_shelter.score_threshold_detect, data_shelter.use_CUDA_detect)
                self.__image__detection_thread.detection_finished.connect(self.__on_image_object_detected)
                self.__image__detection_thread.start()

                self.__detection_dialog.exec_()

                if self.image is not None:
                    self.interface_state = "display_image"
                    self.update_interface()

        elif type == "vid":
            file_path, _ = file_dialog.getOpenFileName(self, "Wybierz wideo", EVALUATION_DATA, "Video Files (*.mp4)", options=options)

            if file_path:
                try:
                    video = load_video(file_path)

                    if video is None:
                        show_alert("Ostrzeżenie!", "Błąd podczas ładowania wideo.", QMessageBox.Warning)
                        return
                    
                except:
                    show_alert("Ostrzeżenie!", "Niepoprawny plik.", QMessageBox.Warning)
                    return
                    
                print(video)
                self.__init_detection_dialog(self.__on_dialog_close_video)
                self.__video__detection_thread = VideoDetectionThread(self.model, video, data_shelter.iou_threshold_detect, data_shelter.score_threshold_detect, data_shelter.use_CUDA_detect)
                self.__video__detection_thread.detection_finished.connect(self.__on_video_object_detected)
                self.__video__detection_thread.start()

                self.__detection_dialog.exec_()

                if self.frames is not None:
                    self.interface_state = "display_video"
                    self.frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in self.frames]
                    self.update_interface()

    def __on_image_object_detected(self, data):
        self.image = data
        self.__detection_dialog.close()

        if self.image is None:
            show_alert("Informacja!", "Nie rozpoznano żadnego obiektu na zdjęciu.", QMessageBox.Information)
            return
        
    def __on_video_object_detected(self, data):
        self.frames = data
        self.__detection_dialog.close()

        if self.frames is None:
            show_alert("Informacja!", "Nie rozpoznano żadnego obiektu na całym wideo.", QMessageBox.Information)
            return

    def __on_dialog_close_image(self, event):
        if self.__image__detection_thread.isRunning():
            self.__image__detection_thread.terminate()
            show_alert("Przerwano!", "Detekcja obiektów została przerwana!", QMessageBox.Warning, self.__detection_dialog)
            self.__detection_dialog.lower()
            event.accept()

    def __on_dialog_close_video(self, event):
        if self.__video__detection_thread.isRunning():
            self.__video__detection_thread.terminate()
            show_alert("Przerwano!", "Detekcja obiektów została przerwana!", QMessageBox.Warning, self.__detection_dialog)
            self.__detection_dialog.lower()
            event.accept()

    def __init_detection_dialog(self, function):
        self.__detection_dialog = QDialog(self)
        self.__detection_dialog.setModal(True)
        self.__detection_dialog.setWindowTitle("Detekcja obiektów")
        self.__detection_dialog.setMinimumSize(200, 100)
        self.__detection_dialog.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.__detection_dialog.closeEvent = function

        gif_label = QLabel(self.__detection_dialog)
        movie = QMovie("src\\ui\\resources\\spinner.gif")
        movie.setScaledSize(QtCore.QSize(120, 120))
        gif_label.setMovie(movie)
        movie.start()

        layout = QVBoxLayout(self.__detection_dialog)
        layout.addWidget(QLabel("Trwa detekcja...", self.__detection_dialog, alignment=QtCore.Qt.AlignCenter))
        layout.addWidget(gif_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel("Może to zająć do kilku do kilkunastu minut", self.__detection_dialog, alignment=QtCore.Qt.AlignCenter))
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.__detection_dialog.setLayout(layout)

    def __clear_display(self):
        self.interface_state = "initial"

        self.__image_label.hide()
        self.__video_view.hide()
        self.__img_button.show()
        self.__vid_button.show()

        self.image = None
        self.frames = None