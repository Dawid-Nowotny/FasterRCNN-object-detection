from PyQt5.QtWidgets import QDialog, QCheckBox, QDoubleSpinBox, QPushButton, QVBoxLayout, QLabel, QMessageBox, QSpinBox, QSpacerItem, QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from src.ui.show_alert import show_alert
from src.ui.data_shelter import DataShelter

if DataShelter().lang == "pl":
    from src.ui.translations.pl import DETECTION_PARAMS_TEXT, USE_CUDA_TITLE, EPOCH_NUM_TITLE, IOU_TH_TITLE, ALERT_ERROR, OPERATION_FAILED
else:
    from src.ui.translations.en import DETECTION_PARAMS_TEXT, USE_CUDA_TITLE, EPOCH_NUM_TITLE, IOU_TH_TITLE, ALERT_ERROR, OPERATION_FAILED

class SetTrainingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.finished = False
        self.setWindowIcon(QtGui.QIcon("src\\ui\\resources\\icon.png"))
        self.setWindowTitle(DETECTION_PARAMS_TEXT)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedWidth(200)

        self.__conf_button = QPushButton("OK")
        self.__conf_button.clicked.connect(lambda: self.__confirm())

        self.__init_params()
        self.__set_layouts()

    def __init_params(self):
        self.__epochs = QSpinBox()
        self.__epochs.setMinimum(1)
        self.__epochs.setMaximum(100)

        self.__iou_threshold = QDoubleSpinBox()
        self.__iou_threshold.setMinimum(0.1)
        self.__iou_threshold.setMaximum(1.0)
        self.__iou_threshold.setSingleStep(0.05)

        self.__use_CUDA = QCheckBox(USE_CUDA_TITLE)

    def __set_layouts(self):
        vbox = QVBoxLayout()
        
        vbox.addWidget(QLabel(EPOCH_NUM_TITLE, self), alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__epochs)

        vbox.addWidget(QLabel(IOU_TH_TITLE, self), alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__iou_threshold)

        vbox.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        vbox.addWidget(self.__use_CUDA)

        vbox.addWidget(self.__conf_button)

        vbox.setAlignment(QtCore.Qt.AlignCenter)
        container = QtWidgets.QWidget()
        container.setLayout(vbox)

        self.setLayout(vbox)

    def showEvent(self, event):
        super().showEvent(event)
        data_shelter = DataShelter()

        self.__epochs.setValue(data_shelter.epochs)
        self.__iou_threshold.setValue(data_shelter.iou_threshold)

        self.__use_CUDA.setChecked(data_shelter.use_CUDA)


    def __confirm(self):
        try:
            data_shelter = DataShelter()

            data_shelter.epochs = self.__epochs.value()
            data_shelter.iou_threshold = self.__iou_threshold.value()
            data_shelter.use_CUDA = self.__use_CUDA.isChecked()

        except Exception as e:
            show_alert(ALERT_ERROR, f"Error: {str(e)}\n{OPERATION_FAILED}", QMessageBox.Critical)
            self.close()

        self.finished = True
        self.close()