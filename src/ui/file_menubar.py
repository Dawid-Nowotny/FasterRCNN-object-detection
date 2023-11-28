from PyQt5.QtWidgets import QMenuBar, QAction, QApplication, QMessageBox, QFileDialog
import cv2

from .show_alert import show_alert

class FileMenubar(QMenuBar):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        file_menu = self.addMenu("Plik")

        save_file = QAction("Zapisz aktualnie wyświetlany plik", self)
        save_file.triggered.connect(lambda: self.__save())

        close_app = QAction("Zakończ", self)
        close_app.triggered.connect(lambda: QApplication.quit())

        file_menu.addAction(save_file)
        self.addSeparator()
        file_menu.addAction(close_app)

    def __save(self):
        if self.parent.interface_state == "initial":
            show_alert("Informacja!", "Aktualnie nie wyświetla się żaden plik do zapisania.", QMessageBox.Information)
            return
        
        options = QFileDialog.Options()
        
        if self.parent.interface_state == "display_image":
            file_path, _ = QFileDialog.getSaveFileName(self, "Zapisz obraz", "", "PNG Files (*.png);;JPEG Files (*.jpg)", options=options)
            image_to_save = cv2.cvtColor(self.parent.image, cv2.COLOR_RGB2BGR)
            if file_path:
                cv2.imwrite(file_path, image_to_save)

        elif self.parent.interface_state == "display_video":
            frames_to_save = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in self.parent.frames]

            file_path, _ = QFileDialog.getSaveFileName(self, "Zapisz wideo", "", "MP4 Files (*.mp4)", options=options)

            if file_path:
                height, width, _ = frames_to_save[0].shape
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(file_path, fourcc, 30.0, (width, height))
                for frame in frames_to_save:
                    out.write(frame)
                out.release()