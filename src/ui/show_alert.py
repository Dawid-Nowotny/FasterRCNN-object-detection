from PyQt5.QtWidgets import QMessageBox

def show_alert(title, message, icon):
    alert = QMessageBox()
    alert.setWindowTitle(title)
    alert.setText(message)
    alert.setIcon(icon)
    alert.exec_()