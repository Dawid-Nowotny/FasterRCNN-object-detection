from PyQt5.QtWidgets import QMenu, QAction, QMessageBox, QDialog, QLabel, QApplication, QVBoxLayout, QMenu, QAction
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore

from src.ui.show_alert import show_alert
from src.ui.data_shelter import DataShelter

from .training_thread import TrainingThread
from .training_params_dialog import SetTrainingDialog
from .optim_params_dialog import SetOptimDialog
from .scheduler_params_dialog import SetSchedulerDialog

if DataShelter().lang == "pl":
    from src.ui.translations.pl import (
        TRAINING_MENU_NAME, TRAIN_MODEL_TEXT, OPTIM_PARAMS_TEXT, SCHEDULER_PARAMS_TEXT, CANT_START_TRANING_NO_DATASET_TEXT, CANT_START_TRANING_NO_MODEL_TEXT, 
        MODEL_TRAINED_SUCCESSFULLY, TRAINING_INTERRUPTED, MODEL_TRANING_TEXT, MODEL_CURR_TRAINING_TEXT, USER_PATIENCE_TEXT, TIME_TRAINING_TEXT,
        ALERT_WARNING, ALERT_SUCCESS, ALERT_INTERRUPTED
    )
else:
    from src.ui.translations.en import (
        TRAINING_MENU_NAME, TRAIN_MODEL_TEXT, OPTIM_PARAMS_TEXT, SCHEDULER_PARAMS_TEXT, CANT_START_TRANING_NO_DATASET_TEXT, CANT_START_TRANING_NO_MODEL_TEXT, 
        MODEL_TRAINED_SUCCESSFULLY, TRAINING_INTERRUPTED, MODEL_TRANING_TEXT, MODEL_CURR_TRAINING_TEXT, USER_PATIENCE_TEXT, TIME_TRAINING_TEXT,
        ALERT_WARNING, ALERT_SUCCESS, ALERT_INTERRUPTED
    )

class TrainingMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(TRAINING_MENU_NAME, parent)
        self.parent = parent

        train_model = QAction(TRAINING_MENU_NAME, self)
        train_model.triggered.connect(lambda: self.__run_training())

        set_optim_params = QAction(OPTIM_PARAMS_TEXT, self)
        set_optim_params.triggered.connect(lambda: self.__set_optim_params())

        set_scheduler_params = QAction(SCHEDULER_PARAMS_TEXT, self)
        set_scheduler_params.triggered.connect(lambda: self.__set_scheduler_params())

        self.addAction(train_model)
        self.addAction(set_optim_params)
        self.addAction(set_scheduler_params)

    def __run_training(self):
        if self.parent.train_loader is None:
            show_alert(ALERT_WARNING, CANT_START_TRANING_NO_DATASET_TEXT, QMessageBox.Warning)
            return
        
        if self.parent.model is None:
            show_alert(ALERT_WARNING, CANT_START_TRANING_NO_MODEL_TEXT, QMessageBox.Warning)
            return
        
        dialog = SetTrainingDialog()
        dialog.exec_()

        if not dialog.finished:
            return
        
        dialog.finished = False
        dialog.lower()
        data_shelter = DataShelter()

        self.__init_training_dialog()

        self.__training_thread = TrainingThread(
            self.parent.model, self.parent.train_loader, self.parent.val_loader, self.parent.test_loader,
            data_shelter.lr, data_shelter.momentum, data_shelter.weight_decay, 
            data_shelter.dampening, data_shelter.nesterov, data_shelter.maximize,
            data_shelter.step_size, data_shelter.gamma,
            data_shelter.epochs, data_shelter.iou_threshold, data_shelter.use_CUDA
            )
        self.__training_thread.model_trained.connect(self.__on_model_trained)
        self.__training_thread.finished.connect(self.__on_training_finished)
        self.__training_thread.start()

        self.__training_dialog.exec_()

    def __on_training_finished(self):
        self.__training_dialog.close()
        show_alert(ALERT_SUCCESS,MODEL_TRAINED_SUCCESSFULLY, QMessageBox.Information)

    def __on_model_trained(self, data):
        model, losses_list, val_losses_list, train_accuracy_list, test_accuracy_list, val_accuracy_list, test_mAP, val_mAP = data
        self.parent.model = model
        self.parent.losses_list = losses_list 
        self.parent.val_losses_list = val_losses_list
        self.parent.train_accuracy_list = train_accuracy_list
        self.parent.accuracy_list = test_accuracy_list
        self.parent.val_accuracy_list = val_accuracy_list
        self.parent.test_mAP = test_mAP
        self.parent.val_mAP = val_mAP

        self.parent.show_training_results.setEnabled(True)
        
    def __on_dialog_close(self, event):
        if self.__training_thread.isRunning():
            self.__training_thread.terminate()
            show_alert(ALERT_INTERRUPTED, TRAINING_INTERRUPTED, QMessageBox.Warning, self.__training_dialog)
            self.__training_dialog.lower()
            event.accept()

    def __init_training_dialog(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        self.__training_dialog = QDialog(self)
        self.__training_dialog.setModal(True)
        self.__training_dialog.setWindowTitle(MODEL_TRANING_TEXT)
        self.__training_dialog.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.__training_dialog.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.__training_dialog.closeEvent = self.__on_dialog_close
        self.__training_dialog.setFixedWidth(275)

        gif_label = QLabel(self.__training_dialog)
        movie = QMovie("src\\ui\\resources\\spinner.gif")
        movie.setScaledSize(QtCore.QSize(120, 120))
        gif_label.setMovie(movie)
        movie.start()
        
        layout = QVBoxLayout(self.__training_dialog)
        layout.addWidget(QLabel(MODEL_CURR_TRAINING_TEXT, self.__training_dialog, alignment=QtCore.Qt.AlignCenter))
        layout.addWidget(gif_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel(USER_PATIENCE_TEXT, self.__training_dialog, alignment=QtCore.Qt.AlignCenter))
        layout.addWidget(QLabel(TIME_TRAINING_TEXT,
                                self.__training_dialog, alignment=QtCore.Qt.AlignCenter))
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.__training_dialog.setLayout(layout)
        self.__training_dialog.move(int((screen_geometry.width() - self.width()) / 2) - 50, int((screen_geometry.height() - self.height()) / 2) - 100)

    def __set_optim_params(self):
        dialog = SetOptimDialog()
        dialog.exec_()

    def __set_scheduler_params(self):
        dialog = SetSchedulerDialog()
        dialog.exec_()