from PyQt5.QtWidgets import QDialog, QCheckBox, QDoubleSpinBox, QPushButton, QVBoxLayout, QLabel, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from src.ui.show_alert import show_alert
from src.ui.data_shelter import DataShelter

if DataShelter().lang == "pl":
    from .translations.pl import DETECTION_PARAMS_TITLE, USE_CUDA_TITLE, SCORE_TH_TITLE, IOU_TH_TITLE, OPERATION_FAILED, ALERT_ERROR
else:
    from .translations.en import DETECTION_PARAMS_TITLE, USE_CUDA_TITLE, SCORE_TH_TITLE, IOU_TH_TITLE, OPERATION_FAILED, ALERT_ERROR

class SetDetectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.finished = False
        self.setWindowIcon(QtGui.QIcon("src\\ui\\resources\\icon.png"))
        self.setWindowTitle(DETECTION_PARAMS_TITLE)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedWidth(200)

        self.__conf_button = QPushButton("OK")
        self.__conf_button.clicked.connect(lambda: self.__confirm())

        self.__init_params()
        self.__set_layouts()

    def __init_params(self):
        self.__score_threshold_detect = QDoubleSpinBox()
        self.__score_threshold_detect.setMinimum(0.1)
        self.__score_threshold_detect.setMaximum(1.0)
        self.__score_threshold_detect.setSingleStep(0.05)

        self.__iou_threshold_detect = QDoubleSpinBox()
        self.__iou_threshold_detect.setMinimum(0.1)
        self.__iou_threshold_detect.setMaximum(1.0)
        self.__iou_threshold_detect.setSingleStep(0.05)

        self.__use_CUDA_detect = QCheckBox(USE_CUDA_TITLE)

    def __set_layouts(self):
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(SCORE_TH_TITLE, self), alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__score_threshold_detect)

        vbox.addWidget(QLabel(IOU_TH_TITLE, self), alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.__iou_threshold_detect)

        vbox.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        vbox.addWidget(self.__use_CUDA_detect)

        vbox.addWidget(self.__conf_button)

        vbox.setAlignment(QtCore.Qt.AlignCenter)
        container = QtWidgets.QWidget()
        container.setLayout(vbox)

        self.setLayout(vbox)

    def showEvent(self, event):
        super().showEvent(event)
        data_shelter = DataShelter()

        self.__score_threshold_detect.setValue(data_shelter.score_threshold_detect)
        self.__iou_threshold_detect.setValue(data_shelter.iou_threshold_detect)

        self.__use_CUDA_detect.setChecked(data_shelter.use_CUDA_detect)

    def __confirm(self):
        try:
            data_shelter = DataShelter()

            data_shelter.score_threshold_detect = self.__score_threshold_detect.value()
            data_shelter.iou_threshold_detect = self.__iou_threshold_detect.value()
            data_shelter.use_CUDA_detect = self.__use_CUDA_detect.isChecked()

        except Exception as e:
            show_alert(ALERT_ERROR, f"Error: {str(e)}\n{OPERATION_FAILED}", QMessageBox.Critical)
            self.close()

        self.finished = True
        self.close()