import cv2

from src.label_colors import label_colors
from src.image_detection.image_detect_objects import image_detect_objects

def process_video(model, video, iou_threshold=0.5, score_threshold=0.6, use_cuda=True):
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
                x, y, w, h = box
                color = label_colors.get(label, (0, 0, 0))
                
                text_x, text_y = x, y - 10
                if text_y < 10:
                    text_y = y + h + 20
                
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                frame = cv2.putText(frame, f'{label} {score}', (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 5)

        frames.append(frame)

    video.release()
    return frames, object_detected