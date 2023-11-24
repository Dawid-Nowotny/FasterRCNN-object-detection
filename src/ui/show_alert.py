from PyQt5.QtWidgets import QMessageBox

def show_alert(title, message, icon, parent=None):
    alert = QMessageBox(parent)
    alert.setWindowTitle(title)
    alert.setText(message)
    alert.setIcon(icon)
    alert.exec_()