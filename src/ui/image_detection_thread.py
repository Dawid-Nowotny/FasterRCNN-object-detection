from PyQt5.QtCore import QThread, pyqtSignal

from src.image_detection.image_detect_objects import image_detect_objects
from src.image_detection.visualize_detections import visualize_detections

class ImageDetectionThread(QThread):
    detection_finished = pyqtSignal(object)

    def __init__(self, model, image, iou_threshold_detect, score_threshold_detect, use_CUDA_detect):
        super().__init__()
        self.model = model
        self.image = image
        self.iou_threshold_detect = iou_threshold_detect
        self.score_threshold_detect = score_threshold_detect
        self.use_CUDA_detect = use_CUDA_detect
        
    def run(self):
        detections = image_detect_objects(self.model, self.image, self.iou_threshold_detect, self.score_threshold_detect, self.use_CUDA_detect)

        if not detections:
            self.detection_finished.emit(None)
        else:
            image_with_detections = visualize_detections(self.image, detections)
            self.detection_finished.emit(image_with_detections)