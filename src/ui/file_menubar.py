from PyQt5.QtWidgets import QMenuBar, QAction, QApplication, QMessageBox, QFileDialog
import cv2

from .show_alert import show_alert

from .data_shelter import DataShelter
if DataShelter().lang == "pl":
    from .translations.pl import FILE_TITLE, SAVE_FILE_TITLE, ICON_INFO_TITLE, ICON_SOURCE_TITLE, CLOSE_TITLE, NO_FILE_TO_SAVE, SAVE_IMG_TITLE, SAVE_VID_TITLE, ALERT_MSG
else:
    from .translations.en import FILE_TITLE, SAVE_FILE_TITLE, ICON_INFO_TITLE, ICON_SOURCE_TITLE, CLOSE_TITLE, NO_FILE_TO_SAVE, SAVE_IMG_TITLE, SAVE_VID_TITLE, ALERT_MSG

class FileMenubar(QMenuBar):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        file_menu = self.addMenu(FILE_TITLE)
        
        save_file = QAction(SAVE_FILE_TITLE, self)
        save_file.triggered.connect(lambda: self.__save())
        
        icon_info = QAction(ICON_INFO_TITLE, self)
        icon_info.triggered.connect(lambda: QMessageBox.information(self, ICON_SOURCE_TITLE, 
        """
        <a href="https://loading.io/icon/">icon 'spinner' from loading.io</a>
        <br><a href="https://icons8.com/">Icons by icons8</a>
        """))
        
        close_app = QAction(CLOSE_TITLE, self)
        close_app.triggered.connect(lambda: QApplication.quit())

        file_menu.addAction(save_file)
        file_menu.addSeparator()
        file_menu.addAction(icon_info)
        file_menu.addSeparator()
        file_menu.addAction(close_app)

    def __save(self):
        if self.parent.interface_state == "initial":
            show_alert(ALERT_MSG, NO_FILE_TO_SAVE, QMessageBox.Warning)
            return
        
        options = QFileDialog.Options()
        
        if self.parent.interface_state == "display_image":
            file_path, _ = QFileDialog.getSaveFileName(self, SAVE_IMG_TITLE, "", "PNG Files (*.png);;JPEG Files (*.jpg)", options=options)
            image_to_save = cv2.cvtColor(self.parent.image, cv2.COLOR_RGB2BGR)
            if file_path:
                cv2.imwrite(file_path, image_to_save)

        elif self.parent.interface_state == "display_video":
            frames_to_save = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in self.parent.frames]

            file_path, _ = QFileDialog.getSaveFileName(self, SAVE_VID_TITLE, "", "MP4 Files (*.mp4)", options=options)

            if file_path:
                height, width, _ = frames_to_save[0].shape
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(file_path, fourcc, 30.0, (width, height))
                for frame in frames_to_save:
                    out.write(frame)
                out.release()