from PyQt5.QtWidgets import QMenuBar, QAction, QApplication, QDialog, QMessageBox

class FileMenubar(QMenuBar):
    def __init__(self):
        super().__init__()

        file_menu = self.addMenu("Plik")

        close_app = QAction("Zakończ", self)
        close_app.triggered.connect(lambda: QApplication.quit())

        self.addSeparator()
        file_menu.addAction(close_app)