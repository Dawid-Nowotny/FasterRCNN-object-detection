from PyQt5.QtCore import QThread, pyqtSignal

from src.video_detection.process_video import process_video

class VideoDetectionThread(QThread):
    detection_finished = pyqtSignal(object)

    def __init__(self, model, video, iou_threshold_detect, score_threshold_detect, use_CUDA_detect):
        super().__init__()
        self.model = model
        self.video = video
        self.iou_threshold_detect = iou_threshold_detect
        self.score_threshold_detect = score_threshold_detect
        self.use_CUDA_detect = use_CUDA_detect

        
    def run(self):
        frames, object_detected = process_video(self.model, self.video, self.iou_threshold_detect, self.score_threshold_detect, self.use_CUDA_detect)

        if object_detected:
            self.detection_finished.emit(frames)
        else:
            self.detection_finished.emit(None)