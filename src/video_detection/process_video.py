import cv2

from src.utils.get_screen_resolution import get_screen_resolution
from src.label_colors import label_colors
from src.image_detection.image_detect_objects import image_detect_objects

def process_video(model, video, iou_threshold=0.5, use_cuda=True):
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
    screen_width, screen_height = get_screen_resolution()
    cv2.resizeWindow('Video', screen_width, screen_height)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
            break

        detections = image_detect_objects(model, frame, iou_threshold, use_cuda)

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

        cv2.imshow('Video', frame)

    video.release()
    cv2.destroyAllWindows()