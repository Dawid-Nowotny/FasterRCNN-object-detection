import torch
import cv2

from src.label_colors import label_colors
from src.image_detection.image_detect_objects import image_detect_objects

def process_video(model, video, iou_threshold=0.5, score_threshold=0.6, use_cuda=True):
    device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")
    model.eval()
    model.to(device)
    
    frames = []
    object_detected = False

    while True:
        ret, frame = video.read()
        if not ret:
            break

        detections = image_detect_objects(model, frame, iou_threshold, score_threshold, use_cuda)

        if detections:
            object_detected = True

        for detection in detections:
            label = detection['label']
            box = detection['bounding_box']
            score = detection['score']

            if box is not None:
                x, y, x2, y2 = box
                color = label_colors.get(label, (0, 0, 0))
                
                text_x, text_y = x, y - 10
                if text_y < 10:
                    text_y = y2 + 20
                
                frame = cv2.rectangle(frame, (x, y), (x2, y2), color, 2)
                frame = cv2.putText(frame, f'{label} {score}', (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 5)

        frames.append(frame)

    video.release()
    return frames, object_detected