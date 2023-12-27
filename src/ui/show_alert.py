from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

def show_alert(title, message, icon, parent=None):
    alert = QMessageBox(parent)
    alert.setWindowTitle(title)
    alert.setWindowIcon(QIcon("src\\ui\\resources\\icon.png"))
    alert.setText(message)
    alert.setIcon(icon)
    alert.exec_()