from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from src.utils.plot_utils import plot_losses, plot_accuracies

from .data_shelter import DataShelter
if DataShelter().lang == "pl":
    from .translations.pl import TRAINING_RESULTS_TITLE, MAP_TEST, MAP_VAL, MAP_50_TEST, MAP_50_VAL
else:
    from .translations.en import TRAINING_RESULTS_TITLE, MAP_TEST, MAP_VAL, MAP_50_TEST, MAP_50_VAL

class TrainingResultsDialog(QDialog):
    def __init__(self, losses_list, val_losses_list, train_accuracy_list, accuracy_list, val_accuracy_list, test_mAP, val_mAP, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QtGui.QIcon("src\\ui\\resources\\icon.png"))
        self.setWindowTitle(TRAINING_RESULTS_TITLE)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)

        self.__losses_fig = plot_losses(losses_list, val_losses_list)
        self.__accuracy_fig = plot_accuracies(train_accuracy_list, accuracy_list, val_accuracy_list)
        self.__test_mAP, self.__test_mAP_50 = self.fetch_mAP(test_mAP)
        self.__val_mAP, self.__val_mAP_50 = self.fetch_mAP(val_mAP)

        self.__set_layouts()

    def __set_layouts(self):
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        vbox3 = QVBoxLayout()
        hbox = QHBoxLayout()

        vbox1.addStretch()
        vbox1.addWidget(QLabel(MAP_TEST, self), alignment=QtCore.Qt.AlignCenter)
        vbox1.addWidget(QLabel(str(self.__test_mAP), self), alignment=QtCore.Qt.AlignCenter)
        vbox1.addWidget(QLabel(MAP_VAL, self), alignment=QtCore.Qt.AlignCenter)
        vbox1.addWidget(QLabel(str(self.__val_mAP), self), alignment=QtCore.Qt.AlignCenter)

        vbox1.addWidget(QLabel(MAP_50_TEST, self), alignment=QtCore.Qt.AlignCenter)
        vbox1.addWidget(QLabel(str(self.__test_mAP_50), self), alignment=QtCore.Qt.AlignCenter)
        vbox1.addWidget(QLabel(MAP_50_VAL, self), alignment=QtCore.Qt.AlignCenter)
        vbox1.addWidget(QLabel(str(self.__val_mAP_50), self), alignment=QtCore.Qt.AlignCenter)
        vbox1.addStretch()

        canvas_losses = FigureCanvas(self.__losses_fig)
        toolbar_losses = NavigationToolbar(canvas_losses, self)

        vbox2.addWidget(toolbar_losses)
        vbox2.addWidget(canvas_losses)

        canvas_accuracy = FigureCanvas(self.__accuracy_fig)
        toolbar_accuracy = NavigationToolbar(canvas_accuracy, self)

        vbox3.addWidget(toolbar_accuracy)
        vbox3.addWidget(canvas_accuracy)

        hbox.addLayout(vbox1)
        hbox.addItem(QSpacerItem(20, 0))
        hbox.addLayout(vbox2)
        hbox.addLayout(vbox3)

        hbox.setAlignment(QtCore.Qt.AlignCenter)
        container = QtWidgets.QWidget()
        container.setLayout(hbox)

        self.setLayout(hbox)

    def fetch_mAP(self, metrics):
        map_value = metrics['map'].item() * 100 if metrics['map'] is not None else None
        map_50_value = metrics['map_50'].item() * 100 if metrics['map_50'] is not None else None
        return round(map_value, 2), round(map_50_value, 2)