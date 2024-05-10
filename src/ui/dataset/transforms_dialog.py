from PyQt5.QtWidgets import QHBoxLayout, QDialog, QSpinBox, QCheckBox, QDoubleSpinBox, QPushButton, QVBoxLayout, QMessageBox, QLabel
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt

from src.ui.spinbox_creator import create_spinbox
from src.ui.show_alert import show_alert
from src.ui.data_shelter import DataShelter

if DataShelter().lang == "pl":
    from src.ui.translations.pl import TRANSFORMS_TITLE, OPERATION_FAILED, ALERT_ERROR
else:
    from src.ui.translations.en import TRANSFORMS_TITLE, OPERATION_FAILED, ALERT_ERROR

class SetTransformsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.finished = False
        self.setWindowIcon(QtGui.QIcon("src\\ui\\resources\\icon.png"))
        self.setWindowTitle(TRANSFORMS_TITLE)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        
        self.__set_checkboxes()
        self.__set_spinboxes()

        self.__ok_button = QPushButton("OK")
        self.__ok_button.clicked.connect(lambda: self.__confirm())

        self.__set_layouts()

    def __set_checkboxes(self):
        self.__resize = QCheckBox("Image resize")

        self.__horizontal_flip = QCheckBox("RandomHorizontalFlip")
        self.__vertical_flip = QCheckBox("RandomVerticalFlip")

        self.__color_jitter = QCheckBox("ColorJitter")

        self.__random_rotation = QCheckBox("RandomRotation")

        self.__normalize = QCheckBox("Normalize")

    def __set_spinboxes(self):
        #Resize
        self.__resize1 = create_spinbox(QSpinBox(), 8, 1024, 1, self.__resize, 224)
        self.__resize2 = create_spinbox(QSpinBox(), 8, 1024, 1, self.__resize, 224)

        #Color Jitter
        self.__brightness = create_spinbox(QDoubleSpinBox(), 0.0, 1.0, 0.01, self.__color_jitter, 0.2)
        self.__contrast = create_spinbox(QDoubleSpinBox(), 0.0, 1.0, 0.01, self.__color_jitter, 0.2)
        self.__saturation = create_spinbox(QDoubleSpinBox(), 0.0, 1.0, 0.01, self.__color_jitter, 0.2)
        self.__hue = create_spinbox(QDoubleSpinBox(), 0.0, 1.0, 0.01, self.__color_jitter, 0.2)

        #Random rotation
        self.__angle = create_spinbox(QSpinBox(), 0, 180, 1, self.__random_rotation, 30)

        #Normalize
        self.__mean1 = create_spinbox(QDoubleSpinBox(), 0.0, 1.0, 0.01, self.__normalize, 0.48)
        self.__mean2 = create_spinbox(QDoubleSpinBox(), 0.0, 1.0, 0.01, self.__normalize, 0.45)
        self.__mean3 = create_spinbox(QDoubleSpinBox(), 0.0, 1.0, 0.01, self.__normalize, 0.40)

        self.__std1 = create_spinbox(QDoubleSpinBox(), 0.0, 1.0, 0.01, self.__normalize, 0.22)
        self.__std2 = create_spinbox(QDoubleSpinBox(), 0.0, 1.0, 0.01, self.__normalize, 0.22)
        self.__std3 = create_spinbox(QDoubleSpinBox(), 0.0, 1.0, 0.01, self.__normalize, 0.22)


    def __set_layouts(self):
        vbox = QVBoxLayout()
        resize_hbox = QHBoxLayout()
        mean_hbox = QHBoxLayout()
        std_hbox = QHBoxLayout()
        
        #Resize
        vbox.addWidget(self.__resize, alignment=QtCore.Qt.AlignCenter)
        resize_hbox.addWidget(self.__resize1)
        resize_hbox.addWidget(self.__resize2)
        vbox.addLayout(resize_hbox)

        #Flips
        vbox.addWidget(self.__horizontal_flip, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__vertical_flip, alignment=QtCore.Qt.AlignCenter)
        
        #Color Jitter
        vbox.addWidget(self.__color_jitter, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__brightness)
        vbox.addWidget(self.__contrast)
        vbox.addWidget(self.__saturation)
        vbox.addWidget(self.__hue)

        #Random rotation
        vbox.addWidget(self.__random_rotation, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__angle)

        #Normalize
        vbox.addWidget(self.__normalize, alignment=QtCore.Qt.AlignCenter)

        mean_hbox.addWidget(self.__mean1)
        mean_hbox.addWidget(self.__mean2)
        mean_hbox.addWidget(self.__mean3)

        std_hbox.addWidget(self.__std1)
        std_hbox.addWidget(self.__std2)
        std_hbox.addWidget(self.__std3)

        vbox.addWidget(QLabel("Mean", self), alignment=QtCore.Qt.AlignCenter)
        vbox.addLayout(mean_hbox)
        vbox.addWidget(QLabel("Std", self), alignment=QtCore.Qt.AlignCenter)
        vbox.addLayout(std_hbox)

        vbox.addWidget(self.__ok_button)

        vbox.setAlignment(QtCore.Qt.AlignCenter)
        container = QtWidgets.QWidget()
        container.setLayout(vbox)

        self.setLayout(vbox)

    def showEvent(self, event):
        super().showEvent(event)
        data_shelter = DataShelter()

        #Transform checkoxes
        self.__resize.setChecked(data_shelter.resize)
        self.__horizontal_flip.setChecked(data_shelter.horizontal_flip)
        self.__vertical_flip.setChecked(data_shelter.vertical_flip)
        self.__color_jitter.setChecked(data_shelter.color_jitter)
        self.__random_rotation.setChecked(data_shelter.random_rotation)
        self.__normalize.setChecked(data_shelter.normalize)

        #Resize
        self.__resize1.layout().itemAt(0).widget().setValue(data_shelter.resize1)
        self.__resize1.layout().itemAt(0).widget().setValue(data_shelter.resize2)

        #Color Jitter
        self.__brightness.layout().itemAt(0).widget().setValue(data_shelter.brightness)
        self.__contrast.layout().itemAt(0).widget().setValue(data_shelter.contrast)
        self.__saturation.layout().itemAt(0).widget().setValue(data_shelter.saturation)
        self.__hue.layout().itemAt(0).widget().setValue(data_shelter.hue)

        #Random rotation
        self.__angle.layout().itemAt(0).widget().setValue(data_shelter.angle)

        #Normalize
        self.__mean1.layout().itemAt(0).widget().setValue(data_shelter.mean1)
        self.__mean2.layout().itemAt(0).widget().setValue(data_shelter.mean2)
        self.__mean3.layout().itemAt(0).widget().setValue(data_shelter.mean3)

        self.__std1.layout().itemAt(0).widget().setValue(data_shelter.std1)
        self.__std2.layout().itemAt(0).widget().setValue(data_shelter.std2)
        self.__std3.layout().itemAt(0).widget().setValue(data_shelter.std3)

    def __confirm(self):
        try:
            data_shelter = DataShelter()

            #Transform checkoxes
            data_shelter.resize = self.__resize.isChecked()
            data_shelter.horizontal_flip = self.__horizontal_flip.isChecked()
            data_shelter.vertical_flip = self.__vertical_flip.isChecked()
            data_shelter.color_jitter = self.__color_jitter.isChecked()
            data_shelter.random_rotation = self.__random_rotation.isChecked()

            #Resize
            data_shelter.resize1 = self.__resize1.layout().itemAt(0).widget().value()
            data_shelter.resize2 = self.__resize2.layout().itemAt(0).widget().value()

            #Color Jitter
            data_shelter.brightness = self.__brightness.layout().itemAt(0).widget().value()
            data_shelter.contrast = self.__contrast.layout().itemAt(0).widget().value()
            data_shelter.saturation = self.__saturation.layout().itemAt(0).widget().value()
            data_shelter.hue = self.__hue.layout().itemAt(0).widget().value()

            #Random rotation
            data_shelter.angle = self.__angle.layout().itemAt(0).widget().value()

            #Normalize
            data_shelter.mean1 = self.__mean1.layout().itemAt(0).widget().value()
            data_shelter.mean2 = self.__mean2.layout().itemAt(0).widget().value()
            data_shelter.mean3 = self.__mean3.layout().itemAt(0).widget().value()

            data_shelter.std1 = self.__std1.layout().itemAt(0).widget().value()
            data_shelter.std2 = self.__std2.layout().itemAt(0).widget().value()
            data_shelter.std3 = self.__std3.layout().itemAt(0).widget().value()

        except Exception as e:
            show_alert(ALERT_ERROR, f"Error: {str(e)}\n{OPERATION_FAILED}", QMessageBox.Critical)
            self.close()

        self.finished = True
        self.close()