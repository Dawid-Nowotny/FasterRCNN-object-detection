from PyQt5.QtCore import QThread, pyqtSignal

from src.run_epochs import run_epochs

class TrainingThread(QThread):
    finished = pyqtSignal()
    model_trained = pyqtSignal(object)

    def __init__(self, model, train_loader, val_loader, test_loader, lr, momentum, weight_decay, dampening, nesterov, maximize, step_size, gamma, epochs, iou_threshold, use_CUDA):
        super().__init__()
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        self.lr = lr
        self.momentum = momentum
        self.weight_decay = weight_decay
        self.dampening = dampening
        self.nesterov = nesterov
        self.maximize = maximize
        self.step_size = step_size
        self.gamma = gamma
        self.epochs = epochs
        self.iou_threshold = iou_threshold
        self.use_CUDA = use_CUDA

    def run(self):
        model, losses_list, val_losses_list, accuracy_list, val_accuracy_list, test_mAP, val_mAP = run_epochs(
            self.model, self.train_loader, self.val_loader, self.test_loader,
            self.epochs, self.lr, self.momentum, self.weight_decay, 
            self.dampening, self.nesterov, self.maximize,
            self.step_size, self.gamma, self.iou_threshold, self.use_CUDA
        )
        self.model_trained.emit((model, losses_list, val_losses_list, accuracy_list, val_accuracy_list, test_mAP, val_mAP))
        self.finished.emit()